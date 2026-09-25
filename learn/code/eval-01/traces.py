"""Check every recipe excerpt and quoted reason in eval-01 against the HW3 key, and print the counts the unit uses.

    python3 code/record.py eval-01 traces.py      -> runs/eval-01-traces.json
Exit 1 if any excerpt line, rule line or quote is not in the source, or a trace is not HIGH confidence.
"""
import json
import re
from collections import Counter
from pathlib import Path

HW3 = Path("../../../private/research-base/evaluation/repos/recipe-chatbot/homeworks/hw3")
UNIT = next(Path("../../units/evaluation").glob("01-*.md"))
key = [json.loads(l) for l in open(HW3 / "reference_files/labeled_traces.jsonl")]
readme = (HW3 / "README.md").read_text()
rules = {m.group(1).lower(): f"{m.group(1)}: {m.group(2).strip()}" for m in re.finditer(r"- \*\*([\w -]+)\*\*: (.+)", readme)}
flat = lambda s: re.sub(r"\s+", " ", s)
everything = flat(readme + " ".join(r["response"] + " " + r["reasoning"] + " " + r["query"] for r in key))

c = Counter(r["label"] for r in key)
print(f"HW3 key: {len(key)} traces, PASS {c['PASS']}, FAIL {c['FAIL']}")
bad = 0
batch = Counter()
for section in re.split(r"(?m)^## ", UNIT.read_text())[1:]:
    name = section.split("\n", 1)[0].strip()
    body = section.split("### Key")[0]
    for fence in re.findall(r"```text\n(.*?)```", body, flags=re.S):
        lines = [l.strip() for l in fence.strip().splitlines() if l.strip()]
        req = re.sub(r"^\d+\. ", "", lines[0])
        query = re.fullmatch(r'Request: "(.*)"', req).group(1)
        diet = lines[1].removeprefix("Diet on record: ")
        found = [r for r in key if r["query"] == query and r["dietary_restriction"] == diet]
        problems = []
        if lines[2] != "Rule: " + rules.get(diet, "?"):
            problems.append("rule line differs from README")
        for l in lines[3:]:
            if l.startswith("["):
                continue
            m = re.fullmatch(r'(?:Step \d+|Last step): "(.*)"', l)
            text = m.group(1) if m else l.removeprefix("Recipe: ")
            found = [r for r in found if text in r["response"]]
        if len(found) != 1:
            problems.append(f"{len(found)} traces match")
        r = found[0] if len(found) == 1 else {"trace_id": "?", "label": "?", "confidence": "?"}
        if r["confidence"] != "HIGH":
            problems.append("not HIGH confidence")
        bad += bool(problems)
        item = ""
        if name.startswith("Step: Label the batch"):
            batch[r["label"]] += 1
            item = f"batch item {sum(batch.values())} | "
        print(f"{name} | {item}{r['trace_id']} {r['label']} {r['confidence']}" + (" | PROBLEM: " + "; ".join(problems) if problems else ""))
    prose = re.sub(r"```.*?```", " ", section, flags=re.S)
    quotes = [q for line in prose.splitlines() for q in line.split('"')[1::2] if len(q) >= 25]
    for q in quotes:
        for part in [p.strip(" .") for p in q.split("...") if len(p.strip(" .")) >= 15]:
            if flat(part) not in everything:
                bad += 1
                print(f"{name} | QUOTE NOT IN SOURCE: {part[:70]}")
print(f"batch: {sum(batch.values())} recipes, FAIL {batch['FAIL']}, PASS {batch['PASS']}")
print("all excerpts and quotes found in the source" if not bad else f"{bad} problems")
raise SystemExit(1 if bad else 0)
