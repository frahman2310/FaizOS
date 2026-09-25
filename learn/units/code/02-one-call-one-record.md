skill: code
id: code-02
level: 1
title: One call, one record in a log
builds on: code-01
pattern: 1. Make the log once, before any call. 2. Call and keep the reply. 3. Build one record from the reply, one key at a time. 4. Append the record, then return the text.
sources: ../private/research-base/code/research/xie-2019-theory-of-instruction.md, ../private/research-base/code/research/subgoals-how-do-i-use-subgoals.md, ../private/research-base/code/research/ericson-2019-adaptive-parsons.md
runs: runs/code-02-flash1_a.json, runs/code-02-flash1_b.json, runs/code-02-help_try1.json, runs/code-02-help_try1_trace.json, runs/code-02-help_try2.json, runs/code-02-help_try2_trace.json, runs/code-02-help_try3.json, runs/code-02-help_turn.json, runs/code-02-help_turn_b.json, runs/code-02-later_a.json, runs/code-02-later_b.json, runs/code-02-later_c.json, runs/code-02-retry_a.json, runs/code-02-retry_b.json, runs/code-02-retry_c.json, runs/code-02-show1.json, runs/code-02-show1_trace.json, runs/code-02-show2.json, runs/code-02-show2_trace.json, runs/code-02-show3.json, runs/code-02-show3_trace.json, runs/code-02-try1.json, runs/code-02-try1_trace.json, runs/code-02-try2.json, runs/code-02-try2_trace.json, runs/code-02-try3.json, runs/code-02-try3_wrong.json, runs/code-02-turn_a.json, runs/code-02-turn_b.json, runs/code-02-turn_c.json
code: code/code-02/flash1_a.py, code/code-02/flash1_b.py, code/code-02/help_try1.py, code/code-02/help_try1_trace.py, code/code-02/help_try2.py, code/code-02/help_try2_trace.py, code/code-02/help_try3.py, code/code-02/help_turn.py, code/code-02/help_turn_b.py, code/code-02/later_a.py, code/code-02/later_b.py, code/code-02/later_c.py, code/code-02/retry_a.py, code/code-02/retry_b.py, code/code-02/retry_c.py, code/code-02/show1.py, code/code-02/show1_trace.py, code/code-02/show2.py, code/code-02/show2_trace.py, code/code-02/show3.py, code/code-02/show3_trace.py, code/code-02/try1.py, code/code-02/try1_trace.py, code/code-02/try2.py, code/code-02/try2_trace.py, code/code-02/try3.py, code/code-02/try3_wrong.py, code/code-02/turn_a.py, code/code-02/turn_b.py, code/code-02/turn_c.py
targets: E3 (one record per call), E4 (the record vs the reply vs the text)
scored: Your turn

## Step: Goal

**Goal: one call, one record in a log**

Last time you read values out of an AI reply, one key at a time. Today your code keeps a note of every call it makes.

The problem: at the end of the month the AI bill arrives, and nobody can say which request used how much. The fix: every time the code calls the AI, it writes one **record** (a dict about that one call, like one line in a ledger) into a **log** (a list that collects the records, like the ledger book itself).

Four steps, the same every time. You will see them under every exercise:

1. **Make the log once**, before any call: an empty list.
2. **Call and keep** the reply, as in the last unit.
3. **Build one record** from the reply, one key at a time.
4. **Append** the record to the log (add it at the end), then **return** the text.

The rule the whole unit is built around: one call writes exactly one record.

Same order as last time: I show a small example, you try one with me, three times, each adding one idea. Only the last exercise is marked.

Reply "ready", or ask about any word above.

**Your answer.**

### Key
Kind: show
New: record, log, the four pattern steps (subgoal labels)
No question to mark. If he asks about a word, answer from this message and code-01 only, then move to Show 1.

## Step: Show 1

**Show 1: a list that grows**

```python
log = []
log.append({"amount": 500})
log.append({"amount": 120})
print(len(log))
print(log[1])
```
It prints:
```output
2
{'amount': 120}
```

