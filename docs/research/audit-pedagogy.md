# Pedagogy audit: the v2 curriculum against expert teaching practice

Written 2026-09-25, after Faiz's first v2 session (code-01, voided, C49). Adversarial and independent. Nothing
was edited except this file. Read in full: `docs/learning-evidence.md` (C1 to C49, ledger),
`docs/research/structures/INTEGRATED.md`, the five structures and `review.md`, `postmortem.md`,
`recommended-method.md`, `.claude/skills/faiz-teach/SKILL.md`, `learn/engine.py`, `learn/check_unit.py`,
`hooks/teaching-guard.py`, and all 8 units (`learn/units/code/01-04`, `learn/units/llm/01-04`), read step by
step as he would receive them.

Earlier audits (`audit-units.md`, `audit-system.md`) checked facts, numbers and machinery. None checked the
teaching itself. That is the gap this file covers.

---

## Executive verdict

**No. As built, the design is not fit to teach him.** His three complaints after the first session are
accurate and they are not delivery slips. They are built into the spec, the rulebook, the engine and the
checker:

1. **"You didn't show me a worked example."** Correct. The worked example, which `recommended-method.md`
   (line 46) and `postmortem.md` (line 158) made the backbone and which he asked for in C45, was dropped on the
   way to `code.md` and `INTEGRATED.md`. No code unit and no LLM unit contains one. The code "Trace" step
   calls its code a worked example, but he does all the working: a 35-cell table on a pattern he has never
   seen traced. `llm-behaviour.md` line 93 says outright: "No worked example ... commits ... before any
   teaching".
2. **"You're overloading me immediately."** Correct. Every code unit opens with a scored test, before any
   teaching. The first trace carries about ten new things at once (his record: about 8 new things got 0
   answers, twice, B5). The first sitting schedules two brand-new unit formats back to back (code and LLM),
   plus recall, plus a score prediction.
3. **"You didn't explain the code."** Mostly correct. Each block has a "How this code works" paragraph, but
   it is a prose summary of what the code does, not a model of how to read it. The tracing method and the
   five-field debug card are used before they are ever taught, although the very studies cited for them
   (Xie et al. 2018; Michaeli and Romeike 2019) taught the strategy explicitly first.

Behind these sits one structural fault. The system is an excellent **assessment and scheduling machine** with
the **teaching phases removed**. Rosenshine's sequence is: review, present new material in small steps,
model, guided practice with checks for understanding at about 80% success, then independent practice
(Rosenshine 2012, American Educator). Here, "I do" is absent, "we do" is absent, and "you do" is scored from
the first minute. Then the rules make recovery hard: an answer after any hint scores 0, the code and LLM
pass rules are all-or-nothing on one or two items, a failed unit is "never served again" and no parallel
unit exists, and the stuck order forbids re-explaining. That combination is the opposite of mastery
learning, which Bloom and Guskey define by its corrective loop, not by its bar.

The builder's work is not worthless. The provenance machinery (every number from a run, every code line
from a real program, the checker, labels defined in every Predict step, targeted E1 to E4 bugs, card
variants, the 7-day cold item) is genuinely good and should stay. What must change is what happens between
"here is new material" and "now you are scored".

**Counts: 9 blockers, 25 major, 17 minor (51 findings).**

---

## Expert standards used (each finding cites one or more)

