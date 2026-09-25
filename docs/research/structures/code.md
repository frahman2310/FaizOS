# Learning structure: Code

> **Amended 2026-09-24:** the independent review (`review.md`) kept this structure with changes. Where this file disagrees with `INTEGRATED.md` (plain step names, shared recall queue, one mastery rule, start order, the week), `INTEGRATED.md` wins.


Written 2026-09-24. Builds on `recommended-method.md`, `postmortem.md` and `curricula/skill-methods.md` C5
(read those for the general method). This file only covers what is special to code, and where the new
experts change or challenge the earlier plan.

Tags: **[M]** measured in a study, **[S]** stated by an expert or a course, **[R]** self-reported by
learners. Grades in section 8: **strong**, **moderate**, **weak**.

Goal, in his words (C44): "code needs to be learnt": specifying, reading and judging, debugging, small
edits. Not writing large programs from a blank file.

---

## 1. What kind of learning this is, and what the new experts add

**Kind.** A procedural skill with a known order (trace, explain, adapt a pattern, debug), practised on a
small set of repeating patterns. Unlike design or evaluation, there is an exact judge on every step: the
machine. Running the code or the tests says right or wrong in seconds, with no expert opinion needed.
That changes the unit: prediction checked by running replaces "compare with the expert" for most steps.

**He is a "conversational programmer".** Guzdial's group names learners who learn code to work with
engineers, not to build software. Normal courses fail them because they teach syntax first; a
"purpose-first" course that teaches a handful of domain patterns got novices doing scaffolded writing,
debugging and explaining after 30 minutes [M, small prototype study]
https://dl.acm.org/doi/10.1145/3411764.3445571 ; the group is defined in Chilana et al. 2016 [S]
https://hci.cs.sfu.ca/ChilanaCHI16ConvProgrammers.pdf . **Consequence:** the course is organised by six
AI-engineering patterns (section 3), not by Python features.

