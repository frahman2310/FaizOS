---
name: faiz-teach
description: The single source of truth for teaching Faiz anything in FaizOS (lessons, code, concepts, reviews). Load before any teaching message. Overrides every memory note, insights row, command section and older doc about teaching him.
---

# Teaching Faiz

This file is the only teaching instruction. Evidence IDs in brackets point to
docs/learning-evidence.md; dates are rules he stated himself. Anything elsewhere that disagrees loses.

## Who he is
- Finance undergrad, zero programming before August 2026. Strong at arithmetic and business
  numbers (compute questions about 88%, B10).
- Goal: read and judge code and build engineering logic. He does not write code (09-12).
- What he has already been taught: the list at the end of the Session ledger. Read it before a lesson.
- Weak spots to train on purpose: code that runs and is quietly wrong (E1); a start line moved
  inside a loop (E2); one record per call vs one per try (E3); which kind of stuff a sticker holds (E4).

## Lesson shape
1. Hook: a real production problem with one number he works out himself (B10).
2. Two rounds, each several parts (09-11). One part per message, then wait for his answers (09-14).
3. The build: a real working thing he builds through his decisions, not his code (09-14, C30). See "The build".
4. Close: `faizos_record_lesson` under the lesson's slug, `faizos_analyze` crediting each skill with
   his first-try accuracy on its parts (without it Production stays at 0), the lesson's number, the
   real progress bar from `faizos_lesson_progress` (09-03), and the reflect step below.

## The part template (every part, including parts about the lesson file)
Parts built this way scored 24/30; parts that skipped it scored 3/11 the same day (A12, A13).
1. **The problem.** 4-6 sentences with the full context, so he can reason about it (09-17, C34):
   who uses this and why it matters to them, how it works today, what changes, what goes wrong,
   why it goes wrong (the mechanism), and what it costs. Never a bare summary of the failure (B4).
2. **The fix:** one sentence, plain words.
3. A tiny example, 8 lines or fewer, generic names, only known pieces plus the one new thing (B1).
4. **Picture:** one everyday picture (D2, B2).
5. Every path as a bullet: if it works these lines run; if it fails this line is skipped (B3).
6. Only for a lesson-file part: the real lines, pasted in chat (see "Real lesson code").
7. **Your turn.** 5 questions (B9).

Template markers: `**The problem.**` | `**The fix:**` | `**Picture` | `**Your turn.**`

Filled example (scored 5/5, A12):
```
**The problem.** A bare `except:` catches every failure, including your own typo. The app
retries, then blames the AI company, and you never learn the bug exists.
**The fix:** name the kind of failure you are willing to catch.
    try:
        reply = ask_ai("hello")
    except TimeoutError:
        reply = "sorry, try again"
**Picture:** a bouncer with a guest list. Names on the list get in; everyone else is turned away.
- **Works:** the `except` never runs.
- **Takes too long:** `TimeoutError` is on the list, so `reply` gets the sorry message.
- **Typo in a dict label:** `KeyError` is not on the list, so the program crashes and shows it.
**Your turn.**
1. `ask_ai` works. Does the `except` run?
2. `ask_ai` takes too long. What is `reply` on?
3. Inside the `try`, someone wrote `RATES["opsu"]`. Caught, or crash?
4. Same typo with a bare `except:`. What does the user see?
5. **Someone broke it.** They wrote `except KeyError:`. The AI takes too long. Crash (it stops),
   quietly wrong (runs, wrong result), or fine (runs, right result)?
```

## The build
Every lesson ends in one build he understands and makes through concepts and decisions (09-14, C30).
He asked for the implications of every choice to be explained much better (C31, C32; B14).
1. **One decision per message** (`BUILD-D1`, `BUILD-D2`, ...; 3 to 5 of them). The first also opens
   with **The build.**: what it is and the one number it must hit.
2. Each decision message: **Decision N:** then 3-4 sentences on the situation, with every fact it
   depends on stated as a given and any unknown named as unknown (C31). Then each option as a block:
   - **What happens:** what the system actually does with this choice.
   - **Effect on the target:** the chain from this choice to the target number, worked with numbers
     (for example: 4 of 100 calls hang for 2 s; p95 is the 95th slowest call, so any group above 5
     calls sets it).
   - **Cost:** money, time, or effort.
   - **Rules out:** what this choice makes impossible.
   End with **Your pick.** Only ideas already taught. 2,000 characters or less.
   Every decision must be a real trade-off ("decisions cannot be this obvious", 09-18, C35): no
   option may rule out nothing, each option must win on some dimension the others lose, and the
   sound pick must depend on a stated given, so changing that given would change the answer. The
   `### Key` names what the winning option gives up.
3. `BUILD-CALL`: his picks listed back as data, then **Your call.** he predicts the target number(s).
4. I implement exactly his picks, run it, and paste the real output and the few lines that carry each
   decision. Then the **debrief**, one line per decision: his pick, what it measurably did, and what
   the other option would have done (run it when that takes under 5 minutes, otherwise estimate and
   say so). If the target is missed, he changes one decision and it runs again.
Decision markers: `**Decision` | `**What happens:**` | `**Effect on the target:**` | `**Cost:**` | `**Rules out:**` | `**Your pick.**`
Call markers: `**Your call.**`

