# Review of the code rebuild (code-01, code-02 and the shared layer)

Written 2026-09-25. Independent and adversarial. Nothing was edited except this file. Read in full:
`gap-audit-code.md` (G1 to G20), `audit-pedagogy.md` (all findings), `curricula/code-teaching-experts-v2.md`,
`docs/learning-evidence.md` (C1 to C49), `structures/INTEGRATED.md`, `structures/code.md`,
`.claude/skills/faiz-teach/SKILL.md`, `learn/check_unit.py`, `learn/engine.py`, `hooks/teaching-guard.py`,
`learn/selftest.py`, and both units, read step by step as he would receive them. Every program listed in
both unit headers was run again. Engine flows were run in a scratch copy of `learn/` with its `.venv` python.
Guard checks that needed a cursor were run with the cursor file created and removed again.

## Verdict

**Not ready today; ready after one small fix.** The teaching itself is rebuilt properly: both units now
show, then practise with him, then test, with worked examples, faded tables, line-by-line readings,
self-explanation prompts, hinge questions whose wrong options each name a known mistake, prepared Help
examples and a Retry and Cold item. Every program output matches its saved run, and every Key is right.

One blocker stops the mastery loop the rebuild depends on: the engine cannot record a Retry (B1). With a
90% bar on one 11-part item, a miss on code-01 is quite likely, so fix this before the sitting. I also
strongly recommend fixing M3 and M4 (Show 2 and Show 3 of code-01 carry more new ideas than declared)
before he sees it, because overload was his main complaint (C49).

**Counts: 1 blocker, 7 major, 16 minor.**

---

## 1. Finding by finding

### Gap audit (G1 to G20)

| # | Status | Evidence |
|---|---|---|
| G1 worked example missing | FIXED | `code.md:85-99` (Show 1 to 3); `check_unit.py:120-121` (first step must be a show); both units have three Shows. Hole: "show" is only a label the author writes (M1) |
| G2 machinery forbids modelling | FIXED | `check_unit.py:31,133-139` Kind show; the guard accepts any step word for word (`teaching-guard.py:96-117`); selftest passes every step in order |
| G3 scored question on untaught code | FIXED | `check_unit.py:124-128` (scored only after a show and a try); both units `scored: Your turn` |
| G4 commit first on new patterns | FIXED | `INTEGRATED.md:35-41` |
| G5 no backward fading | FIXED in units | code-01 Show 1 table filled (l.68-72), Try 1 last row blank (l.97-100), Try 2 two blanks (l.175-179). Not checked by the checker (M1) |
| G6 tables before tracing taught | FIXED | `code.md:40-41`; code-01 Show 1 defines and fills the table |
| G7 Sorva misread | FIXED | `code.md:43`, `code.md:266` |
| G8 no self-explanation prompt | FIXED | every Show ends "One line from you" (code-01 l.74, 151, 234; code-02 l.73, 150, 232) |
| G9 5+ new constructs per step | PARTLY | cap exists (`check_unit.py:132-139`) but counts only what the author lists; no check against a taught list; code-01 Show 2 and Show 3 undercount (M2, M3, M4) |
| G10 house words counted as taught | FIXED | sticker, machine, slot gone from `glossary.md` Taught; units use variable, function, argument, return value, dict, key, list. The checker would not catch "sticker" returning (not on the watchlist) |
| G11 explanation is a summary | FIXED in Shows | code-01 l.59-62, 138-142, 218-222 read in run order with the value each line leaves. Checker only looks for the heading (`check_unit.py:201`) |
| G12 tiny example only as fallback | FIXED | code-01 Show 1 is a 3-line program; code-02 Show 1 a 5-line one |
| G13 subgoal labels hidden | FIXED | labels in Goal (code-01 l.22-29), in the header, and "Steps on hand" under tries |
| G14 broken before correct | FIXED | first broken program is code-01 Show 3 (l.225-232), after two correct examples, and labelled |
| G15 placement not built | NOT FIXED | `code.md:114-116` decides "not yet" in words; no First step item; `code.md:165-166` still says "likely starts at L1 on T2" |
| G16 bar on guided cells | FIXED | `INTEGRATED.md:63`; `engine.py:38-45` counts only the header's scored steps |
| G17 checks not diagnostic | FIXED | hinge options mapped to named mistakes (code-01 Key l.115, l.272; code-02 Key l.117) |
| G18 earlier audit enlarged tables | FIXED | tables are 2 to 4 rows |
| G19 D5 misread | FIXED | `code.md:59-62` |
| G20 freeze blocked the fix | FIXED | `SKILL.md:76-78`; `INTEGRATED.md:57-59` |

