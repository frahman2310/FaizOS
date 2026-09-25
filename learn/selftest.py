#!/usr/bin/env python3
"""Self-test of the machinery (docs/research/audit-system.md): mutate a passing unit one flaw at a time and
check that check_unit.py rejects each; run the guard against bypass attempts; run engine flows in a temp copy.

    python3 learn/selftest.py        # exit 0 when every attack is caught
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from check_unit import problems, steps, is_extra  # noqa: E402

fails = []


def expect(name, ok):
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        fails.append(name)


# ---------- 1. checker attacks ----------
base = next((p for p in sorted((HERE / "units").glob("*/*.md")) if not problems(p)), None)
if base is None:
    print("SKIP  checker attacks: no unit passes check_unit yet")
else:
    text = base.read_text()
    body0 = steps(text)[1][1]                    # a real step body to mutate

    def attack(name, new_text):
        tmp = base.parent / f"zz-selftest-{os.getpid()}.md"
        tmp.write_text(new_text)
        try:
            expect(f"checker rejects: {name}", bool(problems(tmp)))
        finally:
            tmp.unlink()

    inj = lambda s: text.replace(body0, s + "\n\n" + body0, 1)
    attack("invented number in prose", inj("The model is right 4837 times."))
    attack("invented number in inline code", inj("It printed `4837`."))
    attack("'given:' in the middle of a line", inj("This is not given: 4837 anywhere."))
    attack("number inside a quote that is not in a source", inj('He said "the answer here is 4837 exactly".'))
    attack("spelled-out number", inj("It was right forty-two times."))
    attack("invented number in a card", text.replace("## Cards\n", "## Cards\n- Q: How many? | A: exactly 4837\n", 1))
    attack("Key of TBD", re.sub(r"(### Key\n)(.*?)(\n## )", r"\1TBD\3", text, count=1, flags=re.S))
    attack("no cards", text.split("## Cards")[0] + "## Cards\n")
    attack("no cold item", re.sub(r"(?ms)^## Cold\n.*?(?=^## )", "", text))
    attack("no scored line", re.sub(r"(?m)^scored:.*\n", "", text))
    st0 = steps(text)
    first_try = next(n for n, b, k in st0 if "Kind: try" in k)
    first_scored = next(n for n, b, k in st0 if "Kind: scored" in k)
    attack("a scored step before any try (asked before practice)",
           text.replace(f"Kind: try", "Kind: scored", 1).replace(f"scored: ", f"scored: {first_try}, ", 1))
    attack("the first step is a question, not a show", text.replace("Kind: show", "Kind: try", 1))
    attack("a show step with 4 new ideas", re.sub(r"(?m)^New:.*$", "New: dict, key, list, loop", text, count=1))
    attack("a show step with no New: line", re.sub(r"(?m)^New:.*\n", "", text, count=1))
    attack("no Help block", re.sub(r"(?ms)^## Help: .*?(?=^## )", "", text))
    attack("no Retry item", re.sub(r"(?ms)^## Retry\n.*?(?=^## )", "", text))
    attack("a step over 2600 characters", inj("x" * 2700))
    attack("a practice step with a big blank table", text.replace(
        f"## Step: {first_try}\n", f"## Step: {first_try}\n\n| a | b | c |\n|---|---|---|\n" + "| ? | ? | ? |\n" * 3, 1))
    attack("a practice step with no prepared two options",
           re.sub(r"(?m)^Two options:.*\n", "", text))
    attack("a practice step with no prepared worked answer",
           re.sub(r"(?m)^Worked answer:.*\n", "", text))
    attack("'given:' in text he reads", inj("given: the bill is 4837."))
    (HERE / "runs/zz-nocommand.json").write_text('{"output": 1}')
    attack("run without a recorded command", re.sub(r"(?m)^runs:[ \t]*", "runs: runs/zz-nocommand.json, ", text, count=1))
    (HERE / "runs/zz-nocommand.json").unlink(missing_ok=True)
    attack("unexplained jargon", inj("The kappa was low."))
    if "skill: code" in text:
        attack("code block not in the programs", inj("```python\ntotal_cost = compute_everything(4837)\n```"))

# ---------- 2. guard attacks ----------
GUARD = ROOT / "hooks" / "teaching-guard.py"


def guard(text, cursor=None, active=False):
    """Run the Stop hook on a one-message transcript, with its own cursor file (never the real one)."""
    with tempfile.TemporaryDirectory() as d:
        cur = Path(d) / "cursor.json"
        if cursor:
            cur.write_text(json.dumps(cursor))
        t = Path(d) / "t.jsonl"
        t.write_text(json.dumps({"type": "user", "message": {"content": "go"}}) + "\n" +
                     json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}) + "\n")
        r = subprocess.run([sys.executable, str(GUARD)], input=json.dumps({"transcript_path": str(t), "stop_hook_active": active}),
                           capture_output=True, text=True, env={**os.environ, "FAIZ_CURSOR": str(cur)})
        return "block" in r.stdout


if base is not None:
    st = steps(base.read_text())
    other = next(p for p in sorted((HERE / "units").glob("*/*.md")) if p != base)
    s0, s1, key0 = st[0][1], st[1][1], st[0][2]
    expect("guard allows the first step alone", not guard(s0))
    expect("guard allows short feedback then a step", not guard("Right: that was it.\n\n" + s0))
    expect("guard blocks a question added after a step", guard(s0 + "\n\nAlso, what else? **Your answer.**"))
    expect("guard blocks two steps in one message", guard(s0 + "\n\n" + s1))
    expect("guard blocks Key text in the message", guard(s0 + "\n\n" + key0.splitlines()[0]))
    expect("guard blocks a step out of order", guard(s1))
    expect("guard blocks an improvised question", guard("Which is it, A or B?\n\n**Your answer.**"))
    expect("guard blocks an unbolded ask marker", guard("Which is it, A or B? Your answer."))
    w = re.findall(r"[A-Za-z]{5,}", s0)[0]
    expect("guard blocks a step with one word changed", guard(s0.replace(w, w[::-1], 1)))
    expect("guard blocks improvised text before the step", guard("Quick one first: what is 4821/3? Now:\n\n" + s0))
    expect("guard blocks an ask-marker variant", guard("What is a token?\n\n**Your answer:**"))
    expect("guard blocks when stop_hook_active", guard("Invented: what is it?\n\n**Your answer.**", active=True))
    bad = base.parent / f"zz-selftest-bad-{os.getpid()}.md"
    bad.write_text(base.read_text().replace(s0, s0.replace(w, w + " 4837", 1), 1))
    expect("guard blocks a step from a unit that fails the checker",
           guard(s0.replace(w, w + " 4837", 1)))
    bad.unlink()
    for u in sorted((HERE / "units").glob("*/*.md")):         # every real step, in order, must be allowed
        cur = None
        for i, (name, body, _) in enumerate(steps(u.read_text())):
            if is_extra(name):
                continue
            ok = not guard(body, cur)
            cur = {"unit": str(u), "index": i, "finished": False}
            if not ok:
                break
        expect(f"guard allows every step of {u.parent.name}/{u.name} in order", ok)
    moved = base.parent / f"zz-selftest-inline-{os.getpid()}.md"      # a Help block between steps must not count as a step
    t0 = base.read_text()
    helpb = re.search(r"(?ms)^## Help: .*?(?=^## )", t0).group(0)
    names = [n for n, b, k in steps(t0) if not is_extra(n)]
    t1 = t0.replace(helpb, "").replace(f"## Step: {names[1]}\n", helpb + f"## Step: {names[1]}\n", 1)
    hold = base.with_suffix(".selftest-hold")                         # only one unit may hold these step texts
    base.rename(hold)
    moved.write_text(t1)
    try:
        cur, ok = None, True
        for i, (name, body, _) in enumerate([x for x in steps(moved.read_text()) if not is_extra(x[0])]):
            ok = ok and not guard(body, cur)
            cur = {"unit": str(moved), "index": i, "finished": False}
        expect("guard counts only teaching steps (inline Help block)", ok)
    finally:
        moved.unlink()
        hold.rename(base)
    live = {"unit": str(base), "index": 1, "finished": False}
    expect("guard blocks an improvised question mid-unit (no marker)", guard("Close. What do you think a list holds here?", live))
    expect("guard allows stuck help written as statements mid-unit", not guard("Look at your answer to question 2: the key sits inside usage.", live))
    expect("guard allows re-sending an earlier step (re-teach)", not guard(s0, {"unit": str(base), "index": 2, "finished": False}))
    expect("guard blocks starting another unit mid-unit",
           guard(steps(other.read_text())[0][1], {"unit": str(base), "index": 1, "finished": False}))

# ---------- 3. engine flows in a temp copy ----------
with tempfile.TemporaryDirectory() as d:
    shutil.copytree(HERE, Path(d) / "learn", ignore=shutil.ignore_patterns(".venv", "data", "__pycache__"))
    for side in ("private", "docs", "scripts"):             # sources, glossary and checker helpers the units need
        if (ROOT / side).exists():
            (Path(d) / side).symlink_to(ROOT / side)
    py = str(HERE / ".venv/bin/python") if (HERE / ".venv/bin/python").exists() else sys.executable  # engine needs fsrs
    run = lambda *a: subprocess.run([py, "engine.py", *a], cwd=Path(d) / "learn", capture_output=True, text=True)
    expect("engine plans a sitting with no start date (C47)", "code" in run("today").stdout)
    expect("engine plans a day", run("today").returncode == 0)
    units = sorted((Path(d) / "learn/units").glob("*/*.md"))
    if units:
        uid = re.search(r"(?m)^id:\s*(\S+)", units[0].read_text()).group(1)
        expect("engine refuses a result without a prediction", run("done", uid, "--step", "x=1").returncode != 0)
        expect("engine refuses a cold check before a session", run("predict", uid, "50", "--cold").returncode == 0
               and run("done", uid, "--step", "Cold=1", "--cold").returncode != 0)
        expect("engine refuses an unknown card", run("review", "nope", "3").returncode != 0)
        m = next(q for q in units if "code/" in str(q))        # a miss, then the corrective retry
        mid = re.search(r"(?m)^id:\s*(\S+)", m.read_text()).group(1)
        sc = [x.strip() for x in re.search(r"(?m)^scored:(.*)$", m.read_text()).group(1).split(",")]
        run("predict", mid, "80")
        miss = run("done", mid, *sum([["--step", f"{x}=0.2"] for x in sc], []))
        expect("engine records a miss", "not yet" in miss.stdout)
        nxt = subprocess.run([py, "-c", "import engine; print(engine.next_unit('code', engine.load('results.json', [])))"],
                             cwd=Path(d) / "learn", capture_output=True, text=True).stdout
        expect("engine offers RETRY at the next code sitting after a miss", "RETRY" in nxt)
        run("predict", mid, "70", "--retry")
        rt = run("done", mid, "--step", "Retry=1", "--retry")
        expect("engine records a retry", rt.returncode == 0 and "retry" in rt.stdout)

print(f"\n{'all attacks caught' if not fails else str(len(fails)) + ' attack(s) got through'}")
sys.exit(1 if fails else 0)
