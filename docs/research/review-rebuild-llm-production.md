# Review of the rebuild: LLM behaviour and production

Written 2026-09-25. Independent and adversarial. Nothing was edited except this file. The builders' reports
were not used; every claim below was checked against the files, the run JSON, the saved sources, or by
running the checker, the guard and the engine.

Read in full: `docs/research/gap-audit-llm-behaviour.md` (F1 to F35), `docs/research/gap-audit-production.md`
(1.1 to 7.2), `docs/research/audit-pedagogy.md`, `docs/learning-evidence.md`, `structures/INTEGRATED.md`,
`structures/llm-behaviour.md`, `structures/production.md`, `.claude/skills/faiz-teach/SKILL.md`,
`learn/check_unit.py`, `learn/engine.py`, `hooks/teaching-guard.py`, `learn/selftest.py`, and the units
`learn/units/llm/01-it-predicts-it-does-not-look-up.md`, `learn/units/llm/02-tokens.md`,
`learn/units/production/01-what-one-call-costs.md`, plus every run file they list.

What was run: `check_unit.py` on the three units (all PASS); `selftest.py` (all attacks caught); a guard
simulation of every step, Help block, Retry and Cold of the three units, with feedback, stuck moves and a
re-send after Help (scratchpad `gsim.py`, `gsim2.py`); the engine in a temp copy through a miss and a Retry.

---

## 1. Verdict

The rebuild is real. The three things he complained about in C49 are fixed in all three units: each opens
with a goal and a worked demonstration before any question is scored, the expert explanation (Karpathy,
ScaleDojo, Hugging Face) now sits in the step bodies he reads, every pre-question is unscored and answered in
the very next message, and every number I traced matches its run or a verified `facts.md` row. All
production arithmetic is right (recomputed in section 4). The guard lets every step, Help block, Retry and
Cold through in order.

What is not ready is the path after a miss. The engine cannot record a Retry at all (blocker 1), and the
guard blocks the "go back to the step" move the production Help Keys prescribe. Two items (llm-01 Cold,
llm-02 Retry) ask for more than the unit taught. The checker still cannot see the teaching rules that failed
before; it trusts the author's own count of new ideas.

| Unit | Taught sitting (steps 1 to Close) | End to end (miss, Retry, Cold) | Verdict |
|---|---|---|---|
| llm-01 | ready; minor wording fixes | Retry unrecordable (B1); Cold item too hard (M4) | **Not ready** until B1 and M4 are fixed |
| llm-02 | ready; fix the Wrong idea fixed question 2 wording | Retry unrecordable (B1); Retry item unfair (M5) | **Not ready** until B1 and M5 are fixed |
| production-01 | ready; strongest of the three | Retry unrecordable (B1); Help Keys ask for a blocked re-send (M2) | **Not ready** until B1 and M2 are fixed |

If B1 alone is fixed, all three can be taught tomorrow; M2, M4 and M5 each only bite on a stuck path, a
Retry or the day-7 Cold, so they can be fixed before those happen.

**Counts: 1 blocker, 7 major, 22 minor (30 findings).**

---

## 2. Findings

### Blocker

**B1. A Retry can never be recorded, so the corrective loop is dead.**
- Where: `learn/engine.py:316` stores the prediction under `unit` or `unit:cold` only; the `--retry` flag
  (parsed at `:439`) is ignored. `cmd_done` then looks for `unit:retry` (`:328-332`) and exits.
- Reproduced in a temp copy: `predict llm-01 70`, `done llm-01 --step "New case=0.5"` (recorded, not
  passed), `predict llm-01 60 --retry` (stored as `llm-01`), `done llm-01 --step "Retry=1" --retry` gives
  `error: no prediction recorded for llm-01:retry`. The retry is never written, so `next_unit` returns
  "RETRY" for that unit forever (`:180-181`).
- Why it matters now: in both LLM units the only scored item is one question at a 90 bar, so any hint (0.5)
  fails the unit. SKILL.md step 5 and INTEGRATED 2.5 send every miss down this path. `selftest.py` has no
  Retry flow, which is why it passed.
- Fix: in `cmd_predict`, key `f"{a.unit}{':cold' if a.cold else ':retry' if a.retry else ''}"`; add a Retry
  flow to `selftest.py` section 3.

### Major

**M2. The guard blocks the "back to the step" move after a Help block.**
- The Help Keys in production-01 say "Then send Your turn 1's questions 2 and 3 again" (`production/01:318`),
  "Then back to Your turn 2" (`:340`), "back to Your turn 3" (`:359`), "back to Lever" (`:381`). The guard
  blocks any step already sent (`hooks/teaching-guard.py:130-131`). Simulated: every "re-send X after its
  Help" was blocked, in all three units.
