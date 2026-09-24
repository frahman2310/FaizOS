# Review of the five learning structures, before anything is built

Written 2026-09-24 as an adversarial check of `evaluation.md`, `llm-behaviour.md`, `system-design.md`,
`production.md` and `code.md` against `../postmortem.md`, `../recommended-method.md`, `../curricula/*.md`
and `../../learning-evidence.md` (his record, C1 to C45). Only faults and fixes are listed.
Learner update received during the review: "5 hours a week is nothing, workload is not an issue." So
section 1 does not cut time. It asks where more time would add learning, and where it stops helping.

---

## 1. Time, schedule clashes, and where extra time helps

### 1a. What the five files ask for, added up (weeks 1 to 6)

| Skill | Units | Extra sessions | Own daily recall | Capstone | File's own total |
|---|---|---|---|---|---|
| Evaluation | 25 min Mon | rapid rounds 8 min Wed, Fri | about 1 min | 60 to 90 min every 4 to 6 wks | 45 to 50 min (eval 6) |
| LLM behaviour | 20 min Mon, Thu | 1 predict-and-run inside another skill | 3 to 5 min | none | 70 min (llm 6) |
| System design | 40 min Wed | 15 min drill Sat | about 2 min | 60 min every 4th wk | 65 to 70 min (sd 6) |
| Production | 25 min Fri | about 5 min inside others | about 1 min | 45 min mock every 4th wk | 35 to 40 min (prod 6) |
| Code | 30 min Tue, Thu | none | 5 min Mon to Sat | 45 min steer every 3rd Sat | 90 to 105 min (code 6) |
| **Sum** | | | **12 to 14 min a day, in 5 queues** | | **305 to 335 min, about 5.1 to 5.6 h** |

