# ScaleDojo's teaching method: what the full content shows, and what the evidence says about it

Written 2026-09-24. Source: the private study copy in `private/scaledojo/` (all 356 chapters of 5 courses,
1,085 quiz items, 358 weak vs strong answer pairs, 414 lab level listings, 13 unlocked level files, public
pages). Every number below was computed with python3 over that copy. Scripts and intermediate JSON were
kept in the session scratchpad, not the repo. At most one short ScaleDojo line is quoted per section.

---

## The short version

1. **The chapters are good explanations, read passively.** Median 580 words, 3 headings, 2 objectives.
   72% open by defining the concept, 24% by linking to the previous chapter, only about 4 to 13% open on a
   concrete problem. 4% of chapters ask the reader to do anything before the answer appears. In ICAP terms
   (Chi and Wylie 2014) they are Passive; the only non-passive parts sit after the text.
2. **The quiz trains recognition, and it can be beaten without reading the question.** 1,085 four-option
   items, 3 per chapter. About 75% ask for a fact or an explanation (rule: 77%; hand sample: 72%), under 10%
   ask him to apply or judge. 69% of items carry at least one distractor with stacked absolute words.
   A no-content strategy that reads only the options scores 70% overall and 92% in LLD, where the right
   answer is option B in 183 of 198 items.
3. **The weak vs strong interview answers are the best thing in the product.** 358 pairs, one per chapter.
   They are contrasting cases (correct vs erroneous worked answers), a method with moderate to strong
   evidence. The strong answer is a median 6 times longer and adds a trade-off (39% vs 1%), a named
   alternative (38% vs 1%) and a check or metric (39% vs 8%). ScaleDojo shows them to be read; the evidence
   says he should write his own answer first, then compare.
4. **The 24 true worked examples are expert walk-throughs, not faded examples.** All 30 listed chapters
   carry numbers; 26 name a rejected alternative; only 15 name a failure mode and 1 prompts the learner.
   They are a good source of expert reference answers for his design track.
5. **The labs are checklists, not design problems.** Every mission in the 13 unlocked levels is a
   deterministic presence check (add X, connect X to Y, set a dial past a value), and the mission text states
   the answer. The last hint in each level gives the solution. The "simulation" in the GenAI levels is
   three pre-written outcome lines. The AI review and the chaos simulator could not be inspected.
6. **Gamification is completion-based.** XP per chapter and level (+15 to +60), a global leaderboard,
   certificates awarded for levels completed (12 of 12), not for measured skill. No streaks were found.
   Gamification helps a little on average (Sailer and Homner 2020: g = 0.49 cognitive), mostly when it
   adds fiction or social play; leaderboards help top ranks and can hurt low ranks.

Section 8 lists what to adopt, change or skip.

---

## 1. Chapter anatomy (all 356 chapters)

**How it was measured.** Prose words exclude fenced code. Openings were classified by regex (problem-first:
an actor plus an event in the first sentence; bridge: phrases like "so far", "last chapter"; otherwise
concept-first), then 30 random openings were hand-labelled: agreement 26 of 30 (87%). The rule undercounts
problem openings: the hand sample found 4 of 30 (13%), the rule 4%. "Traced example" means a code comment
or sentence that shows the output for specific input values. "Visual components" counts places where a
rendered card, table or diagram left glued text in the scrape. Interactive demos are counted only where the
saved text still describes a control (drag, click, slider); most widgets did not survive scraping, so that
row is a lower bound.

