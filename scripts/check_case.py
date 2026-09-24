#!/usr/bin/env python3
"""Check an investigation case file before it is handed to Faiz.

A case brief may only state numbers the lab actually produced. Every number in the text above the
line '## Log' must appear in one of the saved outputs the case names on its 'Evidence:' line, or sit in
a sentence that says 'assumed:' or 'given:' (a business fact from the scenario, not a measurement).
The case must also carry the sections the skill requires.

    python3 scripts/check_case.py projects/search/cases/case-01.md
"""
import re
import sys
from pathlib import Path

REQUIRED = ["**Your job.**", "**The situation.**", "**The problem.**", "**The bar.**", "**What you have.**",
            "**How you work.**", "**What the lab can do.**", "**How it ends.**",
            "**Evidence:**", "## Log", "**Your move.**"]


def numbers(text):
    return {n.rstrip(".,") for n in re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?%?", text)}


def main(path):
    case = Path(path)
    text = case.read_text()
    out = [f"missing {m}" for m in REQUIRED if m not in text]
    brief = text.split("## Log")[0]
    ev = re.search(r"\*\*Evidence:\*\*(.*)", brief)
    sources = ""
    for rel in re.findall(r"`([^`]+)`", ev.group(1) if ev else ""):
        f = (case.parent / rel).resolve()
        if not f.exists():
            out.append(f"evidence file not found: {rel}")
        else:
            sources += f.read_text(errors="ignore")
    produced = numbers(sources)
    for sentence in re.split(r"(?<=[.!?])\s+|\n", brief):
        if re.search(r"(?i)\b(assumed|given):", sentence) or "**Evidence:**" in sentence or sentence.startswith("#"):
            continue
        for n in numbers(re.sub(r'`[^`]*`|"[^"]*"', "", sentence)):
            bare = n.rstrip("%")
            if n not in produced and bare not in produced and not re.fullmatch(r"20\d\d|\d", bare):
                out.append(f"'{n}' is not in the evidence files and not marked assumed: or given:  ({sentence.strip()[:70]})")
    for line in out:
        print("FAIL  " + line)
    if not out:
        print(f"PASS  {case.name}")
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
