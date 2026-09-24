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
from check_unit import problems, steps  # noqa: E402

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
    attack("steps out of order", text.replace("## Step: " + steps(text)[0][0], "## Step: TEMP", 1)
           .replace("## Step: " + steps(text)[1][0], "## Step: " + steps(text)[0][0], 1)
           .replace("## Step: TEMP", "## Step: " + steps(text)[1][0], 1))
    (HERE / "runs/zz-nocommand.json").write_text('{"output": 1}')
    attack("run without a recorded command", re.sub(r"(?m)^runs:[ \t]*", "runs: runs/zz-nocommand.json, ", text, count=1))
    (HERE / "runs/zz-nocommand.json").unlink(missing_ok=True)
    attack("unexplained jargon", inj("The kappa was low."))
    if "skill: code" in text:
        attack("code block not in the programs", inj("```python\ntotal_cost = compute_everything(4837)\n```"))

# ---------- 2. guard attacks ----------
GUARD = ROOT / "hooks" / "teaching-guard.py"


def guard(text, cursor=None, active=False):
    data = HERE / "data"
    saved = (data / "cursor.json").read_text() if (data / "cursor.json").exists() else None
    data.mkdir(exist_ok=True)
    (data / "cursor.json").write_text(json.dumps(cursor)) if cursor else (data / "cursor.json").unlink(missing_ok=True)
    t = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
    t.write(json.dumps({"type": "user", "message": {"content": "go"}}) + "\n")
    t.write(json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}) + "\n")
    t.close()
    r = subprocess.run([sys.executable, str(GUARD)], input=json.dumps({"transcript_path": t.name, "stop_hook_active": active}),
                       capture_output=True, text=True)
    (data / "cursor.json").write_text(saved) if saved else (data / "cursor.json").unlink(missing_ok=True)
    return "block" in r.stdout


if base is not None:
    st = steps(base.read_text())
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
    expect("guard blocks a repeated step", guard(s0, {"unit": str(base), "index": 0, "finished": False}))

# ---------- 3. engine flows in a temp copy ----------
with tempfile.TemporaryDirectory() as d:
    shutil.copytree(HERE, Path(d) / "learn", ignore=shutil.ignore_patterns(".venv", "data", "__pycache__", "runs"))
    py = str(HERE / ".venv/bin/python") if (HERE / ".venv/bin/python").exists() else sys.executable  # engine needs fsrs
    run = lambda *a: subprocess.run([py, "engine.py", *a], cwd=Path(d) / "learn", capture_output=True, text=True)
    expect("engine refuses a date before the start", "error" in run("start", "2999-01-01").stdout + run("today").stderr + run("today").stdout)
    run("start", "2020-01-06")
    expect("engine plans a day", run("today").returncode == 0)
    units = sorted((Path(d) / "learn/units").glob("*/*.md"))
    if units:
        uid = re.search(r"(?m)^id:\s*(\S+)", units[0].read_text()).group(1)
        expect("engine refuses a result without a prediction", run("done", uid, "--step", "x=1").returncode != 0)
        expect("engine refuses a cold check before a session", run("predict", uid, "50", "--cold").returncode == 0
               and run("done", uid, "--step", "Cold=1", "--cold").returncode != 0)
        expect("engine refuses an unknown card", run("review", "nope", "3").returncode != 0)

print(f"\n{'all attacks caught' if not fails else str(len(fails)) + ' attack(s) got through'}")
sys.exit(1 if fails else 0)
