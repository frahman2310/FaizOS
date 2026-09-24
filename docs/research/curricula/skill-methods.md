# Five skills, five methods: how to teach each one

Written 2026-09-24. Starts from Faiz's own split of AI engineering into five skills (handwritten notes,
2026-09-24): evaluation and error analysis, how LLMs behave, system design, production, and code. His two
findings shape everything below: one explain-then-quiz format for everything suppressed his own thinking,
and a fully open investigation failed because it had no structure and no expert answer to compare against.
The fix both findings point to is the same: **worked examples as the reference point, then his own attempt,
then a side-by-side comparison with an expert answer.**

Does not repeat: ../teaching-methods.md (self-explanation, contrasting cases, prediction, erroneous
examples, productive failure meta-analysis, expertise reversal basics, retrieval, spacing, interleaving),
teaching-structure.md (unit template, five practice types, platform unit shapes), curriculum-map.md
(module order). This file adds: which method fits which kind of knowledge, how worked examples are laid out
on proven platforms, and a method per skill.

Tags: **[M]** measured (a study or platform data with numbers). **[S]** stated (the author or platform
describing its own method, or a finding reported without numbers). **[M-self]** a number the company reports about itself.

---

## A. Kinds of knowledge and the method each one needs

### A1. The two classic splits
| Framework | The kinds | Source |
|---|---|---|
| Revised Bloom (Anderson and Krathwohl 2001) | Factual (terms, facts), conceptual (how facts connect: principles, models), procedural (how to do it and when to use which method), metacognitive (knowing your own thinking). A second axis to the six verbs, so a skill is a cell in a grid, not a rung on a ladder | [S] https://quincycollege.edu/wp-content/uploads/Anderson-and-Krathwohl_Revised-Blooms-Taxonomy.pdf ; https://teaching.uic.edu/cate-teaching-guides/syllabus-course-design/blooms-taxonomy-of-educational-objectives/ |
| Anderson, ACT theory (1982) | A skill starts **declarative** (facts you rehearse while you act, slow, many errors), goes through **knowledge compilation** (steps merge, facts get built into the action), ends **procedural** (fast, no talking yourself through it) | [S] https://gwern.net/doc/iq/1982-anderson-2.pdf ; https://www.jimdavies.org/summaries/anderson1982-3.html |
| 4C/ID (van Merrienboer) | **Non-recurrent** parts (judgement, different every time) are learned from whole tasks plus "supportive information" (mental models, strategies) given before and kept available. **Recurrent** parts (done the same way every time) get "procedural information" just in time, and part-task drill only after they have been met in a whole task | [S] https://www.4cid.org/wp-content/uploads/2021/04/vanmerrienboer-4cid-overview-of-main-design-principles-2021.pdf |

