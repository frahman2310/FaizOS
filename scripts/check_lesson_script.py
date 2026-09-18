#!/usr/bin/env python3
"""Validate a lesson teaching script against the faiz-teach skill.

Usage: python3 scripts/check_lesson_script.py projects/<lesson>/script.md
Exit 0 if the script passes, 1 otherwise. Markers come from the skill so this never drifts from it.
Parts already marked 'Status: done' were validated when sent and are not re-checked.
"""
import re
import sys

SKILL = "/Users/faizr/AI OS for Learning/.claude/skills/faiz-teach/SKILL.md"


def markers(label, default):
    try:
        for line in open(SKILL):
            if line.startswith(label + ":"):
                return [m.strip().strip("`") for m in line.split(":", 1)[1].split("|") if m.strip()]
    except OSError:
        pass
    return default


REQUIRED = markers("Template markers", ["**The problem.**", "**The fix:**", "**Picture", "**Your turn.**"])
DECISION = markers("Decision markers", ["**Decision", "**What happens:**", "**Effect on the target:**",
                                        "**Cost:**", "**Rules out:**", "**Your pick.**"])
CALL = markers("Call markers", ["**Your call.**"])
START_MARKERS = [REQUIRED[0], "**The build.**", DECISION[0], CALL[0]]
ASK_MARKERS = [REQUIRED[-1], DECISION[-1], CALL[-1]]


GLOSSARY = "/Users/faizr/AI OS for Learning/docs/glossary.md"


def glossary():
    """(taught terms, watchlist terms), lower-case. Missing file means nothing is checked."""
    try:
        text = open(GLOSSARY).read()
    except OSError:
        return set(), []
    taught_part = text.split("## Taught", 1)[1].split("## Watchlist", 1)[0] if "## Taught" in text else ""
    taught = {line.split(":", 1)[0].strip().lower() for line in taught_part.splitlines() if ":" in line}
    watch_part = text.split("## Watchlist", 1)[1] if "## Watchlist" in text else ""
    watch = [w.strip().lower() for w in watch_part.replace("\n", ",").split(",") if w.strip()]
    return taught, sorted(watch, key=len, reverse=True)


def jargon_problems(body):
    taught, watch = glossary()
    plain = re.sub(r"```.*?```", " ", body, flags=re.S).lower()
    out = []
    for term in watch:
        if term in taught:
            continue
        m = re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", plain)
        if not m:
            continue
        start = max(plain.rfind(". ", 0, m.start()), plain.rfind("\n", 0, m.start())) + 1
        sentence = re.split(r"(?<=[.!?])\s", plain[start:], maxsplit=1)[0]
        if not re.search(r"\b(means|meaning|is|are|called|short for)\b|\(", sentence):
            out.append(f"'{term}' is not taught yet and is not explained where it first appears")
    return out


def parts(text):
    """Yield (part_id, new_line, body, key_text, status) for every '## ' part."""
    for block in re.split(r"(?m)^## ", text)[1:]:
        head, _, rest = block.partition("\n")
        new = re.search(r"(?m)^New: (.*)$", rest)
        status = re.search(r"(?m)^Status: (.*)$", rest)
        body, _, key = rest.partition("### Key")
        body = re.sub(r"(?m)^(New|Status): .*\n", "", body).strip()
        yield (head.split(" ")[0], new.group(1).strip() if new else None, body,
               key if "### Key" in rest else None, status.group(1).strip() if status else "")


