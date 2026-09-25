# Gap audit: the production skill (cost, latency, rate limits, caching, reliability numbers)

Written 2026-09-25, after C49 ("you didn't show me a worked example, you're overloading me immediately,
you didn't explain the code"). No production unit exists yet (`learn/units/production/` is empty), so this
audits the design every production unit will be built from, and ends with the template they must follow and
a fully written first unit.

**Chain audited, in order:** research base (`docs/research/curricula/skill-methods.md`, `teaching-structure.md`,
`method-effectiveness.md`, `teaching-craft.md`, `curriculum-map.md`, `expert-curricula.md`, `scaledojo.md`,
`scaledojo-method-analysis.md`, `ai-tutoring.md`, `../teaching-methods.md`, `../recommended-method.md`,
`../postmortem.md`, `private/research-base/learning-methods/`, `private/research-base/production-and-llm-behaviour/`,
`private/scaledojo/INDEX.md`) then `docs/research/structures/production.md` then `structures/review.md` then
`structures/INTEGRATED.md` then `.claude/skills/faiz-teach/SKILL.md` then `learn/engine.py`,
`learn/check_unit.py` (and `hooks/teaching-guard.py`, which enforces the unit format) then `learn/facts.md`.
Learner record: `docs/learning-evidence.md` C1 to C49, A to E.

---

## 1. Verdict

**The production design would repeat the code-01 failure on day one.** The research base is clear and
consistent: a novice meeting a new problem type studies a worked example first, then fills in a
completion problem, and only attempts alone from about the third problem, with fading decided by his
performance. `production.md` kept a first-contact worked solution, but as a side note. The review strengthened
it ("fade the arithmetic fast, not the meaning step; add a placement test"). Then `INTEGRATED.md` reduced
production to five step names with no worked step. `SKILL.md` never says "show a worked example before you ask".
And `check_unit.py` hard-codes those five names, so a unit that contains the worked example the research
requires **fails the checker, and the engine refuses to teach it**. The machinery does not just miss the
expert practice. It blocks it.

The first scored step he would meet, **Guess**, asks a novice to write an estimation tree, a 90% range and
the input that dominates, under a 90-second timer, before anything is shown. The one study cited for
estimation (Loretan et al.) tested *worked examples* of estimation, not estimating first, and the same file
says a review found almost no evidence that estimation can be taught at all. That is the "overloaded
immediately, questions that made no sense" pattern (C49, A11, A13) built in.

Two more problems follow the same path. First, the pass rule measures his strength and not his weakness.
Only the Quick set is scored, its items are mostly arithmetic, and he already gets about 88% first try on
arithmetic, but 0 of 5 on what a number means (E11, E12). Second, the bar cannot be measured as written:
"9 of 10" is applied to a 3-item set, and the 7-day cold check is a single item.

**Counts:** 4 blockers, 19 major, 15 minor (38 findings). All four blockers are the same gap seen at four
links of the chain: the worked example was lost between the research and what he receives.

---

## 2. Findings in chain order

Severity: **blocker** = he would get the C49 experience, or the system would refuse the expert practice.
**Major** = an expert practice weakened or contradicted in a way the record says costs him. **Minor** = drift,
staleness, or a gap with little measured cost.

### Stage 1. Research base to `structures/production.md`

| # | Sev | Where | What the research says (base file, then original source) | What was built instead | Exact fix |
|---|---|---|---|---|---|
| 1.1 | **blocker** | production.md:57-67 (step 2 "Exhibit and gut estimate", line 62) | Novices learn a new procedure better from example-then-problem than problem-then-example (skill-methods.md:35, van Gog, Kester, Paas 2011). The only estimation study cited tested **worked examples** of order-of-magnitude reasoning, d = 0.59 to 0.61, and "a systematic review found almost no prior evidence that estimation is teachable" (production.md:41, Loretan et al. arXiv 2405.16480). Mahajan's method asks tutor questions "answered in the next paragraph", so the tree is modelled before it is asked for (production.md:40). Hubbard's 90% ranges are a separate trained skill (about 3 hours of practice with feedback, start from absurd bounds; production.md:43). A prediction helps only with a basis and a one-line reason; a coin-flip guess gains little (teaching-methods.md:56-61, Brod 2021). "Why" about an unseen mechanism produces guessing (teaching-methods.md:42). Tell facts, ask about use once he has the pieces (ai-tutoring.md:66-75, Chi). His words: predict only "if I'm given all the data I need" (C39); "you didn't show me a worked example, you're overloading me immediately" (C49). | Step 2 of every unit, including the first contact with a class: he writes a 2 to 4 leaf tree, a best guess, a 90% range and the dominant input, the tutor "stays silent", a 90-second timer runs. Four untaught demands before any teaching. | First contact with a class: no Guess step. The worked example models the rough estimate ("about 6,500 tokens at $2 a million is about 1.3 cents") in its first lines. The optional opening pick is one two-option question with all data given, unscored. Guess returns from the second unit of a class, after he has seen a worked estimate in that class, as a single rough number. The 90% range is added only after a short taught calibration segment (Hubbard) and is logged as a trial measure, never scored. |
| 1.2 | major | production.md:251 (grade table) | Loretan et al. measured worked examples for estimation (production.md:41). | "Estimate-first as a thread, factor-2 band: grade B-, Loretan". The evidence for *worked* estimation is credited to *estimate first*. | Split the row: "Worked estimation examples: B- (Loretan quasi-experiment)". "Estimating before instruction, for a novice: no direct evidence (D); allowed only after a worked estimate in the same class." |
| 1.3 | major | production.md:48-50, 69-73, 248 | "First two problems of a new type: worked example. From the third: he attempts first" (method-effectiveness.md:122). Fading is set by performance: a first-step test at each unit, climb after 2 right with a right reason, fall back after 2 misses (skill-methods.md:237-244, Kalyuga and Sweller; Salden 2010; Math Academy Way pp. 75-76). Review: the "88% first try" that justified fast fading came from v1 compute questions, not exhibits; he is 0 of 5 on meaning (review.md:108). | "Worked examples appear once per problem class"; a fixed 3-rung fade (worked, completion, own chain) whatever he scores; the whole centre becomes "a bank of exhibit items done at pace". | Two worked examples per class for the meaning and number-picking steps; one for the arithmetic. Fading by the first-step test and the 2-right, 2-miss rule. The meaning step is never faded until he passes it cold (review.md:206, INTEGRATED.md:94-95). |
| 1.4 | major | production.md:65 (step 5 "Lever") vs its own :257 | Sensitivity table **before** the lever choice, graded B (production.md:257, contrasting cases, method-effectiveness.md row 11; Schwartz and Bransford 1998: telling after comparing). Direction questions: 0 of 3 open, 3 of 3 as two options (E12). | "Before seeing it: names the lever, predicts its effect in %, and the input value that flips the decision", then the table. Three open demands on his weakest skill, and the file contradicts itself. | Show the table (each input changed, the saving it gives, computed by code) first. Then one pick from two options with the deciding number. The flip value is taught in a worked example of class C6 before it is ever asked. |
| 1.5 | major | production.md:63 (step 3 "Build the chain") | Show the expert answer only after he commits the whole item; "Production step 3 must wait until his chain is complete (B12: telegraphing flagged 4 times)" (review.md:131). | "At the first wrong link, shows only that link of the worked solution". The review's correction never reached the file; its amended header lists other overrides only. | Reveal after his full chain; feedback names the first wrong link and why (step-based feedback, VanLehn 2011, method-effectiveness.md:54). |
| 1.6 | major | production.md:66 and :186 | Mastery bar 91 to 100% on a retest with new items (Kulik 1990, method-effectiveness.md:55). "9 of 10 on a mixed set" (recommended-method.md:51). | "Timed set: 3 new bank items" per unit, while the bar is "9 of 10". With 3 items the only pass is 3 of 3, and one arithmetic slip (E10 happens) fails the unit. | Quick set is 10 short items in two messages of 5 (B9: 5 per message scored 80%). Pass at 9 of 10. |
| 1.7 | major | production.md:66, 198-199; 3b:104 | Interleaving helps only once each type has been learned; block first learning, interleave in review (method-effectiveness.md:57 and :128; Rohrer). Never test a rule not yet taught (E7: 6+ misses; ai-tutoring.md:186). | Sets "interleaved across unlocked classes" from the first week; level P-1 unlocks C1 and C2 together, so the first unit's set can hold an untaught C2 item. | "Unlocked" means "taught in an earlier unit". First unit of a class: its own items only. Interleaving starts from the second class, in the Quick set and the recall queue. |
| 1.8 | major | production.md:57-67 (no goal step) | Every unit opens with a goal card ("You will decide X. You are done when...") and a concrete failure with numbers (teaching-structure.md:149-150; CFA learning outcome statements, production.md:37). First line names the decision and the stake (teaching-craft.md T1, :105). His rules: every unit states its goal first (C41); the problem with context and background (C34). | The unit starts at the exhibit and a timer. | A first step "The job": the problem in 4 or more plain sentences, what he will be able to decide, what "done" means. |
| 1.9 | major | production.md whole file | One new idea per part, tiny generic example before the real case, one everyday picture (B1: strongest predictor, 80% vs 27%; B2; B5; A12 vs A13). At most one new term per part (teaching-craft.md:148). Math Academy knowledge points: one tiny step, one worked example, 2 to 5 questions, and teaching-craft.md:115 gives the production example itself: "KP1 one call; KP2 calls per day; KP3 with caching". | The part template is absent. Unit 1 as specified carries about 10 new things: exhibit reading, per-million pricing, input vs output rate, estimation tree, 90% range, "dominates", a units chain, easy-case check, +20% sensitivity table, break-even flip value. A11 had about 8 and got 0 answers. | The unit is built from 3 knowledge points, each: tiny picture, worked example, 2 to 4 short questions of the same shape. One new idea per knowledge point. |
| 1.10 | minor | production.md:62, 178, 187 | Speed shows a *compiled* skill (ACT theory, skill-methods.md:27); a first contact is the slow declarative stage. INTEGRATED marks pace as a trial (INTEGRATED.md:52). | A 90-second timer on step 2 of every unit, and "exam pace" sets. | No timer in the first two units of a class. Time is logged, not shown, until then. |
| 1.11 | minor | production.md:192 (readiness 0 to 10), :226-237 (measures) | The review dropped readiness (graded D) and set one dashboard (review.md:107; INTEGRATED.md:37-38). | Still in production.md; its amended header says INTEGRATED wins only on step names, queue, mastery rule, start order and week, so a unit author would build the dropped parts. | Strike the readiness row and the P-level "twice 7 days apart" milestone text, or add them to the header's override list. |
| 1.12 | minor | production.md:3b | One outside task per level (method-effectiveness.md:208). curriculum-map.md:69 names ScaleDojo level 6 "The Cost Calculator" for this module, and :78 level 33 "The Cache Layer". | Only P-4 has an outside task (his FBR assistant budget). | P-1 outside task: ScaleDojo lab level 6 from the brief; P-2: level 33. |
| 1.13 | minor | production.md:265 (excluded) | CFA example layout shows the substitution line with units (skill-methods.md:170-178). Yale: the hard part is "fishing for the correct numbers" (production.md:36). | "Worked examples that show every substitution" excluded. For per-million units, the substitution line is exactly where the number-picking shows. | Keep one substitution line per term, with units, in each worked example; code does the arithmetic. |

### Stage 2. `production.md` and the review to `INTEGRATED.md`

| # | Sev | Where | What the research says | What was built instead | Exact fix |
|---|---|---|---|---|---|
| 2.1 | **blocker** | INTEGRATED.md:17 | production.md:69-73 (first contact: full worked solution, then completion); review.md:108, :206 (keep a worked meaning step; placement test). Worked examples for novices, grade A (method-effectiveness.md:51). | The production structure is "Guess, Chain, Run, Lever, Quick set". The worked step survives only as a trial note (:94-95). The table at :17 is the only thing a builder or the checker copies. | Replace row :17 with the two unit shapes in section 4 below: "First contact: The job, Worked example, Your turn (x3 knowledge points), Lever, Quick set, Close. Later units: First step, Guess, Chain, Run, Lever, Quick set, Close". |
| 2.2 | major | INTEGRATED.md:30-31 | The research unit has "Study or attempt" and "Completion" before any comparison (method-effectiveness.md:146-147; recommended-method.md:45-47). Attempt-first only "from the third problem" and only with tools to attempt (method-effectiveness.md:63, :122; Loibl, Roll, Rummel 2017; Kirschner, Sweller, Clark 2006). | "One frame inside every unit: Commit (his answer first), Check, Compare, Close". No study phase in any skill. | "Study (worked example) or Commit, by placement; then Check, Compare, Close". |
| 2.3 | major | INTEGRATED.md section 2 and :108-114 | Review decision: "placement test and performance-based fading in all five" (review.md:130). First-step test at each unit (skill-methods.md:238-239; Kalyuga and Sweller: r up to .92). | Not in the shared layer and not in the build list; the engine prints "placement check" once with no mechanism (see 4.3). | Add "8b. One placement rule" to section 2: a 90-second first-step item at the start of each unit after the first of a class; right with a right reason twice in a row skips the worked example. |
| 2.4 | minor | INTEGRATED.md:41-42 | Part template where a step explains (A12, B1). | "The part template where a step explains something": production never says which steps explain; audit-system.md finding 19 flagged this and it is still open. | Name them: every Worked example step and every Simpler block. |

### Stage 3. `INTEGRATED.md` to `.claude/skills/faiz-teach/SKILL.md`

| # | Sev | Where | What the research says | What was built instead | Exact fix |
|---|---|---|---|---|---|
| 3.1 | **blocker** | SKILL.md:17-18, 29-34, 59-63 | Worked example before questions on a new type (van Gog 2011; method-effectiveness.md:33); "Written before the session... The example must share the exact shape of what he will be asked" (ai-tutoring.md:169-174); C45, C49. | One line: "Worked examples are his reference point for the applied skills". Nothing tells the tutor to show one before asking, and steps are sent verbatim, so the unit's shape decides everything. | Add under "Words and delivery": "A problem type he has not seen starts with a worked example (the goal, every step with its reason, the answer and what it means) before any question on it. Questions after it have the same shape. Nothing is asked that the unit has not shown or told (E7)." |
| 3.2 | major | SKILL.md:49-57; hooks/teaching-guard.py:99-102, 118-121 | Elaborated feedback d = 0.99 vs 0.24 for bare right or wrong (method-effectiveness.md:53, Wisniewski 2020); "marks each with a worked solution shown after his answer" (production.md:66); Schweser's QBank: explained solutions (production.md:37). | "Wrong: say so, one reframe, one hint." The guard caps feedback before a step at 400 characters, forbids any "?" in it, and blocks any Key line of 25+ characters in the turn. The worked solution lives in the Key, so showing it is blocked. | After a Quick set half, the tutor sends the prepared **Solutions** block (a unit section, not the Key) as its own message; the guard allows a unit's Solutions block verbatim. Keys hold marking rules only. |
| 3.3 | minor | SKILL.md:26-28 | Retrieval works when answers are checked right after (method-effectiveness.md:48). Self-ratings correlate .29 with real learning (curriculum-design.md). production.md:61 has the tutor mark number items against the key. | He grades every card himself, 1 to 4. | Number cards are marked by the key: wrong = 1, right = 3; he rates only "easy" (4) himself. |
| 3.4 | minor | SKILL.md:11 | His latest words win (C47-C49 exist). | "C1 to C46". C49's instruction is not in the rulebook. | Update the range; the 3.1 line carries C49. |

### Stage 4. `SKILL.md` to `learn/engine.py`

| # | Sev | Where | What the research says | What was built instead | Exact fix |
|---|---|---|---|---|---|
| 4.1 | major | engine.py:45-46 | Test what the skill is (curriculum-design.md, von Hippel: teacher tests inflate); production's weak point is meaning, not arithmetic (production.md:27-30; review.md:108; E11 0/2, E12 0/3). | Pass = "Quick set >= 0.9", nothing else. A set of arithmetic items passes on his existing strength. | Keep the rule, but the checker requires 3 or more of the 10 Quick set items to be meaning items (before minus after, which way a number bends a decision, which share is the lever); see 5.4. |
| 4.2 | major | engine.py:351; check_unit.py:151-152 | Same bar cold, with new items (INTEGRATED.md:34-36; Kulik: retest with new items). | The cold check is one `## Cold` item; pass = that item at 0.9 or more. One item cannot show 9 of 10. | Production cold = 10 items (two messages of 5), recorded as the share right; pass 9 of 10. |
| 4.3 | major | engine.py:124-142 (placement printed), :148-170 (rung computed), :173-190 (next unit by file order) | Performance-based fading and placement (review.md:130; skill-methods.md:237-244; Salden 2010). | "production placement check before the first unit" is printed and never recorded or used; `skill_state` computes a rung that `next_unit` ignores; units are served by file name. | `next_unit` picks the first unit whose `level:` equals the current rung; record `--step "First step=1"` and skip the unit's Worked steps when the last two First step values are 1 (add a `skip_if_placed:` header listing them). |
| 4.4 | major | engine.py (no alarm) | Practice pitched at 80 to 85% right is "the sweet spot for learning"; Math Academy lessons pass 95% first try (private/research-base/learning-methods/mathacademy-way.md:12885, p. 404, and :13375-13376). His record: 78 to 80% with the template, 27% without (A9, A12, A13). | Per-step values are stored, but nothing looks at first-try rates inside a unit, so an overloaded unit (C49) shows only as a failed pass. | Dashboard alarm: in-unit first-try rate below 70% on the practice steps = the unit is too hard, rebuild before the next unit of that class; above 95% on 3 units in a row = move up a rung (expertise reversal). |
| 4.5 | minor | engine.py cmd_due (`reviews % len(variants)`); check_unit.py:185-186 | Number items return "as a new exhibit with new numbers, never the same item" (production.md:196-197; INTEGRATED.md:26-27). | Two variants are required, so the third review repeats the first surface. | Require 4 variants on number cards, or generate numbers from a template run by calc.py. |
| 4.6 | minor | engine.py:173-190 | Math Academy: a failed lesson is retried later after reviews of its key prerequisites; 80% then pass (mathacademy-way.md:13375). | A missed unit is never served again; the parallel unit must already exist or the slot stalls. | Prepare production-01's parallel unit before production-01 is taught. |

### Stage 5. The enforcers: `learn/check_unit.py` and `hooks/teaching-guard.py`

| # | Sev | Where | What the research says | What was built instead | Exact fix |
|---|---|---|---|---|---|
| 5.1 | **blocker** | check_unit.py:28, :104-106 | Worked example, completion, then own attempt (skill-methods.md:84-88; recommended-method.md:45-48). | `STEPS["production"] = ["Guess", "Chain", "Run", "Lever", "Quick set", "Close"]`, and any other step name fails "steps must be, in order". A research-true unit cannot pass; `engine.py cmd_done` and `today` refuse units that fail. | Two allowed shapes per skill (see section 4): `first-contact` and `later`, chosen by a `shape:` header. First-contact must contain at least one `Worked example` before the first `Your turn`, and every `Your turn` must follow a `Worked example`. |
| 5.2 | major | check_unit.py:161-163 | Under 150 words of explanation before his first answer; under 250 per segment (teaching-craft.md:157; teaching-structure.md:144; Math Academy "minimum effective dose"). His record: 700 to 2,100 characters worked (B8). At most one new term per part (teaching-craft.md:148). | Up to 2,500 characters of prose per step; no count of new terms; no check of questions per step. | Max 2,100 characters of prose per step; max 900 characters before the first question in a Worked example; 2 to 5 questions per practice step (B9); a `new:` line per step naming at most one new idea. |
| 5.3 | major | check_unit.py:164-165, :175-179 | C48: "explain the code and why it's structured like that in every exercise" (applies to every skill; SKILL.md:62 says "every code block"). | The "How this code works" check and the code-line provenance check run only when `skill == "code"`. | Drop the `skill == "code"` condition on both checks. |
| 5.4 | major | check_unit.py (missing) | Mastery needs a real set (1.6); meaning items (4.1); short answer before options, options only after two misses (method-effectiveness.md:49, Adesope); every item has its worked solution for feedback (3.2); goal first (C41). | None of these are checked. | For production: Quick set has 10 items across two steps, 3 or more tagged `[meaning]`; each item has a line in `## Solutions`; the first step contains lines starting "You will be able to" and "You are done when". |
| 5.5 | minor | check_unit.py (missing) | Practice has the same shape as the worked example just shown (ai-tutoring.md:171; B13: a mismatched example was copied wrongly). | Not checked. | Each `Your turn` names its example (`shape: Worked example 1`); a reviewer (not the checker) signs it off. |

### Stage 6. `learn/facts.md` and the numbers the units will quote

| # | Sev | Where | What the research says | What was built instead | Exact fix |
|---|---|---|---|---|---|
| 6.1 | minor | production.md:202 vs facts.md:45-49 | One dated fact sheet (INTEGRATED.md:37-40). | The anchor card teaches "1.3 tokens per word" (an older OpenAI-era figure). facts.md: 0.75 words per token for older Claude models, and about 30% more tokens on Claude 4.7 and later. | Anchor card uses facts.md wording, with the model named. |
| 6.2 | minor | production.md:203 vs facts.md:35-37 | Same. | Anchor "cached read 0.1x". facts.md: 0.05x on Opus 5.5, 0.025x on Fable 5.1; 2x write for the 1-hour cache. | Anchor: "cache read 0.1x on most models; check facts.md for the model". |
| 6.3 | minor | production.md:116 | "Use one dated model everywhere" (review.md:118-119). | Exhibits use Sonnet 4.6 ($3/$15); llm-02 teaches Sonnet 4.6 and Sonnet 5 side by side. | Production exhibits use Sonnet 5 ($2/$10) and Haiku 4.5 ($1/$5) from facts.md unless the item is about switching models. |
| 6.4 | minor | facts.md (missing) | Every number from a run, facts.md or an exact quote (SKILL.md:66-67). | No production anchors (availability table, burn thresholds, latency figures). They will need exact quotes or calc runs each time. | Add a "Production anchors" section with the quoted source line and date for each (sre-book-appendix-a, sre-workbook-05, openai-latency-optimization). |

### Stage 7. Cohesion between the files

| # | Sev | Where | Problem | Fix |
|---|---|---|---|---|
| 7.1 | major | check_unit.py:26 (code) and the same pattern for every skill | Code's step list also has no worked step; C49 voided code-01 for exactly this. The production gap is not local: the template layer dropped worked examples for all applied skills (C45). | Apply the 5.1 two-shape fix to code, evaluation and design at the same time. |
| 7.2 | minor | skill-methods.md:232; curriculum-map.md:47; method-effectiveness.md:170 | "Friday: Production, mixed set" in three files, while the first unit of a class must be blocked (1.7). | Read as "mixed set from the second class on". |

---

## 3. Prioritised fixes

Do them in this order; the first four unblock everything else.

1. **Checker allows the research shape** (5.1, 7.1): two shapes per skill, first-contact with Worked example and Your turn steps.
2. **INTEGRATED.md row 17 and the frame** (2.1, 2.2): write the two production shapes and "Study or Commit, by placement".
3. **SKILL.md rule** (3.1, 3.4): worked example before any question on a new type; nothing asked that was not shown or told.
4. **Guess moved behind the worked estimate** (1.1, 1.2) and the Lever table before the pick (1.4).
5. **Measurement that can see his weak point** (1.6, 4.1, 4.2, 5.4): 10-item Quick set with 3+ meaning items; 10-item cold check.
6. **Explained solutions actually reach him** (3.2): a `## Solutions` block the guard allows.
7. **Knowledge-point structure and load limits** (1.8, 1.9, 5.2): goal step, one idea per knowledge point, 2,100-character cap.
8. **Placement and fading in the engine** (2.3, 4.3), and the first-try alarm (4.4).
9. C48 for every skill (5.3); interleave only taught classes (1.7); reveal after the full chain (1.5).
10. Minor items: timer (1.10), stale production.md rows (1.11), outside tasks (1.12), substitution line (1.13), facts (6.1 to 6.4), variants (4.5), parallel unit (4.6), card marking (3.3), shape tag (5.5), wording (2.4, 7.2).

---

## 4. The corrected unit template for production

Every rule below names its source. Nothing here is new method; it is the research the chain dropped, put
back in the order it was written.

### 4a. Header

```
id: production-NN
skill: production
shape: first-contact | later
class: C1 to C7 (production.md 3a)
level: rung this unit serves (engine picks by rung)
scored: Quick set
skip_if_placed: Worked example 1, Worked example 2   (later shape only)
sources: learn/facts.md, <saved source files quoted>
runs: runs/production-NN-*.json (every number, made by calc.py)
code: <program files for every code block>
```

### 4b. First-contact shape (the first unit of each class; about 35 to 40 minutes)

| # | Step | Content rule | Source |
|---|---|---|---|
| 1 | **The job** | The problem in 4+ plain sentences with a real stake in money; "You will be able to..." ; "You are done when..."; optionally one two-option pick with all data given, unscored, answered in step 2. Under 900 characters before the pick. | C41, C34, C39; teaching-structure.md:149-150; teaching-craft T1, T3; Pan and Carpenter pre-questions g = 0.66 (teaching-methods.md:170) |
| 2 | **Worked example 1** (knowledge point 1) | Everyday picture in 1 or 2 sentences with its break point; the exhibit; which numbers and why (the number-picking); the formula with each term in plain words; the rough size first, then one substitution line per term with units; code that computes it, with **How this code works**; the answer and what it means; one common wrong turn, labelled wrong before it is shown; then **one** self-explanation question on the key step. | B1, B2; Yale primer (production.md:36); CFA layout (skill-methods.md:170-178); Mahajan modelled estimate (production.md:40); C48; T23; self-explanation g = 0.55, key step only (method-effectiveness.md:56, :127) |
| 3 | **Your turn 1** | Same shape, new surface. Completion: the first link done, he does the rest. 2 to 4 short-answer questions; any direction question as two options. | Completion problems (method-effectiveness.md:52); ai-tutoring.md:171; B9; E12 |
| 4 | **Worked example 2** (knowledge point 2) | As step 2, one new idea only. | Math Academy knowledge points (teaching-craft.md:37, :115) |
| 5 | **Your turn 2** | As step 3. | same |
| 6 | **Worked example 3: what the number means** | Before minus after, written as a subtraction, with the one-side slip labelled wrong; which share is the lever; which way an uncertain input bends the bill. Never faded until passed cold. | E11, E12; review.md:108, :206; INTEGRATED.md:94-95 |
| 7 | **Your turn 3** | 2 or 3 meaning items; direction as two options. | E12 (0/3 open, 3/3 two options) |
| 8 | **Lever** | Table first (each option and the saving it gives, computed); then one pick of two with the deciding number. | production.md:257; contrasting cases (method-effectiveness.md:64) |
| 9 | **Quick set** (first half) | Before it: his score prediction (engine `predict`). 5 short-answer items, this class only, new surfaces; 1 or 2 `[meaning]`. | Kulik bar (method-effectiveness.md:55); Adesope short answer first (:49); calibration as a measure (:84) |
| 10 | **Quick set** (second half) | Preceded by the Solutions message for items 1 to 5. 5 more items, 2 or more `[meaning]`. Scored together: pass 9 of 10. | same |
| 11 | **Close** | Preceded by the Solutions message for items 6 to 10. His line: "Next time I see X, I do Y." | INTEGRATED.md:21-22 |

Target first-try rate on steps 3, 5, 7: about 80%. Under 70% means the unit overloaded him (4.4).

### 4c. Later shape (second unit of a class onward)

1. **First step** (90 seconds, one new item, he writes only his first move and why; recorded, not scored).
   Right twice in a row across units: Worked examples 1 and 2 are skipped (Kalyuga and Sweller).
2. **Guess** (one rough number, after a worked estimate in this class has been seen; a range only after
   the calibration segment, trial).
3. **Chain** (his full chain in words and units; revealed only after he finishes; feedback on the first
   wrong link).
4. **Run** (code computes his chain; How this code works; he says in one line why his guess was off, if it was).
5. **Worked example 3: meaning** (kept until passed cold), then **Your turn 3**.
6. **Lever**, **Quick set** (10 items, interleaved across *taught* classes, 3+ meaning), **Close**.

### 4d. Delivery rules for every step

- One step per message, 2,100 characters of prose at most, one new idea (B5, B8, C25).
- Every term explained in the sentence where it first appears (C1, C33; glossary gate).
- Every number from a calc.py run or facts.md; quoted source numbers inside exact quotation marks.
- Feedback before a step: what was right, or the first wrong move and why, at most 3 points, no question.
- Stuck order: his own earlier number, two options, one everyday picture, the answer with a reason and his
  one-line say-back (D1, D4, D2, D7).
- Solutions for Quick set items come as their own message, from the unit's `## Solutions` block.

---

## 5. Sample first unit: production-01, "What one AI call costs"

Class C1 (one-formula cost), node P1. Prerequisites met: tokens and the price per million tokens were taught
in llm-02. Prices from `learn/facts.md` (checked 2026-09-24): Claude Sonnet 5 $2.00 input and $10.00 output
per million tokens; Claude Haiku 4.5 $1.00 and $5.00; Claude 4.7 and later make about 30% more tokens for the
same text than Sonnet 4.6. All other numbers below were computed with Python on 2026-09-25; before the unit is
used, each must be saved as a run with `learn/calc.py` so the checker can trace it.

Every message he receives is written out below, in order. Keys and marking rules are never shown to him.

### Message 0 (engine, before the unit)
The day's recall cards, one per message, as now. Not part of this unit.

### Message 1. Step: The job

> **The job**
>
> You are building a study helper for students in Pakistan. Each time a student asks something, your app
> sends one call to Sonnet 5, the Claude AI model we price in this unit. Every call carries three things:
> fixed instructions that tell the model how to behave (the same 6,000 tokens on every call), the student's
> question (about 500 tokens) and the answer the model writes (about 400 tokens). The provider charges for
> every token, and the price is different for tokens you send in and tokens it writes back. If you guess the
> bill wrong, a free app that looked cheap can cost more than it earns.
>
> You will be able to: work out what one call costs, what one student costs a month, and which part of the
> bill to cut first.
>
> You are done when: you get 9 of 10 right on a short set at the end, and again 7 days later.
>
> One quick pick before we start (it is not marked; a guess is fine): which part of this bill do you think
> is biggest?
> A. the 400-token answer, because written tokens cost 5 times more
> B. the 6,000 fixed instruction tokens, because they are sent on every call
>
> Say A or B and one line why.
>
> **Your answer.**

Key: not scored. The answer is B (70.6% of the bill). Any letter with a reason is fine; the reveal is the
first line of message 2.

### Message 2. Step: Worked example 1 (what one call costs)

Feedback before the step (under 400 characters): "It is B: the fixed instructions are 70.6% of the bill. Here is how
you work that out."

> **Worked example 1: the cost of one call**
>
> Picture a photocopy shop that charges Rs 2 for every page you hand in to be read, and Rs 10 for every
> page it prints for you. A thick stack in and a thin reply out can still cost more than the reply.
> (Where it breaks: the shop prices pages, the model prices tokens.)
>
> **The numbers, and why these ones.** Input tokens are everything you send: the 6,000 fixed instructions
> plus the 500-token question, so 6,500. Output tokens are what it writes back: 400. Sonnet 5's prices
> (facts.md, checked 2026-09-24): $2.00 per million input tokens, $10.00 per million output tokens.
>
> **Rough size first.** 6,500 input tokens at $2 a million is about 1.3 cents. 400 output tokens at $10 a
> million is 0.4 cents. So about 1.7 cents a call.
>
> **The formula.** cost of one call = input tokens x input price per token + output tokens x output price per token.
> Price per token = price per million / 1,000,000.
>
> - input part: 6,500 x $2 / 1,000,000 = $0.013
> - output part: 400 x $10 / 1,000,000 = $0.004
> - one call: $0.013 + $0.004 = **$0.017**
>
> ```python
> input_tokens = 6000 + 500
> output_tokens = 400
> cost = input_tokens * 2 / 1_000_000 + output_tokens * 10 / 1_000_000
> print(round(cost, 4))
> ```
> ```output
> 0.017
> ```
> **How this code works.** The first line adds the two things you send, so the input count is built from
> the exhibit, not typed in. The second holds what comes back. The third line is the formula: each count
> times its own price, divided by 1,000,000 because prices are per million. `round(cost, 4)` keeps 4 places
> so the tiny number is readable.
>
> **What it means.** The answer is dearer per token, but the instructions are 15 times bigger and go out
> on every call, so they cost more.
>
> **Wrong turn (this is wrong):** pricing all 6,900 tokens at the input rate gives $0.0138, which hides
> the answer's real cost.
>
> Question: in one line, why is the 500-token question priced at $2 a million and not $10?
>
> **Your answer.**

Key: not scored (self-explanation). Right: it is something you send in, so it is input. If wrong: point at
the "Input tokens are everything you send" line (stuck order step 1).

### Message 3. Step: Your turn 1

> **Your turn: a homework helper**
>
> Same shape, new app. A homework helper on Sonnet 5 sends 3,000 tokens of fixed instructions and a
> 200-token question, and gets back a 300-token answer.
>
> The input part is done for you: 3,200 x $2 / 1,000,000 = $0.0064.
>
> 1. What is the output part?
> 2. What does one call cost?
> 3. If answers doubled to 600 tokens, would the cost of a call go up by more than half or by less than half?
>
> **Your answer.**

Key: 1 = $0.003 (300 x $10 / 1,000,000). 2 = $0.0094. 3 = less than half (it becomes $0.0124, up 31.9%,
because only the output part doubles). Not scored; first-try rate recorded for the 4.4 alarm.

### Message 4. Step: Worked example 2 (what one user costs a month)

> **Worked example 2: from one call to one student a month**
>
> Back to the study helper at $0.017 a call. The exhibit adds: a student asks 20 times a day, for 30 days.
>
> **Why these numbers.** A month's bill is calls in a month times the cost of one call. Calls in a month =
> calls a day x days: 20 x 30 = 600 calls.
>
> - one student a month: 600 x $0.017 = **$10.20**
> - 1,000 students a month: 1,000 x $10.20 = **$10,200**
>
> **Where the money goes, per call:**
>
> | Part | Cost | Share of the bill |
> |---|---|---|
> | fixed instructions (6,000 x $2 / 1,000,000) | $0.012 | 70.6% |
> | the answer (400 x $10 / 1,000,000) | $0.004 | 23.5% |
> | the question (500 x $2 / 1,000,000) | $0.001 | 5.9% |
>
> A share is one part divided by the whole: $0.012 / $0.017 = 70.6%.
>
> **What it means.** Every extra student adds $10.20 a month, and almost three quarters of it pays for the
> same instructions sent again and again.
>
> The rule, last: monthly cost = cost per call x calls a day x days x users.
>
> Question: in one line, why does the monthly bill grow with the number of students but the shares in the
> table stay the same?
>
> **Your answer.**

Key: not scored. Right: every student's calls have the same parts, so each part grows by the same factor.

### Message 5. Step: Your turn 2

> **Your turn: the homework helper, a month**
>
> The homework helper costs $0.0094 a call (your answer in the last step). A student uses it 10 times a
> day for 30 days.
>
> 1. What does one student cost a month?
> 2. What share of each call is the fixed instructions ($0.006)?
> 3. Which part is the biggest share: the fixed instructions, the question or the answer?
>
> **Your answer.**

Key: 1 = $2.82 (300 calls x $0.0094). 2 = 63.8%. 3 = the fixed instructions. Not scored.

### Message 6. Step: Worked example 3 (what a number means: a saving)

> **Worked example 3: which cut saves more**
>
> Your study helper costs $0.017 a call. Two ideas: (a) cut the fixed instructions in half, to 3,000
> tokens; (b) cap every answer at 200 tokens.
>
> **A saving is before minus after.** Work out the new cost, then subtract it from the old one.
>
> | | After | Saving per call (before minus after) | Per student a month (x 600) |
> |---|---|---|---|
> | (a) instructions 3,000 | $0.011 | $0.017 - $0.011 = **$0.006** | $3.60 |
> | (b) answers 200 | $0.015 | $0.017 - $0.015 = **$0.002** | $1.20 |
>
> **Wrong turn (this is wrong):** saying cut (a) "saves $0.011". That is the new cost, not the saving.
>
> **What it means.** Cut (a) saves 3 times as much, because it shrinks the biggest share. The biggest
> share is where to look first.
>
> **Which way does an unsure number bend the bill?** The 400-token answer was measured in a test week when
> students asked short questions. If real answers run longer, the true bill is higher than $10.20, never
> lower: more tokens can only add cost.
>
> **Where this stops:** shorter instructions can make answers worse. A cost number decides between options
> that are equally good; it does not tell you the answers are still good.
>
> Question: in one line, why is cut (a)'s saving $0.006 and not $0.011?
>
> **Your answer.**

Key: not scored. Right: $0.011 is what a call costs after the cut; the saving is the difference from $0.017.

### Message 7. Step: Your turn 3

> **Your turn: meaning**
>
> The homework helper costs $0.0094 a call.
>
> 1. If fixed instructions drop to 1,500 tokens, a call costs $0.0064. What is the saving per call?
> 2. The 300-token answers were measured on easy homework. Harder homework gets longer answers. Is the
>    true monthly bill higher or lower than $2.82?
>
> **Your answer.**

Key: 1 = $0.003 (before minus after). 2 = higher. Not scored; recorded for the alarm.

### Message 8. Step: Lever

> **Lever: pick one cut**
>
> A lever is the one change that moves the bill most. For the homework helper ($0.0094 a call, 300 calls a
> student a month), the two cuts you can make this week:
>
> | Cut | Cost per call after | Saving per call | Saving per student a month |
> |---|---|---|---|
> | A. instructions 3,000 to 1,500 tokens | $0.0064 | $0.003 | $0.90 |
> | B. answers capped at 150 tokens | $0.0079 | $0.0015 | $0.45 |
>
> Which cut do you make first, A or B? Give the one number that decides it.
>
> **Your answer.**

Key: not scored. A; the deciding number is the saving per call, $0.003 against $0.0015 (twice as much),
because instructions are the bigger share (63.8%).

### Message 9. (before the first scored step)

> Before the short set: what score out of 100 do you expect on the next 10 questions?

Recorded with `engine.py predict production-01 <p>`.

### Message 10. Step: Quick set (items 1 to 5)

> **Short set, part 1 of 2.** Numbers only, with the unit ($ or %). Prices: Sonnet 5 $2 in, $10 out per
> million tokens; Haiku 4.5 $1 in, $5 out.
>
> A tutor bot on Sonnet 5 sends 4,000 tokens of fixed instructions and a 100-token question, and gets a
> 500-token answer. Each student uses it 15 times a day for 30 days.
>
> 1. Cost of one call?
> 2. Cost of one student a month?
> 3. What share of each call is the answer? [meaning]
> 4. If answers are capped at 250 tokens, what is the saving per call? [meaning]
> 5. Moving the same bot to Haiku 4.5 would cut the cost of a call by about half or by about a fifth?
>
> **Your answer.**

### Message 11. Solutions 1 to 5, then Quick set (items 6 to 10)

Solutions message (from `## Solutions`, its own message):

> 1. Input 4,100 x $2 / 1,000,000 = $0.0082; output 500 x $10 / 1,000,000 = $0.005; call **$0.0132**.
> 2. 15 x 30 = 450 calls; 450 x $0.0132 = **$5.94**.
> 3. $0.005 / $0.0132 = **37.9%**.
> 4. The answer part falls from $0.005 to $0.0025: saving **$0.0025** (before minus after).
> 5. Haiku: 4,100 x $1 + 500 x $5 = $0.0066 a call, **about half** (both prices are half of Sonnet 5's).

Then the step:

> **Short set, part 2 of 2.**
>
> A summariser on Haiku 4.5 reads a 20,000-token document and writes a 300-token summary.
>
> 6. Cost of one call?
> 7. Which saves more per call: sending only the relevant 10,000 tokens, or capping the summary at 150
>    tokens? Give the saving. [meaning]
> 8. A teammate says sending 10,000 tokens "saves $0.0115 a call". Right or wrong, and what did they
>    work out? [meaning]
>
> Back to the tutor bot from part 1 ($5.94 per student a month):
>
> 9. Its 500-token answers were measured with the older Sonnet 4.6 token counter; Sonnet 5 makes about 30%
>    more tokens for the same text. Is the true bill higher or lower than $5.94? [meaning]
> 10. With 2,000 students, what is the monthly bill?
>
> **Your answer.**

Key (Quick set, both halves): Score: items right / 10, first reply only; a half answer (right number, wrong
or missing unit) counts wrong. 6 = $0.0215. 7 = the 10,000-token document, saving $0.01 (the cap saves
$0.00075). 8 = wrong; $0.0115 is the new cost, the saving is $0.01. 9 = higher. 10 = $11,880. Pass: 9 of 10.

### Message 12. Solutions 6 to 10, then Close

> 6. 20,000 x $1 / 1,000,000 + 300 x $5 / 1,000,000 = $0.02 + $0.0015 = **$0.0215**.
> 7. Document: $0.0215 - $0.0115 = **$0.01**. Cap: 150 x $5 / 1,000,000 = **$0.00075**. The input is 93% of this bill, so it is the lever.
> 8. **Wrong**: $0.0115 is the cost after the cut. Before minus after: $0.0215 - $0.0115 = $0.01.
> 9. **Higher**: more tokens for the same text can only add cost.
> 10. 2,000 x $5.94 = **$11,880**.

Then the step:

> **Close**
>
> Finish this line in your own words: "Next time I see an AI bill, I first ..."
>
> **Your answer.**

Key: not scored. Any line naming a real move (price input and output separately; find the biggest share;
saving = before minus after). Recorded with `engine.py close`.

### Cards (join the recall queue tomorrow; each has 4 surfaces, fix 4.5)

- Q: Sonnet 5, 5,000 tokens in, 200 out: cost of a call? | A: $0.012 || Q: Haiku 4.5, 8,000 in, 400 out? | A: $0.01 || Q: Sonnet 5, 1,000 in, 1,000 out? | A: $0.012 || Q: Haiku 4.5, 2,000 in, 100 out? | A: $0.0025
- Q: A cut takes a call from $0.02 to $0.014. Saving per call? | A: $0.006 (before minus after) || Q: $0.05 to $0.035? | A: $0.015 || Q: $0.009 to $0.006? | A: $0.003 || Q: $0.12 to $0.09? | A: $0.03
- Q: Output length measured on easy questions; real ones are harder. Bill higher or lower? | A: higher || Q: Instructions measured before you added two rules. Higher or lower? | A: higher || Q: Tokens counted with a tokenizer that makes fewer tokens than the real one. Higher or lower? | A: higher || Q: You price at the input rate for every token. Your number is too high or too low? | A: too low

(Each card value must be saved as a calc.py run before use.)

### Cold check, 7 days later (two messages of 5; pass 9 of 10)

Before it: "What score out of 100 do you expect?" (`predict production-01 <p> --cold`).

> **Cold check, part 1 of 2.** Sonnet 5: $2 in, $10 out per million tokens; Haiku 4.5: $1 in, $5 out.
>
> Your FBR tax assistant on Sonnet 5 sends 5,000 tokens of fixed instructions and a 300-token question,
> and writes a 600-token answer. Each user asks 8 times a day for 30 days. You have 500 users.
>
> 1. Cost of one call?
> 2. Cost of one user a month?
> 3. The whole month for 500 users?
> 4. What share of a call is the fixed instructions? [meaning]
> 5. Cutting the instructions to 2,500 tokens saves how much per call? [meaning]
>
> **Your answer.**

> **Cold check, part 2 of 2.**
>
> 6. A teammate says that cut "saves $0.0116 a call". Right or wrong, and what did they work out? [meaning]
> 7. What does one call cost on Haiku 4.5?
> 8. Your token counts came from Sonnet 4.6's counter; Sonnet 5 makes about 30% more tokens for the same
>    text. Is the true bill higher or lower than your answer to 3? [meaning]
> 9. Which cut saves more per call: answers capped at 300 tokens, or instructions cut to 2,500? Give both savings. [meaning]
> 10. What do all 500 users cost in one day?
>
> **Your answer.**

Key (Cold): Score: items right / 10, first reply only. 1 = $0.0166. 2 = $3.984. 3 = $1,992. 4 = 60.2%.
5 = $0.005. 6 = wrong: $0.0116 is the new cost; the saving is $0.005. 7 = $0.0083. 8 = higher. 9 = the
instructions ($0.005 against $0.003). 10 = $66.40. Pass: 9 of 10. Solutions block shown after each half, as
in the unit.

### What this unit deliberately leaves out, and why
- No estimation tree, no 90% range, no timer: not yet modelled for him (finding 1.1, 1.10). The rough
  estimate is shown in Worked example 1 so that Guess in production-02 has a model to follow.
- No caching, latency or error budgets: separate classes, taught days apart (production.md:200-201).
- No interleaving with other classes: this is the first class (finding 1.7).

---

## 6. Evidence boundaries worth keeping in view

- Every learning effect here is carried over from maths, physics, programming and medicine; none is tested
  on adults learning LLM cost work (production.md:273).
- "Guess first" has no direct evidence for a novice on a new procedure; its support is prediction before a
  demonstration (moderate, needs a basis) and worked estimation (quasi-experiment). Hence Guess only after a
  modelled estimate.
- The 80 to 85% practice target is Math Academy's stated design (self-reported), matched by his own record
  (78 to 80% with the template). It is an alarm threshold, not a proven optimum.
- The 9 of 10 bar is Kulik's 91 to 100% band on course tests; standardised-test effects of mastery are small
  (0.04 to 0.09). The cold check and the outside task (ScaleDojo level 6) are what show transfer.
