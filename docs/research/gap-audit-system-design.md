# Gap audit: system design, from the research to what Faiz will receive

Written 2026-09-25. Scope: the system design skill only. No design units exist yet, so this audits the
design they will be built from: the research base, `docs/research/structures/system-design.md`,
`docs/research/structures/INTEGRATED.md`, `.claude/skills/faiz-teach/SKILL.md`, `learn/engine.py` and
`learn/check_unit.py`. It asks one question at every link: what did the research say experts do, and did
it survive to the next file? His rules and feedback are from `docs/learning-evidence.md` (C1 to C49).
Nothing but this file was edited.

Severity: **blocker** = a unit built to this design would repeat what he rejected after code-01 (no worked
example, overload, not explained, unclear questions), or cannot be built or recorded at all. **major** = the
research is weakened in a way that will cost learning or honesty. **minor** = a real gap with a small
effect, or a tidy-up.

---

## 1. Verdict

The research base is clear and consistent: for a novice, each new kind of design problem starts with a
studied expert worked example, then a completion problem, and only from the third problem does he commit
his own design first, followed by a decision-by-decision comparison with the expert
(`skill-methods.md` C3 and E, `method-effectiveness.md` line 122, `recommended-method.md` steps 4 to 7,
`curriculum-map.md` lines 20 to 27, `judgement-training.md` line 217). The chain lost this in three places:

1. `system-design.md` turned the "study a worked example" rung into "guess the architect's move", which
   asks him to commit at every decision before seeing any expert reasoning. That is commit-first from the
   very first design. It also dropped modelling and moved all component knowledge to "after an attempt,
   never before".
2. `INTEGRATED.md` made "Commit, Check, Compare, Close" the frame of every unit in every skill, which has no
   place for a worked example or a completion step. This is the same root that produced code-01.
3. `check_unit.py` and `engine.py` hard-code the full "Design Crit" steps and a rubric pass rule, so a unit
   that starts with a worked example cannot pass the checker, and a study unit cannot be recorded.

Built as it stands, design unit 1 would hand a finance student who started programming in August a
ScaleDojo brief with about eight numbers, ask him to name his "top 3 characteristics" and guess an
architect's moves on components (conversation memory, summarisation, output caps) that no track has
taught him. That is the code-01 failure again, in a harder skill.

**Counts: 6 blockers, 19 major, 12 minor.** The corrected template in section 5 and the sample unit in
section 6 fix the blockers at the unit level; section 4 lists the file changes in order.

---

## 2. What the research says experts do (the reference the chain is checked against)

| Expert practice | What the research records | Research-base file | Original source |
|---|---|---|---|
| Worked examples first for novices | For novices on material with many interacting parts, studying worked examples beats solving (g = 0.48); examples-then-problems beats problems-then-examples; it reverses as expertise grows | `skill-methods.md` A2 lines 35, 46; `method-effectiveness.md` row 3; `teaching-methods.md` 2a | van Gog, Kester, Paas 2011; Chen, Kalyuga, Sweller 2015 (d = .65 for examples on high-interactivity material); Barbieri et al. 2023; Kalyuga 2007 |
| The ladder for design | 2 worked examples per problem type, then completion (he writes the deep dive only), then his full design compared section by section, then one number changed, then a new domain; restarts at each harder class | `skill-methods.md` C3 lines 136 to 162; `curriculum-map.md` lines 20 to 27, 34 | 4C/ID (van Merrienboer 2021); Renkl and Atkinson 2003; Renkl et al. 2002 (backward fading) |
| Commit first only after 2 worked examples | "Only after two worked examples of that problem type"; attempt-first fails "cold on a new task class" | `method-effectiveness.md` lines 34, 63, 122; `skill-methods.md` E row C3 line 256 | Kapur 2014; Loibl, Roll, Rummel 2017; Kirschner, Sweller, Clark 2006 |
| Productive failure boundary conditions | Works when the learner can use prior knowledge to generate several solutions; needs consolidation built on his attempt or contrasting cases; "Do not use PF in every lesson", target 3 to 5 key ideas; effects measured in STEM, little evidence outside it; a clear goal state matters | `private/research-base/learning-methods/kapur-roll-productive-failure-chapter.md` lines 32, 73 to 80, 431 to 440; `INDEX.md` lines 233 to 262; `teaching-methods.md` 1f | Kapur and Roll; Sinha and Kapur 2021 (d = 0.36); Loibl et al. 2017; Brand, Hartmann, Rummel |
| Modelling | The expert does the task aloud, showing heuristics, dead ends and control decisions; the learner then does a parallel case; "global before local" | `judgement-training.md` section 1, 8b lines 207 to 212 | Collins, Brown, Newman (cognitive apprenticeship); Schoenfeld's course; Mamede modelled reflection |
| Expert reasoning, not just the answer | Worked examples must show the reason at every decision, the rejected option and the dead end; training from captured expert reasoning g = 0.87 | `recommended-method.md` step 4; `method-effectiveness.md` row 14 | Clark et al. CTA meta-analysis |
| Supportive information before whole tasks | Non-routine skills get "supportive information" (mental models, strategies) given before the task class and kept available | `skill-methods.md` A1 line 28; `INDEX.md` lines 207 to 215 | van Merrienboer 2021 |
| How ScaleDojo teaches design | Components first: 16 Phase 2 modules and Lab Acts 1 to 4 teach one component each; whole-system worked examples come last (module 17, Act 5), and its own method chapter says those examples only compose pieces already covered in depth. Tutorial levels use "ghost nodes" (pre-placed, faded components). Weak vs strong pairs sit after the chapter they test | `scaledojo.md` lines 31 to 60; `scaledojo-method-analysis.md` sections 3 to 5 | `private/scaledojo/learn/genai/capstone-designing-full-genai-systems/how-to-approach-any-genai-system-design.md` |
| How other design programs teach | Hello Interview: core concepts and patterns pages, then breakdowns in one fixed frame, deep dives as Bad/Good/Great, "Try it yourself first" before one section, a level note. Grokking: short one-choice lessons before full problems. ByteByteGo: estimation recipe, 4 fixed steps | `teaching-structure.md` section 9 line 103; `skill-methods.md` B lines 67 to 69; `private/research-base/system-design/INDEX.md` "The frames experts use" | Hello Interview; Design Gurus; Alex Xu |
| Question difficulty | His best formats scored 78 to 80% right first try (bootcamp, part template); Math Academy tunes practice so "the 80-85% accuracy range is the sweet spot for learning"; write-from-blank 0 of 3, cold why-questions 0 of 4, 8 new things at once 0 answered | `learning-evidence.md` A9, A12, B5, B10, A11 | `private/research-base/learning-methods/mathacademy-way.md` p. 404 |
| Question and explanation craft | First line a decision or failure with a stake; under 150 words before his first answer; a component is introduced by the failure it fixes; one comparison; every term defined where it appears; no why-question before he has the facts it needs | `teaching-craft.md` Part B lines 142 to 157; `teaching-methods.md` lines 97 to 101, 198 to 205 | Koedinger 2015; Hinds 1999; Sundararajan and Adesope 2020 |
| Rubric validity and grading | Teacher-made tests show about 3x the effect of independent ones; judging skill is trained by calibrating against expert-graded anchors; partial credit where experts differ | `postmortem.md` cause 5; `judgement-training.md` sections 2 and 4 | Kulkarni et al. 2013; script concordance test; von Hippel |
| Feedback | Step-level feedback; reveal per decision after he commits; at most 3 points; feedback on retrieval so errors are not strengthened | `ai-tutoring.md` 1c, 4f; `method-effectiveness.md` row 1 | VanLehn 2011; Butler and Roediger 2008 |
| Retrieval and spacing | Spaced, interleaved retrieval; retest is not reteach | `postmortem.md` cause 6; `method-effectiveness.md` row 1 | Karpicke and Roediger 2008; Rohrer 2015, 2020 |

