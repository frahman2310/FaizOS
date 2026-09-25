#!/usr/bin/env python3
"""The shared layer (docs/research/structures/INTEGRATED.md section 2). Personal data in learn/data/ (git-ignored).

    uv run engine.py today                       this sitting: recall, next unit(s), cold checks, other sessions
                                                 (sittings follow the week order, not calendar days: C47)
    uv run engine.py due                         today's recall cards: capped, interleaved across skills
    uv run engine.py review CARD RATING          he grades himself: 1 wrong, 2 right with effort, 3 right, 4 easy
    uv run engine.py predict UNIT P [--cold]     his predicted score, asked BEFORE the first scored step
    uv run engine.py done UNIT --step "Trace=0.8" --step "Change=1" ... [--confident-wrong N] [--cold]
    uv run engine.py close UNIT "Next time I see X, I do Y"     his Close line joins the queue
    uv run engine.py outside SKILL SCORE "what"  an outside task (ScaleDojo lab, new product, hidden tests)
    uv run engine.py dashboard                   per skill: main, cold, prediction gap, alarms

Scoring (INTEGRATED section 3, after the 2026-09-25 audits): only steps with Kind: scored count, all of which
come after he has been shown and has practised. Each scored step is 0 to 1 (a right answer after a hint is 0.5,
an answer given to him is 0). Pass = mean of scored steps >= the skill's bar. Evaluation may also record
kappa / missed_fail / traces; design may record rubric / numbers_met (their pass rules then apply).
A miss is followed by corrective teaching and the unit's '## Retry' item (Bloom and Guskey); a second miss
moves to a parallel unit. Confidence is recorded for calibration only and never lowers his level.
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
RECALL_CAP = 20                     # about 10 minutes at about 30 seconds a card
BACKLOG_PAUSE = 40                  # due backlog above this: new cards wait (llm-behaviour.md cap rule)
FLOOR_GAP = 20                      # floor = bar minus 20 points


def passes(skill, s, scored):
    """s: {step: value}; scored: the unit's scored step names (INTEGRATED section 3)."""
    if skill == "evaluation" and "kappa" in s:
        return s["kappa"] >= 0.70 and s.get("missed_fail", 1) == 0 and s.get("traces", 0) >= 24
    if skill == "design" and "rubric" in s:
        return s["rubric"] >= 70 and s.get("numbers_met", 0) >= 1
    vals = [s[k] for k in scored if k in s]
    return bool(vals) and len(vals) == len(scored) and sum(vals) / len(vals) * 100 >= BAR[skill]


BAR = {"code": 90, "llm": 90, "production": 90, "evaluation": 80, "design": 70}    # percent of scored steps


# ---------- storage ----------
def load(name, default):
    f = DATA / name
    return json.loads(f.read_text()) if f.exists() else default


def save(name, obj):
    DATA.mkdir(exist_ok=True)
    (DATA / name).write_text(json.dumps(obj, indent=1, default=str))


def fail(msg):
    sys.exit(f"error: {msg}")


# ---------- units ----------
def unit_files(skill):
    return sorted(p for p in (UNITS / skill).glob("*.md"))


def meta(path):
    text = path.read_text()
    head = text.split("\n## ", 1)[0]
    m = dict(re.findall(r"(?m)^(\w[\w ]*):\s*(.*)$", head))
    return {"id": m.get("id", path.stem), "skill": path.parent.name, "level": int(m.get("level", "1")),
            "scored": [x.strip() for x in m.get("scored", "").split(",") if x.strip()],
            "parallel_of": m.get("parallel_of", "").strip(), "path": path}


def find_unit(uid):
    for s in SKILLS:
        for p in unit_files(s):
            if meta(p)["id"] == uid:
                return meta(p)
    fail(f"no unit with id '{uid}'")


def cards_of(path):
    """'- Q: ... | A: ...' lines; variants separated by ' || ' (a different surface each review)."""
    text = path.read_text()
    block = text.split("## Cards", 1)[1].split("\n## ", 1)[0] if "## Cards" in text else ""
    uid, skill = meta(path)["id"], meta(path)["skill"]
    out = []
    for i, line in enumerate(re.findall(r"(?m)^- (Q: .+)$", block), 1):
        variants = [dict(zip(("q", "a"), [x.strip() for x in re.split(r"\s*\|\s*A:\s*", v.strip()[3:], 1)]))
                    for v in line.split(" || ")]
        out.append({"id": f"{uid}.{i}", "skill": skill, "variants": variants})
    return out