| | api-design | forge | genai | hld | lld | all |
|---|---|---|---|---|---|---|
| chapters | 53 | 84 | 93 | 60 | 66 | 356 |
| median prose words | 510 | 697 | 648 | 508 | 492 | 580 (IQR 489 to 703, range 211 to 1,870) |
| median `##` sections | 3 | 3 | 3 | 2 | 3 | 3 |
| median "You'll learn to" objectives | 2 | 3 | 3 | 1 | 2 | 2 (854 in total) |
| opening: concrete problem (rule) | 4% | 0% | 14% | 2% | 0% | 4% (hand sample 13%) |
| opening: link to earlier chapter | 11% | 42% | 12% | 25% | 26% | 24% |
| opening: define the concept | 85% | 58% | 74% | 73% | 74% | 72% |
| has a code block | 94% | 94% | 49% | 0% | 94% | 67% |
| runnable "Try it yourself" code | 0% | 12% | 1% | 0% | 0% | 3% |
| interactive demo still described | 0% | 1% | 15% | 5% | 2% | 5% (lower bound) |
| visual components (cards, tables, diagrams) | 98% | 92% | 86% | 92% | 79% | 89% |
| traced input to output | 9% | 52% | 25% | 5% | 11% | 23% |
| any worked numbers (traced, 2+ calculations, or capstone) | 17% | 58% | 37% | 22% | 24% | 34% |
| "Ready to Build This?" link to a lab level | 94% | 44% | 44% | 35% | 36% | 49% (173) |
| asks the learner to predict or try before the answer | | | | | | 4% (13); predict or pause: 3 |

**Objectives.** 854 objectives. Top verbs: Explain 114, Understand 103, Implement 66, Recognize 59, Design
53, Distinguish 37. A quarter (Understand, Recognize, Know, See: 200 of 854) name no observable action.

**Pattern.** Every chapter has the same shape: objectives, a short concept-first opening, two or three
sections, one visual summary (often a takeaway card or table, such as a settings-to-task table), then two
Pro blocks at the end (one weak vs strong pair, three quiz items) and, in half the chapters, a link to a lab
level. The concrete scenario usually appears in the middle of the chapter or only in the linked lab level.
GenAI is the exception: 14% of its chapters open on a named failure (a crashed agent, a leaked answer), which
is the problem-first opening his notes asked for. Forge is the most worked (52% traced), HLD the least
(0% code, 5% traced), except its five capstones.

**Against the evidence.**
- Reading is Passive in ICAP (Chi and Wylie 2014: roughly 8 to 10% better learning at each step up, P < A < C
  < I). Koedinger et al. 2015 (in the research base) found the learning benefit of doing interactive
  activities was more than six times that of extra reading or watching.
- Concept-first openings forgo two cheap gains: a pre-question (g = 0.66 for questioned content, Pan and
  Carpenter 2023, `../teaching-methods.md` section 3) and problem-first sequencing (d = 0.36, section 1f).
- Short, one-idea chapters with a visual summary fit segmenting and coherence (moderate to strong). The
  length is right; the missing piece is an action inside the chapter.

---

## 2. Quiz item analysis (1,085 items)

**Coverage.** 353 of 356 chapters have a quiz; 328 have exactly 3 items, 22 have 4. All items have 4 options.
Passing needs 70%, and reading the chapter also counts as passing, so the quiz is optional.

**How items were classified.** Rule, applied in this order to the stem only:
evaluate = a judgement word (best, most appropriate, should you choose, trade-off, what is wrong) plus a
design or option word; apply = a scenario stem of 18+ words with an actor (a team, a client, your service,
a teammate); analyse = a comparison word (difference, compared to, vs, unlike, rather than); understand =
why, how, what problem, what happens if; recall = everything else. Then 60 random items were hand-labelled.

| Demand | rule: all 1,085 | hand: 60 | api-design | forge | genai | hld | lld |
|---|---|---|---|---|---|---|---|
| recall a fact | 44% | 37% | 36% | 46% | 45% | 46% | 44% |
| understand or explain | 33% | 35% | 35% | 32% | 33% | 36% | 31% |
| apply to a scenario | 3% | 7% | 0% | 3% | 4% | 4% | 2% |
| analyse or compare | 19% | 20% | 28% | 18% | 18% | 14% | 22% |
| evaluate a design choice | 1% | 2% | 1% | 1% | 0% | 0% | 2% |

Rule vs hand agreement: 42 of 60 (70%). Most disagreements were "why ... rather than" stems the rule called
analyse and the hand called understand. Both methods agree on the headline: about three quarters of the
items test recall or explanation of what the chapter just said; fewer than 1 in 10 asks him to apply or
judge. 11% of stems refer to "this chapter" (28% in GenAI), so they test the text, not the skill.

**Answer position and length.**

