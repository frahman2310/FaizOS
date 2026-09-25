# Production: the learning structure for "small maths + quality control, applied"

> **Amended 2026-09-24:** the independent review (`review.md`) kept this structure with changes. Where this file disagrees with `INTEGRATED.md` (plain step names, shared recall queue, one mastery rule, start order, the week), `INTEGRATED.md` wins.


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
| **CFA prep (CFA Institute, Kaplan Schweser)** | Learning outcome statements with command words (calculate, interpret, evaluate); inline examples; end-of-module practice problems with solutions; then "thousands" of QBank items, then 4 to 6 timed mocks. Exam pace: 180 items in 270 minutes, 90 seconds each | LOS [S] CFA 2025 sample (skill-methods.md B); pace [S] https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-i-exam ; "95% of Level II candidates who scored 70% or higher on mock exams" passed [M-self] https://www.schweser.com/cfa/level-2/study-packages | The bulk of practice is **item volume with explained solutions**, not worked examples. Speed is part of mastery. A mock score is a readiness gate |
| **Actuarial prep (Coaching Actuaries)** | Adaptive practice exams; "Earned Level" 0 to 10 rises when a score beats a high threshold, falls below a low one, holds between; only full adaptive exams count, not quizzes | Mechanism [S] https://support.coachingactuaries.com/article/227/what-is-an-earned-level . 2024 survey, Exam FM: 95.7% pass at EL 5.5+, 68.6% below [M-self, self-selected survey, no sample size] https://www.coachingactuaries.com/blog/insights/exam-p-and-fm-2024-survey-insights-pass-rates-ratings-and-key-takeaways . Exam P: 30 items in 3 hours, adaptive, scaled 0 to 10 [S] https://analystprep.com/actuarial-exams/soa/exam-p-probability/ | One readiness number per problem class, moved only by mixed sets, never by single drills. Thresholds with a dead band so one lucky set does not promote him |
| **Question-bank evidence (medicine)** | Board candidates work thousands of bank items | Step 1 score vs items done r = 0.53; practice-test score vs Step 1 r = 0.65; N = 47, 46% response [M-cor] https://pmc.ncbi.nlm.nih.gov/articles/PMC8368851/ | Volume and mock scores **predict**; they are not shown to **cause**. Use mock score as a measure, keep retrieval (grade A) as the reason for the bank |
| **Sanjoy Mahajan** (Street-Fighting Mathematics; The Art of Insight) | Divide and conquer into an estimation tree; estimate leaves by gut with a range and take the geometric mean; "reliability comes from intelligent redundancy": two unrelated methods for the same number; easy cases (check a formula at its extremes). Tutor questions interspersed and answered in the next paragraph; "merely watching workout videos produces little fitness" | [S] https://ocw.mit.edu/courses/res-6-011-the-art-of-insight-in-science-and-engineering-mastering-complexity-fall-2014/3bca850386a3005c22134fa62fb3bad5_MITRES_6-011F14_art_insfin.pdf ; tools list [S] https://mitpress.mit.edu/9780262514293/street-fighting-mathematics/ | **New step: estimate before any code runs**, as a tree with a range. Easy-case check on every formula (hit rate 0 and 1) |
| **Fermi and order-of-magnitude teaching** | Redish: an estimation problem in every homework and every exam; most credit for the reasoning, not the answer; acceptable range "typically a factor of two or more". Weinstein: within a factor of 10 is enough to decide most things | Redish [S] https://arxiv.org/abs/2011.12699 ; Weinstein [S] https://plus.maths.org/guesstimation . Worked examples for order-of-magnitude reasoning vs conventional tasks, same teacher, N = 118 complete sets: d = 0.61 and d = 0.59, near and far transfer [M, quasi-experiment] https://arxiv.org/abs/2405.16480 ; a systematic review found almost no prior evidence that estimation is teachable (same paper) | Estimation is **a thread in every unit, not a topic**. Graded on the tree, pass band a factor of 2 |
| **Back-of-envelope in engineering** (Jeff Dean, ByteByteGo, Google NALSD) | A short list of anchor numbers; QPS, peak, storage, servers from them. Google SRE: turn a whiteboard design into resource numbers; AdWords example: 500,000 queries/s, 86.4 TB/day of logs rounded to 100 TB | [S] https://brenocon.com/dean_perf.html ; [S] https://bytebytego.com/courses/system-design-interview/back-of-the-envelope-estimation ; [S] https://sre.google/workbook/non-abstract-design/ | A small **anchor card** for LLM work goes into spaced recall (below). Round early, as NALSD does |
| **Hubbard calibration training** | Stated-confidence ranges on trivia with feedback, "equivalent bet", start from absurd bounds to fight anchoring; about 3 hours trains most people | [M-self] http://www.hubbardresearch.com/wp-content/uploads/2019/06/Introduction-to-Calibrating-Probability-Assessments-Hubbard-Decision-Research.pdf | His estimate carries a **90% range**; the share of ranges that contain the true number is a measure |
| **Deming red bead, SPC** | 20% red beads, paddle of 50: counts run 1 to 19 around 10 from the system alone; np-chart limits "close to 1 and 19". Lesson: blaming workers for common-cause variation changes nothing; change the process | [S] https://www.spcforexcel.com/knowledge/variation/red-bead-experiment/ ; [S] https://deming.org/lessons-from-the-red-bead-experiment-with-dr-deming/ . Western Electric rules (beyond 3 sigma; 2 of 3 beyond 2 sigma; 4 of 5 beyond 1 sigma; 8 in a row one side) [S] https://www.qualitygurus.com/nelson-rules-and-western-electric-rules-for-control-charts/ | **New problem class: "is this a signal?"** before "which lever?". The simulated red bead (run in code) is the opening demo |
| **Six Sigma Green Belt** | Two blocks of about four class days a month apart, a real improvement project between them, DMAIC tollgate review at the end of each phase | [S] https://www.6sigma.us/course/green-belt-training/ ; [S] https://sixsigmastudyguide.com/dmaic-tollgate-reviews/ | The **mock incident** follows DMAIC in miniature (define the number, measure baseline, analyse shares, improve one lever, control with an alert). Belt certification itself is excluded (section 8) |
| **Google SRE workbook** | Every alerting option judged on precision, recall, detection time, reset time; burn-rate table; worked budget spends (a 4-hour bad release used 13% of budget, a 20-hour restore 65%) | [S, saved: sre-workbook-05, sre-workbook-02] | The error-budget class is taught as "how much budget did this spend, and do we page" |

