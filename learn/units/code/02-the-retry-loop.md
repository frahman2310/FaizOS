skill: code
id: code-02
level: 1
title: Asking again after a failure
sources: ../private/research-base/code/research/ericson-2019-adaptive-parsons.md, ../private/research-base/code/research/margulieux-2016-employing-subgoals.md
runs: runs/code-02-predict.json, runs/code-02-trace.json, runs/code-02-table.json, runs/code-02-simpler.json, runs/code-02-parsons_lines.json, runs/code-02-parsons.json, runs/code-02-parsons_wrong.json, runs/code-02-test_parsons.json, runs/code-02-test_parsons-parsons_wrong.json, runs/code-02-bug.json, runs/code-02-bug_probe.json, runs/code-02-cold.json, runs/code-02-cold_fixed.json, runs/code-02-card1_a.json, runs/code-02-card1_b.json, runs/code-02-card2_a.json, runs/code-02-card2_b.json, runs/code-02-card3_a.json, runs/code-02-card3_b.json
targets: E2 (a start line moved inside a loop), E3 (one record per call vs one per try)
scored: Predict, Trace, Change, Find the bug
code: code/code-02

## Step: Predict

A tiny loop. The aim is to count the tries: there is one pause per try, so the count should end at the number of pauses.

```python
PAUSES = [0.2, 0.4, 0.0]      # one pause per try, so the count should end at 3

for pause in PAUSES:
    tries = 0
    tries = tries + 1

print("tries:", tries)
```

**How this code works.** `PAUSES` is a list (items in a fixed order) with one pause for each try. `for pause in PAUSES:` runs the indented lines under it once for each item, with `pause` holding that item. `tries` is the counter: `tries = 0` gives it a value, and `tries = tries + 1` adds one to whatever it holds. The print line is not indented, so it is outside the loop and runs once the loop is done.

Write exactly what it prints, and give one label:

- **crash**: the program stops with an error (write the error's name)
- **quietly wrong**: it runs, but the result is wrong
- **fine**: it runs and the result is right

**Your answer.**

### Key
Prints `tries: 1` (runs/code-02-predict.json). Label: quietly wrong. `tries = 0` is a start line, and it sits inside the loop, so every pass wipes the count and adds 1 again. Moved above the `for` line it would run once and the count would reach 3. This is E2: a start line inside a loop runs on every pass, not once.

Score: 1 if both the printed line and the label are right; half if only one is.

## Step: Trace

The problem: a provider sometimes times out, and one failure should not lose the request. The fix: try again after a pause, and write one record per call. Two new rules: `outcomes.pop(0)` takes the first item out of the list and hands it back (the list gets shorter), and `return` leaves the machine at once, even from inside a loop.

```python
PAUSES = [0.2, 0.4, 0.0]                  # seconds to wait after try 1, 2, 3 fails
outcomes = ["timeout", "ok", "ok"]        # what the fake provider does on each try

def fake_provider(prompt):
    outcome = outcomes.pop(0)
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "rate: " + prompt

def fetch(prompt, records):
    # goal: get one reply, trying again after a failure, and write one record
    # 1. set start values
    tries = 0
    reason = ""
    for pause in PAUSES:
        # 2. try
        tries = tries + 1                                    # (a)
        try:
            text = fake_provider(prompt)                     # (b)
            # 3. record the success and leave
            records.append({"done": True, "tries": tries})   # (c)
            return text
        except RuntimeError as err:
            # 4. note why, wait, go round again
            reason = str(err)                                # (d)
            time.sleep(pause)
    # 5. give up: record the failure once
    records.append({"done": False, "tries": tries, "reason": reason})
    return None

records = []
print(fetch("USD to PKR", records))
```

**How this code works, and why it is built this way.**
- `fake_provider` stands in for the AI company. It takes the next outcome off the list, and for anything but `"ok"` it raises (throws) a `RuntimeError`, which is how a real timeout reaches your code. So it fails and works on cue, offline.
- `try:` and `except RuntimeError as err:` pair up: Python runs the lines under `try`, and if a RuntimeError is raised there it jumps to the lines under `except` instead of crashing. That is what lets one failure be survived.
- The loop gives one try per pause. A try that works writes its record and leaves at once with `return`; a failed try keeps the reason and waits, giving the provider time to recover before the next try.
- `tries` and `reason` get start values before the loop, so they carry across tries. The lines after the loop run only if no try worked; they write the failure record, with the reason, so someone can see why it gave up.
- `records` is made outside and passed in, as `log` was in unit 1, so the records survive after `fetch` is done.

1. Fill every cell, in the order the lines run (`-` for no value yet).

| Pass | After | pause | tries | outcomes | reason | text | records |
|---|---|---|---|---|---|---|---|
| 1 | (a) | | | | | | |
| 1 | (d) | | | | | | |
| 2 | (a) | | | | | | |
| 2 | (b) | | | | | | |
| 2 | (c) | | | | | | |

2. After (d), what kind of value does `err` hold, and what does `reason` hold?
3. What does it print, and how many records are there?
4. One sentence: what is `fetch` for?

**Your answer.**

### Key
From runs/code-02-table.json:

| Pass | After | pause | tries | outcomes | reason | text | records |
|---|---|---|---|---|---|---|---|
| 1 | (a) | `0.2` | 1 | `['timeout', 'ok', 'ok']` | `''` | - | `[]` |
| 1 | (d) | `0.2` | 1 | `['ok', 'ok']` | `'timeout'` | - | `[]` |
| 2 | (a) | `0.4` | 2 | `['ok', 'ok']` | `'timeout'` | - | `[]` |
| 2 | (b) | `0.4` | 2 | `['ok']` | `'timeout'` | `'rate: USD to PKR'` | `[]` |
| 2 | (c) | `0.4` | 2 | `['ok']` | `'timeout'` | `'rate: USD to PKR'` | `[{'done': True, 'tries': 2}]` |

2: `err` holds the error itself, `RuntimeError('timeout')` (its kind is RuntimeError); `reason` holds only its note, the text `'timeout'` (E4).
3: `rate: USD to PKR`; one record, `[{'done': True, 'tries': 2}]` (runs/code-02-trace.json). One call gives one record however many tries it took (E3). Pass 3 never runs: `return text` left the machine.
4: "It asks the provider up to three times, pausing after each failure, and writes one record saying whether the call worked and how many tries it took."

Score: table cells right divided by all table cells. Questions 2 to 4 get feedback but are not in the score.

Simpler: if he does not follow the whole step, send this first (one fewer idea: no error and no pause, the outcomes are just a list), from code/code-02/simpler.py:
```python
def fetch(prompt, records):
    # goal: get one reply, trying again after a failure, and write one record
    tries = 0
    for outcome in ["timeout", "ok"]:
        tries = tries + 1
        if outcome == "ok":
            records.append({"done": True, "tries": tries})
            return "rate: " + prompt
    return None
```
It prints `rate: USD to PKR` and `[{'done': True, 'tries': 2}]` (runs/code-02-simpler.json). Ask: what does `tries` hold on each pass, and why is there no pass after "ok"?

## Step: Change

Put these lines in order under `def fetch(prompt):` to build a loop that tries up to three times and hands back the reply and the number of tries. The indentation is already right. One line does not belong: leave it out and say why.

```python
        tries = tries + 1                        # A
    return None, tries                           # B
        try:                                     # C
    tries = 0                                    # D
            time.sleep(pause)                    # E
        tries = 0                                # F
            return fake_provider(prompt), tries  # G
    for pause in PAUSES:                         # H
        except RuntimeError:                     # I
```

**How this code works.** These are the pieces of `fetch` from the Trace, cut down: no records, and the reply and the number of tries are handed back together, so the caller gets both. `PAUSES` and `fake_provider` are the same as in the Trace. The `try` line and the `except` line pair up: Python runs the lines under `try`, and if the provider raises a RuntimeError it jumps to the lines under `except` instead of crashing. The line that hands back `None` is for when every try failed, so the caller still gets an answer it can check.

New rule: `return x, y` hands back two values together, and Python shows them in round brackets, like `('rate: hi', 2)`. The test (the fake provider times out once, then works): `fetch("hi")` must hand back `('rate: hi', 2)`.

**Your answer.**

### Key
Order: D, H, A, C, G, I, E, B. Leave out F (code/code-02/parsons.py):
```python
def fetch(prompt):
    tries = 0
    for pause in PAUSES:
        tries = tries + 1
        try:
            return fake_provider(prompt), tries
        except RuntimeError:
            time.sleep(pause)
    return None, tries
```
Run: prints `('rate: hi', 2)` and the test prints `PASS` (runs/code-02-parsons.json, runs/code-02-test_parsons.json). F is D's twin moved inside the loop (E2): it resets the count on every pass. With F just above A, it prints `('rate: hi', 1)` and the test fails with `AssertionError` (runs/code-02-parsons_wrong.json, runs/code-02-test_parsons-parsons_wrong.json).

Score: Change=1 only if his order passes the test (tutor builds the file and runs `test_parsons.py`) within 2 attempts; otherwise 0.

## Step: Find the bug

Someone moved one line in `fetch`. It runs with no error. The symptom, counted by the program itself: `calls made: 1`, and the call worked on its second try, but `records: 2` and `records saying failed: 1`.

```python
    for pause in PAUSES:
        tries = tries + 1
        try:
            text = fake_provider(prompt)
            records.append({"done": True, "tries": tries})
            return text
        except RuntimeError as err:
            reason = str(err)
            time.sleep(pause)
        records.append({"done": False, "tries": tries, "reason": reason})
```

**How this code works.** It is the loop from `fetch` in the Trace, with the numbered comments taken out and the start lines above the loop not shown. One line was moved. Nothing crashes, so the only clue is the number of records.

Fill in the debug card yourself:

- **Symptom** (what is wrong, in numbers):
- **Suspect lines** (which lines could write a record):
- **Hypothesis** (why there is an extra record):
- **My check** (one thing to print, and what you expect it to show if you are right):
- **Fix** (the one line, and where it moves):

I will run your check and show you the output; then I run your fix.

**Your answer.**

### Key
The failure record is indented inside the `for` loop, so it runs after every failed try: one record per try instead of one per call (E3). Fix: move `records.append({"done": False, "tries": tries, "reason": reason})` out one level, below the loop, so it runs once, only after every try has failed. His check: if he asks to print `records` after the failure line, show runs/code-02-bug_probe.json: `after the failure line: tries = 1 records = [{'done': False, 'tries': 1, 'reason': 'timeout'}]`. Any other check: add that print to a copy of `bug.py`, record it with `code/record.py`, then show it. After the fix: one record, `[{'done': True, 'tries': 2}]` (runs/code-02-trace.json). Label: quietly wrong. If his first fix fails, he undoes it before the next.

Score: 1 if his card names the failure record line and his fix gives one record, within 2 hypotheses; otherwise 0.

## Step: Close

Finish this line in your own words: "Next time I see a start line or a record line near a loop, I will ..."

**Your answer.**

### Key
Something like: "... ask whether it should run once per call (outside the loop) or once per try (inside it), and count how many times it runs." Record his line with `engine.py close`.

## Cold

A new retry loop. Read it, then answer.

```python
DELAYS = [0.1, 0.3, 0.0]
replies = ["busy", "busy", "ok"]

def ask():
    r = replies.pop(0)
    if r != "ok":
        raise RuntimeError(r)
    return "price 42"

def get(history):
    for delay in DELAYS:
        waited = 0.0
        try:
            value = ask()
            history.append({"worked": True, "waited": waited})
            return value
        except RuntimeError:
            time.sleep(delay)
            waited = waited + delay

history = []
print(get(history))
print(history)
```

**How this code works.** The same shape as `fetch`, with new names. `ask` stands in for the provider: it takes the next reply off the list and raises an error for anything but `"ok"`. `get` gives one try per delay: a try that works writes one record into `history` and leaves, and a failed try pauses and adds that delay to `waited`. `history` is made outside and passed in, so the records are still there after `get` is done.

`waited` is meant to be the total time spent pausing.

1. What does the last line print?
2. Label it: crash, quietly wrong, or fine.
3. If it is not fine, which line moves, and to where?

**Your answer.**

### Key
1. `[{'worked': True, 'waited': 0.0}]` (runs/code-02-cold.json).
2. Quietly wrong: `waited = 0.0` is a start line inside the loop, so the total is wiped on every pass (E2).
3. Move `waited = 0.0` above the `for` line. Then it prints `[{'worked': True, 'waited': 0.4}]` (runs/code-02-cold_fixed.json).

Score: parts right divided by 3.

## Cards
- Q: `for x in [5, 6, 7]:` with `n = 0` and then `n = n + 1` inside it, then `print(n)`, to count the items. What prints, and which label? | A: `1`, quietly wrong: the start line is inside the loop, so it resets on every pass. || Q: `for p in [2, 3, 4]:` with `total = 0` and then `total = total + p` inside it, then `print(total)`, to add the items. What prints, and which label? | A: `4`, quietly wrong: the start line resets the total on every pass, so only the last item counts.
- Q: One call is logged with `for result in ["fail", "fail", "ok"]:` and `records.append(result)` inside the loop. How many records, and is that right? | A: `3`, quietly wrong: one record per try, but it should be one per call. || Q: One call is logged with `for result in ["fail", "ok"]:` and `records.append(result)` inside the loop. How many records, and is that right? | A: `2`, quietly wrong: one record per try, but it should be one per call.
- Q: How many tries does `for pause in [0.1, 0.2, 0.0]:` allow? | A: 3: the loop runs once per item in the list. || Q: How many tries does `for pause in [0.2, 0.0]:` allow? | A: 2: the loop runs once per item in the list.
- Q: Why is the last wait in a backoff list zero? | A: After the last try there is no next try to wait for.
- Q: In a retry loop, why do no more tries run after the one that works? | A: The return line leaves the machine at once, so the rest of the loop and the failure record are skipped.
