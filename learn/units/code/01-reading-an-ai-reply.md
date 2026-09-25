skill: code
id: code-01
level: 1
title: Reading an AI reply
pattern: 1. Call the function and keep what it returns. 2. Print the whole reply once to see its shape. 3. Go one key at a time to the value you want. 4. Check the kind of value you got.
sources: ../private/research-base/code/research/xie-2019-theory-of-instruction.md, ../private/research-base/code/research/subgoals-how-do-i-use-subgoals.md, ../private/research-base/production-and-llm-behaviour/production/anthropic-prompt-caching.md
runs: runs/code-01-flash1_a.json, runs/code-01-flash1_b.json, runs/code-01-flash2_a.json, runs/code-01-flash2_b.json, runs/code-01-help_try1.json, runs/code-01-help_try2.json, runs/code-01-help_try2_trace.json, runs/code-01-help_try3.json, runs/code-01-help_turn_a.json, runs/code-01-help_turn_b.json, runs/code-01-help_turn_c.json, runs/code-01-help_turn_fixed.json, runs/code-01-later_a.json, runs/code-01-later_b.json, runs/code-01-later_c.json, runs/code-01-later_d.json, runs/code-01-later_fixed.json, runs/code-01-retry_a.json, runs/code-01-retry_b.json, runs/code-01-retry_c.json, runs/code-01-retry_d.json, runs/code-01-retry_fixed.json, runs/code-01-show1.json, runs/code-01-show2.json, runs/code-01-show2_trace.json, runs/code-01-show3.json, runs/code-01-show3_crash.json, runs/code-01-try1.json, runs/code-01-try1_trace.json, runs/code-01-try2.json, runs/code-01-try2_trace.json, runs/code-01-try3.json, runs/code-01-try3_check.json, runs/code-01-turn_a.json, runs/code-01-turn_b.json, runs/code-01-turn_c.json, runs/code-01-turn_d.json, runs/code-01-turn_fixed.json
code: code/code-01/flash1_a.py, code/code-01/flash1_b.py, code/code-01/flash2_a.py, code/code-01/flash2_b.py, code/code-01/help_try1.py, code/code-01/help_try2.py, code/code-01/help_try2_trace.py, code/code-01/help_try3.py, code/code-01/help_turn_a.py, code/code-01/help_turn_b.py, code/code-01/help_turn_c.py, code/code-01/help_turn_fixed.py, code/code-01/later_a.py, code/code-01/later_b.py, code/code-01/later_c.py, code/code-01/later_d.py, code/code-01/later_fixed.py, code/code-01/retry_a.py, code/code-01/retry_b.py, code/code-01/retry_c.py, code/code-01/retry_d.py, code/code-01/retry_fixed.py, code/code-01/show1.py, code/code-01/show2.py, code/code-01/show2_trace.py, code/code-01/show3.py, code/code-01/show3_crash.py, code/code-01/try1.py, code/code-01/try1_trace.py, code/code-01/try2.py, code/code-01/try2_trace.py, code/code-01/try3.py, code/code-01/try3_check.py, code/code-01/turn_a.py, code/code-01/turn_b.py, code/code-01/turn_c.py, code/code-01/turn_d.py, code/code-01/turn_fixed.py
targets: E4 (a whole dict vs one value inside it), E1 (crash vs quietly wrong)
scored: Your turn

## Step: Goal

**Goal: read an AI reply**

Today you learn to read the reply that an AI model (the program that writes the answer, like Claude) sends back to your code.

The reply does not arrive as a plain sentence. It arrives as a **dict**: a set of labelled values inside curly brackets `{ }`, like one row of a bank statement where every amount sits under a column name. Each label is called a **key**; what sits under it is its **value**.

Why this matters: every AI app reads its answer, and how much text the call used, out of this reply. Pick the wrong piece and the app either stops with an error or shows the wrong thing with no warning at all.

Four steps, the same every time. They are the plan for this whole unit, and you will see them again under every exercise:

1. **Call** the function and keep what it returns (a function is a named piece of code you run; Show 2 explains it).
2. **Print** the whole reply once to see its shape.
3. **Go one key at a time** to the value you want.
4. **Check the kind** of value you got: a whole dict, or one value inside it.

Step 4 catches the most common slip: printing a whole dict when you wanted one number.

