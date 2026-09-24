skill: code
id: code-02
level: 1
title: The retry loop: try again, wait longer, write one record per call
sources: ../private/research-base/code/research/ericson-2019-adaptive-parsons.md, ../private/research-base/code/research/xie-2019-theory-of-instruction.md
runs: runs/code-02-predict.json, runs/code-02-trace.json, runs/code-02-parsons.json, runs/code-02-parsons_wrong.json, runs/code-02-test_parsons.json, runs/code-02-test_parsons-parsons_wrong.json, runs/code-02-bug.json
targets: E2 (a start line moved inside a loop), E3 (one record per call vs one per try)
code: code/code-02/ (predict.py, trace.py, parsons.py, parsons_wrong.py, test_parsons.py, bug.py)

## Step: Predict

A tiny loop. The aim is to count the tries: there is one wait per try, so the count should end at the number of waits.

```python
BACKOFF = [0.5, 1.0, 0.0]      # one wait per try, so three tries

for wait in BACKOFF:
    attempts = 0
    attempts = attempts + 1

print(attempts)
```

Write exactly what it prints, and give one label:

- **crash**: the program stops with an error
- **quietly wrong**: it runs, but the result is wrong
- **fine**: it runs and the result is right

**Your answer.**

### Key
Prints `1` (runs/code-02-predict.json). Label: quietly wrong. `attempts = 0` is a start line, and it sits inside the loop, so every pass wipes the count and adds 1 again: 0 then 1, three times over. The fix is to move `attempts = 0` above the `for` line; that shape counts to 3 (the correct program in Change prints `('reply to: hi', 3)`, runs/code-02-parsons.json). This is E2: a start line inside a loop runs on every pass, not once.

## Step: Trace

The retry loop from the meter. The fake provider follows a script: it fails, fails, then works. `script.pop(0)` takes the first item out of the list and hands it back. `raise` stops the try with an error, and `except` catches it.

```python
import time

BACKOFF = [0.5, 1.0, 0.0]                             # seconds to wait after try 1, 2, 3 fails
script = ["529 overloaded", "529 overloaded", "ok"]   # what the fake provider does on each try

def fake_provider(prompt):
    outcome = script.pop(0)              # take the first item out of the list
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "reply to: " + prompt

def call(prompt, log):
    attempts = 0                                          # (a)
    why = ""
    for wait in BACKOFF:
        attempts = attempts + 1                           # (b)
        try:
            text = fake_provider(prompt)                  # (c)
            log.append({"ok": True, "attempts": attempts})   # (d)
            return text
        except RuntimeError as err:
            why = str(err)                                # (e)
            time.sleep(wait)                              # (f)
    log.append({"ok": False, "attempts": attempts, "why": why})
    return None

log = []
print(call("summarise this invoice", log))
print(log)
```

1. Fill the table: what each sticker holds right after the named line, on each pass of the loop.

| Pass | After | wait | attempts | why | log |
|---|---|---|---|---|---|
| 1 | (b) | | | | |
| 1 | (e) | | | | |
| 2 | (b) | | | | |
| 2 | (e) | | | | |
| 3 | (b) | | | | |
| 3 | (d) | | | | |

2. Write the two printed lines. How many records are in `log`?
3. In one sentence: what is `call` for?

**Your answer.**

### Key
| Pass | After | wait | attempts | why | log |
|---|---|---|---|---|---|
| 1 | (b) | `0.5` | 1 | `""` | `[]` |
| 1 | (e) | `0.5` | 1 | `"529 overloaded"` | `[]` |
| 2 | (b) | `1.0` | 2 | `"529 overloaded"` | `[]` |
| 2 | (e) | `1.0` | 2 | `"529 overloaded"` | `[]` |
| 3 | (b) | `0.0` | 3 | `"529 overloaded"` | `[]` |
| 3 | (d) | `0.0` | 3 | `"529 overloaded"` | `[{'ok': True, 'attempts': 3}]` |

Printed (runs/code-02-trace.json): `reply to: summarise this invoice`, then `[{'ok': True, 'attempts': 3}]`. One record: one call gives one record, however many tries it took (E3). The failure record after the loop never runs, because `return text` leaves the machine on pass 3. (f) sleeps 0.5 s after try 1 and 1.0 s after try 2: the wait gets longer each time (backoff).
Purpose: "It tries the call up to three times, waiting longer after each failure, and writes one record saying whether the call worked and how many tries it took."

