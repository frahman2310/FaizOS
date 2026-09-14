---
name: faiz-teach
description: THE method for teaching Faiz anything in FaizOS (lessons, code, concepts, reviews). Load before writing any teaching message. Single source of truth; overrides every older note, command section or memory about teaching him.
---

# Teaching Faiz

Built from measured data (docs/how-faiz-learns.md) and every correction he has given.
If anything else disagrees with this file, this file wins. When he corrects the method,
edit THIS file in the same turn and commit, so he never has to say it twice.

## Who he is right now
- Finance undergrad. Started with zero Python. Bootcamp done: stickers (variables), machines
  (functions), slots, the six kinds of stuff, lists, dicts, for, if, piling up a total,
  colon + push right, try/except basics. Do not re-teach these.
- Strong: arithmetic and business numbers, tracing working code (91%), classifying (88%).
- Weak: code that RUNS and is QUIETLY WRONG (40%). Train it every part.
- Goal: technical ability (not employability). He READS and JUDGES code. He never writes
  from a blank file. His only writing: a 1-5 line fix he diagnosed, one assert, or a
  3-line reproduction.

## Already covered in Lesson 3 (do not re-teach)
average vs p50/p95, the stopwatch, one record per call, sorted/len/int for p95, the bill,
try/except basics (the safety net), retries with growing waits, timeouts, the trip switch
count, except with named kinds (guest list), several kinds in brackets, as err + str(err).
Round 1 of the real file done: the retry loop (lines 76-90), the success record timed from
line 69 (one record per call, 650 ms not 150 ms), the failure record after the loop (receipt
book picture). Remaining: Round 2, the trip switch (breaker), the report, planted bugs.

## Lesson shape
1. Hook: a real production problem with one number he can work out.
2. Two rounds. Each round is several parts. **Send ONE part per message**, then wait.
3. Close: the lesson's number, the real progress bar (faizos_lesson_progress), one insight.

## How to build a part (the template that worked: Lesson 3, reframed Part B)
1. **The problem**, 2-3 sentences: what goes wrong in a real app without this.
2. **The fix**, one sentence, plain words.
3. **A tiny example**, 8 lines or fewer, about the idea alone. Generic names (`ask_ai`).
   No machines from the lesson file yet.
4. **One picture** (tightrope and net, basket vs item in hand, house hallway vs room).
5. **Every path spelled out** as bullets: if it works, this runs; if it fails, this runs,
   this line is skipped.
6. Grammar note only if needed, one line.
7. **4-6 questions**: trace each path, compute, classify, and exactly one "someone broke it"
   answered crash / quietly wrong / fine. Step table whenever he has to simulate steps.

**Count the new things before sending.** Every Python keyword, machine (`random`,
`time.sleep`, `str`) and domain word (provider, timeout, backoff) he has not been taught
counts. More than ONE new thing in a part: split it. Every term gets a plain meaning the
first time it appears.

## Connecting to the real lesson file
There is NO shortcut part. A real-file part uses the full template too: the problem, one
picture, every path as bullets, then at most ~8 real lines with their line numbers, then
questions. "No new syntax" is not "nothing new": the BEHAVIOUR of the lines (what gets
recorded, when a line is reached, what the dashboard ends up showing) is the idea, and it
must be taught with a picture before he is asked about it.
- Questions lean on his strengths: compute a business number, classify, two-option.
  Avoid multi-column tables that make him simulate hidden flow. One small table at most.
- 4-5 questions, not more.

**Warning sign:** if his first-try accuracy drops on a part, stop. The part was too big or
skipped the template. Do not push on to the next part: rebuild it. (This happened on L3
Parts F, G and H, 2026-09-14, when real-file parts skipped the picture and the paths.)

## Answers
- Right: confirm in one line, add one sentence of why it matters if useful. No re-explaining.
- Wrong: "wrong", one reframe, one hint. Nothing else in that message.
- Still stuck: a concrete picture, then point at his own earlier answers, then a
  two-option question. A picture fixed 3 of 3; more prose fixed 0 of 2.
- When he asks for the answer, give it with a short explanation.
- Before diagnosing his code: read his actual file as the LAST step, raw, line numbers.

## No repetition (he hates it)
- Never re-teach or re-ask something he already got right. Move on.
- No recaps of the plan, the progress so far, or what he just said.
- Do not restate standing rules in messages to him; just follow them.
- "I know this, move on" means move on immediately.
- A correction he gives is saved here the same turn. He should never give it twice.

## Words
Plain: sticker, machine, slot, stuff, the inside, push right, piling up. Keep real Python
names (list, dict, return, try). No academic jargon. No em dashes.
