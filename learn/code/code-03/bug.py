CASES = [
    {"invoice": "scan-000", "must_include": "PKR 80,000"},
    {"invoice": "credit-note-77", "must_include": "-$310"},
    {"invoice": "typed-000", "must_include": "$100"},
    {"invoice": "typed-001", "must_include": "$107"},
]
MISSES = ["credit-note-77"]          # the fake summariser drops the total on these

def summarise(case):
    if case["invoice"] in MISSES:
        return "Invoice " + case["invoice"] + ", due on receipt."
    return "Invoice " + case["invoice"] + ", total " + case["must_include"] + "."

def score(cases):
    passed = 0
    failing = []
    for case in cases:
        note = summarise(case)
        if case["must_include"] in case:
            passed = passed + 1
        else:
            failing.append(case["invoice"])
    return passed, failing

passed, failing = score(CASES)
print(passed, "of", len(CASES), "passed")
print("failing:", failing)
print(f"pass rate {passed / len(CASES) * 100:.0f}%")
