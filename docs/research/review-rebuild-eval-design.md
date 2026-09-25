# Review of the rebuild: evaluation and system design

Written 2026-09-25. Independent and adversarial. The only file edited is this one. Builders' reports were not
trusted: every claim below was checked against the files, the sources or a run.

**What was read.** `gap-audit-evaluation.md` and `gap-audit-system-design.md` (every finding and fix list),
`audit-pedagogy.md` (shared-layer findings), `learning-evidence.md` (C1 to C49), `structures/INTEGRATED.md`,
`structures/evaluation.md`, `structures/system-design.md`, `.claude/skills/faiz-teach/SKILL.md`, `learn/check_unit.py`,
`learn/engine.py`, `hooks/teaching-guard.py`, `learn/selftest.py`, both units, the HW3 key and README, the private
design excerpt file, the ScaleDojo chapter and the level JSON, all ten `design01-*` runs, `runs/eval-01-traces.json`
and `learn/code/eval-01/traces.py`.

**What was run.**
- Every HW3 trace the eval unit uses (36 traces) was printed in full, including the six the builder read only in
  part (47_31, 51_31, 57_24, 10_8, 10_9, 47_8), with every cut line listed, and each label checked against the
  quoted diet rule.
- Every Key label compared with the source label; every quoted reason compared with the cited trace's reasoning.
- Every design quotation compared with the excerpt file and `scaledojo_levels_unlocked.json`; every design number
  traced to its run.
- Both units through `check_unit.py`; `selftest.py`; synthetic transcripts through the guard in an isolated copy
  (committed guard and the working-tree guard), including Help, Retry, Cold, stuck-order messages, skipped steps
  and re-sent steps; engine flows in a temp copy (week 4 and week 6 sittings, a missed unit, the Retry record).
- Binomial pass chances for the Retry and Cold sizes.

**Files changed during the review.** `hooks/teaching-guard.py`, `learn/check_unit.py`, `learn/engine.py` and
`learn/selftest.py` were edited by someone else between 16:24 and 16:25 and are uncommitted. The units, structures,
INTEGRATED and SKILL.md are as committed in `43d45fb`. Line numbers below are from `43d45fb` unless marked "working
tree".

**Severity.** Blocker: he cannot be taught or recorded as built, or the build repeats what he rejected in C49.
Major: a fix is missing or wrong in a way he will feel in these units. Minor: real, small.

---

## Verdict per unit

| Unit | Verdict | Why |
|---|---|---|
| eval-01, "Does the recipe fit the diet?" | **Not ready** | The teaching is close to right: the standard comes first, then two worked examples with the expert's moves, a completion item, six warm-ups with the key's reason in the next message, a blind batch, then a two-step compare. All 36 labels and every quote are correct. It is blocked by the machinery (BL1) and by the first evaluation sitting, which puts an invented placement check and an invented rapid round next to it (BL2). Before it is taught, also fix the pass bar (E-M1), the Retry and Cold sizes (E-M2), the stuck-order material (S-M2) and the food facts never shown (E-M3). |
| design-01, "Long chats that get cut off" | **Not ready (content nearly ready)** | The worked example comes before any commitment, options are taught in toolbox steps, there is one decision per message, reveals come one decision at a time, and every quote and number checks out. It is blocked only by the shared machinery (BL1). Fix the TalkTherapy key (D-M1), the scoring description (D-M2), the single-item Retry and Cold (D-M3) and the public ScaleDojo answer quotes (D-M6) before teaching. |

**Counts: 2 blockers, 15 major, 16 minor (33 findings).**

---

## 1. Blockers

**BL1 (shared). The machinery is not in a state that can teach or record either unit.**
- Committed engine (`engine.py:311-318`): `predict --retry` is accepted by the parser (`:439`) but stores the
  prediction under the plain key, so `done <unit> --retry` always fails with "no prediction recorded for
  eval-01:retry". Run in a temp copy: "error: no prediction recorded for eval-01:retry". A missed unit can be
  re-taught but its Retry can never be recorded.
- Working tree (uncommitted): the engine bug is fixed, but the new checker fails all 7 units, including both
  reviewed here. It asks for a `Two options:` and a `Worked answer:` line in every try and scored Key. It splits
  `New:` on " and ", which now counts eval step 1 as 4 ideas and design Toolbox 1 as 5. It asks for a `New:` line
  on "How the scored part works" and "Compare: the expert's reasons". While the checker fails a unit, `engine.py
  today` will not serve it (`engine.py:268-269`) and the guard blocks every step of it (`teaching-guard.py:122-124`).
- Fix: finish one consistent set and commit it. Add the stuck-order lines to both units (see S-M2), reword the
  `New:` lines, rerun `check_unit.py` and `selftest.py`, and only then clear the units.