# ---------- calendar ----------
def week_no(today=None):
    """Weeks count sittings, not calendar days (C47: "days don't matter"): 7 slots make a week."""
    return load("state.json", {}).get("slot", 0) // 7 + 1


def current_slot():
    """(slot, units, other): the next slot with a unit; other sessions of skipped empty slots come along."""
    k, other = load("state.json", {}).get("slot", 0), []
    for k in range(k, k + 14):
        units, o = plan(k % 7, k // 7 + 1)
        other += [x for x in o if x not in other]
        if units:
            return k, units, other
    return k, [], other


def plan(wd, w):
    """(units by skill, other sessions) for slot wd (0-6, the INTEGRATED 5 week order), week w."""
    on = lambda s: w >= START_WEEK[s]
    units = {0: ["evaluation"], 1: ["code", "llm"], 2: ["design"], 3: ["code"], 4: ["production"], 5: ["design"], 6: []}[wd]
    if w <= 8 and wd == 3:
        units = units + ["llm"]                       # two LLM units a week up to and including week 8
    units = [s for s in units if on(s)]
    other = []
    if on("evaluation") and wd in (0, 3, 6):
        other.append("evaluation rapid round (8 min)")
    if on("design") and wd in (4, 6):
        other.append("design drill (15 min): write your answer, then compare with a weak and a strong expert answer")
    if wd == 5 and w >= 8:
        other.append("whole task: " + ["evaluation analysis", "ScaleDojo design lab from the brief",
                                       "production mock incident", "code: steer the AI on the FBR tax assistant"][(w - 8) % 4])
    for s in SKILLS:
        if w == START_WEEK[s] and wd == 0 and s in ("evaluation", "production"):
            other.append(f"{s} placement check before the first unit")
    return units, other


# ---------- results and mastery ----------
def sessions(results, skill=None):
    """Taught attempts at a unit: the first session and, after a miss, its retry."""
    return [r for r in results if r["kind"] in ("session", "retry") and (skill is None or r["skill"] == skill)]


def skill_state(results, skill):
    """Walk the skill's sessions in order: rung moves and mastery (INTEGRATED 2.5)."""
    rung, streak_up, streak_down = 1, [], 0
    for r in sessions(results, skill):
        below_floor = r["score"] < BAR[skill] - FLOOR_GAP          # confidence never demotes (audit-pedagogy)
        if r["passed"]:
            streak_up = [u for u in streak_up if u != r["unit"]] + [r["unit"]]
            streak_down = 0
            if len(streak_up) >= 2:
                rung, streak_up = rung + 1, []
        else:
            streak_up = []
            streak_down = streak_down + 1 if below_floor else 0
            if streak_down >= 2:
                rung, streak_down = max(1, rung - 1), 0
    passed_units = []
    for r in sessions(results, skill):
        passed_units = [u for u in passed_units if u != r["unit"]] + [r["unit"]] if r["passed"] else []
    last_two = passed_units[-2:]
    colds = {r["unit"]: r for r in results if r["kind"] == "cold" and r["skill"] == skill}
    mastered = len(last_two) == 2 and all(u in colds and colds[u]["passed"] for u in last_two)
    return rung, mastered


def next_unit(skill, results):
    """(path, note). A missed unit gets corrective teaching and its Retry item once; a second miss moves to a
    parallel unit (new surface, same skill)."""
    sess = sessions(results, skill)
    done_ok = {r["unit"] for r in sess if r["passed"]}
    retried = {r["unit"] for r in results if r["kind"] == "retry"}
    missed = {r["unit"] for r in sess if not r["passed"]} - done_ok
    for p in unit_files(skill):
        m = meta(p)
        if m["id"] in done_ok:
            continue
        if m["id"] in missed and m["id"] not in retried:
            return p, "RETRY: re-teach with its Help blocks and the show steps he missed, then send its ## Retry item"
        if m["id"] in missed:
            par = [meta(q) for q in unit_files(skill) if meta(q)["parallel_of"] == m["id"]]
            fresh = [q for q in par if q["id"] not in done_ok | missed]
            if fresh:
                return fresh[0]["path"], None
            return None, f"{m['id']} was missed twice: prepare a parallel unit (new surface) before the next {skill} slot"
        if m["parallel_of"] and m["parallel_of"] not in missed:
            continue                          # parallel units are only served after a second miss
        return p, None
    return None, f"no {skill} unit prepared yet"


# ---------- recall queue ----------
def scheduler():
    from fsrs import Scheduler
    return Scheduler(desired_retention=0.9, learning_steps=(), relearning_steps=())


def due_cards(limit=RECALL_CAP):
    """Due cards, capped, interleaved: round-robin across skills, then across units within a skill."""
    from fsrs import Card
    q = load("queue.json", {})
    now = dt.datetime.now(dt.timezone.utc)
    due = sorted((cid for cid, c in q.items() if Card.from_dict(c["fsrs"]).due <= now), key=lambda c: q[c]["fsrs"]["due"])
    by_skill = {}
    for cid in due:
        by_skill.setdefault(q[cid]["skill"], {}).setdefault(cid.rsplit(".", 1)[0], []).append(cid)
    lanes = [[cid for grp in zip_longest_units(units) for cid in grp] for units in by_skill.values()]
    mixed = [cid for group in zip_longest(*lanes) for cid in group if cid]
    return mixed[:limit], len(due)


def zip_longest(*lists):
    n = max((len(x) for x in lists), default=0)
    return [[x[i] if i < len(x) else None for x in lists] for i in range(n)]


def zip_longest_units(units):
    return [[c for c in grp if c] for grp in zip_longest(*units.values())]


def add_cards(new):
    q, pending = load("queue.json", {}), load("pending.json", [])
    _, backlog = due_cards()
    tomorrow = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0)
    from fsrs import Card
    for c in pending + new:
        if c["id"] in q:
            continue
        if backlog > BACKLOG_PAUSE:
            pending.append(c) if c not in pending else None
            continue
        card = Card()
        card.due = tomorrow                   # first return is the next day, never in the same unit
        q[c["id"]] = {**c, "fsrs": card.to_dict(), "reviews": 0}
    pending = [c for c in pending if c["id"] not in q]
    save("queue.json", q)
    save("pending.json", pending)
    return len(pending)