How the next messages go: I show a tiny example, then you try one with me, three times, each time adding one idea. Only the last exercise is marked.

Reply "ready", or ask about any word above.

**Your answer.**

### Key
Kind: show
New: the four pattern steps (subgoal labels)
No question to mark. If he asks about a word, answer from this message only (dict, key, value, function), then move to Show 1.

## Step: Show 1

**Show 1: one value out of a dict**

The smallest useful dict, and two ways to print from it:

```python
row = {"account": "HBL-001", "balance": 5200}
print(row["balance"])
print(row)
```
It prints:
```output
5200
{'account': 'HBL-001', 'balance': 5200}
```

**How this code works, line by line.**
- Line 1 builds a dict with two keys, `"account"` and `"balance"`, and gives it the name `row`. A name that holds a value is a **variable**: the `=` means "from now on, `row` holds this". After line 1, `row` holds the whole dict.
- Line 2: `row["balance"]` means "in `row`, look up the key `balance`". Square brackets straight after a dict's name are how you look up one key. The lookup hands back one value, `5200`, and `print` shows it on the screen.
- Line 3 prints `row` itself, with nothing after it, so the screen shows the whole dict, curly brackets and all. Python shows text in single quotes; that is only how it prints text.

Why it is built this way: a reply carries many values and you almost always want one, so you ask for it by its key.

A trace table (one row per line of code, showing what each variable holds after that line and what the screen shows) lets you follow code without running it:

| After line | `row` holds | Screen shows |
|---|---|---|
| 1 | the whole dict | nothing yet |
| 2 | the same dict | `5200` |
| 3 | the same dict | `{'account': 'HBL-001', 'balance': 5200}` |

**One line from you:** why does the last print show curly brackets, and the first one does not?

**Your answer.**

### Key
Kind: show
New: dict with keys and values, variable, looking up one key with square brackets
Unscored. Like: the first print shows the value under one key; the last shows the whole dict (runs/code-01-show1.json). If unsure, point at the table, row 2 against row 3.

## Step: Try with me 1

**Try with me 1**

Same shape, new numbers. Steps on hand: call and keep, print whole, one key at a time, check the kind.

```python
row = {"account": "MCB-7", "balance": 900}
b = row["balance"]
print(b)
```

**How this code works.** Line 1 builds a dict and names it `row`, as in Show 1. Line 2 looks up one key in `row` and gives the name `b` to whatever the lookup hands back. Line 3 prints `b`.

| After line | `row` holds | `b` holds |
|---|---|---|
| 1 | `{'account': 'MCB-7', 'balance': 900}` | nothing yet |
| 2 | the same dict | ? |

1. Fill the `?`.
2. What kind of value does `b` hold?
   A) the whole dict
   B) one number
   C) the word `"balance"`
   D) nothing: line 2 crashes

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-01-try1_trace.json: after line 2, `b` holds `900`; the program prints `900`.
1. `900`. 2. B.
Wrong options: A = E4 (the dict vs the value inside it); C = the key taken for the value; D = thinks a lookup of a key the dict has crashes.
Wrong twice: stuck order, then Help: Try with me 1.

## Step: Show 2

**Show 2: a function hands back a dict**

A **function** is a named piece of code you run by writing its name followed by round brackets. What you put inside the brackets is the **argument**: the input the function works on. A function hands a value back with the word `return`; that value is its **return value**. Picture a bank counter: you hand in a form (the argument), the clerk works on it and hands you back a receipt (the return value).

Here is a stand-in for an AI model (a few lines of Python that pretend to be the model, so it runs offline and costs nothing):

```python
def fake_model(prompt):
    return {"text": "Hello, Faiz", "input_tokens": 5, "output_tokens": 3}

reply = fake_model("Say hello")
print(reply["text"])
```
It prints:
```output
Hello, Faiz
```

**How this code works, in the order it runs.**
- `def fake_model(prompt):` only defines the function. Nothing runs yet. `prompt` is the name the argument will have inside the function: here, the question you send.
- The indented `return` line is the function's body. When the function runs, it hands back a dict: the reply's text and two counts of tokens, the small pieces of text a model reads (input) and writes (output). Providers charge per piece.
- `reply = fake_model("Say hello")` runs the function: `"Say hello"` goes in as `prompt`, the `return` line hands back the dict, and `reply` now holds that whole dict. This is step 1, call and keep.
- `reply["text"]` looks up one key (step 3) and gives `Hello, Faiz`, which `print` shows.