def problems(part_id, new, body, key, status):
    if status.startswith(("done", "withdrawn")):
        return []
    out = []
    if new is None:
        out.append("missing 'New:' line (the one new thing, or 'none')")
    elif re.search(r";| \+ | and ", new):
        out.append(f"'New:' lists more than one thing: {new}")
    if key is None:
        out.append("missing '### Key' section")
    limit = 2000 if part_id.startswith("BUILD") else 2600
    if len(body) > limit:
        out.append(f"part is {len(body)} characters, max {limit}")
    out += jargon_problems(body)
    if re.search(r"(?i)open (the file|meter|[\w/]+\.py)|scroll (up|down)|go to line", body):
        out.append("asks him to open, scroll or hunt in a file; paste the lines in chat instead")

    if part_id.startswith("BUILD-D"):
        out += [f"missing {m}" for m in DECISION if m not in body]
        if re.search(r"(?i)\*\*Rules out:\*\*\s*(nothing|none)", body):
            out.append("an option that rules out nothing is not a trade-off (C35)")
        if key is not None and "gives up" not in key:
            out.append("'### Key' must name what the winning option gives up (C35)")
        for m in DECISION[1:5]:
            if body.count(m) < 2:
                out.append(f"every option needs its own {m} (found {body.count(m)}, need 2+)")
        return out
    if part_id.startswith("BUILD-CALL"):
        return out + [f"missing {m}" for m in CALL if m not in body]

    out += [f"missing {m}" for m in REQUIRED if m not in body]
    if REQUIRED[0] in body and REQUIRED[1] in body:
        problem = body.split(REQUIRED[0], 1)[1].split(REQUIRED[1], 1)[0]
        sentences = len(re.findall(r"[.!?](\s|$)", problem.strip()))
        if sentences < 4:
            out.append(f"The problem has {sentences} sentences; give the full context in 4-6 (C34)")
    turn = body.split(REQUIRED[-1])
    before, after = turn[0], (turn[1] if len(turn) > 1 else "")
    if len(re.findall(r"(?m)^- \*\*", before)) < 2:
        out.append("fewer than 2 paths spelled out as '- **...' bullets")
    questions = re.findall(r"(?m)^\d+\. ", after)
    if not 4 <= len(questions) <= 6:
        out.append(f"{len(questions)} questions, need 4-6")
    if after.count("**Someone broke it.**") != 1:
        out.append("need exactly one '**Someone broke it.**' question")
    elif "quietly wrong (runs, wrong result)" not in after:
        out.append("the Someone broke it question must define the labels (crash, quietly wrong, fine)")
    if key is not None:
        answers = re.findall(r"(?m)^\d+\.\s*(.+)$", key)
        asked = re.sub(r"(?m)^\d+\.\s", "", after)          # question numbers are not content
        readback = [i + 1 for i, a in enumerate(answers)
                    if (nums := re.findall(r"\d[\d,.]*", a.split("(")[0]))
                    and all(re.search(r"(?<![\d.,])" + re.escape(n.rstrip(".,")) + r"(?![\d])", asked)
                            for n in nums)]
        if readback:
            out.append(f"question(s) {readback} only read back a number already in the questions (C36)")
    for code in re.findall(r"```[^\n]*\n(.*?)```", body, flags=re.S):
        if len(code.strip("\n").splitlines()) > 10:
            out.append("code block over 10 lines")
    if key is not None and "Relies on:" not in key:
        out.append("'### Key' needs a 'Relies on:' line listing the rules the questions use")
    return out


def script_problems(text):
    m = re.search(r"(?m)^# Lesson (\d+)", text)
    if m and int(m.group(1)) >= 5:
        prev = int(m.group(1)) - 1
        c = re.search(rf"(?m)^Carry-over from L{prev}:(.*)$", text)
        if not c or not c.group(1).strip():
            return [f"missing 'Carry-over from L{prev}:' with the adjustments from the last lesson's evidence"]
    return []


def main(path):
    text = open(path).read()
    failed = False
    for e in script_problems(text):
        print(f"FAIL  script header\n        {e}")
        failed = True
    for part_id, new, body, key, status in parts(text):
        errs = problems(part_id, new, body, key, status)
        print(f"{'PASS' if not errs else 'FAIL'}  {part_id}{'  (done)' if status.startswith('done') else ''}")
        for e in errs:
            print(f"        {e}")
        failed = failed or bool(errs)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