### Pedagogy audit, findings that touch code or the shared layer

(C2, C8, C9, Q3, Q5, Q6, X5, X6, M1, M3, M4, M5 are LLM, production, evaluation or design only and were not
re-checked. Q1 was about the old code-03, which no longer exists.)

| # | Status | Evidence |
|---|---|---|
| C1 no worked-example step | FIXED | as G1 |
| C3 hint scoring | PARTLY | 0.5 after a hint is now one rule (`SKILL.md:38`, `INTEGRATED.md:49`, `engine.py:15`); still undefined whether stuck moves 1 and 2 on the scored step count as hints; `INTEGRATED.md:67` still says "within 2 attempts" for edits |
| C4 cold bar | NOT FIXED | `code.md:194` says 80% cold; `INTEGRATED.md:46-47` "the same bar cold"; `engine.py:361` uses 90 on one item (M7) |
| C5 answer capped at one line | FIXED | `SKILL.md:53-54`; the guard only checks messages that ask for an answer |
| C6 one stuck order, guard re-send | FIXED in words | same four moves in `INTEGRATED.md:43-45`, `SKILL.md:55-58`, `code.md:118-120`; Help blocks re-ask the step. But see M5 (retry re-teach) and M6 (moves 2 and 4 not prepared) |
| C7 template not checked | PARTLY | units follow it; checker does not enforce it |
| C10 three step lists | PARTLY | `code.md:85-99` is the list; `INTEGRATED.md:15` still shows the old steps (with a note under it); stale lines in `code.md` (minor 14) |
| C11 missed unit never served | FIXED in design, broken in code | `engine.py:169-191` RETRY then parallel; Retry cannot be recorded (B1) |
| C12 rungs ignored | NOT FIXED | `next_unit` still ignores rung |
| C13 cards added on a failed unit | NOT FIXED | `engine.py:372` runs whatever the result; confirmed in the scratch run |
| C14 two new formats in sitting 1 | FIXED | `engine.py:258-259`; confirmed: sitting shows code-01 only |
| C15 message size | FIXED | largest code step 2,014 characters (code-01 Show 2) |
| C16 freeze | FIXED | as G20 |
| S1 scored opener | FIXED | as G3 |
| S2 tracing not modelled | FIXED | as G5, G6 |
| S3 debug card cold | FIXED in design | `code.md:110` (modelled once first); not in these units |
| S4 no guided practice | FIXED | three tries per unit |
| S5 cards and cold from unseen text | PARTLY | both units' cards and Cold are answerable from shown text; the checker does not test it |
| X1 explanation not a reading | FIXED in Shows | as G11 |
| X2 element interactivity | PARTLY | code-02 is well split; code-01 Show 2 and Show 3 are not (M3, M4) |
| X3 tiny example, picture | FIXED | bank statement, bank counter, ledger, clerk pictures |
| X4 names not shown | PARTLY | code-02 Help: Try with me 3 prints output from lines not shown (minor 6) |
| Q2 aim comments | FIXED | code-01 Your turn l.291-303; code-02 l.316, l.324 |
| Q4 padded tables | FIXED | 2 to 4 rows |
| Q7 close lines as self-graded cards | NOT FIXED | `engine.py:382-386` |
| T1 all-or-nothing on one item | PARTLY | one 11-part item at 90%, hint = 0.5, miss leads to Help and Retry; still one item per unit |
| T2 no corrective | FIXED in units | Help blocks for every try and the scored step; engine path broken (B1, M5) |
| T3 prediction before any material | FIXED | `SKILL.md:35-36` (just before the first scored step) |
| T4 self-grading of recall | NOT FIXED | `SKILL.md:26-28` |
| T5 gating on first exposure | PARTLY | gate is the independent item plus 7-day cold, but the independent item is still in the first sitting |
| M2 PRIMM predict scored | FIXED | no scored Predict remains |
| M6 interleaving from day 1 | NOT FIXED | `engine.py:200-211` |
| B1 stuck order does not teach | FIXED | Help move is a second worked example |
| B2 prepared correctives | PARTLY | Help prepared; "two options" and "the answer worked line by line" are not (M6) |
| B3 answer-level feedback | PARTLY | tables now small; `SKILL.md:51-52` still one reframe, one hint |
| B4 no check question before a step | NOT FIXED | `teaching-guard.py:118` |
| B5 guard fails closed | NOT FIXED | `teaching-guard.py:139-140` |
| B6 tutor never models | FIXED | Shows are the model |

---

## 2. The session as he receives it

