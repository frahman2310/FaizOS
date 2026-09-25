"""Check every recipe excerpt, Key label and quoted reason in eval-01 against the HW3 key, and print the counts the unit uses.

    python3 code/record.py eval-01 traces.py      -> runs/eval-01-traces.json
Exit 1 if any excerpt line, rule line or quote is not in the source, a trace is not HIGH confidence, a Key label
differs from the source label, a Key names the wrong trace for a numbered item, or a quote is not in a trace that
the step (or the step before it, whose reason it reveals) cites; a quoted request may come from any trace.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HW3 = Path("../../../private/research-base/evaluation/repos/recipe-chatbot/homeworks/hw3")
UNIT = next(Path("../../units/evaluation").glob("01-*.md"))
key = [json.loads(l) for l in open(HW3 / "reference_files/labeled_traces.jsonl")]
by_id = {r["trace_id"]: r for r in key}
readme = (HW3 / "README.md").read_text()
rules = {m.group(1).lower(): f"{m.group(1)}: {m.group(2).strip()}" for m in re.finditer(r"- \*\*([\w -]+)\*\*: (.+)", readme)}
flat = lambda s: re.sub(r"\s+", " ", s)
text_of = lambda r: flat(r["response"] + " " + r["reasoning"] + " " + r["query"])
LABELLED = re.compile(r'(?:Step \d+|Last step|Last line|Tip): "(.*)"')
KEY_AFTER = re.compile(r"trace (\d+_\d+),? (PASS|FAIL)")                      # "trace 38_22, FAIL"
KEY_BEFORE = re.compile(r"(?:^|[.;] )(\d+) (PASS|FAIL)\b[^()\n]*\(trace (\d+_\d+)\)", re.M)   # "7 FAIL, ... (trace 38_36)"

c = Counter(r["label"] for r in key)
print(f"HW3 key: {len(key)} traces, PASS {c['PASS']}, FAIL {c['FAIL']}")
bad = 0
groups = {}                       # "batch" / "Retry" / "Cold" -> {item number: trace}
prev_cited = set()
for section in re.split(r"(?m)^## ", UNIT.read_text())[1:]:
    name = section.split("\n", 1)[0].strip()
    body, _, keytext = section.partition("### Key")
    group = "batch" if name.startswith("Step: Label the batch") else name.split()[0] if re.match(r"(Retry|Cold)\b", name) else None
    excerpt = {}                  # trace id -> item number (or None)
    for fence in re.findall(r"```text\n(.*?)```", body, flags=re.S):
        lines = [l.strip() for l in fence.strip().splitlines() if l.strip()]
        num = re.match(r"(\d+)\. ", lines[0])
        query = re.fullmatch(r'Request: "(.*)"', re.sub(r"^\d+\. ", "", lines[0])).group(1)
        diet = lines[1].removeprefix("Diet on record: ")
        found = [r for r in key if r["query"] == query and r["dietary_restriction"] == diet]
        problems = []
        if lines[2] != "Rule: " + rules.get(diet, "?"):
            problems.append("rule line differs from README")
        for l in lines[3:]:
            if l.startswith("["):
                continue
            m = LABELLED.fullmatch(l)
            text = m.group(1) if m else l.removeprefix("Recipe: ")
            found = [r for r in found if text in r["response"]]
        if len(found) != 1:
            problems.append(f"{len(found)} traces match")
        r = found[0] if len(found) == 1 else {"trace_id": "?", "label": "?", "confidence": "?"}
        if r["confidence"] != "HIGH":
            problems.append("not HIGH confidence")
        excerpt[r["trace_id"]] = int(num.group(1)) if num else None
        item = ""
        if group:
            groups.setdefault(group, {})[int(num.group(1))] = r["trace_id"]
            item = f"{group} item {num.group(1)} | "
        bad += bool(problems)
        print(f"{name} | {item}{r['trace_id']} {r['label']} {r['confidence']}" + (" | PROBLEM: " + "; ".join(problems) if problems else ""))
    # every Key label equals the source label; numbered items name the trace shown under that number
    labels = [(None, t, lab) for t, lab in KEY_AFTER.findall(keytext)] + [(int(n), t, lab) for n, lab, t in KEY_BEFORE.findall(keytext)]
    named = set(re.findall(r"trace (\d+_\d+)", keytext))
    for t in sorted(named - {t for _, t, _ in labels}):
        bad += 1
        print(f"{name} | KEY NAMES trace {t} WITHOUT A LABEL")
    for n, t, lab in labels:
        src = by_id.get(t, {}).get("label")
        if src != lab:
            bad += 1
            print(f"{name} | KEY LABEL {lab} for trace {t}, source says {src}")
        if n is not None and group and groups.get(group, {}).get(n) != t:
            bad += 1
            print(f"{name} | KEY ITEM {n} names trace {t}, the excerpt shows {groups.get(group, {}).get(n)}")
    for t in set(excerpt) - named:
        bad += 1
        print(f"{name} | KEY DOES NOT NAME the shown trace {t}")
    # every quote is in the README or in a trace this step or the step before cites
    cited = set(excerpt) | named
    pool = key if name == "Cards" else [by_id[t] for t in (cited | prev_cited) if t in by_id]   # cards: any trace
    allowed = flat(readme) + " " + " ".join(text_of(r) for r in pool) + " " + " ".join(r["query"] for r in key)  # requests recur across traces
    prose = re.sub(r"```.*?```", " ", body, flags=re.S)
    quotes = [q for line in prose.splitlines() for q in line.split('"')[1::2] if len(q) >= 25]
    for q in quotes:
        for part in [p.strip(" .") for p in q.split("...") if len(p.strip(" .")) >= 15]:
            if flat(part) not in allowed:
                bad += 1
                print(f"{name} | QUOTE NOT IN A CITED TRACE: {part[:70]}")
    # a label list the learner reads ("1 PASS, 2 FAIL, ...") matches the batch key
    for line in prose.splitlines():
        pairs = re.findall(r"(\d+) (PASS|FAIL)\b", line)
        if len(pairs) >= 6:
            for n, lab in pairs:
                t = groups.get("batch", {}).get(int(n))
                if not t or by_id[t]["label"] != lab:
                    bad += 1
                    print(f"{name} | LISTED LABEL {n} {lab} differs from the batch key")
    prev_cited = cited
for g, items in groups.items():
    gc = Counter(by_id[t]["label"] for t in items.values())
    print(f"{g}: {len(items)} recipes, FAIL {gc['FAIL']}, PASS {gc['PASS']}")
bc = Counter(by_id[t]["label"] for t in groups.get("batch", {}).values())
print(f"batch score points: {sum(bc.values()) + bc['FAIL']} (one per label, one more per expert FAIL)")
sys.path.insert(0, "../..")
from engine import BAR                    # the pass bar the unit tells him, read from the engine, not typed
print(f"evaluation bar: {BAR['evaluation']} (percent of scored points)")
print(f"step values to record: a third = {1/3:.3f}, two thirds = {2/3:.3f} (3 decimals, so a mean at the bar is not lost to rounding)")
print("all excerpts, Key labels and quotes match the source" if not bad else f"{bad} problems")
raise SystemExit(1 if bad else 0)
