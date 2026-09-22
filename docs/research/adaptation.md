# Adapting the teaching research to Faiz (after Lesson 6)

Written 2026-09-22 by the teaching-adapter. Inputs: docs/research/teaching-methods.md, the faiz-teach
skill, docs/learning-evidence.md, docs/glossary.md, projects/judge/script.md (L6). Trigger: C38.
Nothing here is a rule until it is applied to the skill. His stated rules (C rows) win over research.

## 1. What his evidence already shows

| Research finding | His evidence | Verdict |
|---|---|---|
| Worked examples first, for novices (strong) | Tiny example first: 80% (A12) vs real lines first 27% (A13); B1, B13 | Confirmed, strongly |
| Segmenting (moderate) | One part per message fixed A11 (0 answered) into A12 (80%); C25 | Confirmed |
| Load: one new thing at a time (strong) | ~8 new things: 0 answered twice (A11); 9-concept sweep 1/5 (B5) | Confirmed at the extreme |
| Why-questions need prior knowledge (moderate) | Cold why-questions 0/4 (B10) | Confirmed; keep the existing ban |
| Arithmetic questions are performance, not learning | Compute ~88% first try (B10); read-back complaint C36; "more analytical" C38 | Confirmed by his own words |
| Direction failures are a missing worked chain | E12 0/3 in L6 R2, none of the three parts showed a chain first; E11 0/2 then 2/2 once pointed at his own two numbers (D1) | Confirmed; the rule exists but was added after L6, so it is untested |
| Expertise reversal: full detail on new, nothing on known | "ik this dont repeat" (C22), "don't like repetition" (C27) | Confirmed |
| Pre-questions / a number he works out himself | Hooks 12/12 (B10) | Confirmed |
| Retrieval inside new work, changed surface | A given answer retained 1/3 when restated plainly (D7) | Consistent; supports "comes back reworded, in a new system" |
| Analogies help when mapped, with the break named (moderate) | Pictures 8/10 (D2); two failed pictures (stopwatch race, torn notebook) | Partly confirmed; the break line is untested. L6 R2-C's bathroom scale imported the wrong idea (instrument error, not sampling luck) |
| Predict, then reveal (moderate) | Refused as a guess at the L6 build (C37), then restored the same day on one condition: "if I'm given all the data I need to make my prediction there" (C39). L4's prediction (736 ms vs 1,753) was a guess because the effect on p95 was never given (B14) | **Confirmed, with his condition.** Predict only from numbers printed in the message (skill step 3 already says so). Aim a prediction at what surprised in L6: two picks interacting ($4.80 + $2.56 = $7.36, over $5) |
| Error-finding: ask for the mechanism, not a category (moderate) | Label-only broken-code questions 5/6; simulating broken code 0/4 (B11); L5 R2-B Q5 asking value plus label came back blank | **His evidence wins.** Keep Someone broke it label-only. Put the direction and mechanism into a separate question (pattern Q4 below) |
| "More context" vs seductive details | C34, C38 ask for more context; B8 shows long messages failed only with many questions | Compatible: add context the question needs (goal, mechanism, consequence), nothing else |

## 2. Proposed skill edits (.claude/skills/faiz-teach/SKILL.md)

Each replaces a line; none adds a second rule on a topic. All C rules are kept.

**E-1. Problem step (template 1).** Replace:
`1. **The problem.** 4-6 sentences with the full context, so he can reason about it (09-17, C34):`
`   who uses this and why it matters to them, how it works today, what changes, what goes wrong,`
`   why it goes wrong (the mechanism), and what it costs. Never a bare summary of the failure (B4).`
with:
`1. **The problem.** 4-6 sentences with the full context (C34, C38): who uses this and why, how it`
`   works today, what goes wrong, the mechanism in physical terms (what a case, a call or a row actually`
`   does), and what it costs. Turn every rate into counts once ("92% (55 of 60)"). No vague phrase that`
`   hides the mechanism ("happen to", "somehow", "naturally"). Never a bare summary of the failure (B4).`
Reason: L6 R2-C "which cases happen to land on the edge of passing changes run to run" hid the mechanism and mixed two sources of noise. Evidence: C38.