I read each step body in order, as someone who has never seen a dict, a function or a list. Faiz has in
fact seen dicts, lists and KeyError in the bootcamp (ledger "taught" list), so where the stricter reading
and his record disagree, both are noted.

**code-01**

| Step | New ideas (real) | Terms explained? | Question answerable, ~80%? | Notes |
|---|---|---|---|---|
| Goal | AI model, dict, key, value, four steps, function (forward) | yes, except "call" ("how much text the call used", "Call the function") and "returns" before Show 2 | "ready" | fine; declared New lists only the steps |
| Show 1 | variable, lookup, trace table (dict again) | yes, including `=` and trace table | yes, about 95% | model Show |
| Try 1 | none | yes | yes, about 90% | "Steps on hand: call and keep ..." when there is no call: noise (minor 4) |
| Show 2 | function, `def`, argument, return value, **tokens**, **indented body**, **local name gone after the call** | "indented" and "body" not explained (explained only in code-02 Try 3); "stand-in", "offline" fine | yes, but a read-back ("does reply hold the text or the whole dict?" is stated two lines up) | 2,014 characters, 5 to 6 real ideas vs 3 declared (M4) |
| Try 2 | none | yes | yes, about 80% | good |
| Show 3 | nesting, list, `[0]`, chained lookups, dict over several lines, `stop_reason`, KeyError, **crash** label, **quietly wrong** label | yes | yes | 6 to 8 real ideas vs 3 declared, 4 code blocks (M3); "fine" is never shown as a labelled example before Your turn |
| Try 3 | `max_tokens` | yes | yes, about 80% | good hinge |
| Your turn | **comments with `#`**, **print with two values** | both explained inside the scored step | yes, if Show 3 landed | new syntax first met in the marked item (minor 2) |
| Close | none | | yes | |

Sentences he could stumble on: "how much text the call used" (Goal l.20, "call" not yet defined);
"The indented `return` line is the function's body" (Show 2 l.140); the table row "gone: it only exists
inside the function" (Show 2 l.147), which adds variable scope for no gain in this unit.

**code-02** reads well. Each Show adds 2 to 3 ideas, the pictures fit (ledger, clerk), the Parsons try is
well built. Show 3 (l.196-239) is the heaviest: two functions, one calling the other, a list passed in
and changed (the "same list, not a copy" idea, a classic wall), and `return` ending the function. It is
explained with a picture and a table, so I rate it acceptable. `first` is kept but never used, which a
novice may puzzle over (minor 7). Show prompts at l.73 and l.232 are read-backs of the text just above
(C36 asked for questions that build understanding).

**How this code works blocks.** In every Show they do teach reading line by line, in run order, with the
value each line leaves. In tries and scored steps they are short summaries, which is right: a full reading
there would give the answer.

---

## 3. Correctness

- All 38 code-01 programs and 30 code-02 programs listed in the headers were run from
  `learn/code/code-0N`. Every output matches its saved run (file paths in tracebacks aside).
- Every output block in a step body appears in a listed run (checker plus my reading).
- Every Key is right: code-01 Try 1 (900, B), Try 2 (dict, 6, 6), Try 3 (C, 20), Your turn (A crash, B
  quietly wrong, C fine, D quietly wrong), Retry, Cold; code-02 Try 1 (A, 3), Try 2, Try 3 (R, S, P, Q; T
  extra, quietly wrong), Your turn (4 prints; B `KeyError` on the first call before any print; C prints the
  record), Retry, Cold.
- Every Score line is markable: 11, 11, 11 parts (code-01), 10, 10, 11 parts (code-02), each part a
  clear right or wrong. At the 90% bar he may miss one part.
- Help blocks: all four in each unit are correct and on a new surface. Cards: correct, each with a second
  surface.

---

## 4. Machinery

`python3 learn/check_unit.py learn/units/*/*.md`: all 7 units PASS. `python3 learn/selftest.py`: all
attacks caught, exit 0.

**Units that pass the checker but break the rules** (built in a scratch copy from code-01):

| Attack | Result |
|---|---|
| Delete Show 1, 2, 3 and Try 2, 3: prose Goal (Kind: show), one try, then the scored item on nesting and KeyError never shown | **passes** |
| Show 3 declares `New: -` | passes |
| Show lists 6 ideas joined by `;` | passes (counted as 1) |
| A try that asks him to fill every cell of a blank table | passes |
| How block reduced to "**How this code works.** It works." | passes |
| A try with a `Score:` line | passes |
| No Help for any try, only for Your turn | passes |
| Retry an exact copy of Your turn | passes |
| A try with 10 questions | passes |
| Cold Key without `Kind: scored` | passes |
| A card (with a variant) on a rule never shown | passes |
| "sticker" used unexplained | passes |

