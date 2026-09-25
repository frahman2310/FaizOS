skill: code
id: code-01
level: 1
title: Reading an AI reply
pattern: 1. Call the function and keep what it returns. 2. Print the whole reply once to see its shape. 3. Go one key at a time to the value you want. 4. Check the kind of value you got.
sources: ../private/research-base/code/research/xie-2019-theory-of-instruction.md, ../private/research-base/code/research/subgoals-how-do-i-use-subgoals.md, ../private/research-base/production-and-llm-behaviour/production/anthropic-prompt-caching.md
runs: runs/code-01-flash1_a.json, runs/code-01-flash1_b.json, runs/code-01-flash2_a.json, runs/code-01-flash2_b.json, runs/code-01-help_try1.json, runs/code-01-help_try2.json, runs/code-01-help_try2_trace.json, runs/code-01-help_try3.json, runs/code-01-help_try4.json, runs/code-01-help_try5_a.json, runs/code-01-help_try5_b.json, runs/code-01-help_try5_fixed.json, runs/code-01-help_turn_a.json, runs/code-01-help_turn_b.json, runs/code-01-help_turn_c.json, runs/code-01-help_turn_fixed.json, runs/code-01-later_a.json, runs/code-01-later_b.json, runs/code-01-later_c.json, runs/code-01-later_d.json, runs/code-01-later_fixed.json, runs/code-01-retry_a.json, runs/code-01-retry_b.json, runs/code-01-retry_c.json, runs/code-01-retry_d.json, runs/code-01-retry_fixed.json, runs/code-01-show1.json, runs/code-01-show2.json, runs/code-01-show2_trace.json, runs/code-01-show3.json, runs/code-01-show4.json, runs/code-01-show5_a.json, runs/code-01-show5_b.json, runs/code-01-show5_c.json, runs/code-01-show5_fixed.json, runs/code-01-try1.json, runs/code-01-try1_trace.json, runs/code-01-try2.json, runs/code-01-try2_trace.json, runs/code-01-try3.json, runs/code-01-try3_check.json, runs/code-01-try4.json, runs/code-01-try4_check.json, runs/code-01-try5_p.json, runs/code-01-try5_q.json, runs/code-01-try5_r.json, runs/code-01-turn_a.json, runs/code-01-turn_b.json, runs/code-01-turn_c.json, runs/code-01-turn_d.json, runs/code-01-turn_fixed.json
code: code/code-01/flash1_a.py, code/code-01/flash1_b.py, code/code-01/flash2_a.py, code/code-01/flash2_b.py, code/code-01/help_try1.py, code/code-01/help_try2.py, code/code-01/help_try2_trace.py, code/code-01/help_try3.py, code/code-01/help_try4.py, code/code-01/help_try5_a.py, code/code-01/help_try5_b.py, code/code-01/help_try5_fixed.py, code/code-01/help_turn_a.py, code/code-01/help_turn_b.py, code/code-01/help_turn_c.py, code/code-01/help_turn_fixed.py, code/code-01/later_a.py, code/code-01/later_b.py, code/code-01/later_c.py, code/code-01/later_d.py, code/code-01/later_fixed.py, code/code-01/retry_a.py, code/code-01/retry_b.py, code/code-01/retry_c.py, code/code-01/retry_d.py, code/code-01/retry_fixed.py, code/code-01/show1.py, code/code-01/show2.py, code/code-01/show2_trace.py, code/code-01/show3.py, code/code-01/show4.py, code/code-01/show5_a.py, code/code-01/show5_b.py, code/code-01/show5_c.py, code/code-01/show5_fixed.py, code/code-01/try1.py, code/code-01/try1_trace.py, code/code-01/try2.py, code/code-01/try2_trace.py, code/code-01/try3.py, code/code-01/try3_check.py, code/code-01/try4.py, code/code-01/try4_check.py, code/code-01/try5_p.py, code/code-01/try5_q.py, code/code-01/try5_r.py, code/code-01/turn_a.py, code/code-01/turn_b.py, code/code-01/turn_c.py, code/code-01/turn_d.py, code/code-01/turn_fixed.py
targets: E4 (a whole dict vs one value inside it), E1 (crash vs quietly wrong)
scored: Your turn