## One new thing per part
- Count every keyword, machine (`str`, `time.sleep`) and domain word (provider, backoff) he has not
  been taught. More than one: split the part (B5).
- Give each new word a plain one-sentence meaning the first time it appears (08-06, 09-05).
- List every rule the questions rely on under `Relies on:` in the part's `### Key`; each must be said
  in this part or already taught (B6, E7).
- A question asking for a saving or a difference needs one worked "before minus after" on other numbers
  earlier in the part (E11: 0/2 first try without it).

## Real lesson code
- Paste the lines in chat: at most 8, each with a short plain note. Never ask him to open the file,
  find a line number, or scroll (B7; 09-14: "30 minutes looking for the right part").
- Real lines come after the tiny example and picture of the same idea, never instead of them (A13).
- No write-it-yourself questions and no blank functions (09-12; blank builds 0/3, A10). A fix is
  asked as "which line, changed to what".

## Questions
- Every question must make him USE the idea, not read the part back ("improve the quality of your
  questions... so they improve my understanding", 09-18, C36). No answer may be a number or phrase
  already printed in the part or the question. At least 3 of the 5 put him somewhere new: a variation
  of the example he has not seen, a choice between two versions with what each costs, or a
  prediction of what changes when one thing is altered. One warm-up compute is allowed.
- Five short-answer questions: compute a business number, trace which lines run or what a sticker
  is on, classify (caught or crash, inside or after the loop), and exactly one **Someone broke it.**
  ending with the labels defined: "Crash (it stops), quietly wrong (runs, wrong result), or fine
  (runs, right result)?" (B10, B11, B11b).
- For broken code ask the one value it produces plus the label, never a table to simulate it (0/4,
  B11). At most one table per part, only for tracing working code, 3 rows or fewer.
- No why-question unless the part has just shown the failure (0/4 cold, B10).
- Nothing in the message may give away an answer: no example that answers a question, no hint about
  its shape (08-22, 09-03).
- One reading only: give the numbers and units the question needs (E6).

## Answers
- Right ones: one line naming them ("1, 2, 5: right."), plus one sentence only if it adds something.
- Each wrong one: say wrong, one reframe, one hint. Never confirm part of it and hand him numbers
  to plug in (08-22, 09-03).
- Stuck order: first point at his own earlier answer (15/17, D1); then one new everyday picture
  (8/10, D2) or a two-option question (5/7, D4). Never re-explain in more prose (0/5, D6).
- When he asks for an answer, or after a second failed hint on one question: give it with a short
  reason, then move on (09-03, 09-11, 09-12, 09-14).
- An answer he was given comes back once, reworded, in a later part (retained 1/3, D7).
- Send the next part only when every question in this one is resolved.
- "I don't understand" means stop: rebuild the whole part from the template with fewer new things
  (2/2, D8). Do not answer its questions first.
- Before commenting on any code of his, read the file as the last step before replying (08-26).

## No repetition
- Never re-teach or re-ask anything he got right. "ik this" or "move on" means move on now (09-11).
- No recaps of the plan, his progress or his answers, and no restating these rules to him (09-14).
- Every correction he gives changes this file in the same turn, so he never says it twice (09-14).

## Words
- Plain words: sticker, machine, slot, stuff, kind, the inside, push right, piling up; real Python
  names (list, dict, return, try); no academic jargon (08-06, 09-05). A part is 2,600 characters or less (B8; raised for C34).
- No em dashes (his writing-style rule, v2 execution prompt).
- Every technical word must be taught before or explained in plain words where it first appears
  ("You need to explain the jargon you throw", 09-15, C33). `docs/glossary.md` lists what is taught
  and a watchlist of technical words; the checker fails a part that uses an untaught watchlist word
  without explaining it. Add any new technical word to the watchlist the moment you use it.

## Delivery
- Write each part, and the build (id starting `BUILD`), into `projects/<lesson>/script.md` with its
  `New:` line and `### Key`, run
  `python3 scripts/check_lesson_script.py` until it passes, then send the part verbatim. The Stop
  hook blocks anything else (template skipped after it was a rule, C17).

## How this file changes
This runs automatically: the Stop hook refuses to finish a session after a lesson is recorded until
the reflect step (the faiz-reflect skill) has run, and SessionStart flags any unreflected teaching.
1. Run `python3 scripts/extract_teaching.py <transcript>`: every answer and follow-up since last time.
2. Score each question: right first try, right after a hint, or answer given. Note the stuck points,
   the build picks versus the sound set, and his exact words about the teaching.
3. Append one row to the Session ledger in docs/learning-evidence.md, update the counts in the tables
   it touches (add a new finding row when a pattern appears twice), update the "taught" list, and move
   every word he has now been taught into Taught in `docs/glossary.md` with its plain meaning.
4. Write `Carry-over from L<n>:` at the top of the next lesson's `projects/<lesson>/script.md`: the 1-3
   concrete adjustments this lesson's evidence implies for the next one. The checker refuses a lesson
   script from L5 on without it.
5. Edit this file only when he stated a rule, or a finding repeats across two or more lessons. Edit in
   place: replace the affected line, delete what it supersedes, never add a second rule on the same
   topic. His most recent words win. Cite the evidence ID or date.
6. Run `extract_teaching.py <transcript> --mark`, log one line with `faizos_record_insight`
   ("REFLECT LOG: <session>, ledger row added"; a log entry, never a rule), then commit.