**BL2 (evaluation). The first evaluation sitting asks the tutor to invent two formats next to eval-01.**
- `engine.py:126-135`: in week 4, sitting 1, `today` prints eval-01, "evaluation rapid round (8 min)" and
  "evaluation placement check before the first unit" (run: slot 21). No placement item exists anywhere, and no
  keyed rapid-round bank exists. `evaluation.md:111-112` says rapid rounds start at the second sitting and only from
  keyed items. INTEGRATED `:79` still says a placement check is needed because "he already did L5 and L6", the
  premise F15 showed to be wrong.
- The tutor would write both, and the key, from nothing (SKILL.md `:70-71` forbids this; F9, F26). That is three
  new formats in his first evaluation sitting, the overload of B5 and C49.
- Fix: no placement for eval-01, or write F15's two-excerpt placement item as a checked unit. Print the rapid
  round only from the second evaluation sitting and only once a keyed bank file exists. Record both.

---

## 2. Every audit finding, checked

### 2a. Evaluation audit (F1 to F28)

| # | Status | Evidence | What is left |
|---|---|---|---|
| F1 worked-example ladder | PARTLY | Unit: two worked examples and a completion item (eval-01 `:43-151`); `evaluation.md:72-74` puts the ladder per node | `evaluation.md:56-57` still argues that "Full ladder, slow" ignores L5 and L6, and `:151` still skips the worked example after a one-trace test with an open code. Delete both |
| F2 standard first | FIXED | eval-01 `:11-36` quotes the course rule and its own pass and fail examples | |
| F3 modelled moves | FIXED | numbered moves with a dead end, `:62-68`, `:100-106` | The dead ends are the tutor's own words, not the key's (F3 said "rearranges, never adds"). Label them "our note" (minor m6) |
| F4 one node per unit | FIXED | eval-01 teaches labelling only | |
| F5 no grouping on a one-criterion product | FIXED in unit | eval-01 has no grouping step | INTEGRATED `:18` still lists "Group the failures ... Count and decide" as the evaluation structure (E-M5) |
| F6 counts before kappa | FIXED | every result in eval-01 is a count (`:340-346`, `:594-601`) | INTEGRATED `:79` "agreement statistics taught first" is stale |
| F7 one set of rate names | PARTLY | `evaluation.md:104-109` is consistent | `docs/glossary.md:36-37` still labels the catch rate "(TPR)" and the clear rate "(TNR)", the opposite of the HW3 line in `evaluation.md:108` |
| F8 clean key | FIXED for this unit | All 36 traces are HIGH confidence, none is disputed, all read in full by this review; the labels are right on the stated rule (section 4) | Step 1 calls HW3's labels "the expert's label" (`:13`). They are likely model-written. The wording is acceptable because he is invited to argue with the key |
| F9 keyed pool for rapid rounds and parallel units | NOT FIXED | `evaluation.md:165` still uses HW2's unlabelled rows as the rapid-round example; the engine prints rapid rounds anyway (BL2) | Pool run: after eval-01 only 7 HIGH FAILs are unused; 4 are low-carb (excluded) and 48_34 is a "gluten-light" look-alike. No parallel unit and no larger cold set can come from HW3 (E-M6) |
| F10 clear to subtle | FIXED | warm-up 1 repeats the worked cue (chicken, vegetarian); look-alikes come later | |
| F11 reflection table from level 2 | NOT FIXED (deferred) | not in `evaluation.md` | Add it to the level-2 unit spec |
| F12 two-part close | FIXED | `:634-644` | |
| F13 the job first | FIXED | `:11-36` | |
| F14 level bars | PARTLY | INTEGRATED `:70`, `engine.py:48`: raw agreement of 80% | No catch-rate floor. Always PASS scores 9 of 12 (75%); catching 1 of 3 fails passes at 10 of 12 (E-M1) |
| F15 placement premise | NOT FIXED | INTEGRATED `:79`; `evaluation.md:151`; engine prints it only (`:134-135`) | BL2 |
| F16 worked example in INTEGRATED | FIXED | INTEGRATED `:35-42` (show, try, alone) | |
| F17 SKILL gives worked examples a place | FIXED | SKILL `:29-36` | |
| F18 per-trace feedback | FIXED | one warm-up per message; the key's reason opens the next body (`:155`, `:186`, `:213`, `:250`, `:283`, `:311`, `:338`); two compare steps | The gate is counted by him and checked by the tutor, not computed or recorded by the engine (minor m5) |
| F19 stuck order for a binary label | NOT FIXED | SKILL `:55-58` step (2) "two options"; no eval Key has a prepared rung | S-M2 |
| F20 one confidence scale | FIXED | "sure or not sure" everywhere; `--confident-wrong` | |
| F21 C1 to C49; code explanation in every skill | FIXED | SKILL `:11`; `check_unit.py:201` applies to any skill | |
| F22 checker allows the template | FIXED | `check_unit.py:117-131` (kind-based order) | |
| F23 message size including traces | FIXED | `MAX_BODY = 2600` including fences (`:33`); at most 4 excerpts a step; largest eval step 2,411 characters | |
| F24 excerpts checked against the source | PARTLY | `traces.py` checks excerpt lines, rule lines and HIGH confidence | It does not compare each Key label with the source label, and it matches quotes against the whole corpus, not the cited trace. `check_unit.py` does not run it (E-M4). This review checked both by hand: all correct |
| F25 statistics computed, one cold rule | NOT FIXED | no `engine.py labels`; `engine.py:40-41` still has the one-unit `traces >= 24` kappa rule; cold is `Cold >= 0.8` (`:361`) while `evaluation.md:250` says "kappa within 0.10" | Per-step scoring (matches / 3) is mechanical, which lowers the risk. Align the three cold rules (E-M5) |
| F26 rapid round and placement on day 1 | NOT FIXED | `engine.py:126-135` (run) | BL2 |
| F27 glossary evaluation words | NOT FIXED | `glossary.md` watchlist has no trace, label, codebook, calibrate | eval-01 defines "label" inline, so this is minor (m14) |
| F28 licence and trace ids | FIXED | header `:7`; every Key names its trace | |