| | api-design | forge | genai | hld | lld | all |
|---|---|---|---|---|---|---|
| correct = A / B / C / D | 40/40/40/39 | 56/66/68/66 | 73/72/66/78 | 44/45/49/45 | **10/183/4/1** | 223/406/227/229 |
| correct is the longest option | 20% | 12% | 8% | **49%** | 7% | 18% |
| correct is the 2nd longest | 67% | 51% | 68% | 34% | 67% | **58%** |
| correct length / mean distractor length | 1.19 | 1.12 | 1.55 | 1.12 | 1.07 | 1.15 |

Two cues a test-wise reader can exploit: in LLD the answer is B 92% of the time; everywhere else the answer
is usually the second-longest option, because the longest option is often the over-stated distractor.

**Distractor quality.** Absolute markers counted: always, never, every single, entirely, cannot, only, at all,
guarantees, eliminates, no matter, and similar.

| | api-design | forge | genai | hld | lld | all |
|---|---|---|---|---|---|---|
| absolute markers per option: correct / distractor | 0.30 / 1.77 | 0.49 / 1.04 | 0.30 / 1.18 | 0.29 / 1.47 | 0.32 / 1.22 | 0.35 / 1.29 |
| correct option has no absolute marker | 75% | 64% | 74% | 78% | 72% | 72% |
| items with 1+ distractor carrying 2+ markers | 88% | 60% | 66% | 71% | 66% | 69% |
| items with 2+ such distractors | 57% | 22% | 22% | 44% | 34% | 33% |
| hedge words on correct / on distractors | 26% / 9% | 13% / 6% | 25% / 4% | 36% / 9% | 24% / 9% | 24% / 7% |
| options-only strategy score | 79% | 48% | 67% | 74% | 92% | **70%** |

Hand check of 20 random flagged distractors: 15 were implausible to anyone who read the chapter (for example
"fairness cannot be defined mathematically at all"); 5 were real misconceptions and good lures. A further cue:
89 items append a padding tail to one option to even out lengths, such as "as engineers repeatedly find in
practice"; in all 89 the padded option is the correct one. The options-only strategy (LLD: pick B; others:
fewest absolutes, then the hedged option, then the second longest) never reads the stem.

**Explanations.** All 1,085 items have one; median 28 words (10th to 90th percentile 22 to 37). They restate why
the correct option is correct. Only 18% share content words with any distractor (the rule's proxy for
"explains why a wrong option is wrong"); 31% contain any contrast word. Feedback with the correct answer
raises the testing effect and cuts lure intrusions (Butler and Roediger 2008), and elaborated, task-level
feedback beats bare right/wrong (Wisniewski, Zierer, Hattie 2020, d = 0.48 overall, higher for
high-information feedback). The explanations meet the minimum; they miss the misconception each lure encodes.

**Against the evidence.**
- Multiple choice is not bad in itself. Adesope et al. 2017 found strong testing effects for MC practice
  (g = 0.70; short answer g = 0.48; mixed formats best). Little, Bjork and colleagues 2012 showed MC works as
  retrieval practice only when the lures are competitive, because the learner must recall why each wrong
  option is wrong. Implausible lures remove that work.
- Absolute terms, unequal option length and implausible distractors are standard item-writing flaws that
  reward test-wiseness (Haladyna, Downing, Rodriguez 2002; Downing 2005: 33 to 46% of items flawed in one
  exam series, misclassifying 10 to 15% of examinees).
- Lures can be learned as facts (Roediger and Marsh 2005); the absurd ones pose little risk, the 5 in 20 real
  misconceptions do, which is why feedback on them matters.
- For him: recall and "what does the chapter say" items test what he already just read. His own record says
  arithmetic and classification questions feel like practice but are performance (`../teaching-methods.md`
  "What does NOT build analytical thinking").

---

## 3. Interview signals (358 weak vs strong pairs)

354 chapters have one pair, 2 have two. Each is a question, a weak answer and a strong answer, shown after the
chapter for Pro users. The learner reads both; nothing asks him to answer first.