### A2. What works for which kind (evidence)
| Method | Works best for | Evidence |
|---|---|---|
| **Retrieval practice** | Factual, and the facts inside concepts | Swahili word pairs, one week later: about 80% recalled with repeated testing vs 36% and 33% when items were dropped from testing; repeated studying added nothing [M] https://web.mit.edu/jbelcher/www/learner/retrieval.pdf |
| **Generation (answer before being told)** | Low-complexity material, few parts that interact | Worked examples beat problem solving on high-interactivity geometry; generating beat being shown on low-interactivity material [M] Chen, Kalyuga, Sweller 2015 https://eric.ed.gov/?id=EJ1071512 |
| **Worked examples** | Procedural and conceptual material with many interacting parts, for novices | Examples-only and example-then-problem pairs beat problem-only and problem-then-example pairs for novices [M] van Gog, Kester, Paas 2011 https://eric.ed.gov/?id=EJ927458 . Good examples label subgoals, use several examples per problem type, and vary surface features so deep structure shows [S, review] Atkinson et al. 2000 https://journals.sagepub.com/doi/10.3102/00346543070002181 |
| **Completion problems and fading** | The move from studying to doing | Early in skill learning examples win; later, problem solving wins; fading in steps one at a time bridges it [S] Renkl and Atkinson 2003 https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_3 . Fading helps near transfer reliably but not far transfer, so pair it with "which principle is this step" prompts [S] https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6 |
| **Adaptive fading** | Tailoring to the learner | Fading tuned to each student's measured mastery beat fixed fading on immediate and one-week tests in the lab; the classroom replication held on the delayed test only [M] Salden et al. 2010 https://link.springer.com/article/10.1007/s11251-009-9107-8 |
| **Self-explanation** | Getting the most out of each example | Good students produced 52 idea statements vs 18 for poor students while studying the same physics examples, and spent 13 vs 7 minutes on them [M] Chi et al. 1989 https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1302_1 ; prompting it works too [S] Chi et al. 1994 https://andymatuschak.org/files/papers/Chi%20et%20al%20-%201994%20-%20Eliciting%20self-explanations%20improves%20understanding.pdf |
| **Subgoal labels** | Procedures with many steps (code) | Labels in both text and examples improved solving of new programming problems [S] https://www.sciencedirect.com/science/article/abs/pii/S095947521530044X ; App Inventor studies https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/b/1555/files/2020/09/MargulieuxCatramboneGuzdial2016.pdf |
| **Productive failure, then consolidation** | Conceptual understanding and transfer, once the tools to attempt exist | Both orders gave high procedural knowledge; solve-first gave better conceptual knowledge and transfer (variance) [M, two RCTs] Kapur 2014 https://onlinelibrary.wiley.com/doi/abs/10.1111/cogs.12107 . It fails without instruction that compares learner solutions with the canonical one step by step [S] Loibl and Rummel 2014 https://www.sciencedirect.com/science/article/abs/pii/S0959475214000656 |
| **Inventing to prepare** | Seeing why a formula has the form it has | Invention followed by a lecture gave gains in procedure, insight into formulas and evaluating data, though inventors never found the standard formula [S] Schwartz and Martin 2004 https://aaalab.stanford.edu/assets/papers/2004/Inventing_to_prepare_for_future_learning.pdf |
| **Comparing solutions side by side** | Flexible procedure; judging between methods | 70 students; comparing two worked methods side by side gave larger gains in procedural knowledge and flexibility than studying them one at a time, with similar conceptual gains [M] Rittle-Johnson and Star 2007 https://www.semanticscholar.org/paper/Does-comparing-solution-methods-facilitate-and-An-Rittle-Johnson-Star/1591c94ea47a603ca35cae9e01e656305931cb88 |
| **Erroneous examples** | Learners with some prior knowledge | Learners with none did better on correct examples only; learners with a little did better with added wrong examples, large effect [M] Große and Renkl 2007 https://eric.ed.gov/?id=EJ780439 |
| **Interleaving** | Choosing which method fits (confusable problem types) | One-month test: 74% interleaved vs 42% blocked, d = 0.79 [M] https://files.eric.ed.gov/fulltext/ED557355.pdf ; RCT in 54 classes: 61% vs 38%, d = 0.83 [M] https://gwern.net/doc/psychology/spaced-repetition/2019-rohrer.pdf |
| **Deliberate practice** | Recurrent sub-skills with clear right answers | Well-defined tasks at the right difficulty with feedback [S] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6731745/ . Practice explained 26% of performance variance in games, 21% music, 18% sports, 4% education, under 1% professions [M] https://journals.sagepub.com/doi/abs/10.1177/0956797614535810 . Useful for drills, weak as a whole plan |
| **Expertise reversal and when to stop** | Every skill, over time | Structured examples help low-knowledge learners; open problem solving helps as knowledge grows [S] https://link.springer.com/article/10.1007/s11251-009-9107-8 . A rapid "first step" test correlated up to .92 with full tests, at 2.5 to 4.9 times less test time; instruction tailored with it beat fixed instruction [M] Kalyuga and Sweller https://link.springer.com/article/10.1007/BF02504800 |
| **Training self-assessment** | Metacognitive (judging his own work) | Watching a model assess their own work and pick the next task improved students' self-assessment and later self-directed learning (N = 80, N = 90) [M] Kostons, van Gog, Paas 2012 https://eric.ed.gov/?id=EJ950445 |

### A3. His five skills mapped onto the kinds
| Skill | Main kind of knowledge | Recurrent or non-recurrent | So the core method is |
|---|---|---|---|
| 1 Evaluation and error analysis | Procedural (a fixed method) + conceptual (what counts as a failure) | Method recurrent, judgement non-recurrent | Worked example, completion, fading; comparison with expert labels |
| 2 How LLMs behave | Factual + conceptual | Recurrent facts | Predict, run, explain; retrieval and spacing. Not long worked examples |
| 3 System design | Conceptual + metacognitive (his own reasoning) | Non-recurrent | Worked examples in a fixed frame, then attempt first and compare with the expert design |
| 4 Production | Procedural maths + conceptual (which lever) | Arithmetic recurrent, lever choice non-recurrent | CFA-style worked numeric solutions, fast fading, drill on the formulas |
| 5 Code | Procedural, in a known hierarchy (read, trace, explain, write) | Mostly recurrent | Subgoal-labelled examples, tracing, completion, bug finding, prompt problems, tests as the check |

