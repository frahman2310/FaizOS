skill: code
id: code-03
level: 1
title: Scoring a list of test cases
sources: ../private/research-base/code/research/nelson-2017-pltutor-comprehension-first.md, ../private/research-base/code/research/ericson-2019-adaptive-parsons.md
runs: runs/code-03-predict.json, runs/code-03-in_rule.json, runs/code-03-trace.json, runs/code-03-table.json, runs/code-03-simpler.json, runs/code-03-parsons_lines.json, runs/code-03-parsons.json, runs/code-03-parsons_wrong.json, runs/code-03-test_parsons.json, runs/code-03-test_parsons-parsons_wrong.json, runs/code-03-bug.json, runs/code-03-bug_probe.json, runs/code-03-cold.json, runs/code-03-cold_fixed.json, runs/code-03-card1_a.json, runs/code-03-card1_b.json, runs/code-03-card2_a.json, runs/code-03-card2_b.json, runs/code-03-card3_a.json, runs/code-03-card3_b.json, runs/code-03-card4_a.json, runs/code-03-card4_b.json
targets: E1 (crash vs quietly wrong), E4 (which kind of value a sticker holds)
scored: Predict, Trace, Change, Find the bug
code: code/code-03

## Step: Predict

A log is a list of records, and each record is a dict about one call. Positions in a list start at 0.

```python
log = [{"ok": True, "cost": 0.0027}, {"ok": False, "cost": 0.0}, {"ok": True, "cost": 0.0027}]
passed = 0
for row in log:
    if row["ok"]:
        passed = passed + 1
print(passed)
print(log[1])
print(log[1]["cost"] + log[2])
```

**How this code works.** `log` is a list of records, one dict (a set of labelled values) per call, all with the same labels, so one loop can read every record the same way. The `for` loop looks at each record in turn as `row`; `row["ok"]` reads the value under the label `ok`, and when it is True the counter `passed` goes up by one. A number in square brackets after a list picks the item at that position; a label in square brackets after a dict picks the value under that label. The last line adds two things together.

For each of the three print lines, write exactly what it shows, and give one label:

- **crash**: the program stops with an error (write the error's name)
- **quietly wrong**: it runs, but the result is wrong
- **fine**: it runs and the result is right

**Your answer.**

### Key
Real output (runs/code-03-predict.json):

| Line | Shows | Label |
|---|---|---|
| `print(passed)` | `2` | fine |
| `print(log[1])` | `{'ok': False, 'cost': 0.0}` | fine: the whole second record |
| `print(log[1]["cost"] + log[2])` | `TypeError: unsupported operand type(s) for +: 'float' and 'dict'` | crash |

Why the last one crashes (E4): `log[1]["cost"]` is a number, but `log[2]` is a whole dict, and Python cannot add a dict to a number. The fix is `log[2]["cost"]`. If he labels before saying what kind of value each side holds, ask him that first.

Score: lines with both the shown value and the label right, divided by 3.

## Step: Trace

The problem: a summariser writes a note for each invoice, and we need to know how often the note has the right total. The fix: a list of test cases, each with the text the note must include, and a machine that counts. `summarise(case)` is a fake summariser; it leaves the total out for `credit-note-77`.

A rule first. `a in b` asks "is `a` inside `b`?", and what "inside" means depends on `b`:

```python
print("ok" in "it was ok")
print("ok" in {"ok": True})
print(True in {"ok": True})
```
It prints `True`, `True`, `False`. With text, it looks through the letters. With a dict, it looks only at the labels, never the values.

```python
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
```

**How this code works, and why it is built this way.**
- `passed` and `failing` get start values before the loop, so they collect across every case instead of starting over.
- The loop visits each case once. `summarise(case)` makes the note, and the `if` line asks whether the text the case needs is inside that note.
- A case that passes adds one to the count; a case that fails is noted in `failing`, so a person can see which ones to fix, not just how many.
- `return passed, failing` hands both back together, because a count alone would not say which cases failed.

`CASES` holds 3 cases: `scan-000` must include `PKR 80,000`, `credit-note-77` must include `-$310`, `typed-000` must include `$100`. The last line catches the two values handed back, in order, into two stickers.

1. Fill every cell, in the order the lines run. For `case`, write its invoice.

| Pass | After | case | note | passed | failing |
|---|---|---|---|---|---|
| - | (a) | | | | |
| 1 | (b) | | | | |
| 1 | (c) or (d) | | | | |
| 2 | (b) | | | | |
| 2 | (c) or (d) | | | | |
| 3 | (b) | | | | |
| 3 | (c) or (d) | | | | |

2. What kind of value does `failing` hold at the end?
3. One sentence: what is `score` for?

**Your answer.**

### Key
From runs/code-03-table.json:

| Pass | After | case | note | passed | failing |
|---|---|---|---|---|---|
| - | (a) | - | - | 0 | `[]` |
| 1 | (b) | `scan-000` | `'Invoice scan-000, total PKR 80,000.'` | 0 | `[]` |
| 1 | (c) | `scan-000` | same | 1 | `[]` |
| 2 | (b) | `credit-note-77` | `'Invoice credit-note-77, due on receipt.'` | 1 | `[]` |
| 2 | (d) | `credit-note-77` | same | 1 | `['credit-note-77']` |
| 3 | (b) | `typed-000` | `'Invoice typed-000, total $100.'` | 1 | `['credit-note-77']` |
| 3 | (c) | `typed-000` | same | 2 | `['credit-note-77']` |

2: a list of names (pieces of text), because (d) appends `case["invoice"]`, one value from the dict, not the whole `case` (E4).
3: "It counts how many cases get a note that includes the right total, and lists the invoices that did not." The program prints `2 of 3 passed` and `failing: ['credit-note-77']` (runs/code-03-trace.json).

Score: table cells right divided by all table cells. Questions 2 and 3 get feedback but are not in the score.

Simpler: if he does not follow the whole step, send this first (one fewer idea: no `failing` list), from code/code-03/simpler.py:
```python
def score(cases):
    # goal: count the cases whose note has the right total
    passed = 0
    for case in cases:
        note = summarise(case)
        if case["must_include"] in note:
            passed = passed + 1
    return passed
```
It prints `2 of 3 passed` (runs/code-03-simpler.json). Ask: on each pass, what is `note`, and does `passed` go up?

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

**How this code works.** `spend` is a running total: a start value, a loop that visits each record once, a line that adds to the total on every pass, and a return after the loop that hands the total back. The start value is a number, so an empty log still gives a number back. Each record is a dict like the ones in Predict.

The test: `spend(log)` must be `0.0054` for the Predict log, and `spend([])` must be `0.0`.

**Your answer.**

### Key
Order: F, E, C, D, B. Leave out A (code/code-03/parsons.py):
```python
def spend(log):
    total = 0.0
    for row in log:
        total = total + row["cost"]
    return total
```
Run: prints `0.0054`, and the test prints `PASS` (runs/code-03-parsons.json, runs/code-03-test_parsons.json). A adds the whole record (a dict) to a number: crash, `TypeError: unsupported operand type(s) for +: 'float' and 'dict'` (runs/code-03-parsons_wrong.json). `row` is one dict; `row["cost"]` is the number inside it (E4).

Score: Change=1 only if his order passes the test (tutor builds the file and runs `test_parsons.py`) within 2 attempts; otherwise 0.

## Step: Find the bug

Someone rewrote one line of `score`. It runs with no error. The symptom, from a real run: `0 of 3 passed` and `failing: ['scan-000', 'credit-note-77', 'typed-000']`. The summariser did not change, and before the rewrite it was `2 of 3 passed`.

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

**How this code works.** It is `score` from the Trace with the numbered comments taken out: start values, one pass per case, make the note, the pass-or-fail check, then count it or name it, and hand back both. One line was rewritten. Nothing crashes, so the only clue is the pass count.

Fill in the debug card yourself:

- **Symptom** (what is wrong, in numbers):
- **Suspect lines** (which lines decide pass or fail):
- **Hypothesis** (what the wrong line is checking instead):
- **My check** (one thing to print, and what you expect it to show if you are right):
- **Fix** (the one line, rewritten):

I will run your check and show you the output; then I run your fix.

**Your answer.**

### Key
`if case["must_include"] in case:` looks for the total inside the case dict, and `in` on a dict checks only its labels (`invoice`, `must_include`), so no case can pass. `note` is made and never used, which is the clue. Fix:
```python
        if case["must_include"] in note:
```
His check: if he prints both sides for one case, show runs/code-03-bug_probe.json: `labels of case = ['invoice', 'must_include']`, `case["must_include"] in note -> True`, `case["must_include"] in case -> False`. Any other check: add that print to a copy of `bug.py`, record it with `code/record.py`, then show it. After the fix it is back to `2 of 3 passed` (runs/code-03-trace.json). Label: quietly wrong. If his first fix fails, he undoes it before the next.

Score: 1 if his card names the `if` line and his fix brings back `2 of 3 passed`, within 2 hypotheses; otherwise 0.

## Step: Close

Finish this line in your own words: "Next time I see a sticker used in a check or a sum, I will ..."

**Your answer.**

### Key
Something like: "... say what kind of value it holds (a whole list, one dict, one number, one piece of text) before I trust the line." Record his line with `engine.py close`.

## Cold

A new scoring script. Read it, then answer.

```python
TESTS = [
    {"q": "2+2", "want": "4", "got": "4"},
    {"q": "3+3", "want": "6", "got": "7"},
    {"q": "5+1", "want": "6", "got": "6"},
]
right = []
for t in TESTS:
    if t["got"] == t["want"]:
        right.append(t)
print("score:", len(TESTS), "of", len(TESTS))
```

**How this code works.** `TESTS` is a list of test cases, each a dict with the question, the answer wanted and the answer the model gave. The loop keeps the cases where the answer given matches the one wanted, in a separate list, `right`. `len(x)` counts the items in a list. The last line prints the score.

1. What does it print?
2. Label it: crash, quietly wrong, or fine.
3. If it is not fine, write the one line that fixes it.

**Your answer.**

### Key
1. `score: 3 of 3` (runs/code-03-cold.json).
2. Quietly wrong: it counts the whole list `TESTS`, not the list `right`, so a wrong answer still scores.
3. `print("score:", len(right), "of", len(TESTS))`, which prints `score: 2 of 3` (runs/code-03-cold_fixed.json).

Score: parts right divided by 3.

## Cards
- Q: `orders = [{"item": "tea", "qty": 2}, {"item": "jam", "qty": 5}]`. What does `print(orders[1])` show? | A: The whole second dict: `{'item': 'jam', 'qty': 5}`. || Q: `orders = [{"item": "tea", "qty": 2}, {"item": "jam", "qty": 5}]`. What does `print(orders[1]["qty"])` show? | A: `5`: the number under the label in the second dict.
- Q: `total = 0` then `total = total + {"cost": 3}`. Crash, quietly wrong, or fine? | A: Crash: `TypeError`, a dict cannot be added to a number; use the value inside it. || Q: `print(2 + {"x": 1})`. Crash, quietly wrong, or fine? | A: Crash: `TypeError`, a dict cannot be added to a number.
- Q: What does `print("tea" in {"item": "tea"})` show? | A: `False`: `in` on a dict checks only the labels, and "tea" is a value. || Q: What does `print("item" in {"item": "tea"})` show? | A: `True`: `in` on a dict checks the labels, and "item" is a label.
- Q: `names = []`, then for each row of `[{"name": "ali"}, {"name": "sara"}]` the loop runs `names.append(row["name"])`. What does `names` hold? | A: A list of names: `['ali', 'sara']`. || Q: `names = []`, then for each row of `[{"name": "ali"}, {"name": "sara"}]` the loop runs `names.append(row)`. What does `names` hold? | A: A list of whole dicts: `[{'name': 'ali'}, {'name': 'sara'}]`.
- Q: A pass rate falls to zero, but the thing being scored did not change. Where do you look first? | A: At the line that decides pass or fail: print both sides of that check for one case and see which sticker it compares with.