**How this code works, line by line.**
- Line 1: `[]` is an empty list, a list with nothing in it yet. `log` now holds it: a new ledger with no lines.
- Line 2: `log.append(...)` adds one item to the end of `log`. The dot means "do this to `log`"; `append` is a function every list has. The item here is a small dict. After line 2, `log` holds one item.
- Line 3 adds a second dict at the end. The first one stays where it was, unchanged.
- Line 4: `len(log)` counts the items in the list, and `print` shows the count.
- Line 5: `log[1]` is the item at position `1`. Positions count from `0`, as in the last unit, so position `1` is the **second** item.

| After line | `log` holds | Items in `log` |
|---|---|---|
| 1 | `[]` | 0 |
| 2 | `[{'amount': 500}]` | 1 |
| 3 | `[{'amount': 500}, {'amount': 120}]` | 2 |

Why it is built this way: a log only grows. Each append adds one line at the bottom, and nothing already written changes.

**One line from you:** why does `log[1]` show the dict with `120`, not the one with `500`?

**Your answer.**

### Key
Kind: show
New: empty list, append adds one item to the end, len counts the items
Unscored. Like: positions start at `0`, so `log[1]` is the second item, the second one appended (runs/code-02-show1_trace.json).

## Step: Try with me 1

**Try with me 1**

```python
sales = []
sales.append({"item": "chai", "price": 60})
sales.append({"item": "samosa", "price": 40})
sales.append({"item": "chai", "price": 60})
print(len(sales))
```

**How this code works.** Line 1 makes an empty list called `sales`. Lines 2, 3 and 4 each append one dict to the end of it. Line 5 counts the items in `sales` and prints the count.

| After line | `sales` holds | Items |
|---|---|---|
| 1 | `[]` | 0 |
| 2 | `[{'item': 'chai', 'price': 60}]` | 1 |
| 3 | `[{'item': 'chai', 'price': 60}, {'item': 'samosa', 'price': 40}]` | 2 |
| 4 | ? | ? |

1. Fill row 4 (for `sales`, "the same two, plus ..." is enough).
2. What does line 5 print?
   A) `3`
   B) `2`, because the second chai replaces the first
   C) `160`, the prices added up
   D) the whole list

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-02-try1_trace.json:
1. Row 4: the same two dicts, plus `{'item': 'chai', 'price': 60}` at the end; items `3`.
2. A, `3`.
Wrong options: B = thinks a list merges equal items; C = counting mixed up with adding; D = E4 (the list vs its count).
Two options: after line 4, does `sales` hold 2 items (the second chai replaced the first) or 3 items (every append adds one)?
Worked answer: line 1 makes an empty list. Each `append` adds one item at the end and changes nothing already there (Show 1). Lines 2, 3 and 4 are three appends, so after line 4 `sales` holds the same two dicts plus `{'item': 'chai', 'price': 60}` at the end: 3 items, even though two look the same. `len` counts items, it does not add prices, so line 5 prints `3`: option A.
Wrong twice: stuck order, then Help: Try with me 1.

## Step: Show 2

**Show 2: a record built from a reply**

```python
reply = {"text": "Paid", "usage": {"input_tokens": 11, "output_tokens": 2}}
record = {"text": reply["text"], "tokens_out": reply["usage"]["output_tokens"]}
log = []
log.append(record)
print(log)
```
It prints:
```output
[{'text': 'Paid', 'tokens_out': 2}]
```

**How this code works, line by line.**
- Line 1: a reply dict like the last unit's stand-in: the text, plus a `usage` dict of counts.
- Line 2 builds a new dict called `record`. For each key, Python first works out the value after the `:`. `reply["text"]` gives `'Paid'`. `reply["usage"]["output_tokens"]` goes one key at a time and gives `2`. The key names in the record, like `tokens_out`, are yours to choose; the values come out of the reply.
- Line 3 makes the empty log. Line 4 appends the record to it.
- Line 5 prints the log: square brackets outside (a list), curly brackets inside (one dict in it).