### 2b. System design audit (R1 to X4)

| # | Status | Evidence | What is left |
|---|---|---|---|
| R1 excerpts per unit | FIXED | `private/research-base/system-design/excerpts/design-01.md` exists, git-ignored, never committed (`git log -- private` is empty) | |
| R2 QuickChat as practice only, no simulation numbers | PARTLY | unit uses QuickChat for "Guess the move" only; excerpt notes the simulation lines are not used | `system-design.md:179` still gives the unsourced twist "power users grow to 30% of traffic" |
| S1 worked example before guess the move | FIXED | `system-design.md:90-103`; design-01 `:98-161` before `:163` | |
| S2 modelling | FIXED | cues, options, dead ends, pick, three-line replay (`:104-121`) | |
| S3 toolbox before use | FIXED | `system-design.md:48`, `:96`; design-01 `:41-96` | |
| S4 first design only late; evidence graded down | PARTLY | `:116-118` | `:55` and `:69-70` not reworded; `:270` still grades commit-first "moderate"; INTEGRATED `:19`, `:81` still schedule "First design" and "first full design session" in weeks 7-8, and INTEGRATED wins on conflict (`:6`) (D-M5) |
| S5 rung ladder | FIXED | `:105-113`, `:159-161` | `:244` pace line ("2 Study + 3 to 4 Crit") is stale (minor) |
| S6 full worked-example anatomy | PARTLY | rung 1 is one decision, so an estimate and a check against the brief are not needed yet | The 10-part anatomy is not restated anywhere for rungs 3 and up |
| S7 no tutor-written worked cases | PARTLY | design-01 uses the ScaleDojo chapter and interview pair | `system-design.md:142` still lists C1 cases "worked by the tutor" from outline-only files |
| S8 no hidden fact sheet | PARTLY | `:115` | `:43` still says "Claude plays the customer from a hidden fact sheet" |
| S9 one decision per step, 80% target | FIXED | `:87-88`; unit follows it | "Under 60% moves a step down a rung" is not implemented |
| S10 design jargon in glossary | PARTLY | only "context window" was added to the watchlist | sliding window, system prompt, cue, DAU, turn are defined inline in the unit, so minor (m14) |
| S11 anchored rubric, second marker | NOT FIXED | `:193-208` has no anchors; `:186` "Any design meeting the numbers passes by his rubric" | Not needed at rung 1; needed before rung 3 |
| S12 Close checked before recall | PARTLY | design-01 `:303-305`; `system-design.md:102` | SKILL `:41` records his line with no marking step; `engine.py:382-386` stores whatever it is given; `system-design.md:221` still says cards "from his own AARs" |
| S13 drills only after their topic | NOT FIXED | `engine.py:128-129` prints drills from week 6 with no material | D-M4 |
| S14 problem first, toy example, picture | FIXED | `:17-21`, `:48-52` | |
| S15 at most 3 feedback points | FIXED | `:119` | |
| I1 show step in the shared frame | FIXED | INTEGRATED `:35-42` | |
| I2 design owns its supportive information | PARTLY | `system-design.md:96` | INTEGRATED `:80` still says design needs only production's cost and latency classes |
| I3 first-step test | PARTLY | `system-design.md:162-163` | No engine command; nothing records it |
| I4 design template | FIXED | `system-design.md` section 2 | |
| K1 per-decision steps | FIXED | "Guess the move 1", "2", each opening with the previous reveal | |
| K2 scoring explained before prediction | PARTLY | design-01 `:213-226` | It leaves out the "dropped move" and "cost" parts that the Keys mark (D-M2) |
| K3 prepared "Simpler" in every scored Key | NOT FIXED at HEAD | TalkTherapy and Decision note have no `Simpler:`; the working-tree checker now asks for different labels | S-M2 |
| K4 C1 to C49 | FIXED | SKILL `:11` | |
| E1 study units can pass and be recorded | FIXED (mostly) | `engine.py:44-45` mean of scored steps, `BAR design = 70` | The `rung:` header is never read; the bar is 70, not the audit's trial of "no scored step at 0 and mean 0.8" (a documented choice, INTEGRATED `:71`) |
| E2 rubric cold check | NOT FIXED (not needed at rung 1) | `engine.py:361` | |
| E3 drills as units | NOT FIXED | `engine.py:128-129` | D-M4 |
| E4 range checks | NOT FIXED | `engine.py:337` exempts rubric from any range | minor (m13) |
| C1 checker per rung | FIXED | kind-based order | |
| C2 `given:` needs a source | PARTLY | `given:` is banned from bodies (`check_unit.py:203`), and the unit's Key `given:` lines do carry sources | The checker does not require the source tag, and any body line starting "Suppose" is exempt from number checks with no tag (`:84`) |
| C3 design rules enforced (wins on, effect on) | NOT FIXED | no design-specific checks | The unit's table has both columns anyway |
| C4 shorter prose cap | NOT FIXED | cap stays 2,600 | minor |
| X1 one weekly shape | NOT FIXED | `system-design.md:229-244` (Wed Design Crit, Sat drill) vs INTEGRATED `:93-103` vs `engine.py:121` (slots 2 and 5) | D-M5 |
| X2 plain step names | PARTLY | section 2 is plain | `:179-186` keep Kata, Design Crit, ADR, twist |
| X3 one stuck order | PARTLY | `:120` | `:59` still promises "four cards ... when stuck" |
| X4 C32 and C35 enforced | NOT FIXED | same as C3 | |

