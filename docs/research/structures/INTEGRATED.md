# The integrated learning system: five structures, one shared layer

Written 2026-09-24. This is the final specification before anything is built. It combines the five
structures in this folder (`evaluation.md`, `llm-behaviour.md`, `system-design.md`, `production.md`,
`code.md`) with the independent review (`review.md`), which kept all five with changes and redesigned
only the layer between them. Where this file and a structure file disagree, this file wins.

## 1. Why five structures

Each skill is a different kind of learning (Faiz's own analysis, C44), so each has its own session shape,
drawn from the experts who teach that kind of learning best:

| Skill | Kind of learning | Its structure, in plain words | Borrowed from |
|---|---|---|---|
| **Code** | a procedure built by practice; the machine checks every step | **Predict, Trace, Change, Find the bug, Tell the AI** (30 min) | computing-education research: tracing tables, Parsons problems, PRIMM, subgoal labels, explicit debugging, Prompt Problems, CS1-LLM |
| **LLM behaviour** | fixing wrong mental models, plus facts to keep | **Odd result, Pick and say why, Predict, Run, Explain, Wrong idea fixed, New case** (20 min) | physics education (Mazur, Hake, predict-observe-explain), refutation texts, Quantum Country and spaced cards |
| **Production** | applied maths and quality control; the weak point is choosing numbers and reading what they mean | **Guess, Chain, Run, Lever, Quick set** (25 min; every 4th week a 45-min mock incident) | CFA and actuarial prep, Mahajan's estimation, Deming, SRE error budgets |
| **Evaluation** | seeing failures, labelling to a standard, building the list of failure types, reasoning with counts | **Warm-up labels, Label the batch, Group the failures, Compare with the expert, Count and decide** (25 min) + 8-min rapid rounds | perceptual learning (Kellman), rater training, qualitative coding, Gigerenzer's count trees, audit training, Hamel and Shreya |
| **System design** | judgement with many valid answers | **Read the brief, First design, Numbers, Choices, Compare with the expert, What if, Decision note** (40 min); the first two designs of each type are "guess the architect's move" | architectural katas, Google SRE design exercises, Amazon memos, AWS Well-Architected, chess master-game study |

Every unit ends with the same **Close** line ("next time I see X, I do Y"), which goes into the shared
recall queue.

## 2. The shared layer (one of each, not five)

1. **One recall queue.** FSRS scheduling, about 10 minutes a day, mixed across all five skills. Number and
   code items always come back with new numbers or new code, never the same surface.
2. **One confidence measure.** Before every check he predicts his score; the gap between prediction and
   result is the calibration number for all five skills.
3. **One frame inside every unit.** Commit (his answer first, with a reason), Check (run, test, or key),
   Compare (with the expert, one decision at a time), Close.
4. **One stuck order.** His own earlier answer, then two options, then one everyday picture, then the answer
   with a reason. Never more prose.
5. **One mastery rule.** The skill's bar on 2 sessions in a row, then the same bar cold at 7 days. Up one
   rung after 2 at the bar; down one after 2 below the floor (the bar minus 20 points, or a confident wrong
   answer).
6. **One dashboard.** Per skill, only three numbers: the main score, the 7-day cold score, the prediction gap.
7. **One dated fact sheet.** Prices, token rates and limits, taken from the providers' official pages on the
   day it is built, with the date on every line; every skill uses it. (The review found two structures
   using different model prices and an outdated characters-per-token figure.)
8. **One delivery rule.** One step per message; the part template where a step explains something; plain
   words, with every new term explained in the sentence where it first appears; every number produced by running code.
9. **One change rule.** No format changes for 8 weeks. After that, only items marked "trial" may change, and
   only when the 7-day cold score says so.

## 3. Mastery bars per skill

| Skill | Fixed bar | Trial (reviewed after 8 weeks of data) |
|---|---|---|
| Code | 90% of trace cells right; tests pass within 2 attempts | 5-minute trace pace |
| LLM behaviour | right answer with a right one-line reason, on 2 different cases | the 10-item concept check (a guide, not a gate) |
| Production | 9 of 10 on a mixed set | 90-second pace; estimates within a factor of 2 on 80% |
| Evaluation | agreement with the expert (kappa, taught before it is used) of 0.70 or more, and no missed failure, pooled over 24 or more traces | rapid round 90% at 20 seconds; the 5-of-6 warm-up gate |
| System design | 70 of 100 on the reasoning rubric, with every number in the brief met | 80 for level 3 |

## 4. Start order (so no more than about one new thing at a time)

| Week | Starts | Why then |
|---|---|---|
| 1 | **Code** and **LLM behaviour** | code is his most familiar format; LLM concepts (tokens, sampling) are prerequisites for three other tracks |
| 3 | **Production** | needs tokens and pricing from weeks 1-2; his strength; supplies the cost and latency numbers design needs |
| 4 | **Evaluation**, after a placement check (he already did L5 and L6) | needs code reading and SQL (he has them) and repeatable-output concepts (week 2); agreement statistics taught first |
| 6 | **System design**, "guess the architect's move" first | needs production's cost and latency classes |
| 7-8 | first full design session | all five running |

This order rests on the prerequisite graph and 4C/ID, and on his record that about 8 new things at once got
no answers; no study tests staggered starts for one adult, so it is a trial and is checked at week 8.

## 5. The week, once all five run (from week 8)

Workload is not a constraint (C46), so extra time goes where the evidence says more practice adds learning:
system design (judgement grows with the number of cases), evaluation rapid rounds (until the saved traces for
a task class run out), and code practice (until his repeat errors E1 to E4 stop). It does not go to more
flashcards or more production drills, where spacing, not volume, is what helps.

| Day | Sessions (minutes) |
|---|---|
| Every day | Recall queue 10 |
| Mon | Evaluation unit 25 + rapid round 8 |
| Tue | Code unit 30 + LLM behaviour unit 20 (two LLM units a week until week 8, then one) |
| Wed | Design session 40 |
| Thu | Code unit 30 + rapid round 8 |
| Fri | Production unit 25 + design drill 15 (write your answer, then compare with a weak and a strong expert answer) |
| Sat | Design session 40 + one whole task, rotating: week A evaluation analysis, week B a ScaleDojo design lab from the brief, week C production mock incident, week D code: steer the AI on the FBR tax assistant (45-90) |
| Sun | rapid round 8 + design drill 15 (optional) |
| **Total** | about 7 to 8 hours a week |

## 6. Where the evidence is weakest (these are trials, measured and adjustable after 8 weeks)

- The 40-minute design session length and the tutor-scored design rubric: no validity evidence yet; the cold
  ScaleDojo lab score acts as the outside check.
- The evaluation rapid round and warm-up gate: strong in radiology and aviation, untested on AI outputs.
- The LLM-behaviour "change your answer after discussion" step: tested with classmates, not a solo learner.
- Production's fast fading: his 88% came from arithmetic, but he scored 0 of 5 on judging what a number means
  (E11, E12), so the worked "what it means" step stays until he passes it cold.
- The start order and the weekly dose.

## 7. How we know it is working (one dashboard)

| Measure | Healthy | Alarm |
|---|---|---|
| 7-day cold score, each skill | at or near the bar | 10 or more points below the in-session score |
| Prediction gap | 10 points or less after 4 weeks | above 20 |
| Outside tasks (ScaleDojo lab from the brief, a new product's traces, hidden code tests) | at the bar | below it |
| Early warning | high scores inside sessions with low 7-day cold scores: it is teaching recognition, not skill |

## 8. What is still needed before building

- Install the tools the LLM-behaviour and code units run (a token counter and a small local model, or recorded
  outputs), with his approval.
- Build the fact sheet from official pricing pages.
- Prepare the first two weeks of material (code and LLM behaviour) from the saved expert sources, checked
  before any session.
- Keep the machinery small: one queue, one dashboard, one script that enforces the step order.
