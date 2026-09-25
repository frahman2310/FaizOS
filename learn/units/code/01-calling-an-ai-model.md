skill: code
id: code-01
level: 1
title: One AI call and its record
sources: ../private/research-base/code/research/xie-2019-theory-of-instruction.md, ../private/research-base/code/research/margulieux-2016-employing-subgoals.md
runs: runs/code-01-predict.json, runs/code-01-work.json, runs/code-01-trace.json, runs/code-01-table.json, runs/code-01-simpler.json, runs/code-01-change.json, runs/code-01-test_change.json, runs/code-01-test_change-trace.json, runs/code-01-bug.json, runs/code-01-bug_probe.json, runs/code-01-cold.json, runs/code-01-cold_fixed.json, runs/code-01-card1_a.json, runs/code-01-card1_b.json, runs/code-01-card2_a.json, runs/code-01-card2_b.json, runs/code-01-card3_a.json, runs/code-01-card3_b.json
targets: E1 (crash vs quietly wrong), E4 (which kind of value a sticker holds)
scored: Predict, Trace, Change, Find the bug
code: code/code-01

## Step: Predict

A tiny machine that prices one AI call. Tokens are the small pieces of text the model reads (in) and writes (out), and the provider charges dollars for every `1_000_000` tokens. The underscores in `1_000_000` are only there to make it easy to read; Python ignores them.

```python
RATES = {"haiku": {"in": 1.00, "out": 5.00}}   # dollars per 1_000_000 tokens

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

print(cost_of("haiku", 1200, 300))
print(cost_of("sonnet", 1200, 300))
```

**How this code works.** `RATES` is a dict (a set of labelled values) holding the dollar rates for each model name. `cost_of` looks up the rates for the model it is given, multiplies each token count by its rate, adds the two, and divides by `1_000_000` because the rates are per `1_000_000` tokens. The two print lines use the same machine with two model names.

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

Hand check (runs/code-01-work.json): 1200 x 1 + 300 x 5 = 2700, and 2700 / 1000000 = 0.0027. For "sonnet", `RATES[model]` asks for a label the dict does not have, so Python raises `KeyError` at `rate = RATES[model]`, and the program stops because nothing here catches it (a `try`/`except KeyError` around the line would catch it and the program would carry on). If he wrote "nothing" or a number for line 2, that is E1: point at the last line of the error.

Score: lines with both the shown value and the label right, divided by 2.

## Step: Trace

The problem: a bill arrives and nobody knows which call cost what or took how long. The fix: every call writes one record (a dict about that call) into a log (a list of records). The provider is a fake that waits a moment, so it runs offline. `cost_of` is the machine from Predict. The comments starting with a number are the steps of the pattern.

```python
def fake_provider(prompt):
    time.sleep(0.3)                  # pretend the AI takes a moment
    return {"text": "ok: " + prompt, "tokens_in": 1200, "tokens_out": 300}

def call(prompt, model, log):
    # goal: make one AI call and write one record of what it cost and how long it took
    # 1. start the clock
    start = time.time()                                               # (a)
    # 2. send the request
    answer = fake_provider(prompt)                                    # (b)
    # 3. pull the fields out of the reply
    ms = round((time.time() - start) * 1000, -2)                      # (c)
    cost = cost_of(model, answer["tokens_in"], answer["tokens_out"])  # (d)
    # 4. write the record, then hand back the text
    log.append({"model": model, "ms": ms, "cost": cost})              # (e)
    return answer["text"]

log = []
text = call("hi", "haiku", log)
print(text)
print(log)
```

**How this code works, and why it is built this way.**
- `fake_provider` stands in for the AI company. A real call goes over the internet and costs money; this one only waits a moment and hands back a reply dict shaped like a real one, so it runs offline and free.
- `call` wraps one AI call in the jobs every real call needs, in the order of the numbered comments. The clock is read before the send, so the timing covers the call only. The whole reply is kept, because the text and the token counts are both inside it. The time taken is the second clock reading minus the first, and the price comes from `cost_of` with the reply's token counts. Then one record goes into the log, and only the text is handed back, because the text is what the app shows the user.
- `log` is made once outside `call` (`log = []`) and passed in, so every call adds to the same list and the records survive between calls.
- `time.time()` is a clock reading; call it T. `round(..., -2)` rounds to the nearest 100, so tiny clock differences do not change the result. The fake's wait comes out as `300.0` ms.

1. Fill every cell: what each sticker holds right after the marked line runs. Write `-` if it has no value yet.