| After line | `record` holds | `log` holds |
|---|---|---|
| 2 | `{'text': 'Paid', 'tokens_out': 2}` | nothing yet |
| 3 | the same | `[]` |
| 4 | the same | `[{'text': 'Paid', 'tokens_out': 2}]` |

Why it is built this way: the reply carries more than you need. The record keeps only what you will want when the bill comes, like copying the date and amount off a bank slip into your ledger.

**One line from you:** in line 2, why does `tokens_out` hold `2`, and not the whole `usage` dict?

**Your answer.**

### Key
Kind: show
New: a dict built from looked-up values, a list holding dicts
Unscored. Like: the lookup goes past `usage` into `output_tokens`, so it hands back the number (runs/code-02-show2_trace.json).

## Step: Try with me 2

**Try with me 2**

```python
reply = {"text": "Due Friday", "usage": {"input_tokens": 15, "output_tokens": 3}}
record = {"text": reply["text"], "tokens_in": reply["usage"]["input_tokens"]}
log = []
log.append(record)
print(log[0]["tokens_in"])
```

**How this code works.** Line 1 is the reply. Line 2 builds a record from two lookups into it. Line 3 makes an empty log and line 4 appends the record. Line 5 goes one step at a time: `log[0]` takes the first item of the log, then `["tokens_in"]` looks up one key in it, and `print` shows the result.

| After line | `record` holds | `log` holds |
|---|---|---|
| 2 | `{'text': 'Due Friday', 'tokens_in': 15}` | nothing yet |
| 3 | the same | `[]` |
| 4 | the same | ? |

1. Fill the `?`.
2. What does line 5 print?

Steps on hand: make the log once, call and keep, build one record, append then return.

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-02-try2_trace.json:
1. `[{'text': 'Due Friday', 'tokens_in': 15}]` (a list with the one record in it; exact quotes do not matter).
2. `15`.
Slips: the record without the list brackets (E4: the list vs the item in it); `3` (the output count, the wrong key).
Two options: after line 4, does `log` hold the record `{'text': 'Due Friday', 'tokens_in': 15}` by itself, or a list with that record inside it?
Worked answer: line 3 makes `log` an empty list, `[]`. Line 4 appends the record, so `log` is a list with one item: `[{'text': 'Due Friday', 'tokens_in': 15}]`, square brackets outside, curly inside (Show 2, last row). Line 5: `log[0]` takes the first item, the record; `["tokens_in"]` looks up one key in it and hands back `15`. So it prints `15`. (`3` is the output count, under a key the record never copied.)
Wrong twice: stuck order, then Help: Try with me 2.

## Step: Show 3

**Show 3: the whole pattern in one function**

```python
def fake_model(prompt):
    return {"text": "Done", "usage": {"input_tokens": 6, "output_tokens": 4}}

def ask(prompt, log):
    reply = fake_model(prompt)
    record = {"prompt": prompt, "tokens_out": reply["usage"]["output_tokens"]}
    log.append(record)
    return reply["text"]

log = []
first = ask("pay rent", log)
second = ask("pay school fees", log)
print(second)
print(log)
```
```output
Done
[{'prompt': 'pay rent', 'tokens_out': 4}, {'prompt': 'pay school fees', 'tokens_out': 4}]
```

**How this code works, in the order it runs.**
- `fake_model` is the last unit's stand-in: it hands back a reply dict.
- `def ask(prompt, log):` defines a function with two arguments, split by a comma: the question, and the log to write in. Nothing runs yet.
- `log = []` runs once, before any call (step 1).
- `first = ask("pay rent", log)` runs `ask`. Its four lines are steps 2 to 4: call and keep; build one record; append it; return the text. Order matters: each line uses a name the line above made. `return` goes last because it ends the function; a line under it would never run.
- Inside `ask`, `log` is another name for the same list, not a copy, so the appended record is still there after `ask` returns. Picture handing your ledger to a clerk: he writes one line in it and hands you back an answer.
- The second call does the same: one more record. `first` and `second` each hold only the text (this program prints only `second`).