---

## 3. Findings, in chain order

Each finding: severity, where, what the research says, what was built instead, the exact fix.

### 3a. Research base (source material)

**R1. major. Most saved GenAI design worked examples have no text, so keys cannot be sourced or checked.**
- Where: `private/research-base/system-design/INDEX.md` top ("Full text of these was not copied") and
  section 6; `genai-sd-myengineeringpath-worked.md` (heading outline only, 378 words).
- Research: worked examples and keys must come from experts, prepared and checked before the session
  (`curriculum-map.md` Part 3, `postmortem.md` cause 4, `ai-tutoring.md` 3c: plain GPT-4 made logic errors
  in 42% of solutions, Bastani 2025).
- Built instead: `system-design.md` line 121 lists the System Design Handbook code assistant and the
  MyEngineeringPath moderation pipeline as C1 worked cases; both are outlines. The full-text GenAI design
  sources on disk are the ScaleDojo chapters (which, per `scaledojo-method-analysis.md` section 4, carry
  "few numbers, no cost estimate and no evaluation plan"), the ScaleDojo level files, and the
  `system-design-primer` repo (classic, not GenAI). `check_unit.py` accepts a source number only if the
  quotation is found in a listed source file (lines 82 to 84), so these outlines cannot back a key.
- Fix: for each unit, save a private, git-ignored excerpt of the exact source lines the key uses
  (`private/research-base/system-design/excerpts/<unit>.md`, source URL and fetch date on top), and list it
  under `sources:`. Until an excerpt exists, a case may not be used as a worked example or key.

**R2. major. The ScaleDojo lab level used as the first kata is not an expert key, and its numbers disagree.**
- Where: `system-design.md` lines 121, 158 (QuickChat, SD GenAI level 1);
  `private/scaledojo/scaledojo_levels_unlocked.json` details.genai."1".
- Research: lab missions state the answer, the last hint is the solution, and the "simulation" is three
  fixed text lines (`scaledojo-method-analysis.md` section 5, lines 298 to 300).
- Built instead: QuickChat is named as the kata brief with a hinge decision and a twist. Its only "expert
  answer" is the mission list (add memory, summarise after 20 turns or fewer, cap `max_tokens` at 4096)
  with no reasons and no rejected option. Its brief says $5 per 1,000 requests with 10K daily users at 5
  messages a session (at least 50,000 requests a day, so at least $250 a day), while its simulation text
  says the cost is "Within $50 budget". The twist "power users grow to 30%" is not in any source.
- Fix: use QuickChat only as the parallel practice brief. The reasoning key comes from the full-text
  ScaleDojo chapter "Conversation Memory & Context Windows" and its interview-signal pair (see the sample
  unit). Do not use the level's simulation numbers. Any changed-fact number is marked as a variation on a
  `given:` line.

### 3b. `docs/research/structures/system-design.md`

**S1. blocker. The first two designs of every class are "guess the architect's move", not studied worked examples.**
- Where: lines 95 to 100 (Study variant), 131 ("Designs 1 and 2: Study variant (guess the move)"),
  8 to 9 ("every session makes him commit before he sees any expert reasoning").
- Research: first 2 designs are worked examples to study (`skill-methods.md` lines 136 to 143); "do not
  let him attempt a new task class cold" (line 256); commit only "after two worked examples of that problem
  type" (`method-effectiveness.md` line 34); the 35-minute commit-first session runs "once he is past the
  first two worked examples" (`judgement-training.md` line 217); for true novices, reflection tools come
  after the first worked examples (line 261). Guess the move is evidenced on rated chess players
  (Charness et al. 2005, line 154) and ShadowBox on trained Marines, soldiers and firefighters (line 139):
  learners who already know the domain.
- Built instead: at every decision of his first design he writes his choice and reason first, then sees the
  expert's. With no component knowledge, each decision is a guess (his record: cold why-questions 0 of 4,
  B10; rules never stated then tested, E7).
- Fix: rung 1 of each class is a **modelled worked example** he studies with one self-explanation question
  per decision; guess the move is kept, but on a **parallel case after** the modelled one, for decisions he
  has just seen worked (it becomes the completion rung). Rewrite lines 95 to 100 and 131 accordingly.

**S2. blocker. No modelling anywhere in the design session.**
- Where: section 2 table lines 83 to 93 and the Study variant.
- Research: cognitive apprenticeship starts with modelling: the expert solves aloud, showing cues, dead
  ends and why one option was chosen, then the learner does a parallel case (`judgement-training.md`
  section 1 and 8b lines 207 to 212); worked examples show "the reason at every decision, including the
  rejected option and the dead end" (`recommended-method.md` step 4); expert-reasoning capture g = 0.87.