## Step: Goal

**Goal: read an AI reply**

Today you learn to read the reply that an AI model (the program that writes the answer, like Claude) sends back to your code.

The reply does not arrive as a plain sentence. It arrives as a **dict**: a set of labelled values inside curly brackets `{ }`, like one row of a bank statement where every amount sits under a column name. Each label is called a **key**; what sits under it is its **value**.

Why this matters: every AI app reads its answer, and how much text it used, out of this reply. Pick the wrong piece and the app either stops with an error or shows the wrong thing with no warning at all.

Four steps, the same every time. They are the plan for this whole unit, and you will see them again under the exercises:

1. **Call** the function and keep what it returns (a function is a named piece of code you run; Show 2 explains it).
2. **Print** the whole reply once to see its shape.
3. **Go one key at a time** to the value you want.
4. **Check the kind** of value you got: a whole dict, or one value inside it.

Step 4 catches the most common slip: printing a whole dict when you wanted one number.

How the next messages go: I show a small example, then you try one with me. That happens five times, each time adding one idea. Only the last exercise is marked.

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
New: dict (keys with their values); variable; looking up one key with square brackets
Unscored. Like: the first print shows the value under one key; the last shows the whole dict (runs/code-01-show1.json). If unsure, point at the table, row 2 against row 3.

## Step: Try with me 1

**Try with me 1**

Same shape, new numbers.

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
Two options: after line 2, does `b` hold the whole dict `{'account': 'MCB-7', 'balance': 900}`, or the one value under `balance`?
Worked answer: line 2 has `row["balance"]` on the right of `=`. Square brackets after a dict's name look up one key (Show 1, line 2), so the right side hands back only the value under `balance`, which is `900`. The `=` gives that value the name `b`. So `b` holds `900`, one number: option B. The dict stays in `row`, unchanged.
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
- `def fake_model(prompt):` only defines the function; nothing runs yet. `prompt` is the name the argument will have inside the function.
- The next line starts with four spaces (it is indented). The indent marks it as part of the function: it runs each time the function is called. Here `return` hands back a dict: the reply's text and two counts (Show 3 says what they count).
- `reply = fake_model("Say hello")` runs the function: `"Say hello"` goes in as `prompt`, the `return` line hands back the dict, and `reply` now holds that whole dict. This is step 1, call and keep.
- `reply["text"]` looks up one key (step 3) and gives `Hello, Faiz`, which `print` shows.

| After line | `reply` holds | Screen shows |
|---|---|---|
| `def` and `return` | nothing yet: the function is only defined | nothing yet |
| `reply = ...` | `{'text': 'Hello, Faiz', 'input_tokens': 5, 'output_tokens': 3}` | nothing yet |
| `print(...)` | the same dict | `Hello, Faiz` |

Why it is built this way: a real AI call is also a function you call with your question as the argument, and the reply comes back as its return value.

**One line from you:** why does `reply` hold a whole dict, and not just the text?

**Your answer.**

### Key
Kind: show
New: function defined with def plus an indented body then run with round brackets; argument; return value
Unscored. Like: because `return` hands back the whole dict and `=` keeps whatever comes back; the text is one value inside it (runs/code-01-show2_trace.json).

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
Two options: after `reply = ...`, does `reply` hold the text `Your invoice is due Friday`, or the whole dict that `return` hands back?
Worked answer: the `reply = ...` line runs `fake_model`; its `return` line hands back the whole dict, and `=` keeps all of it, as in Show 2. So `reply` holds `{'text': 'Your invoice is due Friday', 'input_tokens': 9, 'output_tokens': 6}`. Next, `reply["output_tokens"]` looks up one key in that dict and hands back `6`, so `used` holds `6`. The last line prints `used`: `6`. (`9` sits under the other key, `input_tokens`.)
Wrong twice: stuck order, then Help: Try with me 2.