| Expert | What they found | Tag and source | What it changes here |
|---|---|---|---|
| Lister (BRACElet) | Students who trace under 50% accuracy usually cannot explain similar code; tracing plus explaining predicted code writing (R² = 0.66) | [M] https://opus.lib.uts.edu.au/bitstream/10453/11384/1/2009002706OK.pdf (local: `research/lister-2009`) | A gate: no "explain" or "specify" work on a pattern until he traces it at 90% |
| Sentance (PRIMM) | Predict, Run, Investigate, Modify, Make; 13 schools, 493 students, PRIMM group beat control on post-test (3.28 vs 2.58, p = .001, but r = .13, small) | [M, quasi-experiment] https://suesentance.net/wp-content/uploads/2020/02/teaching_computer_programming_with_primm__a_sociocultural_perspective_author_copy.pdf | Reading before writing and small modify steps. Predict is low stakes and unscored, on code already shown (corrected 2026-09-25, G3) |
| Schulte (Block Model) | Understanding has levels (atom, block, relations, whole program) and sides (text, execution, purpose); novices read bottom-up | [S] https://dl.acm.org/doi/10.1145/1404520.1404535 ; https://static.teachcomputing.org/pedagogy/QR12-Block-model.pdf | Investigate questions: one per level, ending at purpose |
| Margulieux, Guzdial | Subgoal-labelled worked examples: 36% more problems solved (61% vs 45%) in the lab | [M] local `research/margulieux-2016` | Every worked example carries subgoal labels |
| Margulieux, Morrison, Decker 2020 | Over a semester (265 students): better weekly quizzes, **not** better exams; fewer drops and fails | [M] https://link.springer.com/article/10.1186/s40594-020-00222-7 | Challenge: labels help while learning, fade them; they are not the mastery test |
| Xie, Nelson, Ko 2018 | A 5 to 10 minute explicit tracing strategy (line by line, write memory down) gave 15% higher tracing scores, n = 24 | [M] https://www.benjixie.com/publication/sigcse-2018/ | The tracing strategy is **taught first**: the tutor fills a table row by row in a show, then tables are faded (corrected 2026-09-25, G6) |
| Cunningham et al. 2017 | Students who sketched a full trace got 82% of reading problems right vs 61% with no sketch; an incomplete sketch was as bad as none. Observational, about students' **own** sketches after a CS1 course; on a code-ordering problem only 3% sketched and both groups scored about 97% | [M, observational] https://www.gvu.gatech.edu/sites/default/files/related_project_files/p164-cunningham.pdf | Corrected 2026-09-25 (G6): the paper concludes a sketch technique should be **taught**; it says nothing about handing a novice a large blank table. Tables are modelled in a show, then faded; a full table is the scored independent task only. A table is a tool for hard tracing, not a default task |
| Nelson (PLTutor) | Tracing taught first, values hidden for the learner to fill: 60% higher gain than Codecademy (3.89 vs 2.42 of 27) | [M, small lab] local `research/nelson-2017` | Each state change is shown with its explanation first; only then are values hidden for him to fill (G6) |
| Sorva (notional machines) | Program visualisation helps mainly when the learner engages with it, not when he watches passively | [S, review] https://dl.acm.org/doi/10.1145/2490822 | Corrected 2026-09-25 (G7): a shown, filled table read line by line with a self-explanation prompt is engagement, not passive watching; it comes before he fills tables himself. Only long unprompted animations are left out |
| Ericson (Parsons) | Parsons with distractors took less time than fixing or writing, same learning; adaptive Parsons solved nearly 2x as often | [M] https://dl.acm.org/doi/10.1145/3141880.3141895 ; local `research/ericson-2019`; https://dl.acm.org/doi/10.1145/3411764.3445292 | Parsons is the cheap bridge between reading and editing, not a goal |
| Lee, Lytle (Use-Modify-Create) | UMC lowered felt difficulty and raised ownership; the study measured perceptions, not scores | [S, R] https://dl.acm.org/doi/10.1145/1929887.1929902 ; https://dl.acm.org/doi/abs/10.1145/3304221.3319786 | Modify before make; "Create" is replaced by "Specify" |
| Michaeli, Romeike | A 10-minute explicit debug process (hypothesise, test, undo failed changes): d = 0.69 on bugs fixed (median 4 vs 2 of 9) | [M] https://computingeducation.de/pub/2019_Michaeli-Romeike_WIPSCE19.pdf | A written debug card used every time |
| Ko et al. 2019 | Written-down debug strategy: describe wrong behaviour, list suspect lines, check each | [S] local `research/ko-2019` | The card's wording |
| Becker 2016 vs Denny 2014 | Better error messages cut repeated errors in one study, had no effect in another | [M, conflicting] https://eric.ed.gov/?id=EJ1117113 | Teach reading the traceback bottom-up instead of relying on nicer messages |
| Porter and Zingaro (CS1-LLM) | Weeks 1 to 4 read, trace, explain; then design function, prompt, test, debug; exams similar on reading, slightly lower on writing from scratch | [M-res, historical] local `ai-steering/papers/vadaparty-2024`; book chapters https://www.manning.com/books/learn-ai-assisted-python-programming | Reading first, then the steer loop; confirms writing from scratch is the cost he can accept |
| Denny et al. (Prompt Problems) | Learner sees input and output only, writes a prompt, tests judge; first prompts miss input format and edge cases | [S, R] https://arxiv.org/abs/2307.16364 ; https://arxiv.org/abs/2401.10759 | The "specify" step |
| Denny et al. 2024 (explain with a purpose) | Explain code in words, an LLM rebuilds it, tests judge the explanation | [S] https://arxiv.org/abs/2403.06050 | Explain and specify become one skill checked by tests |
| Kazemitabaar 2023 (CHI) | Novices with Codex: 1.15x completion, 1.8x scores, no loss on manual edits, no difference a week later | [M, n = 69, ages 10 to 17] https://arxiv.org/abs/2302.07427 | AI in the loop is safe for learning if he reads and edits |
| Kazemitabaar 2023 (Koli) | "One prompt for the whole task" gave the best authoring scores and the **worst** later modification scores | [M, n = 33] https://arxiv.org/abs/2309.14049 | He never prompts a whole task before he has traced and modified that pattern |
| Prather 2024 | For struggling novices AI help compounds metacognitive problems, including an illusion of competence | [M, qualitative, n = 21] https://arxiv.org/abs/2405.17739 | Predict before every run; his score prediction before every check |
| 2026 A/B crossover (N = 220) | Evaluating flawed AI solutions instead of solving: higher homework scores, **no** exam gain | [M] https://arxiv.org/abs/2607.27586 | Challenge: "review the AI diff" alone does not teach; he must also write the test that exposes the bug |
| GitHub, Anthropic, Willison | Run tests first; look for invented APIs, ignored constraints, deleted or skipped tests, code that looks right but misses intent; never commit code you cannot explain | [S] https://docs.github.com/en/copilot/tutorials/review-ai-generated-code ; https://code.claude.com/docs/en/best-practices ; local `ai-steering/willison-vibe-coding.md` | The review checklist |
| Hundhausen; Indriasari review | Code review in class improved code quality and discussion (51 studies, mostly benefits, few controlled) | [S, R] https://dl.acm.org/doi/10.1145/1539024.1508972 ; https://dl.acm.org/doi/10.1145/3403935 | Review is kept, but judged by the planted bug found, not by his feeling |