| After | `first` / `second` | Records in `log` |
|---|---|---|
| first call | `first` holds `'Done'` | 1 |
| second call | `second` holds `'Done'` | 2 |

**One line from you:** `ask` hands back only the text, never the log. Why does `log` still hold both records at the end?

**Your answer.**

### Key
Kind: show
New: a function with two arguments, the same list passed in (not a copy), return ends the function so it goes last
Unscored. Like: inside `ask`, `log` is the same list, not a copy, so each append lands in the one log made at the top (runs/code-02-show3.json, runs/code-02-show3_trace.json).

## Step: Try with me 3

**Try with me 3**

A new function, `note`. Aim: each call writes one record (the question and its input count) into the log, and hands back the text. Everything except its body is fixed:

```python
def fake_model(prompt):
    return {"text": "Booked", "usage": {"input_tokens": 8, "output_tokens": 3}}

def note(question, log):
    # the body goes here

log = []
print(note("book a table", log))
print(log)
```

Its body lines are shuffled below, with one extra line that does not belong. They are shown without their indent (the spaces that mark a line as inside the function):

```python
# P
log.append(record)
# Q
return reply["text"]
# R
reply = fake_model(question)
# S
record = {"question": question, "tokens_in": reply["usage"]["input_tokens"]}
# T
log.append(reply)
```

**How this code works.** The fixed part is Show 3's shape: the stand-in, the empty log made once, one call, then the text and the log printed. `print(note(...))` runs `note` first, then prints what it hands back. Each shuffled line does one job: calling the stand-in and keeping the reply, building a record, appending something, or handing back the text.

Write the four letters in order, then name the extra line and say what would go wrong with it.

Steps on hand: make the log once, call and keep, build one record, append then return.

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-02-try3.json: R, S, P, Q prints `Booked` then `[{'question': 'book a table', 'tokens_in': 8}]`.
T is extra: it appends the whole reply, not the record. It still runs (runs/code-02-try3_wrong.json shows the log holding `{'text': 'Booked', 'usage': {'input_tokens': 8, 'output_tokens': 3}}`), so it is quietly wrong (E4).
Slips: Q before P (the append would never run); S before R (`reply` not made yet).
Two options: which comes first inside `note`, R (makes `reply`) or S (reads `reply` to build `record`)?
Worked answer: order each line by what it needs. S looks inside `reply`, so R, which makes `reply`, must come before it: R, then S. P appends `record`, so it comes after S. Q is `return`, which ends the function, so it goes last; a line under it would never run (Show 3). Order: R, S, P, Q. T appends `reply`, the whole reply, not the small record: the program still runs and the log fills up, but with the wrong thing, so it is quietly wrong.
Wrong twice: stuck order, then Help: Try with me 3.

## Step: Your turn

**Your turn (this one is marked)**

```python
def fake_model(prompt):
    return {"text": "Filed", "usage": {"input_tokens": 9, "output_tokens": 2}}

def ask(question, log):
    reply = fake_model(question)
    record = {"question": question, "tokens_in": reply["usage"]["input_tokens"]}
    log.append(record)
    return reply["text"]

log = []
first = ask("file tax return", log)
print(log)
second = ask("check refund", log)
print(second)
print(len(log))
print(log[1]["question"])
```

**How this code works.** The same pattern as Show 3: one empty log made once, then two calls to `ask`, each of which builds one record, appends it and hands back the text. The prints check the log after the first call, then the second text, the count and one key of the record at position `1`.

1. Write what each of the four prints shows.

Now two changed copies. In each, one line inside `ask` is different; everything else is as above. Labels as in the last unit: crash (stops with an error), quietly wrong (runs, but misses the aim), fine (meets the aim). Each changed line keeps the original line's aim.

```python
# B: the record line is now
record = {"question": question, "tokens_in": reply["input_tokens"]}
```
```python
# C: the return line is now
return record  # aim: hand back the text of the reply
```