## Step: Show 3

**Show 3: a dict inside a dict**

A value can itself be a dict. This is called **nesting**. The stand-in in Show 2 kept its two counts at the top; real replies keep them in a dict nested under the key `usage`. The counts are **tokens**: the small pieces of text a model reads (input) and writes (output). Providers charge per token, so these are the numbers an AI bill is built from.

```python
reply = {"text": "Islamabad", "usage": {"input_tokens": 14, "output_tokens": 4}}
print(reply["usage"])
print(reply["usage"]["output_tokens"])
```
It prints:
```output
{'input_tokens': 14, 'output_tokens': 4}
4
```

**How this code works, one bracket at a time.**
- Line 1 builds `reply` with two keys. The value under `text` is the text. The value under `usage` is itself a dict, with its own two keys.
- Line 2: `reply["usage"]` hands back the whole inner dict, so the screen shows curly brackets. Not a number yet.
- Line 3 works left to right (step 3, one key at a time): `["usage"]` hands back the inner dict, then `["output_tokens"]` looks inside that dict and hands back `4`.

| What you write | Kind of value | Screen shows |
|---|---|---|
| `reply["usage"]` | the inner dict | `{'input_tokens': 14, 'output_tokens': 4}` |
| `reply["usage"]["output_tokens"]` | one number | `4` |

Step 4, check the kind: curly brackets on the screen when you wanted a number mean you stopped one key too early.

**One line from you:** why does line 3 need two pairs of square brackets to reach `4`?

**Your answer.**

### Key
Kind: show
New: a value that is itself a dict (nesting); chained lookups one bracket at a time; tokens (what usage counts)
Unscored. Like: `4` sits inside the `usage` dict, so the first brackets open `usage` and the second pick the count inside it (runs/code-01-show3.json).

## Step: Try with me 3

**Try with me 3**

```python
reply = {"text": "Karachi", "usage": {"input_tokens": 20, "output_tokens": 50}}
print(reply["text"])
```

**How this code works.** Line 1 builds a reply shaped like the one in Show 3: the text under `text`, and the two counts in a dict nested under `usage`. Line 2 looks up one key at the top of `reply` and prints the text.

Which one line prints the **input** count (`input_tokens`), and what number does it print?

A) `print(reply["input_tokens"])`
B) `print(reply["usage"])`
C) `print(reply["usage"]["input_tokens"])`
D) `print(reply["usage"]["output_tokens"])`

Steps on hand: call and keep, print whole, one key at a time, check the kind.

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-01-try3_check.json: C prints `20`.
Wrong options: A stops with `KeyError: 'input_tokens'` (skipped `usage`; Show 5 names this a crash); B prints the whole dict `{'input_tokens': 20, 'output_tokens': 50}` (E4: stopped one key early); D prints `50`, the other count.
Two options: B `print(reply["usage"])` or C `print(reply["usage"]["input_tokens"])`: which one goes all the way to a number?
Worked answer: in line 1 the input count is not a key of `reply`; it sits inside the dict under `usage`. So first `["usage"]`, which hands back `{'input_tokens': 20, 'output_tokens': 50}`; then `["input_tokens"]` inside it, which hands back `20`. That is C, and it prints `20`. B stops at the inner dict; A skips `usage`; D picks the other key and prints `50`.
Wrong twice: stuck order, then Help: Try with me 3.

## Step: Show 4

**Show 4: a list inside the reply**

A **list** is values in a row inside square brackets `[ ]`. Each item has a position counted from `0`, so `[0]` means "the first item". In a real Claude reply the text sits inside a list under the key `content`. This is the real shape (other companies use other key names). A dict can be written over several lines, one key per line; the comma after the last item changes nothing.