**What they are pedagogically.** A pair is a contrasting case: an erroneous worked answer next to a correct
one on the same prompt. Comparing cases: d = 0.50 (Alfieri et al. 2013); comparing incorrect with correct
examples beat studying correct ones alone (Durkin and Rittle-Johnson 2012); erroneous examples help on delayed
tests once one correct example has been seen (McLaren et al. 2016). This is the moderate-to-strong evidence
base behind `../teaching-methods.md` 1c and 1e.

**Question types (rule on the prompt).** Scenario then question: 149 (42%). React to a colleague's or
stakeholder's claim: 127 (35%). Direct conceptual question: 44 (12%). Other: 38 (11%). So 77% put him in a
situation, far above the quiz's under 10%.

**What separates weak from strong (keyword features, share of answers).** Median length 13 words vs 81 (6.2
times).

| Feature | weak | strong |
|---|---|---|
| states a trade-off or cost | 1% | 39% |
| names an alternative (instead, rather than) | 1% | 38% |
| proposes a check, metric or test | 8% | 39% |
| sets a condition (if, when, unless, depends) | 11% | 38% |
| gives a reason (because, since) | 22% | 34% |
| uses a number | 5% | 27% |
| names a failure mode | 2% | 22% |
| dismissal or guess (fine, probably, no need) | 18% | 3% |

**Weak answer types (hand-coded, 40 random pairs).**

| Weak type | count | Example shape |
|---|---|---|
| hand-wave: a label with no mechanism ("it's the standard pattern", "probably a typo") | 11 | |
| accepts a flawed proposal ("that seems reasonable") | 10 | stakeholder wants to auto-trade above 95% confidence |
| wrong mechanism or misconception | 10 | picks a matrix for a sparse social graph |
| naive fix with no diagnosis ("retry a few times", "use a bigger model") | 9 | |

Strong answers follow one template: name the mechanism, give the consequence, name the alternative and its
cost, say what to check. That template is the judgement his design and evaluation tracks target.

**How to use them as practice (the change).**
1. Show only the prompt. He writes his answer (60 to 90 seconds, 2 to 4 sentences). Constructive in ICAP.
2. Show the weak answer. He names its type from the table above and the one thing it misses.
3. Show the strong answer. He marks which of the four moves (mechanism, consequence, alternative with cost,
   check) his own answer had, and rewrites the missing one.
4. Space it: the same pair returns later with one number changed (`skill-methods.md` C3, same brief with
   one number changed).
Caveat: the strong answers are polished prose; he should be scored on the four moves, not on length.

---

## 4. The worked-example chapters (30 listed in INDEX.md)

Six of the 30 are method or index chapters (how to approach any API, algorithm, GenAI or HLD design, the HLD
case index, the GenAI graduation checklist). 24 are true worked examples: 5 HLD system designs, 5 GenAI systems (two per chapter), 3 API designs,
9 LLD (7 case studies, a full mock interview, a 25-table schema capstone), 2 Forge capstones.

| Feature (keyword count per chapter) | chapters with 1+ (of 30) | median |
|---|---|---|
| numbers or estimates | 30 | 2 (HLD 7 to 19) |
| rejected alternative or dead end named | 26 | 2 |
| trade-off stated | 22 | 1 |
| decision reason (because, since) | 17 | 1 |
| failure mode | 15 | 1 |
| "Step N" section headings | 16 | |
| prompt for the learner to try or predict | 1 | 0 |

**Step structure.** HLD examples follow a fixed 5-step loop: clarify requirements, estimate scale, high-level
design, one deep dive, trade-offs and failure modes. LLD follows requirements, classes, relationships, code.
GenAI follows the 4-step framework from its method chapter, with two systems per chapter and no step
headings.

**Quality.** The HLD examples are the strongest: they carry a back-of-envelope estimate, say what the
numbers imply before any box is drawn, compare two real approaches for the deep dive with the catch of each,
and end with a failure mode and its fix. The GenAI examples state the one hinge decision and its reason (for
example, filter by tenant before retrieval, not after) but carry few numbers, no cost estimate and no
evaluation plan. LLD examples show code and one or two rejected designs, few reasons.

