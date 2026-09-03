# What actually works, measured

An analysis of every question asked and every task attempted in the session of
2026-08-22 to 09-03. Written because impressions were wrong and the numbers are not.

## Every question, sorted by type

**Type A — compute a number from a stated rule.** 8 of 9 first try, 9 of 9 with one retry.
Cost of 2,000 tokens; which of two costs more; flash and haiku on two workloads; `cost(0, 1M, 3, 15)`;
`final = price + tax`; packages installed from one declared. The single miss was an arithmetic slip
he corrected immediately.

**Type B — apply a stated rule to a case.** 5 of 6 first try.
What is wrong with `return total = x`; `wrap_cost` when `wrapped=0`; which names exist inside a
`def`; `RATES["sonnet"]["out"]`; tracing `longest_word` to pass 2. The miss was the support-bot
question, right on retry.

**Type C — explain why a design choice was made.** **0 of 4.**
Why `daily_cost` calls `cost()` rather than duplicating it. What breaks if you write `2.5` instead
of `item_price * 0.5`. Why `None` rather than `0`. Which function returns money and what three
things it needs. Every one came back "idk".

**Type D — write the code.** Lesson 1: 9 of 9 first try. Lesson 2 Task 1: three attempts.
Lesson 2 Task 2: four attempts, then supplied.

## The finding that explains lesson 2

Count the genuinely NEW things each code task required him to produce.

**Lesson 1, `cost_with_cache`:** three named lines instead of two, added in a return. He had written
two-named-lines-then-return twenty minutes earlier. **New things: 1.** Result: 9 of 9, first try.

**Lesson 2, `cheapest_model`:** `for` syntax with its colon and indent; two trackers initialised to
`None`; `is None`; `or`; `<` inside an `if`; a three-argument function call; loop variable versus the
list it came from; values reaching in from the enclosing function's parameters; `return` positioned
outside the loop. **New things: 9.** Result: four failed attempts.

The v1 record already contains this exact number, recorded twice: *nine concepts produced 1 of 5
blanks, three concepts produced 3 of 3.* Lesson 2's task was a nine-concept task and it produced
0 of 1. The cap was known and I ignored it for the code task while respecting it in the teaching.

**The teaching format was not the problem. The task size was.**

## What demonstrably works

1. **Trace tables with real numbers.** `[12, 7, 20]` walked pass by pass; the `longest_word` trace;
   the fruits loop. He read every one correctly. This is the highest-yield format found.
2. **A concrete analogy for an abstraction.** The parcel — label outside, contents inside — fixed
   the quoted-name error in one attempt after two failures.
3. **A worked example in another domain that transfers EXACTLY.** `shop_bill` transferred (three
   named lines, one return, an optional extra) and produced 9 of 9. `longest_word` did not
   transfer: it used `len()`, never taught, and `>`, the wrong direction for a cheapest search. He
   copied it faithfully including both wrong parts.
4. **Grouped teaching blocks, three or four questions at the end.** He answers fast and engages.
   One-concept-one-question was too slow and he said so.

## What demonstrably fails

1. **Navigation instead of teaching.** "Scroll up and read the def line", "count the commas". He
   broke a line that was already correct while following it.
2. **Worked examples containing parts that do not transfer.** See `longest_word` above.
3. **Why-questions asked cold.** 0 of 4. Design rationale is tacit knowledge learned by being
   burned. Asking him to invent it unprompted asks for something he has never seen.
4. **Code tasks above two new things.**

## The adaptation

**Hard cap: two new things per code task.** Four is the cap for concepts taught; for code he must
produce from nothing, it is two. A loop that keeps a running best is nine, so it gets split:

- task A: write a loop that visits each item and prints it. New things: 1.
- task B: add a running total. New things: 1.
- task C: replace the total with keep-the-best. New things: 2.

Three tiny wins beat one long failure.

**Never ask a why-question cold.** Show the failure first — the duplicated line that goes silently
wrong when one copy changes, the tracker at zero that rejects everything — then ask him to apply
it. Teach the rationale, then test the application.

**Every worked example uses the same operation and the same direction as the task.** If the task
searches for a minimum with `<`, the example searches for a minimum with `<`. No new built-ins.

**Keep:** trace tables, concrete analogies for abstractions, grouped blocks with three or four
questions, and the one-file build.

**On errors:** `api-misuse` is at 7 occurrences and `ordering-pairing` at 4. Both are the same
underlying gap — a name, the value it holds, and which of the two you are passing. That gets its
own drill before any further code task.