**E-2. Fix step (template 2).** Replace:
`2. **The fix:** one sentence, plain words.`
with:
`2. **The fix:** one sentence, plain words. When the new thing is a formula or a measure, follow the`
`   code with **How it works**: each piece of the formula in its own numbered line, what it does, on`
`   one case with real numbers, then what the result means in the problem's own terms.`
Reason: R2-C gave `2*sqrt(p(1-p)/n)` with no intuition; R2-B defined TPR and TNR in one line each. Research 2a, 2f. Evidence: C38, C20 ("explain and TEACH").

**E-3. Picture step (template 4).** Replace:
`4. **Picture:** one everyday picture (D2, B2).`
with:
`4. **Picture:** one everyday picture that runs on the same mechanism, plus one clause "Where it`
`   breaks:" when the mapping is not exact (D2, B2).`
Reason: research 2e (moderate). The L6 bathroom scale pictured instrument error, not sampling luck. Evidence: D2 failures (2 of 10).

**E-4. Worked chain before a direction question.** Replace:
`- A question asking for a saving or a difference, or which way a wrong number bends a decision, needs`
`  one worked chain of the same kind on other numbers earlier in the part (E11: 0/2, E12: 0/3 first try`
`  without it).`
with:
`- A question asking for a saving or a difference, or which way a wrong number bends a decision, needs`
`  a **Worked chain** of the same shape on another case earlier in the part, written as four links:`
`  wrong input → which way the measured number moves → which way the decision bends → what it costs.`
`  After he gets one right cold, the next lesson's chain leaves one link blank, then none is shown`
`  (E11: 0/2, E12: 0/3 first try without it).`
Reason: research section 1, "Fixing the direction weakness" (worked, faded, cold). Evidence: E11, E12, D1.

**E-5. Definitions of measures.** Replace:
`- Give each new word a plain one-sentence meaning the first time it appears (08-06, 09-05).`
with:
`- Give each new word a plain one-sentence meaning the first time it appears (08-06, 09-05). A new`
`  measure (a rate, a formula) also gets one counted case from the part's own numbers ("20 notes the`
`  person failed, the judge also failed 14: catch rate 14 / 20 = 70%").`
Reason: the TPR and TNR one-liners. Evidence: C38, C33.

**E-6. Question mix.** Replace:
`- Five short-answer questions: compute a business number, trace which lines run or what a sticker`
`  is on, classify (caught or crash, inside or after the loop), and exactly one **Someone broke it.**`
`  ending with the labels defined: "Crash (it stops), quietly wrong (runs, wrong result), or fine`
`  (runs, right result)?" (B10, B11, B11b).`
with:
`- Five short-answer questions: at most one warm-up compute; at least three from the question bank`
`  in docs/research/adaptation.md (each needs a chain of two links or more); and exactly one`
`  **Someone broke it.** asking for the label only, ending with the labels defined: "Crash (it stops),`
`  quietly wrong (runs, wrong result), or fine (runs, right result)?" (B10, B11, B11b, C36, C38).`
`  Tag each Key answer with its pattern, e.g. `[chain]`.`
Also delete from the C36 line the now-duplicate sentence `One warm-up compute is allowed.`
Reason: compute already ~88% (B10); C36 and C38 ask for questions that build understanding. Label-only kept because it is 5/6 and value-plus-label came back blank.

