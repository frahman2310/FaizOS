# Production: the learning structure for "small maths + quality control, applied"

> **Amended 2026-09-24:** the independent review (`review.md`) kept this structure with changes. Where this file disagrees with `INTEGRATED.md` (plain step names, shared recall queue, one mastery rule, start order, the week), `INTEGRATED.md` wins.
>
> **Amended 2026-09-25** (`docs/research/review-rebuild-llm-production.md` M8, `gap-audit-production.md` 1.2, 1.3, 1.7, 1.10, 1.11, 1.13, 6.1 to 6.3): every section that contradicted the corrected section 2 is rewritten or struck. There is no speed grade, no timer, no readiness score, no factor-2 or 90%-range grade, and no interleaving before a class has had its first unit. Bars are INTEGRATED section 3 and `learn/engine.py`: **90 on the scored steps, the Retry and the 7-day Cold**, each a set of 10 with at least 3 items about what a number means.


Written 2026-09-24. The skill: cost per call and per user, capacity and latency estimates, error budgets
and SLOs, caching economics, monitoring and drift, and choosing which lever moves a number.
Builds on, does not repeat: `../recommended-method.md` (the 10-step unit, the four proven parts),
`../postmortem.md`, `../curricula/skill-methods.md` C4 (CFA-style example anatomy),
`../curricula/method-effectiveness.md` (component grades), `../curricula/teaching-craft.md`,
`../curricula/curriculum-design.md` (nodes P1 to P7, levels). Materials: `private/research-base/
production-and-llm-behaviour/production/` (called "saved sources" below; file names given).

Tags: **[M]** measured, **[M-cor]** measured but correlational only, **[M-self]** a number a company
reports about itself, **[S]** stated, no numbers. Every number in sections 4 and 5 was produced by running
Python on figures from the saved sources (2026-09-24).

---

## 1. What kind of learning this is, and what the new experts add

### 1a. The kind
Four parts, and only one of them is arithmetic:

| Part | Kind (4C/ID terms) | What goes wrong for a strong-at-numbers learner |
|---|---|---|
| Compute a known formula | recurrent, compiles fast | nothing much; he is at about 88% first try already |
| Pick the right numbers and units from a messy exhibit | recurrent but error-prone | per-call vs per-day, per-token vs per-million, averaging percentages |
| Estimate before computing | recurrent, trainable | never practised if the tutor's code produces every number |
| Read a moving number and choose the lever | non-recurrent judgement | reacting to noise; pulling the lever with the smallest share |

### 1b. What the new experts add (and what it changes in the earlier plan)

