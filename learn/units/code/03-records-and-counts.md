skill: code
id: code-03
level: 1
title: Records and counts: a list of dicts, and counting what passed
sources: ../private/research-base/code/research/nelson-2017-pltutor-comprehension-first.md, ../private/research-base/code/research/ericson-2019-adaptive-parsons.md
runs: runs/code-03-predict.json, runs/code-03-trace.json, runs/code-03-parsons.json, runs/code-03-parsons_wrong.json, runs/code-03-test_parsons.json, runs/code-03-bug.json
targets: E1 (crash vs quietly wrong), E4 (which kind of value a sticker holds)
code: code/code-03/ (predict.py, trace.py, parsons.py, parsons_wrong.py, test_parsons.py, bug.py)

## Step: Predict

A log is a list of records, and each record is a dict about one call.

```python
log = [{"ok": True, "cost": 0.0027}, {"ok": False, "cost": 0.0}, {"ok": True, "cost": 0.0027}]
passed = 0
for row in log:
    if row["ok"]:
        passed = passed + 1
print(passed)
print(len(log))
print(log[1])
print(log[1]["cost"] + log[2])
```

For each of the four print lines, write exactly what it shows, and give one label:

- **crash**: the program stops with an error (write the error's name)
- **quietly wrong**: it runs, but the result is wrong
- **fine**: it runs and the result is right

**Your answer.**

### Key
Real output (runs/code-03-predict.json):

| Line | Shows | Label |
|---|---|---|
| `print(passed)` | `2` | fine |
| `print(len(log))` | `3` | fine |
| `print(log[1])` | `{'ok': False, 'cost': 0.0}` | fine: the whole second record (counting starts at 0) |
| `print(log[1]["cost"] + log[2])` | `TypeError: unsupported operand type(s) for +: 'float' and 'dict'` | crash |

Why the last one crashes (E4): `log[1]["cost"]` is a number, but `log[2]` is a whole dict, and Python cannot add a dict to a number. The fix is `log[2]["cost"]`. Ask him what kind of value each side holds before he labels.

## Step: Trace

The gate's pass counting, trimmed. A summariser writes a note for each invoice; a test case passes when the note includes the right total. `a in b`, with two pieces of text, is yes when `a` appears somewhere inside `b`.

```python
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
    passed = 0                                   # (a)
    failing = []                                 # (b)
    for case in cases:
        note = summarise(case)                   # (c)
        if case["must_include"] in note:
            passed = passed + 1                  # (d)
        else:
            failing.append(case["invoice"])      # (e)
    return passed, failing

passed, failing = score(CASES)
print(passed, "of", len(CASES), "passed")
print("failing:", failing)
print(f"pass rate {passed / len(CASES) * 100:.0f}%")
```

1. Fill the table, one row per pass of the loop, after the if/else has run.

| Pass | case["invoice"] | note | passed | failing |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

2. At the end, what kind of value does `failing` hold: a list of dicts, a list of names, or a number?
3. Write the three printed lines, and in one sentence say what `score` is for.

**Your answer.**

### Key
| Pass | case["invoice"] | note | passed | failing |
|---|---|---|---|---|
| 1 | `scan-000` | `Invoice scan-000, total PKR 80,000.` | 1 | `[]` |
| 2 | `credit-note-77` | `Invoice credit-note-77, due on receipt.` | 1 | `['credit-note-77']` |
| 3 | `typed-000` | `Invoice typed-000, total $100.` | 2 | `['credit-note-77']` |
| 4 | `typed-001` | `Invoice typed-001, total $107.` | 3 | `['credit-note-77']` |

`failing` is a list of names (pieces of text), because (e) appends `case["invoice"]`, one value from the dict, not the whole `case` (E4).
Printed (runs/code-03-trace.json): `3 of 4 passed`, `failing: ['credit-note-77']`, `pass rate 75%`.
Purpose: "It counts how many test cases get a note that includes the right total, and lists the invoices that did not."

## Step: Change

Put these lines in order to build `spend(log)`, which adds up the cost of every record in a log like the one in Predict. The indentation is already right. One line does not belong: leave it out and say what it would do.

```python
        total = total + row              # A
    return total                         # B
    for row in log:                      # C
        total = total + row["cost"]      # D
    total = 0.0                          # E
def spend(log):                          # F
```

The test: `spend(log)` must be `0.0054` for the Predict log, and `spend([])` must be `0.0`.

**Your answer.**

### Key
Order: F, E, C, D, B. Leave out A.
```python
def spend(log):
    total = 0.0
    for row in log:
        total = total + row["cost"]
    return total
```
Run: prints `0.0054`, and the test prints `PASS` (runs/code-03-parsons.json, runs/code-03-test_parsons.json). A adds the whole record (a dict) to a number: crash, `TypeError: unsupported operand type(s) for +: 'float' and 'dict'` (runs/code-03-parsons_wrong.json). `row` is one dict; `row["cost"]` is the number inside it (E4). Watch also for E before C but indented inside the loop (E2).

## Step: Find the bug

Someone rewrote one line of `score`. It runs with no error. The symptom, from a real run: the gate now says `0 of 4 passed`, `pass rate 0%`, and lists all four invoices as failing. The summariser did not change, and before the rewrite it was 3 of 4.

```python
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
```

1. Your hypothesis: which line is wrong, and what is it checking instead?
2. The one line to change, rewritten.

**Your answer.**

### Key
`if case["must_include"] in case:` looks for the total inside the whole case dict. `in` on a dict checks only its labels (`"invoice"`, `"must_include"`), and a total such as `"$100"` is never a label, so every case fails. `note` is made and never used, which is the clue. Fix:
```python
        if case["must_include"] in note:
```
Real run of the buggy file (runs/code-03-bug.json): `0 of 4 passed`, `failing: ['scan-000', 'credit-note-77', 'typed-000', 'typed-001']`, `pass rate 0%`. With the fix it is back to `3 of 4 passed` (runs/code-03-trace.json). Label: quietly wrong. In the real gate (gate.py), today's version and the proposed one would both score 0, the fall would be 0, and every change would be let through with no protection.

Debug card:
- Symptom: 0 of 4 pass; the summariser is unchanged.
- Hypothesis: the check compares the total with the wrong sticker, the dict instead of the note (E4).
- Test: print `note` and `case` for one case; the total is inside `note` and not among the labels of `case`.
- Fix: check against `note`; rerun and see 3 of 4.

## Step: Close

Finish this line in your own words: "Next time I see a sticker used in a check or a sum, I will ..."

**Your answer.**

### Key
Something like: "... say what kind of value it holds (a whole list, one dict, one number, one piece of text) before I trust the line." His line goes into the recall queue.

## Cards
- Q: `log` is a list of dicts. What kind of value is `log[1]`, and what is `log[1]["cost"]`? | A: `log[1]` is one whole dict (the second record); `log[1]["cost"]` is the number inside it.
- Q: `total = total + row` where `row` is a record dict. Crash, quietly wrong, or fine? | A: Crash: `TypeError`, a dict cannot be added to a number. Use `row["cost"]`.
- Q: `"$100" in case`, where `case` is a dict. What does `in` check? | A: Only the dict's labels, not its values, so it is almost always no. Quietly wrong, no crash.
- Q: `failing.append(case["invoice"])` runs for two cases. What does `failing` hold? | A: A list of two names (pieces of text), not two dicts.
- Q: A pass rate suddenly drops to 0% but the thing being scored did not change. First suspect? | A: The scoring code itself: a check against the wrong sticker.