**Against the evidence.** Studying worked examples beats solving from scratch for novices (strong; Sweller;
Barbieri et al. 2023, g = 0.48), and fading steps triggers self-explanation (Renkl, Atkinson). ScaleDojo gives
the full example once and never fades it, never asks for a prediction at a decision point, and seldom shows
the expert's dead end in the order it happened. For his curriculum-map backbone (study, completion, faded,
independent, variation) these chapters are rung 1 only. Their value is as expert reference answers for the
side-by-side comparison after his own attempt.

---

## 5. Labs

**What exists.** HLD 100 levels, LLD 80, API design 50, Forge (algorithms) 76, SQL 50, GenAI 58 (8 tutorial
plus 50). Difficulty skews hard: HLD has 5 Easy and 54 at Expert or above; 93 of 100 HLD levels name a
company. Each level is a brief (named client, budget, latency target, users, data, constraints), themed
(movie characters in LLD, a detective agency in GenAI and SQL).

**What the learner does, by lab.**

| Lab | Action | How it is checked (from the unlocked levels) |
|---|---|---|
| HLD | drag components onto a canvas, wire them | mission checklist (node present, path present, edge present) + match to a reference edge list + every node must be wired; forbidden-connection rules; cost and latency limits; target RPS with a traffic pattern |
| GenAI | same canvas, pipeline stages with config dials | mission checklist (stage present 32, pipeline flow 21, config constraint 18 across 9 levels) |
| LLD | build tables and columns | entity, column and primary key present |
| API design | define resources, methods, schemas | resource, method, field, status code present |
| SQL | write a query against a story database | result check (inferred; not in the file) |
| Forge | fill a function stub in Python or Java | sandboxed hidden test cases plus a target complexity |

**Scoring modes.** The GenAI list has two: `tutorial` (8) and `standard` (50). Deterministic rubric evidence
is solid: every one of the 71 GenAI and 21 other missions inspected is a presence or threshold check, and
each mission's text states the move ("Connect Memory to Prompt Template", "Set temperature to 0.4 or lower").
The home page promises that every design gets AI feedback: "Every design gets scored by AI with detailed
architectural feedback." Its form could not be inspected (paid, server side). The HLD passing hint says a
design must "reasonably match a standard, proven pattern", so the pass gate is closeness to one reference.

**Hints.** 3 to 5 per level, in a fixed ladder: principle ("EXPERT INSIGHT"), applied note ("ARCHITECT'S
NOTE"), then "ACTION", which is the answer (the SQL level's last hint is the full query). Hints unlock one at
a time. Forge adds AI hints on the learner's own code. This matches the Cognitive Tutor ladder (principle,
application, bottom-out), which works if the learner self-explains the bottom-out hint and fails when he
races to it (68% of hint levels skipped in under a second; `ai-tutoring.md` 2c).

**Failure simulation.** "Murphy's Lab" (crash servers, partitions, traffic spikes, live metrics) is advertised
for HLD; nothing of it is in the saved files. In GenAI, `simulation_scenarios` are three fixed text outcomes
per level and `break_it_challenge` asks him to imagine what would happen: no real run. The tutorial levels
add a data-flow walk-through with example values and "ghost nodes" (pre-placed faded components).

**Against the evidence.**
- Simulations beat the same instruction without them (D'Angelo et al. 2014, g = 0.67 for interactive
  simulations), and deterministic, step-level feedback roughly doubles the effect of answer-only feedback
  (VanLehn, `ai-tutoring.md` 1c). A canvas with instant mission ticks is step-level feedback.
- But the missions give the design away. With the answer in the checklist the learner copies, the gaming
  pattern most strongly linked to low learning (Baker et al. 2004). Judgement is never exercised because no
  choice is left open, and one reference pattern marks valid alternatives wrong.
- Automated feedback on constructed work helps (writing: g = 0.55, Fleckenstein et al. 2023) when it is
  specific; LLM feedback that is not grounded in an expert solution makes logic errors (Bastani, 42%;
  `ai-tutoring.md` 3c). ScaleDojo's AI review is a black box on both counts.
- Forge's hidden tests are the best-evidenced check in the product: objective, step-level, and they punish
  the "passed the visible example" illusion.