```python
reply = {
    "content": [{"type": "text", "text": "Gilgit"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 12, "output_tokens": 2},
}
print(reply["content"])
print(reply["content"][0])
print(reply["content"][0]["text"])
```
It prints:
```output
[{'type': 'text', 'text': 'Gilgit'}]
{'type': 'text', 'text': 'Gilgit'}
Gilgit
```

**How this code works, one bracket at a time.**
- The first five lines build one reply with three keys. `content` holds a list with one item in it, a small dict. `stop_reason` says why the model stopped writing: `end_turn` means it finished. `usage` holds the counts, as in Show 3.
- `reply["content"]` hands back the whole list: square brackets outside.
- `reply["content"][0]` takes the first item of that list: the small dict, curly brackets.
- `reply["content"][0]["text"]` looks up `text` in that small dict and hands back `Gilgit`.

| What you write | Kind of value | Screen shows |
|---|---|---|
| `reply["content"]` | a list | `[{'type': 'text', 'text': 'Gilgit'}]` |
| `reply["content"][0]` | a dict, the first item | `{'type': 'text', 'text': 'Gilgit'}` |
| `reply["content"][0]["text"]` | the text | `Gilgit` |

**One line from you:** why does the text need `[0]` before `["text"]`?

**Your answer.**

### Key
Kind: show
New: list with positions counted from 0; the real reply shape (text inside content at [0]); a dict written over several lines
Unscored. Like: `content` holds a list, and a list is opened by position, so `[0]` takes the dict that holds `text` (runs/code-01-show4.json).

## Step: Try with me 4

**Try with me 4**

```python
reply = {
    "content": [{"type": "text", "text": "Karachi"}],
    "stop_reason": "max_tokens",
    "usage": {"input_tokens": 20, "output_tokens": 50},
}
print(reply["stop_reason"])
```

**How this code works.** The reply has the same three keys as in Show 4. Here `stop_reason` is `max_tokens`, which means the reply was cut off because it hit the length limit. The last line looks up one key at the top of `reply` and prints `max_tokens`.

1. Which one line prints the **text** of the reply?
   A) `print(reply["text"])`
   B) `print(reply["content"][0])`
   C) `print(reply["content"][0]["text"])`
   D) `print(reply["content"])`
2. What does B print, and what kind of value is it?

Steps on hand: call and keep, print whole, one key at a time, check the kind.

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-01-try4_check.json:
1. C, prints `Karachi`.
2. B prints `{'type': 'text', 'text': 'Karachi'}`: a dict, the first item of the list, not the text (E4). The value is enough; exact quotes do not matter.
Wrong options: A stops with `KeyError: 'text'` (`text` is not a key of `reply`; it sits inside the list under `content`); D prints the whole list `[{'type': 'text', 'text': 'Karachi'}]`.
Two options: B `print(reply["content"][0])` or C `print(reply["content"][0]["text"])`: which one ends with a text, and which with a dict?
Worked answer: go one key at a time, as in Show 4. `reply["content"]` hands back the list `[{'type': 'text', 'text': 'Karachi'}]`. `[0]` takes its first item, the dict `{'type': 'text', 'text': 'Karachi'}`: that is where B stops, so B prints a dict. `["text"]` looks up `text` in that dict and hands back `Karachi`: that is C. A asks the top of `reply` for `text`, which it does not have; D stops at the list.
Wrong twice: stuck order, then Help: Try with me 4.

## Step: Show 5

**Show 5: crash, quietly wrong, fine**

When code reads the wrong piece, one of two things happens, and from now on you will name which. Here is one of each on the same reply. Anything after `#` is a **comment**: Python ignores it. Here each comment holds the line's **aim**, what the line is meant to show.

```python
reply = {"content": [{"type": "text", "text": "Hyderabad"}], "stop_reason": "end_turn", "usage": {"input_tokens": 12, "output_tokens": 6}}
```
```python
print(reply["output_tokens"])  # aim: the output token count
```
```output
KeyError: 'output_tokens'
```
```python
print(reply["content"])  # aim: the text of the reply
```
```output
[{'type': 'text', 'text': 'Hyderabad'}]
```
```python
print(reply["usage"]["output_tokens"])  # aim: the output token count
```
```output
6
```

