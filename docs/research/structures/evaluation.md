# Evaluation and error analysis: the learning structure for "logic + understanding + methods"

> **Amended 2026-09-24:** the independent review (`review.md`) kept this structure with changes. Where this file disagrees with `INTEGRATED.md` (plain step names, shared recall queue, one mastery rule, start order, the week), `INTEGRATED.md` wins.


Written 2026-09-24. The skill: read real outputs, label pass or fail with a reason, group failures into
types, count them, build and validate LLM judges, and measure whether a fix worked.
Builds on, does not repeat: `../recommended-method.md` (the 10-step unit, the four proven parts),
`../postmortem.md`, `../curricula/skill-methods.md` C1 (worked-example anatomy), `../curricula/
judgement-training.md` 8d (the 35-minute evaluation session), `../curricula/method-effectiveness.md`,
`../curricula/ai-tutoring.md`, `../curricula/teaching-craft.md`, `../curricula/curriculum-design.md`
(nodes E1 to E9, task classes). Materials: `private/research-base/evaluation/` (called "saved" below).

Tags: **[M]** measured, **[M-self]** a number the author or company reports about its own work,
**[S]** stated, no numbers. Every number marked "run" was produced by Python on 2026-09-24.

---

## 1. What kind of learning this is, and what the new experts add

### 1a. The kind
Four different kinds of learning sit inside this one skill. Earlier files treated it as one method.