Time is not the problem (learner's word). The problems are these clashes and one mismatch:

| Clash | Where |
|---|---|
| Monday: evaluation unit and an LLM Break-it unit, two new unit shapes back to back | eval 6 says so itself; llm 6 "Mon and Thu" |
| Thursday: code unit and LLM unit; Wednesday and Friday: eval rapid rounds on top of the design crit and the production unit | code 6, llm 6, eval 6 |
| Saturday: design drill, code steer (every 3rd wk), and the optional mixed review of `curriculum-map.md` | sd 6, code 6, curriculum-map "The week" |
| Capstones collide: design every 4th wk, production every 4th wk, code every 3rd wk, eval every 4 to 6 wks. Week 12 can hold all four (up to 4 hours of whole-task work in one week) | sd 6, prod 3a/6, code 6, eval 4h |
| Every file claims a share of "the 3-minute block" (curriculum-map, skill-methods D1), but the shares add to 12 to 14 minutes | eval 6, prod 6, sd 5c, llm 6, code 5 |

### 1b. Would more time per skill add learning? Where it stops

| Skill | More of what | Helps? | Where it stops, and why |
|---|---|---|---|
| Evaluation | a 3rd rapid round a week | yes, for speed and cue recognition | PLM gains came from 1 to 2 hours in total per category set (eval 1b); after items retire (3 correct, spaced) extra rounds only repeat. The trace pool is the ceiling: about 550 saved traces (HW2 250, HW3 101, HW5 96, NurtureBoss 100); at 90 excerpts a week class 1 is used up in about 4 weeks and he starts memorising items, not cues |
| LLM behaviour | more cards, more units a week | little | 9 concepts in level 1 (llm 3). Quantum Country: about 1.5 h of total review held answers 9+ weeks [SR]. More cards raise daily review load with no new concept; the file itself caps cards at 5 min (llm 5). Spend extra on predict-and-run inside other skills (transfer, Butler 2010) |
| System design | more cases: a 2nd drill, more guess-the-move | **yes, the clearest case** | judgement grows with cases met and compared (sd 6, Klein). Limit is keyed material: 24 worked-example chapters, but 358 weak/strong pairs (recommended-method 4). A 2nd crit a week is limited by prepared keys, not by him |
| Production | more bank items | no | he is already accurate on arithmetic; overlearning past mastery fades by about 4 weeks (Rohrer and Taylor 2006 https://doi.org/10.1002/acp.1266 ). Extra time is better spent on the "meaning" items where his record is weak (E11 0/2, E12 0/3) |
| Code | more daily reps | yes, while E1 to E4 persist | recurrent procedure, part-task practice allowed (code 2, 4C/ID). Stop adding once each of E1 to E4 is 5 right in a row cold (code 5) |

Three limits apply to every skill:
1. **Spacing needs gaps.** For a test a week away the best gap between reviews is about 20 to 40% of that
   delay, about 1 to 3 days (Cepeda et al. 2008, 1,350+ people
   https://journals.sagepub.com/doi/10.1111/j.1467-9280.2008.02209.x ). A second session on the same
   items the same day adds little; extra time should go to new cases, not repeats.
2. **Sitting length is not the risk his record shows.** The 88-question bootcamp day worked (A9); the
   51-question single message failed (A11). The limit is message size (B8, 700 to 2,100 characters) and
   one part per message (C25), not minutes. A 40-minute crit is fine if it arrives as 7 or 8 short messages.
3. **Starting several new tracks at once is the real overload** (section 6), not total hours.

---

## 2. Duplication and complexity

### 2a. The same machine built five times

| Machine | Evaluation | LLM behaviour | System design | Production | Code | One system instead |
|---|---|---|---|---|---|---|
| Spaced recall | 1, 3, 7, 21 d | FSRS, 0.9 | 1, 3, 7, 21 d | 1, 3, 7, 21 d, new numbers | 1, 3, 7, 21 d | **one queue, FSRS, one 10-min daily slot**, items mixed across skills; item types: card, number item with fresh numbers, trace excerpt, code snippet, cue-to-move |
| Recall inside the unit | "Mixed recall" 3 min | "Cards" 3 to 5 | "Recall" 2 | "Mixed recall" 3 | "Warm reps" 4 | **drop from units**; the daily slot does it (4 names for one act) |
| Confidence measure | predicted failure rate; sure/unsure | confidence 1 to 5 | predicted rubric score next week | 90% range; predicted score | predicted score | **one: predicted score before each check, gap logged**; plus sure/unsure per item where a confident error matters (eval, LLM). Production's 90% range stays, but as an estimation skill, not as calibration |
| Close of the unit | "Review": one cue-to-label rule | "Keep": cards | "Record": ADR, rule, prediction | "Score and log" | "no written reflection" | **one 2-min Close**: predicted vs actual, one line "next time I see X, I do Y" into the queue |
| Progress rule | 2 units at bar up / below down | confidence 4-5 wrong sends back | 2 at 70+ up / 2 under 55 back | fixed 3 rungs + readiness 0 to 10 | 2 right up / 2 misses down | **one rule** (section 4) |
| Headline statistic | kappa, fail recall | normalized gain | rubric score | readiness | trace cells, EiPE | per skill: **one main score, the 7-day cold score, the prediction gap** |

### 2b. What the learner would have to learn

| Count | Number | Detail |
|---|---|---|
| Unit names | 5 | "Calibrate, Label, Code, Check"; "Break-it"; "Design Crit"; "Estimate, Compute, Decide"; "Predict, Trace, Change, Break, Steer" |
| Step names | **39** | eval 8, LLM 9, design 8, production 7, code 7 |
| Unit variants | 5 | eval first-time and later-node variants; design Study variant; production first-time and mock incident |
| Practice formats | **40** | eval 8, LLM 6, design 9, production 6, code 11 |
| Numeric thresholds | about **60** | eval about 15, LLM 12, design 12, production 12, code 10 |
| Documents | 1,389 lines | against the postmortem's 251-line, 45-rule rulebook (cause 1) |

This repeats postmortem causes 1 and 8 (the rulebook and the machinery grew faster than the learning).
Thresholds can live in the tracker, unseen. Step names and formats cannot: he meets them every session.

### 2c. Simplification
1. Keep five middles (C44: the kinds of learning really differ). Share one frame around them:
   **daily recall slot, then Commit, Check, Compare, Close** in every skill.
2. Step names: about 20 in plain words (rename table in 5b).
3. Formats live in weeks 1 to 8: about 20. Deferred until level 2 of that skill: eval 4d reliability
   round, 4g, 4h; LLM F (moved into production); design formats 3, 5, 8, 9; code "review an AI diff" and
   "specify" (already level 2+).
4. Drop production's 0-to-10 readiness rating: it is a second mastery system, graded D by its own file (prod 8a).

---

## 3. Evidence quality: the 3 weakest claims per structure

| Structure | Weak claim driving a design choice | Why weak | Verdict |
|---|---|---|---|
| Evaluation | Rapid round, 20-s limit, ARTS retirement (eval 1b, 3c.5) | ARTS rule "from search summary, full paper not read" (eval 1b, gaps); PLMs never tested on text; histology first-years declined by 6 to 7 wks | **trial and measure** |
| Evaluation | Mastery by kappa ≥ 0.70 and fail recall ≥ 0.85 on a 12-trace batch (eval 2, 5b) | Too few items. Run: 12 traces with 3 fails, one missed fail gives recall 0.67 (fails the bar) and kappa 0.75; two disagreements give kappa 0.56. 7-day recode of 20 traces: 2 disagreements drop kappa to 0.73, under 0.80. The bar flips on one trace | keep the measure, **pool over 2 units (24+ traces)** before judging; bars trial |
| Evaluation | HW3 labels as the "expert key" and the gate 5 of 6 (eval 4b, 5b) | author of labels unknown (eval gaps); 5 of 6 is adapted from GRE's 6 of 10 on a different scale, by judgement | keep key, gate is **trial** |
| LLM behaviour | ConcepTest with revote as the core step (llm 2) | Mazur's and Hake's gains came from classrooms with peer discussion, courses not randomised; the file itself says "revote without peers is untested" (llm 8) | **trial**; the predict-and-run part (Crouch 2004) is the better-evidenced core |
| LLM behaviour | LBCI gain ≥ 0.5 "above Hake's interactive mean" (llm 7) | a 10-item home-made test compared with a validated 30-item inventory; teacher-made tests inflate about 3x (0.84 vs 0.27, curriculum-design); one item = 10 points | guide only, **never a level gate** until rewritten once |
| LLM behaviour | Expert-drafted embedded cards (llm 1, 8) | Quantum Country is self-reported and observational, no controlled comparison (llm 1) | trial; cards themselves (retrieval, grade A) stay |
| System design | 40-minute session (sd 6) | graded weak by its own file; from group formats (NALSD 4 to 6 people, katas 3 to 5) | **trial**, split at the break point |
| System design | 100-point reasoning rubric scored by the tutor (sd 5a) | no validity study (sd 8); the tutor writes the key and marks it: postmortem cause 5 | keep, but key built only from named expert sources, and **cold transfer (ScaleDojo lab) is the judge** |
| System design | "2 to 3 options, drawback, risk" per decision; scoping boxed at 5 min (sd 1b) | n = 36 workshop, 12 teams, second-hand protocol studies; Atman compares freshmen with seniors, not solo adults | keep as a prompt, **thresholds trial** |
| Production | Readiness 0 to 10 with dead band (prod 5) | stated product design, self-selected survey, graded D (prod 8a) | **drop** |
| Production | "He is at about 88% first try", so fade fastest (prod 1a) | 88% is v1 compute questions on ML formulas (A1, B10), not messy exhibits. His record on meaning shows the opposite: savings from one side 0/2 (E11), direction of a wrong number 0/3 (E12) | fade the arithmetic fast, **not the meaning step**; add a placement test |
| Production | Speed bars (90 s, 5 min) and the mock 7/10 gate (prod 5) | exam pacing [S]; Schweser 70% is company-reported | **trial** |
| Code | AI in the loop is safe for learning (code 1, Kazemitabaar) | n = 69, ages 10 to 17 | trial; the Koli and 2026 findings (checked: N = 220, homework up, no exam gain, https://arxiv.org/abs/2607.27586 ) argue caution |
| Code | PRIMM order as the unit frame | r = .13, one quasi-experiment (code 8) | keep as order, not as engine |
| Code | EiPE 7-point purpose score, marked by the tutor (code 4, 5) | tutor-marked; replace with the rebuild-by-fresh-model test where possible | keep the test version |

Two factual faults found:
- `llm-behaviour.md` card fact "about 3.5 English characters per token for Claude" (llm 1). The same
  pricing file says Claude 4.7 and later use a tokenizer that makes about 30% more tokens
  (`private/.../anthropic-pricing.md` line 60). The unit prices Sonnet 5 (llm 5, item 10), so that card would be wrong.
- Two price tables: production prices Sonnet 4.6 at $3/$15 (prod 4a), LLM behaviour Sonnet 5 at $2/$10
  (llm 5). Both appear in that file, but he will meet both as "the price". Use one dated model everywhere.

---

## 4. Conflicting rules between the structures

| Rule | Conflict | One rule | Keep a difference? |
|---|---|---|---|
| Mastery bar | 9/10 (prod, recommended); kappa 0.70 (eval); 70/100 (design); 90% cells (code); 9/10 answer and reason (LLM) | **Mastered = skill bar on 2 sessions in a row, then the same bar cold at 7 days** | bars differ by skill (table 7b), because a rubric with partial credit and kappa are not percentages |
| Cold recheck bar | same bar (prod, LLM); "within 0.10" (eval); 70 (design); 80% vs 90% in session (code) | **cold bar = session bar** | no |
| Up and down | 4 different rules (2a) | **2 in a row at the bar: up one rung. 2 in a row below the floor (bar minus 20 points): down one rung.** A confident wrong answer (sure, and wrong) counts as below the floor | no |
| Fading | production fixed (worked, completion, own) whatever he scores; others by performance | **placement test and performance-based fading in all five** | LLM has no worked-example rung (concepts, Chen 2015) |
| When the expert answer shows | per trace (eval calibration); per batch (eval); per decision (design); mid-chain at first wrong link (prod step 3); after 2 failed hypotheses (code) | **never before he commits his answer for that item** | the item size differs by kind: a step for procedures (production chain, code trace), a label for classification, a decision for judgement. Production step 3 must wait until his chain is complete (B12: telegraphing flagged 4 times) |
| Stuck order | LLM: own answer, two options, picture, answer. Code: drops the picture. Design: "which worked case?", reasoning cards. Eval, production: none | **own earlier answer (D1 15/17), two options (D4 5/7), one everyday picture (D2 8/10), answer with the reason (C19). Never more prose (D6 0/5)** | design's reasoning cards may supply the two options |
| Reflection | code "no written reflection"; design ADR plus AAR; eval one rule | **the shared Close** (2a) | the ADR stays as design's product, not as its reflection |
| First answer format | production: short answer first, options after 2 misses (Adesope); LLM ConcepTest: 4 options first | keep both | yes: ConcepTest options are built from known wrong models; his direction questions went 0/3 open to 3/3 with two options (E12) |
| Recall schedule | FSRS vs fixed ladder | **FSRS for the one queue** | no |
| Price and token facts | Sonnet 4.6 vs Sonnet 5; 3.5 chars/token vs +30% tokens | one dated fact sheet shared by all five | no |

---

## 5. Fit with his record

### 5a. Repeats of failures he already reported

| Risk in the structures | His record | Fix |
|---|---|---|
| Jargon in step names and in-session words: Calibrate, Code (qualitative coding, which also collides with the Code skill), axial, kappa, ConcepTest, Refute, Conjecture, Crit, Twist, Steer, Parsons, EiPE, ADR, NALSD, DMAIC, hinge decision, one-way door | C1 broken 5 times; C5, C21, C33 | plain names (5b); every term through the glossary gate before first use |
| Eval's unit name "Calibrate, Label, Code, Check" does not match its own 8 steps (no "Label" or "Check" step, eval 2) | C28 "inconsistent" | name = the steps |
| Kappa is his main eval feedback from unit 1, but the ledger says "Not yet taught: Cohen's kappa" | E7: a rule never stated, then tested (6+) | teach kappa as a frequency table first (the file's own 4e method), before it is ever a bar |
| Eval capstone: 100 traces, "no expert shown until the end", 60 to 90 min (eval 4h); design real-case replay; open coding in 4d | case-01 open investigation: "What am I supposed to do here", "unstructured and pointless", stopped (C41 to C43) | stage every whole task: a job statement, 3 or 4 fixed stages, an expert comparison after each stage (Loibl, postmortem cause 3) |
| The part template is absent from 4 of 5 files (only LLM mentions a picture) | A12 80% vs A13 27% on the same day; tiny generic example first, strongest predictor (B1) | any new idea inside any unit arrives in the part template: problem, fix, tiny example, picture, paths, about 5 questions |
| One part per message stated only in code | C25; B8 | every unit is sent one step per message, 700 to 2,100 characters |
| LLM "Keep" step: he answers each new card once right after learning it | C22, C27: "don't repeat" | first card return is next day, never in the same unit |
| Five queues of daily recall, 12 to 14 min | C27 (dislikes repetition), cause 6 (re-testing is not re-teaching) | one 10-min queue, items with new surfaces |
| Cold "why" reasons scored at 9/10 for an LLM level | cold why-questions 0/4 (B10); Crouch: explanations reach only about 30% | reason score tracked, gate on answer plus one-line reason with the run in view; trial |
| Timed items (20 s, 90 s) | no record either way | trial and measure; stop if accuracy falls |

### 5b. Plain step names (proposal)

| Skill | Proposed steps |
|---|---|
| All | (daily) Recall. Unit: Commit, Check, Compare, Close |
| Evaluation | Warm-up labels (6 with the expert's reason), Label the batch, Group the failures, Compare with the expert, Count and decide, Close |
| LLM behaviour | Odd result, Pick and say why, Predict, Run, Explain, Wrong idea fixed, New case, Close |
| System design | Read the brief, First design, Numbers, Choices, Compare with the expert, What if, Decision note, Close |
| Production | Guess, Chain, Run, Lever, Quick set, Close |
| Code | Predict, Trace, Change, Find the bug, Tell the AI, Close |

### 5c. What worked and is dropped or weakened
- Everyday picture dropped from code's stuck order (D2 8/10).
- Short-question rhythm (A9, 5 to 10 short questions a round): kept in eval, code, production; the design
  crit has 7 written steps and few questions. Add 1 or 2 short checks after each design step.
- Decisions with numbers (C32, C39): kept in design and production; keep "state each option's effect on
  the target number" (B14) as a rule for design choices.

---

## 6. Order of starting the five tracks

Prerequisites from `curriculum-design.md` 4b: B1 to P1 to P7; P1 + P2 to D1 (design frame needs cost and
latency); C2, C3 to E1 (traces are JSON, counting is SQL); B2 to E5 (judges depend on repeatable output);
E6 to D3 (design class 2 needs retrieval metrics, sd 3a says so).
Load: each new track brings a new unit shape and about 8 step names. His record: 1 new thing a part 80%,
about 8 new things 0 answered twice (B5, A11). The postmortem's 14 methods in 50 days (section 1) is the
same failure in another form. No study tests staggered starts for one adult, so the order below is
**trial and measure**; it rests on 4C/ID and the prerequisite graph.

| Week | Starts | Why then | Running |
|---|---|---|---|
| 1 | **Code** (continues bootcamp and L3: predict, trace, crash / quiet / fine) and **LLM behaviour** | code is his most familiar format; LLM concepts 1 to 3 are prerequisites for three tracks | recall queue from day 1 |
| 3 | **Production** | needs B1 (tokens, week 1 to 2); short unit, his strength; supplies P1, P2 for design | code, LLM |
| 4 | **Evaluation** (placement first: he did L5 evals and L6 judge) | needs C2, C3 (has them) and B2 (week 2); kappa taught first | code, LLM, production |
| 6 | **System design**, Study variant first | needs P1 + P2 (production classes 1 and 2, weeks 3 to 5) | all |
| 7 to 8 | first full Design Crit; LLM drops to 1 unit a week after week 8 | | all five |

---

## 7. Verdict and the integrated specification

### 7a. Verdict per structure

| Structure | Verdict | Changes |
|---|---|---|
| Evaluation | keep with changes | plain names; kappa taught before used; judge bars on 24+ pooled traces; rapid round and 5-of-6 gate as trials; staged capstone; eval "Code" step renamed |
| LLM behaviour | keep with changes | cards into the shared queue, no in-unit card answering; LBCI a guide, not a gate; revote is a trial; fix the token and price facts; estimate items (F) move to production |
| System design | keep with changes | plain names; one step per message with short checks; formats 3, 5, 8, 9 after level 1; rubric keyed only from named sources, cold lab as judge; starts week 6 |
| Production | keep with changes | drop readiness 0 to 10; add a placement test; fade arithmetic fast but keep a worked "meaning" step (E11, E12); per-link reveal waits for his full chain; speed a trial |
| Code | keep with changes | picture back in the stuck order; shared Close instead of "no reflection"; AI steps stay level 2+ |
| The cross-skill layer | **redesign** | five recall queues, five calibration measures, five progress rules, four capstone clocks become one of each (below) |

### 7b. One mastery rule, skill thresholds

Mastered = the bar on 2 sessions in a row, then the same bar cold at 7 days. Up one rung after 2 at the
bar; down one after 2 below the floor (bar minus 20 points, or a sure-and-wrong answer).

| Skill | Bar (fixed) | Trial bars, reviewed after 8 weeks of data |
|---|---|---|
| Evaluation | kappa ≥ 0.70 and no missed fail, pooled over 24+ traces | rapid round 90% at 20 s; gate 5 of 6 |
| LLM behaviour | right answer with a right one-line reason, 2 surfaces | LBCI 9/10 on reasons |
| System design | 70/100 with every brief number met | 80 for level 3 |
| Production | 9/10 on a mixed set | 90 s pace; factor-2 estimate 80% |
| Code | 90% of trace cells; tests pass in 2 attempts | 5-min trace |

### 7c. The week (from week 8, all five running)

| Day | Session (minutes) |
|---|---|
| Mon to Sat | Recall, one queue, 10 |
| Mon | Evaluation unit 25 + rapid round 8 |
| Tue | Code unit 30 + LLM unit 20 (1 a week after week 8; 2 before) |
| Wed | Design Crit 40 (break point allowed) |
| Thu | Code unit 30 + rapid round 8 |
| Fri | Production unit 25 + design drill 15 (weak/strong pair) |
| Sat | one whole task, rotating so none collide: wk A eval analysis (staged), wk B design lab from the brief, wk C production mock incident, wk D code steer on the FBR assistant (45 to 90) + design drill 15 |
| **Total** | about 330 to 380 min, 5.5 to 6.3 h. Extra time, if wanted, goes first to design drills, then a 3rd rapid round, then code reps (1b) |

### 7d. Shared machinery
1. **One queue**: FSRS, 10 minutes a day, mixed across skills, new surfaces for number and code items.
2. **One confidence measure**: predicted score before every check; the gap is the calibration number for
   all five; sure/unsure per item in eval and LLM.
3. **One frame**: Recall, then Commit, Check, Compare, Close; one stuck order; one Close line into the queue.
4. **One dashboard**: per skill, the main score, the 7-day cold score, the prediction gap. Nothing else
   shown to him.
5. **One dated fact sheet** for prices and token rates, used by every skill.
6. **Change rule**: no format changes for 8 weeks; then only trial items in section 3 may change, and only
   on the measured cold score.