**How this code works.** The first line builds a reply with the Show 4 shape, written on one line. Each `print` line runs on it by itself.
- First print: `output_tokens` is not a key of `reply`; it sits inside `usage`. Asking a dict for a key it lacks stops the program with a `KeyError`: a **crash**. Fixed line: `print(reply["usage"]["output_tokens"])`.
- Second: it runs with no error, but shows a whole list, not the text the aim asks for, and gives no warning. That is **quietly wrong**, the more dangerous slip. Fixed line: `print(reply["content"][0]["text"])`, which shows `Hyderabad`.
- Third: it runs and shows the number the aim asks for: **fine**.

To label any line, ask two questions in order. Does it stop with an error? Then it is a crash. If not, does the screen match the aim? Yes: fine. No: quietly wrong.

**One line from you:** both of the first two lines are wrong. Why is the second one more dangerous?

**Your answer.**

### Key
Kind: show
New: `#` comment holding the aim; crash (KeyError stops the program); quietly wrong versus fine
Unscored. Like: a crash tells you at once; a quietly wrong line runs and shows something, so nobody notices (runs/code-01-show5_a.json, show5_b.json, show5_c.json, show5_fixed.json).

## Step: Try with me 5

**Try with me 5**

A new reply and three lines. Label only this time.

```python
reply = {"content": [{"type": "text", "text": "Sialkot"}], "stop_reason": "end_turn", "usage": {"input_tokens": 9, "output_tokens": 4}}
```
```python
# P
print(reply["text"])  # aim: the text of the reply
```
```python
# Q
print(reply["usage"]["input_tokens"])  # aim: the input token count
```
```python
# R
print(reply["usage"])  # aim: the input token count
```

**How this code works.** The first line builds a reply with the same shape as in Show 5. P, Q and R each run one `print` on it, and each is judged by itself against the aim in its comment.

For each of P, Q and R: crash, quietly wrong, or fine? Use the two questions from Show 5.

Steps on hand: call and keep, print whole, one key at a time, check the kind.

**Your answer.**

### Key
Kind: try
Unscored; aim: right first time. From runs/code-01-try5_p.json, try5_q.json, try5_r.json:
P crash (`KeyError: 'text'`); Q fine (shows `9`); R quietly wrong (shows `{'input_tokens': 9, 'output_tokens': 4}`, E4).
Two options: for R, it runs and shows `{'input_tokens': 9, 'output_tokens': 4}`, and its aim is the input count. Is that fine, or quietly wrong?
Worked answer: P asks the top of `reply` for `text`; the text sits inside `content`, so P stops with `KeyError: 'text'`: crash. Q goes into `usage`, then `input_tokens`, and shows `9`, the count the aim asks for: fine. R runs with no error, so it is not a crash; but it stops at the `usage` dict and shows two counts in curly brackets, not the one number the aim asks for: quietly wrong.
Wrong twice: stuck order, then Help: Try with me 5.

## Step: Your turn

**Your turn (this one is marked)**

The three labels from Show 5:
- **crash**: the program stops with an error, like `KeyError` when a dict lacks the key.
- **quietly wrong**: it runs, but shows something other than what the aim says.
- **fine**: it runs and shows what the aim says.

Each program is this reply line plus one `print` line. `# A` names the program; the comment on the print line is its aim.

```python
reply = {"content": [{"type": "text", "text": "Lahore"}], "stop_reason": "end_turn", "usage": {"input_tokens": 8, "output_tokens": 2}}
```
```python
# A
print(reply["text"])  # aim: the text of the reply
```
```python
# B
print(reply["usage"])  # aim: the output token count
```
```python
# C
print(reply["stop_reason"])  # aim: why the model stopped
```
```python
# D
print(reply["content"][0])  # aim: the text of the reply
```