---

## 6. Gamification

| Element | What ScaleDojo does | Evidence | Verdict for one learner |
|---|---|---|---|
| XP | a one-time bonus per module (reading or 70% quiz), +15 to +60 per lab level | points alone: little effect on learning; gamification overall g = 0.49 cognitive, 0.36 motivational, 0.25 behavioural, driven mostly by game fiction and social interaction (Sailer and Homner 2020) | rewards completion, including reading; skip |
| leaderboard | global, marked live | raises quantity of work but not quality; low ranks lose motivation (leaderboard studies 2021 to 2025) | no peer group; skip |
| certificates | per track, "Levels completed 12 / 12", credential ID, LinkedIn share | raise completion in MOOCs (completion halved when edX removed free certificates) but measure attendance, not skill | skip; his shipped artifacts are the proof |
| streaks | none found in the saved pages | loss aversion keeps habits; no learning evidence | he already has a ship streak |
| stickers, stories, movie themes | GenAI tutorial stickers, detective and film framing | game fiction moderated behavioural effects; off-topic story is a seductive detail (`../teaching-methods.md` section 3) | keep the named client and stakes; drop the costume |

---

## 7. Effectiveness verdict per element

Evidence grade follows `../teaching-methods.md` (strong, moderate, weak). Skills: E = evaluation, L = LLM
behaviour, S = system design, P = production, C = code.

| Element | Evidence | Likely effect as ScaleDojo runs it | Fits | Weakness to fix |
|---|---|---|---|---|
| short one-idea chapters (580 words) | segmenting, coherence: moderate to strong | good for first exposure, small on its own | L, S, P | passive; add one question before and one inside |
| objectives list | weak for learning; useful for signalling | small | all | a quarter use "understand"; state an observable action |
| concept-first opening | problem-first d = 0.36; pre-questions g = 0.66 | forgoes these gains in 72% of chapters | L, S | open on the failure or the brief, as GenAI does in 14% |
| visual takeaway cards and tables | signalling, dual coding: moderate | helps review | L, P | none needed |
| code blocks (67%), runnable in 3% | reading code: weak; tracing and predicting output: moderate | small | C | turn each block into predict-the-output, then run |
| interactive demos (5% visible) | simulation g = 0.67 when the learner acts | moderate where present | L | add "predict first, then drag" |
| quiz (3 MC per chapter) | MC testing g = 0.70 only with competitive lures | small: 70% gettable without reading the stem | L | short answer first, MC second; plausible lures from the weak-answer types; shuffle positions |
| quiz explanations | feedback d = 0.48; elaborated beats bare | moderate | L | say why each lure is wrong |
| weak vs strong answer pairs | contrasting and erroneous examples: moderate to strong | moderate if read, larger if he writes first | S, E, P | write first, classify the weak answer, score the four moves |
| worked-example capstones (24) | worked examples g = 0.48; strong for novices | strong on first use | S (HLD best), E | no fading, no predictions, few dead ends in order; add cost and eval plan to GenAI ones |
| lab brief (client, budget, SLA, data) | stakes and authentic tasks: weak to moderate | moderate, raises relevance | S, P | keep |
| lab missions and reference match | step feedback strong; but answer given in mission | small: copy-and-tick | S | hide missions, ask for the design first, check after |
| hint ladder ending in the answer | Cognitive Tutor ladder: moderate | moderate if he self-explains the last hint | S, C | require a one-line why after any bottom-out hint |
| Forge hidden tests | objective step feedback: strong | strong | C | none |
| chaos simulator (not inspected) | simulation: moderate to strong | unknown | S, P | he can do this himself with real load tests |
| AI design review (not inspected) | automated feedback g = 0.55; ungrounded LLM feedback risky | unknown | S | ground any review in an expert answer and a rubric |
| XP, leaderboard, certificates | small, unstable, completion-based | small or negative | none | skip |

---

## 8. Adopt, change, or skip

**Adopt as is**
1. **The named brief.** Client, problem, budget per 1k requests, latency SLA, users, data, constraints.
   It is the design-track brief format in `curriculum-map.md` already; ScaleDojo's GenAI briefs are a ready
   bank of 58.