---

## B. How proven platforms lay out worked examples and practice

| Platform | Precise structure | One concrete example | Source |
|---|---|---|---|
| **Khan Academy** | Video worked example, then exercises. Each exercise has hints, one step at a time; showing every hint gives a full worked example. Advice: try first if the problem looks a little familiar. Levels: 70 to 85% on an exercise gives Familiar (50 of 100 points), all right from Familiar gives Proficient (80), all right on a unit test or course challenge from Proficient gives Mastered (100) | Hints reveal step 1, then step 2, and so on, so the learner can stop as soon as the next step is clear | [S] https://blog.khanacademy.org/how-should-people-practice-on-khan-academy/ ; levels [S] https://support.khanacademy.org/hc/en-us/articles/5548760867853--How-do-Khan-Academy-s-Mastery-levels-work |
| **Math Academy** | Each lesson: an introduction, then 3 to 4 "knowledge points" of rising difficulty. Each is one worked example (steps grouped under subgoal labels) followed by 2 to 5 practice questions on the same type, adapting to performance. Fail a lesson twice at the same point and you get remedial reviews on its key prerequisites from the knowledge graph. Reviews later are mixed so it is not obvious which example to copy: scaffolding is stripped on purpose (expertise reversal). About 7 practice problems per worked example read | Lesson "Exponents with Rational Bases": part 1 express 4 x 4 x 4 as 4^3, later parts harder; fail part 2 twice and it sends reviews of that part's prerequisite | [S] The Math Academy Way, pp. 75-76, 183, 223 https://www.justinmath.com/files/the-math-academy-way.pdf ; spaced repetition flows down the graph [S] https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/ |
| **Brilliant** | Problem before procedure (pretest), one concept per 5 to 15 minute lesson, a chain of small problems, custom feedback per answer | See teaching-structure.md | [S] https://brilliant.org/about/ |
| **Hello Interview** | Every breakdown uses the same headings in order: Understanding the problem, Functional requirements, Non-functional requirements, The set up, Core entities, The API, High-level design, Potential deep dives, What is expected at each level. A "Try it yourself first" prompt before the non-functional requirements. Each deep dive lists Bad, Good and Great options with the reason | Bitly uniqueness: Bad = long-URL prefix (any two URLs sharing the first N characters collide); Great = hash with collision retries; Great = unique counter with base62 (no collisions by design) | [S] https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly ; levels [S] https://www.hellointerview.com/blog/the-system-design-interview-what-is-expected-at-each-level |
| **ByteByteGo (Alex Xu)** | Four steps every time: scope, high-level design with buy-in, deep dive, wrap-up. Scope is written as a Candidate/Interviewer dialogue, then back-of-envelope numbers | URL shortener: 100M URLs a day gives 1,160 writes/s, 11,600 reads/s (10:1), 365 billion records and 36.5 TB over 10 years; 62^7 = 3.5 trillion is above 365 billion, so 7 characters | [S] https://bytebytego.com/courses/system-design-interview/design-a-url-shortener |
| **ScaleDojo capstone** | "How to approach any GenAI system design": clarify requirements (scale, latency, budget, safety), identify capabilities (generation, retrieval, agency, multi-modality), compose the pipeline from known patterns, layer cross-cutting concerns (safety, cost, resilience, observability, evaluation). Then 5 worked examples and a graduation checklist. Interview Signal and quiz are Pro only | Enterprise RAG: 2 million documents, 50 departments, 10,000 concurrent users, zero cross-tenant leakage; support copilot: 50,000 tickets a day, 60% simple, three tiers | [S] https://scaledojo.dev/genai/learn/capstone-designing-full-genai-systems/how-to-approach-any-genai-system-design ; https://scaledojo.dev/genai/learn/capstone-designing-full-genai-systems/worked-example-enterprise-rag-and-support-copilots |
| **Hamel Husain evals** | Look at real traces, write free-text notes (open coding), group notes into a failure taxonomy (axial coding), count, fix the biggest. Review at least 30 traces yourself, about 100 in total, stop at saturation. Pass/fail, not 1 to 5 scales. One domain expert decides | NurtureBoss (leasing assistant): after dozens of annotated conversations, date handling failed 66% of the time; three issues were over 60% of all problems; after fixes date handling success went from 33% to 95% | [M-self] https://hamel.dev/blog/posts/field-guide/ ; [S] https://hamel.dev/blog/posts/evals-faq/ |
| **Exercism** | Concept exercises (one concept, unlocked by prerequisites, automated feedback) then practice exercises (open problems using those concepts), tests run locally, optional human mentor, then community solutions to compare | Pass the tests, then read several community solutions to the same exercise | [S] https://exercism.org/docs/building/product/concept-exercises ; https://exercism.org/docs/building/tracks/practice-exercises |
| **Codecademy** | Lesson exercises with instructions and hints, "Get Unstuck, Get Code Solution" for the answer, quizzes, then guided projects with no code solution | Exercise, hint, then solution only on request | [S] https://www.codecademy.com/resources/blog/lesson-plan-hour-of-code |
| **CS50** | Problem to solve, demo, background, advice with a pseudocode skeleton and one scaffolded function, how to test (inputs with expected outputs), check50 for correctness, style50 for style | Cash: seven pseudocode comments, then a worked `calculate_quarters()` function, then "stop here and make your program" | [S] https://cs50.harvard.edu/x/2024/psets/1/cash/ |
| **Project Euler, LeetCode** | Euler: the forum thread for a problem opens only after you submit the right answer, then you compare many approaches. LeetCode editorials: several approaches, each with intuition, algorithm, code, complexity | Solve first, compare second, by design | [S] https://en.wikipedia.org/wiki/Project_Euler ; [S] https://dev.to/dfs_with_memo/leetcode-survival-guide-1cp3 (LeetCode pages refused automated fetch) |
| **CFA curriculum** | Learning outcomes with command words (calculate, interpret, evaluate); numbered EXAMPLEs: an exhibit of data, a question with options A/B/C, then "Solution: B is correct", the formula, the numbers substituted, the answer; module ends with a summary and practice problems with solutions | Holding-period return from +14%, -10%, -2%: (1.14)(0.90)(0.98) - 1 = 0.55% | [S] CFA 2025 Level I sample, Learning Module 1 https://content.e-bookshelf.de/media/reading/L-25380709-2218aebaf5.pdf |