| Code | Source | The part that matters here |
|---|---|---|
| ROS | Rosenshine 2012, *Principles of Instruction*, American Educator (https://www.aft.org/sites/default/files/Rosenshine.pdf) | present new material in small steps; provide models and worked examples; guide practice; check for understanding; aim for about 80% success in guided practice; independent practice only after |
| CLT | Sweller; Kalyuga (expertise reversal); Chen, Kalyuga and Sweller 2015, J. Ed. Psych 107(3) (https://eric.ed.gov/?id=EJ1071512) | worked examples beat problem solving for novices on high element-interactivity material; "answer first" (generation effect) helps only on low element-interactivity material; guidance fades as expertise grows |
| REN | Renkl and Atkinson (fading, self-explanation prompts) | example, then completion with the last steps blank (backward fading), with a prompt to explain a step |
| MAY | Mayer (segmenting, pretraining, coherence) | learner-paced segments; teach the names and parts of key concepts before the process; cut extra material |
| KAP | Kapur; Sinha and Kapur 2021, Review of Educational Research 91(5) (https://journals.sagepub.com/doi/10.3102/00346543211019105) | problem solving before instruction helps conceptual understanding and transfer (d = 0.36), stronger with high fidelity; boundary conditions include prior knowledge, scaffolded generation and expert **consolidation afterwards**; not a method for building procedural fluency from zero |
| DRB | Dunlosky et al. 2013; Roediger and Karpicke; Bjork; Rohrer (interleaving); Dunlosky and Rawson 2012 (overconfidence in self-scoring) | retrieval and spacing: strong; interleaving helps discriminate between types already learned; learners who grade their own recall over-credit partial answers |
| BG | Bloom 1968; Guskey 2005, 2010 (https://tguskey.com/wp-content/uploads/Mastery-Learning-3-Lessons-of-Mastery-Learning.pdf) | the feedback, corrective and enrichment cycle is what gives mastery learning its power; correctives must teach the idea **differently** from the first time, then a parallel second check |
| FB | Hattie and Timperley 2007; Wiliam (embedded formative assessment) | feedback must reduce the gap: where am I going, how am I going, where next; process-level feedback beats bare right or wrong |
| DI | Engelmann and Carnine, Theory of Instruction ("faultless communication") | examples must admit only one interpretation; every rule used in a test was taught first |
| KA | Khan Academy; Brilliant | explanation or worked example available on every item ("get help", step-by-step solution); many short items per skill; a wrong or hinted item lowers mastery credit but the learner simply gets more items |
| ICAP | Chi and Wylie 2014 | interactive and constructive activities beat passive, but only when the learner has something to construct from |
| CT | Anderson, Corbett, Koedinger, Pelletier 1995 (cognitive tutors); VanLehn 2011 | step-level feedback and hints (d about 0.76, close to human tutors at 0.79), bottom-out hint that shows the step; answer-level feedback only is far weaker |
| AT | Graesser, AutoTutor | expectation and misconception dialogue: pump, hint, prompt, then **assertion** (the tutor says it) and a summary |
| BAS | Bastani et al. 2024/2025, PNAS (https://www.pnas.org/doi/10.1073/pnas.2422633122) | unguarded GPT-4 help cut later exam scores (17% in the base arm); a tutor with teacher-written hints and solutions and no answer-dumping removed most of the harm. The lesson is "structured help", not "no help" |
| PRIMM | Sentance et al. | Predict is a low-stakes discussion prompt after code is shown, not a scored test |
| MAZ | Crouch and Mazur 2001 | ConcepTests follow pre-class reading and a short presentation; the 35 to 70% first-vote band assumes that teaching came first, plus peer discussion |

---

## 1. Cohesion: do the documents, rules and code agree?

They do not. Where INTEGRATED says it "wins", the engine and checker implement a third version.

| # | Sev | Where | Contradiction | Expert standard | Fix |
|---|---|---|---|---|---|
| C1 | **blocker** | `recommended-method.md:46` (step 4 worked example), `postmortem.md:158`, C45; vs `code.md:74-77`, `INTEGRATED.md:15`, `check_unit.py:26-27` | The research answer makes worked examples the backbone for novices on applied skills. The structures, the spec and the checker's step lists contain no worked-example step for code or LLM. The checker cannot fail a unit for missing one, so every unit omits it. | CLT, ROS, REN | Add a required first teaching step per skill (`Worked example`) to `STEPS` in `check_unit.py`, and to INTEGRATED section 1. |
| C2 | **blocker** | `llm-behaviour.md:33, 256` (target 35 to 70% right on the first vote) vs `engine.py:43-44` and `BAR["llm"] = 100` (line 54) | The structure plans for him to get the first vote wrong 30 to 65% of the time. The engine fails the whole unit if that first vote is wrong. Expected pass rate per unit is roughly half. The structure's own mastery rule (`llm-behaviour.md:207`: transfer right twice on two surfaces) is not what the engine checks. | MAZ, BG | Pass rule = New case plus Cold, each right with a right reason. Pick and say why becomes an unscored diagnostic. |
| C3 | major | `SKILL.md:35-36` (right after a hint = 0), `SKILL.md:51` (wrong: one reframe, one hint), unit Score lines ("within 2 attempts", "within 2 hypotheses"), `code.md:78` ("reference edit after 2 hints") | Every second attempt comes after a hint by the rulebook's own feedback rule, so it scores 0, yet the units allow 2 attempts. Whether a "Simpler" block (stuck move 0) counts as a hint is not defined. Different tutors will score the same session differently. | FB, CT | One rule: first-try credit 1, after one hint 0.5, after the answer is shown 0; the attempt count follows from it. State whether Simpler is a hint (it should not be: it is re-teaching). |
| C4 | major | `code.md:164` (cold at 7 days: 80%) vs `INTEGRATED.md:34-35` ("same bar cold") vs `engine.py:351` (cold passes only at `BAR`) | Code cold items have 3 parts, so 90% means 3 of 3; LLM cold means 1 of 1. The structure said 80%. | BG (a parallel second check, not a harsher one) | Cold bar 80% for all skills, and at least 5 cold items so the bar is not one slip. |
| C5 | major | C19, C23 ("give me the actual answer explaining each line") vs `SKILL.md:52-53` (answer "with a one-line reason") and `teaching-guard.py:120-121` (feedback before a step capped at 400 characters) | His standing rule asks for a line-by-line explanation. The rulebook and guard cap it at one line and 400 characters. | AT (assertion plus summary), FB | Answer given = the prepared worked answer, line by line, in its own message; no cap on a requested explanation. |
| C6 | major | Every unit's `Simpler:` block ("then the step's question again") vs `teaching-guard.py:131-132` ("steps go forward only"); `INTEGRATED.md:32-33` has no step 0 | The prepared fallback tells the tutor to re-ask the step; the guard blocks re-sending it. The stuck order differs across INTEGRATED (4 moves), SKILL (5, with Simpler), `code.md:89-90` (3, no picture). | ROS (re-teach, then re-check) | One stuck order, written once, and the guard allows re-sending the current step after a corrective. |
| C7 | major | `INTEGRATED.md:41-42` ("the part template where a step explains something") vs all 8 units | The template he scored 80% on (A12: problem, tiny generic example, everyday picture, paths spelled out) is required by the spec but used by no unit, and not checked. Code units go straight to real code (A13 pattern: 27%). | B1 to B4 in his own record; MAY | Checker requires the template blocks in every teaching step. |
| C8 | major | `production.md:66` (timed set = 3 items) vs `INTEGRATED.md:52` and `engine.py:46` ("9 of 10") | A 3-item set cannot be scored as 9 of 10; the effective bar is 3 of 3. The first-time worked solution (`production.md:69`) is not in the checker's production steps (`check_unit.py:28`). | BG, CLT | 10-item quick set, or bar 80% on 5; add the first-time worked-solution step to the checker. |
| C9 | major | `INTEGRATED.md:53`, `engine.py:48` (kappa 0.70, **no** missed failure, 24+ traces) vs `evaluation.md:121` (novice: kappa 0.60, fail recall 0.75), `evaluation.md:48` (human raters often kappa 0.2 to 0.3), unit size 6 + 12 = 18 traces, `learning-evidence.md:218` (kappa not yet taught) | The bar is harsher than the structure's own novice bar, needs more traces than a unit holds, and uses a statistic he has not been taught. First-time worked example (`evaluation.md:83`) is not in the checker's steps. | BG, DI | Use the structure's level bars; teach kappa with a worked example before first use. |
| C10 | minor | `code.md:74-80` (7 steps: Warm reps, Predict, Trace, Explain, Change, Break, Steer; placement test at 85-87) vs INTEGRATED (5) vs checker (6, "Tell the AI" optional to level 2) | Three step lists for one skill; the placement test that decided whether he needs the example (`recommended-method.md:44-45`) was lost. | CLT (expertise reversal needs a placement check) | One list; restore the first-step placement test. |
| C11 | major | `SKILL.md:44-45`, `engine.py:181-186` | A missed unit is never served again; its parallel unit must be written; none exist. One miss stops that skill. No corrective step exists anywhere. | BG | See T2. |
| C12 | minor | `engine.py:150-171` computes a rung; `next_unit` (174-190) ignores it | Level up and down has no effect on what he is taught. Fading "by level" (`system-design.md` 3b) cannot happen. | CLT | Select units and fading by rung, or delete rungs. |
| C13 | minor | `engine.py:359` adds a unit's cards even when he failed it; `llm-behaviour.md:215` ("no card before the concept is understood") and the Keep step (`llm-behaviour.md:73`) are not implemented | Failed content goes into spaced recall as if learned. | DRB (retrieval of what was never encoded is guessing) | Add cards only on pass, or after the corrective. |
| C14 | major | `INTEGRATED.md:56-67` ("no more than about one new thing at a time") vs `engine.py:127-129` (sitting 2 = code + LLM) | His very first sitting is two brand-new unit formats (6 + 8 steps), recall and two score predictions. | ROS (small steps), MAY (segmenting) | One unit per sitting for the first two weeks. |
| C15 | minor | `check_unit.py:162-163` (2,500 characters of prose per step) vs B8 (700 to 2,100 best) | Trace steps run 2,446 to 3,059 characters plus a table. | B8 | Cap at 2,000 including code, or split. |
| C16 | minor | `SKILL.md:11` ("his latest words win") vs `SKILL.md:73-78`, `INTEGRATED.md:43-44` (format frozen 8 weeks) | The freeze would have locked in a design that failed on day 1; C49 had to override it. | FB (the teacher adjusts on evidence) | Freeze numbers and bars, not the presence of teaching steps; allow a change when a session fails. |

---

## 2. Sequencing: taught and modelled before asked?

| # | Sev | Where | Finding | Expert standard | Fix |
|---|---|---|---|---|---|
| S1 | **blocker** | Step 1 of every code unit: `code-01.md:11-46`, `code-02.md:11-38`, `code-03.md:11-47`, `code-04.md:11-54`; `code.md:75` | Every code unit opens with a **scored** Predict before any teaching. code-02's opener is the E2 trap (start line inside a loop), which he missed 4 of 5 times first try (E2): expected first-question success about 20%, not 80%. code-01's opener mixes a nested dict, a function, arithmetic on floats, KeyError and three labels. | ROS (about 80% success; model first), PRIMM (Predict is unscored) | Predict becomes an unscored warm-up after the worked example, on the pattern just modelled. First question of any session should be one he gets right 80% of the time. |
| S2 | **blocker** | `code-01.md:82-90` (35 cells), `code-02.md:86-94` (35), `code-03.md:92-100` (28), `code-04.md:93-99` (15); `code.md:40-42` | The trace-table method is never demonstrated. He is asked to fill a full memory table the first time he sees one, scored at 90% of cells. Xie et al. 2018 and Nelson (PLTutor), both cited, **taught** the tracing strategy explicitly before practice. | ROS (model), CLT (worked example), REN (completion before full problem) | Unit starts with the tutor's filled table for the example, one row at a time with the reason for each cell, then a half-filled table (backward fading), then his own table on a new input. |
| S3 | **blocker** | `code-01.md:169-177` (and every Find the bug); `code.md:46` | The five-field debug card (symptom, suspect lines, hypothesis, check, fix) is handed to him cold in unit 1 and scored. Michaeli and Romeike's d = 0.69 came from a 10-minute explicit lesson on the process first. | ROS, CLT | One modelled debug: the tutor fills the card for a bug, thinking aloud; then a card with the first 3 fields filled; then his own. |
| S4 | major | Every unit | There is no guided practice ("we do") anywhere: every step after the opener is either scored or a commit. Acquisition and assessment are merged. His best formats (A9 bootcamp 78%, A12 80%) were short taught parts with practice questions, not scored tests. | ROS (guided practice with checks, then independent), CT (step-level help during practice) | Insert an unscored guided-practice step with step-level feedback between the example and the scored step. |
| S5 | major | code-04 Trace Key line 118 ("`row` still holds R3 at (c), left over from the first loop"); code-03 Trace (note strings never shown); `llm-02.md:95` (digit rule only in Wrong idea fixed, which the skip rule at line 45 lets him skip, then Cold line 146 tests it); cards built from Key text: `llm-01.md:156` (retrieval), `llm-02.md:160` (Sonnet 5, 30% more tokens) | Rules and facts tested that were never stated to him (his E7, 6+ cases before v2). Key text is never shown to him, yet cards and cold items rely on it. | DI | Checker rule: every card answer and cold answer must be derivable from step bodies he is shown; skip rules may not skip the only step that states a tested rule. |

(The LLM "commit before teaching" sequence is covered under M1.)

---

## 3. Explanations: plain words, worked example, controlled load?

| # | Sev | Where | Finding | Expert standard | Fix |
|---|---|---|---|---|---|
| X1 | major | Every "How this code works" block (e.g. `code-01.md:26, 76-80`) | It is a paragraph saying what the code does, in order. It does not show the reading: no line-by-line walk with the value each line produces, no "why this line and not that", no self-explanation prompt. It satisfies C48's letter (checker line 164 only checks the heading exists), not its intent ("explain the code"). | CLT (worked example shows the process), REN (self-explanation prompt), C9, C20 | Each teaching step shows the code with a line-by-line walk (value after each line), one reason per line, then one "why is line X there?" prompt with its answer shown after. |
| X2 | major | `code-01.md:52-80` Trace; `code-02.md:44-84` Trace | Element interactivity is not controlled. code-01 Trace introduces about ten things at once: `time.time()`, `time.sleep`, a symbolic clock value T, `round(x, -2)` with a negative digit count, a reply dict with three keys, `cost_of` called inside `call`, a list passed into a function and changed there (aliasing, a classic novice wall), `return` vs what goes in the log, the subgoal comments, the (a) to (e) marker convention and the trace-table convention. code-02 adds `pop(0)`, `raise`, errors crossing a function boundary, `try/except ... as err`, `str(err)`, `return` inside a loop and a record after the loop. His record: about 8 new things at once gave 0 answers, twice (A11, B5). | CLT, MAY (segmenting and pretraining) | At most 2 new things per step. Split code-01 into "a record in a log" and "timing a call"; teach `pop` and `raise` in their own tiny examples first. Add a `new:` header per step and have the checker cap it (the old lesson checker did this). |
| X3 | major | All code units | His three strongest measured predictors (B1 tiny generic example of 8 lines or fewer before real code, B2 one everyday picture, B3 every path spelled out) are absent. Code units go straight to lesson-shaped code; no picture appears in any code unit. | His own data (A12 80% vs A13 27% on the same day), MAY | Every new idea gets a tiny generic example and one picture before the real code. |
| X4 | minor | `code-01.md:52-74` (uses `time` with no `import time` shown); `code-04.md:168-179` (`PAUSES` and `fake_provider` not shown, symptom depends on them); "as in unit 1", "like `fetch` in unit 2" | Small gaps a novice falls into. | DI | Show every name the question depends on. |
| X5 | minor | `llm-01.md:12-18` (and the same opener in llm-02 to 04) | The first LLM message packs parameters, tokens, a probability for every next piece, raw text vs chat, and a small-model caveat into one paragraph before a probability table. | MAY (pretraining: names and parts first) | A 3-line "the words you need" block before the table, one idea each. |
| X6 | minor | "What it costs" in `llm-01.md:94-97`, `llm-03.md:95-97` | Trivial arithmetic (1,000 / 5) attached to a concept step adds a task without adding understanding; he flagged read-back questions before (C36). | MAY (coherence) | Keep the cost step only where the number changes a decision. |

---

## 4. Questions: clear, answerable, right type?

| # | Sev | Where | Finding | Expert standard | Fix |
|---|---|---|---|---|---|
| Q1 | **blocker** | `code-03.md:88-100` with Key 110-118 | The `note` column needs the exact note text (for example `'Invoice scan-000, total PKR 80,000.'`), but `summarise` is never shown and the notes never appear in the step. 3 of 28 cells are unanswerable, so the best possible score is 25 / 28 = 89%, below the 90% bar. **code-03 cannot be passed as written.** The checker passed it. | DI | Show the three notes, or drop the column. Add a checker test: every Key cell value must appear in, or be computable from, the step body. |
| Q2 | major | `code-03.md:22, 42` (`print(log[1])` labelled "fine") and every crash / quietly wrong / fine item | "Quietly wrong" only has meaning against an intended result. Line 2 of code-03's Predict states no intent, so "fine" and "quietly wrong" are both defensible. His E1 errors (11 cases) are partly this ambiguity. | DI | Every labelled line carries its aim in a comment ("# aim: the second record"). |
| Q3 | major | `llm-02.md:38` (right answer D: a fixed list built from lots of text) vs `llm-02.md:152` (Cold Key: numbers "follow a fixed rule", the rarity idea "is right for words but not for numbers") | The Pick table's row 2 ("1234567") is explained by a digit rule, not by D. The unit rewards an answer its own cold item later calls wrong for numbers. | DI (faultless communication) | Remove the digit row from the Pick table, or make the right option name both mechanisms. |
| Q4 | major | All Trace tables | Tables are padded: `prompt` and `model` never change in code-01 (10 cells), `start` holds a symbol, and a single formatting habit (quotes, `0.0` vs `0`) can cost 4 cells and fail the 90% bar. A 35-cell table in one reply also breaks his 5-question message size (B9). | CLT (extraneous load), B9 | Tables of 8 to 12 cells, only the names that change; mark on value, not formatting. |
| Q5 | minor | Every "Pick and say why" and "New case" | Three demands per question (letter, one-line reason in specific terms, confidence 1 to 5), scored 0 unless the reason matches the Key's wording. | FB (score what was taught) | Accept any reason that names the mechanism; take confidence as a single tap after the answer. |
| Q6 | minor | `llm-04.md:127-140` | The right answer (A: the app stores notes and sends them) uses a memory-feature idea never shown in the unit. | DI | Show one line about app memory features in Wrong idea fixed. |
| Q7 | minor | Close steps ("Next time I see a machine called with several slots, I will ...") | Abstract sentence-completion prompts with an expected wording; fine as reflection, but they go into the recall queue as cards he graded himself. | DRB | Keep, but do not queue them as scored cards. |

---

## 5. Testing and scoring

| # | Sev | Where | Finding | Expert standard | Fix |
|---|---|---|---|---|---|
| T1 | **blocker** | `engine.py:41-44` (code pass = one Trace at 90% **and** one binary Change; LLM pass = 2 of 2), `SKILL.md:35-36` (answer after hint = 0), `SKILL.md:44-45` (failed unit never served again) | Mastery is decided by one or two items, in the same sitting he first meets the material, with no partial credit after help, and a miss ends that unit for good. One confusing cell or one hint fails the unit. This is punitive and statistically noisy. Khan Academy and ASSISTments also withhold mastery credit when a hint is used, but they give many short items, so one hinted item costs little, and a worked solution is one click away on every item. | BG, KA, ROS (80% success during practice) | Mastery on several short items (for example 3 small traces, bar 80%), after teaching and guided practice; hinted items count 0.5; a miss triggers a corrective, not an end. |
| T2 | major | Whole design; `engine.py:174-190` | There is **no corrective instruction**. The only response to a miss is a "parallel unit (new surface)", which is a re-test, and none exist. Guskey is explicit: correctives must present the idea differently (new example, new explanation, a different format), then a parallel formative check. | BG | For every unit, prepare: a corrective (a second worked example on a new surface, taught differently), then a parallel item, run in the same or next sitting. |
| T3 | major | `SKILL.md:29-31` (predict a 0 to 100 unit score before the first scored step); `engine.py:154` (a confident wrong answer counts as "below the floor"); `engine.py:325-327` (unit cannot be recorded without the prediction) | For code units the first scored step is step 1, so he must predict his score before seeing any material: a guess, not a calibration measure. Calibration research asks for judgments after study or per item. Counting confident errors toward demotion teaches him to report low confidence. | DRB (judgments of learning are meaningful after study), FB | Ask for a prediction after the worked example and guided practice, before the scored step; record confidence for diagnosis only, never for demotion. |
| T4 | minor | `SKILL.md:26-28` (he grades his own recall 1 to 4, no rubric) | Learners grading their own free recall over-credit partial answers (Dunlosky and Rawson 2012), which makes FSRS space them too far. | DRB | Tutor compares to the card answer and proposes the grade; he can object. |
| T5 | major | In-session scores feed pass, rung and dashboard (`engine.py:349-351, 396`) | Scores taken during first exposure measure performance during acquisition, which is known to be a poor proxy for learning (Soderstrom and Bjork 2015). The design's own early-warning rule warns about exactly this, then gates on it anyway. | DRB | Gate on the delayed items (end of sitting and the 7-day cold), not on the first attempt. |

---

## 6. Methods per skill: inside their evidence boundaries for a novice?

| # | Sev | Where | Finding | Expert standard | Fix |
|---|---|---|---|---|---|
| M1 | **blocker** | `llm-behaviour.md:65-80, 93`; every LLM unit's "Pick and say why" (scored, step 2, e.g. `llm-02.md:31-45`) | "Commit before any teaching" is used on a novice, is **scored**, and gates the unit. This misreads the sources cited for it: Mazur's ConcepTests come after pre-reading and a short presentation, and use peer discussion (excluded here); Chen, Kalyuga and Sweller 2015 found "answer first" wins only for **low** element-interactivity material, and tokenization or sampling is not low for someone who met code in August. His own record: cold why-questions 0 of 4 (B10). llm-01 and llm-04 partly survive because the opener half-states the answer; llm-02 (tokens) asks him to infer how tokenizers are built with nothing to infer from. | MAZ, CLT, KAP (generation before instruction needs prior knowledge and consolidation), ROS | Unscored "what do you think?" is fine as a hook. Then teach the mechanism with a worked example (the run plus the refutation), then the scored check. |
| M2 | major | Code Predict step (`code.md:75`) | PRIMM's Predict is a low-stakes prompt, discussed, after the code is introduced; here it is a scored test on a trap. | PRIMM, ROS | As S1. |
| M3 | major | `system-design.md` section 2 (First design before expert reasoning, 40-minute crit) and `INTEGRATED.md:19, 64` | Two "guess the architect's move" cases per type, then commit-and-compare, is a reasonable use of worked cases, but productive failure's boundary is prior knowledge and consolidation. By week 7 he will have seen 2 worked designs of one class and be asked for a full first design with 7 steps in 40 minutes. The d = 0.36 cited (`system-design.md:249`) is for conceptual transfer in school maths and science, not whole-system design from near zero. | KAP, CLT | Keep "guess the move" for the first 4 to 6 cases per class, then completion designs (conjecture given, he does numbers and choices), then full designs. |
| M4 | minor | Evaluation rapid rounds at 20 seconds (`INTEGRATED.md:53` trial), warm-up gate | Kellman's perceptual learning works after the categories are explained; pace targets are fine as trials, not bars. Main risk is the kappa bar (C9). | DRB, CLT | Speed only after 80% accuracy untimed. |
| M5 | minor | `production.md:66` ("at exam pace"), 90-second estimates | Timed practice before accuracy is set. Fluency comes after accuracy in Rosenshine and Direct Instruction. Production's first-time worked solution (`production.md:69`) is the most expert-aligned step in the whole design and should be the model for the others. | ROS, DI | Untimed until 80% accurate. |
| M6 | minor | `engine.py:199-210` (recall interleaved across all skills from day 1) | Interleaving helps tell apart types already learned (Rohrer); with nothing learned yet, mixing adds load. | DRB | Block within a skill for the first 2 weeks, then interleave. |

What is inside its evidence: spaced retrieval with FSRS, card variants on new surfaces, the 7-day cold item, predict-then-run demos after teaching (Crouch 2004), refutation texts (after the right idea is taught), planted quiet bugs from his own error record, Parsons problems with one distractor (code-02, code-03), and verified outputs. Keep all of these.

---

## 7. Tutor behaviour: do the rules block good teaching?

| # | Sev | Where | Finding | Expert standard | Fix |
|---|---|---|---|---|---|
| B1 | **blocker** | `SKILL.md:54-56` ("Never re-explain in longer prose"), `INTEGRATED.md:32-33`, `recommended-method.md:84` | The stuck order has no move that **teaches**: own earlier answer, two options, a picture, then the answer. "Never re-explain" rests on D6 (0 of 5), which were five cases of *more prose of the same explanation*. The same record shows full rebuilds from the template worked 2 of 2 (D8), and he has asked to be taught, not tested, at least five times (C17, C19, C20, C49, plus "explain/teach, I'm a beginner" x4). A lost learner needs a different explanation, not a narrower question. | BG (correctives teach differently), AT (the ladder ends in an assertion), CT (bottom-out hint shows the step), ROS (re-teach when success is low) | Replace with: (1) point at his own earlier answer; (2) two options; (3) a prepared second worked example on a new surface, short, with the picture; (4) the answer explained line by line, then he says it back. Reword the ban to "never repeat the same explanation longer". |
| B2 | major | `SKILL.md:68-69` (Claude does not invent examples) and the guard's verbatim rule (`teaching-guard.py:106-117`) | Right in spirit (Bastani: unguarded AI harms learning; `postmortem.md` cause 1). But with no prepared corrective in the units, the rule leaves the tutor only the Simpler block, which is another question. The guardrail that helped in Bastani was teacher-written hints and solutions, i.e. prepared help, not the absence of help. | BAS, BG | Prepare, check and store the corrective example and the line-by-line answer in every unit, so "no improvising" and "always able to teach" are both true. |
| B3 | major | `SKILL.md:50-51, 57` (right: one line; wrong: one reframe, one hint; at most 3 points), guard 400-character cap | Fine for a one-number answer. For a 35-cell table or a 5-field debug card, it forces answer-level feedback on a multi-step task. Step-level feedback is what makes tutors work. | CT (VanLehn: step-based d 0.76 vs answer-based 0.31), FB (process-level feedback) | Feedback per row or per field, in order, stopping at the first wrong row with its reason. |
| B4 | minor | `teaching-guard.py:118-119` (no "?" before a step) | A check-for-understanding question cannot share a message with the next step. Workable (ask in a separate message) but it discourages the checks Rosenshine requires. | ROS | Allow one check question before the step. |
| B5 | minor | `teaching-guard.py:140-141` (fails closed) | Any checker error blocks teaching mid-session. | n/a | Fail open with a logged warning during a live session. |
| B6 | major | `SKILL.md:26-28, 62` and the unit shape together | The tutor's whole role is reduced to sending verbatim steps and marking. No step asks the tutor to model, think aloud or demonstrate. The AI is being used as a quiz engine, which is the weakest use of a tutor in VanLehn's review and the opposite of AutoTutor's dialogue. | CT, AT, ICAP (interactive needs something to build on) | Add tutor-led "watch me do it" steps with prepared scripts. |

---

## 8. What Khan Academy, CS50 or a Rosenshine-trained teacher would do in week 1

**What they would all do the same way.** Show first, then practise with help, then test; one idea at a time;
many short items; a way back when he is lost that teaches rather than tests.

- **A Rosenshine-trained teacher, first sitting (about 40 minutes).** 5 minutes of review of what he already
  knows (dicts, lists, `for`, KeyError, all on his "taught" list). State the goal in one line ("today: read
  one AI call and the record it writes"). Present one new idea (a record appended to a log) with a tiny
  generic example (3 lines, a shopping list), then the real 6-line version. Model the trace out loud: fill
  the table row by row, saying why each cell holds what it holds. Check for understanding with 3 quick
  questions he should get right about 80% of the time. Guided practice: a near-identical function with the
  table half filled (backward fading); feedback after each row. Independent practice: 3 short traces on new
  inputs, 8 to 10 cells each. Timing, `round`, errors and retries wait for later sittings. Weekly review on
  day 7.
- **Khan Academy.** A short worked-example video or article per skill, then practice items one at a time
  with "get help" hints that end in a full worked solution; wrong or hinted items do not count toward
  mastery, but more items follow, so nothing is ever "never served again"; unit tests and course challenges
  mix skills later, not on day 1. Brilliant adds one small interactive idea per screen and explains every
  answer, right or wrong.
- **CS50 / CS50P.** Lecture with live-coded, narrated demonstrations of the exact pattern (the teacher
  writes it, runs it, breaks it, fixes it), then a section and short walkthrough videos that model the
  approach to each problem, then the problem set with tests (`check50`) and unlimited resubmission.
  Debugging is shown live in lecture (and with `debug50`) before students are asked to debug.
- **A cognitive tutor or AutoTutor.** Feedback on each step as it is taken, hints that escalate to the
  worked step, an explanation (assertion) when hints fail, and a knowledge estimate built from many steps.

**Week 1, redesigned.** Sitting 1: code only (record in a log), as above. Sitting 2: LLM only, with the
mechanism taught first ("the model gives a chance to every next piece", shown with his capital-of-Pakistan
run as a worked example), then predict-and-run, then the ConcepTest as a check. Sitting 3: code (timing a
call), same shape. Sitting 4: LLM tokens, with the tokenizer's build rule and the digit rule taught before
any question. Recall starts the day after the first pass, blocked by skill. Scored checks only at the end of
each sitting and at 7 days.

---

## Prioritised fix list

1. **Add "I do" to every unit (C1, S2, S3, X1, B6).** A required `Worked example` step before any scored step:
   the tutor's filled trace table or filled debug card, one row at a time, one reason per cell, then one
   self-explanation prompt with its answer. Make `check_unit.py` require it.
2. **Add "we do" (S4, B3).** An unscored completion step (half-filled table, first 3 debug fields given) with
   feedback after each row, before the scored step.
3. **Stop scoring before teaching (S1, M1, M2, C2).** Code Predict and LLM Pick become unscored warm-ups
   placed after the example. LLM pass = New case + Cold with a right reason. The first question of a
   sitting targets about 80% success.
4. **Replace the stuck order with a teaching ladder (B1, B2, C5, C6).** Own earlier answer, two options, a
   prepared second worked example on a new surface with a picture, then the answer line by line and he says
   it back. Prepare the corrective in every unit. Let the guard re-send a step after a corrective.
5. **Build the mastery corrective loop (T1, T2, C11).** A miss triggers the corrective, then a parallel item
   in the same or next sitting. Write parallel items now. Retire "never served again".
6. **Make scoring fair and less noisy (C3, C4, T1, T3, T5).** Several short items per bar; hinted item = 0.5,
   shown answer = 0; cold bar 80% on 5+ items; gate on end-of-sitting and 7-day items; prediction after
   practice; confidence never used for demotion.
7. **Control load (X2, Q4, C14, C15, X5).** At most 2 new things per step, enforced by a `new:` header in the
   checker; split code-01 and code-02 Traces; tables of 8 to 12 cells; one unit per sitting in weeks 1 and 2;
   2,000-character cap including code.
8. **Restore his measured template (C7, X3).** Problem, tiny generic example, one picture, paths spelled out,
   in every teaching step; checker enforces the blocks.
9. **Fix the broken items (Q1, Q2, Q3, S5, Q6, X4).** Show code-03's notes; add an aim comment to every
   labelled line; fix the llm-02 Pick table; no skip rule may skip a step that states a tested rule; cards
   and cold answers only from shown text (checker test); show every name a question depends on.
10. **Make the documents one system (C8, C9, C10, C12, C13, C16).** One step list and one bar table per skill,
    matching the structures' own novice bars (production item count, evaluation kappa 0.60 and fail recall
    0.75 with kappa taught first); rungs drive selection or go; cards only after a pass; the 8-week freeze
    applies to numbers, not to whether teaching steps exist.

After these, re-audit one rebuilt unit (code-01) with him before building the rest. His session ledger is
the only validity evidence the system has; A12 (80%) shows what works for him, and it looks like
Rosenshine's sequence.