# ---------- commands ----------
def cmd_start(a):
    dt.date.fromisoformat(a.date)
    st = load("state.json", {})
    st["start"] = a.date
    save("state.json", st)
    print(f"Week 1 starts {a.date}.")


def cmd_today(a):
    today = dt.date.today()
    results = load("results.json", [])
    k, units, other = current_slot()
    done = load("state.json", {}).get("slot_done", [])
    units = [u for u in units if u not in done or units.count(u) > done.count(u)]
    if k // 7 + 1 <= 2:
        units = units[:1]                     # one new unit per sitting in weeks 1-2 (audit-pedagogy: load)
    served, total = due_cards()
    print(f"Week {k // 7 + 1}, sitting {k % 7 + 1} of 7")
    print(f"Recall: {len(served)} cards today" + (f" ({total - len(served)} more wait for tomorrow)" if total > len(served) else ""))
    for r in cold_due(results, today):
        print(f"Cold check due (since {r['cold_due']}): {r['unit']}  (its ## Cold item; predict first)")
    from check_unit import problems
    for s in units:
        path, note = next_unit(s, results)
        if path and problems(path):
            path, note = None, f"{meta(path)['id']} fails learn/check_unit.py; fix it before teaching"
        print(f"Unit {s}: " + (meta(path)["id"] + "  (file: " + str(path.relative_to(HERE)) + "; never show him the name)"
                                + (f"  {note}" if note else "") if path else f"none ({note})"))
    for o in other:
        print(f"Also: {o}")
    if not units and not other:
        print("No unit today.")


def cold_due(results, today):
    """One cold check per unit, from its latest session, listed from its due date until done."""
    latest = {}
    for r in sessions(results):
        latest[r["unit"]] = r
    done_cold = {r["unit"] for r in results if r["kind"] == "cold"}
    return [r for u, r in latest.items() if u not in done_cold and dt.date.fromisoformat(r["cold_due"]) <= today]