| After | prompt | model | start | answer | ms | cost | log |
|---|---|---|---|---|---|---|---|
| (a) | | | | | | | |
| (b) | | | | | | | |
| (c) | | | | | | | |
| (d) | | | | | | | |
| (e) | | | | | | | |

2. While (d) runs, what does `rate` hold inside `cost_of`?
3. Write the two printed lines.
4. In one sentence: what is `call` for?

**Your answer.**

### Key
From runs/code-01-table.json (A = `{'text': 'ok: hi', 'tokens_in': 1200, 'tokens_out': 300}`, the whole reply dict):

| After | prompt | model | start | answer | ms | cost | log |
|---|---|---|---|---|---|---|---|
| (a) | `'hi'` | `'haiku'` | T | - | - | - | `[]` |
| (b) | `'hi'` | `'haiku'` | T | A | - | - | `[]` |
| (c) | `'hi'` | `'haiku'` | T | A | `300.0` | - | `[]` |
| (d) | `'hi'` | `'haiku'` | T | A | `300.0` | `0.0027` | `[]` |
| (e) | `'hi'` | `'haiku'` | T | A | `300.0` | `0.0027` | `[{'model': 'haiku', 'ms': 300.0, 'cost': 0.0027}]` |

2: `rate` holds the inner dict `{'in': 1.0, 'out': 5.0}`, not a number (E4).
3 (runs/code-01-trace.json): `ok: hi`, then `[{'model': 'haiku', 'ms': 300.0, 'cost': 0.0027}]`. `text` holds only the piece of text; `answer` held the whole dict (E4).
4: "It makes one AI call, hands back the reply text, and writes one record of what the call cost and how long it took."

Score: table cells right divided by all table cells (a blank cell is wrong, as a half table is as weak as none: Cunningham, in code.md). Questions 2 to 4 get feedback but are not in the score.

Simpler: if he does not follow the whole step, send this first (one fewer idea: no clock), from code/code-01/simpler.py, then the step's question again:
```python
def call(prompt, log):
    # goal: make one AI call and write one record
    answer = fake_provider(prompt)                     # send the request
    log.append({"tokens_in": answer["tokens_in"]})     # write the record
    return answer["text"]                              # hand back the text
```
It prints `ok: hi` and `[{'tokens_in': 1200}]` (runs/code-01-simpler.json). Ask: after the send line, what does `answer` hold; after the record line, what does `log` hold?

## Step: Change

Make every record also hold the total tokens for the call (in plus out). Change or add at most 2 lines inside `call`. Your edit must pass this test (`program` is your edited file):

```python
log = []
program.call("hi", "haiku", log)
assert log[0]["tokens"] == 1500
assert log[0]["cost"] == 0.0027
print("PASS")
```

**How this test works.** `program` is your edited file, loaded so the test can use your `call`. It makes a fresh empty log, makes one call, then looks at the first record (`log[0]`: position 0 is the first). Each `assert` line checks that one thing is true and stops the test with an `AssertionError` if it is not, so `PASS` prints only when both hold. The second check makes sure your edit did not break the cost.

Write the lines you would add or change, and say which marked line they replace or sit next to.

**Your answer.**

### Key
Replace (e) with (code/code-01/change.py):
```python
    tokens = answer["tokens_in"] + answer["tokens_out"]
    log.append({"model": model, "ms": ms, "cost": cost, "tokens": tokens})
```
Also right: one line, `"tokens": answer["tokens_in"] + answer["tokens_out"]` inside the dict at (e). How to check his edit: put his lines into a copy of `trace.py` and run `test_change.py` on it. The reference edit prints `PASS` (runs/code-01-test_change.json); the unedited file fails with `KeyError: 'tokens'` (runs/code-01-test_change-trace.json). Common wrong edit (E4): `"tokens": answer`, which stores the whole dict; the test catches it.

Score: Change=1 only if his edit makes the test print PASS within 2 attempts; otherwise 0.

## Step: Find the bug

Someone edited `call`. It runs with no error. The symptom: every call is now logged at `0.0063` dollars, but the same call cost `0.0027` in the Trace.

```python
def call(prompt, model, log):
    start = time.time()
    answer = fake_provider(prompt)
    ms = round((time.time() - start) * 1000, -2)
    cost = cost_of(model, answer["tokens_out"], answer["tokens_in"])
    log.append({"model": model, "ms": ms, "cost": cost})
    return answer["text"]
```

