skill: code
id: code-01
level: 1
title: Calling an AI model and writing down what it cost and how long it took
sources: ../private/research-base/code/research/xie-2019-theory-of-instruction.md, ../private/research-base/code/research/sentance-2019-primm.md
runs: runs/code-01-predict.json, runs/code-01-trace.json, runs/code-01-change.json, runs/code-01-test_change.json, runs/code-01-test_change-trace.json, runs/code-01-bug.json
targets: E1 (crash vs quietly wrong), E4 (which kind of value a sticker holds)
code: code/code-01/ (predict.py, trace.py, change.py, test_change.py, bug.py)

## Step: Predict

A tiny machine that prices one AI call. The provider charges dollars per million tokens, and tokens are the small pieces of text the model reads (in) and writes (out).

```python
RATES = {"haiku": {"in": 1.00, "out": 5.00}}   # dollars per million tokens

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

print(cost_of("haiku", 1200, 300))
print(cost_of("sonnet", 1200, 300))
```

For each of the two print lines, write exactly what it shows, and give it one label:

- **crash**: the program stops with an error (write the error's name)
- **quietly wrong**: it runs, but the result is wrong
- **fine**: it runs and the result is right

**Your answer.**

### Key
Real output (runs/code-01-predict.json):

| Line | Shows | Label |
|---|---|---|
| `cost_of("haiku", 1200, 300)` | `0.0027` | fine |
| `cost_of("sonnet", 1200, 300)` | `KeyError: 'sonnet'` | crash |

Why: 1200 x 1.00 + 300 x 5.00 = 2700, and 2700 / 1,000,000 = 0.0027. For "sonnet", `RATES[model]` looks for a label the dict does not have, so the program stops at `rate = RATES[model]`. A missing dict label is always a crash, never a quiet wrong. If he wrote "nothing" or a number for line 2, that is E1: mark it and point at the last line of the error.

## Step: Trace

The real pattern: a machine that calls the model and writes one record (a dict describing one call) into a log (a list of records). The network call is replaced by a fake that always takes `0.3` seconds, so it runs offline.

```python
import time

RATES = {"haiku": {"in": 1.00, "out": 5.00}}   # dollars per million tokens

def fake_provider(prompt):
    time.sleep(0.3)                             # pretend the AI takes 0.3 seconds
    return {"text": "reply to: " + prompt, "tokens_in": 1200, "tokens_out": 300}

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

def call(prompt, model, log):
    start = time.time()                                                # (a)
    answer = fake_provider(prompt)                                     # (b)
    ms = round((time.time() - start) * 1000, -2)                       # (c)
    cost = cost_of(model, answer["tokens_in"], answer["tokens_out"])   # (d)
    log.append({"model": model, "ms": ms, "cost": cost})              # (e)
    return answer["text"]                                              # (f)

log = []
text = call("summarise this invoice", "haiku", log)
print(text)
print(log)
```

`time.time()` is a clock reading in seconds; call it T. `round(..., -2)` rounds to the nearest 100.

1. Fill the table: what each sticker holds right after the marked line runs. Write `-` if it has no value yet.

| After | start | answer | ms | cost | log |
|---|---|---|---|---|---|
| (a) | | | | | |
| (b) | | | | | |
| (c) | | | | | |
| (d) | | | | | |
| (e) | | | | | |

2. Write the two lines the program prints.
3. In one sentence: what is `call` for?

**Your answer.**

### Key
| After | start | answer | ms | cost | log |
|---|---|---|---|---|---|
| (a) | T | - | - | - | `[]` |
| (b) | T | the whole dict: `{"text": "reply to: summarise this invoice", "tokens_in": 1200, "tokens_out": 300}` | - | - | `[]` |
| (c) | T | same | `300.0` | - | `[]` |
| (d) | T | same | `300.0` | `0.0027` | `[]` |
| (e) | T | same | `300.0` | `0.0027` | `[{'model': 'haiku', 'ms': 300.0, 'cost': 0.0027}]` |

Printed (runs/code-01-trace.json):
```
reply to: summarise this invoice
[{'model': 'haiku', 'ms': 300.0, 'cost': 0.0027}]
```
Purpose: "It makes one AI call, hands back the reply text, and writes one record of what the call cost and how long it took." E4 check: `answer` holds the whole dict; `text` holds only the one piece of text inside it. The table must be complete; a half table is marked incomplete (Cunningham 2017, in code.md).

## Step: Change

Make every record also hold the total tokens for the call (in plus out). Change or add at most 2 lines inside `call`. Your edit must pass this test (`program` is your edited file):

```python
log = []
program.call("summarise this invoice", "haiku", log)
assert log[0]["tokens"] == 1500
assert log[0]["cost"] == 0.0027
print("PASS")
```

Write the lines you would add or change, and say which marked line they replace or sit next to.

**Your answer.**

### Key
Replace (e) with:
```python
    tokens = answer["tokens_in"] + answer["tokens_out"]
    log.append({"model": model, "ms": ms, "cost": cost, "tokens": tokens})
```
Also right: one line, `"tokens": answer["tokens_in"] + answer["tokens_out"]` inside the dict at (e). Run: the edited file prints `PASS` (runs/code-01-test_change.json); the unedited file fails with `KeyError: 'tokens'` (runs/code-01-test_change-trace.json). Why: the record is built at (e), so a new label goes into that dict. Common wrong edit (E4): `"tokens": answer`, which stores the whole dict instead of a number; the test catches it because a dict is not equal to 1500.

## Step: Find the bug

Someone edited `call`. It runs with no error. The symptom: every Haiku call is now logged at `0.0063` dollars, but the same call cost `0.0027` in the trace above, and the bill is more than double what it should be.

```python
def call(prompt, model, log):
    start = time.time()
    answer = fake_provider(prompt)
    ms = round((time.time() - start) * 1000, -2)
    cost = cost_of(model, answer["tokens_out"], answer["tokens_in"])
    log.append({"model": model, "ms": ms, "cost": cost})
    return answer["text"]
```

1. Your hypothesis: which line is wrong, and what is it doing?
2. The one line to change, rewritten.

**Your answer.**

### Key
The cost line hands the slots over in the wrong order: `tokens_out` (300) goes into the `tokens_in` slot and `tokens_in` (1200) into `tokens_out`, so the 1200 is priced at the output rate. Fix:
```python
    cost = cost_of(model, answer["tokens_in"], answer["tokens_out"])
```
Real run of the buggy file (runs/code-01-bug.json): `[{'model': 'haiku', 'ms': 300.0, 'cost': 0.0063}]`. Label: quietly wrong, not a crash; Python fills slots by position and never checks names.

Debug card:
- Symptom: cost `0.0063` per call, expected `0.0027`.
- Hypothesis: the token counts reach `cost_of` swapped.
- Test: work it by hand both ways: 1200 x 1.00 + 300 x 5.00 = 2700 (right), 300 x 1.00 + 1200 x 5.00 = 6300 (the bug). 6300 / 1,000,000 = 0.0063 matches the symptom.
- Fix: put the slots back in the def line's order; rerun and see `0.0027`.

## Step: Close

Finish this line in your own words: "Next time I see a machine called with several slots, I will ..."

**Your answer.**

### Key
Something like: "... check each value against the def line, in order, because swapped slots run fine and give a wrong number." His line goes into the recall queue.

## Cards
- Q: `RATES = {"haiku": ...}` and the code runs `RATES["sonnet"]`. Crash, quietly wrong, or fine? | A: Crash: `KeyError: 'sonnet'`. A missing dict label always stops the program.
- Q: `cost_of(model, tokens_out, tokens_in)` when the def line is `cost_of(model, tokens_in, tokens_out)`. What happens? | A: Quietly wrong: it runs, but each count is priced at the other count's rate.
- Q: In `answer = fake_provider(prompt)`, what kind of value does `answer` hold? | A: The whole dict (text plus token counts); `answer["text"]` is the one piece of text inside it.
- Q: Why does `call` write the clock reading `start` before the provider line? | A: So the time taken is measured around the call: after minus before.
- Q: How many records does `call` add to the log for one call? | A: Exactly one.
