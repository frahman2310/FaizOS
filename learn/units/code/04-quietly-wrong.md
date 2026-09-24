skill: code
id: code-04
level: 1
title: A call report and a stopwatch
sources: ../private/research-base/code/research/michaeli-romeike-2019-systematic-debugging.md, ../private/research-base/code/research/ko-2019-teaching-explicit-strategies.md
runs: runs/code-04-sort_demo.json, runs/code-04-predict.json, runs/code-04-trace.json, runs/code-04-table.json, runs/code-04-broken.json, runs/code-04-simpler.json, runs/code-04-change.json, runs/code-04-test_change.json, runs/code-04-test_change-trace.json, runs/code-04-bug.json, runs/code-04-fixed.json, runs/code-04-bug_probe.json, runs/code-04-cold.json, runs/code-04-cold_fixed.json, runs/code-04-card1_a.json, runs/code-04-card1_b.json, runs/code-04-card2_a.json, runs/code-04-card2_b.json, runs/code-04-card3_a.json, runs/code-04-card3_b.json
targets: E1 (crash vs quietly wrong vs fine), E2 (a start line inside a loop), E4 (which kind of value a sticker holds); review of code-01 to code-03
scored: Predict, Trace, Change, Find the bug
code: code/code-04

## Step: Predict

Two rules first. A machine that belongs to a list runs only when you put round brackets after its name: `nums.sort()` lines the list up, smallest first, in place. And positions start at 0, so a list of five has positions 0 to 4. A tiny example:

```python
nums = [3, 1, 2]
nums.sort()
print(nums)
```
It prints `[1, 2, 3]`.

Now five call times. The aim of lines A and B is the middle time once the list is lined up.

```python
times = [210, 180, 950, 200, 190]      # ms for five calls; the aim is the middle time
times.sort
print("A", times[2])
times.sort()
print("B", times[2])
print("C", times[5])
```

For each of the three print lines, write exactly what it shows, and give one label:

- **crash**: the program stops with an error (write the error's name)
- **quietly wrong**: it runs, but the result is wrong
- **fine**: it runs and the result is right

**Your answer.**

### Key
Real output (runs/code-04-predict.json):

| Line | Shows | Label |
|---|---|---|
| A | `A 950` | quietly wrong: `times.sort` has no brackets, so it names the machine but never runs it, and position 2 still holds the slowest call |
| B | `B 200` | fine: `times.sort()` ran, so position 2 is the middle time |
| C | `IndexError: list index out of range` (nothing printed) | crash: there is no position 5 in a list of five |

Accept "crash" for the last line with any error name he writes; the name is feedback only.

Score: lines with both the shown value and the label right, divided by 3.

## Step: Trace

The problem: a log holds one record per call, and the team wants to know how many calls worked and how many of those needed a retry. The fix: first keep the calls that worked, then count within them. This version is correct.

```python
LOG = [
    {"ok": True, "tries": 1},
    {"ok": False, "tries": 3},
    {"ok": True, "tries": 2},
]

def report(log):
    # goal: sum up a log: how many calls worked, and how many of those needed a retry
    # 1. keep the calls that worked
    oks = []                                   # (a)
    for row in log:
        if row["ok"]:
            oks.append(row)                    # (b)
    # 2. count the ones that needed more than one try
    retried = 0                                # (c)
    for row in oks:
        if row["tries"] > 1:
            retried = retried + 1              # (d)
    # 3. hand back the summary
    return {"worked": len(oks), "retried": retried}

print(report(LOG))
```

1. Fill every cell, one row for each time a marked line runs, in order. Call the records R1, R2, R3 (top to bottom). `-` means no value yet.

| Order | Line | row | oks | retried |
|---|---|---|---|---|
| 1 | (a) | | | |
| 2 | (b) | | | |
| 3 | (b) | | | |
| 4 | (c) | | | |
| 5 | (d) | | | |

2. What does it print?
3. A broken copy has `for row in log:` in place of `for row in oks:`. Which printed number changes, to what, and which label does the broken copy get?
4. One sentence: what is `report` for?

**Your answer.**

### Key
From runs/code-04-table.json:

| Order | Line | row | oks | retried |
|---|---|---|---|---|
| 1 | (a) | - | `[]` | - |
| 2 | (b) | R1 | `[R1]` | - |
| 3 | (b) | R3 | `[R1, R3]` | - |
| 4 | (c) | R3 | `[R1, R3]` | 0 |
| 5 | (d) | R3 | `[R1, R3]` | 1 |

R2 never reaches (b) because it did not work, and R1 never reaches (d) because it took one try. `row` still holds R3 at (c), left over from the first loop.
2: `{'worked': 2, 'retried': 1}` (runs/code-04-trace.json).
3: `retried` becomes 2: `{'worked': 2, 'retried': 2}` (runs/code-04-broken.json). Quietly wrong: R2 failed after 3 tries, yet it is counted as a call that worked after a retry.
4: "It sums up a log: how many calls worked, and how many of those needed more than one try."

Score: table cells right divided by all table cells. Questions 2 to 4 get feedback but are not in the score.

Simpler: if he does not follow the whole step, send this first (one fewer idea: only the first loop), from code/code-04/simpler.py:
```python
def report(log):
    # goal: count the calls that worked
    oks = []
    for row in log:
        if row["ok"]:
            oks.append(row)
    return {"worked": len(oks)}
```
It prints `{'worked': 2}` (runs/code-04-simpler.json). Ask: which records get into `oks`, and why not R2?

## Step: Change

Make the summary also say how many calls failed. Change one line of `report`. It must pass this test (`program` is your edited file):

```python
summary = program.report(program.LOG)
assert summary["worked"] == 2
assert summary["retried"] == 1
assert summary["failed"] == 1
print("PASS")
```

Write the line as you would rewrite it.

**Your answer.**

### Key
The return line (code/code-04/change.py):
```python
    return {"worked": len(oks), "retried": retried, "failed": len(log) - len(oks)}
```
Run: prints `{'worked': 2, 'retried': 1, 'failed': 1}` and `PASS` (runs/code-04-change.json, runs/code-04-test_change.json). The unedited file fails with `KeyError: 'failed'` (runs/code-04-test_change-trace.json). Other right answers count the records where `row["ok"]` is false; check them the same way: put his line into a copy of `trace.py` and run `test_change.py` on it. Common wrong edit (E4): `"failed": log`, which stores the whole list.

Score: Change=1 only if his edit makes the test print PASS within 2 attempts; otherwise 0.

## Step: Find the bug

A retry loop with a stopwatch. Every try takes the same short time. One line is in the wrong place. The symptom, from a real run: the call failed once and worked on the second try; the user's own stopwatch says `300.0` ms, but the log says `100.0` ms.

```python
def ask(q, log):
    for pause in PAUSES:
        clock = time.time()
        try:
            text = fake_provider(q)
            ms = round((time.time() - clock) * 1000, -2)
            log.append({"ok": True, "ms": ms})
            return text
        except RuntimeError:
            time.sleep(pause)
```

Fill in the debug card yourself:

- **Symptom** (what is wrong, in numbers):
- **Suspect lines** (which lines decide what the time measures):
- **Hypothesis** (why the logged time is too low):
- **My check** (one thing to print, and what you expect it to show if you are right):
- **Fix** (the one line, and where it moves):

I will run your check and show you the output; then I run your fix.

**Your answer.**

### Key
`clock = time.time()` is a start line inside the loop (E2). The clock restarts on every try, so `ms` measures only the last try, not the whole call with the failed try and the pause. Fix: move `clock = time.time()` above the `for` line. His check: if he prints when the clock starts, show runs/code-04-bug_probe.json: `try 1 : clock started 0.0 ms after the user pressed send`, `try 2 : clock started 200.0 ms after the user pressed send`, `logged ms: 100.0`. Any other check: add that print to a copy of `bug.py`, record it with `code/record.py`, then show it. After the fix: `the log says: [{'ok': True, 'ms': 300.0}]`, matching the user (runs/code-04-fixed.json). Label: quietly wrong; retried calls, the slowest ones, look fast. If his first fix fails, he undoes it before the next.

Score: 1 if his card names the clock line and his fix makes the log say `300.0`, within 2 hypotheses; otherwise 0.

## Step: Close

Finish this line in your own words: "Next time code runs with no error, before I trust its numbers I will ..."

**Your answer.**

### Key
Something like: "... check one number against a value I worked out by hand, because quietly wrong code looks exactly like fine code." Record his line with `engine.py close`.

## Cold

A new report. Read it, then answer.

```python
calls = [{"ok": True, "ms": 120}, {"ok": False, "ms": 900}, {"ok": True, "ms": 300}]
good = []
for c in calls:
    if c["ok"]:
        good.append(c)
slowest = 0
for c in calls:
    if c["ms"] > slowest:
        slowest = c["ms"]
print("slowest good call:", slowest)
```

1. What does it print?
2. Label it: crash, quietly wrong, or fine.
3. If it is not fine, write the one line that fixes it.

**Your answer.**

### Key
1. `slowest good call: 900` (runs/code-04-cold.json).
2. Quietly wrong: the second loop walks every call, so the failed call's time is used.
3. The second `for c in calls:` becomes `for c in good:`, which prints `slowest good call: 300` (runs/code-04-cold_fixed.json).

Score: parts right divided by 3.

## Cards
- Q: `names = ["sara", "ali"]`, then `names.sort`, then `print(names)`. What prints, and which label? | A: `['sara', 'ali']`, quietly wrong: with no round brackets the machine is named but never runs. || Q: `nums = [9, 4, 7]`, then `nums.sort`, then `print(nums[0])` to get the smallest. What prints, and which label? | A: `9`, quietly wrong: with no round brackets the list is never lined up.
- Q: `calls = [{"ok": False, "tries": 2}, {"ok": True, "tries": 1}]`, and a loop over `calls` adds 1 to `retried` when `c["tries"] > 1`. It is meant to count calls that worked after a retry. What prints? | A: `1`, quietly wrong: the loop walks every call, so a failed call is counted. || Q: `calls = [{"ok": True, "tries": 3}, {"ok": False, "tries": 2}, {"ok": False, "tries": 4}]`, and a loop over `calls` adds 1 to `retried` when `c["tries"] > 1`. It is meant to count calls that worked after a retry. What prints? | A: `3`, quietly wrong: the loop walks every call, so failed calls are counted.
- Q: `print([4, 5, 6][3])`. Crash, quietly wrong, or fine? | A: Crash: `IndexError`, positions run 0 to 2. || Q: `x = ["a", "b"]`, then `print(x[2])`. Crash, quietly wrong, or fine? | A: Crash: `IndexError`, positions run 0 to 1.
- Q: The stopwatch start line sits inside a retry loop. What does the logged time measure? | A: Only the last try, not the whole call with its failed tries and pauses.
- Q: A program ran to the end with no error. Is its result right? | A: Not proven: check one number against a value worked out by hand, because quietly wrong code runs to the end just like fine code.