**Engine flows** (scratch copy):

- `today` gives code-01 alone in sitting 1 (right). `done` without a prediction is refused (right).
- A miss (`Your turn=0.64`) is recorded "not yet"; the next code sitting says RETRY (right).
- **`predict code-01 80 --retry` stores the prediction under `code-01`, and `done ... --retry` then fails
  with "no prediction recorded for code-01:retry"** (B1). After patching the state file by hand, a failed
  retry leads to "missed twice: prepare a parallel unit" and a passed retry moves on (right).
- Cold is refused before its date (right), then accepted, but a failed cold changes nothing and a second
  cold can be recorded; a cold recorded under any step name other than `Cold` scores 100 and "not yet".
- The unit's cards enter recall after the failed session (C13).

---

## 5. Cohesion

Agree: show, try, then scored; tries unscored with an 80% aim; bar only on scored, Retry and Cold; hint =
0.5, answer given = 0; the four-move stuck order; Help then Retry after a miss; one unit per sitting in
weeks 1 and 2; prediction just before the first scored step.

Disagree:
- Cold bar: `code.md:194` 80% vs `INTEGRATED.md:46-47` and `engine.py:361` 90 (M7).
- RETRY re-teach: `engine.py:181` and `SKILL.md:43` say re-send the show steps; the guard forbids it (M5).
- Stuck moves 2 and 4 must come "from the unit" (`SKILL.md:57-58`, `INTEGRATED.md:45`), but no unit holds
  them (M6).
- Step lists: `INTEGRATED.md:15` still names Predict, Trace, Change; `code.md:95` says Your turn traces "in
  full" (code-01's does not); `code.md` sections 3a, 5 and 7 still use the old trace-cell bars and a
  "Predict step" measure (minor 14).
- Help: `code.md:97` says one for every try and the scored step; the checker needs only one (M1).

---

## Findings

### Blocker

**B1. A Retry cannot be recorded.** `learn/engine.py:316` stores every non-cold prediction under the bare
unit id and ignores `--retry`; `engine.py:328-332` looks for `code-01:retry` and fails. SKILL.md step 5
tells the tutor to run exactly these two commands. The first miss stops the corrective loop.
Fix: line 316, key `f"{a.unit}{':cold' if a.cold else ':retry' if a.retry else ''}"` (and the message on
line 318); add a selftest flow: predict, miss, predict --retry, done --retry.

### Major

**M1. The checker cannot see whether a "show" shows anything.** `check_unit.py:120-128` trusts the Kind
label, so a prose Goal plus one try plus the scored item passes with no worked example at all, and a try
can be a 40-cell blank table. Fix: the first try must come after a show holding a python block, its output
block and a filled table or line-by-line list; at least as many shows as tries before the scored step; a
Help block for every try and the scored step (`code.md:97`); a question cap per try (about 5).

**M2. The new-idea cap counts only what the author writes.** `check_unit.py:132-139`: `New: -` or ideas
joined by `;` pass. The gap-audit fix (G9: fail a Show that uses a construct not in `New:` or a taught
list) was not built. Fix: split `New:` on `,` and `;`; keep a taught-constructs list per unit (`builds on:`
plus earlier units' `New:`) and flag code lines using a keyword or form (def, return, append, len, `[0]`,
`#`, two-value print) not in either.

**M3. code-01 Show 3 carries 6 to 8 new ideas, declared as 3.** `01-reading-an-ai-reply.md:196-241`:
nesting, list, position `[0]`, chained lookups, a dict over several lines, `stop_reason`, KeyError, and
both the crash and quietly wrong labels, in 4 code blocks. "fine" is never shown as a labelled example
before Your turn (`code.md:107` requires one of each). Fix: keep Show 3 to nesting, list and `[0]`; move
the two slips into a short Show 4 with one example of each label (crash, quietly wrong, fine), followed by
a label-only try before Your turn.