| Moment | `prompt` holds | `reply` holds |
|---|---|---|
| the call starts | `'Say hello'` | nothing yet |
| the call returns | gone: it only exists inside the function | `{'text': 'Hello, Faiz', 'input_tokens': 5, 'output_tokens': 3}` |

Why it is built this way: a real AI call is also a function you call with your question as the argument, and the reply comes back as its return value.

**One line from you:** after the call, does `reply` hold the text or the whole dict?

**Your answer.**

### Key
Kind: show
New: function defined with def and run with round brackets, argument, return value
Unscored. The whole dict; the text is one value inside it (runs/code-01-show2_trace.json).

## Step: Try with me 2

**Try with me 2**

```python
def fake_model(prompt):
    return {"text": "Your invoice is due Friday", "input_tokens": 9, "output_tokens": 6}

reply = fake_model("When is my invoice due?")
used = reply["output_tokens"]
print(used)
```

**How this code works.** The function has the same shape as in Show 2, with a different dict after `return`. The line `reply = ...` calls it with a question as the argument and keeps what it returns. The line `used = ...` looks up one key in `reply` and names the result `used`. The last line prints `used`.

| After line | `reply` holds | `used` holds |
|---|---|---|
| `def` and `return` | nothing yet: the function is only defined | nothing yet |
| `reply = ...` | ? | nothing yet |
| `used = ...` | the same as above | ? |

1. Fill both `?`. For `reply`, say which kind of value it is and what is in it.
2. What does the last line print?

Steps on hand: call and keep, print whole, one key at a time, check the kind.

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-01-try2_trace.json:
1. `reply`: the whole dict `{'text': 'Your invoice is due Friday', 'input_tokens': 9, 'output_tokens': 6}` (the kind, "the whole dict", is what matters; exact quotes do not). `used`: `6`.
2. `6`.
Slips: the text for `reply` (E4: one value vs the dict); `9` for `used` (the other count read).
Wrong twice: stuck order, then Help: Try with me 2.

## Step: Show 3

**Show 3: the real reply shape**

Real replies nest: some values are themselves dicts or lists. A **list** is values in a row inside square brackets; each item has a position counted from `0`, so `[0]` means "the first item". This is the shape of a real Claude reply (other companies use other key names):

```python
reply = {
    "content": [{"type": "text", "text": "Islamabad"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 14, "output_tokens": 4},
}
print(reply["usage"])
print(reply["usage"]["output_tokens"])
print(reply["content"][0]["text"])
```
```output
{'input_tokens': 14, 'output_tokens': 4}
4
Islamabad
```

**How this code works: one bracket at a time (step 3), checking the kind each time (step 4).**
- The first five lines build the reply. A dict may be spread over several lines, and the comma after its last item changes nothing. `content` holds a list with one dict in it, `stop_reason` says why the AI stopped writing (`end_turn` means it finished), `usage` holds a dict of counts.
- `reply["usage"]` gives the whole `usage` dict. Not a number yet.
- `reply["usage"]["output_tokens"]` works left to right: `["usage"]` gives that dict, then `["output_tokens"]` looks inside it and gives `4`.
- `reply["content"]` gives a list; `[0]` takes its first item, a dict; `["text"]` gives `Islamabad`.

Two slips, so you can name them later:
```python
reply = {"usage": {"input_tokens": 14, "output_tokens": 4}}
print(reply["output_tokens"])
```
```output
KeyError: 'output_tokens'
```
`output_tokens` is not a key of `reply`; it sits inside `reply["usage"]`. Asking a dict for a key it lacks stops the program: a **crash**. The quieter slip: if you wanted the output count and wrote `print(reply["usage"])`, the program runs and shows a whole dict, with no warning. That is **quietly wrong**.

**One line from you:** why does the first print show curly brackets, but the second shows `4`?

**Your answer.**

### Key
Kind: show
New: a value that is itself a dict (nesting), list and position [0], KeyError as a crash
Unscored. The first stops at the `usage` dict; the second goes one key further, to the number (runs/code-01-show3.json, runs/code-01-show3_crash.json).