**How this code works.** The first line builds a reply with the same shape as in Shows 4 and 5, written on one line. Programs A to D each run one `print` on it and nothing else, so each is judged on its own.

For each of A to D: 1. what it shows, 2. its label, 3. if it is a crash or quietly wrong, the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-01-turn_a.json to turn_d.json and turn_fixed.json:
- A: shows `KeyError: 'text'`; crash; fix `print(reply["content"][0]["text"])` (shows `Lahore`).
- B: shows `{'input_tokens': 8, 'output_tokens': 2}`; quietly wrong (E4: the whole dict, not the count); fix `print(reply["usage"]["output_tokens"])` (shows `2`).
- C: shows `end_turn`; fine.
- D: shows `{'type': 'text', 'text': 'Lahore'}`; quietly wrong (E4: the piece, not its text); fix `print(reply["content"][0]["text"])`.
For "what it shows", the value is enough; exact quotes and spacing do not matter. For a crash, `KeyError` with the key is enough.
Two options: for the program he is stuck on, does it stop with an error, or does it run? If it runs, does the screen show what its aim says, or something else?
Worked answer: A asks the top of `reply` for `text`; the text sits inside `content` at position `0`, so it stops with `KeyError: 'text'`: crash; fixed `print(reply["content"][0]["text"])`, which shows `Lahore`. B runs and shows the whole `usage` dict `{'input_tokens': 8, 'output_tokens': 2}`, but the aim is one count: quietly wrong; go one key further, `print(reply["usage"]["output_tokens"])`, which shows `2`. C runs and shows `end_turn`, which is why the model stopped: fine. D runs and shows the dict `{'type': 'text', 'text': 'Lahore'}`, the first item of the list, not its text: quietly wrong; add `["text"]`, giving `print(reply["content"][0]["text"])`.
Score: 11 parts (A 3, B 3, C 2, D 3); right parts over 11.

## Step: Close

**Close**

You have now read several replies one key at a time, and named what goes wrong when a line stops too early or skips a key.

Finish this sentence in your own words: "Next time I read a value out of an AI reply, I ..."

**Your answer.**

### Key
Kind: close
Like: "... print the whole reply once, go one key at a time, and check whether I have a whole dict or the value inside it." Record with engine.py close.

## Help: Try with me 1

**One more worked example: one value out of a dict**

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

**One line from you:** why does `n` hold `3`, and not the whole dict?

**Your answer.**

### Key
Kind: show
New: -
Like: `order["qty"]` looks up one key, so it hands back only the value under it (runs/code-01-help_try1.json).

## Help: Try with me 2

**One more worked example: keeping what a function returns**

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

**One line from you:** which line turns the whole dict into one number, and how?

**Your answer.**

### Key
Kind: show
New: -
Like: `n = answer["input_tokens"]`: it looks up one key in the dict `answer` holds (runs/code-01-help_try2_trace.json).

## Help: Try with me 3

**One more worked example: a dict inside a dict**

A second example, fully worked, one bracket at a time:

```python
reply = {"text": "Multan", "usage": {"input_tokens": 11, "output_tokens": 3}}
print(reply["usage"])
print(reply["usage"]["output_tokens"])
```
```output
{'input_tokens': 11, 'output_tokens': 3}
3
```

**How this code works.** Step 2, print whole: the first print stops at `["usage"]`, so it shows the whole `usage` dict. That shows where the counts live: inside `usage`, not at the top of `reply`. Step 3, one key at a time: the second print goes into `usage`, then asks for `output_tokens`, and gets one number. Step 4, check the kind: curly brackets on the screen mean you stopped one key too early.

**One line from you:** to print the input count `11` here, which two keys do you ask for, in which order?

**Your answer.**

### Key
Kind: show
New: -
Like: `usage` first, then `input_tokens`: `reply["usage"]["input_tokens"]` (runs/code-01-help_try3.json).

## Help: Try with me 4

**One more worked example: the text inside the list**

A second example, fully worked:

```python
reply = {
    "content": [{"type": "text", "text": "Mardan"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 7, "output_tokens": 2},
}
print(reply["content"][0])
print(reply["content"][0]["text"])
```
```output
{'type': 'text', 'text': 'Mardan'}
Mardan
```

**How this code works.** `reply["content"]` is a list with one item. `[0]` takes that first item, a small dict, so the first print shows curly brackets: the dict, not the text. The second print adds one more key, `["text"]`, and gets the text itself. Read it left to right, and after each bracket say what kind of value you hold: list, then dict, then text.

**One line from you:** what does the first print show, and why is it not the text?

**Your answer.**

### Key
Kind: show
New: -
Like: the dict `{'type': 'text', 'text': 'Mardan'}`; it stops at the first item of the list, one key before the text (runs/code-01-help_try4.json).

## Help: Try with me 5

**One more worked example: labelling a line**

Two lines on a new reply, each labelled with the two questions:

```python
reply = {"content": [{"type": "text", "text": "Bahawalpur"}], "stop_reason": "end_turn", "usage": {"input_tokens": 15, "output_tokens": 8}}
print(reply["usage"])  # aim: the output token count
```
```output
{'input_tokens': 15, 'output_tokens': 8}
```
```python
print(reply["stop_reason"])  # aim: why the model stopped
```
```output
end_turn
```

**How this code works.**
- First line: does it stop with an error? No, it shows a dict, so it is not a crash. Does the screen match the aim? The aim is one count; the screen shows two counts in curly brackets. No match: quietly wrong. Fixed line: `print(reply["usage"]["output_tokens"])`, which shows `8`.
- Second line: no error. The screen shows `end_turn`, which is why the model stopped, as the aim says: fine.

**One line from you:** a line runs with no error. What do you check next, before calling it fine?

**Your answer.**

### Key
Kind: show
New: -
Like: whether the screen shows what the aim says (runs/code-01-help_try5_a.json, help_try5_b.json, help_try5_fixed.json).

## Help: Your turn

**One more worked example: three lines labelled and fixed**

Three programs on a new reply, each labelled and fixed, worked in full:

```python
reply = {"content": [{"type": "text", "text": "Peshawar"}], "stop_reason": "end_turn", "usage": {"input_tokens": 10, "output_tokens": 5}}
print(reply["input_tokens"])  # aim: the input token count
```
```output
KeyError: 'input_tokens'
```
```python
print(reply["usage"]["output_tokens"])  # aim: the input token count
```
```output
5
```
```python
print(reply["stop_reason"])  # aim: why the model stopped
```
```output
end_turn
```

**How this code works.**
- First: `input_tokens` is not a key of `reply` (it sits inside `usage`), so it stops with an error: crash. Fix: `print(reply["usage"]["input_tokens"])`, which shows `10`.
- Second: it runs and shows a number, but the output count, not the input count the aim asks for: quietly wrong. Fix: the same line as the first fix.
- Third: it shows why the model stopped, as the aim says: fine.

To label a line: does it stop with an error (crash)? If not, does the screen match the aim (fine) or not (quietly wrong)?

**One line from you:** the second line shows a number, and the aim wants a number. Why is it still quietly wrong?

**Your answer.**

### Key
Kind: show
New: -
Like: it is the wrong number: the output count, not the input count the aim names (runs/code-01-help_turn_a.json, help_turn_b.json, help_turn_c.json, help_turn_fixed.json). A right answer on a Your turn part after this block scores half.

## Retry

**Your turn again, on a new reply (marked)**

A new reply. Same labels: crash (stops with an error), quietly wrong (runs, but misses the aim), fine (meets the aim). Each program is the reply line plus one `print` line; the comment is its aim.

```python
reply = {"content": [{"type": "text", "text": "Rawalpindi"}], "stop_reason": "max_tokens", "usage": {"input_tokens": 16, "output_tokens": 30}}
```
```python
# A
print(reply["usage"])  # aim: the input token count
```
```python
# B
print(reply["content"][0]["text"])  # aim: the text of the reply
```
```python
# C
print(reply["usage"]["tokens"])  # aim: the output token count
```
```python
# D
print(reply["content"][0]["type"])  # aim: the text of the reply
```