**His own record points the same way** (`docs/learning-evidence.md`): a step table of working code **with the
last cells blank** 3 of 4 (D5: backward fading, not a full blank table; corrected 2026-09-25, G19) and tables
of working code 5 of 6 (B11), but simulating broken code in a table 0 of 4 (B11), so planted bugs stay out of
tables; "someone broke it" with only a
label 5 of 6; tiny example first was the strongest predictor (B1); code shown in chat, not in files (B7);
writing from blank 0 of 4 (B10). His four repeat errors (E1 quiet wrong vs crash, E2 start line inside a
loop, E3 one record per call vs per try, E4 what kind of value a name holds) become fixed item types.

---

## 2. The structure: one code unit, "show, try with me, your turn" (about 30 minutes)

> **Rewritten 2026-09-25** after the voided first code session (C49) and the gap audit
> (`docs/research/gap-audit-code.md`, G1 to G20). The old order (Predict, Trace, Change, Break, Steer) put a
> scored question on untaught code first and a full blank memory table second; no step showed a worked example.
> The template below is `docs/research/curricula/code-teaching-experts-v2.md` section (e), which carries the
> sources and a message-by-message sample of unit 1. The unit format is enforced by `learn/check_unit.py`
> (Kind: show / try / scored / close).

The tutor prepares everything before the session, runs every program with `learn/code/record.py`, and stores
the outputs. All code is shown in chat. One step per message, 700 to 2,100 characters where possible (his B8),
2,600 at most including code. Real terms (variable, function, argument, return value, dict, key, list), each
explained in the sentence where it first appears. Every code block comes with a **How this code works** block
that reads the code line by line in run order, saying what each line leaves behind and why it is built that
way, and never gives the answer to a question (C48, G11).

| # | Step | Kind | What the message contains | Source |
|---|---|---|---|---|
| 0 | Recall | (queue) | Up to 3 old cards, never on today's pattern | Rosenshine 1; FSRS queue |
| 1 | Goal and steps | show | The job in one line; the problem it solves; the pattern's 2 to 4 **subgoal labels** as a short list, up front; one line per new word | CS1 Subgoals project; Xie 2019 4.1.1 |
| 2 | **Show 1** (I do, tiny) | show | One knowledge point. A 2 to 5 line correct program, its recorded output, each line read in words with the value it leaves; a filled trace table the first time tables appear; one self-explanation prompt on the key line | Rosenshine 2 to 4; CS50P lecture 0; his B1 |
| 3 | **Try with me 1** (we do) | try | Same shape, new surface; the trace table filled except its last row; one hinge question whose wrong options each match a named wrong idea (E1 to E4) | Renkl and Atkinson; Wiliam |
| 4 | **Show 2** | show | The next knowledge point, one new idea added to the same kind of example; same line-by-line reading; one prompt | Math Academy knowledge points; Xie "added complexity" |
| 5 | **Try with me 2** | try | The last two rows blank, or one line to complete | Renkl backward fading |
| 6 | **Show 3** (the real shape) | show | The real-sized version (up to about 15 lines) with the subgoal labels named in its reading. Broken versions appear only here or later, after two correct examples, each run and labelled (crash / quietly wrong) as it is shown | Margulieux 2016; CS50P lecture 4; Große and Renkl 2007 |
| 7 | **Try with me 3** | try | Parsons with one distractor, or a pick-the-line hinge | Ericson; Subgoals formative practice |
| 8 | **Your turn** (you do) | scored | A new program of the same shape: trace it in full, then predict and label changed copies (crash / quietly wrong / fine), now that each label has been shown; each labelled line carries its aim | Rosenshine 9; PRIMM Modify |
| 9 | Close | close | "Next time I see ..., I ..."; cards join the queue | Rosenshine 10 |
| extra | Help: <step> | show | A second worked example on a new surface, for every try and the scored step, sent in the stuck order | Khan hints; Rosenshine re-teaching |
| extra | Retry / Cold | scored | Same kind, new surface: after a miss, and 7 days later | Bloom and Guskey; `recommended-method.md` |