### 2c. Shared-layer findings from `audit-pedagogy.md`

| # | Status | Evidence |
|---|---|---|
| C1 worked example required | FIXED | `check_unit.py:120-121` first step must be a show |
| C3 one hint rule | PARTLY | SKILL `:38` (hint 0.5, answer 0); whether sending a Help block counts as a hint is not stated |
| C4 cold bar and item count | NOT FIXED | eval Cold has 3 items, design Cold 1 (E-M2, D-M3) |
| C5 line-by-line answer | FIXED | SKILL `:53-54` |
| C6 one stuck order, re-send after a corrective | PARTLY | INTEGRATED `:43-45` and SKILL `:55-58` agree; the committed guard blocks re-sending a step (`:130-131`, tested), the working tree allows it; the engine's RETRY note (`:181`) says to re-teach show steps, which the committed guard blocks |
| C7 template in teaching steps | PARTLY | both units follow it; the checker does not check it |
| C9 evaluation bar and kappa | PARTLY | kappa is not used before it is taught; the bar has no catch floor (E-M1) |
| C11 corrective loop | PARTLY | Help and Retry exist; no parallel unit exists and the eval pool cannot supply one (E-M6) |
| C12 rungs drive selection | NOT FIXED | `engine.py:169-191` ignores the rung |
| C13 cards only after a pass | NOT FIXED | `engine.py:372` adds cards on every session, passed or not |
| C14 one new format per sitting | PARTLY | weeks 1-2 fixed (`:258-259`); week 4 sitting 1 is not (BL2) |
| C15 message cap including code | FIXED (2,600) | |
| C16 freeze does not protect teaching gaps | FIXED | INTEGRATED `:57-59` |
| T1, T2 several items, corrective | FIXED for sessions | 12 scored labels, 3 scored design answers, Help blocks |
| T3 prediction after practice | FIXED | eval `:346`, design `:224` |
| T4 self-graded recall | NOT FIXED | SKILL `:26-27` |
| B1, B2 stuck order teaches, prepared help | PARTLY | Help blocks exist; rungs (2) and (4) have no prepared text (S-M2) |
| B4 check question before a step | NOT FIXED | guard `:118-119` still blocks any "?" in feedback (tested) |
| B5 guard fails closed | NOT FIXED | guard `:139-140` |
| M6 recall blocked by skill for 2 weeks | NOT FIXED | `engine.py:200-211` interleaves from day 1 |

---

## 3. Findings (shared, evaluation, design)

### Shared