Shared pattern: **same headings every time; the worked solution shows each step with its reason; the
learner attempts first where he can; the expert answer is unlocked after, for comparison.**

---

## C. The method for each of the five skills

Common ladder (4C/ID, Renkl and Atkinson): **1 study a worked example → 2 completion problem (last steps
blank) → 3 faded example (more steps blank, backward fading) → 4 independent problem → 5 novel variation
(new surface, same structure)**. The skills differ in where they enter, how fast they climb, and what the
answer is checked against. Every step with a blank asks him to write his step and one line of why before
the expert step is shown (self-explanation, prediction). This is where his own reasoning comes in.

### C1. Evaluation and error analysis (core: logic, understanding, method)
**Method.** Full ladder, slow. Worked examples first (van Gog 2011), because the method has many
interacting steps. Erroneous examples only after 2 correct ones (Große and Renkl 2007).

**Anatomy of one worked example** (after Hamel's field guide, laid out CFA-style):
1. **Goal:** the decision this analysis feeds ("ship the leasing bot to 5 more properties or not").
2. **Givens:** the app, the trace sample (for example 40 traces), what the user wanted, the cost of one failure in money.
3. **Step 1, read and note:** 6 traces shown with the expert's free-text note beside each, and why that note (what the user needed vs what they got).
4. **Step 2, group:** notes grouped into 3 to 5 failure types, with the rule for each group.
5. **Step 3, count:** a pivot table of counts and share; the reason for ranking by count x cost, not count alone.
6. **Step 4, turn one type into a pass/fail check:** the exact criterion, one pass and one fail example.
7. **Step 5, measure the checker:** its agreement with the human labels (true positive and true negative rates), and whether that is good enough to trust.
8. **The check:** does the fix move the number? (NurtureBoss: 33% to 95%.)
9. **Common wrong turns:** using a generic metric before reading traces; 1 to 5 scales; trusting a judge never compared with human labels; stopping at 10 traces.

**Practice ladder.** Worked example → completion (steps 1 to 3 done, he writes steps 4 and 5) → faded (only
step 1 done) → independent on a new set of real traces → novel variation (a different product: RAG, agent,
extraction).
**His reasoning, when:** at every blank step, and fully from step 4 on. He labels before seeing the expert labels.
**Checked against:** the expert's labels and taxonomy (his agreement is computed as a number), then a measured result: did the fix change the failure rate.
**Retention:** a monthly fresh trace set from a different product; failure-type names go into the spaced recall queue.
**Evidence:** worked examples for novices [M] van Gog 2011; comparison with the expert answer is what makes attempts productive [S] Loibl and Rummel 2014; Hamel's steps and numbers [M-self] above.

### C2. How LLMs behave (understanding and memory)
**Method.** Mostly factual and conceptual pieces with few interacting parts, so **generation beats worked
examples** (Chen, Kalyuga, Sweller 2015). Each mechanism is taught as a short "predict, run, explain"
demonstration, then kept by spaced retrieval (Karpicke and Roediger 2008).

**Anatomy of one worked example (a mechanism card):**
1. **Claim:** one sentence ("the same text in Urdu costs more tokens than in English").
2. **Predict:** he writes the direction and a rough size before anything runs.
3. **Demonstration with numbers:** the real run (token counts, or the same prompt at temperature 0 and 1, five times each).
4. **Why:** the mechanism in three to five lines.
5. **Consequence in money or risk:** cost per 1,000 calls, or the rate of a wrong answer.
6. **Where it breaks:** the boundary case (for example, temperature 0 is not guaranteed deterministic).
7. **Recall question:** one line, filed for spaced review.

**Practice ladder.** Short: card → predict-and-run on a new case → explain a surprising output in one line →
use the fact as one link inside an evaluation, design or cost question (retrieval inside new work,
../teaching-methods.md section 4).
**His reasoning, when:** the prediction before every run.
**Checked against:** the measured result of the run, which is the expert answer here.
**Retention:** the recall queue at 1, 3, 7 and 21 days; 3 minutes a day.
**Evidence:** retrieval 80% vs 36% [M]; generation for low-interactivity material [M]; prediction [S, see ../teaching-methods.md 1d].

### C3. System design (building his own reasoning)
**Method.** Whole tasks in one fixed frame (4C/ID). Inside each task class: the first 2 designs are worked
examples; after that, **he designs first, then compares with the expert design section by section** (Kapur
2014 with Loibl and Rummel 2014 consolidation; Project Euler and Hello Interview do the same). This is the
answer to his note that the old system suppressed his thinking: from the third problem on, his design comes
before any expert design. It is also the answer to the failed open investigation: the frame fixes the
steps, and an expert design always exists to compare against.

**Anatomy of one worked example** (Hello Interview headings plus ScaleDojo's GenAI steps):
1. **Brief with numbers:** users, requests a day, latency target, budget, what must never happen.
2. **Requirements:** functional and non-functional, each with its number.
3. **Capabilities:** generation, retrieval, agency, multi-modality: which ones, and why.
4. **Pipeline:** components in order, each with the one reason it is there.
5. **Estimate:** back-of-envelope cost and latency (ByteByteGo style arithmetic).
6. **Deep dive:** one hard decision shown as Bad, Good, Great, each with its deciding number.
7. **Cross-cutting layer:** safety, cost, resilience, observability, evaluation: one line each.
8. **The check:** does the design meet each number in the brief?
9. **Common wrong turns:** adding complexity before a simple design works; agents where a fixed workflow does; no evaluation plan; tenant data leaks.
10. **Level note:** what a mid, senior, staff answer adds (Hello Interview).

**Practice ladder.** 2 worked examples → completion (he writes the deep dive only) → his full design, then
side-by-side comparison with the expert's → the same brief with one number changed (10x users, half the
budget: what moves?) → a new domain (novel variation). Then a harder task class and the ladder restarts
(the 4C/ID saw-tooth).
**His reasoning, when:** every design from the third on, written before any reveal; after the comparison he writes one line per section, "mine vs expert: why they differ, which is better for this brief".
**Checked against:** the expert design (Hello Interview, ScaleDojo, ByteByteGo), the 100-point rubric in teaching-structure.md, and the brief's numbers.
**Retention:** one old brief a fortnight redone cold, with one number changed (interleaved with new ones).
**Evidence:** solve-first gives better conceptual knowledge and transfer [M] Kapur 2014; only with comparison to the canonical solution [S] Loibl and Rummel 2014; comparing designs side by side [M] Rittle-Johnson and Star 2007; worked examples first for novices [M] van Gog 2011.

### C4. Production (maths and quality control, applied)
**Method.** He is strong at numbers (about 88% first try, ../teaching-methods.md), so fade fast
(expertise reversal). CFA-style worked numeric solutions for each new formula; drill (part-task practice)
only for formulas he misses; the real skill is which lever moves the decision, taught through "what flips
it" variations.

**Anatomy of one worked example** (CFA example layout plus Google SRE error-budget worked numbers):
1. **Exhibit:** the data table (requests a day, error rate, price per 1,000 tokens, cache hit rate).
2. **Question:** one decision ("does the cache pay for itself?").
3. **Formula:** named, with each term defined.
4. **Substitution:** numbers in, one line per step, units shown.
5. **Answer and meaning:** the number, then what it means for the decision.
6. **Sensitivity:** which input, if 20% wrong, flips the decision, and in which direction.
7. **Common wrong turns:** mixing per-call and per-day units; ignoring retries; averaging percentages.
Example of the style: SRE book, 2.5 million requests a day at a 99.99% target allows 250 errors; a problem that fails 0.0002% of queries spends 20% of a 99.999% quarterly budget [S] https://sre.google/sre-book/embracing-risk/

**Practice ladder.** Worked example → completion (formula given, he substitutes) → independent → "what
flips it" variation → a monitoring case: a dashboard where one number drifts, he says which lever and why.
**His reasoning, when:** the sensitivity and lever questions; the arithmetic itself is checked, not taught.
**Checked against:** the exact numeric answer, then the expert's lever choice.
**Retention:** interleave cost, latency and error-budget problems in one set (interleaving d = 0.79 to 0.83 [M]).
**Evidence:** CFA and SRE formats [S]; first-step test to skip examples he does not need [M] Kalyuga and Sweller; interleaving [M] Rohrer.

### C5. Code (understand, steer, read and judge, debug, small edits)
**Method.** Follow the known skill order: reading and tracing before explaining, explaining before writing
[S] Lopez et al. 2008 https://dl.acm.org/doi/10.1145/1584322.1584336 ; teaching tracing, syntax and
templates explicitly raised completion and cut errors [S] Xie et al. 2019
https://www.benjixie.com/publication/cse-2019/ . Steering an AI coding assistant is a separate skill with
its own practice: the prompt problem (write a prompt that makes the model produce code passing given
tests) [S, n = 54 field study] https://arxiv.org/abs/2307.16364 .

**Anatomy of one worked example** (subgoal-labelled code walkthrough):
1. **Goal:** what the code must do, in one line, with one input and expected output.
2. **Code** with subgoal labels as comments grouping lines (load, clean, compute, return).
3. **Trace table:** variable values after each key line for the sample input.
4. **Why each block:** one line per subgoal.
5. **The check:** the test that proves it works, and its output.
6. **Common wrong turns:** off-by-one, silent None, wrong join producing duplicate rows.
7. **Steer version:** the spec he would give an AI assistant to produce this code: goal, inputs, outputs, constraints, and the test it must pass.

**Practice ladder.** Worked example → predict the output before running → completion (fill 1 to 3 lines, or a
Parsons problem: put given lines in order; as good as writing on a one-week test, in less time [M]
https://dl.acm.org/doi/10.1145/3141880.3141895) → find the bug (after 2 correct examples) using a fixed
debugging process (hypothesis, test, narrow down; explicit teaching raised debugging performance [M, n = 28]
https://computingeducation.de/pub/2019_Michaeli-Romeike_WIPSCE19.pdf) → small edit → prompt problem → review
an AI-written diff against its tests.
**Steering routine** (Anthropic's stated practice): explore, plan, code, commit, and give the assistant a way
to verify its work, tests first [S] https://code.claude.com/docs/en/best-practices
**His reasoning, when:** the prediction before each run, the hypothesis before each debug step, the spec before each AI request.
**Checked against:** tests passing (measured), then the expert or community solution (Exercism, CS50).
**Retention:** one small read-and-trace a day inside other tracks (evaluation scripts, cost scripts).
**Evidence on AI help:** novices with Codex completed 1.15x more tasks and scored 1.8x higher, with no loss on
manual edit tasks and no significant difference a week later [M] https://arxiv.org/abs/2302.07427 ; but
struggling novices had their metacognitive problems made worse by AI help [S]
https://arxiv.org/abs/2405.17739 . Hence: he predicts and specifies before the AI writes.

---

## D. Weekly structure and the rule for fading

### D1. The week (5 units of 20 to 25 minutes, as in curriculum-map.md, plus 3 minutes daily)
| Day | Unit | Why here |
|---|---|---|
| Daily | 3-minute recall: LLM-behaviour cards and missed items at 1, 3, 7, 21 days | Retrieval and spacing [M] |
| Mon | Evaluation (C1) | Core; needs a fresh head |
| Tue | Code (C5) | Core; practice every other weekday |
| Wed | System design (C3) | Core; builds on Monday's evaluation plan |
| Thu | Code (C5) + one LLM-behaviour predict-and-run (C2) | Code twice a week because it is a hierarchy that decays |
| Fri | Production (C4), mixed set | Interleaved cost, latency, error budget |
| Sat (optional) | Mixed review: one old item from each track, cold | Interleaving [M]; spacing |
Core share: evaluation, design and code are about 70% of the time, matching his "core" labels.
The module capstone (curriculum-map.md) replaces one week's units every 4 to 6 weeks.

### D2. Moving from worked examples to independent work
1. **Start of each unit, a first-step test:** one new problem, 90 seconds, he writes only his first step (Kalyuga and Sweller [M]).
2. **Placement:** first step right and reason right, twice in a row → skip the worked example, go to the faded or independent step. Wrong → full worked example.
3. **Climbing:** move up one rung (worked → completion → faded → independent → variation) after 2 correct in a row with a correct one-line reason (Math Academy's "enough correct" rule [S]; adaptive fading [M] Salden 2010).
4. **Falling back:** 2 misses in a row at one rung → back one rung, and review the prerequisite that step uses (Math Academy's fail-twice rule [S]).
5. **New task class:** harder problems restart at a worked example (4C/ID saw-tooth [S]).
6. **Retire the worked example** once he passes a novel variation cold; from then on the skill appears only in mixed reviews and inside other tracks (expertise reversal [S]).
Speed differs by track: C4 fades fastest (strong at numbers), C3 slowest (judgement, non-recurrent), C2 barely uses worked examples at all.

---

## E. What not to do, per skill
| Skill | Do not | Why |
|---|---|---|
| All | Use one format for all five | His own record; the kinds of knowledge differ (A3) |
| All | Give open tasks with no expert answer to compare | Productive failure fails without canonical comparison [S] Loibl and Rummel 2014; minimal guidance underperforms for novices [M, review] https://www.tandfonline.com/doi/abs/10.1207/s15326985ep4102_1 |
| All | Keep full worked examples after he has passed a novel variation | Expertise reversal [S] |
| C1 Evaluation | Start with generic metrics or a judge before reading traces; use 1 to 5 scales; show wrong examples before two right ones | Hamel FAQ [S]; Große and Renkl [M] |
| C2 LLM behaviour | Teach facts with long worked examples; explain before he predicts; test once and never again | Generation beats examples for simple material [M]; retrieval 80% vs 36% [M] |
| C3 System design | Show the expert design before his attempt (after the first two); let him attempt a new task class cold; add complexity before a working simple design | Kapur, van Gog [M]; Hello Interview [S] |
| C4 Production | Drill arithmetic he already gets right; teach formulas without the decision they serve; block problems by type | Bjork, via ../teaching-methods.md; interleaving [M] |
| C5 Code | Let the AI write code before he predicts or specifies; ask him to write from scratch before he can trace; judge by "looks right" instead of tests | Prather 2024 [S]; Lopez 2008 [S]; Anthropic best practices [S] |

## Gaps
- Salden 2010's exact fading criterion and effect sizes were not read (full text refused connection); the D2 thresholds (2 in a row) follow Math Academy's stated practice, not a tested optimum.
- Rittle-Johnson and Star 2007 result is from the abstract, not the full paper.
- No study found that tests worked examples for LLM system design or evals specifically; the methods are carried over from maths, physics and programming research.
- ScaleDojo Interview Signal and quizzes are behind the Pro paywall; LeetCode editorial pages refused automated fetch.