**Net challenge to the earlier plan.** recommended-method.md gives every skill the same 10 steps, with a
worked example as the centre. For this skill the evidence says the centre is **a bank of exhibit items
done at pace with explained solutions, each opened by his own estimate and closed by a lever choice**.
Worked examples appear once per problem class and show the number-picking and the meaning, not the maths.

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
| 2 | **Worked example 1** (knowledge point 1) | show | One everyday picture with where it stops; which numbers from the exhibit and why; the formula in plain words; **a rough size first**, then one substitution line per term with units; code that computes it with a **How this code works** block; what the answer means; one wrong turn, labelled wrong before it is shown; one self-explanation question on the key step. | B1, B2; Yale primer; CFA layout (skill-methods.md:170-178); Mahajan's modelled estimate; Loretan et al. (worked estimation); C48 |
| 3 | **Your turn 1** | try | Same shape, new surface. Completion: the first link done, he does the rest. 2 to 4 short questions, aimed at about 80% right first try; any direction question as two options. | completion problems; Renkl and Atkinson; B9; E12 |
| 4 | **Worked example 2** (knowledge point 2) | show | As step 2, one new idea (for C1: calls a month and the share of the bill). | Math Academy knowledge points (teaching-craft.md:115) |
| 5 | **Your turn 2** | try | As step 3. The first **rough guess** he is asked for comes here, after he has seen a worked rough estimate, as one number. | gap-audit 1.1 |
| 6 | **Worked example 3: what the number means** | show | A saving as before minus after, written as a subtraction, the one-side slip labelled wrong; the biggest share is where to cut first; which way an unsure input bends the bill (higher or lower). Never faded until he passes it cold. | E11, E12; review.md:108, :206; INTEGRATED.md section 6 |
| 7 | **Your turn 3** | try | 2 or 3 meaning items; direction as two options. | E12 (0/3 open, 3/3 as two options) |
| 8 | **Lever** | try | The table first (each option: cost after, saving per call and per month, what it risks), computed; then one pick of two with the deciding number. He never names a lever or its size before seeing the table. | contrasting cases (grade B, section 8a); Schwartz and Bransford 1998 |
| 9 | **Quick set 1** | scored | Before it, his score prediction (`engine.py predict`). 5 short-answer items on new surfaces, this class only (interleaving starts from the second class); 1 or 2 about what a number means. | Kulik bar; Adesope short answer first |
| 10 | **Quick set 2** | scored | Opens with the worked solutions to items 1 to 5 (inside the step, so the guard sends them verbatim), then 5 more items, 2 or more about meaning. Both halves together: **10 items, at least 3 about meaning, pass 9 of 10** (INTEGRATED section 3). | elaborated feedback d = 0.99 vs 0.24 |
| 11 | **Close** | close | Opens with the solutions to items 6 to 10; then his line "Next time I see X, I first ...". | INTEGRATED 1 |