- The LLM Help blocks avoid this (each ends "go back to the check you were on and answer it"), but in
  production Help: Your turn 1 asks only question 1, so questions 2 and 3 are left unasked or improvised.
- Also: stuck move 1 phrased naturally ("Look at your answer to How it works ...") is blocked, because any
  text containing "your answer" is treated as a step (`:51`, `:106-107`). Moves 1, 2 and 4 pass only if the
  tutor avoids that phrase.
- Fix: let the guard allow a re-send of the current step (index equal to the cursor) when the previous
  assistant message was that step's Help block; or rewrite each production Help block to end with the
  remaining questions of its step, and delete the "back to" lines. Add one line to SKILL.md: stuck moves
  never use the words "your answer".

**M3. LLM mastery still rests on one item in the sitting and one item cold, at a 90 bar.**
- `llm/01:5` and `llm/02:5` score only "New case"; Cold is a single item (`01:254-272`, `02:269-280`);
  the bar is 90 (`engine.py:48`, INTEGRATED.md:68). A 0.5 fails; one slip on day 7 blocks mastery.
- audit-pedagogy C4 and T1 asked for several short items and an 80 bar cold. Production fixed this (10
  items); LLM did not.
- Fix: score the three Checks as guided practice as now, but make the New case 2 or 3 short transfer items
  (the Help: New case examples show they exist), and a Cold of 3 to 5 items, bar 80.

**M4. llm-01's Cold item tests an idea that lives only in Keys and a conditional Help block.**
- `llm/01:256-272`: "Q: What is the largest city in Pakistan? A:" gives Islamabad 38.6% over Karachi 37.8%
  (checked: `runs/llm01-city-question.json`). Full marks need "text shaped like this is usually followed by
  Islamabad, because capital questions are common" (`:271-272`).
- The always-sent bodies teach that wording shape moves chances toward the answer (`01:42`). They never
  show a pattern pulling toward a wrong answer. The nearest ideas are the Checks Key (`:173`, Karachi as a
  common word) and Help: Checks (`:185`, "Pun"), neither always sent. Expected first try well under 80%, on
  the one item that decides mastery.
- Fix: add one line to Wrong idea fixed or Checks showing a wording that pulls a wrong but common piece up
  (the run already exists: Karachi 10.3% in row 2, `01:21`), or replace the Cold with a surface the body
  covers directly.

**M5. llm-02's Retry asks for evidence the unit barely provides, and scores its absence as a fail.**
- `llm/02:256-267`: he must refute "the tokenizer cuts every name longer than 6 letters" with evidence from
  the unit; the reason alone scores 0.5, which fails the Retry (bar 90).
- The always-sent bodies mostly support the teammate: "withholding" (11 letters) is cut, "strawberry" (10)
  is cut, "Google" and " salary" are 6 letters. The Key's evidence is that the piece "holding" (7 letters) is
  one token (`:266`), a subtle reading of Checks question 3. "electricity" (11 letters, one token) appears
  only in Help: Predict (`:92`).
- The Retry is also much harder than the New case it replaces (a near copy of the opening table, `:207-216`).
- Fix: put a long common word kept whole in an always-sent body (for example add " electricity" to Run and
  compare), or score the reason alone as 1 and make the evidence a bonus.

**M6. Nothing records or alarms on the first-try rate, so an overloaded unit is invisible again.**
- F9 and production 4.4: NOT FIXED. `engine.py` stores only what `done` receives and passes on scored steps
  (`:354-362`); the dashboard (`:399-428`) has no in-unit rate. The production try Keys say "record
  first-try rate" (`production/01:102`, `:156`, `:207`) and the structures set an alarm under 70%
  (`production.md:88-89`, `llm-behaviour.md:94`), but no command takes it.
- This is the one measure that would have caught C49 inside a session.
- Fix: accept `--try "<step>=<right first try>/<asked>"` in `done`, store it, and print "ALARM try steps
  under 70%" on the dashboard.

**M7. The checker cannot see the rules that failed before; it trusts the author.**
- `check_unit.py:132-139` counts the Key's own `New:` line. llm-01 How it works lists 3 items that hold 5
  ideas (`01:52`: training nudges, patterns not a list, wording changes chances, one piece at a time, nothing
  checks); production The job lists 2 while the body adds a third and fourth (tokens, per-1,000,000 prices,
  `production/01:18-24`, Key `:38`).