## Step: Change

Put these lines in order under `def call(prompt):` to build a loop that tries up to three times and hands back the reply and the number of tries. The indentation is already right. One line does not belong: leave it out and say why.

```python
        attempts = attempts + 1                    # A
    return None, attempts                          # B
        try:                                       # C
    attempts = 0                                   # D
            time.sleep(wait)                       # E
        attempts = 0                               # F
            return fake_provider(prompt), attempts # G
    for wait in BACKOFF:                           # H
        except RuntimeError:                       # I
```

The test (the fake provider fails twice, then works): `call("hi")` must hand back `("reply to: hi", 3)`.

**Your answer.**

### Key
Order: D, H, A, C, G, I, E, B. Leave out F.
```python
def call(prompt):
    attempts = 0
    for wait in BACKOFF:
        attempts = attempts + 1
        try:
            return fake_provider(prompt), attempts
        except RuntimeError:
            time.sleep(wait)
    return None, attempts
```
Run: prints `('reply to: hi', 3)` and the test prints `PASS` (runs/code-02-parsons.json, runs/code-02-test_parsons.json). F is D's twin moved inside the loop (E2): it resets the count on every pass. With F placed just above A, the program prints `('reply to: hi', 1)` and the test fails with `AssertionError` (runs/code-02-parsons_wrong.json, runs/code-02-test_parsons-parsons_wrong.json). Same text, different indentation, different result.

## Step: Find the bug

Someone moved one line in `call`. It runs with no error. The symptom, from a real run: 1 call was made and it worked on the third try, but the log holds 3 records, and 2 of them say the call failed.

```python
    for wait in BACKOFF:
        attempts = attempts + 1
        try:
            text = fake_provider(prompt)
            log.append({"ok": True, "attempts": attempts})
            return text
        except RuntimeError as err:
            why = str(err)
            time.sleep(wait)
        log.append({"ok": False, "attempts": attempts, "why": why})
```

1. Your hypothesis: which line is wrong, and why does it give 3 records?
2. The one line to change.

**Your answer.**

### Key
The last line, the failure record, is indented inside the `for` loop. It runs after every failed try, so the log gets one record per try instead of one per call (E3): a failed record for try 1, a failed record for try 2, then the success record for try 3. Fix: move it out of the loop by one level of indentation, so it runs once, only after all three tries have failed:
```python
    log.append({"ok": False, "attempts": attempts, "why": why})
```
Real run of the buggy file (runs/code-02-bug.json): `records in log: 3`, `records saying failed: 2`. With the line outside the loop, the same script gives one record, `[{'ok': True, 'attempts': 3}]` (runs/code-02-trace.json). Label: quietly wrong; a report built on this log would count 3 calls and a failure rate of 2 in 3 for a call that worked.

Debug card:
- Symptom: 3 records for 1 call; 2 say failed though the call worked.
- Hypothesis: the failure record is written inside the loop, once per failed try.
- Test: count the failed tries in the script (2) and compare with the failed records (2): they match, so the line runs per try.
- Fix: un-indent the line to sit after the loop; rerun and see 1 record.

## Step: Close

Finish this line in your own words: "Next time I see a start line or a log line near a loop, I will ..."

**Your answer.**

### Key
Something like: "... ask whether it should run once per call (outside the loop) or once per try (inside it), and count how many times it runs with three tries." His line goes into the recall queue.

## Cards
- Q: A start line such as `attempts = 0` sits inside the loop. What happens? | A: It resets on every pass, so only the last pass counts. Quietly wrong, no crash.
- Q: A call fails twice and works on the third try. How many records should the log get? | A: One. One record per call, not per try.
- Q: The failure `log.append(...)` is indented inside the retry loop. What does the log show for fail, fail, ok? | A: Three records: two failed and one ok, for a single call that worked.
- Q: What does `BACKOFF = [0.5, 1.0, 0.0]` do in the retry loop? | A: It sets how long to wait after each failed try, getting longer each time; the loop also runs once per item, so it sets the number of tries.
- Q: Why does the loop stop after the try that works? | A: `return text` leaves the machine at once, so no more passes run and the failure record is skipped.
