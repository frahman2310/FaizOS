"""Check questions.jsonl: every anchor is in its doc (normalised), all anchors of a
question fall within one 120-word window, 2-3 anchors of 1-5 words, and no anchor
string leaks into a client-worded question. Exit 1 on any failure."""
import json, re, sys
from pathlib import Path

LAB = Path(__file__).parent
WINDOW = 120
norm = lambda s: re.sub(r"\s+", " ", s.lower()).strip()

docs = {}
def words_index(doc):
    if doc not in docs:
        text = norm((LAB / "corpus/raw" / f"{doc}.txt").read_text(errors="replace"))
        # char offset -> word index
        starts = [m.start() for m in re.finditer(r"\S+", text)]
        docs[doc] = (text, starts)
    return docs[doc]

def word_at(starts, off):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= off: lo = mid
        else: hi = mid - 1
    return lo

def check(q):
    errs = []
    a = q["anchors"]
    if not 2 <= len(a) <= 3: errs.append(f"{len(a)} anchors")
    for x in a:
        if not 1 <= len(x.split()) <= 5: errs.append(f"anchor word count: {x!r}")
    if q["doc"] == "ratecard_2023": errs.append("doc is ratecard_2023")
    if q["wording"] == "client":
        for x in a:
            if norm(x) in norm(q["question"]): errs.append(f"anchor in client question: {x!r}")
    text, starts = words_index(q["doc"])
    events = []  # (first word, last word, anchor idx)
    for k, x in enumerate(a):
        x = norm(x)
        hits = [m.start() for m in re.finditer(re.escape(x), text)]
        if not hits: errs.append(f"not found: {x!r}")
        n = len(x.split())
        events += [(word_at(starts, h), word_at(starts, h) + n - 1, k) for h in hits]
    if errs: return errs
    # smallest span containing one occurrence of every anchor
    events.sort()
    best = None
    for s, _, _ in events:
        ends = {}
        for s2, e2, k in events:
            if s2 >= s and (k not in ends or e2 < ends[k]): ends[k] = e2
        if len(ends) == len(a):
            span = max(ends.values()) - s + 1
            best = span if best is None else min(best, span)
    if best is None or best > WINDOW: errs.append(f"anchors not within {WINDOW} words (best span {best})")
    return errs

qs = [json.loads(l) for l in (LAB / "questions.jsonl").read_text().splitlines() if l.strip()]
bad = 0
for q in qs:
    e = check(q)
    if e:
        bad += 1
        print(q["id"], "; ".join(e))
ids = [q["id"] for q in qs]
assert len(ids) == len(set(ids)), "duplicate ids"
print(f"{len(qs)} questions, {bad} failing")
sys.exit(1 if bad else 0)