Prepared blocks outside the order (all required by the checker):
- **`## Help: <step>`** for every try step and every scored step: a second worked example on a new surface,
  taught differently (for example, a case where output, not input, is the biggest share), ending on the same
  question shape. Sent as move 3 of the stuck order, and before a Retry.
- **`## Retry`**: 10 new items, at least 3 about meaning, pass 9 of 10, after a miss and its Help blocks.
- **`## Cold`** (7 days later): 10 new items, at least 3 about meaning, pass 9 of 10, one message.
- **Cards**: every number card carries 4 surfaces (`||`), so a review never repeats the numbers.

Target first-try rate on the try steps: about 80%. Under 70% means the unit overloaded him; rebuild it
before the next unit of that class (gap-audit 4.4).

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
- No timer in the first two units of a class; time is logged, not shown (gap-audit 1.10).
- Stuck order: his own earlier number or the show step it uses; two options; the step's Help block; the answer
  worked line by line, which he says back.

**Every fourth production unit is a mock incident** (45 minutes, section 4e) instead, once classes C1 to C6 have
each had their first-contact unit.

### Why this differs from the other four skills
| Skill | Its centre | Production's centre instead |
|---|---|---|
| Evaluation | labelling real traces, agreement with expert labels | a number, checked exactly by code |
| System design | commit a whole design, compare section by section | many small items at pace; judgement only at the lever step |
| Code | read, trace, predict output | the chain is written in words and units, code only computes |
| LLM behaviour | predict, run, explain one mechanism | predict a *size* (range) and a *lever*, not a behaviour |
| Production | **estimate, compute, decide, at speed, with variation read before any lever** | speed and calibration are graded; no other skill grades them |

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
| **P-1 Computes** | C1, C2 | 9 of 10 exact on a mixed C1+C2 set, median time 2 minutes or less per item; estimates within a factor of 2 on 7 of 10 |
| **P-2 Budgets** | + C3, C4 | 9 of 10 on a mixed C1 to C4 set; break-even hit rate and burn-rate page decision right without the formula shown |
| **P-3 Reads variation** | + C5, C6 | on 5 charts, says signal or noise and names the rule, 4 of 5; lever choice matches the expert on 4 of 5 with the effect size within a factor of 2 |
| **P-4 Runs production** | + C7 | mock incident score 70% or more on two in a row; outside task: the cost and latency budget for his FBR tax assistant within 20% of measured (curriculum-design.md 6a) |

Support fades inside a class and resets at the next (4C/ID). Promotion needs the milestone twice, 7 days apart.

---

## 4. Practice formats, one concrete example each

### 4a. Exhibit-based problem (C1)
**Exhibit.** Support bot on Claude Sonnet 4.6: input $3/MTok, output $15/MTok, cache read $0.30/MTok,
5-minute cache write $3.75/MTok (anthropic-pricing.md). System prompt 6,000 tokens, user message 500,
answer 400. 20 calls per user per day, 30 days.
**Question.** Cost per call and per user per month, with no caching.
**Key.** (6,000 + 500) x $3/M + 400 x $15/M = **$0.0255 per call**; x 20 x 30 = **$15.30 per user per month**.
**Meaning.** The system prompt is 70.6% of the bill, the answer 23.5%, the user message 5.9%.
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
Scored on 10 points: 2 per step, one for the number, one for the reason. Pass 7.