**M4. code-01 Show 2 carries 5 to 6 new ideas, declared as 3.** `01-reading-an-ai-reply.md:118-158`: adds
tokens, an indented body ("indented" and "body" unexplained here) and local scope (table row l.147), at
2,014 characters. Fix: drop the "gone" row, explain indent in one clause, move tokens to Show 3 where
`usage` first matters; turn the prompt into a why question ("why does `reply` hold a dict and not the
text?").

**M5. The RETRY re-teach is blocked by the guard.** `engine.py:181` and `SKILL.md:42-44` say re-send the
Help blocks and "the show steps he missed"; `teaching-guard.py:127-131` blocks any step already sent
(confirmed with a finished cursor: "steps go forward only"). Also `Help: Your turn` (code-01 l.469,
code-02 l.473) says "back to your four programs", which are not on screen in a later sitting. Fix: when
`engine.py today` says RETRY, write a cursor flag that lets that unit's shows be re-sent once; give each
unit a short retry opener, or word the Help blocks so they stand alone.

**M6. Stuck moves 2 and 4 have no prepared text.** `SKILL.md:55-58` and `INTEGRATED.md:43-45` require
"two options" and "the answer worked line by line" and forbid improvised prose; no Key holds either (Keys
give the answer, not a worked line-by-line version). The tutor must improvise exactly where he is most lost
(pedagogy B2). Fix: add `Two options:` and `Worked answer:` lines to every try and scored Key; checker
requires them.

**M7. Cold bar and cold miss are undefined across the documents.** `code.md:194` 80% cold;
`INTEGRATED.md:46-47` same bar; `engine.py:361` 90 on the single item named `Cold`. A failed cold triggers
nothing, and repeated cold records are accepted (`engine.py:340-346`). Fix: one number in INTEGRATED section
3 and code.md section 5; engine refuses a second cold; a cold miss is listed by `today` with the unit's
Help blocks and its Retry, as for a session miss.

### Minor

1. Retry repeats what was just shown. SKILL step 5 sends Help blocks right before Retry; code-01 Retry D
   (l.501) is the same line and aim as Help: Your turn's second example (l.450), and Retry C (l.497)
   repeats Show 3's crash. Swap in a different slip (for example `reply["content"]["text"]`).
2. code-01 Your turn introduces `#` comments and a two-value `print` inside the scored item (l.284, l.306).
   Show both in Show 3 or the label Show.
3. "call" and "returns" used in Goal before Show 2 defines them (code-01 l.20, l.24).
4. "Steps on hand: call and keep ..." under Try 1, which has no call (code-01 l.87).
5. Show prompts that are read-backs of the line above: code-01 l.151, code-02 l.73, l.232 (C36).
6. code-02 Help: Try with me 3 prints `Sent` and `[{'name': 'Ali', 'tokens_out': 2}]` from a call, prints
   and a stand-in not shown (l.418-429). Show the three missing lines.
7. code-02 Show 3 stores `first` and never uses it (l.209); function calling function is not named.
8. `engine.py` accepts any number of retries and cold records; cold "passed" reads only the step `Cold`.
9. Cards join recall after a failed unit (`engine.py:372`; pedagogy C13).
10. Guard lets Key text through in any message without "your answer", and lets Retry or Cold be sent at any
    time, including in the first sitting (`teaching-guard.py:51-52, 127`). Block Cold before its due date.
11. Hint scoring on the scored step for stuck moves 1 and 2 is not stated (C3); `INTEGRATED.md:67` "within
    2 attempts" conflicts with 0.5 per hint.
12. Placement not built (G15): no First step item; `code.md:165-166` contradicts `code.md:115`.
13. Not fixed from the pedagogy audit, lower stakes: self-graded recall (`SKILL.md:26-28`, T4), recall
    interleaved from day 1 (M6), close lines queued as self-graded cards (Q7), no check question before a
    step (B4), guard fails closed (B5), rungs ignored (C12).
14. Stale text: `INTEGRATED.md:15` old code steps; `code.md:95` "trace it in full"; `code.md:141, 194, 231`
    trace-cell bars and "Predict step right first try"; `code.md:217` Tue/Thu (C47); `engine.py:9` docstring
    "Trace=0.8"; `code-teaching-experts-v2.md:232` old stuck order "unchanged".
15. Checker gaps beyond M1 and M2: How block content not checked (`check_unit.py:201`), Retry may copy Your
    turn, Retry and Cold Kind not checked, "sticker" not on the watchlist, card and cold answers not checked
    against shown text (pedagogy S5).
16. `today` shows "sitting 2 of 7" on his first sitting, because the empty evaluation slot is skipped
    (`engine.py:107-115`); cosmetic, but it reads as if he missed one.

---

## What to do before code-01

1. Fix B1 (one line) and add its selftest flow.
2. Split code-01 Show 3 and trim Show 2 (M3, M4), rerun `check_unit.py` and the guard selftest.
3. Add `Two options:` and `Worked answer:` to the three tries and Your turn (M6).
4. Decide M5 before the first miss can happen (the next code sitting after a miss).

The rest can follow in order of severity.
