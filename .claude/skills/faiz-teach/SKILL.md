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
4. Close: the lesson's number, the real progress bar from `faizos_lesson_progress` (09-03), and
   the reflect step below.

## The part template (every part, including parts about the lesson file)
Parts built this way scored 24/30; parts that skipped it scored 3/11 the same day (A12, A13).
1. **The problem.** 2-3 sentences: what goes wrong in a real app without this (B4).
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
5. **Someone broke it.** They wrote `except KeyError:`. The AI takes too long.
   Crash, quietly wrong, or fine?
```

## The build
Every lesson ends in one build he understands and makes through concepts and decisions (09-14, C30).
1. **The build.** What it is and the one number it must hit, 2 sentences.
2. 3 to 5 decisions, each headed **Decision N:**, one situation with a real number, 2-3 options.
   Every option states what it costs and what it rules out ("rules out ___"). Only ideas already taught.
3. **Your call.** He picks an option for each decision and predicts the build's number.
4. I implement exactly his choices, run it, and paste the real output and the few lines that
   carry each decision in chat. He compares prediction and result. If the number is missed, he
   changes one decision and it runs again.
Build markers: `**The build.**` | `**Decision` | `**Your call.**`

## One new thing per part
- Count every keyword, machine (`str`, `time.sleep`) and domain word (provider, backoff) he has not
  been taught. More than one: split the part (B5).
- Give each new word a plain one-sentence meaning the first time it appears (08-06, 09-05).
- List every rule the questions rely on; each must be said in this part or already taught (B6, E7).

## Real lesson code
- Paste the lines in chat: at most 8, each with a short plain note. Never ask him to open the file,
  find a line number, or scroll (B7; 09-14: "30 minutes looking for the right part").
- Real lines come after the tiny example and picture of the same idea, never instead of them (A13).
- No write-it-yourself questions and no blank functions (09-12; blank builds 0/3, A10). A fix is
  asked as "which line, changed to what".

## Questions
- Five short-answer questions: compute a business number, trace which lines run or what a sticker
  is on, classify (caught or crash, inside or after the loop), and exactly one **Someone broke it.**
  answered crash / quietly wrong / fine (B10, B11).
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
  names (list, dict, return, try); no academic jargon (08-06, 09-05). A part is 2,000 characters or less (B8).
- No em dashes (his writing-style rule, v2 execution prompt).

## Delivery
- Write each part, and the build (id starting `BUILD`), into `projects/<lesson>/script.md` with its
  `New:` line and `### Key`, run
  `python3 scripts/check_lesson_script.py` until it passes, then send the part verbatim. The Stop
  hook blocks anything else (template skipped after it was a rule, C17).

## How this file changes
After every teaching session (the reflect step):
1. Run `python3 scripts/extract_teaching.py <transcript>` for the new question/answer exchanges.
2. Score each question: right first try, right after a hint, or answer given. Note the stuck
   points and his exact words about the teaching.
3. Append one row to the Session ledger in docs/learning-evidence.md, update the counts in the
   tables it touches, and update the "taught" list under the ledger.
4. Edit this file only when he stated a rule, or a finding changed direction across two or more
   sessions. Edit in place: replace the affected line, delete what it supersedes, never add a second
   rule on the same topic. His most recent words win. Cite the new evidence ID or date.
5. Run `extract_teaching.py <transcript> --mark`, log one line with `faizos_record_insight`
   ("REFLECT LOG: <session>, ledger row added"; a log entry, never a rule), then commit both files.