- Still missing (F17, F18, F26, F27, production 5.2, 5.4): a check that every scored, Retry, Cold and card
  answer rests on always-sent step bodies (M4 and M5 are exactly this); a goal line in step 1; words before
  the first question; production's 10 items with 3 or more about meaning; code-line provenance outside the
  code skill (`:214`).
- Fix: require each Score and card answer to name the step it rests on (`Rests on: <step>`), and check that
  step is not a Help block; count glossary watchlist terms per body instead of trusting `New:`; add the
  production item and meaning counts.

**M8. The files that "win" still describe the old units.**
- INTEGRATED.md:16-17 still lists LLM as "Odd result, Pick and say why, Predict, Run, Explain, Wrong idea
  fixed, New case" and production as "Guess, Chain, Run, Lever, Quick set". The note at `:21-24` says these
  are the "you do and review steps", which is false: "Pick and say why" and "Explain" no longer exist, and
  production-01 has no Guess, Chain or Run. INTEGRATED says it wins over the structures (`:6`). `:110`
  still names a "change your answer after discussion" step that does not exist.
- production.md keeps sections that contradict its corrected section 2: "a bank ... at pace ... Worked
  examples appear once per problem class" (`:48-51`); "speed and calibration are graded" (`:125`); speed
  thresholds (`:219`, `:228`, `:274`); readiness 0 to 10 (`:233`) and "milestone twice, 7 days apart"
  (`:150`); "Interleaving is the default from the first week" (`:239-240`); anchor card "1.3 tokens per word",
  "cached read 0.1x" (`:243-244`); "Estimate-first ... B-" (`:292`); "Worked examples that show every
  substitution" excluded (`:306`) while the unit shows them. It also claims the checker requires a Help block
  for every try and scored step (`:80-83`); it requires one.
- llm-behaviour.md keeps: "this one is built from wrong models made visible, then broken by a real run" as
  opposed to worked examples (`:23-25`); a 4-option ConcepTest as practice format A (`:152-158`); the
  first-vote band 35 to 70% "at step 2" (`:273`, `:33`); "Break-it units" (`:255`); "Not yet: a wrong answer
  with confidence 4 or 5 sends the concept back" (`:227`), against "confidence never demotes".
- A builder of llm-03 or production-02 reads these first. Fix: rewrite INTEGRATED 1 rows 16-17 with the
  current step names and Kinds; strike or mark "superseded" every stale section listed.

### Minor