2. For B: what it shows, its label, and the fixed line.
3. For C: what `print(second)` shows, its label, and the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-02-turn_a.json, turn_b.json, turn_c.json:
1. `[{'question': 'file tax return', 'tokens_in': 9}]`; `Filed`; `2`; `check refund` (4 parts).
2. B shows `KeyError: 'input_tokens'` (on the first call, before any print); crash; fix: put back `reply["usage"]["input_tokens"]` (3 parts).
3. C: `print(second)` shows `{'question': 'check refund', 'tokens_in': 9}`; quietly wrong (E4: the record, not the text; the log is still right); fix `return reply["text"]` (3 parts).
Exact quotes and spacing do not matter; the value and the kind (list, dict, number, text) do.
Two options: for the part he is stuck on, is the value a list, a dict or the text? For B and C: does it stop with an error, or run and miss its aim?
Worked answer: 1. After the first call `log` holds one record, so `print(log)` shows `[{'question': 'file tax return', 'tokens_in': 9}]`. The second call returns the text, so `print(second)` shows `Filed`. Two calls, two records: `len(log)` is `2`. `log[1]` is the second record, and its `question` is `check refund`. 2. B asks `reply` for `input_tokens`, but that key sits inside `usage`; the first call stops with `KeyError: 'input_tokens'` before any print runs: crash; fix `reply["usage"]["input_tokens"]`. 3. C returns `record`, so `second` holds `{'question': 'check refund', 'tokens_in': 9}` instead of the text: it runs, quietly wrong; fix `return reply["text"]`.
Score: 10 parts; right parts over 10.

## Step: Close

**Close**

Finish this sentence in your own words: "Next time my code calls an AI, I ..."

**Your answer.**

### Key
Kind: close
Like: "... make the log once before any call, and each call builds one record from the reply, appends it, then returns only the text." Record with engine.py close.

## Help: Try with me 1

**Help for Try with me 1: one more worked example**

```python
fees = []
fees.append({"month": "Jan", "paid": 3000})
fees.append({"month": "Feb", "paid": 3000})
print(len(fees))
print(fees[0])
```
```output
2
{'month': 'Jan', 'paid': 3000}
```

**How this code works.** Line 1 makes an empty list. Each `append` adds one dict to the end, even when it looks almost the same as one already there: a list keeps every item you add, in order. `len` counts the items; it does not add up the numbers inside them. `fees[0]` is the first item.

| After line | `fees` holds | Items |
|---|---|---|
| 1 | `[]` | 0 |
| 2 | `[{'month': 'Jan', 'paid': 3000}]` | 1 |
| 3 | `[{'month': 'Jan', 'paid': 3000}, {'month': 'Feb', 'paid': 3000}]` | 2 |

**One line from you:** two of the dicts in a list look almost the same. Does `len` count them once or twice, and why?

**Your answer.**

### Key
Kind: show
New: -
Like: twice: each `append` adds one item, even a near copy (runs/code-02-help_try1_trace.json).

## Help: Try with me 2

**Help for Try with me 2: one more worked example**

```python
reply = {"text": "Refund sent", "usage": {"input_tokens": 13, "output_tokens": 4}}
record = {"text": reply["text"], "tokens_out": reply["usage"]["output_tokens"]}
done = []
done.append(record)
print(done[0]["text"])
```
```output
Refund sent
```

**How this code works.** Line 2 builds the record `{'text': 'Refund sent', 'tokens_out': 4}`. Line 3 makes an empty list and line 4 appends the record, so `done` holds a list with one dict in it: `[{'text': 'Refund sent', 'tokens_out': 4}]`. Line 5 goes one step at a time: `done[0]` is that first dict, and `["text"]` looks up one key in it.

**One line from you:** why does line 5 need `[0]` before `["text"]`?

**Your answer.**

### Key
Kind: show
New: -
Like: `done` is a list; `[0]` takes the record out of it, and only a dict has the key `text` (runs/code-02-help_try2_trace.json, runs/code-02-help_try2.json).

