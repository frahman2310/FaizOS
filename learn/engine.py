#!/usr/bin/env python3
"""The shared layer (docs/research/structures/INTEGRATED.md section 2): one recall queue, one results log,
one dashboard, one daily plan. Personal data lives in learn/data/ (git-ignored).

    uv run engine.py start 2026-09-28        # set day 1 of week 1 (once)
    uv run engine.py today                   # what today holds: due cards, the unit(s) scheduled
    uv run engine.py due                     # due recall cards, oldest first
    uv run engine.py review CARD_ID RATING   # 1 again, 2 hard, 3 good, 4 easy
    uv run engine.py done UNIT_ID SCORE --predicted P [--cold]   # record a unit or its 7-day cold check
    uv run engine.py dashboard               # per skill: main score, 7-day cold score, prediction gap
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
UNITS = HERE / "units"
SKILLS = ["code", "llm", "production", "evaluation", "design"]
START_WEEK = {"code": 1, "llm": 1, "production": 3, "evaluation": 4, "design": 6}
BAR = {"code": 90, "llm": 90, "production": 90, "evaluation": 70, "design": 70}   # INTEGRATED section 3
WEEK = {   # weekday (0 = Mon) -> skills with a unit that day, from week 8; earlier weeks skip unstarted skills
    0: ["evaluation"], 1: ["code", "llm"], 2: ["design"], 3: ["code"], 4: ["production"], 5: ["design"], 6: [],
}
EARLY_LLM_EXTRA = 3                                 # before week 8: a second LLM unit on Thursday


def load(name, default):
    f = DATA / name
    return json.loads(f.read_text()) if f.exists() else default


def save(name, obj):
    DATA.mkdir(exist_ok=True)
    (DATA / name).write_text(json.dumps(obj, indent=1, default=str))


def scheduler():
    from fsrs import Scheduler
    return Scheduler(desired_retention=0.9, learning_steps=(), relearning_steps=())


def unit_files(skill):
    return sorted((UNITS / skill).glob("*.md"))


def unit_id(path):
    m = re.search(r"(?m)^id:\s*(\S+)", path.read_text())
    return m.group(1) if m else path.stem


def cards_of(path):
    text = path.read_text()
    block = text.split("## Cards", 1)[1] if "## Cards" in text else ""
    skill = re.search(r"(?m)^skill:\s*(\S+)", text).group(1)
    out = []
    for i, m in enumerate(re.finditer(r"(?m)^- Q: (.+?) \| A: (.+)$", block), 1):
        out.append({"id": f"{unit_id(path)}.{i}", "skill": skill, "q": m.group(1).strip(), "a": m.group(2).strip()})
    return out


def week_no(today=None):
    start = load("state.json", {}).get("start")
    if not start:
        sys.exit("No start date yet: run  uv run engine.py start YYYY-MM-DD")
    today = today or dt.date.today()
    return (today - dt.date.fromisoformat(start)).days // 7 + 1


def cmd_start(a):
    st = load("state.json", {})
    st["start"] = a.date
    save("state.json", st)
    print(f"Week 1 starts {a.date}.")


def next_unit(skill, results):
    done = {r["unit"] for r in results if r["kind"] == "session" and r["score"] >= BAR[skill]}
    for f in unit_files(skill):
        if unit_id(f) not in done:
            return f
    return None


def cmd_today(a):
    w = week_no()
    today = dt.date.today()
    results = load("results.json", [])
    skills = [s for s in WEEK[today.weekday()] if w >= START_WEEK[s]]
    if w < 8 and today.weekday() == EARLY_LLM_EXTRA and w >= START_WEEK["llm"]:
        skills.append("llm")
    print(f"Week {w}, {today:%A %d %b}")
    print(f"Recall queue: {len(due_cards())} due (about 10 minutes)")
    colds = [r for r in results if r["kind"] == "session" and r.get("cold_due") == str(today)]
    for r in colds:
        print(f"7-day cold check due: {r['unit']}")
    if not skills:
        print("No unit today." + (" Saturday whole task." if today.weekday() == 5 and w >= 8 else ""))
    for s in skills:
        f = next_unit(s, results)
        print(f"Unit: {s} → {f.relative_to(HERE) if f else '(no unit prepared yet)'}")


def due_cards():
    from fsrs import Card
    state = load("queue.json", {})
    now = dt.datetime.now(dt.timezone.utc)
    return sorted((cid for cid, c in state.items() if Card.from_dict(c["fsrs"]).due <= now),
                  key=lambda cid: state[cid]["fsrs"]["due"])


def cmd_due(a):
    state = load("queue.json", {})
    for cid in due_cards():
        print(f"{cid}  [{state[cid]['skill']}]  {state[cid]['q']}")


def cmd_review(a):
    from fsrs import Card, Rating
    state = load("queue.json", {})
    c = state[a.card]
    card, _ = scheduler().review_card(Card.from_dict(c["fsrs"]), Rating(a.rating))
    c["fsrs"] = card.to_dict()
    save("queue.json", state)
    print(f"{a.card} next due {card.due:%Y-%m-%d}")


def cmd_done(a):
    from fsrs import Card
    results = load("results.json", [])
    path = next(p for s in SKILLS for p in unit_files(s) if unit_id(p) == a.unit)
    skill = path.parent.name
    today = dt.date.today()
    r = {"date": str(today), "skill": skill, "unit": a.unit, "score": a.score, "predicted": a.predicted,
         "kind": "cold" if a.cold else "session"}
    if not a.cold:
        r["cold_due"] = str(today + dt.timedelta(days=7))
        state = load("queue.json", {})
        for c in cards_of(path):                      # the unit's cards join the one queue
            state.setdefault(c["id"], {**c, "fsrs": Card().to_dict()})
        save("queue.json", state)
    results.append(r)
    save("results.json", results)
    print(f"Recorded {a.unit}: {a.score} (predicted {a.predicted}).")


def cmd_dashboard(a):
    results = load("results.json", [])
    print(f"{'skill':12}{'main':>6}{'cold':>6}{'gap':>6}  status")
    for s in SKILLS:
        rs = [r for r in results if r["skill"] == s]
        sess = [r for r in rs if r["kind"] == "session"]
        cold = [r for r in rs if r["kind"] == "cold"]
        gaps = [abs(r["score"] - r["predicted"]) for r in rs[-4:] if r.get("predicted") is not None]
        main = sess[-1]["score"] if sess else None
        c = cold[-1]["score"] if cold else None
        mastered = len(sess) >= 2 and all(r["score"] >= BAR[s] for r in sess[-2:]) and c is not None and c >= BAR[s]
        status = "mastered" if mastered else ("not started" if not rs else f"bar {BAR[s]}")
        fmt = lambda v: f"{v:>6}" if v is not None else f"{'-':>6}"
        print(f"{s:12}{fmt(main)}{fmt(c)}{fmt(round(sum(gaps) / len(gaps)) if gaps else None)}  {status}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("start").add_argument("date")
    sub.add_parser("today")
    sub.add_parser("due")
    p = sub.add_parser("review"); p.add_argument("card"); p.add_argument("rating", type=int, choices=[1, 2, 3, 4])
    p = sub.add_parser("done"); p.add_argument("unit"); p.add_argument("score", type=int)
    p.add_argument("--predicted", type=int, required=True); p.add_argument("--cold", action="store_true")
    sub.add_parser("dashboard")
    a = ap.parse_args()
    globals()[f"cmd_{a.cmd}"](a)