| # | Where | Finding | Fix |
|---|---|---|---|
| m1 | `llm/01:12-25` | First LLM message: 206 words before the question (structure limit about 150), about 5 new ideas though the Key lists 3; "0.5B learned numbers" is opaque to him | Move the demo-model paragraph to Run and compare (the structure's own rule, `llm-behaviour.md:79`); say "0.5 billion adjustable numbers the model learned" or drop the size |
| m2 | `llm/01:34-48` (346 words), `llm/02:34-56` (323) | How it works is over the structure's own "about 250 words" (`llm-behaviour.md:77`); within his B8 character range | Trim the "On your rows" paragraph or the picture's break line |
| m3 | `llm/01:40` | "One piece is picked (unit 3 shows how)": llm-03 does not exist (only 01 and 02 in `learn/units/llm/`) | Drop the pointer until llm-03 is rebuilt |
| m4 | `llm/01:198`, `:209` | "asked in a chat" is never explained (runs add a system line, `llm01-multiply2-model.json`); the Score line needs two parts (likely pieces AND nothing checked) from a one-line answer | Say "asked as a question"; accept "no calculation happened" as covering both parts |
| m5 | `llm/01:14`, `:44`; all runs | The demo model is `Qwen/Qwen2.5-0.5B-Instruct` (a chat-trained model); units call it Qwen2.5-0.5B and quote "a glorified autocomplete", which Karpathy says of base models | Name the Instruct model once; keep the quote with "Karpathy says of the first-stage model" |
| m6 | `llm/02:139`, Key `:146` | "Which bill would you quote" expects "neither yet": a trick framing; he will pick one and be marked short | Ask "What would you measure before quoting, and why is one sentence not enough?" |
| m7 | `llm/02:207-223` | "One price per token whatever the language" is stated only inside a "Suppose" (`:135`) and a Help block, yet the teammate's claim is about price; the New case is a near copy of the opening table | State the fact once in Wrong idea fixed; use a different surface (for example a system prompt in Roman Urdu) |
| m8 | `llm/02:115` | The demo-model description is repeated from llm-01 (C27, F31) | Keep "the tiny demo model" only |
| m9 | `production/01:43-77` | Worked example 1 is 2,294 characters, 418 words, 9 blocks; the Python block adds a code-reading load the unit never uses again | Drop the code block and its How this code works, or move it to Worked example 2 |
| m10 | `production/01:247`, `:446`, `:471` | No rounding tolerance: is 38% right for 37.9%? Retry gives 58% (0 decimals), Cold 60.2% (1 decimal); a 9 of 10 bar makes this decisive. With his 88% arithmetic first try, P(9 or more of 10) is about 66% from slips alone | Add "shares within 0.5 point, dollars to 4 decimal places accepted" to every Score line |
| m11 | `production/01:230` vs `:246`, `:276` | "No help on this set" vs "a right answer after a hint counts half" | Delete the hint clause |
| m12 | `production/01:424-472` | Retry and Cold are 10 items in one message (his B9: about 5 per message) | Two messages of 5, as the audit's sample did; the guard allows two Cold blocks if named `Cold` and `Cold 2` (needs `is_extra` to match) |
| m13 | `engine.py:372` | Cards are added after a failed unit (C13); reproduced: all 5 llm-01 cards queued after New case = 0.5 | Add cards only when `passed` or after the Retry |
| m14 | `SKILL.md:26-27` | He still grades his own recall (production 3.3, pedagogy T4) | Tutor proposes the grade against the stored answer; number cards marked by the key |
| m15 | `teaching-guard.py:51`, `:103-105` | Key text is checked only when the message contains "your answer", so a Key can be pasted in any other message before he answers | Run the Key check on every assistant message while a unit is open |
| m16 | `teaching-guard.py:118`, `:139-140` | Feedback with a "?" before a step is blocked (pedagogy B4); a checker error blocks teaching mid-session (B5) | Allow one question in feedback; fail open with a logged warning |
| m17 | `llm-behaviour.md:88-91` | Placement lets steps 3 and 4 be skipped, but Run and compare states tested facts (paste the source: `llm/01:105`, card 3, Checks 3; letters and per-model tokenizers: `llm/02:115`, Checks 3, Cold) | Only step 3 may be skipped |
| m18 | `method-effectiveness.md:156`, `skill-methods.md:34`, `:115`, `private/research-base/learning-methods/INDEX.md:180`, `review.md:130` | F1 residue: "LLM behaviour: No worked examples" and "generate, do not show" remain in the research base | Correct as in `llm-behaviour.md:61-70` |
| m19 | `docs/glossary.md:41-43` | F19 not fixed: token, model, prompt still "taught", so never checked; training, call, chat, input, output not on the watchlist | Move them to the watchlist until a unit that teaches them is passed |
| m20 | `engine.py:133-135`, `:169-191` | Rungs and placement are computed or printed but never used; "production placement check before the first unit" is printed with no placement item (2.3, 4.3, C12) | Delete the printout until a placement item exists; select units by rung later |
| m21 | `INTEGRATED.md:68`; `learn/facts.md` | F11: the reason is still part of the fixed LLM bar, not a trial; production anchors (6.4) are not in facts.md | Mark the reason gate "trial"; add dated production anchors before C2 or C3 units |
| m22 | `engine.py:187`; `llm/01:278`, `llm/02:287` | No parallel units exist (4.6); two card variants come from Help blocks he may never see (self-contained, low risk) | Write the parallel units before the second miss can happen; take the variants from always-sent steps |

---

## 3. Status of every audit finding

FIXED, PARTLY or NOT FIXED, with the evidence.

### 3.1 gap-audit-llm-behaviour.md

| ID | Status | Evidence |
|---|---|---|
| F1 | PARTLY | Corrected in `llm-behaviour.md:61-70`, `:293`; still wrong elsewhere (m18) |
| F2 | PARTLY | `llm-behaviour.md:109` fixed; `:23-25` still sets this skill apart from worked examples (M8) |
| F3 | FIXED | Pre-question unscored, no hints (`llm/01:25`, `:32`; `llm/02:25`, `:32`); consolidated next message with a line per option (`01:36`) |
| F4 | NOT FIXED | No Crouch and Mazur file saved; band still at `llm-behaviour.md:33`, `:273` |
| F5 | FIXED | `llm-behaviour.md:74-86`; How it works in both units |
| F6 | FIXED | Tutor states the mechanism (`01:38-44`); self-explanation on the key line (`01:46`, `02:54`) |
| F7 | NOT FIXED (not yet due) | llm-03 not rebuilt; `learn/units/llm/` holds only 01 and 02 |
| F8 | FIXED | "piece" defined in `01:16`; token defined in `02:14` |
| F9 | NOT FIXED | M6 |
| F10 | PARTLY | INTEGRATED 2.3 requires a show first (`:35-42`); 2.8 still says "where a step explains something" (`:55`) |
| F11 | NOT FIXED | m21 |
| F12 | FIXED | "no hints" in both pre-question Keys |
| F13 | PARTLY | Help blocks for every try and scored step, allowed by the guard (`teaching-guard.py:127`); re-send still blocked (M2) |
| F14 | FIXED | Quotes and mechanism in bodies (`01:36-44`, `02:38-52`) |
| F15 | PARTLY | Range C1 to C49 (`SKILL.md:11`); prediction after practice (`:35-36`); confidence per step not recorded |
| F16 | FIXED | `scored: New case`; engine passes on scored steps only (`engine.py:38-45`) |
| F17 | PARTLY | Order, New cap and Help enforced (`check_unit.py:117-148`); the rest missing (M7) |
| F18 | PARTLY | Skip rule gone from units; placement text still allows skipping a step that states tested facts (m17) |
| F19 | NOT FIXED | m19 |
| F20 | FIXED | Worked demonstration is message 2 in both units |
| F21 | PARTLY | llm-02 opening is lean; llm-01 opening still heavy (m1) |
| F22 | FIXED | Goal lines `01:12`, `02:12` |
| F23 | FIXED | Predict after the mechanism, data given, reason asked (`01:57-66`, `02:65-74`) |
| F24 | FIXED | Focused self-explanation questions |
| F25 | FIXED | Answer opens the next message |
| F26 | PARTLY | New case rules are in bodies (`01:40`); llm-01 Cold is not (M4) |
| F27 | PARTLY | Cards from bodies, two variants from Help blocks (m22) |
| F28 | FIXED | Phone keyboard (`01:44`), shop till (`02:52`), each with a break line |
| F29 | FIXED | ScaleDojo and Hugging Face in `02:6`; Karpathy in `01:6`; all quotes verified word for word |
| F30 | FIXED | Direction questions as two options; why-items one line first |
| F31 | PARTLY | `given:` barred from bodies (`check_unit.py:203`); caveat repeated (m8) |
| F32 | FIXED | Priced decisions (`01:124-130`, `02:134-139`) |
| F33 | FIXED | Checks group 3 questions |
| F34 | PARTLY | Most terms defined where used; "learned numbers", "in a chat" not (m1, m4) |
| F35 | FIXED | The five old questions are gone; new parse issues are m1, m4, m6 |

### 3.2 gap-audit-production.md

| ID | Status | Evidence |
|---|---|---|
| 1.1 | FIXED | No Guess on first contact (`production.md:64-78`); rough estimate modelled (`production/01:53`) before his first guess (`:148`) |
| 1.2 | NOT FIXED | `production.md:292` |
| 1.3 | PARTLY | Worked example per knowledge point; `production.md:48-51`, `:289` still "once per class, fast fade" |
| 1.4 | FIXED | Table first, then a two-way pick (`production/01:213-220`) |
| 1.5 | FIXED | `production.md:97` |
| 1.6 | FIXED | 10 items in two halves; engine mean of two fifths |
| 1.7 | PARTLY | `production.md:76` blocks the first class; `:239-240` contradicts |
| 1.8 | FIXED | The job (`production/01:12-32`) |
| 1.9 | FIXED | Three knowledge points, each worked then tried |
| 1.10 | PARTLY | No timer (`production.md:111`); speed still graded at `:125`, `:219`, `:228` |
| 1.11 | NOT FIXED | `production.md:150`, `:233` |
| 1.12 | NOT FIXED | No outside task at P-1 |
| 1.13 | PARTLY | Substitution lines in the unit; exclusion row `:306` contradicts |
| 2.1 | PARTLY | INTEGRATED.md:17 unchanged (M8) |
| 2.2 | FIXED | INTEGRATED 2.3 |
| 2.3 | NOT FIXED | No placement rule in the shared layer (m20) |
| 2.4 | PARTLY | Kind: show names the teaching steps; INTEGRATED:55 wording unchanged |
| 3.1 | FIXED | `SKILL.md:29-36` |
| 3.2 | FIXED | Solutions inside step bodies (`production/01:252-257`, `:282-287`); guard sends them |
| 3.3 | NOT FIXED | m14 |
| 3.4 | FIXED | `SKILL.md:11` |
| 4.1 | PARTLY | Unit has 5 meaning items of 10 (`:248`, `:278`); not checked (M7) |
| 4.2 | FIXED | Cold is 10 items (`:449-472`) |
| 4.3 | NOT FIXED | m20 |
| 4.4 | NOT FIXED | M6 |
| 4.5 | FIXED | Number cards carry 4 surfaces |
| 4.6 | PARTLY | Retry item added; no parallel unit (m22); Retry unrecordable (B1) |
| 5.1 | FIXED | Kind-based order (`check_unit.py:117-131`) |
| 5.2 | PARTLY | Cap 2,600 characters, not 2,100; no before-question or question-count checks |
| 5.3 | PARTLY | How this works now any skill (`:201`); code provenance still code only (`:214`) |
| 5.4 | NOT FIXED | M7 |
| 5.5 | NOT FIXED | No shape tag or check |
| 6.1, 6.2 | NOT FIXED | `production.md:243-244` |
| 6.3 | PARTLY | Unit uses Sonnet 5 and Haiku 4.5; `production.md:157` still Sonnet 4.6 |
| 6.4 | NOT FIXED | No production anchors in `facts.md` |
| 7.1 | FIXED | The Kind rule applies to every skill |
| 7.2 | NOT FIXED | "Friday: Production, mixed set" still at `skill-methods.md:232`, `curriculum-map.md:47`, `method-effectiveness.md:170` |

### 3.3 audit-pedagogy.md (shared layer, as it touches these two skills)

| ID | Status | Evidence |
|---|---|---|
| C1, C2, M1 | FIXED | Worked steps required; pre-question unscored |
| C3 | FIXED | Hinted = 0.5 (`SKILL.md:38`), minor clash in production (m11) |
| C4, T1 | PARTLY | Production 10 items; LLM still one item at 90 (M3) |
| C5 | FIXED | Answer line by line on request (`SKILL.md:53-54`); guard does not cap it |
| C6 | PARTLY | One stuck order (INTEGRATED 2.4 = SKILL 55-58); re-send blocked (M2) |
| C7 | PARTLY | Show steps carry pictures and worked parts; no checker check of the template |
| C8 | FIXED | Production set of 10 |
| C11, T2 | PARTLY | Help blocks and Retry exist; the Retry cannot be recorded (B1); no parallel units |
| C12 | NOT FIXED | m20 |
| C13 | NOT FIXED | m13, reproduced |
| C14 | FIXED | One unit per sitting in weeks 1 and 2 (`engine.py:258-259`) |
| C15 | PARTLY | 2,600 characters |
| C16 | FIXED | INTEGRATED 2.9, SKILL.md:76-78 |
| S5, Q3 | FIXED | Digit row and untaught Cold facts gone from llm-02 |
| T3 | FIXED | Prediction after practice; confidence never demotes (`engine.py:149`) |
| T4 | NOT FIXED | m14 |
| T5 | NOT FIXED | Pass still gates on the in-session item |
| B1, B2, B6 | FIXED | Stuck order teaches; prepared Help blocks; worked scripts |
| B4, B5 | NOT FIXED | m16 |

---

## 4. Correctness

**Runs.** Every model output and token count in the three units was traced to its JSON in `learn/runs/`:
llm-01 (capital 21.9 / 8.1 / 6.0 / 5.6 / 5.5; 81.9 / 10.3 / 1.6 / 0.7 / 0.7; friend 45.0 / 12.5 / 7.8 / 5.1 /
1.8; currency 24.4 / 20.7 / 17.9 and 63.5; Canberra 10.4 and 96.9, blank 20.5; language 38.8 / 23.6 / 7.6,
blank 16.7; city 21.2 / 8.8 / 8.6 / 5.7 / 5.4 and 38.6 / 37.8 / 16.0 / 1.3 / 1.2; 683 x 47 answered 32519,
true 32101; 347 x 29 answered 9503, true 10063; the novel answer "Jhumpa Lahiri") and llm-02 (10 / 15 / 16
tokens; ` تن` `خوا` `ہ`; ٹیکس as 2; Qwen 27; `str` `aw` `berry` and answer 2; "hewtning"; `with` `holding`;
JazzCash 2 and 3; 10 / 16 and 10 / 33; 8 / 15 and 8 / 24; Google 1, Easypaisa 4 pieces as listed; Islamabad
`Islam` `abad`, answer 2). All match. Word counts of the Urdu and English sentences are right.

**Quotes.** Checked word for word in the saved sources: Karpathy "something you read a month ago", "gives
you the answer for the probabilities of what comes next", "a glorified autocomplete", "it always works
better if you just give it to them", "the models don't see characters they see tokens", "now get it
correct"; ScaleDojo "repeatedly finds the most frequent adjacent pair ... into a single new piece" and its
five-word run (l+o, lo+w, e+r match the source's first three merges); Hugging Face "frequently used words
... meaningful subwords." All exact. One context issue: m5.

**Prices.** Sonnet 5 $2 / $10 and Haiku 4.5 $1 / $5 per million, verified rows `facts.md:21`, `:23`.

**Production arithmetic, recomputed.** Every figure is right:
- Worked example 1: 6,500 x 2 / 1e6 = 0.013; 400 x 10 / 1e6 = 0.004; call 0.017; rough 0.014 + 0.004 =
  0.018 (about 0.02); wrong turn 6,900 x 2 / 1e6 = 0.0138; 6,000 / 400 = 15. Code prints 0.017.
- Your turn 1: 0.003, 0.0094; 3,500 x 2 / 1e6 = 0.007, too low.
- Worked example 2: 600 calls, $10.20, $10,200; shares 70.6%, 23.5%, 5.9% (sum 100.0).
- Your turn 2: about $3; $2.82; 63.8%.
- Worked example 3: (a) 3,500 x 2 / 1e6 + 0.004 = 0.011, saving 0.006, x 600 = 3.60; (b) 0.015, saving
  0.002, 1.20; ratio 3.
- Your turn 3: 1,700 x 2 / 1e6 + 0.003 = 0.0064; saving 0.003. Lever: 0.90; cap 150 gives 0.0079, saving
  0.0015, 0.45.
- Quick set: 0.0132; 450 calls, 5.94; 37.9%; 0.0025; Haiku 0.0066; 0.0215; 0.01 vs 0.00075; input 93.0%;
  lower; 11,880.
- Retry: 0.0069; 360 calls, 2.484; 745.20; 57.97% (Key 58%); 0.0049, saving 0.002; Haiku 0.00345; cap
  saving 0.00125; higher; 24.84 a day.
- Cold: 0.0166; 240 calls, 3.984; 1,992; 60.2%; 0.0116, saving 0.005; Haiku 0.0083; higher; cap saving 0.003;
  66.40 a day.
- Help blocks and all 16 card surfaces: all right.

**Keys and Score lines.** Every Key answer is right. Score lines are markable except where noted: llm-01 New
case two-part wording (m4), production rounding (m10), llm-02 Wrong idea fixed question 2 framing (m6).

---

## 5. Each unit as he receives it

One row per message; step bodies only, in order. "New" counts ideas he has not met before.

### llm-01

| # | Message | New | Answerable from what was shown? | Likely first try | Notes |
|---|---|---|---|---|---|
| 1 | Goal and odd result | 4 to 5 | yes: two options, the rows make (b) obvious | about 85% | m1: 206 words before the question; "learned numbers" |
| 2 | How it works | 5 (Key says 3) | yes: point at the Q and A shape | about 90% | Karpathy explains before any test; m2, m3 |
| 3 | Predict | 0 | yes, all data given | about 70% (try) | fine; Help: Predict is a clean worked prediction |
| 4 | Run and compare | 1 (paste the source) | yes | about 90% | "prompt" defined in the sentence |
| 5 | Wrong idea fixed | 0 | yes; asks before minus after explicitly (E11) | about 85% | decision priced, not a read-back |
| 6 | Checks (3) | 0 | yes | about 80% | good spread: direction, why, fix |
| 7 | New case (scored) | 0 | yes: "one piece at a time, nothing checks" is in message 2 | about 80% | m4 |
| 8 | Close | 0 | yes | n/a | |
| Retry | | 0 | mostly: "no list, so nothing comes back not found" is inferable | about 70% | |
| Cold | | 0 | no, see M4 | about 55% | M4 |

Sentences he may not parse: "0.5B is its size: 0.5B learned numbers, B = billions" (`01:14`); "One piece is
picked (unit 3 shows how)" (`01:40`, a unit he will not get); "asked in a chat" (`01:198`).

### llm-02

| # | Message | New | Answerable? | Likely first try | Notes |
|---|---|---|---|---|---|
| 1 | Goal and odd result | 2 | yes, from the numbers | about 95% | clean |
| 2 | How it works | 4 (Key says 3) | yes | about 85% | "merges", "subwords", "decomposed" inside quotes; adjacent and corpus defined; m2 |
| 3 | Predict | 0 | yes | about 75% (try) | Help: Predict is well matched |
| 4 | Run and compare | 2 | yes | about 85% | m8 repetition |
| 5 | Wrong idea fixed | 1 (Qwen 27) | question 1 yes; question 2 is a trick | about 60% on question 2 | m6 |
| 6 | Checks (3) | 0 | question 2 needs "each list from its own pile", only implied | about 70% | |
| 7 | New case (scored) | 0 | yes | about 85% | near copy of message 1 (m7) |
| 8 | Close | 0 | yes | n/a | |
| Retry | | 0 | evidence part barely supported | about 45% full marks | M5 |
| Cold | | 0 | yes | about 85% | |

### production-01

| # | Message | New | Answerable? | Likely first try | Notes |
|---|---|---|---|---|---|
| 1 | The job | 3 to 4 (Key says 2) | yes | about 95% | goal and "done when" present |
| 2 | Worked example 1 | 3 plus Python | yes | about 90% | m9: longest message in the three units |
| 3 | Your turn 1 | 0 | yes, completion with the first link done | about 85% | Help: Your turn 1 ends on question 1 only (M2) |
| 4 | Worked example 2 | 3 | yes | about 90% | |
| 5 | Your turn 2 | 0 | yes; his first rough guess, after a modelled one | about 85% | |
| 6 | Worked example 3 | 3 | yes | about 85% | E11 and E12 taught head on, one-side slip labelled wrong |
| 7 | Your turn 3 | 0 | yes | about 80% | direction as two options (E12) |
| 8 | Lever | 0 | yes, table first | about 85% | |
| 9 | Quick set 1 (scored, 5) | 0 | yes, every rule was worked | about 85% per item | m10, m11 |
| 10 | Quick set 2 (solutions 1 to 5, then 5) | 0 | yes | about 85% per item | |
| 11 | Close (solutions 6 to 10, then close line) | 0 | yes | n/a | |

Nothing in production-01 tests a rule it did not show. Every term is defined where it first appears
("fixed instructions", "input", "output", "share", "lever", "summariser", "Haiku 4.5").

---

## 6. Guard results (synthetic transcripts, as `selftest.py` does)

| Message | llm-01 | llm-02 | production-01 |
|---|---|---|---|
| Each step in order, with short feedback before it | allowed | allowed | allowed |
| Each Help block, any time | allowed | allowed | allowed |
| Retry alone, or after a short line | allowed | allowed | allowed |
| Cold alone | allowed | allowed | allowed |
| Re-send the step after its Help block | **blocked** | **blocked** | **blocked** (the Keys ask for it: M2) |
| Stuck move 1 without "your answer" | allowed | allowed | allowed |
| Stuck move 1 with "Look at your answer to ..." | **blocked** | **blocked** | **blocked** |
| Stuck move 2, two options from the Score line, no ask marker | allowed | allowed | allowed |
| Stuck move 4, answer line by line then "say it back" | allowed | allowed | allowed |
| Feedback containing "?" before the next step | blocked | blocked | blocked (m16) |
| A Key line pasted in a message without "your answer" | **allowed** (m15) | | |

So the stuck order works only if the tutor never says "your answer" and never re-sends a step.

---

## 7. Cohesion

- **Step names and Kinds.** `llm-behaviour.md:74-86`, the two LLM units and the checker agree (show, show,
  try, show, try, try, scored, close; Help on every try and scored step; Retry and Cold scored).
  `production.md:64-86`, production-01 and the checker agree. INTEGRATED.md:16-17 does not (M8).
- **Bars.** INTEGRATED 3, SKILL.md:40-41 and `engine.py:48` agree (90 / 90 / 90). The engine's production
  mean of two fifths equals 9 of 10. LLM cold is one item (M3).
- **Stuck order.** INTEGRATED 2.4, SKILL.md:55-58, `llm-behaviour.md:96` and `production.md:112` say the same
  four moves; the guard blocks two natural forms of them (M2).
- **Retry.** SKILL.md:42-44 and INTEGRATED 2.5 describe it; the engine cannot record it (B1).
- **Recall.** SKILL.md:27-28 and `engine.py:308` send a lapsed card to "its unit's wrong-idea step";
  production units have no such step. Minor wording; point to the unit's Help blocks instead.
- **Prediction.** SKILL.md:35-36 asks for it just before the first scored step; the guard forbids a "?" in
  feedback before a step, so it must be its own message before the scored step. Workable; say so in SKILL.md.

---

## 8. Fix order

1. B1 (one line in `engine.py:316`, plus a Retry flow in `selftest.py`).
2. M2 (guard re-send after Help, or self-contained production Help blocks; the "your answer" phrasing note).
3. M4 and M5 (llm-01 Cold, llm-02 Retry), before day 7 and before any miss.
4. M3 and M6 (more LLM scored items, first-try recording and alarm).
5. M7 and M8 (checker rests-on rule; rewrite the stale rows and sections), before llm-03 or production-02 is
   built.
6. The minor table, in any order; m10 and m1 first because they touch his first sittings.