| Expert or field | What they do | Evidence | What it changes |
|---|---|---|---|
| **Yale SOM breakeven primer** (Thomas and Wasserstein 2024, case-method teaching) | Says outright that students struggle not with the maths ("basic arithmetic") but with "fishing for the correct numbers" and what to do with the answer. Teaches by reworking one case with one input swapped: $1M fixed / $3M variable gives breakeven revenue $2.5M; swap to $3M / $1M and it jumps to $3.75M | [S] https://som.yale.edu/sites/default/files/2025-04/A%20Primer%20on%20Breakeven%20Analysis.pdf | **Challenge to skill-methods.md C4:** a CFA-style worked example spends most lines on substitution, which he does not need. Here the worked part is *which numbers from the exhibit and why*, and *what the answer means*. The substitution line is run by code |
| **CFA prep (CFA Institute, Kaplan Schweser)** | Learning outcome statements with command words (calculate, interpret, evaluate); inline examples; end-of-module practice problems with solutions; then "thousands" of QBank items, then 4 to 6 timed mocks. Exam pace: 180 items in 270 minutes, 90 seconds each | LOS [S] CFA 2025 sample (skill-methods.md B); pace [S] https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-i-exam ; "95% of Level II candidates who scored 70% or higher on mock exams" passed [M-self] https://www.schweser.com/cfa/level-2/study-packages | Kept: explained solutions after every scored item. Not used (2026-09-25): item volume as the centre, speed as part of mastery, a mock score as a readiness gate (worked examples come first, section 2) |
| **Actuarial prep (Coaching Actuaries)** | Adaptive practice exams; "Earned Level" 0 to 10 rises when a score beats a high threshold, falls below a low one, holds between; only full adaptive exams count, not quizzes | Mechanism [S] https://support.coachingactuaries.com/article/227/what-is-an-earned-level . 2024 survey, Exam FM: 95.7% pass at EL 5.5+, 68.6% below [M-self, self-selected survey, no sample size] https://www.coachingactuaries.com/blog/insights/exam-p-and-fm-2024-survey-insights-pass-rates-ratings-and-key-takeaways . Exam P: 30 items in 3 hours, adaptive, scaled 0 to 10 [S] https://analystprep.com/actuarial-exams/soa/exam-p-probability/ | Not used (2026-09-25): the readiness number and its dead band. Mastery is INTEGRATED's one rule (90 on 2 units in a row, then 90 cold) |
| **Question-bank evidence (medicine)** | Board candidates work thousands of bank items | Step 1 score vs items done r = 0.53; practice-test score vs Step 1 r = 0.65; N = 47, 46% response [M-cor] https://pmc.ncbi.nlm.nih.gov/articles/PMC8368851/ | Volume and mock scores **predict**; they are not shown to **cause**. Use mock score as a measure, keep retrieval (grade A) as the reason for the bank |
| **Sanjoy Mahajan** (Street-Fighting Mathematics; The Art of Insight) | Divide and conquer into an estimation tree; estimate leaves by gut with a range and take the geometric mean; "reliability comes from intelligent redundancy": two unrelated methods for the same number; easy cases (check a formula at its extremes). Tutor questions interspersed and answered in the next paragraph; "merely watching workout videos produces little fitness" | [S] https://ocw.mit.edu/courses/res-6-011-the-art-of-insight-in-science-and-engineering-mastering-complexity-fall-2014/3bca850386a3005c22134fa62fb3bad5_MITRES_6-011F14_art_insfin.pdf ; tools list [S] https://mitpress.mit.edu/9780262514293/street-fighting-mathematics/ | A **rough size first**, modelled in each worked example and only then asked of him (gap-audit 1.1); never before teaching. Trees with ranges only in a later, taught estimation class |
| **Fermi and order-of-magnitude teaching** | Redish: an estimation problem in every homework and every exam; most credit for the reasoning, not the answer; acceptable range "typically a factor of two or more". Weinstein: within a factor of 10 is enough to decide most things | Redish [S] https://arxiv.org/abs/2011.12699 ; Weinstein [S] https://plus.maths.org/guesstimation . Worked examples for order-of-magnitude reasoning vs conventional tasks, same teacher, N = 118 complete sets: d = 0.61 and d = 0.59, near and far transfer [M, quasi-experiment] https://arxiv.org/abs/2405.16480 ; a systematic review found almost no prior evidence that estimation is teachable (same paper) | Estimation is **a thread in every unit, not a topic**: worked, then practised. Not graded on a factor-2 band (2026-09-25) |
| **Back-of-envelope in engineering** (Jeff Dean, ByteByteGo, Google NALSD) | A short list of anchor numbers; QPS, peak, storage, servers from them. Google SRE: turn a whiteboard design into resource numbers; AdWords example: 500,000 queries/s, 86.4 TB/day of logs rounded to 100 TB | [S] https://brenocon.com/dean_perf.html ; [S] https://bytebytego.com/courses/system-design-interview/back-of-the-envelope-estimation ; [S] https://sre.google/workbook/non-abstract-design/ | A small **anchor card** for LLM work goes into spaced recall (below). Round early, as NALSD does |
| **Hubbard calibration training** | Stated-confidence ranges on trivia with feedback, "equivalent bet", start from absurd bounds to fight anchoring; about 3 hours trains most people | [M-self] http://www.hubbardresearch.com/wp-content/uploads/2019/06/Introduction-to-Calibrating-Probability-Assessments-Hubbard-Decision-Research.pdf | Not used until a taught calibration segment exists; then a trial measure only, never scored |
| **Deming red bead, SPC** | 20% red beads, paddle of 50: counts run 1 to 19 around 10 from the system alone; np-chart limits "close to 1 and 19". Lesson: blaming workers for common-cause variation changes nothing; change the process | [S] https://www.spcforexcel.com/knowledge/variation/red-bead-experiment/ ; [S] https://deming.org/lessons-from-the-red-bead-experiment-with-dr-deming/ . Western Electric rules (beyond 3 sigma; 2 of 3 beyond 2 sigma; 4 of 5 beyond 1 sigma; 8 in a row one side) [S] https://www.qualitygurus.com/nelson-rules-and-western-electric-rules-for-control-charts/ | **New problem class: "is this a signal?"** before "which lever?". The simulated red bead (run in code) is the opening demo |
| **Six Sigma Green Belt** | Two blocks of about four class days a month apart, a real improvement project between them, DMAIC tollgate review at the end of each phase | [S] https://www.6sigma.us/course/green-belt-training/ ; [S] https://sixsigmastudyguide.com/dmaic-tollgate-reviews/ | The **mock incident** follows DMAIC in miniature (define the number, measure baseline, analyse shares, improve one lever, control with an alert). Belt certification itself is excluded (section 8) |
| **Google SRE workbook** | Every alerting option judged on precision, recall, detection time, reset time; burn-rate table; worked budget spends (a 4-hour bad release used 13% of budget, a 20-hour restore 65%) | [S, saved: sre-workbook-05, sre-workbook-02] | The error-budget class is taught as "how much budget did this spend, and do we page" |

