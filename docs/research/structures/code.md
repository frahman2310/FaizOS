# Learning structure: Code

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
| Sentance (PRIMM) | Predict, Run, Investigate, Modify, Make; 13 schools, 493 students, PRIMM group beat control on post-test (3.28 vs 2.58, p = .001, but r = .13, small) | [M, quasi-experiment] https://suesentance.net/wp-content/uploads/2020/02/teaching_computer_programming_with_primm__a_sociocultural_perspective_author_copy.pdf | The unit order. The effect is small, so PRIMM is the frame, not the engine |
| Schulte (Block Model) | Understanding has levels (atom, block, relations, whole program) and sides (text, execution, purpose); novices read bottom-up | [S] https://dl.acm.org/doi/10.1145/1404520.1404535 ; https://static.teachcomputing.org/pedagogy/QR12-Block-model.pdf | Investigate questions: one per level, ending at purpose |
| Margulieux, Guzdial | Subgoal-labelled worked examples: 36% more problems solved (61% vs 45%) in the lab | [M] local `research/margulieux-2016` | Every worked example carries subgoal labels |
| Margulieux, Morrison, Decker 2020 | Over a semester (265 students): better weekly quizzes, **not** better exams; fewer drops and fails | [M] https://link.springer.com/article/10.1186/s40594-020-00222-7 | Challenge: labels help while learning, fade them; they are not the mastery test |
| Xie, Nelson, Ko 2018 | A 5 to 10 minute explicit tracing strategy (line by line, write memory down) gave 15% higher tracing scores, n = 24 | [M] https://www.benjixie.com/publication/sigcse-2018/ | He always traces with a memory table, never in his head |
| Cunningham et al. 2017 | Students who sketched a full trace got 82% of reading problems right vs 61% with no sketch; an incomplete sketch was as bad as none | [M] https://www.gvu.gatech.edu/sites/default/files/related_project_files/p164-cunningham.pdf | The trace table must be complete; half tables are marked incomplete |
| Nelson (PLTutor) | Tracing taught first, values hidden for the learner to fill: 60% higher gain than Codecademy (3.89 vs 2.42 of 27) | [M, small lab] local `research/nelson-2017` | Trace items hide values; he fills them |
| Sorva (notional machines) | Program visualisation helps mainly when the learner does the simulating, not watching | [S, review] https://dl.acm.org/doi/10.1145/2490822 | He fills the memory table himself; no watch-only animations |
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

**His own record points the same way** (`docs/learning-evidence.md`): step tables of working code 3 of 4
(D5) and 5 of 6 (B11), but simulating broken code in a table 0 of 4 (B11); "someone broke it" with only a
label 5 of 6; tiny example first was the strongest predictor (B1); code shown in chat, not in files (B7);
writing from blank 0 of 4 (B10). His four repeat errors (E1 quiet wrong vs crash, E2 start line inside a
loop, E3 one record per call vs per try, E4 what kind of value a name holds) become fixed item types.

---

## 2. The structure: one code unit, "Predict, Trace, Change, Break, Steer" (30 minutes)

The tutor prepares everything before the session, runs every snippet, and stores expected outputs.
All code is shown in chat, 30 lines at most per block.

| # | Step | Min | What he does | What the tutor does | Material comes from |
|---|---|---|---|---|---|
| 1 | Warm reps | 4 | 3 cold items from old patterns, mixed, spaced at 1, 3, 7, 21 days; at least one is E1 to E4 | Runs them, marks, queues misses | His review queue |
| 2 | Predict | 3 | A tiny version (8 lines at most) of today's pattern: writes the output and a label: crash, quietly wrong, or fine. Then his score prediction for the unit | Runs it; if wrong, asks only "which line did you read differently?" | Forge chapter snippets (outputs stripped), CS50P lecture code |
| 3 | Trace | 7 | The real 15 to 30 line worked example, with subgoal labels as comments. Fills a memory table for one input (every name, every row, hidden values) | Checks cell by cell against the run; incomplete table sent back | His own lesson code in `projects/`, CS50P, Forge |
| 4 | Explain | 2 | Three block questions (one line, one block, the whole) ending in one sentence: what is this for | Scores purpose level on the 7-point EiPE rubric; later, feeds his sentence to a fresh model and runs the tests on what it builds | Zilles rubric, Denny 2024 |
| 5 | Change | 5 | Parsons with one distractor (first time on a pattern), then a 1 to 5 line edit to meet a changed spec | Runs the given tests; shows the reference edit after he passes or after 2 hints | Exercism exemplars, CS50P psets, own code |
| 6 | Break | 6 | A planted quiet bug in the same code. Uses the debug card: symptom, suspect lines, hypothesis, predicted check result, run, fix, rerun tests, undo failed fixes | Runs only what he asks; holds the answer until 2 failed hypotheses | Real bugs from his record, `projects/meter/meter_broken.py`, Real Python IDLE example |
| 7 | Steer | 3 | Level 2 and up: writes a spec (goal, input, output, constraint, one test) for an AI; or reviews an AI diff with the checklist and writes a test that exposes its bug | Sends the spec to a fresh model with no context, runs hidden tests, reports pass/fail per test | Prompt Problems format; GitHub and Anthropic checklists |

Close (inside step 7): predicted score vs actual, misses go into the queue. No written reflection;
the prediction gap is the reflection.

**Placement and fading** (unchanged from skill-methods D2): a 90-second first-step test on a new pattern;
right twice → skip steps 2 to 3 and start at Change. Subgoal labels are removed from the third example
of a pattern (Margulieux 2020: they help quizzes, not exams).

**Stuck order** (from his record, D1, D4): his own earlier answer or table; then two options; then the
answer with the reason. Never more prose (D6: 0 of 5).

**Why this differs from the other four skills**

| | Evaluation | System design | Production | LLM behaviour | **Code** |
|---|---|---|---|---|---|
| Who judges | expert labels | expert design | exact number | the measured run | **the machine: run output and tests** |
| Core move | label, then compare | commit, compare, changed fact | faded numeric solution | predict, run, one line | **predict, trace, change, break, steer** |
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
| Memory table for every trace | moderate | Xie 2018 (n = 24), Cunningham 2017 (observational) |
| Subgoal-labelled worked examples, faded | moderate | lab gains strong; semester exams null |
| PRIMM order | moderate for the order, weak for size | one quasi-experiment, r = .13 |
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
| Watch-only animations or visualisers (UUhistle style) | Sorva: learners gain when they simulate, not watch; the memory table does that |
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