**S-M1 (major). The guard does not enforce the teaching order inside a unit.** `teaching-guard.py:127-138` checks
only that a unit starts at step 1 and that a finished unit is not left open. Tested on the committed and the
working-tree guard: after step 1 of either unit, the first scored step ("Label the batch 1", "Your move on
TalkTherapy") is allowed straight away, skipping every worked example and try. Retry and Cold are also allowed
mid-unit, before any miss is recorded. Fix: allow step i only if i equals the saved index plus one (or the same
index, for a re-send after a corrective). Allow Retry only after a recorded miss, and Cold only when `today` lists
it.

**S-M2 (major). Stuck rungs (2) and (4) have no prepared text, so the tutor must improvise or be blocked.**
SKILL `:55-58`: (2) two options, (4) the answer worked line by line, and "never improvise new prose". No try or
scored Key in either unit has prepared two options or a worked answer (design has `Simpler:` on most steps, eval
has none). Tested: an improvised two-option question that ends with the ask marker is blocked ("does not come from
a checked unit"). A prepared Key line sent together with a step is blocked as key text. The same text without the
ask marker is not checked at all. For a binary label, "two options" only repeats the question (F19). Fix: in every
try and scored Key add `Two options:` (for labels: F19's rungs, "which line do you check first, the rule or the
ingredient?") and `Worked answer:`. Say in SKILL.md that stuck rungs 1, 2 and 4 go without the ask marker, or let
the guard accept lines tagged for the stuck order.

### Evaluation

**E-M1 (major). The 80% bar sits just above labelling everything PASS, and nothing checks the failures.** The
batch has 3 FAIL and 9 PASS (`:589`). Always PASS scores 9 of 12 = 75% and just misses. Catch one of the three fails
and pass everything else: 10 of 12 = 83%, a pass with a catch rate of 1 in 3. `evaluation.md:51-53` warns about
this exact trap, and the unit's own Compare Key calls question 2 (fails caught) "the one that matters most"
(`:607`). INTEGRATED `:70` and `engine.py:48` use raw agreement only. Fix: pass = at least 10 of 12 and at least 2 of
the 3 expert FAILs also failed. Record the catch count as a step (the engine already accepts `missed_fail`), and
pool it over units later.

**E-M2 (major). The Retry (4 items) and Cold (3 items) at 80% need a perfect score, which is noise, not a
measure.** The engine passes Retry and Cold on `value * 100 >= 80` (`engine.py:361`), so the Retry needs 4 of 4
and the Cold 3 of 3. Run: a learner who is truly right 85% of the time passes the Retry 52% of the time and the
Cold 61%. At 90% it is 66% and 73%. One slip fails the item, and a failed Cold triggers re-teaching (working-tree
engine). `evaluation.md:250` itself plans 10 cold traces. Fix: 10 items each, pass at 8 or more of 10 (85% learner:
82% pass chance; 90%: 93%) with at most one expert FAIL passed. The HW3 pool cannot supply this (E-M6), so add
person-labelled items first. Until then, record Retry and Cold as a trial and do not gate mastery on them alone.

**E-M3 (major). Some questions need food facts the unit never shows.** "Finish the expert's work" (`:143-151`,
his first try item) asks what spaghetti, Parmesan and crusty bread mean under paleo. The Key counts him right only
"if he says FAIL with spaghetti as a grain", but "pasta and bread are wheat, and wheat is a grain" is never stated
before this question; step 1 only says soy sauce contains wheat. "Grain" is never explained. A student who fails it
on the Parmesan (dairy), a correct route, is marked not right. The scored batch then depends on facts that appear
only in Help blocks he may never see: shrimp is seafood (item 5; stated only in Help `:780`), cod is a fish (item
6), tofu is made from soybeans (item 11), and almond and coconut flour contain no wheat (item 12; "flour" means
wheat to most readers in Pakistan). "Vegan", "gluten" and "Parmesan" are used before they are explained (`:18-20`).
Fix: one "food facts you need" line in step 1 or before step 4 (pasta, bread and naan are wheat, a grain; shrimp
(jhinga) is seafood; cod and salmon are fish; tofu is made from soybeans; almond and coconut flour have no wheat;
vegan means no animal products at all). Accept any correct banned line as right in step 4.

**E-M4 (major). The source check does not check what matters most.** `traces.py` confirms each excerpt line
exists and each trace is HIGH confidence. It does not compare the Key's label with the source label, it accepts a
quote found in any of the 101 records rather than the cited one, and `check_unit.py` never runs it (F24). A
mislabelled Key or a quote attached to the wrong recipe would pass. This review checked all 36 labels and every
quote by hand, and all are right. Fix: `traces.py` fails on any Key label that differs from the source and on any
quote that is not in the cited trace. The checker fails a unit whose listed verifier run is older than the unit
file.

**E-M5 (major, cohesion). The evaluation documents still disagree on the steps, the bar, the cold rule and the
rate names.** INTEGRATED `:18` lists "Group the failures" and "Count and decide" for every unit. `evaluation.md:238`
sets mastery at kappa 0.70 and catch 0.85, INTEGRATED `:70` at 80% raw, and the engine follows INTEGRATED.
`evaluation.md:250` says cold is "kappa within 0.10", while the engine uses `Cold >= 0.8`. `evaluation.md:151`
keeps the old placement skip. `glossary.md:36-37` gives TPR the opposite meaning to `evaluation.md:108`.
`evaluation.md:260` says a 25-minute unit; eval-01 is 18 messages plus warm-up feedback. Fix: make
`evaluation.md` sections 3b, 3c, 5b, 5c and 6 match INTEGRATED and the engine, and fix the glossary line.

**E-M6 (major). The clean key pool is used up.** Run: HW3 has 21 HIGH FAILs and eval-01 uses 14. Of the 7 left,
4 are low-carb (excluded for needing nutrition knowledge) and 48_34 is a "gluten-light" look-alike. The engine's
second-miss path needs a parallel unit (`engine.py:182-187`), and E-M2 needs about 6 more FAILs. None of these can
come from HW3. Fix: a person labels HW3 `raw_traces.jsonl` against the quoted rule, or build class-3 units from
HW5. Count the clean pool before the next eval unit is written.

### Design

**D-M1 (major). The TalkTherapy key scores 0 for a move the brief points to.** The brief's problem (`:237`) is
that the bot asks "So tell me about yourself" two messages after the patient shared a story. In the toolbox's
terms, that means no history is being sent at all, and "send everything" is the move that fixes it. The lab's own
missions start with "Add Conversation Memory" (resend the chat) and only then "Enable summarization after 30 turns".
The Key gives 0 to "send everything" (`:257`), although the gap audit's sample gave 0.5 for it with the fit
caveat. A student who reasons correctly from the first symptom is marked wrong on a scored step, and the Decision
note repeats the same decision, so one reading error costs two of the three scored answers. Fix: drop the "2
messages later" symptom from this brief (keep the two "Must" lines), or score "send everything, then summarise once
sessions outgrow the window" as 1 and "send everything" with "only while it fits" as 0.5.

**D-M2 (major). The scoring he is shown is not the scoring he gets.** "How the scored part works" (`:217-220`)
describes "your pick" and "a fact from the brief". The TalkTherapy Key also requires "one move you dropped, and
why" (`:257`), and the short-chats Key requires "what the team's plan would cost" (`:279`). His prediction is asked
without that data (C39, K2). Fix: one line per scored step naming its three parts.

**D-M3 (major). Retry and Cold are one item each at bar 70, so only a perfect answer passes.** Each is scored 1,
0.5 or 0 (`:417`, `:433`); 0.5 is below 70. Fix: three items each (a move, a start point, a short-chat case), pass
at a mean of 0.7.

**D-M4 (major). Design drills are printed from week 6 with no drill material.** `engine.py:128-129` adds "design
drill (15 min) ... compare with a weak and a strong expert answer" at sittings 5 and 7 from week 6. No drill unit,
key or topic list exists, so the tutor would pick a ScaleDojo pair, perhaps on a topic he has not studied (E3,
S13). Fix: do not print drills until drill units exist in `learn/units/design-drill/`, each tied to a taught unit.

**D-M5 (major, cohesion). The design documents contradict the rebuilt ladder, and INTEGRATED wins.**
INTEGRATED `:19` still describes design as "Read the brief, First design ... the first two designs of each type
are guess the move", and `:81` schedules the "first full design session" for weeks 7-8. The ladder puts a full
design at rung 5, after completion, faded and first-step checks. INTEGRATED `:6` says it wins on conflict.
`system-design.md` keeps `:43` (hidden fact sheet), `:142` (C1 cases "worked by the tutor" from outline files),
`:179` (unsourced 30% twist), `:186` (rubric-only pass), `:221` (cards from his own AARs), `:229-244` (Wed/Sat
week, "Design Crit" and "Study variant") and `:270` (commit-first graded "moderate"). The engine runs two design
units a week (slots 2 and 5), but only one exists. Fix: rewrite INTEGRATED rows `:19`, `:80-81` to the rung ladder
and delete or correct the listed lines.

**D-M6 (major, licence). ScaleDojo answer keys are published in a public repository.** `gh repo view`:
frahman2310/FaizOS is PUBLIC, and `learn/units/` is tracked. design-01 quotes the lab's mission answers
("Enable summarization after 20 turns to prevent context overflow", "... after 30 turns ..."), a hint line, and a
sentence from a paid interview-signal answer ("Both symptoms point at the same root cause"). Each quote is short,
and the full texts stay in the git-ignored excerpt file (good). But no ScaleDojo licence or terms are saved
anywhere (`private/scaledojo/INDEX.md` says "personal study copy"), and these lines are the lab's answers. Fix: save
ScaleDojo's terms. Until they allow it, keep the quotes of missions, hints and paid answers in the private excerpt
file and cite them by section in the Key, or make the repo private.

**D-M7 (major). Toolbox 2 carries too much, and its numbers clash with the step before.** It adds sliding window,
running summary, the bigger-window price fact and a 4-row, 5-column table of token counts (more than 3 new ideas,
INTEGRATED `:39`). Its running-summary figure, 1,800 tokens (`:78`), is larger than the 1,550-token history room of
the toy window taught one message earlier (`:48`), with no word that this is a different, larger window. A careful
reader will ask how a summary that does not fit can be the fix. Fix: split the price fact into its own short step,
or say "a real model's window, much larger than the toy". Or use 200-token messages so the summary row stays under
1,550.

### Minor

- **m1** eval step 1 (`:11-36`) is 2,411 characters (his best band tops out at 2,100, B8) with about five new
  ideas. It uses "ships" (`:13`), a word he flagged as jargon (C33). Replace it with "gives".
- **m2** Help: Label the batch 4 (`:838-863`) moves the dressing's honey line into the main list and drops "For the
  Dressing:" (51_31), yet move 6 says the dead end is "never reading the dressing". Keep the heading line.
- **m3** The Cold (`:949`) asks for his prediction in the same message as the items; SKILL `:45` says predict first.
- **m4** Help blocks for the batch reveal the answer to a scored item if they are sent mid-batch as stuck rung 3. Say
  they are sent only after the batch.
- **m5** The warm-up gate (`:352`) is counted by him and checked by the tutor; its result is not recorded anywhere.
- **m6** The dead ends in the worked examples are the tutor's own words; mark them as "our note", not the expert's.
- **m7** design-01 says "prerequisites: none" (`:8`), but Goal question 2 (`:30`) is a why-question that needs "you
  pay per token", which the unit does not state. Name llm-01/llm-02 as prerequisites or add the line.
- **m8** Guess the move 2 (`:195-199`) mixes "avg 5 messages/session" with "turn 20" after defining a turn as a
  message and its reply.
- **m9** The toolbox claim that the model "runs out of room partway through its answer and stops" (`:50`) is
  ScaleDojo's simplification. On current Anthropic and OpenAI APIs a request whose input plus reply cap exceeds the
  window is usually rejected, and replies stop mid-sentence when they hit the reply cap. The lab's own fix caps
  `max_tokens`. Add one honest line.
- **m10** The Decision note scores the TalkTherapy decision a second time, so the two scored answers rise or fall
  together.
- **m11** The engine's RETRY note (`engine.py:181`) says re-teach "the show steps he missed". The committed guard
  blocks re-sending them (tested), and SKILL `:42-44` says Help blocks only. Align all three.
- **m12** Cards are queued even when the unit is failed (`engine.py:372`); recall is self-graded (SKILL `:26-27`).
- **m13** `rung:` is never read (`engine.py:71-77`); rubric is not range-checked (`:337`).
- **m14** The glossary watchlist lacks trace, label, codebook, sliding window, system prompt, cue, DAU (F27, S10).
  Both units define them inline, so today this only weakens the checker.
- **m15** `check_unit.py:84` exempts every body line starting "Suppose" from number checks with no source or
  variation tag (C2). design-01's "Suppose" numbers are all backed by runs, but the checker would not catch one that
  is not.
- **m16** The guard still blocks any "?" in feedback before a step (B4) and fails closed on its own errors (B5).

---

## 4. Correctness, item by item

**Evaluation traces.** All 36 traces were read in full, including 47_31, 51_31, 57_24, 10_8, 10_9 and 47_8.
- Every Key label equals the source label, and every trace is HIGH confidence.
- Every quoted reason is word for word from the cited trace's reasoning. Checked: Worked 1 (38_22); Worked 2
  (59_18); pasta (46_3); warm-ups 43_9, 55_25, 27_40, 16_36, 46_19, 46_18; all 12 compare sentences; the Help
  quotes from 46_17, 55_32, 47_8, 10_8, 57_24 and 51_31.
- Every rule line equals the README (l.129-144), and the tiny examples are the README's own (l.117-126).
- Every label is right on the stated rule. No cut step or garnish hides a breaking line in any PASS trace. The cut
  lines that do break a rule are in traces that are already FAIL:
  - 46_19: "serve with a slice of whole grain bread";
  - 46_25: "cooked shrimp" tip;
  - 46_15: "feta cheese" tip;
  - 47_31: its optional cheese topping section.
- Details on the six traces read only in part before:
  - 47_31 is a clean FAIL: optional cheese under dairy-free, and the request's "cheese is okay" is a wish.
  - 51_31 is a clean FAIL: optional honey or maple syrup in the dressing under Whole30.
  - 57_24 is a clean PASS: optional feta under vegetarian.
  - 10_8 and 10_9 are clean PASSes: shrimp, cream, butter and Parmesan under pescatarian.
  - 47_8 is a clean PASS: nutritional yeast under dairy-free.
- Only presentation issue found: m2 (51_31 layout).

**Design quotes and numbers.**
- Every quotation matches the excerpt file and `scaledojo_levels_unlocked.json`: the QuickChat problem, users,
  data and both constraints; the TalkTherapy problem, data and both constraints; the level 1 hint; missions gen1_7
  (`summarize_after lte 20`, so "after 20 turns at most" is right) and gen0_3_7 (`lte 30`); the chapter's
  "too low wastes model calls ..." line; and the strong answer's opening.
- All numbers trace to runs: 1,550 (`design01-room`), 150 (`reply-left`), 6,000, 1,500 and 1,800 (`msg20-*`), 350
  (`start-ok`), 250 (`start-late`), 10,000 (`dau`), 70 (`bar`), 0.5 (`half`).
- The 1M-window price fact matches `facts.md:39-40` (Claude 4.6 and later).
- Keys are right except TalkTherapy (D-M1).

**Score lines.** All are markable. Eval batch: matches divided by 3, recorded as four steps whose mean is matches
divided by 12. Design: 1, 0.5 or 0 per step.

**Retry, Cold, cards.**
- Eval Retry (43_14 FAIL, 26_4 FAIL by the "X or Y" rule, 19_36 PASS, 29_7 PASS) and Cold (46_15 FAIL, 47_31 FAIL,
  16_19 PASS) are right and use only rules the unit teaches. Their size is the problem (E-M2).
- Design Retry and Cold are right. They are one item each (D-M3).
- All cards can be answered from shown text.

**Is the Retry and Cold size fair, and what to do.** No. At an 80% bar, 4 items need 4 of 4 and 3 items need 3 of
3, so a learner at 85% accuracy fails about half the time on luck alone. Proposed fix: 10 new items each, pass at 8
or more of 10 with at most one expert FAIL passed, drawn from person-checked items. Until that pool exists, report
Retry and Cold as trials and do not end mastery on them alone. For design, 3 items at a 0.7 mean.

---

## 5. Message by message, as he receives them

**eval-01.**
1. The job and the rule. Clear problem, rule, tiny example, picture, paths. About five new ideas, 2,411
   characters. "Vegan", "gluten" and "Parmesan" are unexplained, and "ships" is jargon. All four check questions
   can be answered from the text (about 90%).
2. Worked example 1. Clear; the question is easy.
3. Worked example 2. Clear; the question is easy.
4. Finish the expert's work. Needs "spaghetti is wheat, a grain", which has not been shown (E-M3). Expected first
   try about 65-75%, below the 80% aim.
5. to 10. Warm-ups 1 to 6. Each opens with the key's reason for the last one. Expected first try about 85%. Warm-up
   3 (raw vegan) needs "boiling is above 48°C", which is school knowledge. "Legumes" is defined just in time in
   warm-up 5.
11. Warm-up result. Counts and a prediction with the data in hand.
12. to 15. Blind batch. Items 5, 6, 11 and 12 rest on facts not shown (E-M3). Expected 10 to 11 of 12.
16. and 17. Compare. Counts first, then reasons; answerable.
18. Close. Answerable.

No sentence was found that he could not parse, apart from the undefined words above.

**design-01.**
1. Goal and the problem. Clear. Question 2 is a why-question that needs "pay per token" (m7).
2. Toolbox 1. Clear, worked arithmetic first. Four new ideas.
3. Toolbox 2. Too dense; the 1,800 figure clashes with the toy window (D-M7).
4. Worked example 1. Clear modelling; two-option checks.
5. Worked example 2. Clear. "summarize_after" is shown as the lab's name, which is fine.
6. Guess the move 1. Every term defined inline (DAU, session, power users, turn). About 85% first try.
7. Guess the move 2. Answerable by elimination (about 80%). The turn and message mix is noted in m8.
8. How the scored part works. Incomplete (D-M2).
9. TalkTherapy. The brief's first symptom misleads (D-M1). About 65-70% first try.
10. Short chats. A good non-obvious case (C35). It may be low first try (about 65-70%) after three summary answers
    in a row, which is intended.
11. and 12. Decision note and Close. Clear.

---

## 6. The guard, tested

Synthetic transcripts in an isolated copy, run on the committed guard and on the working-tree guard.
- Every step of both units, sent in order with short feedback before it: allowed.
- Help blocks mid-unit and after the close: allowed.
- Retry and Cold: allowed, including mid-unit (S-M1).
- Feedback with "?" or over 600 characters before a step: blocked.
- A full Key line quoted in feedback: blocked.
- An improvised stuck-order question ending with the ask marker: blocked (S-M2).
- The same question without the marker: not checked at all.
- Skipping from step 1 to the first scored step: **allowed** (S-M1).
- Re-sending a step after a Help block: blocked by the committed guard, allowed by the working tree (m11).
- `selftest.py` passed on the committed state before the working-tree edits.

---

## 7. Cohesion and licence, summary

- **Aligned.** INTEGRATED 2.3-2.5, SKILL.md steps 3-6, the committed checker's kinds and the engine's bars (80 and
  70) agree with each other and with both units' structure.
- **Out of step.** `evaluation.md` sections 1c, 3c, 4a, 5b, 5c and 6; `system-design.md` lines 43, 142, 179, 186,
  221, 229-244 and 270; INTEGRATED `:18-19` and `:79-81`; the glossary's TPR line (E-M5, D-M5).
- **HW3 material** is GPL v3 and the unit header carries the licence (fine).
- **ScaleDojo.** Used as short excerpts. Full texts stay private and git-ignored and have never been committed. The
  public repo does carry ScaleDojo lab answers and a paid-answer phrase with no terms on file (D-M6).
