# The Trace Key's memory table: trace.py's score() with a print after every marked line.
from trace import CASES, summarise

def score(cases):
    passed = 0
    failing = []
    print("after (a): case -  note -  passed", passed, " failing", failing)
    for case in cases:
        note = summarise(case)
        print("after (b): case", case, " note", repr(note), " passed", passed, " failing", failing)
        if case["must_include"] in note:
            passed = passed + 1
            print("after (c): case", case["invoice"], " note", repr(note), " passed", passed, " failing", failing)
        else:
            failing.append(case["invoice"])
            print("after (d): case", case["invoice"], " note", repr(note), " passed", passed, " failing", failing)
    return passed, failing

print(score(CASES))
