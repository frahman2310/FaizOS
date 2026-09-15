# Lesson 5 · evals · teaching script
Goal: an eval set of real cases and a gate that blocks a bad change. Skills: eval-set-construction,
deterministic-assertions, ci-eval-gate, github-actions, oidc-keyless-deploy, iam-trust-scoping.
Number: pass rate on 100 cases, and one change the gate blocks.

Carry-over from L4: three adjustments, from docs/learning-evidence.md
- Every saving or difference question comes after one worked "before minus after" on other numbers (E11: 0/2 first try in L4).
- Every Someone broke it question defines the labels inline (B11b: both L4 label misses were the word "wrong").
- The build goes one decision per message, each option with its effect on the target number worked through, then a debrief with the road not taken (B14: decision 5 "no deadline" predicted 736 ms, measured 1,753 ms; C31, C32).
Also: evals are where his weak spot lives (E1, quietly wrong); lean every part on catching quiet failures with numbers.

## R1-Av1 · A fixed test for every change
New: an eval set, a fixed list of real cases with what a right answer must contain
Status: withdrawn 2026-09-15 (undefined jargon: prompt, ship, summariser, eval set; C33)

# Lesson 5 · evals · Round 1 · Part A · A fixed test for every change

**The problem.** You change your summariser's prompt, try it on 3 invoices, they look fine, and you ship. By Monday 40 of every 100 summaries leave out the total, and nothing warned you.

**The fix:** keep an eval set, a fixed list of real cases each saying what a right answer must contain, and run every case after every change.

```python
cases = [
    {"invoice": "INV-001", "must_contain": "$120"},
    {"invoice": "INV-002", "must_contain": "$45"},
]
```

The pass rate is cases passed divided by all cases. To compare two runs, take before minus after: 90% then 85% is a drop of 90 - 85 = 5 points. Separate chances multiply: two coin flips both heads is 0.5 x 0.5 = 0.25.

**Picture:** a driving test on a fixed route. Every driver takes the same turns, so scores can be compared. A quick drive round the block tells you almost nothing.

- **The summary contains the `must_contain` text:** that case passes.
- **It does not:** that case fails.
- **Every change:** all cases run again, so two pass rates can be compared.

**Your turn.**

1. 100 cases, 88 pass. What is the pass rate?
2. The old prompt passed 88 cases and the new one passes 60. How many points did the pass rate drop?
3. The case says `must_contain: "$45"` and the summary reads "Total due: $54". Pass or fail?
4. 40 in 100 summaries are broken, so each checked invoice has a 0.6 chance of looking fine. What is the chance all 3 invoices you checked by eye look fine?
5. **Someone broke it.** The `must_contain` values were copied from the new prompt's own summaries, so the new prompt passes 100%. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 88%
2. 28 points (88 - 60)
3. fail
4. 0.216, about 22%
5. quietly wrong (the test just repeats the new prompt's answers)
Relies on: pass rate = passed / all; before minus after; separate chances multiply; a case passes only if the text is contained exactly

## R1-A · Checking every change the same way
New: a test case, one real invoice paired with the text a correct summary must include
Status: pending

# Lesson 5 · Round 1 · Part A · Checking every change the same way

**The problem.** Your app sends each invoice to the AI with the same written instructions, and the AI writes back a short summary. You reword the instructions, read 3 summaries, they look fine, and put the change live. A week later you find that 40 of every 100 summaries leave out the total amount.

**The fix:** before any change goes live, run it on the same list of real invoices, each paired with the one piece of text a correct summary must include. Each of those pairs is called a test case.

```python
test_cases = [
    {"invoice": "INV-001", "must_include": "$120"},
    {"invoice": "INV-002", "must_include": "$45"},
]
```

**Picture:** a teacher's answer key. For each exam question it lists the one thing a correct answer must have, so every student is marked exactly the same way.

- **The summary includes the required text exactly:** that test case passes.
- **It does not:** that test case fails.
- **After every change:** the whole list runs again and you count how many passed.

**Your turn.**

1. INV-002 must include `$45`. The summary says "Total due: $54". Pass or fail?
2. INV-001 must include `$120`. The summary says "Invoice total $120, due Friday". Pass or fail?
3. The list has 100 test cases and 88 pass. What percentage passed?
4. 40 in every 100 summaries leave out the total. Which is more likely to catch that: reading 3 summaries by eye, or checking all 100 test cases?
5. **Someone broke it.** The required text for every test case was copied from the new instructions' own summaries, so every test case passes. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. fail
2. pass
3. 88%
4. checking all 100 test cases
5. quietly wrong (the answer key was copied from the answers being marked)
Relies on: a test case passes only when the exact text appears; percentage = passed / all x 100
