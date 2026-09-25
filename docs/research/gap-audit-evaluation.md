# Gap audit: the evaluation skill, from research to what Faiz receives

Written 2026-09-25, after C49 ("you didn't show me a worked example, you're overloading me immediately, you
didn't explain the code"). No evaluation unit exists yet, so this audit checks the design every evaluation
unit will be built from, link by link, and ends with the unit template those units must follow and a fully
written first unit.

**The chain checked.** Research base (`curricula/judgement-training.md`, `skill-methods.md`,
`teaching-structure.md`, `method-effectiveness.md`, `teaching-craft.md`, `curriculum-map.md`,
`expert-curricula.md`, `huggingface.md`, `scaledojo-method-analysis.md`, `recommended-method.md`,
`postmortem.md`, `private/research-base/evaluation/`, `private/research-base/learning-methods/`) →
`structures/evaluation.md` → `structures/INTEGRATED.md` → `.claude/skills/faiz-teach/SKILL.md` →
`learn/engine.py`, `learn/check_unit.py` and the Stop hook `hooks/teaching-guard.py`. His rules and record:
`docs/learning-evidence.md` (A1 to E12, C1 to C49). `structures/review.md` was read as the link between
evaluation.md and INTEGRATED.md.

**What was run.** The HW3 expert key (`private/research-base/evaluation/repos/recipe-chatbot/homeworks/hw3/
reference_files/labeled_traces.jsonl`) was loaded in Python: 101 traces, 75 PASS, 26 FAIL, 94 marked HIGH
confidence and 7 MEDIUM; the median bot reply is 2,011 characters (shortest 1,120, longest 3,232). HW2's
`query_response.jsonl` was loaded: 250 rows with only `id`, `query`, `response`, no labels. Agreement numbers
below were computed with a small kappa function (marked "run"). Every trace used in the sample unit was read
in full, and each pass trace was checked for a hidden ingredient that would break its diet.

**Severity.** Blocker: he cannot learn the skill as built, or the build repeats a failure he already
reported. Major: an expert practice is dropped, weakened or contradicted in a way he will feel in the first
units. Minor: a real gap that will not stop the first units.

---

## Verdict

The research base describes how experts train raters and error analysts: first the standard, then
worked examples of labelled cases with the expert's cues, then practice with feedback after every case,
then blind practice compared with the expert, with the statistics taught as counts before they are used.
Almost all of that was lost between `skill-methods.md` and the checker. `evaluation.md` kept the rating and
comparison half of frame-of-reference training and cut the teaching half; it cut the worked-example ladder
to "one step, the first time a task class appears"; INTEGRATED dropped even that; SKILL.md has no place
for a worked example; and `check_unit.py` fixes six evaluation step names with no worked-example step, so a
unit that passes the checker cannot contain one. On top of that, the first unit as specified asks for about
12 new things, uses kappa as feedback before kappa is taught, puts 12 to 24 full traces (about 24,000 to
48,000 characters) into single messages, and makes per-trace feedback impossible because one step is one
message and the hook blocks key text. Built as specified, the first evaluation session would repeat
exactly what he reported after the first code session.

The design is fixable without new research. Every fix below uses material already saved: the HW3 criterion
and diet rules, the HW3 key's written reasons, the Cartwheel HW4 worked example, Hamel's NurtureBoss notes,
and the methods already graded in the research base.

**Counts: 5 blockers, 16 major, 7 minor (28 findings).**

---

## 1. What the research says experts do (the reference for every finding)

| # | Expert practice | Where the research base records it | Original expert source |
|---|---|---|---|
| R1 | Study worked examples first, then completion, then fading, then independent work; "full ladder, slow" for evaluation; 2 worked examples per problem type | skill-methods.md:84-111 (C1), :237-243 (D2); method-effectiveness.md:122, :155; recommended-method.md:46, :61; curriculum-map.md:20-32 | van Gog, Kester and Paas 2011; Renkl and Atkinson 2003; Renkl 2002 (`learning-methods/renkl-2002-smooth-transitions-fading.md`); Atkinson et al. 2000 (`atkinson-2000-learning-from-examples.md`) |
| R2 | Frame-of-reference rater training: learn the dimensions, see behaviour examples at each level, rate practice cases, compare with expert true ratings and discuss the gaps | evaluation.md:40 | Woehr and Huffcutt 1994; Roch et al. 2012 (d = 0.83 and 0.50) |
| R3 | Essay-scoring calibration: a 10-exemplar calibration set before scoring, pass mark, no answer far off | evaluation.md:41 | ETS / GRE (EJ1238527) |
| R4 | Modelling: the expert does the task and says the hidden cues and decisions aloud; show cue → what it means → what to do; show a dead end; model on a parallel case | judgement-training.md:21-35, :197, :202-213 | Collins, Brown and Newman; Klein (over 80% of decisions by recognising cues); Mamede modelled reflection |
| R5 | Content from captured expert reasoning; experts omit about 70% of their decision steps when they teach | method-effectiveness.md:67 (row 14); postmortem.md:90-93 | Cognitive task analysis meta-analysis, g = 0.87 |
| R6 | Perceptual learning: many short classification trials with feedback after each, concepts taught before the module | evaluation.md:37-39 | Kellman (PLMs), Krasne et al. |
| R7 | Feedback after each calibration case with the reason; after a batch for blind labelling; learner explains first, then sees the reason | evaluation.md:201-207; method-effectiveness.md:53, :86 | Kulkarni calibrated peer review; Bonner and Walker; Earley 2001; Kulik and Kulik 1988 |
| R8 | Teach rates as counts (a frequency tree or table) before any formula | evaluation.md:44 | Gigerenzer and Sedlmeier (75 to 90% vs 60%; rule training fell to 20% at 5 weeks) |
| R9 | Qualitative coding needs volume: 30+ traces, to saturation; a codebook entry has a definition, when not to use it and a close negative; 5 to 8 modes with 3+ positives each | evaluation.md:43; `hamel-husain/evals-faq.md` l.230-238, l.297; `repos/cartwheel-homeworks/homework/module-2/hw4.md` l.96-141 | Hamel Husain and Shreya Shankar; MacQueen; Hruschka |
| R10 | Low load: one new idea per step, under 150 words before the first answer, confusable ideas taught on different days | teaching-craft.md:115-116 (T11, T12), :131 (T27), :148, :157; teaching-structure.md:142-144 | Math Academy knowledge points; Sweller; 4C/ID |
| R11 | Look-alike cases cause confident errors; add them after the basics, with a reflection table | judgement-training.md:59-61, :199, :261 | Mamede 2010, 2012, 2019 |
| R12 | A fixed frame every unit, enforced by the system | teaching-structure.md:129 (A6), :195; recommended-method.md:32-33 | Hello Interview, ByteByteGo, Hamel; LLM-tutor RCTs (ai-tutoring.md) |
| R13 | Mastery bar plus a 7-day recheck; placement by a first-step test on the same kind of task | method-effectiveness.md:55, :123; skill-methods.md:46, :238-239 | Kulik et al. 1990; Kalyuga and Sweller (`kalyuga-2007-expertise-reversal-rapid-assessment.md`) |
| R14 | After-action review: expected, actual, why, what to keep and change | judgement-training.md:137, :245 | Tannenbaum and Cerasoli meta-analysis, d = 0.67 |

His own record sets the delivery limits these practices must meet: one new thing per part (B5, 80%) vs about
8 (0 answered, twice); every rule a question relies on stated first (B6, E7); messages of 700 to 2,100
characters (B8); about 5 questions per message (B9); 80% first try with the part template vs 27% without it
on the same day (A12, A13); worked examples as his reference point (C45); "explain and TEACH, not just give
me a skeleton shape to copy" (C20); C49.

---

## 2. Findings, in chain order

### Link 1: research base → `structures/evaluation.md`

**F1. [blocker] The worked-example ladder was cut to one labelling step, used once per task class.**
- Where: evaluation.md:56-57 (challenge 3), :83-85.
- Research says: evaluation is "full ladder, slow", two worked examples before any attempt, a nine-part
  anatomy (goal, givens, read and note, group, count, turn one type into a check, measure the checker, did
  the fix work, common wrong turns) (skill-methods.md:90-111, R1); method-effectiveness.md:155 and
  recommended-method.md:61 repeat it. Erroneous examples only after 2 correct ones (skill-methods.md:92).
- Built instead: challenge 3 argues the ladder "ignores that he has done L5 and L6" and replaces it with 6
  traces showing the expert's open code, once per task class. Grouping, counting, the judge and the fix
  measurement are never modelled before he does them. L5 and L6 never had him label real traces against a
  standard (learning-evidence.md:203-204, :213-219), so the premise is wrong.
- Fix: restore the ladder per node, not per task class: each node (label, group, count, judge, validate,
  measure a fix) opens with 2 worked examples of that node, then one completion item, before any blind
  practice. Placement (F15) may skip the first worked example only for a node he has done before.

**F2. [blocker] Frame-of-reference training kept its second half and dropped its first.**
- Where: evaluation.md:72 (step 3 Calibrate), :146-152 (4b).
- Research says: FOR is four moves in order: learn the dimensions, see examples at each level, rate
  practice cases, compare with the expert (evaluation.md:40 itself, R2). ETS raters calibrate before scoring
  live essays (R3); the calibration set is a check after training, not the training.
- Built instead: the first thing he does in every unit is label expert-labelled traces. No step states the
  standard (for HW3 the course's own criterion and diet rules, `hw3/README.md` l.111-146) or shows a pass and
  a fail at each level before he labels. He meets the rule only through the expert's feedback after he has
  already guessed. This is C17 ("teach me the concept before you test me") and E7 (a rule never stated,
  then tested).
- Fix: every unit on a new product opens with the standard (the written rule, quoted from the source, with
  the source's own pass and fail examples) and 2 worked examples, before any warm-up label.

**F3. [major] Modelling of the expert's cues is not specified anywhere.**
- Where: evaluation.md:83-85 ("the expert's open code and the reason beside each").
- Research says: show the reasoning as cue → what it means → what to do, name what triggered each move, show
  a dead end, finish with a 3 to 5 line replay (judgement-training.md:197, :207-212, R4); build content from
  captured expert reasoning because experts omit most decision steps (method-effectiveness.md:67, R5).
- Built instead: a label and a reason next to each trace. That is an answer key, not a model of how an
  expert reads a trace (where to look first, what to ignore, which line decided it).
- Fix: every worked example is laid out as numbered moves: (1) read the rule first, (2) what in the request
  to ignore and why, (3) the line that decides it, (4) what it means under the rule, (5) the label, (6) one
  dead end the expert did not take. Each move is taken only from the source key's written reason and the
  source's rule text (the tutor rearranges, never adds).

**F4. [major] The first unit asks for about 12 new things in 25 minutes.**
- Where: evaluation.md:68-77.
- Research says: one new term per part, under 150 words before the first answer (teaching-craft.md:148,
  :157, R10); knowledge points of one step each (T11); confusable ideas on different days (T27, :131). His
  record: about 8 new things got no answer twice (B5, A11).
- Built instead: in one unit: trace, label, cue, calibration gate, open code, sure/unsure, codebook entry
  (name, binary definition, when not to use, close negative), expert taxonomy, match/merge/missing, kappa,
  fail recall, lenient or strict bias, negotiated agreement, pivot by type x cost, a changed fact.
- Fix: one node per unit. Unit 1 teaches only "label an output against one written rule". Agreement beyond
  chance, open coding, grouping, counting, judges each get their own unit with their own worked examples, in
  Hamel's order (evaluation.md:115-116).

**F5. [major] "Group the failures" on 12 traces cannot be done, and on HW3 it makes no sense.**
- Where: evaluation.md:74 (step 5 Code), :161-169 (4d).
- Research says: open then axial coding needs at least 30 traces and runs to saturation
  (`evals-faq.md` l.230-238, l.297); Cartwheel asks for 5 to 8 modes with at least 3 confirmed positives each
  (`hw4.md` l.126-141); evaluation.md's own 4d uses 100 traces.
- Built instead: every unit groups the open codes from a 12-trace batch. At HW3's rate (26 of 101 fail, run)
  a 12-trace batch holds about 3 fails, and HW3 has one criterion ("We picked dietary adherence because the
  rules are clear and objective", README l.23), so there is nothing to group. This is the kind of question
  he called senseless (C42, C43).
- Fix: grouping is its own node, taught on a set built for it (NurtureBoss, Hamel's own notes and axial codes,
  `recipe-chatbot/lesson-4/nurtureboss_traces_labeled.json`, 100 traces; Cartwheel HW4 worked example),
  after labelling is at the bar. Never in a unit whose product has one criterion.

**F6. [major] Kappa and fail recall are used as feedback from unit 1, and nothing teaches them.**
- Where: evaluation.md:75 (step 6), :206; carried to INTEGRATED.md:53 ("kappa, taught before it is used")
  and :62 ("agreement statistics taught first") with no unit, step or owner.
- Research says: teach rates as counts first (Gigerenzer, R8); evaluation.md applies this to the judge only
  (4e, :171-177). The review flagged it (review.md:148). His record: "Not yet taught: Cohen's kappa"
  (learning-evidence.md:218); rules tested before they are taught fail (E7, 6+ cases).
- Built instead: the first batch ends with "kappa, fail recall, lenient or strict bias".
- Fix: until the kappa unit, feedback is counts only ("you agreed on 10 of 12; the expert failed 3 and you
  caught 2"). The engine still computes kappa for the bar, but it is not shown. The kappa unit (eval-02) opens
  on the problem, taken from evaluation.md:51-53: on HW3 a labeller who passes everything agrees on 74.3% and
  has kappa 0 (run), then builds kappa from a 2 by 2 count table, never as a formula first.

**F7. [major, cohesion] "TPR" points in opposite directions in two places he will read.**
- Where: evaluation.md:174-177 ("TPR 0.90 (on passes)"), following HW3 (README l.161: TPR is "How often the
  judge correctly identifies adherent recipes"); `docs/glossary.md`:39-40 and L6 (catch rate = TPR = share of
  FAILs caught); evaluation.md also adds a third name, "fail recall".
- Research says: one running example, fixed names, same numbers throughout (teaching-craft.md T8); E12 shows
  he already struggles with which way a rate bends a decision.
- Built instead: the same letters mean catch-the-fails in the glossary and catch-the-passes in the judge
  worked example and the pass-rate correction formula.
- Fix: keep his taught words (catch rate on fails, clear rate on passes) everywhere; when HW3 or `judgy`
  material is shown, add one line converting it ("HW3 calls the pass rate TPR; in our words that is the
  clear rate"). Drop "fail recall" as a word he sees; use "catch rate".

**F8. [major] The "expert key" is not reliably expert, and it contradicts itself.**
- Where: evaluation.md:149-152, :297 (author unknown), :285 (Claude excluded as expert labeller because it
  has no outside anchor).
- Research says: FOR compares the learner with expert true ratings (R2); ETS calibrates against exemplars
  scored by trained raters (R3).
- Found (run): every HW3 record carries a fluent `reasoning` paragraph and a HIGH or MEDIUM `confidence`
  field, the pattern of model-written labels (an inference; the course does not say who labelled). The
  diet definitions are marked "(Reference from OpenAI o4)" (README l.129). The key is inconsistent: trace
  27_40 (raw vegan soup) fails because sautéing and simmering exceed 118°F (48°C), while trace 9_25 (raw
  vegan salad) passes with "toasted sunflower seeds" (toasting is heating); 35_15 (paleo) passes with optional
  "cooked bacon bits", arguably a processed food, while 26_30 and 46_3 fail on optional ingredients; 48_3 fails a quinoa salad at MEDIUM
  confidence because feta "could be" cross-contaminated. The same weakness that excluded Claude is in the
  key.
- Fix: for worked examples, calibration and the blind batch, use only HIGH-confidence traces whose label
  follows directly from the quoted rule, read in full by a person before use (the sample unit below does
  this; 31 traces were read). Keep a "disputed" list (9_25, 35_15, 48_3 so far) for a later unit where he
  argues against the key with evidence (negotiated agreement, evaluation.md:75). Prefer human-annotated
  sources for open coding (NurtureBoss notes are Hamel's; Cartwheel's worked example is the course
  authors').

**F9. [major] The rapid round has no answer key, and the keyed pool is far smaller than the volume planned.**
- Where: evaluation.md:136-144 (4a uses HW2 `query_response.jsonl` against the HW2 taxonomy), :58-59,
  :241-243; INTEGRATED.md:71-73.
- Research says: PLMs show the right answer after every item, and the concepts are taught before the module
  (evaluation.md:37, R6).
- Found (run): HW2 has 250 rows with no labels at all, so every rapid-round answer would be written by the
  tutor, the practice evaluation.md:285 excludes. HW3 has 26 FAILs, drawn from "60 challenging edge cases"
  (README l.45); after removing carb-count diets (which need nutrition knowledge no source teaches) and
  disputed labels, by my count about 13 clean FAILs remain. The sample unit and its cold check use 12 of them.
- Fix: build the rapid-round and parallel-unit banks only from keyed, person-checked items; count the clean
  pool per task class before scheduling; where the pool is short, get more keyed items (a person labels
  HW3 `raw_traces.jsonl` against the quoted rule, or use HW5's 96 traces with `first_failure_state` for class
  3). Never let the tutor supply the key.

**F10. [major] No rule orders items so that first attempts mostly succeed.**
- Where: evaluation.md (no ordering rule for calibration or batch items).
- Research says: look-alikes cause confident errors and belong after the basics, with a reflection table
  (R11); worked examples first for novices (R1); his record is about 80% first try when a part follows the
  template and 27% when it does not (A12, A13). The research base does not contain a measured optimal
  success rate; Math Academy reports 93% of lessons passed first time (self-reported,
  method-effectiveness.md:97), and Khan's "Familiar" band is 70 to 85% (skill-methods.md:64).
- Built instead: the batch is drawn from HW3, whose fails are deliberately hard edge cases.
- Fix: order every set clear → subtle: the first warm-up item repeats the worked example's cue on a new
  surface; look-alikes (a bot that calls its own recipe "sugar-free", an optional ingredient, a diet hidden
  in the profile, not the request) come only after the rule they depend on is stated; disputed labels never
  appear in scored sets. Target about 80% first try in unit 1 and adjust from his results.

**F11. [minor] The structured reflection table was dropped without a reason.**
- Where: evaluation.md:73 (blind batch keeps only "sure or unsure").
- Research says: judgement-training.md 8d (:242) uses the reflection table on 3 hard traces; Mamede: lower
  scores on the day, higher a week later (:59); for novices only after worked examples (:261).
- Fix: from level 2, every trace he marks "unsure" gets the table (evidence for fail, against, expected but
  absent) before the reveal.

**F12. [minor] The after-action review shrank to one line.**
- Where: evaluation.md:77 → INTEGRATED.md:21-22 (Close: "next time I see X, I do Y").
- Research says: four parts (expected, actual, why, keep or change); debriefs d = 0.67 with structure (R14).
- Fix: the Close step asks two things: what he expected (his predicted agreement) against what happened (the
  count), then the rule line. Two short answers, not four paragraphs.

### Link 2: `evaluation.md` → `INTEGRATED.md`

**F13. [major] The "Frame and predict" step was dropped: no step states the job.**
- Where: evaluation.md:71 → INTEGRATED.md:18 and review.md:162 (steps start at "Warm-up labels").
- Research says: open with the decision or the failure and its stake (teaching-craft.md T1; judgement-training
  8d "Case", :240). His rules: "Explain the problem with the right context and background" (C34); every unit
  states its goal in its first step (C41 resolution).
- Built instead: the first message of every unit is a trace to label.
- Fix: step 1 of every unit is "The job and the rule", in the part template (problem with context, fix,
  tiny example, picture, paths, about 5 questions).

**F14. [major] The bar moved: a calibration-gate rule became the mastery bar, and the levels vanished.**
- Where: INTEGRATED.md:53; evaluation.md:118-123 (three levels), :209-215.
- Research says: evaluation.md sets novice kappa 0.60 and catch 0.75, competent 0.70 and 0.85, and applies "no
  expert-fail labelled pass" to the 6-trace calibration gate, not to mastery (:212). Review: pool over 24+
  traces because one trace flips the bar (review.md:99).
- Built instead: one bar for every level: kappa 0.70 and no missed failure, from the first unit. Run: on 24
  traces with 6 fails, 23 right with one missed fail (kappa 0.88) fails the bar; 22 right with two false
  alarms (kappa 0.80) passes it. At level 1 that sets the competent bar for a novice.
- Fix: level 1 uses the novice bar (kappa 0.60, catch 0.75) pooled over his last 24+ blind labels; level 2
  uses INTEGRATED's bar. Keep "never pass a trace the expert failed" as the warm-up gate (trial).

**F15. [major] Placement rests on a premise the record does not support.**
- Where: INTEGRATED.md:62 ("after a placement check (he already did L5 and L6)").
- Research says: a first-step test must use the first step of the same task (Kalyuga, R13).
- Built instead: L5 was test cases and gates; L6 was SQL counts and one judge (learning-evidence.md:203-204,
  :213-219). Neither had him read a real output against a written standard. A binary label alone is right
  half the time by chance.
- Fix: placement = 2 excerpts (one pass, one fail), each answered with label + the deciding line + the rule
  it breaks. Both fully right → skip worked example 1 of the label node only; the standard step is never
  skipped on a new product; nodes he has never done (grouping, judges) are never skipped.

**F16. [major] INTEGRATED omits evaluation.md's only worked-example rule and its fading rule.**
- Where: evaluation.md:83-85, :125-130 → INTEGRATED.md:18, :34-36 (one generic up/down rule).
- Research says: rungs within a class, down one after 2 misses, restart at a worked example for a new class
  (skill-methods.md:237-243; R1).
- Built instead: the integrated specification, which "wins" on conflict (INTEGRATED.md:6), has no worked
  example for evaluation at all, so every later file follows it.
- Fix: add to INTEGRATED 1 and 3: "each evaluation node opens with 2 worked examples and 1 completion item;
  rungs: worked → completion → blind with warm-up → blind without; a new node or product restarts at the
  worked examples".

### Link 3: `INTEGRATED.md` → `faiz-teach/SKILL.md`

**F17. [major] SKILL.md names worked examples as his reference point but gives them no place in a session.**
- Where: SKILL.md:17-18 (C45 cited) vs :23-45 (session steps: recall, unit steps verbatim, mark, cold).
- Research says: R1; C45; C49.
- Built instead: the tutor is told to send the unit's steps verbatim; since the unit format has no worked
  example step (F22), nothing in the session produces one.
- Fix: add to "How a session runs": "A unit on a new node or product starts with its standard and two
  worked examples; they are steps like any other and are never skipped unless placement allows it."

**F18. [blocker] One step per message, the step list and the hook make per-trace feedback impossible.**
- Where: SKILL.md:31-34; check_unit.py:29-30; hooks/teaching-guard.py:103-105, :108-109.
- Research says: feedback after each calibration trace, with the expert label and reason (evaluation.md:205;
  Kulkarni; Bonner and Walker; R7); on disagreements he explains first, then sees the reason (:207, Earley);
  the gate branches ("else 4 more", :72).
- Built instead: "Warm-up labels" is one step, so its 6 traces go in one message and feedback comes after
  all 6. The expert's reasons live in the Key, and the hook blocks any Key line of 25+ characters from
  appearing in a message, so the reason cannot be shown as feedback at all. "Compare with the expert" is one
  step, so he cannot answer before the reasons are revealed. The gate has no branch.
- Fix: one warm-up trace per step (Warm-up label 1 to 6); the expert label and reason for trace n is written
  into the body of step n+1 (so it is shown text, not Key text); Compare is two steps (his numbers and his
  view of each disagreement, then the expert's reasons); the gate result is computed by the engine and
  printed for the tutor, with the branch written in the unit.

**F19. [minor] The stuck order does not fit a binary label.**
- Where: SKILL.md:54-56 ("(2) two options").
- Research says: D1 (point at his own earlier answer, 15 of 17) and D4 (two options) in his record.
- Built instead: a label already has two options, so rung 2 repeats the question.
- Fix: for labels: (1) point at the rule line, (2) point at the one ingredient or step line to check, (3) his
  own earlier worked-example answer, (4) the answer with the key's reason.

**F20. [minor, cohesion] Two confidence scales.**
- Where: SKILL.md:38 ("confidence 4 or 5") vs evaluation.md:73 ("sure or unsure").
- Fix: evaluation uses "sure / not sure" per label; the engine counts "sure and wrong" as the confident-wrong
  number.

**F21. [minor, cohesion] SKILL.md cites C1 to C46 and applies C48 to code only.**
- Where: SKILL.md:11, :62; check_unit.py:164-165.
- Fix: cite C1 to C49; apply "How this code works" to any code block in any skill (evaluation units will show
  SQL and Python for counts and judges).

### Link 4: `engine.py`, `check_unit.py`, the hook

**F22. [blocker] The checker's evaluation step list has no worked example, no standard, no completion step.**
- Where: check_unit.py:29-30 (six fixed names), :34 (optional steps exist only for code).
- Research says: R1, R2, R4, R12 (the frame is enforced by the system, so the system must contain the
  expert parts).
- Built instead: a unit that follows the research fails the checker ("steps must be, in order: ..."), and a
  unit that passes it cannot teach. The engine refuses to serve or record a unit that fails the checker
  (engine.py:263-266, :319-321), so the enforcement guarantees C49 happens again.
- Fix: replace the evaluation list with the template in section 4 (names with numbered warm-up and batch
  steps; "Use the labels" optional until its node).

**F23. [blocker] Message size is uncapped for traces.**
- Where: check_unit.py:161-163 (the 2,500-character cap counts prose outside code fences only).
- Research says: short segments with a check after each (teaching-structure.md:124, A1); under 250 words per
  segment (:144). His record: 700 to 2,100 characters worked; 10,440 characters with 51 questions was not
  answered (B8, B9, A11).
- Built instead (run): HW3 replies have a median of 2,011 characters. A 12-trace batch in one step is about
  24,000 characters with 36 answers (label, open code, sure); the 24-trace pool INTEGRATED implies is about
  48,000. Traces sit in fences, so the checker passes them.
- Fix: count fenced text too; cap a step at 2,500 characters including traces; at most 4 traces per step;
  traces shown as excerpts (request, diet on record, dish name, ingredient list, and only the step lines the
  label depends on), each marked "[steps cut: checked, nothing in them changes the label]".

**F24. [major] Nothing checks that a trace or its label comes from the source.**
- Where: check_unit.py:70-75 (fenced blocks stripped before number checks; "given:" lines exempt), :169-179
  (code-block checks run for the code skill only).
- Research says: expert material prepared and checked before the session (recommended-method.md:15, :81-82;
  postmortem cause 4, :84-93).
- Built instead: an invented or edited trace passes, a Key label that differs from the source passes, and any
  "cost of one failure" number can be added on a "given:" line (HW3 has no cost data, so the Count and decide
  step invites invented numbers).
- Fix: an evaluation unit header lists `traces: <source file>` and each step names its trace ids; the checker
  confirms every excerpt line is a substring of that record's text, and every Key label equals the source
  label; "given:" lines are not allowed in evaluation units.

**F25. [major] Kappa is typed in by the tutor, not computed; the cold rule differs in three places.**
- Where: engine.py:48 (`traces >= 24` inside one unit; `missed_fail` defaults to 1), :330-334 (kappa,
  missed_fail, traces entered as step values), :348 (score = mean of steps or kappa x 100), :351 (cold passes
  if `Cold x 100 >= 70`); SKILL.md:35-39 (marks per step; no rule for labels).
- Research says: every number produced by running code (INTEGRATED.md:41-42; SKILL.md:66-67); pool over 24+
  (review.md:99); evaluation.md:225 cold rule "10 unseen traces, kappa within 0.10 of the last unit".
- Built instead: the tutor would count agreements and compute kappa by hand; one unit must hold 24 traces
  (F23); a forgotten `missed_fail=0` fails a passing unit; the cold check is a share of 0.70, not agreement.
- Fix: `engine.py labels <unit> --his "P,F,..." [--sure "1,0,..."]` reads the Key labels from the unit,
  computes agreement, catch, clear, kappa and the pooled bar over the last 24+ blind labels, prints the counts
  for the Compare step, and records the result; the same command with `--cold` applies evaluation.md's cold
  rule (trial, noisy at 10 items).

**F26. [major] The rapid round and the placement check are print-only, and both land on day 1.**
- Where: engine.py:132-133, :139-141.
- Research says: PLM items need a key, a time limit, retirement after 3 spaced correct answers (evaluation.md
  :39, :130) and concepts taught first (R6); placement is recorded and moves the rung (R13).
- Built instead: text lines. Week 4 sitting 1 lists placement, the first unit and a rapid round together:
  three new formats in one sitting (B5). Nothing records placement or rapid-round results.
- Fix: rapid rounds start at the second evaluation sitting, only on categories already taught, from a keyed
  bank; record results; placement is recorded with `engine.py outside` or a new `place` command.

**F27. [minor] The jargon gate does not know the evaluation words.**
- Where: docs/glossary.md:52 (watchlist has kappa, TPR, TNR; lacks trace, label, open code, codebook, close
  negative, calibrate, catch rate as used here); check_unit.py:137-150 accepts any defining clause.
- Fix: add the evaluation terms; a term used in a step must be taught in the unit's "job and rule" step or an
  earlier unit.

**F28. [minor] Excerpt attribution is not required.**
- Where: check_unit.py (no rule); the HW3 material is GPL v3 (`recipe-chatbot/LICENSE`).
- Fix: each evaluation unit header carries `source licence:`; excerpts name their trace id in the Key.

---

## 3. Prioritised fixes

Do these before any evaluation unit is written (C49 overrides the 8-week freeze for these):

1. **Put the teaching half back** (F1, F2, F3, F13, F16, F17, F22): new evaluation template (section 4) in
   INTEGRATED 1, SKILL.md and `check_unit.py` STEPS: The job and the rule → 2 worked examples → finish the
   expert's work → warm-up labels → label the batch → compare (two steps) → use the labels (from its node) →
   close.
2. **One node per unit, in Hamel's order** (F4, F5, F6): eval-01 label against one rule; eval-02 agreement
   beyond chance (kappa as counts); eval-03 look-alikes and arguing with the key; eval-04 open notes, taught
   from the Cartwheel worked example; later units group, count, judge, validate, measure a fix.
3. **Make feedback possible** (F18): one warm-up trace per step, expert reason in the next step's body, a
   two-step Compare, the gate computed by the engine.
4. **Cap the message and check the source** (F23, F24, F28): count fenced text, 4 excerpts per step, excerpts
   verified against the source record and label, no "given:" lines.
5. **Compute, do not type, the statistics** (F25, F14, F7): `engine.py labels`, level bars pooled over 24+,
   counts shown until kappa is taught, one set of rate names.
6. **Clean the key and the pool** (F8, F9, F10): HIGH-confidence, person-checked items only; a disputed list;
   count the clean pool before scheduling rapid rounds or parallel units.
7. **Then** F15, F26, F11, F12, F19 to F21, F27.

---

## 4. The corrected unit template (every evaluation unit)

Header (checked):
```
id: eval-NN
skill: evaluation
level: 1
node: label | agreement | look-alikes | open notes | group | count | judge | validate | fix
traces: private/research-base/evaluation/.../<file>   (source of every excerpt and Key label)
source licence: <licence>
scored: Label the batch 1, Label the batch 2, Label the batch 3
```

Steps, in this order, one per message, each ending **Your answer.**:

| # | Step name | What it does | Research | Hard rules |
|---|---|---|---|---|
| 1 | The job and the rule | Part template: the problem with context (4+ sentences: the product, who gets hurt by a miss, the decision the labels feed), the rule quoted from the source, the source's own pass and fail examples as the tiny example, one everyday picture, the paths, about 5 short questions | FOR dimensions (R2); T1; C34, C41; A12 | One new idea only. Every rule a later question needs is stated here (B6) |
| 2 | Worked example 1 | One trace, the expert's moves numbered: rule first, what to ignore, the deciding line, what it means, the label, one dead end; one focused question on the key move | R1, R4, R5 | Moves come only from the source rule and the key's written reason |
| 3 | Worked example 2 | A close negative of example 1: looks alike, opposite label, same moves | Cartwheel close negative (R9); contrasting cases (method-effectiveness.md:64) | Same layout as example 1 |
| 4 | Finish the expert's work | Completion: moves 1 to 3 done, he writes the label and the deciding line; feedback on his answer comes at the top of the next step | Backward fading (Renkl 2002, R1) | Same shape as the examples |
| 5-10 | Warm-up label 1 to 6 | One trace per step: label, deciding line, sure / not sure. Step n+1 opens with the expert label and reason for trace n | FOR, ETS, Kulkarni (R2, R3, R7) | Balanced 3 pass / 3 fail; first item repeats the worked cue; clear to subtle |
| 11 | Warm-up result | The last warm-up reason, the gate result (computed), his prediction for the batch | Gate (evaluation.md:72, trial); INTEGRATED 2.2 | Prediction asked with the data he needs (C39) |
| 12-14 | Label the batch 1 to 3 | 4 excerpts per step, no feedback until the end | Blind labelling (evaluation.md:73) | At most 2,500 characters per step including excerpts |
| 15 | Compare: your numbers | Counts from `engine.py labels`; each disagreement listed; he says whose label is right and which line, before any reason | Kulkarni bias feedback; Earley (R7) | Counts only until kappa is taught (R8) |
| 16 | Compare: the expert's reasons | Each disagreement's key reason; he may argue the key with a line from the trace | Negotiated agreement (evaluation.md:75); FOR discussion | Reasons are shown text, not Key text |
| 17 | Use the labels | The node's own task (group, count and decide, judge check). Absent until the node is taught; its first unit replaces steps 2 to 4 with worked examples of that task | Hamel's order (evaluation.md:115-116) | Never on a one-criterion product |
| 18 | Close | Expected vs actual (his prediction vs the count), then "next time I see X, I do Y" | AAR (R14) | Two short answers |

Then `## Cold` (7 days later: 10 new excerpts, same product, same rule, in 3 steps; rule per evaluation.md
5c, trial) and `## Cards` (each card with a second surface).

Checker rules for this template: the step names above in order (warm-up and batch numbered); steps 2 to 4
required when `node` is new or `level: 1`; every excerpt a substring of its source record; every Key label
equal to the source label; each step at most 2,500 characters including fences; no "given:" lines; every
code block with **How this code works**.

---

## 5. Sample first unit: eval-01, "Does the recipe respect the user's diet?"

Source of every trace, label and reason: Recipe Bot HW3, `private/research-base/evaluation/repos/
recipe-chatbot/homeworks/hw3/reference_files/labeled_traces.jsonl` (Husain and Shankar, AI Evals course,
GNU GPL v3); rule text and examples: `hw3/README.md` l.111-146. All 31 traces used (unit and cold check) are
HIGH confidence and were read in full; none is on the disputed list. Diets that need carbohydrate
knowledge (keto, low-carb, diabetic) are left out because no source teaches that knowledge. Excerpts keep
the request, the diet on record, the dish name and the ingredient list word for word; cooking steps are
shown only where the label depends on them.

Expected length: 17 messages, about 30 to 35 minutes (longer than INTEGRATED's 25; C46 says time is not the
constraint).

Header:
```
id: eval-01
skill: evaluation
level: 1
node: label
traces: private/research-base/evaluation/repos/recipe-chatbot/homeworks/hw3/reference_files/labeled_traces.jsonl
source licence: GNU GPL v3 (recipe-chatbot/LICENSE)
scored: Label the batch 1, Label the batch 2, Label the batch 3
```

### Message 1. The job and the rule

**The problem.** A recipe chatbot gets requests like "Nut-free lunch that's safe for my kid's school". Each
user's diet is on record next to the request: vegetarian, nut-free, paleo and so on. If the bot sends a
recipe that breaks that diet, the user may eat something they must not eat, and they stop trusting the bot.
The team that built it (the AI Evals course by Hamel Husain and Shreya Shankar) wants one number: how often
does the bot respect the diet? Before anyone can build an automatic checker for that, a person has to read
real replies and mark each one. That mark is called a **label** (pass or fail, decided by one written rule).
Today you learn to label the way their key does.

**The fix: one written rule, applied line by line.** The course's rule: "The bot should provide recipes that
actually meet the user's stated dietary restrictions." Each diet has its own short rule, and every recipe you
see today comes with its rule printed above it, so there is nothing to memorise.

**Tiny example (the course's own):**
- User asks for vegan pasta → the bot includes honey (not vegan): FAIL.
- User asks for vegan pasta → the bot uses nutritional yeast (a dried yeast with a cheesy taste) instead of
  parmesan: PASS.
- User asks for gluten-free bread → the bot uses regular soy sauce (contains wheat): FAIL.

**Picture.** You are an auditor ticking invoices against the company's spending policy. You do not care
what the invoice calls itself, or who sent it. You check each line against the policy. One line outside the
policy and the invoice fails.

**The paths.**
- Every ingredient fits the diet's rule, and no cooking step breaks it → PASS.
- Any one line breaks the rule → FAIL. That includes a line marked "optional" or an "X or Y" choice, because
  the user may follow it.
- What the bot says about its own recipe ("sugar-free", "perfect for a pescatarian diet") is a claim, not
  evidence. Only the ingredients and steps count.
- The request can be silent about the diet ("I want to eat healthy"). The diet on record still applies.

**Questions** (one line each):
1. Vegan pasta with honey: PASS or FAIL?
2. A recipe titled "Sugar-Free Chews" lists "1 tablespoon honey (optional)". For a sugar-free user: PASS or
   FAIL?
3. Which do you check a recipe against: the words in the request, or the diet on record?
4. One ingredient breaks the rule and nine fit. Label?
5. In the auditor picture, what plays the part of the spending policy?

**Your answer.**

Key (never shown): 1 FAIL. 2 FAIL (optional still counts; the title is a claim). 3 The diet on record. 4 FAIL.
5 The diet's rule. Score: not scored (teaching step). Stuck order: point at the path line that answers it.

### Message 2. Worked example 1

(Opens with one line of feedback on Message 1, then:)

**Watch how the expert labels one reply.**

```text
Request: "I don't like vegetables but I want to eat healthy"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Lemon Herb Grilled Chicken (Serves 2)
Ingredients:
- 2 boneless, skinless chicken breasts
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- Juice and zest of 1 lemon
- 1 teaspoon dried oregano or thyme
- Salt and pepper to taste
- Optional: fresh parsley or basil for garnish
[steps cut: checked, nothing in them changes the label]
```

The expert's moves:
1. **Rule first.** Before reading the recipe: the diet is vegetarian, so no meat or fish.
2. **Ignore what is not the rule.** "I don't like vegetables" and "healthy" are the user's wishes. They do not
   change what vegetarian allows, so they cannot decide the label.
3. **Find the deciding line.** "2 boneless, skinless chicken breasts".
4. **What it means under the rule.** Chicken is meat. Vegetarian excludes all meat.
5. **Label: FAIL.** The key's reason: "includes chicken breasts as the main ingredient... vegetarian... excludes
   all forms of meat, including chicken."
6. **Dead end not taken.** The request never says "vegetarian", so a reader who only reads the request would
   pass a healthy-looking chicken dish. That is why move 1 comes first.

**Question:** Which line decided the label: (a) "I don't like vegetables but I want to eat healthy" or (b) "2
boneless, skinless chicken breasts"? And in a few words, why does the other one not matter?

**Your answer.**

Key: (b). The request states wishes; the rule comes from the diet on record. Source: trace 38_22, FAIL.

### Message 3. Worked example 2

(One line of feedback, then:)

**Same main ingredient, different user.**

```text
Request: "Nut-free lunch that's safe for my kid's school"
Diet on record: nut-free
Rule: Nut-free: No tree nuts or peanuts
Recipe: Chicken and Veggie Wraps
Ingredients (for 2 servings):
- 2 large whole wheat tortillas
- 1 cooked chicken breast, sliced
- 1 small cucumber, thinly sliced
- 1 small red bell pepper, thinly sliced
- 1 carrot, grated
- 2 tablespoons plain Greek yogurt
- 1 teaspoon Dijon mustard (optional)
- Salt and pepper to taste
- Lettuce leaves (romaine or iceberg)
[steps cut: checked, nothing in them changes the label]
```

The expert's moves:
1. **Rule first.** Nut-free: no tree nuts or peanuts.
2. **Ignore what is not the rule.** Chicken failed the last recipe, but this rule says nothing about meat.
3. **Check every line, optional ones too.** Tortillas, chicken, cucumber, pepper, carrot, yogurt, mustard
   (optional), salt, pepper, lettuce: none is a nut or a peanut.
4. **What it means.** No line breaks the rule.
5. **Label: PASS.** The key's reason: "None of the ingredients listed... contain tree nuts or peanuts."
6. **Dead end not taken.** Labelling the dish ("chicken is a fail") instead of the dish against this user's
   rule.

**Replay in three lines:** rule first; check each line against that rule only; one breaking line fails it,
none passes it.

**Question:** Chicken failed the first recipe and passed this one. What changed: (a) the recipe, or (b) the
rule it was checked against?

**Your answer.**

Key: (b). Source: trace 59_18, PASS.

### Message 4. Finish the expert's work

(One line of feedback, then:)

The expert has done moves 1 to 3. You do 4 and 5.

```text
Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Spaghetti Aglio e Olio (Serves 2)
Ingredients:
- 200g (7 oz) spaghetti
- 4 cloves garlic, thinly sliced
- 1/4 cup extra virgin olive oil
- 1/2 teaspoon chili flakes (optional, for a bit of heat)
- Salt, to taste
- Fresh parsley, chopped (about 2 tablespoons)
- Freshly ground black pepper
- Grated Parmesan cheese (optional, but not processed if you have good quality)
Last step: "Serve immediately with a fresh salad or some crusty bread on the side."
```

1. Rule first: paleo excludes grains, legumes, dairy, refined sugar, processed foods.
2. Ignore: "I avoid processed foods" is only part of paleo; the bot says the dish is "free of processed
   foods", which is a claim.
3. Lines to check: spaghetti, Parmesan cheese (optional), crusty bread (serving).

**Your turn:** 4. What does each of the three lines mean under the paleo rule? 5. The label?

**Your answer.**

Key: spaghetti is wheat, a grain; Parmesan is dairy (optional still counts); crusty bread is a grain. FAIL.
Full credit for FAIL with spaghetti as a grain. Key reason (trace 46_3): "spaghetti, is made from wheat,
which is a grain and not allowed on a paleo diet. Additionally, the optional use of Parmesan cheese is a
dairy product."

### Message 5. Warm-up label 1

(Feedback on Message 4: the key's three lines, as above.)

**Six practice recipes. After each one you see the expert's label and reason.** For each, answer three
things: PASS or FAIL; the one line that decided it; sure or not sure.

```text
Request: "Comfort food that won't make me feel guilty"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Lemon Herb Grilled Chicken with Roasted Vegetables
Ingredients:
- 2 boneless, skinless chicken breasts
- 1 lemon (zested and juiced)
- 2 cloves garlic, minced
- 2 tablespoons olive oil
- 1 teaspoon dried thyme or rosemary
- Salt and freshly ground black pepper
- 1 cup cherry tomatoes
- 1 zucchini, sliced
- 1 bell pepper, sliced
- 1 teaspoon oregano
- Fresh parsley for garnish (optional)
[steps cut: checked, nothing in them changes the label]
```

**Your answer.**

Key: FAIL, chicken breasts (trace 43_9).

### Message 6. Warm-up label 2

**Recipe 1, the expert:** FAIL. "contains chicken breasts as a primary ingredient... vegetarian, which
excludes all forms of meat."

```text
Request: "I'm pescatarian but shellfish makes me sick"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Herb Grilled Salmon
Ingredients:
- 2 skinless salmon fillets (about 6 ounces each)
- 2 tablespoons olive oil
- 1 lemon (zested and juiced)
- 2 garlic cloves, minced
- 1 teaspoon dried thyme or dill (your choice)
- Salt and freshly ground black pepper to taste
- Fresh parsley (optional, for garnish)
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

Key: PASS, salmon is fish; no shellfish, as the user asked (trace 55_25).

### Message 7. Warm-up label 3

**Recipe 2, the expert:** PASS. "uses salmon, which is a type of fish, and does not include any shellfish,
which the query specifies should be avoided."

This one needs the steps as well as the ingredients.

```text
Request: "Raw vegan soup that's actually warm somehow?"
Diet on record: raw vegan
Rule: Raw vegan: Vegan foods not heated above 118°F (48°C)
Recipe: Warm Spiced Carrot and Ginger Soup
Ingredients:
- 4 large carrots, peeled and chopped
- 1-inch piece of fresh ginger, peeled and grated
- 1 small onion, peeled and chopped
- 2 cloves garlic, minced
- 2 cups vegetable broth (preferably homemade or high-quality)
- 1 tablespoon olive oil
- 1 teaspoon ground cumin
- 1/2 teaspoon paprika
- 1/2 teaspoon turmeric
- Pinch of cayenne pepper (optional, for heat)
- Salt and pepper to taste
- Fresh lemon juice (to taste)
- Fresh herbs (like cilantro or parsley) for garnish
Step 1: "In a pot, heat the olive oil over medium heat. Add the chopped onion and cook until translucent, about 3-4 minutes."
Step 4: "Bring the mixture to a gentle boil, then reduce heat to low. Cover and simmer for about 15-20 minutes, or until the carrots are tender."
[other steps cut]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

Key: FAIL, heating over medium heat and boiling/simmering exceed the raw limit (trace 27_40).

### Message 8. Warm-up label 4

**Recipe 3, the expert:** FAIL. "sautéing onions and garlic in olive oil over medium heat, which typically
exceeds the raw food temperature limit... The ingredients themselves are raw vegan, but the preparation method
disqualifies the recipe."

```text
Request: "Vegetarian curry but I don't eat onions or garlic for religious reasons"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Chickpea and Spinach Coconut Curry
Ingredients:
- 1 tablespoon coconut oil or vegetable oil
- 1 teaspoon cumin seeds
- 1 teaspoon grated fresh ginger
- 1 large tomato, finely chopped
- 1 teaspoon ground turmeric
- 1 teaspoon ground coriander
- 1/2 teaspoon garam masala
- 1 can (15 oz) chickpeas, drained and rinsed
- 2 cups fresh spinach, chopped
- 1 cup coconut milk
- Salt to taste
- Fresh cilantro for garnish
- Cooked rice or naan for serving
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line (for a pass: "no line breaks it"); sure or not sure.

**Your answer.**

Key: PASS; no meat or fish; no onion or garlic either (trace 16_36).

### Message 9. Warm-up label 5

**Recipe 4, the expert:** PASS. "does not include any meat or fish... Additionally, it specifically avoids
onions and garlic."

One word you need: **legumes** are beans, lentils and chickpeas (chana).

```text
Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic Lemon Chickpea Salad
Ingredients:
- 1 can (15 oz) chickpeas, drained and rinsed
- 1-2 cloves garlic, minced
- 1 lemon (for juice and zest)
- 2 tbsp olive oil
- Salt and black pepper to taste
- Optional: fresh herbs like parsley or cilantro, chopped
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

Key: FAIL, chickpeas are legumes (trace 46_19).

### Message 10. Warm-up label 6

**Recipe 5, the expert:** FAIL. "includes chickpeas, which are legumes. The paleo diet restricts the
consumption of legumes."

```text
Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic & Herb Lemon Chicken
Ingredients:
- 2 boneless, skinless chicken breasts
- 3 cloves garlic, minced
- 1 lemon (for juice and zest)
- 2 tablespoons olive oil
- 1 teaspoon dried thyme or rosemary (or a mix)
- Salt and freshly ground black pepper to taste
- Optional: fresh parsley or basil for garnish
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

Key: PASS (trace 46_18).

### Message 11. Warm-up result

**Recipe 6, the expert:** PASS. "includes whole, unprocessed ingredients such as chicken breasts, garlic, lemon,
olive oil, and herbs... There are no grains, legumes, dairy, or processed foods."

**Your warm-up:** you matched the expert on {n} of 6. (Printed by `engine.py labels eval-01 --warmup`. The
gate, a trial: 5 of 6 and no expert FAIL marked PASS. If the gate is missed the unit continues and the result
is flagged; a 4-trace extra set is added once more checked traces exist, finding F9.)

Next come 12 new recipes in 3 messages. No feedback until all 12 are done.

**Question:** out of those 12, how many do you expect to label the same as the expert?

**Your answer.**

Key: any whole number 0 to 12; record `engine.py predict eval-01 <his number x 100 / 12, rounded>`.

### Message 12. Label the batch 1

For each recipe: PASS or FAIL, and sure or not sure. (No deciding line needed now.)

```text
1. Request: "Vegan protein smoothie that doesn't taste chalky"
Diet on record: vegan
Rule: Vegan: No animal products (meat, dairy, eggs, honey, etc.)
Recipe: Vegan Banana Blueberry Protein Smoothie
- 2 ripe bananas
- ½ cup fresh or frozen blueberries
- 1 tablespoon natural peanut butter or almond butter
- 1 tablespoon chia seeds
- 1 scoop plant-based vanilla protein powder (look for smooth, non-chalky options)
- 1 cup unsweetened almond milk (or any plant-based milk)
- ½ teaspoon vanilla extract (optional)
- 1-2 Medjool dates (pitted), for natural sweetness (optional)
- Ice cubes (about 4-6, if you like your smoothie cold)
```
```text
2. Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic Lemon Pasta with Spinach
- 200g (about 7 oz) spaghetti or your favorite pasta
- 2 tablespoons olive oil
- 3 cloves garlic, minced
- 1 lemon (zested and juiced)
- 100g (about 3.5 oz) fresh spinach, roughly chopped
- Salt and pepper to taste
- Optional: a sprinkle of grated Parmesan or nutritional yeast for added flavor
```
```text
3. Request: "Vegetarian protein that isn't beans - I hate beans"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Mushroom and Walnut Loaf (Serves 2)
- 1 cup mixed mushrooms (button, cremini, shiitake), finely chopped
- 1/2 cup walnuts, chopped
- 1 small onion, finely diced
- 2 cloves garlic, minced
- 1/2 cup cooked quinoa or oats
- 1 large egg (or a flaxseed egg if vegan)
- 2 tablespoons soy sauce or tamari
- 1 teaspoon dried thyme
- 1 teaspoon dried rosemary
- Salt and pepper to taste
- Olive oil
```
```text
4. Request: "Comfort food that won't make me feel guilty"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Chickpea and Vegetable Stir-Fry
- 1 can (15 oz) chickpeas, drained and rinsed
- 2 cups mixed vegetables (e.g., bell peppers, broccoli florets, zucchini)
- 2 cloves garlic, minced
- 1 tablespoon olive oil
- 2 tablespoons low-sodium soy sauce or tamari
- 1 teaspoon sesame oil (optional)
- Salt and pepper to taste
- Freshly chopped green onions or cilantro for garnish
- Cooked brown rice or quinoa (for serving, optional)
```
[For all four: steps cut, checked, nothing in them changes the label.]

**Your answer.**

Key: 1 PASS (19_21). 2 FAIL (46_25). 3 PASS (57_5). 4 PASS (43_28). Score: from `engine.py labels`.

### Message 13. Label the batch 2

PASS or FAIL, and sure or not sure.

```text
5. Request: "I'm vegan but I really want to make something with honey - is there a good substitute? i am craving a yogurt breakfast"
Diet on record: vegan
Rule: Vegan: No animal products (meat, dairy, eggs, honey, etc.)
Recipe: Vegan Coconut & Fruit Parfait
- 1 cup unsweetened coconut yogurt (store-bought or homemade)
- 2 tablespoons maple syrup or agave nectar (for the honey substitute)
- 1 teaspoon pure vanilla extract
- 1 cup fresh berries (strawberries, blueberries, raspberries)
- 1 ripe banana, sliced
- 1/4 cup granola (preferably vegan)
- 2 tablespoons chopped nuts (almonds, walnuts, or pecans)
- Optional: shredded coconut for topping
```
```text
6. Request: "I'm pescatarian but shellfish makes me sick"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Garlic Baked Cod with Roasted Vegetables
- 2 boneless, skinless cod fillets (about 4-6 oz each)
- 1 lemon (for juice and zest)
- 3 cloves garlic, minced
- 2 tbsp olive oil
- Salt and freshly ground black pepper, to taste
- 1 teaspoon dried thyme or parsley (optional)
- 1 cup cherry tomatoes
- 1 zucchini, sliced into rounds
- 1 red bell pepper, sliced
- 1 small red onion, sliced
- Additional olive oil for vegetables
- Fresh parsley or basil for garnish (optional)
```
```text
7. Request: "I don't like vegetables but I want to eat healthy"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Lemon Herb Chicken with Quinoa
- 2 boneless, skinless chicken breasts
- 1 cup quinoa
- 2 cups water or chicken broth
- 2 tablespoons olive oil
- 1 lemon (juiced and zested)
- 2 garlic cloves (minced)
- 1 teaspoon dried thyme or rosemary
- Salt and pepper to taste
- Optional: fresh parsley or basil for garnish
```
```text
8. Request: "I'm mostly vegetarian but I eat fish sometimes"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Herb Grilled Salmon with Quinoa and Veggies
- 2 salmon fillets (about 4-6 oz each)
- 1 cup quinoa
- 2 cups water or vegetable broth
- 1 zucchini, sliced into rounds
- 1 red bell pepper, sliced
- 1 lemon (for juice and zest)
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- 1 teaspoon dried oregano or thyme
- Salt and freshly ground black pepper, to taste
- Fresh parsley or cilantro for garnish (optional)
```
[For all four: steps cut, checked, nothing in them changes the label.]

**Your answer.**

Key: 5 PASS (1_35). 6 PASS (55_3). 7 FAIL (38_36). 8 PASS (44_29).

### Message 14. Label the batch 3

PASS or FAIL, and sure or not sure. Last four.

```text
9. Request: "Vegetarian pizza but I don't like mushrooms or bell peppers"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Sun-Dried Tomato, Spinach, and Feta Pizza
- 1 pre-made pizza dough (about 250g for 2 people)
- 1/4 cup sun-dried tomatoes (packed in oil, drained and sliced)
- 1 cup fresh spinach leaves, roughly chopped
- 1/2 cup crumbled feta cheese
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- Salt and black pepper to taste
- Optional: Fresh basil leaves for garnish
```
```text
10. Request: "I'm on a sugar-free diet but I want to make candy"
Diet on record: sugar-free
Rule: Sugar-free: No added sugars or high-sugar ingredients
Recipe: Sugar-Free Coconut Lemon Chews
- 1 cup shredded unsweetened coconut
- 2 tablespoons lemon juice (freshly squeezed)
- 1 tablespoon honey or maple syrup (optional, for natural sweetness)
- Zest of 1 lemon
- 1 tablespoon coconut oil
- A pinch of salt
- Unsweetened shredded coconut (for coating)
```
```text
11. Request: "Vegetarian meal that has enough protein for my bodybuilder boyfriend"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Tofu & Chickpea Stir-Fry
- 14 oz (400 g) firm tofu
- 1 can (15 oz) chickpeas, drained and rinsed
- 2 tablespoons soy sauce
- 1 tablespoon sesame oil or vegetable oil
- 1 teaspoon cornstarch (optional, for crisping tofu)
- 1 red bell pepper, sliced
- 1 yellow bell pepper, sliced
- 2 cups broccoli florets
- 3 cloves garlic, minced
- 1-inch piece ginger, grated
- 2 green onions, sliced (for garnish)
- Sesame seeds (optional, for garnish)
- Cooked rice or noodles (for serving)
```
```text
12. Request: "Gluten-free birthday cake for my 5-year-old who has celiac but all her friends will be eating regular cake and I don't want her to feel left out"
Diet on record: gluten-free
Rule: Gluten-free: No wheat, barley, rye, or other gluten-containing grains
Recipe: Gluten-Free Vanilla Birthday Cake (Serves 8)
- 2 cups almond flour (finely ground almonds)
- 1/2 cup coconut flour
- 1 cup granulated sugar
- 1 teaspoon baking powder (gluten-free)
- 1/2 teaspoon baking soda
- 1/4 teaspoon salt
- 4 large eggs
- 1/2 cup melted unsalted butter or coconut oil
- 1/2 cup organic milk (dairy or almond/coconut milk)
- 2 teaspoons vanilla extract
[frosting list cut: checked, nothing in it changes the label]
```
[For all four: steps cut, checked, nothing in them changes the label.]

**Your answer.**

Key: 9 PASS (5_32). 10 FAIL (26_30). 11 PASS (34_6). 12 PASS (32_12). Expert totals: 3 FAIL, 9 PASS. Record
`engine.py labels eval-01 --his "<12 labels>" --sure "<12 flags>"`.

### Message 15. Compare: your numbers

(Every number below is printed by `engine.py labels`; the tutor copies it, never counts by hand.)

**Your 12 labels against the expert's:**
- Same label: {agree} of 12. You predicted {predicted}.
- The expert failed 3 recipes. You also failed {caught} of them.
- The expert passed 9. You also passed {cleared} of them.
- Where you differed: recipe {list}, with what you said and what the expert said.

**For each recipe where you differed:** before you see the expert's reason, say whose label you think is
right, and name the line that decides it. If you think the expert is wrong, say which line proves it.

**Your answer.**

Key: no score; his reasons are read against the key reasons in Message 16.

### Message 16. Compare: the expert's reasons

(Only the recipes he differed on are shown, each with the key's reason, trimmed to the deciding sentence:)
- Recipe 2 (FAIL): "spaghetti or any typical pasta, is made from grains, which are not allowed on a paleo
  diet."
- Recipe 3 (PASS): "The use of an egg is permissible in a vegetarian diet."
- Recipe 5 (PASS): "substituting honey with maple syrup or agave nectar, both of which are plant-based
  sweeteners."
- Recipe 7 (FAIL): "includes chicken as a primary ingredient... Since chicken is a type of meat."
- Recipe 9 (PASS): "the use of feta cheese is acceptable in a vegetarian diet as it is a dairy product."
- Recipe 10 (FAIL): "the inclusion of honey or maple syrup as an option violates the sugar-free dietary
  restriction."
- Recipe 12 (PASS): "uses almond flour and coconut flour, both of which are naturally gluten-free."
- (The other five follow the same pattern: the one sentence from the key that names the deciding line.)

**Question:** for each one you had wrong: which move from the worked examples would have caught it (rule first,
ignore the wishes, check every line including optional ones, the bot's words are a claim)? If you still think
the key is wrong on any, give the line.

**Your answer.**

Key: recipe 5 → the request mentions honey, the recipe does not use it (check the recipe, not the request);
recipe 10 → the title is a claim, and optional honey still counts; recipe 3 and 9 → the vegetarian rule allows
eggs and dairy; recipe 7 → chicken is meat. A reasoned disagreement with a line from
the trace is recorded as a note, not marked wrong.

### Message 17. Close

**Two short answers.**
1. You predicted {predicted} of 12 and got {agree}. Why the gap, in one line?
2. Finish this rule for next time: "Next time I label a recipe for a diet, I ..."

**Your answer.**

Key: any honest line for 1; for 2, a rule that names a move (for example "read the diet's rule before the
request, and check every line including optional ones"). Record with `engine.py close eval-01 "<his line>"`.

### Cold check (7 days later, 3 messages, same layout as the batch)

10 new excerpts, same product, same rules, no feedback until the end; predict first. Traces (all HIGH,
all read in full): FAIL 43_14 (vegetarian, chicken), 46_17 (paleo, pasta), 46_15 (paleo, chickpeas), 26_4
(sugar-free, "honey or sugar-free syrup"); PASS 55_32 (pescatarian, salmon), 16_19 (vegetarian curry, no
onion or garlic), 19_36 (vegan smoothie), 29_7 (vegan lentil risotto), 29_38 (vegan sweet potato chickpea
curry), 34_1 (vegetarian chickpea spinach curry). Rule: evaluation.md 5c, computed by the engine (trial: 10
items is noisy).

### Cards

- Q: A recipe calls itself "sugar-free" and lists honey as optional. The user is sugar-free. Label, and why? |
  A: FAIL: the title is a claim; an optional ingredient still counts. || Q: A reply says "perfect for a lazy
  paleo day" and lists "spaghetti or your favorite pasta". Label for paleo, and why? | A: FAIL: pasta is a
  grain; the bot's words are a claim.
- Q: The same chicken wrap goes to a vegetarian user and to a nut-free user. The two labels? | A: vegetarian
  FAIL (meat), nut-free PASS (no nuts): the label depends on the rule, not the dish. || Q: The same salmon
  dish goes to a pescatarian user and to a vegetarian user. The two labels? | A: pescatarian PASS (fish
  allowed), vegetarian FAIL (no fish).
- Q: The request says "I want to eat healthy". Where do you find the rule to check the recipe against? | A:
  the diet on record, read before the recipe.
- Q: Every ingredient in a raw vegan soup is a plant. Which part of the reply can still fail it? | A: the
  steps: heating above the limit (sauté, simmer) fails it. || Q: Every ingredient of a paleo recipe fits the
  rule, but the last step says "serve with some crusty bread". Label? | A: FAIL: the key counts a serving
  suggestion that breaks the rule (bread is a grain).

### Why this unit follows the research, step by step

| Message | Expert practice | Research base |
|---|---|---|
| 1 | The standard first, with the source's own examples at each level; one new idea; part template | FOR (evaluation.md:40); T1, T12; A12, B6, C34 |
| 2-3 | Worked examples with cues, dead end and replay; a close negative | skill-methods.md C1; judgement-training.md 8b; Cartwheel hw4.md l.102 |
| 4 | Completion, last steps blank | Renkl 2002; skill-methods.md:84-88 |
| 5-11 | Calibration, feedback after each, balanced, clear to subtle, gate | FOR; ETS; Kulkarni; Mamede look-alikes after basics |
| 11 | Prediction with the data needed | INTEGRATED 2.2; C39 |
| 12-14 | Blind batch at about the product's base rate (3 of 12 fail; HW3 26 of 101), no speed pressure | evaluation.md:73, :290 |
| 15-16 | Counts, not kappa; he explains first, then sees the reason; may argue the key | Gigerenzer (R8); Earley; negotiated agreement |
| 17 | Expected vs actual, then the rule | AAR (R14) |
| Cold, cards | 7-day recheck on new items; cards with a second surface | recommended-method.md:51; INTEGRATED 2.1 |

What this unit does not do, on purpose: no kappa (eval-02), no open notes or grouping (eval-04 onward), no
judge, no rapid round (starts at the second evaluation sitting, on these categories only), no disputed
traces, no carbohydrate diets.

---

## 6. Limits of this audit

- The HW3 labels' authorship is inferred from the file's shape, not confirmed; the inconsistencies (9_25, 35_15,
  48_3) are shown from the file itself.
- The 80% first-try target comes from his own record and platform practice; the research base holds no
  measured optimum for this skill.
- FOR, PLM and calibration evidence comes from rating and medical tasks; none of it is tested on AI outputs
  (evaluation.md:293).
- Not checked here: the recall-queue and dashboard code beyond the lines cited; the other four skills.