def cmd_due(a):
    q = load("queue.json", {})
    served, total = due_cards()
    for cid in served:
        v = q[cid]["variants"][q[cid].get("reviews", 0) % len(q[cid]["variants"])]
        print(f"{cid}  [{q[cid]['skill']}]  {v['q']}   ||  answer: {v['a']}")
    if total > len(served):
        print(f"({total - len(served)} more due; they wait for tomorrow)")


def cmd_review(a):
    from fsrs import Card, Rating
    q = load("queue.json", {})
    if a.card not in q:
        fail(f"no card '{a.card}'")
    c = q[a.card]
    card, _ = scheduler().review_card(Card.from_dict(c["fsrs"]), Rating(a.rating))
    c["fsrs"], c["reviews"] = card.to_dict(), c.get("reviews", 0) + 1
    if a.rating == 1:
        c["lapses"] = c.get("lapses", 0) + 1
    save("queue.json", q)
    print(f"{a.card} next due {card.due:%Y-%m-%d}" + ("  (lapsed: revisit its unit's wrong-idea step)" if a.rating == 1 else ""))


def cmd_predict(a):
    find_unit(a.unit)
    if not 0 <= a.p <= 100:
        fail("prediction must be 0 to 100")
    st = load("state.json", {})
    st.setdefault("predictions", {})[f"{a.unit}{':cold' if a.cold else ''}"] = a.p
    save("state.json", st)
    print(f"Prediction for {a.unit}{' (cold)' if a.cold else ''}: {a.p}")


def cmd_done(a):
    u = find_unit(a.unit)
    from check_unit import problems
    if problems(u["path"]):
        fail(f"{a.unit} fails learn/check_unit.py, so it is not taught or recorded; fix the unit first")
    skill, today = u["skill"], dt.date.today()
    results, st = load("results.json", []), load("state.json", {})
    tag = ":cold" if a.cold else ":retry" if a.retry else ""
    key = f"{a.unit}{tag}"
    predicted = st.get("predictions", {}).pop(key, None)
    if predicted is None:
        fail(f"no prediction recorded for {key}: run  engine.py predict {a.unit} P{' --' + tag[1:] if tag else ''}  before the first scored item")
    steps = {}
    for kv in a.step:
        k, _, v = kv.partition("=")
        v = float(v)
        if not 0 <= v <= 1 and k not in ("kappa", "rubric", "traces", "missed_fail", "numbers_met"):
            fail(f"step value must be 0 to 1: {kv}")
        steps[k.strip()] = v
    if a.cold:
        prior = [r for r in sessions(results) if r["unit"] == a.unit]
        if not prior:
            fail(f"{a.unit} has no session yet, so no cold check")
        if dt.date.fromisoformat(prior[-1]["cold_due"]) > today:
            fail(f"cold check for {a.unit} is not due until {prior[-1]['cold_due']}")
        scored = list(steps)                  # the cold item's own scored parts
    elif a.retry:
        if not [r for r in sessions(results) if r["unit"] == a.unit and not r["passed"]]:
            fail(f"{a.unit} has no missed session, so no retry")
        if "Retry" not in steps:
            fail('record the retry item as --step "Retry=<0..1>"')
        scored = ["Retry"]
    else:
        scored = u["scored"]
        missing = [s for s in scored if s not in steps and s not in ("kappa", "rubric")]
        if missing:
            fail(f"score every scored step of {a.unit}: missing {missing} (declared in its 'scored:' line)")
    vals = [steps[s] for s in scored if s in steps and s not in ("kappa", "rubric", "traces", "missed_fail", "numbers_met")]
    score = round(100 * sum(vals) / len(vals)) if vals else round(steps.get("rubric", steps.get("kappa", 0) * 100))
    kind = "cold" if a.cold else "retry" if a.retry else "session"
    passed = {"cold": steps.get("Cold", 0) * 100 >= BAR[skill], "retry": steps.get("Retry", 0) * 100 >= BAR[skill],
              "session": passes(skill, steps, scored)}[kind]
    r = {"date": str(today), "skill": skill, "unit": a.unit, "kind": kind, "score": score,
         "predicted": predicted, "steps": steps, "confident_wrong": a.confident_wrong, "passed": passed}
    if not a.cold:
        r["cold_due"] = str(today + dt.timedelta(days=7))
        k, units, _ = current_slot()
        if skill in units:                    # the sitting ends when each of its units is recorded
            st["slot_done"] = st.get("slot_done", []) + [skill]
            if all(st["slot_done"].count(x) >= units.count(x) for x in units):
                st["slot"], st["slot_done"] = k + 1, []
        waiting = add_cards(cards_of(u["path"]))
        if waiting:
            print(f"{waiting} new cards wait: the recall backlog is over {BACKLOG_PAUSE}")
    results.append(r)
    save("results.json", results)
    save("state.json", st)
    print(f"Recorded {a.unit}{' (' + kind + ')' if kind != 'session' else ''}: {score}, {'passed' if r['passed'] else 'not yet'} "
          f"(predicted {predicted}, gap {score - predicted:+d}).")