## Step: Try with me 3

**Try with me 3**

```python
reply = {
    "content": [{"type": "text", "text": "Karachi"}],
    "stop_reason": "max_tokens",
    "usage": {"input_tokens": 20, "output_tokens": 50},
}
print(reply["stop_reason"])
```

**How this code works.** The reply has the same three keys as in Show 3. Here `stop_reason` is `max_tokens`, which means the reply was cut off because it hit the length limit. The last line looks up one key and prints `max_tokens`.

Which one line prints the **input** count (`input_tokens`), and what number does it print?

A) `print(reply["input_tokens"])`
B) `print(reply["usage"])`
C) `print(reply["usage"]["input_tokens"])`
D) `print(reply["content"][0]["input_tokens"])`

Steps on hand: call and keep, print whole, one key at a time, check the kind.

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-01-try3_check.json: C prints `20`.
Wrong options: A crashes, `KeyError: 'input_tokens'` (skipped `usage`); B prints the whole dict `{'input_tokens': 20, 'output_tokens': 50}`, quietly wrong (E4); D crashes, `KeyError: 'input_tokens'` (the count is not in the content piece).
Wrong twice: stuck order, then Help: Try with me 3.

## Step: Your turn

**Your turn (this one is marked)**

The three labels, each one you have now seen:
- **crash**: the program stops with an error, like `KeyError` when a dict lacks the key (Show 3).
- **quietly wrong**: it runs, but shows something other than what the aim says, like a whole dict when you wanted a number (Show 3).
- **fine**: it runs and shows what the aim says.

Each program is this reply line plus one `print` line. Anything after `#` is a comment, which Python ignores: `# A` names the program, and the comment on the print line is its aim.

```python
reply = {"content": [{"type": "text", "text": "Lahore"}], "stop_reason": "end_turn", "usage": {"input_tokens": 8, "output_tokens": 2}}
```
```python
# A
print(reply["text"])  # aim: the text of the reply
```
```python
# B
print("output tokens:", reply["usage"])  # aim: the output token count
```
```python
# C
print(reply["stop_reason"])  # aim: why the model stopped
```
```python
# D
print(reply["content"][0])  # aim: the text of the reply
```

**How this code works.** The first line builds a reply with the same shape as in Show 3, written on one line. Programs A to D each run one `print` on it and nothing else, so each is judged on its own. In B, `print` shows the words in quotes, then the value after the comma.

For each of A to D: 1. what it shows, 2. its label, 3. if it is a crash or quietly wrong, the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-01-turn_a.json to turn_d.json and turn_fixed.json:
- A: shows `KeyError: 'text'`; crash; fix `print(reply["content"][0]["text"])` (shows `Lahore`).
- B: shows `output tokens: {'input_tokens': 8, 'output_tokens': 2}`; quietly wrong (E4: the whole dict, not the count); fix `print("output tokens:", reply["usage"]["output_tokens"])` (shows `output tokens: 2`).
- C: shows `end_turn`; fine.
- D: shows `{'type': 'text', 'text': 'Lahore'}`; quietly wrong (E4: the piece, not its text); fix `print(reply["content"][0]["text"])`.
For "what it shows", the value is enough; exact quotes and spacing do not matter. For a crash, `KeyError` with the key is enough.
Score: 11 parts (A 3, B 3, C 2, D 3); right parts over 11.

## Step: Close

**Close**

You have now read four replies one key at a time.

Finish this sentence in your own words: "Next time I read a value out of an AI reply, I ..."

**Your answer.**

### Key
Kind: close
Like: "... print the whole reply once, go one key at a time, and check whether I have a whole dict or the value inside it." Record with engine.py close.

## Help: Try with me 1

**Help for Try with me 1: one more worked example**

A second example, fully worked, on a new dict:

```python
order = {"item": "chai", "qty": 3}
n = order["qty"]
print(n)
print(order)
```
```output
3
{'item': 'chai', 'qty': 3}
```

**How this code works.** Line 1 builds a dict with keys `item` and `qty` and names it `order`. Line 2 looks up the key `qty` in `order`; the lookup hands back the value under that key, and `n` now holds just that value. Line 3 prints `n`. Line 4 prints the whole dict, to compare.