2. **Expert worked examples with numbers**, especially the 5 HLD and 5 GenAI capstones, as the reference
   answer he compares his own design against, section by section.
3. **Forge-style hidden tests** for any code exercise he writes: visible example plus hidden edge cases.

**Adopt with changes**
1. **Weak vs strong pairs → write, classify, compare.** Prompt only; his answer; weak answer typed
   (hand-wave, accepts a flawed proposal, wrong mechanism, naive fix); strong answer scored on four moves.
   This is the single best-evidenced upgrade and it serves S, E and P.
2. **Quiz → short answer first, then a fixed MC.** Retrieval before recognition; when MC is used, lures come
   from the four weak-answer types, no absolute stacking, equal option length, random position. Explanations
   say why each lure fails. Keep 1 to 3 items, spaced into later lessons.
3. **Labs → decide before the checklist.** He sketches the pipeline and sets the dials from the brief alone;
   the missions become the after-check, and any valid alternative that meets the numbers passes. Then one
   "break it" run with a real number (for LLM behaviour, an actual API call at two temperatures).
4. **Worked examples → faded.** Second example of a type hides the deep dive and the trade-offs; he writes
   them, then compares (`curriculum-map.md` ladder).
5. **Chapter openings → the failure first.** Borrow the 16 GenAI problem-first openings as templates.

**Skip**
1. XP, global leaderboard, certificates, stickers. They reward reading and completion, and he is one learner.
2. Detective and movie framing. Keep stakes, drop costume.
3. Reading a chapter as a way to "pass" it.
4. The ScaleDojo quiz items as they are, as a measure of whether he learned something: 70% is reachable
   without reading the question.

---

## Limits of this analysis

- Heuristics were checked by hand on samples (openings 30, quiz 60, distractors 20, weak answers 40, traced
  examples 14); the traced-example rule missed HLD numeric examples, so 34% "any worked numbers" is a floor.
- Interactive widgets mostly did not survive scraping; the demo count is a lower bound.
- The AI review, Murphy's Lab and 401 of the 414 lab levels were not inspectable (paid or server side). Lab
  conclusions rest on 13 unlocked levels, mostly tutorials and level 1s.
- No public page describing ScaleDojo's own method was captured (the method blog saved empty); method
  claims come from the welcome chapters and the home page.

## Sources (external, added for this analysis)

- ICAP, Chi and Wylie 2014: https://www.tandfonline.com/doi/abs/10.1080/00461520.2014.965823 ; gamification, Sailer and Homner 2020: https://eric.ed.gov/?id=EJ1245270
- Practice testing, Adesope et al. 2017: https://journals.sagepub.com/doi/abs/10.3102/0034654316689306 ; competitive MC lures, Little et al. 2012: https://doi.org/10.1177/0956797612443370
- MC lures, Roediger and Marsh 2005: http://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/Roediger-Marsh-2005_JEPLMC.pdf ; feedback and MC, Butler and Roediger 2008: https://link.springer.com/article/10.3758/MC.36.3.604
- Feedback, Wisniewski et al. 2020: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/epub ; item-writing flaws, Haladyna et al. 2002: https://site.ufvjm.edu.br/fammuc/files/2016/05/item-writing-guidelines.pdf
- Simulations, D'Angelo et al. 2014: https://www.sri.com/publication/education-learning-pubs/stem-and-computer-science-pubs/simulations-for-stem-learning-systematic-review-and-meta-analysis-full-report/ ; automated feedback, Fleckenstein et al. 2023: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2023.1162454/full
- Incorrect examples, Durkin and Rittle-Johnson 2012: https://www.researchgate.net/publication/257408490 ; leaderboard ranks: https://www.sciencedirect.com/science/article/abs/pii/S0360131521001743 ; MOOC certificates: https://link.springer.com/chapter/10.1007/978-3-319-59044-8_21
- Research base: Koedinger et al. 2015 (doer effect), Schwartz and Bransford 1998, Kalyuga (expertise reversal), Renkl and Atkinson (fading), Aleven et al. 2016 (hints, via `ai-tutoring.md`).
