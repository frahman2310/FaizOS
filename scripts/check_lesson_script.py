#!/usr/bin/env python3
"""Validate a lesson teaching script against the faiz-teach part template.

Usage: python3 scripts/check_lesson_script.py projects/meter/script.md
Exit 0 if every part passes, 1 otherwise. Deterministic, stdlib only.
"""
import re
import sys

SKILL = "/Users/faizr/AI OS for Learning/.claude/skills/faiz-teach/SKILL.md"


def required_markers():
    """Template markers come from the faiz-teach skill, so the checker never drifts from it."""
    try:
        for line in open(SKILL):
            if line.startswith("Template markers:"):
                return [m.strip().strip("`") for m in line.split(":", 1)[1].split("|") if m.strip()]
    except OSError:
        pass
    return ["**The problem.**", "**The fix:**", "**Picture", "**Your turn.**"]


REQUIRED = required_markers()


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
