skill: code
id: code-04
level: 1
title: Quietly wrong: code that runs to the end and gives the wrong answer
sources: ../private/research-base/code/research/michaeli-romeike-2019-systematic-debugging.md, ../private/research-base/code/research/ko-2019-teaching-explicit-strategies.md
runs: runs/code-04-predict.json, runs/code-04-predict_fixed.json, runs/code-04-trace.json, runs/code-04-trace_steps.json, runs/code-04-change.json, runs/code-04-test_change.json, runs/code-04-test_change-trace.json, runs/code-04-bug.json, runs/code-04-fixed.json
targets: E1, E2, E3, E4 mixed (review of units code-01 to code-03)
code: code/code-04/ (predict.py, predict_fixed.py, trace.py, trace_steps.py, change.py, test_change.py, bug.py, fixed.py)

## Step: Predict

Five call times, and the aim is the p50: the middle time when all times are lined up.

```python
times = [210, 180, 950, 200, 190]      # milliseconds for five calls

times.sort
middle = times[len(times) // 2]        # the middle one: the p50
print(middle)
```

`len(times) // 2` is 5 split in two, rounded down: 2, the third spot.

Write exactly what it prints, and give one label:

- **crash**: the program stops with an error
- **quietly wrong**: it runs, but the result is wrong
- **fine**: it runs and the result is right

**Your answer.**

### Key
Prints `950` (runs/code-04-predict.json). Label: quietly wrong. `times.sort` names the machine but does not run it: a machine only runs with brackets. So the list keeps its old order and the third spot holds 950, the slowest call, not the middle one. With `times.sort()` the list is lined up and it prints `200` (runs/code-04-predict_fixed.json). No error appears, which is exactly why it is dangerous (E1).

## Step: Trace

A report over a log of four calls. The program runs to the end, and one number it prints is wrong.

```python
LOG = [
    {"ok": True,  "attempts": 1, "cost": 0.0027},
    {"ok": True,  "attempts": 3, "cost": 0.0027},
    {"ok": False, "attempts": 3, "cost": 0.0},
    {"ok": True,  "attempts": 2, "cost": 0.0027},
]

def report(log):
    oks = []                                       # (a)
    for row in log:
        if row["ok"]:
            oks.append(row)                        # (b)
    retried = 0                                    # (c)
    for row in log:
        if row["attempts"] > 1:
            retried = retried + 1                  # (d)
    spend = 0.0
    for row in log:
        spend = spend + row["cost"]                # (e)
    return {"succeeded": len(oks), "retried": retried,
            "cost per success": round(spend / len(oks), 4)}

print(report(LOG))
```

`retried` is meant to be the number of calls that succeeded on a retry.

1. Fill the table: one row per record, showing what happens to each sticker when that record is visited in each loop.

| Record | added to oks at (b)? | retried after (d) | spend after (e) |
|---|---|---|---|
| 1st | | | |
| 2nd | | | |
| 3rd | | | |
| 4th | | | |

2. Write the printed line. Which number is wrong, and which row of your table shows why?
3. In one sentence: what is `report` for?

**Your answer.**

### Key
| Record | added to oks at (b)? | retried after (d) | spend after (e) |
|---|---|---|---|
| 1st | yes | 0 | `0.0027` |
| 2nd | yes | 1 | `0.0054` |
| 3rd | no | 2 | `0.0054` |
| 4th | yes | 3 | `0.0081` |

Printed (runs/code-04-trace.json): `{'succeeded': 3, 'retried': 3, 'cost per success': 0.0027}`. Spend values from runs/code-04-trace_steps.json. The wrong number is `retried: 3`; the 3rd row shows it: that call failed, yet `retried` went up, because the second loop walks `log` (every call) instead of `oks` (the calls that worked). Right answer: 2. Label: quietly wrong.
Purpose: "It sums up a log: how many calls worked, how many needed a retry to work, and the cost per call that worked."

## Step: Change

Fix `report` so that `retried` counts only calls that succeeded after more than one try. Change one line. It must pass this test (`program` is your edited file):

```python
summary = program.report(program.LOG)
assert summary["succeeded"] == 3
assert summary["retried"] == 2
assert summary["cost per success"] == 0.0027
print("PASS")
```

Write the line as you would rewrite it, and say which marked line it sits above.

**Your answer.**

### Key
The loop line above (d), second loop:
```python
    for row in oks:
```
Run: prints `{'succeeded': 3, 'retried': 2, 'cost per success': 0.0027}` and `PASS` (runs/code-04-change.json, runs/code-04-test_change.json). The unedited file fails at `assert summary["retried"] == 2` with `AssertionError` (runs/code-04-test_change-trace.json). Also right: keep `for row in log:` and change the check to `if row["ok"] and row["attempts"] > 1:` (same result; one line). This is meter.py's own choice: it loops over `oks` for the retry count.

## Step: Find the bug

The retry loop again, now with timing. Every try takes `0.3` seconds, and the waits are the backoff from before. One line is in the wrong place. The symptom, from a real run: a call failed twice and worked on the third try. The user's own stopwatch says they waited `2400.0` ms, but the log says `300.0` ms.

```python
def call(prompt, log):
    for wait in BACKOFF:
        start = time.time()
        try:
            text = fake_provider(prompt)
            ms = round((time.time() - start) * 1000, -2)
            log.append({"ok": True, "ms": ms})
            return text
        except RuntimeError:
            time.sleep(wait)
```

1. Your hypothesis: which line is wrong, and why is the logged time so low?
2. The one line to change.

**Your answer.**

### Key
`start = time.time()` is a start line inside the loop (E2). The clock restarts at the top of every try, so `ms` measures only the last try (0.3 s), not the whole call with its two failed tries and two waits. Fix: move `start = time.time()` above the `for` line, so the clock starts once per call.
Real runs: buggy file `the log says: [{'ok': True, 'ms': 300.0}]` (runs/code-04-bug.json); after the move, `the log says: [{'ok': True, 'ms': 2400.0}]`, matching the user's `2400.0` (runs/code-04-fixed.json). Hand check: 0.3 + 0.5 + 0.3 + 1.0 + 0.3 = 2.4 seconds. Label: quietly wrong. It is dangerous because retried calls, the slowest ones, look fast, so the p95 would look healthy while users wait.

Debug card:
- Symptom: log says 300 ms, the user waited 2400 ms.
- Hypothesis: the clock starts inside the loop, so only the last try is timed.
- Test: the logged 300 equals one try's 0.3 s exactly; the gap, 2100 ms, is two failed tries plus both waits.
- Fix: move the start line above the loop; rerun and see 2400.

## Step: Close

Finish this line in your own words: "Next time code runs with no error, before I trust its numbers I will ..."

**Your answer.**

### Key
Something like: "... check one number against a value I worked out by hand, because quietly wrong code looks exactly like fine code." His line goes into the recall queue.

## Cards
- Q: `times.sort` with no brackets. What happens to the list? | A: Nothing: the machine is named but not run, so the list keeps its order. Quietly wrong, no crash.
- Q: A report counts "succeeded on retry" by looping over every record, not only the ones that worked. What goes wrong? | A: Calls that failed after several tries are counted as retried successes. Quietly wrong.
- Q: `start = time.time()` sits inside the retry loop. What does the logged time measure? | A: Only the last try, not the whole call with its failed tries and waits.
- Q: The code ran with no error. Is the result right? | A: Not proven: check one number by hand, because quietly wrong code runs to the end just like fine code.
- Q: Which three places hide most quietly wrong bugs so far? | A: A start line inside a loop, a log line in the wrong loop (per try vs per call), and a sticker holding the wrong kind of value.
