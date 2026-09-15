#!/usr/bin/env python3
"""Validate a lesson teaching script against the faiz-teach part template.

Usage: python3 scripts/check_lesson_script.py projects/meter/script.md
Exit 0 if every part passes, 1 otherwise. Deterministic, stdlib only.
"""
import re
import sys

SKILL = "/Users/faizr/AI OS for Learning/.claude/skills/faiz-teach/SKILL.md"


def markers(label, default):
    """Markers come from the faiz-teach skill, so the checker never drifts from it."""
    try:
        for line in open(SKILL):
            if line.startswith(label + ":"):
                return [m.strip().strip("`") for m in line.split(":", 1)[1].split("|") if m.strip()]
    except OSError:
        pass
    return default


REQUIRED = markers("Template markers", ["**The problem.**", "**The fix:**", "**Picture", "**Your turn.**"])
BUILD_REQUIRED = markers("Build markers", ["**The build.**", "**Decision", "**Your call.**"])
START_MARKERS = [REQUIRED[0], BUILD_REQUIRED[0]]
ASK_MARKERS = [REQUIRED[-1], BUILD_REQUIRED[-1]]


def build_problems(new, body, has_key):
    out = [f"missing {r}" for r in BUILD_REQUIRED if r not in body]
    if new is None:
        out.append("missing 'New:' line")
    decisions = re.split(re.escape(BUILD_REQUIRED[1]), body.split(BUILD_REQUIRED[-1])[0])[1:]
    if not 3 <= len(decisions) <= 5:
        out.append(f"{len(decisions)} decisions, need 3-5")
    for i, d in enumerate(decisions, 1):
        if d.count("rules out") < 2:
            out.append(f"decision {i}: every option must say what it rules out (need 2+)")
    if len(body) > 4000:
        out.append(f"build is {len(body)} characters, max 4000")
    if not has_key:
        out.append("missing '### Key' section (the target number and a sound set of choices)")
    return out


def parts(text):
    """Yield (part_id, new_line, body) for every '## ' part in a script."""
    for block in re.split(r"(?m)^## ", text)[1:]:
        head, _, rest = block.partition("\n")
        part_id = head.split(" ")[0]
        new = re.search(r"(?m)^New: (.*)$", rest)
        body = rest.split("### Key")[0]
        body = re.sub(r"(?m)^(New|Status): .*\n", "", body).strip()
        yield part_id, (new.group(1).strip() if new else None), body, "### Key" in rest


def problems(part_id, new, body, has_key):
    if part_id.startswith("BUILD"):
        return build_problems(new, body, has_key)
    out = []
    for r in REQUIRED:
        if r not in body:
            out.append(f"missing {r}")
    if new is None:
        out.append("missing 'New:' line (the one new thing, or 'none')")
    elif re.search(r";| \+ | and ", new):
        out.append(f"'New:' lists more than one thing: {new}")
    turn = body.split("**Your turn.**")
    before, after = turn[0], (turn[1] if len(turn) > 1 else "")
    if len(re.findall(r"(?m)^- \*\*", before)) < 2:
        out.append("fewer than 2 paths spelled out as '- **...' bullets before Your turn")
    questions = re.findall(r"(?m)^\d+\. ", after)
    if not 4 <= len(questions) <= 6:
        out.append(f"{len(questions)} questions, need 4-6")
    if after.count("**Someone broke it.**") != 1:
        out.append("need exactly one '**Someone broke it.**' question")
    for code in re.findall(r"```[^\n]*\n(.*?)```", body, flags=re.S):
        n = len(code.strip("\n").splitlines())
        if n > 10:
            out.append(f"code block of {n} lines, max 10")
    if len(body) > 2000:
        out.append(f"part is {len(body)} characters, max 2000")
    if re.search(r"(?i)open (the file|meter|[\w/]+\.py)|scroll (up|down)|go to line", body):
        out.append("asks him to open, scroll or hunt in a file; paste the lines in chat instead")
    if not has_key:
        out.append("missing '### Key' answer section")
    return out


def main(path):
    text = open(path).read()
    failed = False
    for part_id, new, body, has_key in parts(text):
        errs = problems(part_id, new, body, has_key)
        print(f"{'PASS' if not errs else 'FAIL'}  {part_id}")
        for e in errs:
            print(f"        {e}")
        failed = failed or bool(errs)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
