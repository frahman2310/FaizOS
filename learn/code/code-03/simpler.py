from trace import CASES, summarise

def score(cases):
    # goal: count the cases whose note has the right total
    passed = 0
    for case in cases:
        note = summarise(case)
        if case["must_include"] in note:
            passed = passed + 1
    return passed

print(score(CASES), "of", len(CASES), "passed")