- Built instead: the tutor is "Silent" during the conjecture (line 87); expert reasoning appears only as a
  reveal after he commits. His C45 ("worked examples and detailed workings of sample questions are a good
  reference point") and C49 ("you didn't show me a worked example") are not met by any step.
- Fix: every new class opens with a prepared modelled case, cut into steps: the brief and its cues, the
  options with what each costs, the dead end and why it was dropped, the pick, and a 3-line abstracted
  replay (cue, what it means, move). Each step ends with one self-explanation question.

**S3. blocker. Component knowledge is withheld until after an attempt.**
- Where: line 48 (Kleppmann: "Background reading is organised as trade-off tables per component, read after
  an attempt, never before"); line 269 (reading "after an attempt").
- Research: 4C/ID gives supportive information before the task class and keeps it available
  (`skill-methods.md` line 28); productive failure needs prior knowledge he can activate
  (`kapur-roll-productive-failure-chapter.md` lines 32, 73 to 75); "very low prior knowledge plus a hard
  open problem overloads" and why-questions before he has the facts do not build thinking
  (`teaching-methods.md` lines 78 to 79, 100). ScaleDojo teaches every component in its own chapter and lab
  level before any whole-system design (`scaledojo.md` lines 31 to 60), and its design-method chapter says
  the capstone examples only combine pieces already covered in depth. Grokking uses one-choice lessons
  before full problems (`teaching-structure.md` line 103).
- Built instead: he meets sliding windows, summarisation, reranking, tenant filters or tool schemas for the
  first time inside a decision he must commit to.
- Fix: before each decision point is used in any unit, a **toolbox step** teaches that decision's options
  from the expert chapter (problem first, a tiny example, a trade-off table where each option wins on
  something, one or two short questions). The table stays available for the rest of the class. Rewrite
  line 48 to "read before the class, kept open during it".

**S4. major. "First design" before instruction does not meet the boundary conditions it cites, and the evidence is misread.**
- Where: section 2 step 2 (line 87), section 3b rule 3 (line 134), line 55 and lines 69 to 70 (Atman,
  Cross), line 249 (graded "moderate").
- Research: Kapur and Roll say do not use productive failure in every lesson, and target 3 to 5 big ideas
  (lines 437 to 440); its measured effects are mostly STEM, with "little evidence" for domain-general or
  non-STEM skills (`INDEX.md` lines 235 to 236); grasping the goal state matters (Brand et al.,
  `INDEX.md` line 261). Cross reports that early conjecture comes from "specific experience of the problem
  type" (quoted at line 55); Atman found freshmen's long scoping did not help, which is a finding about
  scoping, not evidence that novices should conjecture early.
- Built instead: every full session from design 4 on opens with his own design before any expert
  reasoning, justified as suiting novices.
- Fix: "First design" only on a class where he has passed the completion rung and a 90-second first-step
  test; the productive-failure opening is used on the class's hinge decision, not on every step; the
  evidence line for this choice drops to weak, and lines 69 to 70 are reworded to "scoping is boxed because
  novice scoping did not help (Atman); a conjecture needs experience of the type, so it comes after the
  worked cases (Cross)".

**S5. major. The fading chain is compressed from about five rungs to two, and contradicts itself.**
- Where: line 111 ("slowest; restarts each class") against lines 131 to 134 (two study designs, then
  design 3 with the conjecture given, then full design from design 4).
- Research: study, completion, faded, independent, variation (`skill-methods.md` line 84); backward fading
  one step at a time (Renkl et al. 2002, `INDEX.md` lines 163 to 170); climb only after 2 correct in a row
  with a correct reason (`skill-methods.md` D2).
- Built instead: design 3 is described as backward fading over four stages (twist and record, then options,
  then numbers, then conjecture) but is a single design, so three of those stages never happen.
- Fix: rungs per class: 1 modelled example plus guess on a parallel case; 2 a second modelled case with
  guess; 3 completion (pipeline and numbers given, he writes the hinge decision and the what-if);
  4 faded (pipeline given, he writes numbers and decisions); 5 full design; 6 changed-fact variation.
  Move up only after 2 passes in a row (D2); two misses at a rung, back one rung.

**S6. major. The worked-example anatomy was cut down, so numbers and cross-cutting parts are never modelled.**
- Where: Study variant lines 95 to 100 (brief, then decisions, then ADR).
- Research: the design worked example has 10 parts: brief with numbers, requirements, capabilities,
  pipeline, estimate, one deep dive as Bad/Good/Great, cross-cutting layer, the check against the brief,
  common wrong turns, what a senior answer adds (`skill-methods.md` lines 143 to 153; ScaleDojo's
  four-step method; Hello Interview level note).
- Built instead: no estimate, no check against the brief, no wrong turns in the study sessions. The first
  time he produces a "bill of materials" (a jargon term, S10) is in a full design.
- Fix: the modelled case carries all 10 parts over its steps, with the estimate shown as a worked chain
  before he is asked for one (`teaching-methods.md` "Fixing the direction weakness" 1 to 4).

**S7. major. Worked cases for class C1 are to be written by the tutor.**
- Where: line 121 ("briefs worked by the tutor").
- Research: "Worked examples come from experts, not from Claude"; Claude builds only the in-between rungs
  and names the expert example each was cut from (`curriculum-map.md` lines 96 to 102); postmortem cause 4;
  SKILL.md line 69 ("Claude does not invent the curriculum, the method or the examples").
- Fix: C1 worked cases come from full-text ScaleDojo chapters (context windows and memory, streaming and
  latency, the economics of calls, model routing) and their interview-signal pairs; the tutor only cuts
  them into steps and variations, each naming its source lines.

**S8. major. The "hidden fact sheet" and "write it as an assumption" rule conflict with his rules.**
- Where: line 86; line 43 (kata assumptions).
- Research and his rules: C31 (a decision depended on "where the majority of my users are which is unknown
  ... correct that"), C39 ("I don't mind predicting if I'm given all the data I need"), C41 and C34 (state
  the job and the background clearly); grasping the goal state matters (Brand et al.). Kata assumptions
  are a format for teams of 3 to 5 working architects (line 43).
- Built instead: facts he needs are hidden unless he asks the right question, and unknowns become his
  guesses.
- Fix: every brief lists all facts, each with its source, and lists unknowns as "unknown: assume X" with the
  assumption given. Asking customer questions becomes a scored skill only at level 3 (as line 137 already
  says for the internal FAQ).

**S9. major. Steps are large open writing tasks with no short checks and no difficulty target.**
- Where: section 2 steps 1 to 4 (line 86: top 3 characteristics from a list of 7, the driving number, up to
  3 questions; line 89: at 3 decision points, 2 to 3 options, pick, drawback, risk, cue, door type).
- Research: his best formats were 5 to 10 short questions at 78 to 80% first try (A9, A12); 8 new things in
  one part got 0 answered (A11, B5); 16-question messages brought "give me the answers" (B8); writing from
  blank 0 of 3 (B10); Math Academy tunes practice to 80 to 85% right. The independent review asked for
  "1 or 2 short checks after each design step" (`review.md` lines 170 to 171); it did not reach
  INTEGRATED, SKILL.md or the checker.
- Fix: one decision per step; at most 5 short questions per message; each commit is a pick with a one-line
  reason and the cue, not free prose; a first-try target of about 80% per unit, checked after each session
  (a step under 60% first try moves that step down a rung next time).

**S10. major. The design vocabulary is itself jargon, and the checker cannot see it.**
- Where: throughout (conjecture, crit, kata, NALSD, bill of materials, one-way door, hinge decision, top 3
  characteristics, ADR, twist); `docs/glossary.md` watchlist has none of: RAG, retrieval, vector database,
  embedding, chunk, tenant, guardrail, cache, agent, tool call, sliding window, summarisation, trade-off,
  rubric, daily users, requests per second, output cap, fallback.
- Research and his rules: C1, C5, C33 (jargon broken 5 times); every term defined where first used
  (`teaching-craft.md` line 146 rule 5).
- Fix: add the terms above to the glossary watchlist before the first design unit; keep INTEGRATED's plain
  step names in everything he sees ("Decision note", not ADR; "What if", not twist).

**S11. major. The rubric is scored by the tutor against the tutor's key, and the "outside check" is the same rubric.**
- Where: lines 172 to 187 (rubric), 165 ("Any design meeting the numbers passes by his rubric even if a
  mission is unticked"), 194 to 195; INTEGRATED lines 90 to 91.
- Research: tests written by the teacher inflate effects about 3 times (postmortem cause 5); judging skill
  is calibrated against expert-graded anchors (Kulkarni 2013, `judgement-training.md` section 4); the
  review kept the rubric only if its key is built from named sources and a cold outside task judges it.
- Built instead: the outside ScaleDojo lab is itself scored by the rubric, so nothing independent exists;
  ScaleDojo's AI review is a black box and levels 2 to 58 are locked in the saved copy (line 283).
- Fix: (1) anchor every rubric line at 0, half and full with a ScaleDojo weak and strong answer on that
  topic; (2) a second, blind marker (a separate agent given only his answer, the key and the anchors) scores
  each design; report agreement, and treat a gap over 15 points as an unscored session; (3) the
  independent measure is his four-move coverage (mechanism, consequence, alternative with cost, check) on
  unseen interview-signal prompts, scored against the strong answer, plus the ScaleDojo lab's own mission
  pass reported as is, never rescored by the rubric.

**S12. major. His Close line and "cue to move" cards go into spaced recall without being checked.**
- Where: line 200 (cards from "his own AARs"); `engine.py` lines 369 to 373 store his Close line as the
  card's answer.
- Research: retrieval works when answers are checked right after (`method-effectiveness.md` row 1); lures
  and errors are learned when retrieved without feedback (Roediger and Marsh 2005, Butler and Roediger
  2008, in `scaledojo-method-analysis.md` section 2).
- Fix: each unit's Key holds the expert cue-to-move rule; the tutor marks his Close line against it; the
  card stores the corrected line (his words where right).

**S13. minor. Weak vs strong drills can use topics he has not studied.**
- Where: line 164 (the Enterprise RAG tenant pair as the drill example) and line 213 (drill from week 6).
- Research: ScaleDojo shows each pair after its chapter; answering on an untaught topic is a cold
  why-question (B10, E7).
- Fix: a drill pair may be used only after the chapter or toolbox step it tests.

**S14. minor. The tiny generic example, the one picture and the problem-first opening (B1, B2, B4) are absent from the design shape.**
- Fix: in the template (section 5), the toolbox step opens on the failure, uses the source's own toy
  example (for memory: the 2,000-token toy window) before the real brief, and carries one picture.

**S15. minor. The crit narration can exceed the 3-point feedback rule.**
- Where: line 91 ("marks up his draft in place, narrating each change"); SKILL.md line 57 (at most 3
  points).
- Fix: narrate at most 3 changes in the message; the rest sit in the marked draft he can open on request.

### 3c. `docs/research/structures/INTEGRATED.md`

**I1. blocker. The shared frame makes every unit commit-first, deleting the worked-example and completion steps.**
- Where: line 30 ("One frame inside every unit. Commit ..., Check ..., Compare ..., Close").
- Research: the recommended unit has recall, a first-step test, placement, a worked example, completion,
  and only then his attempt "from the third problem of a type" (`recommended-method.md` lines 43 to 54).
- Built instead: no step in any skill's frame for studying an example. This is the root cause behind
  code-01 (C49) and it applies unchanged to design.
- Fix: replace line 30 with "Study (when the problem type is new, or the first-step test is failed),
  Commit, Check, Compare, Close"; add the first-step test and placement to the shared layer.

**I2. major. No track teaches the components that design units need.**
- Where: section 1 table and section 4 start order (line 63: design needs only "production's cost and
  latency classes").
- Research: `curriculum-map.md` Part 2 had modules M1 to M11 (SD chapters and lab levels on retrieval,
  tools, agents, memory, guardrails, serving, cost) as the place component knowledge is taught; 4C/ID
  supportive information; ScaleDojo's components-first order.
- Built instead: five skill tracks; LLM behaviour covers tokens, temperature and statelessness; nothing
  covers chunking, reranking, tenant filters, tool schemas, agent loops or caching, yet design classes C2
  to C5 decide between them.
- Fix: design owns its supportive information: each class begins with its toolbox steps, sourced from the
  matching ScaleDojo module (C1: modules 2 and 3; C2: 5 to 8; C3: 9 and 12; C4: 10 and 11; serving and cost
  from 13 and 15 as they enter). State this in the design row and the start order.

**I3. major. The first-step test and placement were dropped.**
- Where: section 2 (no placement), `engine.py` (no command); `system-design.md` rule 6 line 141 has it but
  nothing implements it.
- Research: a 90-second first-step test correlates up to .92 with full tests and adaptive instruction built
  on it gave 0.46 (Kalyuga 2007, `INDEX.md` lines 182 to 191); `recommended-method.md` steps 2 and 3.
- Fix: every design unit from rung 2 on opens with a first-step item (write only the first decision and its
  reason); right twice in a row with a right reason skips the next study rung.

**I4. minor. The delivery rule names "the part template" but design has none.**
- Where: line 41. Fix: section 5 of this file is that template for design.

### 3d. `.claude/skills/faiz-teach/SKILL.md`

**K1. major. The delivery rules cannot express a worked example or a per-decision reveal.**
- Where: lines 29 to 34 (steps sent verbatim, one per message) with the fixed step list in the checker.
- Research: reveal per decision, never the whole design first (`judgement-training.md` 8b; ShadowBox).
- Built instead: "Compare with the expert" is one step covering all decisions, so either all reveals go in
  one message (overload, B8) or the rule is broken.
- Fix: allow repeated decision steps (`## Step: Guess the move 1`, `2`, ...), each opening with the reveal
  of the previous decision as its feedback line; add one line to "How a session runs": "A new problem type
  starts with its Study steps; never ask him to commit on a decision he has not seen worked."

**K2. minor. The prediction is asked before he has seen how the unit is scored.**
- Where: lines 30 to 31. His rule C39: predictions need all the data. Fix: the step before the first scored
  step states the scoring lines in plain words; then ask for the prediction.

**K3. minor. The "Simpler:" block in the stuck order is not required by the checker.**
- Where: line 54. Fix: `check_unit.py` requires a `Simpler:` block in every scored step's Key.

**K4. minor. The header cites C1 to C46; the log now runs to C49.**
- Where: line 11. Fix: "C1 to C49".

### 3e. `learn/engine.py`

**E1. blocker. A study unit cannot be recorded, and the design score shown is not the score that passes.**
- Where: lines 49 to 50 (`rubric >= 70 and numbers_met >= 1`), 347 to 351 (score = mean of scored steps).
- Built instead: a guess-the-move or worked-example unit has no rubric, so it can never pass; a full design
  shows the step mean on the dashboard and in the prediction gap while passing on the rubric, and the floor
  (`BAR - 20`) is applied to the step mean.
- Fix: read a `rung:` header. Rungs 1 and 2 (study and guess): pass when no scored step is 0 and the mean is
  0.8 or more (trial value; no study sets a pass mark for guess the move); the score is that mean. Rungs 3
  and up: the score is the rubric and pass is rubric 70 or more with `numbers_met = 1`. One number feeds the
  pass, the dashboard, the prediction gap and the floor.

**E2. major. The design cold check ignores the brief's numbers and the rubric.**
- Where: line 351 (`Cold * 100 >= BAR`).
- Research: the cold check is "a cold design of a new brief in that class 7 days later at 70+", numbers met
  (`system-design.md` line 190).
- Fix: for rungs 3 and up, a cold design records `rubric` and `numbers_met` like a session; rungs 1 and 2
  keep the single Cold item.

**E3. major. Drills and the study rung are not units, so the best-evidenced element is never measured.**
- Where: lines 134 to 135 (the drill is a text line); plan slots 2 and 5 serve whatever design unit is next
  from week 6, with no study rung and no "first full design in weeks 7 and 8".
- Research: weak vs strong pairs are the "single best-evidenced upgrade" (`scaledojo-method-analysis.md`
  line 361).
- Fix: drills become short units in `learn/units/design-drill/` with their own Key (four-move coverage) and
  a `drill` result kind; the plan serves rungs in order.

**E4. minor. `rubric` and `numbers_met` are not range-checked.**
- Where: line 332. Fix: rubric 0 to 100, numbers_met 0 or 1.

### 3f. `learn/check_unit.py`

**C1. blocker. The design step list forces the full design session and forbids a worked example.**
- Where: lines 31 to 32 (`"design": ["Read the brief", "First design", "Numbers", "Choices", "Compare with
  the expert", "What if", "Decision note", "Close"]`) and line 105 (exact order, no repeats).
- Built instead: a rung-1 unit (toolbox, modelled example, guess on a parallel case) fails the checker; a
  unit that opens with "First design" on a new class passes.
- Fix: step lists per rung, read from the `rung:` header (section 5 gives them); repeated numbered steps
  allowed; at rungs 1 and 2, fail any unit whose first scored step comes before its worked-example steps.

**C2. major. Lines starting `given:` are exempt from every number check.**
- Where: lines 74 to 75.
- Research and his rules: C31 ("every given states its source or unknown"); postmortem cause 4 (invented
  givens contradicted each other in L6).
- Fix: a `given:` line must end with `(source: <listed file>)` and its numbers must appear in that file, or
  with `(variation of <source>)` for a changed-fact number; otherwise it fails.

**C3. major. None of his design rules is enforced.**
- Where: the checker has design-specific code only in the step list.
- His rules: C35 (each option must win on some dimension), C32 and B14 (state each option's effect on the
  target number), C45 and C49 (a worked example before practice), C48's intent (explain why the thing shown
  is built that way).
- Fix: in design units, every option table row needs a "wins on" cell and an "effect on" cell; every
  modelled step needs a "Why this move" line; enforce the watchlist from S10.

**C4. minor. The prose cap is 2,500 characters per step; the craft standard is under 150 words before his first answer.**
- Where: lines 161 to 163; `teaching-craft.md` line 157. Fix: cap prose before the first question at about
  1,000 characters, and a whole step at about 1,600.

### 3g. Cohesion problems across the chain

| # | Severity | Problem | Files | Fix |
|---|---|---|---|---|
| X1 | major | Three different weekly shapes: `system-design.md` section 6 (Wed session, Sat drill, 65 to 70 min); INTEGRATED section 5 (Wed and Sat sessions, Fri and Sun drills); `engine.py` (slots 2 and 5, drills at slots 4 and 6, no study rung) | sd lines 210 to 216; INTEGRATED lines 81 to 85; engine line 127 | INTEGRATED wins; delete sd section 6's table and point to INTEGRATED; engine serves rungs in order |
| X2 | minor | Step names: sd uses Brief, Conjecture, Numbers, Options, Crit, Twist, Record; INTEGRATED and the checker use plain names | sd line 78; INTEGRATED line 19 | keep the plain names; rename sd's section 2 |
| X3 | minor | Stuck order: sd uses "which worked case does this look like?" and reasoning cards; SKILL uses the shared order. With no worked cases yet, the sd prompt points at nothing | sd lines 87, 89; SKILL line 54 | use the shared order; the two options in stuck step 2 come from the toolbox table |
| X4 | minor | The evidence file says C32 and C35 are "kept in v2" in the design Choices step, but no checker or template enforces them | learning-evidence C32, C35 | C3 above |

---

## 4. Prioritised fixes

**Before any design unit is written (blockers):**
1. INTEGRATED line 30: add "Study" to the shared frame, with the first-step test and placement (I1, I3).
2. `system-design.md` sections 2 and 3b: rung 1 is a modelled worked example, guess the move moves onto a
   parallel case after it; add modelling; supportive information before, not after (S1, S2, S3, S5).
3. `check_unit.py`: step lists per rung, repeated decision steps, worked example before the first scored
   commit at rungs 1 and 2 (C1).
4. `engine.py`: `rung:` header, one score that feeds pass, dashboard, gap and floor (E1).
5. Give component knowledge a home: design toolbox steps sourced per class from the ScaleDojo modules (I2).

**Before the first design session (majors):**
6. Private source excerpts for every worked case and key; no tutor-written worked cases (R1, R2, S7).
7. `given:` lines carry a source or a variation tag (C2); no hidden fact sheet (S8).
8. One decision per step, at most 5 short questions, about 80% first-try target (S9); SKILL per-decision
   steps (K1).
9. Glossary watchlist gets the design terms (S10).
10. Close lines and cards checked against the Key's expert rule (S12).
11. Full worked-example anatomy in the modelled cases (S6); "First design" only after completion and the
    first-step test, evidence graded weak (S4).
12. Rubric anchored with weak and strong answers, blind second marker, independent four-move measure (S11);
    rubric cold checks (E2); drills as units (E3); checker enforces C32 and C35 (C3); one weekly shape (X1).

**Tidy-ups (minors):** S13, S14, S15, I4, K2, K3, K4, E4, C4, X2 to X4.

---

## 5. The corrected unit template (design)

Every design unit follows this. It is built only from sections 2 and 3 above. Headers are for the
engine and checker; he never sees file names or Keys.

```
skill: design
id: design-NN
rung: 1 | 2 | 3 | 4 | 5 | 6        (1 study+guess, 2 second study+guess, 3 completion, 4 faded, 5 full, 6 variation)
class: C1 | C2 | ...
title: <plain words>
decision points: <the 1 to 3 decisions this unit covers>
prerequisites: <unit ids whose ideas the steps use>
scored: <step names>
sources: <private excerpt files with the exact lines used>
runs: <every computed number>
```

**Step lists by rung** (one step per message; each step ends with **Your answer.**, has a Key with
`Score:` if scored and a `Simpler:` block):

| Rung | Steps, in order |
|---|---|
| 1 and 2 | Goal and problem; Toolbox (one step per decision point); Worked example 1..n (one step per decision: cues, options, dead end, pick, why); Guess the move 1..n (parallel case, one decision per step, each opening with the reveal of the previous one); What if; Decision note (fill-in frame); Close |
| 3 | First-step check; Read the brief; Worked pipeline and numbers (given, with one self-explanation question); Choices 1..n (his); Compare with the expert 1..n; What if; Decision note; Close |
| 4 | First-step check; Read the brief; Numbers (his, checked by a run); Choices 1..n; Compare 1..n; What if; Decision note; Close |
| 5 and 6 | First-step check; Read the brief; First design; Numbers; Choices 1..n; Compare 1..n; What if; Decision note; Close |

**Rules every step follows** (source in brackets):
1. Opens on a decision or failure with a stake; background in 4 or more plain sentences where the step
   introduces the case (C34; craft rule 1).
2. At most one new idea per step and under 150 words before the first question; at most 5 short
   questions (B5, B9; craft rule 14).
3. Every term he has not been taught is explained in the sentence where it first appears (C1, C33).
4. Every number comes from a listed run, `facts.md`, a quoted source line, or a `given:` line with its
   source or "variation" tag (C31; postmortem cause 4).
5. Option tables: each option has "wins on" and "effect on the target number" (C35, C32, B14).
6. Direction questions ("does it go up or down", "toward or away") are asked as two options (E12, D4).
7. No question depends on a rule not stated in this unit or a listed prerequisite (B6, E7).
8. Modelled steps say the cue, what it means, and the move, and include one dropped option with why
   (Collins; Schoenfeld; `recommended-method.md` step 4).
9. Reveals are per decision, after he commits, with the expert's cue and the option the expert dropped
   (ShadowBox; guess the move).
10. Feedback: right gets one line naming what was right; wrong gets "not yet", one reframe, one hint; the
    stuck order is the shared one; at most 3 points (SKILL.md).
11. The Close line is marked against the Key's expert rule before it enters recall (S12).
12. Target about 80% right first try across the unit's questions; a step under 60% first try is moved down a
    rung next time (A9, A12; Math Academy p. 404).
13. Pass: rungs 1 and 2, no scored step at 0 and a mean of 0.8 or more (trial); rungs 3 and up, rubric 70 or
    more with every brief number met. Move up a rung after 2 passes in a row (`skill-methods.md` D2).
14. Cold item at 7 days: a new brief of the same shape, one decision, same scoring as the unit's rung.

---

## 6. Sample first unit, written in full

Class C1 (single-call feature), rung 1, one decision point: what to do with a long conversation history.
Prerequisites: llm-02 (tokens) and llm-04 (the model keeps no memory between calls; a 20-message chat that
resends every earlier message used 63,000 input tokens in `runs/llm04-chat-total.json`).

Sources (all full text, private): the ScaleDojo chapter "Conversation Memory & Context Windows" and its
interview-signal pair 9 (`private/scaledojo/learn/genai/tokens-embeddings-and-memory/conversation-memory-and-context-windows.md`;
`scaledojo_paid.json` gated entry for that chapter); ScaleDojo GenAI level 1 and tutorial level 0.3 briefs
(`scaledojo_levels_unlocked.json`); `learn/facts.md` (Claude 4.6 and later: 1M-token window at standard
pricing). ScaleDojo text is paraphrased, with short quotations only. Runs still to be made with
`calc.py` are marked "run to make".

What he receives, message by message, after the day's recall:

---

**Message 1. Goal and problem**

> Design, unit 1: long chats that get cut off.
>
> A small company runs a chatbot. Most chats are short, but some users keep one chat going for a long
> time. In those long chats, two things go wrong: the bot's answers stop mid-sentence, and the bill for
> those chats is much higher than for short ones. You already know why the second one happens: the model
> keeps no memory, so the app sends the whole chat so far with every new message (your LLM unit 4 run: a
> 20-message chat used 63,000 input tokens). Today you will see how an engineer fixes both problems with
> one decision, then you will make that decision yourself for a real company's brief.
>
> Done means: you pick how a chatbot handles long chats, give the reason, and name what it costs, in 3
> lines.
>
> First, a check on what you already know. When a chatbot seems to "remember" your earlier messages,
> where does that memory actually live?
> A. Inside the model, which stores each chat.
> B. In the text the app sends again with every new message.
>
> **Your answer.**

Key (not sent): B. Not scored. Purpose: activates the prerequisite (llm-04) that every later step uses.
Simpler: "Think of your LLM unit 4 run: what did the app send on message 20?"

---

**Message 2. Toolbox: why answers get cut off**

> The model can read only a limited amount of text in one call. That limit is its **context window**
> (the most text the model can take in one call, counted in tokens). Three things share it on every
> call: the **system prompt** (the fixed instructions the app sends every time), the chat history, and
> the room left for the model's reply.
>
> A toy example from the course you bought: a window of 2,000 tokens. The system prompt takes 150 tokens,
> and 300 tokens are held back for the reply.
>
> 1. How many tokens are left for the chat history?
> 2. The history grows to 1,700 tokens and the app does nothing about it. Which part gets squeezed?
>    A. the system prompt  B. the room for the reply
> 3. So what does the user see?
>
> **Your answer.**

Key (not sent): 1. 1,550 (run to make: `calc.py design01-room '2000 - 150 - 300'`; the source states
1550). 2. B: the reply loses its room. 3. The reply stops mid-sentence, the cut-off in message 1.
Score: not scored (toolbox). Simpler for 2: "History takes 1,700 of the 1,850 tokens left after the
system prompt. How many are left for the reply?"
given: window 2,000, system prompt 150, reply room 300 (source: ScaleDojo chapter, the toy window).

---

**Message 3. Toolbox: the four ways to handle a long history**

> So a long history must be kept in check. Engineers choose one of four moves. Each is best at something.
>
> | Move | What it does | Wins on | Effect on cost per message as the chat grows | What it loses |
> |---|---|---|---|---|
> | Send everything | resend the whole chat every time | nothing forgotten; simplest | keeps growing | cut-offs return once the window fills |
> | Bigger window | switch to a model with a larger context window | nothing forgotten for longer | keeps growing: every token resent is paid again | only delays the cut-off |
> | **Sliding window** (keep only the last few messages, drop older ones) | drop the old part | cheapest; no extra call | stays flat | anything older is gone for good |
> | **Running summary** (older messages squeezed into a short summary by one extra model call; the last few kept word for word) | shrink the old part | keeps the gist of the whole chat | stays roughly flat, plus an occasional summary call | small details in old messages |
>
> Picture the running summary as the minutes of a long meeting: the last few exchanges written out word
> for word, everything before that as short minutes.
>
> 1. A user asks about something from 10 messages ago. The app keeps only the last 5 messages. Can the bot
>    answer it? Yes or no, and why in one line.
> 2. Which move adds an extra model call, and why?
>
> **Your answer.**

Key (not sent): 1. No: that message was dropped, so it is not in the text sent. 2. The running summary:
producing the summary is itself a model call. Not scored. Source: the ScaleDojo chapter's two strategies
and the hybrid; `facts.md` (a 1M-token window is billed at the same per-token rate, so a bigger window
does not make resent history cheaper).

---

**Message 4. Worked example, part 1: reading the cues**

> Now watch an engineer think it through. This case is from your ScaleDojo course.
>
> A support chatbot's chats often run long. Users complain it forgets details from early in the chat. The
> team also says the bill for long chats is far higher than for short ones.
>
> The engineer's first move is to read each complaint as a clue (a **cue**, a fact in the case that
> points to a cause):
> - "It forgets early details" points to history being cut: old messages are dropped or pushed out.
> - "Long chats cost far more" points to history being resent in full: every message pays for the whole
>   chat again.
> - Both at once: the app may resend everything until the window fills, then cut. One root cause, two
>   symptoms.
>
> Which cue tells the engineer the history is being resent in full?
> A. users say it forgets early details
> B. long chats cost far more than short ones
>
> **Your answer.**

Key (not sent): B. Not scored (self-explanation). Simpler: "Which of the two gets bigger every time the
full chat is sent again: what it forgets, or what it costs?"

---

**Message 5. Worked example, part 2: the dead end and the pick**

> The first idea many people have: "make the context window bigger." The engineer drops it. Why: a bigger
> window only moves the cut-off further out, and every message still pays for the whole chat again, so the
> bill problem gets worse, not better. The course lists this as the weak answer.
>
> The engineer's pick: a running summary. Keep the last few messages word for word, and squeeze everything
> older into a short summary.
>
> Replay in three lines:
> - Cue: forgets early details, and long chats cost more.
> - What it means: history is resent in full, then cut.
> - Move: keep recent messages word for word, summarise the rest. Cost: an occasional extra call, and some
>   old details are lost.
>
> In one line each: what does the summary part fix, and what does keeping the last few messages word for
> word fix?
>
> **Your answer.**

Key (not sent): the summary keeps cost per message from growing and keeps the gist of early details; the
word-for-word recent messages keep exact detail for what is being discussed now. Not scored. Simpler: two
options, "the summary fixes (A) the bill (B) the exact wording of the last message".

---

**Message 6. How the next part is scored, and your prediction**

> Next you make the same kind of decision for a real company, then two short follow-ups. Scoring:
> - Your pick: 1 if it is the move the course's expert makes, with a reason that uses a fact from the
>   brief; 0.5 for an acceptable other move with the right reason; 0 otherwise.
> - The follow-up question and your 3-line decision note: 1 if right and complete, 0.5 if half, 0 if not.
> - You pass the unit if no scored answer is 0 and the average is 0.8 or more.
>
> Before you start: predict your score from 0 to 100.
>
> **Your answer.**

Key (not sent): record with `engine.py predict design-01 <p>`.

---

**Message 7. Guess the move 1 (scored)**

> The company: QuickChat, a young startup (brief from your ScaleDojo lab, level 1).
> - Problem: their chatbot randomly cuts off answers mid-sentence. Users are angry.
> - Users: 10,000 a day, about 5 messages each chat.
> - Chats: about 800 tokens on average; some power users reach 15,000 tokens.
> - Must: handle chats with many back-and-forth messages. Must: never cut an answer off.
> - Unknown: how big the model's context window is. Assume the 15,000-token chats do not fit.
>
> What should QuickChat do with long histories?
> A. Send everything  B. Bigger window  C. Sliding window  D. Running summary
>
> Give: your pick, one reason, the fact in the brief that decided it, and your confidence from 1 to 5.
>
> **Your answer.**

Key (not sent): D. The expert move: the course's level 1 answer turns on summarisation after 20 turns or
fewer, and its hint says memory must summarise old messages so long chats stop being cut off.
Score: 1 for D with a reason naming the cut-off or the power users' 15,000-token chats. 0.5 for C if the
reason says it stops the cut-off and he notes it forgets old messages (the brief asks for long back-and-
forth chats, so losing them is a real cost). 0 for A or B (the cut-off returns; B also raises cost).
Simpler: "Which move both stops the cut-off and keeps something of the early chat?"
given: 10,000 daily users, 5 messages a chat, 800 and 15,000 tokens (source: scaledojo_levels_unlocked.json level 1).

---

**Message 8. Reveal 1, then guess the move 2 (scored)**

> The expert's move: D, a running summary. Cue: answers cut off in long chats, and the brief says chats
> must go on for many messages. Dropped: C, because QuickChat's users need the earlier chat, and a sliding
> window throws it away.
>
> One more part of the same fix. Summarising keeps the history small, but the reply still needs its own
> room (message 2). What else should QuickChat set?
> A. Nothing: the reply takes whatever room is left.
> B. A cap on reply length, so a fixed room is always kept free for the reply.
>
> Pick, and say in one line how it connects to the cut-off.
>
> **Your answer.**

Key (not sent): B. The course's level 1 answer caps the reply at 4,096 tokens or fewer; the chapter's
point is that the window must hold the reply, or the reply is cut off. Score: 1 for B with the link to
reply room; 0.5 for B without it; 0 for A. Simpler: "In the toy window, what happened to the reply when the
history took more than its share?"

---

**Message 9. Reveal 2, then what if (scored)**

> The expert's move: B, a cap on reply length, so the reply always has room. Cue: "never cut an answer
> off."
>
> Back to the toy window: 2,000 tokens, with 1,550 left for history. The app starts summarising when the
> history reaches 1,200 tokens. A teammate moves the starting point to 1,800 tokens "to save summary
> calls."
>
> 1. Before any summary starts, does the history run past the room it has? Yes or no.
> 2. So which problem comes back?
>    A. answers cut off  B. higher bill
> 3. The teammate instead moves it to 200 tokens. What is wasted?
>
> **Your answer.**

Key (not sent): 1. Yes: 1,800 is more than 1,550. 2. A. 3. Summary calls on chats that were never going to
get long: extra cost for nothing. Source: the chapter's point that starting too late defeats the purpose
and starting too early wastes calls. Score: 1 if all three are right; 0.5 for two; 0 otherwise.
given: 1,200 threshold (source: ScaleDojo chapter toy window); 1,800 and 200 (variation of that source).

---

**Message 10. Decision note (scored)**

> Write the decision down the way engineers do, by filling three blanks:
>
> We decided to ______ for QuickChat, because ______ (the fact in the brief). It costs us ______.
>
> **Your answer.**

Key (not sent): keep the last few messages word for word and summarise older ones, with a cap on reply
length; because answers cut off in long chats (or power users reach 15,000 tokens) and chats must run long;
it costs an extra summary call now and then and some lost detail from early in the chat. Score: 1 if all
three blanks are right, including a real cost; 0.5 if the cost is missing or is "nothing"; 0 otherwise.

---

**Message 11. Close**

> Your rule for next time, in one line: "Next time I see ______, I do ______."
>
> **Your answer.**

Key (not sent): expert rule: "Next time a chat gets cut off or its cost climbs with chat length, I keep
recent messages word for word, summarise the older ones, and cap the reply length." Mark his line against
it; store the corrected line with `engine.py close design-01 "<line>"`.

---

**Cold item, 7 days later (one message, scored, new surface, same decision)**

> A therapy app (brief from your ScaleDojo lab, tutorial level 0.3). Patients share personal stories, and
> two messages later the bot asks them to introduce themselves again. Sessions are 45 minutes and run 20 to
> 60 messages. Must: remember everything said in the current session. Must: not lose the thread after 20 or
> more messages. Budget: $50 per 1,000 messages; replies within 10 seconds. Unknown: the model's context
> window; assume a 60-message session does not fit.
>
> Which move: send everything, bigger window, sliding window, or running summary? Give your pick, the fact in
> the brief that decides it, and what the move costs.
>
> **Your answer.**

Key (not sent): running summary with recent messages kept (the level's answer: memory with summarisation
after 30 turns or fewer). Sliding window fails "remember everything in the session". Cost: an extra call
now and then, and some old detail, which matters here because patients share details; name it. Score: 1 for
the summary with the deciding fact and a real cost; 0.5 for the summary without the cost, or for "send
everything" if he checks it only works while the session fits the window; 0 for a sliding window or a
bigger window.
given: 20 to 60 messages, $50 per 1,000, 10 seconds (source: scaledojo_levels_unlocked.json level -6).

**Cards (enter recall after the unit)**
- Q: A chatbot's long chats cost far more than short ones. Which cue is that, and what does it mean? | A:
  The history is being resent in full, so every message pays for the whole chat again. || Q: Users say a
  bot forgets what they said early in a long chat. What does that cue point to? | A: Old messages are being
  dropped or pushed out of the context window.
- Q: Why is "use a bigger context window" a weak fix for long chats? | A: It only moves the cut-off
  further out, and every message still pays for the whole chat again. || Q: A teammate says a model with a
  1M-token window solves long chats. What stays wrong? | A: Resent history is still paid at the same rate
  per token on every message, so cost keeps growing.

**Why this unit meets the research**, in one line each: worked example before any commit (van Gog; S1);
modelled with cues, a dead end and a replay (Collins, Schoenfeld; S2); options taught before use, each
winning on something (4C/ID, C35; S3); guess the move only on decisions just seen worked (ShadowBox after
training; S1); one decision per message, per-decision reveal (K1); every number from a source, a run or a
tagged variation (C2, C31); questions sized for about 80% first try, direction asked as two options (S9,
E12); Close checked before it enters recall (S12).

---

## 7. Limits of this audit

- Only the design skill was traced; the shared-layer findings (I1, E1, C2) also touch the other four
  skills and should be checked there.
- The 0.8 pass value for rungs 1 and 2 and the 60% move-down trigger are trials: no study found sets a pass
  mark for guess the move.
- ScaleDojo's AI review and levels 2 to 58 were not inspectable in the saved copy, so the independent
  measure in S11 leans on the interview-signal pairs.
- The sample unit has not been run through `check_unit.py` (the checker does not yet accept rung-1 steps,
  C1), and three of its numbers need `calc.py` runs before it can be taught.