**How this code works.** It is the `call` from the Trace with the numbered comments taken out: clock, send, time taken, price, record, hand back the text. One line was edited. Nothing crashes, so the only clue is the wrong number.

Fill in the debug card yourself:

- **Symptom** (what is wrong, in numbers):
- **Suspect lines** (which lines could make that number):
- **Hypothesis** (what the wrong line is doing):
- **My check** (one thing to print, and what you expect it to show if you are right):
- **Fix** (the one line, rewritten):

I will run your check and show you the output; then I run your fix.

**Your answer.**

### Key
The cost line hands the counts over in the wrong order: `tokens_out` goes into the `tokens_in` slot, so the bigger count is priced at the output rate. Fix:
```python
    cost = cost_of(model, answer["tokens_in"], answer["tokens_out"])
```
His check: if he asks to print what reaches `cost_of`, show runs/code-01-bug_probe.json: `cost_of got tokens_in = 300 and tokens_out = 1200`. Any other check: add that print to a copy of `bug.py`, record it with `code/record.py`, then show it. Hand check (runs/code-01-work.json): 300 x 1 + 1200 x 5 = 6300, and 6300 / 1000000 = 0.0063, the symptom. After his fix, run it: the fixed line gives `0.0027` (runs/code-01-trace.json). Label: quietly wrong; Python fills slots by position and never checks names. If his first fix fails, he undoes it before trying the next.

Score: 1 if his card names the cost line as the wrong line and his fix gives `0.0027`, within 2 hypotheses; otherwise 0.

## Step: Close

Finish this line in your own words: "Next time I see a machine called with several slots, I will ..."

**Your answer.**

### Key
Something like: "... check each value against the def line, in order, because swapped slots run fine and give a wrong number." Record his line with `engine.py close`.

## Cold

A new machine. Read it, then answer.

```python
PRICES = {"small": {"in": 2.00, "out": 10.00}}   # dollars per 1_000_000 tokens

def price(size, n_in, n_out):
    p = PRICES[size]
    return (n_in * p["in"] + n_out * p["out"]) / 1_000_000

reply = {"words": "done", "n_in": 4000, "n_out": 500}
bill = []
bill.append({"size": "small", "dollars": price("small", reply["n_in"], reply["n_in"])})
print(bill)
```

**How this code works.** The same pattern as the first machine, with new names. `PRICES` holds the dollar rates for each size, and `price` looks up the rates for a size and works out the dollars. `reply` stands in for one AI reply, and `bill` is a list that collects one record per call.

1. What does it print?
2. Label it: crash, quietly wrong, or fine.
3. If it is not fine, write the one line that fixes it.

**Your answer.**

### Key
1. `[{'size': 'small', 'dollars': 0.048}]` (runs/code-01-cold.json).
2. Quietly wrong: `reply["n_in"]` is handed over twice, so the output slot gets the input count.
3. `bill.append({"size": "small", "dollars": price("small", reply["n_in"], reply["n_out"])})`, which prints `[{'size': 'small', 'dollars': 0.013}]` (runs/code-01-cold_fixed.json).

Score: parts right divided by 3.

## Cards
- Q: `ages = {"ali": 7}` then `print(ages["sara"])`. Crash, quietly wrong, or fine? | A: Crash: `KeyError: 'sara'`. The program stops unless a try/except catches the KeyError. || Q: `stock = {"tea": 12}` then `print(stock["jam"])`. Crash, quietly wrong, or fine? | A: Crash: `KeyError: 'jam'`. The program stops unless a try/except catches the KeyError.
- Q: `def change_due(paid, price): return paid - price`, then `print(change_due(300, 500))` for a 300 bill paid with 500. What prints, and which label? | A: `-200`, quietly wrong: the slots are swapped, so it runs and gives the wrong number. || Q: `def share(total, people): return total / people`, then `print(share(2, 8))` to split 8 between 2 people. What prints, and which label? | A: `0.25`, quietly wrong: the slots are swapped.
- Q: `order = {"item": "tea", "qty": 3}` then `x = order["qty"]`. What kind of value does `x` hold? | A: One number: `3`, the value under the label. || Q: `order = {"item": "tea", "qty": 3}` then `x = order`. What kind of value does `x` hold? | A: The whole dict: `{'item': 'tea', 'qty': 3}`.
- Q: Why does a call read the clock before the send line and again after it? | A: So the time taken is after minus before, measured around the call only.
- Q: How many records should one call add to the log? | A: Exactly one, whatever happened inside the call.