| After line | `order` holds | `n` holds |
|---|---|---|
| 1 | `{'item': 'chai', 'qty': 3}` | nothing yet |
| 2 | the same dict | `3`, one number |

The name on the left of `=` gets what the right side hands back: here one value, not the dict and not the key's name.

Now back to Try with me 1: what does `b` hold, and which option is that?

**Your answer.**

### Key
Kind: show
New: -
`b` holds `900`; option B (runs/code-01-try1_trace.json). Worked example from runs/code-01-help_try1.json.

## Help: Try with me 2

**Help for Try with me 2: one more worked example**

A second example, fully worked:

```python
def fake_model(prompt):
    return {"text": "Pay by card", "input_tokens": 7, "output_tokens": 4}

answer = fake_model("How do I pay?")
n = answer["input_tokens"]
print(n)
```
```output
7
```

**How this code works.** `def` only defines `fake_model`. The line `answer = ...` runs it: the question goes in as `prompt`, the `return` line hands back the whole dict, and `answer` keeps it. The line `n = ...` looks up the key `input_tokens` in that dict, so `n` holds one number. The last line prints it.

| After line | `answer` holds | `n` holds |
|---|---|---|
| `answer = ...` | the whole dict `{'text': 'Pay by card', 'input_tokens': 7, 'output_tokens': 4}` | nothing yet |
| `n = ...` | the same dict | `7` |

Now back to Try with me 2: what do `reply` and `used` hold there, and what prints?

**Your answer.**

### Key
Kind: show
New: -
From runs/code-01-help_try2_trace.json. His answer for Try with me 2: `reply` the whole dict; `used` `6`; prints `6` (runs/code-01-try2_trace.json).

## Help: Try with me 3

**Help for Try with me 3: one more worked example**

A second example, fully worked, one bracket at a time:

```python
reply = {
    "content": [{"type": "text", "text": "Multan"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 11, "output_tokens": 3},
}
print(reply["usage"])
print(reply["usage"]["output_tokens"])
```
```output
{'input_tokens': 11, 'output_tokens': 3}
3
```

**How this code works.** Step 2, print whole: the first print stops at `["usage"]`, so it shows the whole `usage` dict. That shows where the counts live: inside `usage`, not at the top of `reply`. Step 3, one key at a time: the second print goes into `usage`, then asks for `output_tokens`, and gets one number. Step 4, check the kind: curly brackets on the screen mean you stopped one key too early.

Now back to Try with me 3: which option goes into `usage` first and then asks for the input count?

**Your answer.**

### Key
Kind: show
New: -
From runs/code-01-help_try3.json. His answer: C, prints `20` (runs/code-01-try3_check.json).

## Help: Your turn

**Help for Your turn: one more worked example**

Three programs on a new reply, each labelled and fixed, worked in full:

```python
reply = {"content": [{"type": "text", "text": "Peshawar"}], "stop_reason": "end_turn", "usage": {"input_tokens": 10, "output_tokens": 5}}
print(reply["input_tokens"])  # aim: the input token count
```
```output
KeyError: 'input_tokens'
```
```python
print(reply["content"])  # aim: the text of the reply
```
```output
[{'type': 'text', 'text': 'Peshawar'}]
```
```python
print(reply["usage"]["input_tokens"])  # aim: the input token count
```
```output
10
```

**How this code works.**
- First: `input_tokens` is not a key of `reply` (it sits inside `usage`), so it is a crash. Fix: `print(reply["usage"]["input_tokens"])`.
- Second: it runs, but shows a list holding a dict, not the text the aim asks for, so it is quietly wrong. Fix: `print(reply["content"][0]["text"])`, which shows `Peshawar`.
- Third: it shows the number the aim asks for, so it is fine.

To label a line: does it stop with an error (crash)? If not, does the screen match the aim (fine) or not (quietly wrong)?

Now back to your four programs: take the one you were stuck on and answer its three questions.

**Your answer.**

### Key
Kind: show
New: -
From runs/code-01-help_turn_a.json, help_turn_b.json, help_turn_c.json, help_turn_fixed.json. A right answer on a Your turn part after this block scores half.

## Retry

**Your turn again, on a new reply (marked)**

A new reply. Same labels: crash, quietly wrong, fine. Each program is the reply line plus one `print` line.