**How this code works.** The first line builds a reply shaped like the ones in this unit: the text inside a list under `content`, the counts nested under `usage`. Programs A to D each run one `print` on it, and each is judged on its own.

For each of A to D: 1. what it shows, 2. its label, 3. if it is a crash or quietly wrong, the fixed line.

**Your answer.**

### Key
Kind: scored
From runs/code-01-retry_a.json to retry_d.json and retry_fixed.json:
- A: `{'input_tokens': 16, 'output_tokens': 30}`; quietly wrong (E4); fix `print(reply["usage"]["input_tokens"])` (shows `16`).
- B: `Rawalpindi`; fine.
- C: `KeyError: 'tokens'`; crash (`usage` has no key `tokens`); fix `print(reply["usage"]["output_tokens"])` (shows `30`).
- D: `text`; quietly wrong (the value under `type`, which happens to be the word text, not the reply's text); fix `print(reply["content"][0]["text"])` (shows `Rawalpindi`).
Score: 11 parts (A 3, B 2, C 3, D 3); right parts over 11. Record as Retry = right parts over 11.
Two options: does it stop with an error, or run? If it runs, does the screen show what the aim says?
Worked answer: A stops at the `usage` dict, two counts, when the aim is one: quietly wrong, go one key further to `input_tokens`. B goes list, first item, `text`: fine. C asks `usage` for a key it lacks, `tokens`: crash; the output count is under `output_tokens`. D goes to the first item of the list, then asks for `type`, whose value is the word `text`: it runs but is not the reply's text, quietly wrong; ask for `["text"]` instead.

## Cold

**A week later: one more reply (marked)**

Another company's reply, with other key names. Here the text sits under `choices`, then position `0`, then `message`, then `content`; and `prompt_tokens` and `completion_tokens` are this company's names for the input and output counts. Labels: crash (stops with an error), quietly wrong (runs, but misses the aim), fine (meets the aim). Each program is the reply line plus one `print` line; the comment is its aim.

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
Score: 11 parts (A 3, B 2, C 3, D 3); right parts over 11. Record as Cold = right parts over 11.
Two options: does it stop with an error, or run? If it runs, does the screen show what the aim says?
Worked answer: follow the path the message gives: `choices`, `[0]`, `message`, `content`. A stops at `message`, a dict: quietly wrong, add `["content"]`. B goes into `usage` to the output count: fine. C starts at `message`, which is not a key at the top: crash. D stops at the `usage` dict when the aim is one count: quietly wrong, go on to `prompt_tokens`.

## Cards
- Q: `reply = {"usage": {"input_tokens": 12, "output_tokens": 7}}` then `x = reply["usage"]`. What kind of value does `x` hold? | A: The whole usage dict, `{'input_tokens': 12, 'output_tokens': 7}`, not a number. || Q: `reply = {"usage": {"input_tokens": 25, "output_tokens": 9}}` then `x = reply["usage"]["output_tokens"]`. What kind of value does `x` hold? | A: One number, `9`: the second key went inside the usage dict.
- Q: `reply = {"usage": {"input_tokens": 12, "output_tokens": 7}}` then `print(reply["output_tokens"])`. Crash, quietly wrong, or fine? | A: Crash, `KeyError: 'output_tokens'`: the count sits inside `usage`, not at the top. || Q: `reply = {"content": [{"type": "text", "text": "Sukkur"}]}` then `print(reply["text"])`. Crash, quietly wrong, or fine? | A: Crash, `KeyError: 'text'`: the text sits inside the list under `content`, at position `0`.
- Q: In `reply["content"][0]["text"]`, what does `[0]` do? | A: Takes the first item of the list under `content`. || Q: In `reply["choices"][0]["message"]`, what does `[0]` do? | A: Takes the first item of the list under `choices`.