| Part | Kind | The field that trains it best | What goes wrong without it |
|---|---|---|---|
| See the failure in a trace (pass or fail, which type) | perceptual classification: cue recognition, speeds up with volume | radiology, dermatology, pilots (Kellman's perceptual learning) | he reads 15 traces a session; experts have seen thousands |
| Label to a shared standard | calibrated rating against exemplars | essay scoring, performance appraisal, radiology double reading | his labels drift lenient or strict and nobody notices |
| Build the standard (the failure types) | qualitative coding: open then axial, codebook | social science coding (Saldaña, MacQueen, Hruschka) | types that overlap, or 40 of them, or an LLM invents them |
| Reason about the numbers and causes | base rates, error rates, sampling; sceptical inference | diagnostic test teaching (Gigerenzer), financial audit | trusting 74% agreement, blaming the first plausible cause |

The first three are what is new here. The fourth plays to his strength (finance, numbers).

### 1b. What the new experts add

| Expert or field | What they do | Evidence | What it changes |
|---|---|---|---|
| **Kellman, perceptual learning modules (PLMs)** | Many short classification trials, varied cases, mixed categories, feedback showing the right answer; almost no explanation inside the module (concepts are taught before) | Non-pilots after 1 to 2 hours were as accurate as, and faster than, pilots with 500 to 2,500 hours before training [M] https://journals.sagepub.com/doi/abs/10.1177/154193129403801808 . Maths PLMs: two sessions of 60 trials, gains fully kept at 2 weeks; linear measurement kept at 4.5 months [M] https://files.eric.ed.gov/fulltext/ED547784.pdf | **New format: the rapid round** (section 4a). Volume of short cases is the missing ingredient in 8d |
| **PLMs in medicine** (Krasne, Rimoin, Kellman) | Adaptive modules: 261 histology images; skin lesions; 415 ECGs with a fluency criterion (correct within 15 s) | Skin lesions: effect sizes 1.1 to 2.2, kept at 1 year, self-selected groups [M] https://pubmed.ncbi.nlm.nih.gov/25592621/ . Histology: large gain kept at 6 to 7 weeks, but first-years declined from post-test [M] https://pubmed.ncbi.nlm.nih.gov/24524000/ . Review: only 5 studies, 2 randomised [M] https://pubmed.ncbi.nlm.nih.gov/32654795/ . ECG structure [S] https://onlinelibrary.wiley.com/doi/abs/10.1002/aet2.10454 | Mastery includes **speed on new cases**, not only accuracy. Refresh at about 6 weeks |
| **Kellman's ARTS sequencing** | An item retires after 3 correct answers under a time limit on 3 widely spaced presentations | [S, from search summary, full paper not read] https://files.eric.ed.gov/fulltext/ED549436.pdf | Retirement rule for rapid-round items |
| **Frame-of-reference (FOR) rater training** | Raters learn the dimensions, see behaviour examples at each level, rate practice cases, then compare with expert "true" ratings and discuss the gaps | Accuracy d = 0.83 (Woehr and Huffcutt 1994) and d = 0.50 (Roch et al. 2012, four times as many studies), both as reported in [M] https://pmc.ncbi.nlm.nih.gov/articles/PMC6752840/ ; effects still present 2 weeks later [M] https://researchconnect.suny.edu/en/publications/rater-training-revisited-an-updated-meta-analytic-review-of-frame/ | The calibration step is FOR training, done properly: expert labels **with the reason**, not just the label |
| **Essay-scoring calibration (ETS, GRE)** | Before scoring, raters pass a calibration set of 10 exemplars: at least 6 exact, no answer 2+ points off; 2 attempts; 20 to 40 minutes. Calibrating on day 1 only held accuracy over 5 days | [M] https://files.eric.ed.gov/fulltext/EJ1238527.pdf ; kappa 0.70 as the ETS acceptability line [S, search summary] https://www.ets.org/research/policy_research_reports/publications/report/1998/hxww.html | **Challenge to judgement-training.md 8d:** 3 calibration traces is too few to detect drift. Use 6, and a "no critical miss" rule (never pass a trace the expert failed). Calibration can fade to once per product |
| **Radiology double reading** | Two readers, discrepancies reviewed | Discrepancy 0.4 to 22% by setting [M] https://link.springer.com/article/10.1007/s13244-018-0599-0 ; breast-density readers' self-agreement rose from kappa 0.62 to 0.79 with training [M, search summary] https://pubmed.ncbi.nlm.nih.gov/24951217 | His **self-agreement a week later** is a measure (intra-rater kappa), not only agreement with the expert |
| **Qualitative coding** (Saldaña; MacQueen; Hruschka; Campbell; O'Connor and Joffe) | First-cycle codes, then second-cycle grouping, analytic memos [S] https://uk.sagepub.com/sites/default/files/upm-assets/146042_book_item_146042.pdf . Codebook entry = code, brief definition, full definition, when to use, when not to use, example [S] https://journals.sagepub.com/doi/10.1177/1525822X980100020301 . Double-code 10 to 25% of units; revise and recode in rounds; about 20 codes at most (Hruschka), 30 to 40 (MacQueen) [S] https://discovery.ucl.ac.uk/id/eprint/10091273/ | Coders start very different; codebook revision and recoding reach kappa about 0.8 on most codes [M, qualitative report] https://journals.sagepub.com/doi/10.1177/1525822X04266540 . Negotiated agreement took reliability from 54% to 96% [M] https://journals.sagepub.com/doi/abs/10.1177/0049124113500475 | **Codebook building is its own practice format** (4d), with "when not to use" and a close negative per type. Cap at about 10 types per product |
| **Gigerenzer, natural frequencies** | Teach people to turn probabilities into counts ("of 1,000 women, 10 have cancer, 9 test positive...") with a tree or grid, instead of teaching Bayes' rule | Study 1a medians after training: 75% (tree) and 90% (grid) vs 60% for rule training; rule training fell to a median 20% at 5 weeks while frequency training held (small groups, 5 to 13 at follow-up) [M] http://wexler.free.fr/library/files/sedlmeier%20(2001)%20teaching%20bayesian%20reasoning%20in%20less%20than%20two%20hours.pdf . 160 gynaecologists: 21% to 87% after one session [M] https://www.stat.berkeley.edu/~aldous/157/Papers/health_stats.pdf . Meta-analysis: 24% vs 4% from format alone [M] https://pubmed.ncbi.nlm.nih.gov/29048176/ | Judge catch and clear rates and pass-rate correction are taught **as a frequency tree first**, formula second (4e) |
| **Audit judgement training** (Bonner and Walker; Earley; Plumlee et al.) | Practice with feedback that explains why; self-explanation of the rationale; train divergent thinking (list explanations for an anomaly) then convergent thinking (eliminate the infeasible) | Explanatory feedback or rules plus outcome feedback were needed to acquire procedural knowledge [M] https://www.semanticscholar.org/paper/The-effects-of-instruction-and-experience-on-the-of-Walker-Bonner/37c038b8413826648618a86e7c85aba36c82b145 . Self-explanation and explanatory feedback each helped, together best [M] https://doi.org/10.2308/accr.2001.76.1.81 . Both-stage training gave four times the odds of a viable explanation vs divergent alone [M] https://meridian.allenpress.com/accounting-review/article/90/1/351/127779/Training-Auditors-to-Perform-Analytical-Procedures | **Root-cause step** becomes the auditor's two passes (4g). Feedback is always explanatory |
| **Audit sampling** (PCAOB AS 2315) | Sample deviation rate vs tolerable rate, with an allowance for sampling risk; then the "nature and cause" of each deviation | [S] https://pcaobus.org/oversight/standards/auditing-standards/details/AS2315 (paras .41, .42) | "Did the fix work" is framed as an audit conclusion he already knows: rate, upper bound, tolerable rate, then the cause |
| **Google People + AI Guidebook** | An "error audit": collect canonical error examples; sort into system limitation, context error, background error; ask stakes per error | [S] https://pair.withgoogle.com/chapter/errors-failing/ | Adds **cost of a failure to the user** as a column in every count table |
| **Eugene Yan, Anthropic, OpenAI, HF** (saved) | Binary labels; balanced set with 50 to 100 fails in 200+; judge scored by recall, precision, kappa; human kappa often 0.2 to 0.3 (`eugene-yan/product-evals.md`). Read transcripts; separate outcome from transcript (`anthropic/demystifying-evals-for-ai-agents.md`). Human-human baseline first: two raters correlated 0.563, judge 0.567 (`huggingface-cookbook/llm_judge.md`) | [S] and [M-self] | The benchmark for him and for a judge is **expert agreement, not 100%** |

### 1c. Challenges to the existing research
1. **"80% agreement with expert labels"** (recommended-method.md section 6) is raw agreement. In HW3's
   101 labelled traces (75 pass, 26 fail), a labeller who passes everything scores 74% (run) with kappa 0.
   Replace with kappa plus catch rate (section 5).
2. **SCT items in 8d** are borrowed from medicine and untested for traces. The saved material has a better
   tool built for this skill: close negatives (Cartwheel HW4). They replace SCT.
3. **"Full ladder, slow"** (skill-methods.md C1) ignores that he has done L5 and L6. Worked examples are for
   each new task class; inside a class he enters where the first-step test puts him.
4. **Volume.** 8d labels 15 traces a session; perceptual learning needs hundreds of varied cases. The rapid
   round supplies them in 8 minutes.

---

## 2. THE STRUCTURE: the evaluation unit (corrected 2026-09-25)

**Corrected after `../gap-audit-evaluation.md` (C49).** The first version of this section opened every unit
with labelling, cut the worked examples to one step per task class, used kappa before it was taught and put
12 full traces in one message. It is replaced by the template below: frame-of-reference training in its full
order (the standard, examples at each level, practice with feedback, then blind rating compared with the
expert), the worked-example ladder for each node, and one trace per message where feedback follows each
trace. Unit format v3 (`learn/check_unit.py`) enforces the kinds: show, try, scored, close.

**One node per unit**, in Hamel's order: label against one rule (eval-01) → agreement beyond chance, taught as
counts (eval-02) → look-alikes and arguing with the key (eval-03) → open notes (eval-04) → group → count →
judge → validate the judge → measure a fix. A node's first unit opens with 2 worked examples of that node.

One message per step, in this order, each ending **Your answer.**:

| # | Step | Kind | What it does | Research | Hard rules |
|---|---|---|---|---|---|
| 1 | **The job and the rule** | show | The problem with context (the product, who is hurt by a miss, the decision the labels feed); the rule quoted from the source; the source's own pass and fail examples; one everyday picture; the paths; a short check | FOR dimensions (Woehr and Huffcutt; Roch); C34; A12 | At most 3 new ideas; every rule a later question uses is stated here (B6) |
| 2 | **Worked example 1** | show | One trace, the expert's moves numbered: rule first, what to set aside, the deciding line, what it means under the rule, the label with the key's reason, one dead end; one question on the key move | Renkl and Atkinson; Collins, Brown and Newman (modelling); CTA | Moves come only from the source rule and the key's written reason |
| 3 | **Worked example 2** | show | A close negative of example 1: looks alike, opposite label, same moves | Cartwheel close negatives; contrasting cases | Same layout as example 1 |
| 4 | **Finish the expert's work** | try | Moves 1 to 3 done; he writes what the lines mean and the label | backward fading (Renkl 2002) | Feedback at once; the key reason opens the next step |
| 5-10 | **Warm-up label 1 to 6** | try | One trace per message: label, deciding line, sure or not sure. Message n+1 opens with the expert's label and reason for trace n | FOR; ETS calibration; Kulkarni | About 3 pass and 3 fail; the first repeats the worked cue on a new surface; clear to subtle; aimed at about 80% right |
| 11 | **Warm-up result** | try | The reason for trace 6; he counts his matches; gate (5 of 6, no expert FAIL passed; trial); he predicts his batch score with his warm-up count in hand | ETS gate; C39 | The gate result is a count, not a statistic |
| 12+ | **Label the batch 1 to n** | scored | At most 4 excerpts per message, blind, no feedback until the end | blind labelling | At most 2,600 characters per message including excerpts |
| next | **Compare: your numbers** | try | The expert's labels listed; he counts: matches, expert FAILs he also failed, expert PASSes he also passed; for each difference he says whose label is right and which line, before any reason | Gigerenzer (counts first); Earley (explain first) | Counts only until kappa is taught (eval-02) |
| next | **Compare: the expert's reasons** | show | The key's deciding sentence for each trace; he names the move that would have caught each miss, or argues the key with a line | negotiated agreement; FOR discussion | Reasons are shown text, not answer-key text |
| (node) | **Use the labels** | depends | The node's own task (group, count and decide, check a judge); absent until that node | Hamel's order | Never on a one-criterion product |
| last | **Close** | close | Predicted vs actual (his count), then "next time I see X, I do Y" | after-action review | Two short answers |

Outside the order: `## Help: <step>` blocks (a second worked example on a new surface) for the first tries
and every scored step, sent when he is stuck or after a miss; `## Retry` (new traces, same rule) and
`## Cold` (7 days later, new traces), both scored.

**Excerpts.** Request, diet on record, rule, dish name and the lines the label depends on, word for word
from the source; cut parts marked in square brackets ("checked, nothing in them changes the label"). Only
HIGH-confidence traces whose label follows directly from the quoted rule and that a person has read in full.
Kept out of scored sets: the audit's disputed list (9_25, 35_15, 48_3), plus 1_35 and 1_37, whose "granola
(preferably vegan)" line is an "X or Y" choice by the unit's own path rule, and 47_30, whose "or your
preferred bread" line is the same. Each unit lists a run that checks every excerpt line and quoted reason
against the source (eval-01: `learn/code/eval-01/traces.py`, run as `runs/eval-01-traces.json`).

**Feedback words.** Until kappa is taught, every result is a count ("you matched 10 of 12; the expert failed
3 and you also failed 2"). Rates on a judge use one pair of plain names everywhere: **catch rate** (of the
traces a person marked FAIL, the share the judge also marked FAIL) and **clear rate** (of the traces a person
marked PASS, the share the judge also marked PASS), as in `docs/glossary.md`. "Fail recall" is not used. When
HW3 or `judgy` material is shown, one line converts it: HW3 calls the clear rate TPR and the catch rate TNR,
because it treats PASS as the positive class.

**Other formats** run outside the unit: the 8-minute rapid round (4a), from the second evaluation sitting,
only on categories already taught and only from keyed items; and, every 4 to 6 weeks, a full error analysis
on 100 traces as a capstone (4h).

### Why this differs from the other four skills
| Skill | Its centre | Evaluation's centre instead |
|---|---|---|
| Production | a number, checked exactly by code | a label set, checked by **agreement** with an expert set, where the expert can be wrong |
| System design | one whole design, compared decision by decision | **many small cases**, then a pattern across them (the count) |
| Code | trace and predict one program | no single right output; the standard (codebook) is **built by him** and revised |
| LLM behaviour | predict one mechanism, run it | recognise failures **at speed** across varied cases |
| Evaluation | **calibrate to a standard, label blind, build the standard, measure agreement, decide** | the only skill that starts each session by checking the learner's own instrument |

A generic unit (recommended-method.md section 2) has one problem and one expert solution. Here the unit
of practice is a **batch**, feedback is a **statistic plus reasons**, and a calibration gate comes first,
because a labeller who has drifted makes every later step wrong.

---

## 3. Progression

### 3a. Task classes (each restarts at a worked example; from curriculum-design.md 6b)
| Class | Outputs judged | Saved material | New node |
|---|---|---|---|
| 1 | single-call outputs, binary pass/fail | Recipe Bot HW2 (250 query-response pairs, taxonomy), HW3 (101 labelled traces) | E1, E2, E3, E5 |
| 2 | retrieval plus answer, two-stage | HF `rag_evaluation.md`, OpenAI flywheel leasing assistant, NurtureBoss (100 traces, lesson-4) | E6 |
| 3 | multi-step workflow, first failing step | Recipe HW5 (96 traces, `first_failure_state`), Cartwheel HW4 (tool results vs reply) | E8 per step |
| 4 | agent trajectories and online checks | Anthropic agent evals, OpenAI trace grading, Cartwheel HW5-6 | E8, E9 |

Inside each class the nodes run in Hamel's fixed order: label → codebook → count → cheap check → judge →
validate judge → measure a fix (curriculum-design.md edge E2 → E4 → E5 → E7).

### 3b. Levels and milestones
| Level | He can, observed | Threshold |
|---|---|---|
| Novice | labels a class-1 batch after calibration; writes an open code naming the first failure; computes catch and clear rates from a table | kappa ≥ 0.60 vs expert; catch rate ≥ 0.75 |
| Competent | builds a codebook of 4 to 10 types from 50 to 100 traces with counts x cost; writes and validates a judge; corrects a pass rate | kappa ≥ 0.70; catch rate ≥ 0.85; self-agreement at 7 days ≥ 0.80; judge catch and clear rates ≥ 0.85 on held-out data |
| Proficient | on a new product with no expert labels: sizes the sample for the decision, labels, codes, and his codebook survives an expert check; spots a biased metric | first cold batch kappa ≥ 0.60 on a new product; ship/no-ship call matches the expert on 4 of 5 cases |

### 3c. The fading rule
1. **Placement:** first-step test at the start of a node: one trace, 90 seconds, pass/fail plus open code. Right label and a usable code twice → skip the worked example.
2. **Rungs within a class:** expert notes shown → completion (notes hidden after 6) → blind batch with calibration → blind batch, expert taxonomy shown only after his codebook → new product, no taxonomy.
3. **Up** one rung after 2 units at the level's threshold; **down** one after 2 units below it; a new class restarts at rung 1 (4C/ID saw-tooth).
4. **Calibration fades** from every unit to the first unit on each product once he passes 3 gates in a row (GRE day-1 calibration held for 5 days [M]).
5. **Rapid-round items** retire after 3 correct answers under the time limit on 3 spaced presentations (ARTS [S]).

---

## 4. Practice formats, one concrete example each

### 4a. Rapid classification round (perceptual learning), 8 minutes
25 to 30 short excerpts, each shown for up to 20 seconds: choose "pass" or one failure type from the
current codebook. Right answer and the cue shown after each. Types mixed, products mixed, look-alikes
included. No explanation beyond the cue (concepts come from the main unit).
- **Example:** HW2 `query_response.jsonl` excerpts against the HW2 taxonomy. "Quick salmon dinner ideas"
  answered with a 10 to 15 minute marinade: *Inconsistent Time Estimates*; "2 salmon fillets" with no
  number of servings: *Missing Serving Size*; a plain recipe that meets the request: *pass*. Class 3
  variant: HW5 traces, choose the first failing step (in the set: GetRecipes 32, GenRecipeArgs 20,
  GetCustomerProfile 13, run).

### 4b. Calibration set with expert labels (frame-of-reference)
6 traces from the product, balanced about 3 fail and 3 pass even though the product is not balanced,
each with the expert's reason revealed after his label.
- **Example:** HW3 dietary adherence, `labeled_traces.jsonl` (75 PASS, 26 FAIL, each with `reasoning`).
  "Gluten-light recipe, I'm not celiac" answered with a quinoa salad: he labels, names the cue, then reads
  the key's reason. Note: the course treats these labels as ground truth; who made them is not stated,
  so disagreements are argued on evidence, not settled by authority.

### 4c. Close-negative pairs (contrasting cases)
Two traces that look alike and differ on the one cue that decides the label. He labels both before
seeing either answer.
- **Example:** Cartwheel HW4 worked example. Reply "your refund of $47.50 has been processed" when the
  tool returned `queued_for_approval`: *unconfirmed_write*, fail. Same reply when the tool returned
  `refunded`: pass. Every codebook entry must carry one such pair.

### 4d. Codebook building (open, then axial coding)
He writes open codes on a batch, groups them, and writes each type in MacQueen's format. Then a
reliability round: 7 days later he re-labels a random 20% without looking; types below kappa 0.8 on his
own two passes are rewritten or merged (Hruschka).
- **Example:** NurtureBoss, `recipe-chatbot/lesson-4/nurtureboss_traces.json` (100 traces). Expert notes
  exist on a few, for comparison after he commits: "Did not invoke tool; sent 'Can we send you a text
  message confirmation?' 2x in a row", axial code *Did not invoke tool*; also *Made-up apartment details*,
  *No handoff when needed*. The talk file gives the counts to compare against
  (`talks/aakash-gupta-hamel-shreya-evals-step-by-step.md`, Step 4).

### 4e. Judge validation as a frequency tree
He draws the tree before any formula. Then code computes the catch rate, the clear rate and the corrected
pass rate (`repos/judgy`, which calls the clear rate TPR and the catch rate TNR).
- **Example (run, illustrative judge):** 1,000 traces at HW3's base rate: 743 pass, 257 fail. A judge
  with a clear rate of 0.90 (on passes) and a catch rate of 0.80 (on fails) flags 206 of the 257 fails and wrongly flags 74 of
  the 743 passes. It reports 72.0% pass; the true rate is 74.3%; correcting with (0.72 + 0.80 − 1) /
  (0.90 + 0.80 − 1) gives 74.3%. Changed fact: fails drop to 5%; how many flags are now false?

### 4f. "Did the fix work" as an audit sample
Rate, interval, tolerable rate, then the nature and cause of each remaining failure (AS 2315 .41, .42).
- **Example:** Eugene Yan (`eugene-yan/product-evals.md`): requirement under 5% defects; 200 samples at
  3% gives ± 2.4 points, upper bound 5.4%, cannot ship; 400 samples gives ± 1.7, upper bound 4.7% (run).
  Hamel's NurtureBoss date handling 33% → 95% is the before-after case [M-self].

### 4g. Sceptic's two passes on a cause
Pass 1: at least 3 explanations for the failure pattern. Pass 2: for each, the evidence that would rule
it out, then which survive. Expert comparison after.
- **Example:** HW5, most first failures at GetRecipes (32 of 96). Retriever, bad arguments (GenRecipeArgs is
  the first failure in 20 more), or the recipe data? The transition heat-map
  (`hw5/results/failure_transition_heatmap.png`) is the evidence he reads.

### 4h. Capstone: full error analysis, 100 traces (every 4 to 6 weeks, 60 to 90 minutes)
Whole task, no expert shown until the end: sample, label, code to saturation, count x cost, one judge
validated on held-out data, a recommendation. Scored against the released reference (HW reference
patches, walkthroughs) and the curriculum rubric.

---

## 5. Feedback, assessment, mastery, retention

### 5a. Feedback rules
| Where | Timing | Form | Evidence |
|---|---|---|---|
| Rapid round | after each item | right answer plus the cue | PLM [M] |
| Calibration | after each trace | expert label plus reason | FOR [M]; Bonner and Walker [M] |
| Blind batch | after the batch | statistic, bias direction, then disagreements one by one | Kulkarni bias feedback [M] (judgement-training.md) |
| Every disagreement | he explains first, then sees the reason | self-explanation then explanatory feedback | Earley 2001 [M] |

### 5b. Mastery criteria
| What | Pass | Why this number |
|---|---|---|
| Calibration gate | 5 of 6 exact; no expert-fail labelled pass | GRE uses 6 of 10 with no 2-point miss [M]; binary labels allow a stricter bar |
| Blind labelling vs expert | kappa ≥ 0.70 and catch rate ≥ 0.85, on 2 units | ETS kappa 0.70 [S]; fails are what matter (Yan [S]) |
| Rapid round | ≥ 90% on new excerpts, median ≤ 20 s | PLM accuracy plus fluency; ECG PALM 15 s [S] |
| Codebook | self-agreement kappa ≥ 0.80 at 7 days on 20%; ≤ 10 types | Hruschka 0.8 [M]; code caps [S] |
| Judge | catch and clear rates ≥ 0.85 on held-out test, interval reported | Hamel: above 80%, ideally 90% (saved talk) [S] |
| Fix measurement | right ship/no-ship call with the interval | AS 2315 logic [S] |

A node is mastered at these bars on two units, plus the 7-day recheck (recommended-method.md).

### 5c. Retention and spacing
| When | What | Pass |
|---|---|---|
| 1, 3, 7, 21 days | cue → label rules and codebook definitions in the daily recall | recall the rule and one example |
| 7 days | 10 unseen traces from the same product, cold | kappa within 0.10 of the last unit |
| about 6 weeks | refresher rapid round on retired items (histology first-years declined by 6 to 7 weeks [M]) | ≥ 85% |
| monthly | a new product, first batch cold, no calibration | kappa ≥ 0.60 |

---

## 6. Weekly dose and session length

| Slot | Length | Content |
|---|---|---|
| Main unit (Monday, skill-methods.md D1) | 25 min | section 2 |
| Rapid rounds (Wednesday, Friday) | 8 min each | 4a, after that day's unit |
| Daily recall | about 1 min of the 3-minute block | 1 evaluation item |
| Every 4 to 6 weeks | 60 to 90 min, replaces the main unit | capstone 4h |
| **Total** | **about 45 to 50 min a week** | the largest single-skill share, matching evaluation in 60% of postings |

Why this size: PLM gains came from 1 to 2 hours in total per category set [M], so 16 minutes of rapid
rounds a week covers a task class in 4 to 6 weeks. Why short: 8 to 25 minutes fits his record that long
blocks broke his attention (postmortem, method 8). Conflict to settle in the timetable: llm-behaviour.md
also asks for Monday in weeks 1 to 6.

---

## 7. Measures that show it is working

| Measure | Healthy | Alarm |
|---|---|---|
| Kappa vs expert, per product | rising across units to ≥ 0.70 | flat for 3 units |
| Catch rate (his, against the expert) | ≥ 0.85 | under 0.75: he is passing failures |
| Bias | his fail rate within 5 points of the expert's | consistently lenient or strict by 10+ |
| Predicted vs actual failure rate | gap ≤ 10 points after 4 weeks | above 20 |
| 7-day self-agreement | ≥ 0.80 | under 0.70: labels are guesses |
| Rapid-round speed on new items | median falling toward 20 s | falling speed with falling accuracy |
| Cold transfer (new product) | first batch kappa ≥ 0.60 | under 0.50 |
| Early warning | rapid rounds ≥ 90% but blind-batch kappa under 0.60 means he recognises taught types but does not find new ones |

---

## 8. Evidence grade per choice, and what is excluded

### 8a. Grades
| Choice | Grade | Basis |
|---|---|---|
| Calibration with expert reasons before labelling | moderate to strong | FOR meta-analyses d = 0.50 to 0.83 [M]; GRE [M] |
| Rapid classification rounds | moderate | large effects, few randomised studies, medical and maths [M]; never tested on text traces |
| Mastery by kappa plus catch rate | moderate | agreement statistics are standard [S]; the exact bars are borrowed |
| Codebook format and reliability rounds | moderate | Hruschka, Campbell [M, small]; MacQueen, O'Connor and Joffe [S] |
| Frequency tree before the formula | moderate to strong | meta-analysis 24% vs 4% [M]; training studies with small follow-up [M] |
| Explanatory feedback plus self-explanation | moderate | Bonner and Walker, Earley [M, lab studies with students and auditors] |
| Sceptic's two passes | moderate | Plumlee et al. [M, one study] |
| Close negatives | weak to moderate | contrasting cases [M, other domains]; Mamede look-alikes (judgement-training.md) |
| Audit sampling framing of fix measurement | weak as teaching evidence | [S], chosen because he already knows it |
| Weekly dose | weak | derived from PLM dosage and his record, not tested |

### 8b. Excluded
| Excluded | Why |
|---|---|
| 1 to 5 or Likert labels | inconsistent across raters (Yan, Hamel [S]); binary everywhere |
| SCT items from 8d | medical, untested for traces; close negatives do the same job with saved material |
| An LLM proposing the taxonomy before he codes | Shreya: agents skip the reading [S]; he would learn to accept, not to see |
| Claude as the "expert" labeller | no outside anchor (postmortem cause 4); Claude may be a second coder only to flag disagreements |
| Rater error training alone (naming biases) | in a 5-group trial, FOR-based groups rated closer to the expert than the rater-error group [M] https://pmc.ncbi.nlm.nih.gov/articles/PMC6752840/ |
| Teaching Bayes' rule as a formula first | rule training decayed to 20% at 5 weeks [M] |
| Synthetic-only trace sets | out of distribution (Yan [S]); synthetic only to fill a missing type |
| Peer breakout alignment (course lesson 4) | no peers; replaced by expert key plus his own 7-day recode |
| Speed pressure in the blind batch | speed is trained only in rapid rounds, so accuracy is not traded away where labels count |

### Gaps
- No study tests perceptual learning, FOR training or codebook rounds on LLM traces; all carried over by analogy.
- Roch 2012 and Woehr and Huffcutt effect sizes read from a secondary source, not the originals (paywalled).
- ARTS retirement rule and ECG PALM results come from summaries; the full papers were not read.
- Sedlmeier and Gigerenzer's follow-up groups were 5 to 13 people.
- The expert labels in HW3 have no stated author; the key is used, but he can overturn it with evidence.
