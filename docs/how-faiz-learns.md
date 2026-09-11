# How Faiz learns

Measured from the Python bootcamp (2026-09-11, 10 rounds, 89 questions, taught in chat), set
against lessons 1-2, the drill and the first attempt at lesson 3. This file is the operating
manual for every lesson from L3 on. It supersedes the one-big-file format in
`faiz-teaching-method`.

## The result

| | Before the bootcamp | In the bootcamp |
|---|---|---|
| Writing code with 2+ new pieces, from blank | **0 of 5** | **4 of 5 first try, 5 of 5 by the second** |
| First-try accuracy on questions | about 60% (L2, drill, L3 opener) | **71 of 89 (80%)** |
| Old crashes he diagnosed himself | 0 | 5 (text division, lost `"haiku"`, `return` in the loop, whole list passed, `price_of` from another file) |

He wrote his first unaided `for` line, running total and `if`, and then `total = total +
c["tokens"]`, the exact line he got wrong when lesson 3 opened a week earlier.

Nothing about his ability changed between the two columns. The teaching did.

## Accuracy by question type

| Question type | First try | What it tells us |
|---|---|---|
| Compute or trace a working program | **30 of 33 (91%)** | His strength. Arithmetic plus a clear model of stickers = near-perfect. |
| Classify (which kind / legal or crash / yes or no) | **22 of 25 (88%)** | Fastest way to find a wrong belief. Cheap, high-volume, fun. |
| Write it yourself, after tracing it | **4 of 5 (80%)** | Works when it comes **after** 4-8 trace questions on the same idea. |
| Predict what a broken version does | **4 of 10 (40%)** | **The weak spot.** See below. |

## The weak spot: crash or quiet wrong answer

Every broken-code question he got right was one where the break **crashes** (missing sticker,
missing slot). Every one he got wrong was one where the code **runs and quietly gives a wrong
answer**, or the reverse:

- slots filled in the wrong order: he said crash, it runs
- `total = 0` moved inside the loop: "idk", it runs and ends on 90
- appending onto a pre-filled list: skipped, it runs and doubles the list
- a dict asked for a missing label: he said "nothing", it crashes

So his model of **when Python stops versus when it carries on wrongly** is unreliable. That is
the single most useful thing to fix, because silent wrong answers are exactly what evals,
tests and monitoring exist to catch. Lessons 5 and 6 are built on it.

**Rule:** every round includes one or two "someone broke it" questions, always with a
fill-in step table, never as a bare "what happens?".

## Where the other 18 misses came from

| Cause | Misses | Fix |
|---|---|---|
| Crash vs quiet wrong answer | 5 | the rule above |
| Skimming a symbol (quotes, a capital letter, position 2 vs 3rd item) | 4 | put contrast pairs (`price`/`Price`, `3`/`"3"`) in the quick-fire, routinely |
| Mixing up kinds (the list vs one item, a dict vs the number inside it) | 3 | ask "what kind is this?" before any line that uses it |
| **A rule I never stated** (`return` stops the machine, top-of-file stickers are visible inside, my own bad wording) | 3 | before a round, list every rule its questions rely on and check each was said out loud |
| Connecting two things he already knew | 3 | point him at his own two earlier answers |

None of the 18 was carelessness. Each one was a missing rule or an untrained judgement.

## What fixed an "idk"

| Recovery move | Worked |
|---|---|
| One concrete picture (cashier closing the till, basket vs item in your hand, house hallway vs room) | **3 of 3**, instantly |
| Point at his own two earlier answers | 2 of 2 |
| Shrink to a two-option question | 1 of 1 |
| Step table with the last cells blank | 1 of 1 |
| Re-explaining in prose, or asking him to simulate a broken version unaided | **0 of 2** |

When he asks outright for the answer after two tries, give it with the explanation. He has said
so twice. Never reveal it unasked.

## Why the bootcamp worked

1. **Every rule was taught before it was tested.** The only misses of that kind were the three
   rules I forgot to say.
2. **Trace, then write.** Every "write it yourself" came after a run of trace questions on the
   same idea. That is why the writing questions went from 0 of 5 to 5 of 5.
3. **Plain words, one picture per idea.** sticker (variable), machine (function), slot
   (parameter), stuff (value), the inside (block), push right (indent), piling up (running
   total). Real Python names (list, dict, `return`) stayed; academic words went.
4. **Many small questions.** 5-10 per round. He asked for more, not fewer.
5. **His own crashes as the examples.** Each round ended with him diagnosing a real mistake he
   had made. It turns a past failure into a solved puzzle.
6. **In chat, short messages, no file.** Zero friction between the question and the answer.
7. **He sets the pace.** "ik this dont repeat" means move on. Accept a correct verbal answer
   rather than making him write it out.

## The lesson format from L3 on

Every lesson is a run of bootcamp-style rounds, then one small build.

1. **Hook:** one money number he can work out in his head.
2. **Rounds, in chat.** Each round is one idea: plain words, one picture, then 5-10 quick
   questions. Mostly classify and compute, one or two "someone broke it" with a step table,
   ending with one "write it yourself" line.
3. **New libraries are taught as machines someone else built:** its name, its slots, what comes
   out. Same vocabulary as the bootcamp. At most one new piece of Python grammar per lesson.
4. **The build:** a small file holding only the task and a PASS/FAIL checker. No teaching inside
   the file. Each task asks for one or two new things at most.
5. **Close:** the lesson's number, the real progress bar, and one insight recorded.

Wrong answers: "wrong", one short reframe, one hint. If still stuck: a picture, then his own
earlier answers, then a two-option question. Reveal only when he asks.