### 4f. Question-bank set (all classes, interleaved, timed)
| # | Item | Key | Source |
|---|---|---|---|
| 1 | 99.9% over 30 days: minutes of full outage allowed? | 43.2 | appendix-a |
| 2 | 0.5% errors on a 99.9% SLO: burn rate, days to empty? | 5; 6 days | sre-workbook-05 |
| 3 | 3 retries at each of 3 layers: attempts on the database per user action? | 4^3 = 64 | sre-book-22 |
| 4 | Queue 10x the thread count, 100 ms per request: added latency? | about 1 s | sre-book-22 |
| 5 | 97% SLO, budget 109,897 errors; a bad release caused 14,066: share? | 12.8% (book: 13%) | sre-workbook-02 |
| 6 | 10k input + 200 output tokens at $0.06 / $0.12 per 1K: cost per call? | $0.624 | huyen |
| 7 | Cut the prompt 50%: latency effect? Cut the answer 50%? | 1 to 5%; about 50% | openai-latency-optimization |
Short answer first; options only for items he gets wrong twice (Adesope rule, method-effectiveness.md 1b).
Pace: single-formula items 90 seconds (CFA pace), multi-step 5 minutes (between CFA and Exam P's 6).

---

## 5. Assessment, mastery and retention

| What | Threshold | Why this number |
|---|---|---|
| Exact answer | 9 of 10 on a mixed set, twice, 7 days apart | mastery bar 91 to 100% (Kulik, grade B) |
| Speed | median 90 s single-formula, 5 min multi-step | CFA and Exam P pace [S]; speed shows compiled skill (ACT theory, skill-methods.md A1) |
| Estimate | within a factor of 2 on 70% by P-1, 80% by P-3; never off by 10x | Redish's factor-2 band; Weinstein's factor-10 floor |
| Calibration | his 90% ranges contain the truth 80 to 95% of the time | Hubbard's method; below 80% means overconfident |
| Lever choice | matches the expert on 4 of 5, effect size within a factor of 2 | judgement, graded like design |
| Signal or noise | 4 of 5 charts right, rule named | Western Electric rules |
| Class readiness (0 to 10) | +1 when a mixed set scores 90%+, -1 below 70%, no change between; only mixed sets count | Coaching Actuaries' dead-band mechanism [S] |
| Mock incident | 7 of 10, twice in a row, for P-4 | Schweser's 70% mock gate [M-self] |

**Retention plan.**
- Recall queue at 1, 3, 7, 21 days (grade A). Items return as a new exhibit with new numbers, never the
  same item (Brilliant's variant banks, teaching-craft.md).
- **Interleaving is the default** from the first week: every set mixes all unlocked classes, because
  choosing the formula is the skill (d = 0.79 to 0.83). First contact with a class is blocked inside one unit only.
- Confusable pairs are taught days apart, mixed later: availability (time) vs aggregate (requests);
  error rate vs burn rate; TTFT vs TPOT; cache write vs read multiplier.
- **Anchor card** (spaced recall, 1 item a day): 1.3 tokens per word; 2 bytes per parameter in 16-bit;
  output latency scales with output tokens, input barely; cached read 0.1x, write 1.25x; 99.9% = 43.2
  min a month; 14.4x burn = page. All from the saved sources.
- One production item a week appears inside another skill's unit (a design's cost line, an eval's
  sample size), which is retrieval inside new work.

---

## 6. Weekly dose and session length

| Slot | Length | Content |
|---|---|---|
| Friday unit (curriculum-map.md) | 25 min | the unit in section 2 |
| Daily recall | about 1 min of the 3-minute block | 1 production item or anchor |
| Inside other skills | about 5 min a week | one cost or latency line in a design or eval |
| Every 4th week | 45 min, replaces the Friday unit | mock incident |
| **Total** | **about 35 to 40 min a week** | about 15% of study time; the core three keep 70% |

Volume: about 12 bank items a week (3 per unit + recall + inside work), so about 150 over 12 weeks
across 7 classes. That is far below board-exam volumes, on purpose: the item pool is small and he is
already accurate. If a class sits below readiness 5 for 3 weeks, add a second weekly unit for that class only.

---

## 7. Measures that show it is working

| Measure | Healthy | Alarm | Action on alarm |
|---|---|---|---|
| 7-day cold accuracy on production items | 85% or more | under 75% | shorten the recall gaps for that class |
| Factor-2 estimate rate | rising to 80% by week 8 | flat under 60% | one Mahajan tree worked example; two-method rule on every estimate |
| Range hit rate (90% ranges) | 80 to 95% | under 70% (overconfident) or 100% with huge ranges | start from absurd bounds (Hubbard) |
| Median time per single-formula item | 90 s or less by P-2 | rising | more timed mixed sets, not more examples |
| Lever match with expert | 4 of 5 | under 3 of 5 | worked lever solutions, sensitivity table before his pick |
| Unit score vs 7-day score gap | under 10 points | unit 90%+ and 7-day under 70% | it taught recognition: more interleaving, new surfaces |
| Score prediction gap | 10 points or less | over 20 | show predicted vs actual every unit |
| Outside task: cost and latency budget of his product | within 20% of measured | off by 2x | P-4 not reached |

---

## 8. Evidence grade for each choice, and what is excluded

### 8a. Grades
| Choice | Grade | Basis |
|---|---|---|
| Spaced, interleaved retrieval on a bank | A | method-effectiveness.md rows 1, 2, 9 |
| Short answer before options; explained solution after each item | A / B | Adesope; elaborated feedback d = 0.99 vs 0.24 |
| One worked solution per class, then completion, then his own chain (fast fade) | A for novices, reverses with expertise | expertise reversal; he is not a novice at arithmetic |
| Worked part = number-picking and meaning, not substitution | C | Yale primer [S]; consistent with expertise reversal |
| Item volume and mock scores as readiness measures | C | correlational (r = 0.53, 0.65) and company-reported (95.7% vs 68.6%, 95% at 70%+) |
| Estimate-first as a thread, factor-2 band | B- | Loretan et al. d = 0.59 to 0.61 quasi-experiment; Redish, Mahajan [S] |
| 90% ranges as a calibration measure | C | Hubbard [M-self]; calibration interventions g = 0.25 (method-effectiveness.md row 26) |
| Control-chart reading, red bead demo | C for learning, A as statistics | the rules are standard statistics; no study of teaching them to engineers found |
| Speed thresholds | C | exam pacing [S]; not a learning study |
| Dead-band readiness rating | D for learning, useful mechanism | stated product design only |
| Mock incident in DMAIC order | C | Green Belt training design [S]; debriefs d = 0.67 (method-effectiveness.md row 13) |
| Sensitivity table before lever choice | B | contrasting cases, prediction before reveal (rows 11, 15) |

### 8b. Excluded
| Excluded | Why |
|---|---|
| Six Sigma belt certification and full DMAIC projects | needs a team, months and a live process; ASQ requires 3 years' work experience. Keep only the phase order and the control chart |
| Running the physical red bead experiment | the lesson is the chart, not the beads; a coded run gives the same numbers in 1 minute |
| Case discussion as the method (HBS style) | no peers; case-based learning evidence "inconclusive" (method-effectiveness.md row 27). Keep the exhibits and the swapped-input rework |
| Worked examples that show every substitution | he already computes at 88%; expertise reversal makes them a cost |
| Arithmetic drill | the tutor's code computes; drill only a formula he misses twice |
| Memorising Jeff Dean's latency list | dated (NVMe and fast networks changed it) and not LLM-specific; the anchor card replaces it |
| Deep GPU arithmetic (comms cost, tensor parallel maths from kipply) | beyond API-first work; kept only as one C2 item on memory-bound floors |
| Full 3 to 4.5 hour mock exams | built for licensing exams; 45-minute incident mocks match his job and dose |
| Points, leaderboards, XP for items done | gamification raises activity, not learning (row 21); readiness moves only on mixed-set scores |
| Blocked practice by formula type after first contact | interleaving evidence; blocking inflates unit scores |

**Gaps.** No study tests any of this on adults learning LLM production. Question-bank and mock evidence is
correlational or company-reported. Salden-style adaptive fading thresholds and the dead-band values are
set by judgement. The PMC paper on Western Electric rule false-alarm rates was blocked by a CAPTCHA and
not used. Hubbard's before/after hit rates were not read in a primary source, so only the method and
the 3-hour figure are used.