Rules that sit on top of the order:
- **One knowledge point per show**, at most 3 new ideas (listed in the step's `New:` line). Each try aims at
  about 80% right first time; tries are never scored. The bar applies only to Your turn, Retry and Cold (G16).
- **Nothing is asked before it is taught** (G3). Predicting output is a check after a show, never first contact.
- **Tables are faded, not handed over blank** (G5, G6): filled and read aloud in a show, then the last row blank,
  then the last two, then a full table only in the scored step.
- **Correct before broken** (G14): planted bugs only after two correct worked examples of the pattern, and the
  crash / quietly wrong / fine labels only after an example of each has been shown.

Later units of the same pattern: one show, tries with more blanks, then Change (edit to pass a test), then
Find the bug (label-only first, then the debug card modelled once by the tutor), then Tell the AI. From the
third problem of a pattern he attempts first and then sees the expert version (`method-effectiveness.md`
section 3). A new pattern starts again at Show (4C/ID saw-tooth).

**Placement and fading** (skill-methods D2): a 90-second first-step test on a new pattern; right twice → the
unit starts at Try with me 3. After C49 his placement on T1 is "not yet". Subgoal labels are removed from the
third example of a pattern (Margulieux 2020: they help quizzes, not exams).

**Stuck order** (from his record, D1, D4; `SKILL.md`): his own earlier answer or the show it uses; two options;
the step's prepared Help block (a second worked example); the answer worked line by line, which he says back.
Never more improvised prose (D6: 0 of 5).

**Why this differs from the other four skills**

| | Evaluation | System design | Production | LLM behaviour | **Code** |
|---|---|---|---|---|---|
| Who judges | expert labels | expert design | exact number | the measured run | **the machine: run output and tests** |
| Core move | label, then compare | commit, compare, changed fact | faded numeric solution | predict, run, one line | **show, try with me, your turn; later change, find the bug, steer** |
| Material | real traces | briefs | formulas | model calls | **a fixed library of 6 patterns, each with planted bugs** |
| Practice kind | non-recurrent judgement | non-recurrent | recurrent maths | facts and concepts | **recurrent procedure: speed and accuracy drills are allowed (4C/ID part-task practice)** |
| Errors | missed failures | trade-off missed | arithmetic | wrong mental model | **quiet wrong results are the main teaching material** |
| AI's role | judge to validate | none | none | the object studied | **a tool he steers inside the unit** |

---

## 3. Progression

### 3a. Levels and milestones

| Level | Name | Milestone (observed, on code he has not seen) |
|---|---|---|
| L1 | Reader | Traces a 30-line function with 90% of table cells right; labels crash / quiet / fine 9 of 10; explains purpose at 5 of 7 or better; solves a Parsons with distractors |
| L2 | Fixer | 5 bugs found with the card, each under 10 minutes, no new bugs added; 3 edits of 5 to 20 lines passing tests; reads a SQL join and says the row count before running |
| L3 | Steerer | 3 changes where a fresh AI, given only his spec and tests, passes hidden tests in 2 prompts or fewer; finds the planted bug in 4 of 5 AI diffs and writes the test that catches it |

### 3b. The skill ladder, per pattern

trace → explain → Parsons → modify → debug → specify for an AI → review an AI diff.
He climbs a rung after 2 right in a row with a right one-line reason; falls one rung after 2 misses.
Lister's gate: explain and specify open only after trace reaches 90% on that pattern.

### 3c. Task classes (the six patterns, in order)

Each class restarts at a worked example (4C/ID saw-tooth). Order follows the prerequisite graph in
`curriculum-design.md` (C1 to C9) and the FBR product it feeds.

| Class | Pattern | Subgoal labels | Worked example source | Planted-bug family |
|---|---|---|---|---|
| T1 | API call and reading the reply | build request, send, check status, pull fields | CS50P lecture 4 (requests, JSON); Anthropic Messages API docs | dict vs the value inside (E4), missing key |
| T2 | Retry loop with timeout | set start values, try, record, wait, give up | `projects/meter/meter.py` `call()`; Forge errors chapter; CS50P lecture 3 | start line inside the loop (E2), one record per try (E3) |
| T3 | Eval script | load cases, score each, count, compare to baseline, decide | `projects/evals/gate/gate.py` | counting the wrong list, off-by-tolerance |
| T4 | SQL query | pick tables, join, filter, group, aggregate | `projects/search/lab/lab.db` | count of all rows vs count of hits (E1) |
| T5 | Retrieval function | score, sort, keep top k, check hit | `projects/search/lab/lab.py` `top()`, `hit()` | sort direction, k off by one |
| T6 | Agent loop | send, read tool request, run tool, append result, stop rule | Anthropic tool-use docs; local `ai-steering/willison-agentic-patterns/02` | missing stop rule, result not appended |

Placement: his bootcamp covered the parts of T1 to T3 (A9, 69 of 88), so the first-step test is run on
T2 and T3 first; he likely starts at L1 on T2.

---

## 4. Practice formats, one example each

All outputs below were produced by running the code on 2026-09-24.

| Format | Example | Right answer |
|---|---|---|
| Predict and label (E2) | `log = []` / `for call in range(3):` / `    log = []` / `    log.append(call)` / `print(len(log))` | `1`, quietly wrong (the start line moved inside the loop) |
| Trace with memory table (E3) | `meter.py` `call()` with `BACKOFF = [0.5, 1.0, 0.0]`; the provider fails twice then answers. Table: `attempts`, `why`, rows in `log` after each try | attempts 3; `why` "529 overloaded" then unchanged after success; **one** row in `log`, written on the success |
| Explain in plain English | `hit(passage, q)` from `lab.py` | "True when the passage comes from the right document and contains every anchor phrase" (purpose level), not a line-by-line story |
| Explain so an AI rebuilds it | `top()` with names hidden (`foo(a, b, c, d)`); he completes "Create a function foo that..." | A fresh model's code passes the tests on `top()` |
| Parsons with a distractor (E2) | The lines of `gate.py` `score()` shuffled, plus a twin `passed = 0` placed inside the loop | `passed = 0` and `failing = []` before the loop; the twin left out |
| Modify | Change `gate()` so it also prints how many cases newly **pass** | Passes a given test with the "better" version |
| Find the planted bug (E1) | `meter_broken.py` line 120 reads `for row in log:` instead of `for row in oks:` | Symptom: when the provider is down, "succeeded on retry" shows 3 though 0 calls succeeded (fixed file: 0). Quietly wrong, no crash |
| SQL quiet wrong (E1) | `select count(res.rank) ...` to count questions found in run 1 | Gives 100 (counts rank 0, "not found", too). Right: `sum(res.rank between 1 and r.k)` gives 45 |
| Read a traceback | CS50P lecture 3 NameError after shrinking a `try` block | Read the last line first, then the line number above it |
| Specify for an AI (prompt problem) | Only input and output shown: provider fails twice then succeeds → 3 attempts, 1 log row; provider always fails → 3 attempts, 1 failure row, `None` returned | His spec makes a fresh model's `call()` pass all 4 hidden tests in 2 prompts or fewer |
| Review an AI diff | A diff that "fixes" a failing gate by raising `TOLERANCE` from 2 to 5 and deleting one case | Names the pitfall (test weakened, not code fixed; GitHub list), writes the test that fails on it |

---

## 5. Assessment, mastery and retention

| Skill | Check | Mastery bar |
|---|---|---|
| Trace | Memory table on unseen code of the class | 90% of cells right, 2 sessions in a row, then 80% or more cold at 7 days |
| Label | crash / quiet / fine, 10 mixed items | 9 of 10 |
| Explain | EiPE rubric, or AI rebuild passes tests | 5 of 7, or tests pass |
| Change | Given tests | All pass, in 2 attempts or fewer |
| Debug | Planted bug with the card | Found under 10 minutes, fix passes tests, no new failures, failed fixes undone |
| Specify | Hidden tests on fresh-model code | Pass in 2 prompts or fewer |
| Review | AI diff with one planted bug | Found in 4 of 5, plus the exposing test |
| Speed (recurrent skill) | Trace a 20-line function | 5 minutes or less by the end of L1 |

A pattern is mastered when the class's rungs pass and a transfer item passes: an unseen Forge lab with
hidden tests, or an Exercism exercise in the matching concept, done cold.

**Retention.** Daily reps: 3 items, 5 minutes, drawn from all mastered patterns, interleaved (never
three of one pattern), spaced 1, 3, 7, 21 days. At least one per day targets E1 to E4 until each has 5
right in a row cold. Other tracks supply code too: every evaluation or production unit includes one
trace of its own script (skill-methods C5). This is re-testing, not re-teaching (postmortem cause 6).

---

## 6. Weekly dose and session length

| Slot | Length | What |
|---|---|---|
| Tue, Thu | 30 min each | One full unit (section 2) |
| Mon to Sat | 5 min | Daily reps (section 5) |
| Every 3rd week, Sat | 45 min | One steer session on the FBR assistant: he specifies a real change, the AI writes it, he reviews and runs the tests |

About 1 h 30 to 1 h 45 a week. Session length 30 minutes: his best formats sat at 5 to 10 short items per
message (B9) and messages of 700 to 2,100 characters (B8); one unit is about 7 such messages. Pace: one
pattern (task class) every 2 to 3 weeks, so L1 to L3 across six classes in about 4 to 5 months.

---

## 7. Measures that show it is working

| Measure | Healthy | Alarm |
|---|---|---|
| Predict step right first try | rising within a pattern, 80%+ by its third unit | flat for 3 units |
| Trace cells, cold at 7 days | 80% or more | under 70% |
| E1 to E4 misses on daily reps | falling to 0 per week | same count 3 weeks running |
| Debug: time to find a planted bug | falling; under 10 min | hypotheses changing code at random (no card use) |
| Prompts to pass hidden tests | 2 or fewer by L3 | over 4, or passes only by pasting code |
| Transfer (unseen Forge lab or Exercism) | passes cold | unit checks 90%+ but transfer fails: recognition, not skill |
| Prediction gap (his score guess vs actual) | 10 points or less after 4 weeks | over 20 (Prather's illusion of competence) |
| Explain-before-commit | he can explain every line of each AI diff he accepts | any accepted diff he cannot explain |

---

## 8. Evidence grade for each choice, and what is left out

| Choice | Grade | Why |
|---|---|---|
| Read and trace before explain, explain before write | strong | Lister, Lopez replicated; Xie; CS1-LLM |
| Tracing strategy modelled, then faded tables; full table only when scored | moderate | Xie 2018 (n = 24), PLTutor, Cunningham 2017 (observational); corrected 2026-09-25 (G6) |
| Subgoal-labelled worked examples, faded | moderate | lab gains strong; semester exams null |
| Worked example, then completion, then independent (show, try, your turn) | strong | Rosenshine; Renkl and Atkinson; Sweller; gap audit G1 to G5 |
| PRIMM predict as an unscored check after a show | moderate for the order, weak for size | one quasi-experiment, r = .13; Predict is low stakes in PRIMM itself |
| Parsons with distractors | moderate | same learning, less time; efficiency, not superiority |
| Explicit debug card | moderate | d = 0.69, one classroom study, plus Ko |
| Planted quiet bugs from his own record | moderate | his E1 to E4 counts; B11 label format 5 of 6 |
| Purpose-first patterns (six classes) | weak to moderate | one prototype study, fits his goal exactly |
| Specify via prompt problems | weak | deployments and perceptions, no controlled learning test |
| AI review with an exposing test | weak | review alone showed no exam gain (N = 220); test writing added by CS50P pset 5 design |
| Daily interleaved reps | strong | spacing and interleaving (recommended-method) |
| Predict your score before each check | moderate | calibration research; guards against Prather's illusion |

**Left out, and why**

| Left out | Why |
|---|---|
| Writing whole programs from a blank file | Not his goal; his record 0 of 4; CS1-LLM accepts lower from-scratch writing |
| Syntax drills (Xie's S2) beyond what edits need | He edits, the AI types |
| Long, unprompted watch-only animations (UUhistle style) | Sorva: learners gain when they engage; a shown table read line by line with a prompt is kept (G7) |
| Nicer error messages as the fix | Conflicting evidence (Becker vs Denny); reading tracebacks is taught instead |
| Long CS50P lectures as the main method | Passive; lecture code is used as snippets |
| "Create" from Use-Modify-Create | Replaced by Specify; UMC evidence is perception only |
| Peer code review | No peers; review is against a planted bug and tests |
| Prompting a whole task before tracing the pattern | Kazemitabaar 2023: best authoring, worst modification |
| Style checking (style50), OOP, regex, async | Not in the six patterns; async enters only at a service-repo capstone (C7, C9) |
| Points, streaks, certificates | Weak evidence (recommended-method section 8) |

**Limits.** No study covers adult self-learners steering AI coding tools; most effects come from school
or CS1 classes; the 2026 A/B study and the AI-steering work are young. Promptly and CS1-LLM results are
partly self-reported. The six-pattern library is my synthesis from the curriculum graph and his product,
not from one source.