**E-7. Build givens and the prediction** (step 3 as re-edited for C39). Replace:
`   guessing (09-22, C39). Before scripting Decision 1, write and run the model the build uses and take`
`   every given from its output, so givens in different decisions cannot clash (L6 D3 vs D4).`
with:
`   guessing (09-22, C39). At least one prediction combines two of his picks (L6: $4.80 + $2.56 broke`
`   $5). Before scripting Decision 1, write and run the model the build uses and take every given from`
`   its output, so givens in different decisions cannot clash (L6 D3 vs D4). Every rate says where it`
`   came from in a few words (your labels, the model run, or "assumed:") and carries its wobble when`
`   it rests on fewer than 100 notes.`
Reason: 93% catch and 2% false alarm were stated with no reason, D3/D4 clashed (scan share), and the one L6 surprise was two picks interacting. Evidence: C31, C38, C39.

**E-8. Part size.** Replace:
`... A part is 2,600 characters or less (B8; raised for C34).`
with:
`... A part is 2,600 characters or less, or 3,200 when it carries a **How it works** block. Past that,`
`split it into two parts, each with its own questions (B8; C34, C38).`
Reason: the R2-C rewrite below with full context is 3,169 characters against 2,494 before. B8 shows 700-2,100 worked, 3,413 and up was rejected, and the long failures carried 16 questions; 3,200 stays under that line while holding 5 questions. A higher limit for every part is not justified: most parts do not introduce a formula. Build decisions stay at 2,000.

Glossary: add to Taught when L6 reflect runs, if not already: `catch rate`, `clear rate`, `wobble`, `true rate` (the rate on every case the firm will ever see). Add `TPR, TNR, sample, true rate` to the watchlist.

## 3. Question bank patterns

Each pattern needs a chain of at least two links. Use at least three per part (E-6).

**Q1. The direction chain** (trains E12). *Template:* "X is off in this direction [concrete cause]. Which way does [measured number] move, which way does [decision] bend, and what reaches [customer]?" *Example:* "The judge was checked only on notes the summariser wrote for Acme, whose invoices are all typed. On the firm's real mix, a third scans, does its catch rate read high or low, and which way does that bend the release gate?" (high; toward shipping; bad scan notes reach suppliers). *When:* only after a Worked chain of the same shape in the same part (E-4); faded next lesson.

**Q2. What does this number prove.** *Template:* "[System] reports [number]. Does that show A or only the weaker B? Name what else you would need to see A." Two options, since two-option questions recover him 5/7 (D4). *Example:* "The judge marks 300 of 320 notes PASS. Does that show the summariser is right 94% of the time, or only that the judge says so? What single measurement turns it into the first?" (only the judge; its catch and clear rates against a person). *When:* the part introduces any measured number. Also trains E12's second half.

**Q3. Flip point.** *Template:* "At what value of [input] does the decision change? Show the break-even." *Example:* "Labelling costs $2 a case. What is the smallest set that makes a 4-point rise at 90% believable, and what does it cost?" (225 cases, $450). *When:* any part with a threshold or a trade-off. Uses his arithmetic strength inside a decision rather than as the goal.

**Q4. Contrasting pair.** *Template:* "Two setups differ only in [one thing]. Which one's result can you trust (or costs more), and what one number decides it?" *Example:* "Team A goes 88% to 92% on 60 cases; team B the same on 1,000. Which can call it real?" (B; wobble 2 vs 8). *When:* right after the mechanism is shown; research 1c (moderate to strong). The best single upgrade for a classify question.

**Q5. Before minus after** (trains E11). *Template:* "Proposal 1 does X, proposal 2 does Y. Which saves more per week? Give before, after, and the gap for each." Asking for all three numbers makes the one-sided answer impossible. *Example:* "Fixing missing_total removes 131 of 320 weekly failures; fixing wrong_currency and truncated_page_2 together removes 18% and 9% of 320. Which fix leaves fewer failures, and by how many?" (missing_total: 189 left vs about 234; 45 fewer). *When:* any saving, difference or gain.

