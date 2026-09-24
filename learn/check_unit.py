#!/usr/bin/env python3
"""Check a unit file before any of it is sent. A unit that fails is not taught.

    python3 learn/check_unit.py learn/units/code/01-*.md     # one or more files; exit 1 on any failure

What it enforces (docs/research/structures/INTEGRATED.md):
- the skill's own steps, in its own order, one '## Step: <name>' per message, each ending '**Your answer.**'
  and followed by a '### Key' the learner never sees;
- every number in a step's text comes from a saved run or the fact sheet; a number from a listed source is
  accepted only on a line that quotes it; scenario facts sit on a line marked 'given:' (no invented numbers);
- listed sources and runs exist; no step longer than 2,000 characters; watchlist jargon explained where used.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
ASK = "**Your answer.**"
STEPS = {
    "code": ["Predict", "Trace", "Change", "Find the bug", "Tell the AI", "Close"],
    "llm": ["Odd result", "Pick and say why", "Predict", "Run", "Explain", "Wrong idea fixed", "New case", "Close"],
    "production": ["Guess", "Chain", "Run", "Lever", "Quick set", "Close"],
    "evaluation": ["Warm-up labels", "Label the batch", "Group the failures", "Compare with the expert",
                   "Count and decide", "Close"],
    "design": ["Read the brief", "First design", "Numbers", "Choices", "Compare with the expert", "What if",
               "Decision note", "Close"],
}
OPTIONAL = {("code", "Tell the AI"): 2}          # step: first level at which it is required


def header(text):
    h = {}
    for line in text.split("\n## ", 1)[0].splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            h[m.group(1)] = m.group(2).strip()
    for k in ("sources", "runs"):
        h[k] = [x.strip() for x in h.get(k, "").split(",") if x.strip()]
    return h


def steps(text):
    """[(name, body, key)] for every '## Step: name' block."""
    out = []
    for block in re.split(r"(?m)^## ", text)[1:]:
        head, _, rest = block.partition("\n")
        if not head.startswith("Step: "):
            continue
        body, _, key = rest.partition("### Key")
        out.append((head[6:].strip(), body.strip(), key.strip()))
    return out


def numbers(text):
    return {n.rstrip(".,").replace(",", "") for n in re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", text)}


def problems(path):
    path = Path(path)
    text = path.read_text()
    h = header(text)
    out = []
    skill, level = h.get("skill"), int(h.get("level", "1") or 1)
    if skill not in STEPS:
        return [f"unknown skill '{skill}'"]
    found = [s[0] for s in steps(text)]
    expected = [s for s in STEPS[skill] if level >= OPTIONAL.get((skill, s), 0)]
    allowed = [s for s in STEPS[skill] if s in found]
    if found != allowed or [s for s in expected if s not in found]:
        out.append(f"steps must be, in order: {expected}; found {found}")
    measured, quoted = "", ""                        # runs and the fact sheet vs long sources
    for kind in ("runs", "sources"):
        for rel in h[kind]:
            f = HERE / rel if (HERE / rel).exists() else ROOT / rel
            if not f.exists():
                out.append(f"listed file not found: {rel}")
            elif kind == "runs":
                measured += f.read_text(errors="ignore")
            else:
                quoted += f.read_text(errors="ignore")
    known = numbers(measured + (HERE / "facts.md").read_text())
    from_sources = numbers(quoted)                   # accepted only on a line that quotes the source
    try:
        from check_lesson_script import jargon_problems
    except Exception:
        jargon_problems = lambda b: []
    for name, body, key in steps(text):
        if not body.rstrip().endswith(ASK):
            out.append(f"step '{name}' must end with {ASK}")
        if not key:
            out.append(f"step '{name}' has no ### Key")
        if len(body) > 2000:
            out.append(f"step '{name}' is {len(body)} characters, max 2000")
        out += [f"step '{name}': {j}" for j in jargon_problems(body)]
        prose = re.sub(r"```.*?```", " ", body, flags=re.S)
        for line in prose.splitlines():
            if re.search(r"(?i)\bgiven:", line):
                continue
            quoting = '"' in line or "\u201c" in line
            for n in numbers(re.sub(r"`[^`]*`", "", line)):
                if n in known or (quoting and n in from_sources):
                    continue
                if not re.fullmatch(r"\d|10|20\d\d", n):
                    out.append(f"step '{name}': number {n} is not in a listed run, source or facts.md "
                               f"(mark the line 'given:' if it is a scenario fact)")
    if "## Cards" not in text:
        out.append("missing '## Cards' (the items this unit adds to the recall queue)")
    return out


def main(paths):
    bad = 0
    for p in paths:
        errs = problems(p)
        print(("PASS  " if not errs else "FAIL  ") + str(p))
        for e in errs:
            print("      " + e)
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