**What this table changes (corrected 2026-09-25).** The centre is a worked example per knowledge point, then
guided practice, then a scored set of 10 with explained solutions (section 2). Worked examples show which
numbers and why, one substitution line per term, and what the answer means; the "what it means" step is never
faded until he passes it cold. His own estimate comes only after a worked one. No timer, no pace.

---

## 2. THE STRUCTURE: the unit (corrected 2026-09-25)

**Corrected 2026-09-25** after C49 and `docs/research/gap-audit-production.md` (findings 1.1, 1.3 to 1.10, 5.4).
The earlier "Estimate, Compute, Decide" unit opened with an untaught estimate under a timer and kept the worked
solution as a side note; that is replaced below. Format: unit format v3 (`learn/check_unit.py`): each step's
Key has `Kind: show | try | scored | close`; show steps list at most 3 `New:` ideas; nothing is scored before
at least one show and one try. The first full unit built to this template is
`learn/units/production/01-what-one-call-costs.md`.

### 2a. First contact with a problem class (the first unit of each class; about 35 to 40 minutes)

| # | Step | Kind | Content rule | Source |
|---|---|---|---|---|
| 1 | **The job** | show | The problem in 4 or more plain sentences with a real money stake; every term explained where it first appears; "You will be able to ..."; "You are done when ..." (9 of 10 now and 7 days later). Ends with one check on the words just taught, never a guess. | C34, C41; teaching-structure.md:149-150; teaching-craft T1 |
| 2 | **Worked example 1** (knowledge point 1) | show | One everyday picture with where it stops; which numbers from the exhibit and why; the formula in plain words; **a rough size first**, then one substitution line per term with units; code only where the unit uses code again (none in C1: review m9), always with a **How this code works** block; what the answer means; one wrong turn, labelled wrong before it is shown; one self-explanation question on the key step. | B1, B2; Yale primer; CFA layout (skill-methods.md:170-178); Mahajan's modelled estimate; Loretan et al. (worked estimation); C48 |
| 3 | **Your turn 1** | try | Same shape, new surface. Completion: the first link done, he does the rest. 2 to 4 short questions, aimed at about 80% right first try; any direction question as two options. | completion problems; Renkl and Atkinson; B9; E12 |
| 4 | **Worked example 2** (knowledge point 2) | show | As step 2, one new idea (for C1: calls a month and the share of the bill). | Math Academy knowledge points (teaching-craft.md:115) |
| 5 | **Your turn 2** | try | As step 3. The first **rough guess** he is asked for comes here, after he has seen a worked rough estimate, as one number. | gap-audit 1.1 |
| 6 | **Worked example 3: what the number means** | show | A saving as before minus after, written as a subtraction, the one-side slip labelled wrong; the biggest share is where to cut first; which way an unsure input bends the bill (higher or lower). Never faded until he passes it cold. | E11, E12; review.md:108, :206; INTEGRATED.md section 6 |
| 7 | **Your turn 3** | try | 2 or 3 meaning items; direction as two options. | E12 (0/3 open, 3/3 as two options) |
| 8 | **Lever** | try | The table first (each option: cost after, saving per call and per month, what it risks), computed; then one pick of two with the deciding number. He never names a lever or its size before seeing the table. | contrasting cases (grade B, section 8a); Schwartz and Bransford 1998 |
| 9 | **Quick set 1** | scored | Before it, his score prediction (`engine.py predict`). 5 short-answer items on new surfaces, this class only (interleaving starts from the second class); 1 or 2 about what a number means. | Kulik bar; Adesope short answer first |
| 10 | **Quick set 2** | scored | Opens with the worked solutions to items 1 to 5 (inside the step, so the guard sends them verbatim), then 5 more items, 2 or more about meaning. Both halves together: **10 items, at least 3 about meaning, pass 9 of 10** (INTEGRATED section 3). | elaborated feedback d = 0.99 vs 0.24 |
| 11 | **Close** | close | Opens with the solutions to items 6 to 10; then his line "Next time I see X, I first ...". | INTEGRATED 1 |

