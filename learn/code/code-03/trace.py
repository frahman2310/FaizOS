CASES = [
    {"invoice": "scan-000", "must_include": "PKR 80,000"},
    {"invoice": "credit-note-77", "must_include": "-$310"},
    {"invoice": "typed-000", "must_include": "$100"},
]
MISSES = ["credit-note-77"]          # the fake summariser drops the total on these

def summarise(case):
    if case["invoice"] in MISSES:
        return "Invoice " + case["invoice"] + ", due on receipt."
    return "Invoice " + case["invoice"] + ", total " + case["must_include"] + "."

def score(cases):
    # goal: count the cases whose note has the right total, and name the others
    # 1. set start values
    passed = 0
    failing = []                                 # (a)
    for case in cases:
        # 2. score each case
        note = summarise(case)                   # (b)
        if case["must_include"] in note:
            # 3. count it, or name it
            passed = passed + 1                  # (c)
        else:
            failing.append(case["invoice"])      # (d)
    # 4. hand back both
    return passed, failing

passed, failing = score(CASES)
print(passed, "of", len(CASES), "passed")
print("failing:", failing)