```python
reply = {"content": [{"type": "text", "text": "Rawalpindi"}], "stop_reason": "max_tokens", "usage": {"input_tokens": 16, "output_tokens": 30}}
```
```python
# A
print("input tokens:", reply["usage"])  # aim: the input token count
```
```python
# B
print(reply["content"][0]["text"])  # aim: the text of the reply
```
```python
# C
print(reply["output_tokens"])  # aim: the output token count
```
```python
# D
print(reply["content"])  # aim: the text of the reply
```

**How this code works.** The first line builds a reply shaped like the ones in this unit. Programs A to D each run one `print` on it, and each is judged on its own.

For each of A to D: 1. what it shows, 2. its label, 3. if it is a crash or quietly wrong, the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-01-retry_a.json to retry_d.json and retry_fixed.json:
- A: `input tokens: {'input_tokens': 16, 'output_tokens': 30}`; quietly wrong; fix `print("input tokens:", reply["usage"]["input_tokens"])` (shows `input tokens: 16`).
- B: `Rawalpindi`; fine.
- C: `KeyError: 'output_tokens'`; crash; fix `print(reply["usage"]["output_tokens"])` (shows `30`).
- D: `[{'type': 'text', 'text': 'Rawalpindi'}]`; quietly wrong; fix `print(reply["content"][0]["text"])`.
Score: 11 parts (A 3, B 2, C 3, D 3); right parts over 11.

## Cold

**A week later: one more reply (marked)**

Another company's reply, with other key names. Here the text sits under `choices`, then position `0`, then `message`, then `content`; and `prompt_tokens` and `completion_tokens` are this company's names for the input and output counts. Each program is the reply line plus one `print` line.

```python
reply = {"choices": [{"message": {"role": "assistant", "content": "Quetta"}}], "usage": {"prompt_tokens": 12, "completion_tokens": 3}}
```
```python
# A
print(reply["choices"][0]["message"])  # aim: the text of the reply
```
```python
# B
print(reply["usage"]["completion_tokens"])  # aim: the output token count
```
```python
# C
print(reply["message"]["content"])  # aim: the text of the reply
```
```python
# D
print(reply["usage"])  # aim: the input token count
```

**How this code works.** The first line builds the reply; the other key inside `message` only says who wrote it. Programs A to D each run one `print` on it, and each is judged on its own.

For each of A to D: 1. what it shows, 2. its label, 3. if it is a crash or quietly wrong, the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-01-later_a.json to later_d.json and later_fixed.json:
- A: `{'role': 'assistant', 'content': 'Quetta'}`; quietly wrong (stops one key early); fix `print(reply["choices"][0]["message"]["content"])` (shows `Quetta`).
- B: `3`; fine.
- C: `KeyError: 'message'`; crash (skipped `choices` and `[0]`); fix as for A.
- D: `{'prompt_tokens': 12, 'completion_tokens': 3}`; quietly wrong; fix `print(reply["usage"]["prompt_tokens"])` (shows `12`).
Score: 11 parts (A 3, B 2, C 3, D 3); right parts over 11.

## Cards
- Q: `reply = {"usage": {"input_tokens": 12, "output_tokens": 7}}` then `x = reply["usage"]`. What kind of value does `x` hold? | A: The whole usage dict, `{'input_tokens': 12, 'output_tokens': 7}`, not a number. || Q: `reply = {"usage": {"input_tokens": 25, "output_tokens": 9}}` then `x = reply["usage"]["output_tokens"]`. What kind of value does `x` hold? | A: One number, `9`: the second key went inside the usage dict.
- Q: `reply = {"usage": {"input_tokens": 12, "output_tokens": 7}}` then `print(reply["output_tokens"])`. Crash, quietly wrong, or fine? | A: Crash, `KeyError: 'output_tokens'`: the count sits inside `usage`, not at the top. || Q: `reply = {"content": [{"type": "text", "text": "Sukkur"}]}` then `print(reply["text"])`. Crash, quietly wrong, or fine? | A: Crash, `KeyError: 'text'`: the text sits inside the list under `content`, at position `0`.
- Q: In `reply["content"][0]["text"]`, what does `[0]` do? | A: Takes the first item of the list under `content`. || Q: In `reply["choices"][0]["message"]`, what does `[0]` do? | A: Takes the first item of the list under `choices`.