Prepared blocks outside the order (the checker requires at least one Help block, a Retry and a Cold; production
units write a Help block for every try and scored step):
- **`## Help: <step>`**: a second worked example on a new surface, taught differently (for example, a case where
  output, not input, is the biggest share), ending on the same question shape. Sent as move 3 of the stuck order,
  then the step itself is sent again, whole; and before a Retry.
- Every try and scored step's Key has a prepared **`Two options:`** line (move 2) and **`Worked answer:`** line
  (move 4) (checker). On a scored step a right answer after Two options scores 0.5, after the Worked answer 0.
- **`## Retry`** and **`## Retry 2`**: 10 new items in two messages of 5, at least 3 about meaning, pass 9 of 10,
  after a miss and its Help blocks; recorded once as `Retry=<right/10>`.
- **`## Cold`** and **`## Cold 2`** (7 days later): the same shape; recorded once as `Cold=<right/10>`.
- **Cards**: every number card carries 4 surfaces (`||`), so a review never repeats the numbers.
- Every Score line states rounding: a share to 1 decimal place or the nearest whole percent; a bill to the cent.

Target first-try rate on the try steps: about 80%, recorded with `engine.py tries <unit> <right> <total>` after
the last try step. Under 70% is the overload alarm: use the Help blocks, and rebuild the unit before the next unit
of that class (gap-audit 4.4).

### 2b. Later units of a class (second unit onward)