**Q6. Quietly wrong: which way and who notices** (trains E1, kept apart from Someone broke it). *Template:* "[A change] runs without error. Is the number it reports too high or too low, and who is the first person to notice, how?" *Example:* "The JOIN now reads an invoices table loaded twice. Is the money at risk too high or too low, and who notices first?" (double; the finance director, when the at-risk total beats the week's invoiced total). *When:* in the same part as, but a different question from, the label-only Someone broke it.

**Q7. Find the wrong step.** *Template:* "A colleague reasoned: 1) ... 2) ... 3) ... Which step is wrong, and what is the right conclusion?" (research 1e; only after one correct example). *Example:* "1) Catch rate is 70%. 2) So 70% of the judge's FAILs are real failures. 3) So the fail count is 30% too high." (step 2: catch rate is about the person's FAIL pile, not the judge's; the count reads low, not high). *When:* when a common wrong belief exists; also a refutation (2g).

**Q8. What would have to be true.** *Template:* "For [the losing option] to be the right pick, what would [given] have to be?" *Example:* "For random labelling (L6 D1 option B) to beat 200 random plus 200 complaints, what would have to be true about the complaints?" (they miss a failure kind). *When:* build debriefs and the last question of Round 2; research grade weak, use for the causal chain it forces.

## 4. Explanation pattern

**Checklist** (every new idea; each item one to three sentences):
1. Goal in money or risk: what decision uses this, what goes wrong without it.
2. Every rate also as counts from the story (88% = 53 of 60; the rise = 2 cases).
3. The mechanism in physical terms: what a case, row or call does. No "happen to", "somehow", "naturally".
4. One source of trouble per part. If two causes exist (sampling luck and an AI that answers differently each run), teach one and say the other comes later.
5. A formula gets **How it works**: each piece on its own line, with a number, and what the result means in the story.
6. The picture runs on the same mechanism, with "Where it breaks" when the mapping is loose.
7. Every given in a build states its source, or is named as an assumption.
8. Any question on direction or saving has a worked chain of the same shape above it.
9. Every term defined in the sentence it first appears; a new measure gets one counted case.

**Before** (L6 R2-C as sent, 2,494 characters). Problems:
- "which cases happen to land on the edge of passing changes run to run" names no mechanism, and mixes two different sources of noise (the AI answering differently each run, and which 60 cases were picked). The formula only measures the second.
- The formula `2 * sqrt(p * (1 - p) / n)` arrives with no reason for `p(1-p)`, the square root, or the 2.
- The rise is never turned into counts (4 points on 60 cases is 2 cases).
- The bathroom scale pictures a faulty instrument, not luck in which cases were picked.
- The third path bullet ("count only the cases that flipped") is a second new idea in one line.
- Q4 (best of five, E12) had no worked chain above it: missed first try.
- Q1 and Q2 asked him to rerun the given line and read back "8 points" from Q2's own text.

**After** (passes scripts/check_lesson_script.py at a 3,200 limit; 3,169 characters):

````markdown
# Lesson 6 · Round 2 · Part C · Telling a real gain from luck

**The problem.** Before each change to the summariser, the team runs the checked judge on the 60 test cases from Lesson 5. Last Tuesday the pass rate read 88% (53 of 60); someone reworded the instructions and the next run read 92% (55 of 60), and the release note called it a success. That rise is 2 cases. The 60 cases stand in for the thousands of invoices the firm will send next month, and a different 60, fairly picked, would score a few cases higher or lower with nothing changed. If luck alone can move the rate more than 4 points on 60 cases, the note is reporting luck, and a team that ships on luck will one day ship a change that made the notes worse.

**The fix:** work out how far a rate measured on this many cases can sit from the true rate (the rate on every invoice the firm will send) by luck alone. That distance is the wobble. Believe a rise only if it is bigger.

```python
from math import sqrt
n, p = 60, 0.88        # cases in the set, rate measured on them
wobble = 2 * sqrt(p * (1 - p) / n)
print(wobble)          # 0.084, about 8 points
```

**How it works**, from the inside out:
1. `p * (1 - p)` is how unsure one case is: 0.5 x 0.5 = 0.25 for a case that passes half the time, 0.9 x 0.1 = 0.09 at 90%, and 0 at 100%, where nothing can move.
2. `/ n` then `sqrt`: more cases shrink the wobble, but only by the square root, because lucky and unlucky cases cancel partly, not fully. 4 times the cases, half the wobble.
3. `2 *` widens it to cover about 19 of every 20 fair samples.
So 88% on 60 cases means the true rate sits somewhere from about 80% to 96%.

**Picture:** tossing a coin. In 10 tosses the share of heads often lands anywhere from 30% to 70%; in 100 tosses, 40% to 60%; in 1,000, 47% to 53%. 100 times the tosses buys only 10 times the steadiness. Where it breaks: a coin is 50/50, your cases pass about 90%, so they wobble less (step 1).

**Worked chain** (a wrong number bending a decision, on another case): the team drops the 10 hardest cases because "they always fail" → the measured rate reads high → every version clears the release bar more easily → a version that got worse on hard invoices ships.

- **Rise bigger than the wobble:** the true rate very likely moved; the note can say improved.
- **Rise smaller than the wobble:** it may be luck; the note says undecided.

**Your turn.**

1. A set of 400 cases scores 90%. What is its wobble, in points?
2. Team A goes 88% to 92% on 60 cases; team B goes 88% to 92% on 1,000. Which team can call it a real gain? Give the wobble that decides each.
3. The team wants to trust a 4-point rise at a rate near 90%, and labelling a case costs $2. What is the smallest set that does it, and what does it cost?
4. A release needs a reported rise, so the engineer scores the new version on five different random sets of 60 and reports the best. Which way does the reported rate move, which way does the release decision bend, and what reaches the firm?
5. **Someone broke it.** For the 60-case set, someone typed `n, p = 600, 0.88`. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 3 points (2 x sqrt(0.09 / 400) = 0.03)
2. team B (wobble about 2, and 4 is bigger); team A is undecided (wobble about 8)
3. 225 cases (2 x sqrt(0.09 / 225) = 0.04), $450
4. reads high (the luckiest of five) → bends toward shipping → changes that did nothing ship, and sooner or later one that hurt
5. quietly wrong (it prints about 2.7 points, so the 4-point rise looks real and luck ships)
Relies on: the wobble formula and its three steps; a rise inside the wobble proves nothing; worked chain shape (wrong input, reading, decision, cost)
````

What changed and why: the rise is shown as counts (checklist 2); the noise source is one, named physically (3, 4); the formula is built line by line (5); the coin picture runs on the same mechanism and names its break (6); Q4 now has a worked chain above it (8); questions 2, 3 and 4 use bank patterns Q4 (pair), Q3 (flip) and Q1 (direction chain), plus one warm-up and a label-only Someone broke it. Flip counting on the same cases (the exact method for a before-and-after on one set) is dropped here as a second new idea; teach it as its own part in L7 if the gate lesson needs it.

## 5. Checker changes (scripts/check_lesson_script.py)

1. **Size:** `limit = 2000 if BUILD else (3200 if "**How it works" in body else 2600)`.
2. **Formula needs How it works:** if a code block contains `sqrt(`, `**`, or two or more of `* / + -` between names, and the body has no `**How it works`, fail.
3. **Direction question needs a worked chain:** if any question matches `(?i)which way|reads (high|low)|bend|too (high|low)|what does .* prove`, the text before `**Your turn.**` must contain `**Worked chain`, else fail (E-4).
4. **Question mix:** require a `[tag]` on each Key answer from {warmup, chain, prove, flip, pair, gap, which-way, wrong-step, must-be-true, broke}; fail if more than one `warmup`, fewer than three bank tags, or `broke` count is not 1 (E-6).
5. **Vague phrases:** fail on `happen(s)? to`, `somehow`, `naturally`, `and so on`, `etc`, `various` in the problem or How it works text (E-1).
6. **Rates as counts:** warn when the problem cites a percentage with no `(N of M)` anywhere in it (E-1, warning only; some rates have no whole).
7. **Build givens trace to the model:** BUILD-D1 carries a `Model: projects/<lesson>/<file>` line; for every BUILD-D part, each percent and dollar figure in the `Givens:` sentence must appear in that file's saved output or be preceded by `assumed:` (E-7). This mechanically blocks the D3/D4 clash.
8. **Picture break:** not enforceable reliably; leave to the checklist.
9. **Harder decisions** (section 6): in a BUILD-D part, fail if no `Unknown:` or `unknown` appears in the situation, if no option's Effect or Cost names a second condition (a regex on `in a .* month|at quarter end|if .* rises|later`), or if the Key lacks both "gives up" and an "If ..." sentence naming the given that would change the pick.
10. **Call interaction:** in BUILD-CALL, fail if no question names two decision numbers ("Decisions 2 and 3").

## 6. Harder, realistic build decisions (C39)

His words: "The decisions need to be harder, more like actual engineering decisions and more realistic." The L6 decisions already met C35 (each option loses somewhere), yet each had one clean answer once the target was read, because every given was certain, the target named every constraint, and nothing changed over time. Real decisions are hard for other reasons:

1. **Uncertain data.** A key rate rests on few cases, so it is a range, not a number. Sometimes the range straddles the target (then measuring more first is the right move); sometimes it does not (then it is safe to decide now). He already has the wobble to tell which.
2. **Conflicting constraints from other people.** Finance caps the bill; an operations user wants something the target does not mention. The target is one team's view; the pick decides whose need loses.
3. **Second-order effects.** A choice that works today gets worse when something else moves (scan share, volume, prices). The option's number must be shown under both conditions.
4. **Correlated failure.** Checking a system with a copy of itself shares its blind spots (the cheap judge misses what the cheap summariser misreads).
5. **Reversibility and costs that show later.** Some choices are cheap to undo, some break history (switching the judge breaks the weekly trend line).
6. **Interaction across decisions.** A pick multiplies an earlier one (two calls per note from Decision 2 doubles every price in Decision 3).
7. **Choosing what to measure first.** Sometimes the best option is "spend $X to shrink the unknown before deciding".

**Checklist for every decision message** (replaces nothing in C31, C35; tightens both):
- [ ] At least two of the seven sources above are live in this decision, and the Key names which.
- [ ] Every given has a source (labels, model run, or "assumed:"), and a rate on under 100 cases carries its range.
- [ ] One constraint comes from a named person or team, and at least one option breaks it.
- [ ] At least one option's Effect or Cost is shown under a second condition (bad month, growth, later).
- [ ] The earlier pick this decision depends on is stated ("Decision 2 makes two calls per note").
- [ ] The Key says what the winner gives up and which single given, if it flipped, changes the pick (C35).
- [ ] Everything still fits 2,000 characters. If a fourth option (such as "measure first") is needed, it gets its own decision message rather than a bigger one.

**Proposed skill edit E-9.** Replace:
`   Every decision must be a real trade-off ("decisions cannot be this obvious", 09-18, C35): no`
`   option may rule out nothing, each option must win on some dimension the others lose, and the`
`   sound pick must depend on a stated given, so changing that given would change the answer. The`
`   `### Key` names what the winning option gives up.`
with:
`   Every decision must be a real trade-off that feels like engineering (C35, C39): no option may rule`
`   out nothing, each option must win on some dimension the others lose, and at least two of these are`
`   live: an uncertain given shown as a range, a constraint from another person or team, an effect`
`   shown under a second condition (bad month, growth), shared blind spots, a choice that is hard to`
`   undo, a dependence on an earlier pick, or the option to measure first. The `### Key` names what the`
`   winning option gives up and the one given that, if it changed, would change the pick.`

**Keep the 2,000-character limit.** The rewrite below carries five of the seven sources in 1,993 characters. B8 puts his comfortable range at 700 to 2,100 characters; a decision has no questions to lighten it, so there is no evidence for more. If a decision needs more, split it.

**Before: L6 BUILD-D3 as sent** (1,629 characters). Problems:
- Every given is certain: the cheap AI's 50% on scans is stated as fact, though it rests on about 72 bad scans (range 38% to 62%).
- The only constraint is the target, so B-versus-C is settled by reading the $5 line.
- Nothing changes over time, so the month-end scan rise (which then clashed with D4) is invisible here.
- 93% has no source.
- Option C (strong AI on 800 random) is presented as clearly best; he still merged it with the cheap AI and broke $5 ($7.36), which the decision never showed as a possibility.

**After** (passes the checker, 1,993 characters; numbers recomputed: catch 2/3 x 93% + 1/3 x 50% = 79%; top of range 83%; 1-in-3 month 0.4 x 93% + 0.6 x 50% = 67%; option C $6.17 and $10.13; 800 notes x 8% / 40 suppliers = 1.6 bad each):

````markdown

# Lesson 6 · The build · Decision 3 of 4

**Decision 3: which AI judges, and on which notes.** Givens (model run and your labels): 4,000 notes a week, 1 in 7 a scan; Decision 2 makes two calls per note. Cheap AI $0.0004 a call, strong AI $0.003. On your 216 bad labelled notes the strong AI caught 93% (wobble about 3 points). The cheap AI, which also writes the notes, caught 93% of bad typed notes but only 50% of the 72 bad scans (with its wobble, anywhere from 38% to 62%). Finance caps judging at $5 a week; the director wants a per-supplier failure count every Friday for 40 suppliers. Unknown: whether scans stay 1 in 7 (last quarter end, 1 in 3). Switching AI later breaks the weekly trend: rates before and after cannot be compared.

**Option A, cheap AI on all 4,000.**
- **What happens:** 8,000 cheap calls; every note marked, every supplier counted.
- **Effect on the target:** a third of bad notes are scans, so catch is about 79%, and at most 83% even at the top of the scan range. In a 1-in-3 month scans are 60% of bad notes and catch falls to about 67%. Its misses are the summariser's own misses.
- **Cost:** $3.20 at any scan share.
- **Rules out:** the 85% catch rate.

**Option B, strong AI on 800 random notes.**
- **What happens:** 1,600 strong calls; 3,200 notes never marked.
- **Effect on the target:** catch about 93% on both kinds; the weekly rate wobbles about 2 points. 800 notes over 40 suppliers is 20 each, under 2 bad on average, so Friday counts of 0, 1 or 2 rank suppliers by luck.
- **Cost:** $4.80, whatever the mix.
- **Rules out:** the director's per-supplier list.

**Option C, cheap AI on typed notes, strong AI on scans.**
- **What happens:** every note marked; scans go to the strong AI by file type.
- **Effect on the target:** catch about 93% on both kinds, full Friday list.
- **Cost:** $6.17 a week at 1 in 7; $10.13 in a 1-in-3 month.
- **Rules out:** the $5 cap, and a bill finance can plan, since it moves with the scan share.

**Your pick.**

### Key
B, because the target caps judging at $5 and asks for the rate, not a per-supplier list. It gives up the Friday list: the director uses the complaints table from Round 1. If the list were part of the job, C with a raised budget; A would win only if 79% were acceptable. No extra measuring needed first: even the top of A's scan range stays under 85%.
````

What changed: the scan rate is a range and the Key says why that range does not justify measuring first (source 1, 7); finance and the director pull in different directions (2); A and C are shown in a 1-in-3 month (3); A's shared blind spot is named (4); switching AI later breaks the trend (5); Decision 2's two calls are carried in (6). The hybrid he invented in L6 is now option C, with its real bill shown.