def cmd_close(a):
    u = find_unit(a.unit)
    add_cards([{"id": f"{a.unit}.close", "skill": u["skill"],
                "variants": [{"q": f"Your rule from {a.unit}: complete it. \"Next time ...\"", "a": a.line}]}])
    print("Close line added to the recall queue.")


def cmd_outside(a):
    if a.skill not in SKILLS or not 0 <= a.score <= 100:
        fail("skill must be one of " + ", ".join(SKILLS) + " and score 0 to 100")
    results = load("results.json", [])
    results.append({"date": str(dt.date.today()), "skill": a.skill, "unit": a.what, "kind": "outside",
                    "score": a.score, "predicted": None, "passed": a.score >= BAR[a.skill]})
    save("results.json", results)
    print(f"Outside task recorded for {a.skill}: {a.score}.")


def cmd_dashboard(a):
    results = load("results.json", [])
    start = load("state.json", {}).get("start")
    print(f"{'skill':12}{'main':>6}{'cold':>6}{'gap':>6}{'rung':>6}  status / alarms")
    for s in SKILLS:
        rs = [r for r in results if r["skill"] == s]
        sess = sessions(results, s)
        cold = [r for r in rs if r["kind"] == "cold"]
        outside = [r for r in rs if r["kind"] == "outside"]
        recent = sess[-3:]
        main = round(sum(r["score"] for r in recent) / len(recent)) if recent else None
        c = round(sum(r["score"] for r in cold[-3:]) / len(cold[-3:])) if cold else None
        gaps = [r["score"] - r["predicted"] for r in rs[-6:] if r.get("predicted") is not None]
        gap = round(sum(gaps) / len(gaps)) if gaps else None
        rung, mastered = skill_state(results, s)
        notes = []
        if main is not None and c is not None and main - c >= 10:
            notes.append("ALARM cold 10+ below session")
        if main is not None and main >= 90 and c is not None and c < 70:
            notes.append("EARLY WARNING: teaching recognition, not skill")
        weeks_in = week_no() - START_WEEK[s]
        if gap is not None and abs(gap) > 20:
            notes.append(f"ALARM prediction gap {gap:+d}")
        elif gap is not None and weeks_in >= 4 and abs(gap) > 10:
            notes.append(f"gap {gap:+d} above 10 after 4 weeks")
        if outside and not outside[-1]["passed"]:
            notes.append("outside task below the bar")
        status = "mastered" if mastered else ("not started" if not rs else f"bar {BAR[s]}")
        f = lambda v: f"{v:>6}" if v is not None else f"{'-':>6}"
        print(f"{s:12}{f(main)}{f(c)}{f(gap)}{rung:>6}  {status}" + ("; " + "; ".join(notes) if notes else ""))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("start").add_argument("date")
    sub.add_parser("today")
    sub.add_parser("due")
    p = sub.add_parser("review"); p.add_argument("card"); p.add_argument("rating", type=int, choices=[1, 2, 3, 4])
    p = sub.add_parser("predict"); p.add_argument("unit"); p.add_argument("p", type=int); p.add_argument("--cold", action="store_true")
    p.add_argument("--retry", action="store_true")
    p = sub.add_parser("done"); p.add_argument("unit"); p.add_argument("--step", action="append", default=[])
    p.add_argument("--confident-wrong", type=int, default=0); p.add_argument("--cold", action="store_true")
    p.add_argument("--retry", action="store_true")
    p = sub.add_parser("close"); p.add_argument("unit"); p.add_argument("line")
    p = sub.add_parser("outside"); p.add_argument("skill"); p.add_argument("score", type=int); p.add_argument("what")
    sub.add_parser("dashboard")
    a = ap.parse_args()
    globals()[f"cmd_{a.cmd}"](a)