1. **First step** (try): one new item, he writes only his first move and why; recorded, not scored. Right twice
   in a row across units: Worked examples 1 and 2 may be skipped (Kalyuga and Sweller's first-step test).
2. **Guess** (try): one rough number, only because a worked estimate in this class has been seen. A 90% range
   comes only after a taught calibration segment (Hubbard) and is a trial measure, never scored.
3. **Chain** (try): his full chain in words and units; the expert chain is shown only after he finishes, with
   feedback on the first wrong link (gap-audit 1.5).
4. **Run** (show): code computes his chain, with its How this code works block; he says in one line why his
   guess was off, if it was.
5. **Worked example 3: meaning** (show, kept until passed cold), then **Your turn 3** (try).
6. **Lever** (try, table first), **Quick set 1 and 2** (scored, 10 items interleaved across *taught* classes,
   3 or more about meaning), **Close**.

### 2c. Delivery rules for every step
- One step per message, at most 2,600 characters including code (checker); at most 3 new ideas per show step.
- Plain words; every term explained in the sentence where it first appears (glossary check).
- Every number from a `calc.py` run or a verified `facts.md` row; made-up scenario numbers on a line starting
  "Suppose"; never "given:" in text he reads. Prices from `facts.md` (Sonnet 5 and Haiku 4.5 unless the item is
  about switching models).
- No timer and no speed grade in any unit (gap-audit 1.10; corrected 2026-09-25).
- Stuck order: his own earlier number or the show step it uses; two options; the step's Help block; the answer
  worked line by line, which he says back.

**Every fourth production unit is a mock incident** (45 minutes, section 4e) instead, once classes C1 to C6 have
each had their first-contact unit.

### Why this differs from the other four skills
| Skill | Its centre | Production's centre instead |
|---|---|---|
| Evaluation | labelling real traces, agreement with expert labels | a number, checked exactly by code |
| System design | commit a whole design, compare section by section | many small items; judgement only at the lever step |
| Code | read, trace, predict output | the chain is written in words and units, code only computes |
| LLM behaviour | predict, run, explain one mechanism | predict a *size* (range) and a *lever*, not a behaviour |
| Production | **choose the numbers, compute, say what the number means, then pick the lever** | at least 3 of every 10 scored items are about what a number means (E11, E12) |

---

## 3. Progression

### 3a. Problem classes (each restarts at one worked solution)
| Class | Node (curriculum-design.md) | Typical item | Main saved source |
|---|---|---|---|
| **C1 One-formula cost** | P1 | cost per call from tokens and price; per user per month | anthropic-pricing, huyen-building-llm-applications |
| **C2 Latency and capacity** | P2, P5 | latency = TTFT + TPOT x output tokens; GPUs to hold a model; throughput vs batch | databricks, kipply, hf-blog-optimizing, anyscale-numbers |
| **C3 Error budget and burn rate** | P3, P6 | allowed errors; share of budget an outage spent; burn rate and page or not | sre-book-03, sre-workbook-02, sre-workbook-05, appendix-a |
| **C4 Caching economics** | P4 | break-even hit rate; monthly saving; what breaks the prefix | anthropic-prompt-caching, openai-prompt-caching |
| **C5 Signal or noise** | P6 | control limits on a daily rate; which Western Electric rule fires | Deming/SPC sources above, sre-book-06 |
| **C6 Sensitivity and lever choice** | P7 | which input dominates; which lever, by how much, at what cost | openai-latency-optimization, sre-book-21/22 (retries, queues) |
| **C7 Live dashboard drift** | P6, P7 | a number moves over days; decide signal, cause, lever, alert | all of the above, as a mock incident |

### 3b. Levels and milestones
| Level | Classes unlocked | Milestone (observed, not self-reported) |
|---|---|---|
| **P-1 Computes** | C1, C2 | 9 of 10 on the scored set of the C1 and C2 units, then 9 of 10 cold |
| **P-2 Budgets** | + C3, C4 | 9 of 10 on a set mixing C1 to C4; break-even hit rate and burn-rate page decision right without the formula shown |
| **P-3 Reads variation** | + C5, C6 | 9 of 10 on a set of chart items (signal or noise, the rule named) and lever items |
| **P-4 Runs production** | + C7 | mock incident 9 of 10 (`engine.py outside production`, the production bar); outside task: the cost and latency budget for his FBR tax assistant within 20% of measured (curriculum-design.md 6a) |

Support fades inside a class and resets at the next (4C/ID); the "what it means" step never fades until passed
cold. Promotion is INTEGRATED's one mastery rule: the bar (90) on the scored steps of 2 units in a row, then the
same bar cold at 7 days.

---

## 4. Practice formats, one concrete example each

Design sketches, not unit material (corrected 2026-09-25). 4b to 4e were computed on 2026-09-24 at Sonnet 4.6
prices; a unit recomputes every number with `learn/calc.py` from `learn/facts.md`, on Sonnet 5 ($2 / $10) and
Haiku 4.5 ($1 / $5) unless the item is about switching models (gap-audit 6.3).

### 4a. Exhibit-based problem (C1)
Built: `learn/units/production/01-what-one-call-costs.md`, Worked examples 1 and 2 (study helper on Sonnet 5:
$0.017 a call, $10.20 per student a month; instructions 70.6%, answer 23.5%, question 5.9% of a call).
**Wrong turns.** Pricing the answer at the input rate; per-million read as per-thousand.

### 4b. Fermi estimate, then check (C2)
**Question.** A 7B model in 16-bit on a card with 2 TB/s memory bandwidth. Estimate time per output token.
**Tree.** Each token reads all weights once: 7B x 2 bytes = 14 GB; 14 GB / 2 TB/s = **7 ms** floor.
**Check.** Databricks measured TPOT 14 ms for this case (50% bandwidth use). Ratio 2.0: **inside the factor-2 band**.
**Second method (Mahajan's redundancy).** Llama2-70B in 16-bit = 140 GB = 3.5 A100-40GB, so at least 4;
Databricks: "needs at least 4xA100-40B GPUs to fit". Two unrelated checks agree.
**Then latency:** TTFT 46 ms + 14 ms x 400 tokens = **5.6 s**; halve the answer to 200 tokens: **2.8 s**.

### 4c. Sensitivity table (C4 + C6)
Same exhibit as 4a. Cached prefix is read at 0.1x and written at 1.25x of the input price.
| Hit rate on the 6,000-token prefix | Cost per call | Saving vs no cache |
|---|---|---|
| 0.1 | $0.02793 | -9.5% (caching loses money) |
| 0.2 | $0.02586 | -1.4% |
| 0.5 | $0.01965 | 22.9% |
| 0.8 | $0.01344 | 47.3% |
| 0.95 | $0.01034 | 59.5% |
**Break-even hit rate** = (1.25 - 1) / (1.25 - 0.1) = **21.7%**. **Flip question:** calls from one user
come 20 a day, often more than 5 minutes apart; is the hit rate above 21.7%? That, not the price, decides.
**+20% on each input:** prefix +14.1% cost, answer +4.7%, user message +1.2%. The lever is the prefix.

### 4d. Control-chart reading (C5)
**Opening demo (red bead, run in code).** 20% red, paddle of 50: centre 10, limits **1.5 to 18.5**.
Every count inside is the system, not the worker.
**Item.** An LLM judge fails 5% of 400 traces a day on average. Limits: 5% plus or minus 3 x 1.09% =
**1.73% to 8.27%**. Tuesday 7.5%: inside, no action. Eight days in a row at 5.5 to 6.5%: all inside the
3-sigma limits, but the "8 in a row on one side" rule fires: a **shift**, find what changed (a prompt
edit, a model version).
**Wrong turn.** Treating the 7.5% day as an incident and the 8-day creep as nothing.

### 4e. Mock incident (C7, DMAIC in miniature, 45 minutes)
**Dashboard over 10 days** (numbers from 4a and 4c): cost per call rises from $0.0114 to $0.0279 after a
deploy on day 6; cache hit rate falls from 90% to 10%; error rate 1.44% for the last hour on a 99.9%
30-day SLO.
| DMAIC step | His task | Key |
|---|---|---|
| Define | which number matters first | the error rate: burn rate 1.44% / 0.1% = **14.4**, 2% of the month's budget in 1 hour, which is the SRE workbook's page threshold |
| Measure | budget left if it continues | 30 / 14.4 = **2.1 days** to exhaustion |
| Analyse | is the cost jump a signal; cause | step change at a deploy, hit rate 90% to 10%; something now changes the prompt prefix (a timestamp at the top is a classic, per anthropic-prompt-caching.md) |
| Improve | lever and its size | move the changing part below the cache breakpoint; cost per call 2.46 times higher, brought back to baseline; at 5,000 users, **$83,790 back to $34,110 a month** |
| Control | the alert that would have caught it | alert on hit rate below the 21.7% break-even and on 14.4x burn over 1 hour and 5 minutes |
Scored on 10 points: 2 per step, one for the number, one for the reason. Pass 9 (the production bar, INTEGRATED 3).

### 4f. Question-bank set (interleaved across classes already taught, untimed)
| # | Item | Key | Source |
|---|---|---|---|
| 1 | 99.9% over 30 days: minutes of full outage allowed? | 43.2 | appendix-a |
| 2 | 0.5% errors on a 99.9% SLO: burn rate, days to empty? | 5; 6 days | sre-workbook-05 |
| 3 | 3 retries at each of 3 layers: attempts on the database per user action? | 4^3 = 64 | sre-book-22 |
| 4 | Queue 10x the thread count, 100 ms per request: added latency? | about 1 s | sre-book-22 |
| 5 | 97% SLO, budget 109,897 errors; a bad release caused 14,066: share? | 12.8% (book: 13%) | sre-workbook-02 |
| 6 | 10k input + 200 output tokens at $0.06 / $0.12 per 1K: cost per call? | $0.624 | huyen |
| 7 | Cut the prompt 50%: latency effect? Cut the answer 50%? | 1 to 5%; about 50% | openai-latency-optimization |
Short answer first; two options only as the stuck-order hint (scores 0.5) (Adesope rule, method-effectiveness.md 1b).
No pace targets (struck 2026-09-25).

---

## 5. Assessment, mastery and retention (rewritten 2026-09-25)

Bars are INTEGRATED section 3 and `learn/engine.py` (`BAR["production"] = 90`).

| What | Threshold | Why this number |
|---|---|---|
| Scored steps of a unit | 90: 9 of 10 (Quick set 1 and 2), at least 3 items about what a number means; 2 units in a row | INTEGRATED 3 and 2.5; mastery bar 91 to 100% (Kulik, grade B) |
| 7-day Cold | the same bar, 90: 9 of 10 new items, 3 or more about meaning | INTEGRATED 2.5 |
| Retry after a miss | 90: 9 of 10 new items, after the Help blocks; a second miss moves to a parallel unit | Bloom and Guskey mastery learning |
| Try steps, first try | about 80%; under 70% is the overload alarm (not a bar) | Rosenshine |
| Mock incident | 9 of 10 (the production bar), for P-4 | INTEGRATED 3 |

Struck (they contradicted section 2 or INTEGRATED): speed thresholds, the factor-2 estimate grade, the 90%-range
calibration grade, the lever-match grade of 4 of 5, the signal-or-noise grade of 4 of 5 (now inside the 9 of 10
set), the 0 to 10 readiness score, and "twice, 7 days apart" (now: 2 units in a row, then cold).

**Retention plan.**
- One shared recall queue (INTEGRATED 2.1, FSRS). Number items return as a new exhibit with new numbers, never
  the same item (each number card carries 4 surfaces).
- **Interleaving** starts only after a class has had its first-contact unit: the first unit of a class is
  blocked; later scored sets mix classes already taught, because choosing the formula is the skill
  (d = 0.79 to 0.83). Never from the first week (gap-audit 1.7).
- Confusable pairs are taught days apart, mixed later: availability (time) vs aggregate (requests);
  error rate vs burn rate; TTFT vs TPOT; cache write vs read multiplier.
- **Anchor card** (spaced recall, added only after the unit that teaches each line; wording from `learn/facts.md`,
  model named): Anthropic's rule of thumb, about 0.75 words per token in English, for Sonnet 4.6 and earlier;
  Claude 4.7 and later (Sonnet 5) make about 30% more tokens for the same text; 2 bytes per parameter in 16-bit;
  output latency scales with output tokens, input barely; cache read 0.1x base on most models (0.05x on Opus
  5.5, 0.025x on Fable 5.1), write 1.25x for 5 minutes and 2x for 1 hour; 99.9% = 43.2 min a month; 14.4x
  burn = page.
- One production item a week appears inside another skill's unit (a design's cost line, an eval's
  sample size), which is retrieval inside new work.

---

## 6. Weekly dose and session length

| Slot | Length | Content |
|---|---|---|
| Production unit, when `engine.py today` lists it (sittings, not weekdays: C47) | 35 to 40 min | the unit in section 2 |
| Daily recall | about 1 min of the 3-minute block | 1 production item or anchor |
| Inside other skills | about 5 min a week | one cost or latency line in a design or eval |
| Every 4th production unit, once C1 to C6 have had their first unit | 45 min | mock incident |
| **Total** | **about 35 to 40 min a week** | about 15% of study time; the core three keep 70% |

Volume: about 12 bank items a week (3 per unit + recall + inside work), so about 150 over 12 weeks
across 7 classes. That is far below board-exam volumes, on purpose: the item pool is small and he is
already accurate. A class that misses the bar gets its Help blocks and Retry, then a parallel unit (INTEGRATED 2.5).

---

## 7. Measures that show it is working (rewritten 2026-09-25; INTEGRATED section 7 wins)

| Measure | Healthy | Alarm | Action on alarm |
|---|---|---|---|
| 7-day Cold score | at the bar, 90 | 10 or more points below the in-session score | it taught recognition: Help blocks, new surfaces, shorter recall gaps for that class |
| Try steps, first try (`engine.py tries`) | about 80% | under 70% | the unit overloaded him: slow down, Help blocks, rebuild before the next unit of the class |
| Score prediction gap | 10 points or less | over 20 | show predicted vs actual every unit |
| Meaning items, cold | every meaning item right | a meaning item missed cold | keep Worked example 3 unfaded; add a Help block on that surface |
| Outside task: cost and latency budget of his product | within 20% of measured | off by 2x | P-4 not reached |

Struck: median time per item, factor-2 estimate rate, range hit rate, lever match with expert (no grade for them).

---

## 8. Evidence grade for each choice, and what is excluded

### 8a. Grades
| Choice | Grade | Basis |
|---|---|---|
| Spaced, interleaved retrieval on a bank | A | method-effectiveness.md rows 1, 2, 9 |
| Short answer before options; explained solution after each item | A / B | Adesope; elaborated feedback d = 0.99 vs 0.24 |
| A worked example per knowledge point, then completion, then independent; the meaning step never faded until passed cold | A for novices at a new class | Sweller; Renkl and Atkinson; he is a novice at meaning (E11, E12) though not at arithmetic |
| Worked part stresses number-picking and meaning; substitution shown as one line per term | C | Yale primer [S]; one short line costs little (gap-audit 1.13) |
| Item volume and mock scores as readiness measures | C; not used as gates | correlational (r = 0.53, 0.65) and company-reported (95.7% vs 68.6%, 95% at 70%+) |
| Worked estimation examples (a rough size modelled, then asked) | B- | Loretan et al. d = 0.59 to 0.61 quasi-experiment; Redish, Mahajan [S] |
| Estimating before instruction, for a novice | D; not used | no direct evidence (gap-audit 1.2) |
| 90% ranges as a calibration measure | C | Hubbard [M-self]; calibration interventions g = 0.25 (method-effectiveness.md row 26) |
| Control-chart reading, red bead demo | C for learning, A as statistics | the rules are standard statistics; no study of teaching them to engineers found |
| Speed thresholds | C; not used | exam pacing [S]; not a learning study |
| Dead-band readiness rating | D; not used | stated product design only |
| Mock incident in DMAIC order | C | Green Belt training design [S]; debriefs d = 0.67 (method-effectiveness.md row 13) |
| Sensitivity table before lever choice | B | contrasting cases, prediction before reveal (rows 11, 15) |

### 8b. Excluded
| Excluded | Why |
|---|---|
| Six Sigma belt certification and full DMAIC projects | needs a team, months and a live process; ASQ requires 3 years' work experience. Keep only the phase order and the control chart |
| Running the physical red bead experiment | the lesson is the chart, not the beads; a coded run gives the same numbers in 1 minute |
| Case discussion as the method (HBS style) | no peers; case-based learning evidence "inconclusive" (method-effectiveness.md row 27). Keep the exhibits and the swapped-input rework |
| Timed sets and speed grades | exam pacing, not a learning study; a timer on first contact adds load (gap-audit 1.10) |
| Arithmetic drill | the tutor's code computes; drill only a formula he misses twice |
| Memorising Jeff Dean's latency list | dated (NVMe and fast networks changed it) and not LLM-specific; the anchor card replaces it |
| Deep GPU arithmetic (comms cost, tensor parallel maths from kipply) | beyond API-first work; kept only as one C2 item on memory-bound floors |
| Full 3 to 4.5 hour mock exams | built for licensing exams; 45-minute incident mocks match his job and dose |
| Points, leaderboards, XP for items done | gamification raises activity, not learning (row 21); there is no readiness score |
| Blocked practice by formula type after first contact | interleaving evidence; blocking inflates unit scores |

**Gaps.** No study tests any of this on adults learning LLM production. Question-bank and mock evidence is
correlational or company-reported. Salden-style adaptive fading thresholds and the dead-band values are
set by judgement. The PMC paper on Western Electric rule false-alarm rates was blocked by a CAPTCHA and
not used. Hubbard's before/after hit rates were not read in a primary source, so only the method and
the 3-hour figure are used.