## Help: Try with me 3

**Help for Try with me 3: one more worked example**

The same job in the right order, on a new function, with the whole program:

```python
def fake_model(prompt):
    return {"text": "Sent", "usage": {"input_tokens": 7, "output_tokens": 2}}

def remind(name, book):
    reply = fake_model(name)
    record = {"name": name, "tokens_out": reply["usage"]["output_tokens"]}
    book.append(record)
    return reply["text"]

book = []
print(remind("Ali", book))
print(book)
```
It prints:
```output
Sent
[{'name': 'Ali', 'tokens_out': 2}]
```

**How this code works.** Read it by what each line needs. `reply` must exist before the record can look inside it, so the call comes first. `record` must exist before it can be appended. `return` ends the function, so it comes last. The log gets the record, the small dict you built, and not the reply.

**One line from you:** why must the `reply = ...` line come before the `record = ...` line?

**Your answer.**

### Key
Kind: show
New: -
Like: the record line looks inside `reply`, so `reply` must exist first (runs/code-02-help_try3.json).

## Help: Your turn

**Help for Your turn: one more worked example**

```python
def fake_model(prompt):
    return {"text": "Checked", "usage": {"input_tokens": 5, "output_tokens": 1}}

def check(invoice, book):
    reply = fake_model(invoice)
    record = {"invoice": invoice, "tokens_out": reply["usage"]["output_tokens"]}
    book.append(record)
    return reply["text"]

book = []
one = check("INV-1", book)
print(book)
two = check("INV-2", book)
print(two)
print(len(book))
print(book[0]["invoice"])
```
```output
[{'invoice': 'INV-1', 'tokens_out': 1}]
Checked
2
INV-1
```

**How this code works.** After the first call, `book` holds one record. The second call adds one more, and `two` holds only the text, because the function returns `reply["text"]`. Two calls, two records. If the last line of `check` were `return reply`, the program would still run, but `print(two)` would show the whole reply dict instead of `Checked`: quietly wrong. A lookup of a key the dict does not have would stop it with a `KeyError`: a crash.

**One line from you:** suppose the record line inside `check` used `reply["output_tokens"]` instead. Crash, quietly wrong or fine, and why?

**Your answer.**

### Key
Kind: show
New: -
Like: crash, `KeyError`: `output_tokens` is not a key of `reply`, it sits inside `usage`, so the first call stops (runs/code-02-help_turn.json, help_turn_b.json). A right answer on a Your turn part after this block scores half.

## Retry

**Your turn again, on a new function (marked)**

```python
def fake_model(prompt):
    return {"text": "Sent", "usage": {"input_tokens": 12, "output_tokens": 5}}

def send(message, calls):
    reply = fake_model(message)
    record = {"message": message, "tokens_out": reply["usage"]["output_tokens"]}
    calls.append(record)
    return reply["text"]

calls = []
a = send("remind Ali", calls)
b = send("remind Sara", calls)
print(calls)
c = send("remind Omar", calls)
print(c)
print(len(calls))
print(calls[0]["message"])
```

**How this code works.** The same pattern: the list `calls` is made once, then `send` is called three times, and each call builds one record, appends it and hands back the text.

1. Write what each of the four prints shows.

Two changed copies; everything else is as above. Labels: crash (stops with an error), quietly wrong (runs, but misses the aim), fine (meets the aim).

```python
# B: the record line is now
record = {"message": message, "tokens_out": reply["usage"]["output"]}
```
```python
# C: the return line is now
return calls  # aim: hand back the text of the reply
```

2. For B: what it shows, its label, and the fixed line.
3. For C: what `print(c)` shows, its label, and the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-02-retry_a.json, retry_b.json, retry_c.json:
1. `[{'message': 'remind Ali', 'tokens_out': 5}, {'message': 'remind Sara', 'tokens_out': 5}]`; `Sent`; `3`; `remind Ali` (4 parts).
2. B: `KeyError: 'output'`; crash; fix `reply["usage"]["output_tokens"]` (3 parts).
3. C: `[{'message': 'remind Ali', 'tokens_out': 5}, {'message': 'remind Sara', 'tokens_out': 5}, {'message': 'remind Omar', 'tokens_out': 5}]`; quietly wrong; fix `return reply["text"]` (3 parts).
Score: 10 parts; right parts over 10. Record as Retry = right parts over 10.
Two options: for the part he is stuck on, is the value a list, a dict or the text? For B: is `output` a key inside `usage`? For C: does `c` hold the text, or the list of records?
Worked answer: two calls before `print(calls)`, so it shows two records; the third call returns `Sent`; three calls, three records; `calls[0]` is the first record, `remind Ali`. B looks inside `usage` for `output`, but the key there is `output_tokens`, so the first call stops with a `KeyError`: crash. C returns the log list, so it runs but `print(c)` shows all three records, not the text `Sent`: quietly wrong.

## Cold

**A week later: one more function (marked)**

```python
def fake_model(prompt):
    return {"text": "Approved", "usage": {"input_tokens": 20, "output_tokens": 1}}

def review(claim, history):
    reply = fake_model(claim)
    record = {"claim": claim, "tokens_in": reply["usage"]["input_tokens"]}
    history.append(record)
    return reply["text"]

history = []
r1 = review("fuel receipt", history)
print(history)
r2 = review("hotel bill", history)
print(r2)
print(len(history))
print(history[1]["claim"])
print(history[0]["tokens_in"])
```

**How this code works.** An expense-checking stand-in: `history` is made once, `review` is called twice, and each call writes one record and hands back the text.

1. Write what each of the five prints shows.

Two changed copies; everything else is as above. Labels: crash (stops with an error), quietly wrong (runs, but misses the aim), fine (meets the aim).

```python
# B: the record line is now
record = {"claim": claim, "tokens_in": reply["usage"]}  # aim: the input token count
```
```python
# C: the record line is now
record = {"claim": claim, "tokens_in": reply["input_tokens"]}
```

2. For B: what the last print shows, its label, and the fixed line.
3. For C: what it shows, its label, and the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-02-later_a.json, later_b.json, later_c.json:
1. `[{'claim': 'fuel receipt', 'tokens_in': 20}]`; `Approved`; `2`; `hotel bill`; `20` (5 parts).
2. B: last print shows `{'input_tokens': 20, 'output_tokens': 1}`; quietly wrong (E4); fix `reply["usage"]["input_tokens"]` (3 parts).
3. C: `KeyError: 'input_tokens'`; crash; fix as in B (3 parts).
Score: 11 parts; right parts over 11. Record as Cold = right parts over 11.
Two options: for the part he is stuck on, is the value a list, a dict or the text? For B and C: does it stop with an error, or run and miss its aim?
Worked answer: one call before `print(history)`, so it shows one record; `r2` holds the text `Approved`; two calls, two records; `history[1]` is the second record, `hotel bill`; `history[0]["tokens_in"]` is `20`. B stores the whole `usage` dict under `tokens_in`, so the last print shows that dict: quietly wrong. C skips `usage`: crash on the first call.

## Cards
- Q: `log = []`, then two `log.append(...)` lines, then `print(len(log))`. What prints? | A: `2`: each append adds one item. || Q: `log = []`, then three `log.append(...)` lines, the last one `log.append({"amount": 10})`, then `print(log[2])`. What prints? | A: `{'amount': 10}`: position `2` is the third item.
- Q: A function calls the AI once, builds a record and appends it. After 3 calls, how many records are in the log? | A: 3: one record per call. || Q: The same function is called twice with the same question. How many records? | A: 2: every call appends one record, even a repeat.
- Q: The last line of an `ask` function is `return reply["text"]`. What does a call hand back, and where did the record go? | A: Only the text; the record was appended to the log. || Q: The last line is changed to `return reply`, with the aim of handing back the text. Crash, quietly wrong, or fine? | A: Quietly wrong: it runs but hands back the whole reply dict.
