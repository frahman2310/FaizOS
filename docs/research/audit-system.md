# Audit of the v2 learning machinery against its specification

Written 2026-09-24. An independent, adversarial check of `learn/engine.py`, `learn/check_unit.py`,
`learn/demo.py`, `hooks/teaching-guard.py`, `hooks/session-start.sh`, `scripts/check_teaching_system.py` and
`.claude/skills/faiz-teach/SKILL.md` against `docs/research/structures/INTEGRATED.md` (wins on conflict),
`review.md`, the five structure files, `recommended-method.md`, `postmortem.md`, `curricula/{method-effectiveness,
ai-tutoring,curriculum-design}.md` and `docs/learning-evidence.md` (C1 to C46). Nothing was fixed.

**Resolution (2026-09-24, same day):** the engine, checker and guard were rebuilt against these findings.
`learn/selftest.py` plants each attack (invented numbers, loose quotes, missing Score/Cold/cards, code not in
a program, repeated or out-of-order steps, Key leaks, improvised or pre-step questions, retries under
`stop_hook_active`, failing units) and exits 1 if any gets through; `scripts/check_teaching_system.py` runs it
at every session start, and a crash of that gate is now printed. Result: 33 of 33 caught. Added after the
audit: the engine refuses to serve or record a unit that fails the checker; number and code cards need a
second surface (INTEGRATED 2.1).


All tests ran on a copy of `learn/` in the session scratchpad (real `learn/data` untouched; it does not exist
yet), using the project venv with `uv run --no-sync`, with `engine.dt` monkeypatched to move the date.
Start date used: 2026-09-28 (Monday). `fsrs` is 6.3.2. The current tree passes its own gate
(`check_teaching_system.py`: 63 of 63), so every finding below slips past the existing checks.

Severity: **blocker** = the system would produce a wrong mastery signal or let unchecked teaching through in
normal use, before week 2; **major** = a spec item missing or implemented against the spec or the research;
**minor** = robustness or wording.

## Findings

| # | Component | Severity | Problem | Evidence or reproduction | Fix |
|---|---|---|---|---|---|
| 1 | SKILL.md step 5 + engine `BAR` | **blocker** | One scoring rule for all five skills ("share of steps answered right first time") replaces the skill bars of INTEGRATED 3. Code's bar is 90% of *trace cells* plus tests within 2 attempts; LLM's is right answer *and* right reason on 2 cases; production 9 of 10 on a mixed set; evaluation kappa 0.70 pooled over 24+ traces with no missed failure; design 70/100 rubric with every brief number met. With 6 to 8 steps, step-percent can only be 0, 17, 33, 50, 67, 83, 100 (code, production) or 0, 12.5, ... 87.5, 100 (LLM, design), so the 90 bar means "every step perfect", including "Odd result" (Key: "any honest observation") and "Close", which have no right answer. Evaluation's 70 would be passed at 5 of 6 steps with no kappa computed at all. The mastery, dashboard and change rule all run on this number. | SKILL.md lines 34-35; engine.py line 24; spec INTEGRATED 3, review 4 ("a rubric with partial credit and kappa are not percentages"). llm-02 Key for Odd result: "Any honest observation." | Score each skill by its own bar, recorded as its own unit (cells, kappa, rubric points, items of 10); say in each unit which steps are scored and how; exclude unscored steps (Odd result, Close) from the score. |
| 2 | Cold check (SKILL.md step 6, engine `today`/`done --cold`) | **blocker** | The 7-day cold check, which feeds mastery, the dashboard's cold column, the early warning and the 8-week change rule, has no working material or guard. (a) It re-asks "that unit's cards", which have been in the recall queue since the unit (due the same day, see 6), so they are neither cold nor new: the spec's recognition trap. (b) The "one new problem" has no file, no format, no checker coverage; none exists (`grep -ri cold learn/units` is empty) and the first one is due 2026-10-06. (c) It is listed only on the exact date: missed by a day, it never appears again. (d) `done --cold` is accepted on any day, for any unit, even one never done, so the gate is honour-based. | Test t3: cold for code-01 shown on 10-06, gone on 10-07; `done llm-01 90 --cold` on the session day made llm "mastered"; `done llm-04 100 --cold` for a never-done unit recorded. | Add a `## Cold` section per unit (new numbers or new code, checked by check_unit like steps); list overdue cold checks until done; reject `--cold` before `cold_due` or without a session; score the cold item only, not the cards. |
| 3 | teaching-guard.py | **blocker** | The guard does not enforce what the rulebook and ai-tutoring 4g (Harvard: "the platform enforced the sequence") say it does. It only checks that *some* passing step body is a substring of the reply. Bypasses, each reproduced against a copy of the guard pointed at a copy of the repo: | Results: step + improvised question after it: **pass**; improvised text before a step: **pass**; two steps in one message: **pass**; step with its `### Key` pasted after it: **pass**; step 7 sent first (no order or session state): **pass**; improvised question ending `Your answer.` (not bold) or `**Your answer:**`: **pass** (unguarded); step from a unit whose header crashes the checker (`level: one` raises ValueError, the top-level `except: pass` fails open): **pass**; any message on the second Stop (`stop_hook_active`): **pass**. Correctly blocked: one word changed, a failing unit's step, an improvised question ending exactly `**Your answer.**`. Also, a Stop hook runs after the text is already shown, so "block" can only ask for a correction, never stop the send. | Require the reply to equal exactly one step (normalised), the next one in order for the scheduled unit (keep a small session cursor in `learn/data`); forbid Key text in replies; block on any `answer`-like ask marker variant; fail closed on checker exceptions for unit steps; state in the rulebook that the hook corrects after sending. |
| 4 | engine mastery (`cmd_dashboard`) | major | Mastery rule only half built. No rungs or levels (units carry `level:` but the engine ignores it); no "up one rung after 2 at the bar"; no floor (bar minus 20) and no "down one rung after 2 below"; no confident-wrong rule (confidence is not recorded, see 18). "2 sessions in a row" counts the same unit recorded twice on one day; the cold score used is the latest cold of *any* unit in the skill, not of the units in the streak; the status flips back as soon as a later session falls. | Test t2/t3: code-01 recorded at 83 then 100 on the same day counts as two sessions; code "mastered" after cold 95 on code-02, then "bar 90" after a 40 on code-03 with the old cold still shown. | Store rung per skill in state; apply up/down on each session; mastery = 2 consecutive at bar for distinct units + cold of those units at bar after >= 7 days. |
| 5 | engine `next_unit` | major | A unit below the bar is re-served unchanged (same code, same numbers) at the next slot, e.g. Tuesday's failed code unit returns on Thursday. That tests recognition, repeats items (C22, C27) and has no down-rung path. A failed cold check changes nothing: the unit stays "done". | Test t3: code-03 at 40 on Tue 10-13 is the unit again on Thu 10-15. | On a miss, serve a parallel unit (same skill, new surface) or drop a rung; on a failed cold check, re-queue the skill point. |
| 6 | engine `cmd_done` (cards) | major | New cards are created with `Card()` whose due time is now, so a unit's cards are due in the same session he learned them. review.md 5a (from C22, C27): "first card return is next day, never in the same unit"; llm-behaviour.md: "first return the next day". | Test t2: right after `done code-01`, `due` lists all 5 code-01 cards and 4 llm-01 cards. | Set the new card's due to the next day on entry. |
| 7 | engine `due_cards` | major | Recall is not interleaved. Cards are ordered by due timestamp, and cards of one unit are created together, so they come back as a block per unit and per skill. Spec: "mixed across all five skills"; interleaving d = 0.79 to 0.83 (recommended-method 1, method-effectiveness row 9). | Test t2: due list is code-01.1 to .5 then llm-01.1 to .4, three weeks later too. | Round-robin across skills and units within the due set. |
| 8 | engine queue + unit Cards | major | "Number and code items always come back with new numbers or new code, never the same surface" (INTEGRATED 2.1) is not implemented: cards are fixed Q/A strings, including code cards (code-01.1 to .5 quote fixed code). | queue.json after `done code-01`. | Allow card variants (`- Q1/Q2/...`) or a generator per number/code card; serve a different variant each review. |
| 9 | engine recall slot | major | "About 10 minutes" is only printed. No cap, no overflow rule; the due list grows without limit. llm-behaviour.md's own cap rule (stop adding new cards for 3 days if the cap is hit twice a week) is also missing. | Test t3: "Recall queue: 25 due (about 10 minutes)" by week 3 with only 5 units done. | Cap served cards per day (count or time), carry the rest; pause new cards on repeated overflow. |
| 10 | SKILL.md step 4 + dashboard gap | major | The prediction is asked "before the last step", after he has answered most steps and seen feedback, so it is a postdiction and the calibration gap is flattered. Spec 2.2: "Before every check he predicts his score". The gap is also computed as an absolute value over the last 4 records (session and cold mixed), not "after 4 weeks", and loses direction (over- or under-confidence). | SKILL.md line 33; engine.py line 157. | Ask for the prediction before the first scored step (and before each cold check); keep the signed gap; report it over a time window. |
| 11 | engine dashboard | major | Only the three numbers exist; none of INTEGRATED 7's judgements: cold 10+ points below session (alarm), gap above 20 (alarm), the early warning (high in-session with low cold), outside tasks. "Main score" is simply the last session. | Code: engine.py 150-163. | Compute and show the two alarms and the early-warning flag; add a row kind for outside tasks. |
| 12 | engine week plan (`WEEK`, `cmd_today`) | major | The plan lists units only. Missing: evaluation rapid rounds (Mon, Thu, Sun), design drill (Fri, Sun), the Saturday whole-task rotation (eval analysis / ScaleDojo lab / production mock / code steer). The "Saturday whole task" line is dead code: it prints only when no unit is scheduled, but design is on Saturday from week 6. Placement checks (evaluation week 4, production per review 7a) are missing. Design runs Wed and Sat from week 6 with no "guess the architect's move" variant, though the full design session is weeks 7-8. | Test t1, weeks 1-10: Saturday is `design` from week 6 and `-` before; no week ever shows the Saturday task. | Add non-unit sessions to the plan with an A-D rotation by week number; add placement entries at each skill's start week. |
| 13 | check_unit numbers | major | Everything inside code fences and inline backticks is exempt from the number check, and code shown in a step is never compared with the program in `code/<unit>/` that produced the run. For code units, the code and printed outputs are the content, so an invented output passes. | `bad/B_codeblock.md` (`total_cost = 4821` in a fence) and `bad/C_inlinecode.md` (`` `4821` ``): both PASS. code-04 lists `code: code/code-04/...` but nothing checks it. | Check each fenced block against the listed program file (exact match or a named excerpt); check numbers in output blocks against the runs. |
| 14 | check_unit numbers | major | Easy launders: (a) a line containing `given:` anywhere (case-insensitive, even "not given: anywhere") is skipped entirely; (b) any line with a `"` accepts any number that appears anywhere in the long listed sources (transcript timestamps included): 72 of 89 two-digit numbers pass for code-01, 58 of 89 for llm-02; (c) 0-9, 10 and 2000-2099 are always allowed ("7 of 10 right" passes); (d) spelled-out numbers ("forty-two percent") pass. | `bad/E_given.md`, `bad/E2_given_inline.md`, `bad/U_quote83.md` (`He said "yes": the model is right 83% of the time`), `bad/G_smallnums.md`, `bad/H_words.md`: all PASS. | `given:` only at line start and only for values the Key marks as scenario inputs; require the quoted number to sit inside the quotation marks and match a source sentence; drop the free-number whitelist except list markers; flag number words. |
| 15 | check_unit Cards and Keys | major | Cards go straight into the recall queue but are unchecked: numbers in answers are not traced, and a `## Cards` section with no parseable `- Q: ... \| A: ...` line passes (zero cards enter the queue silently). Keys are not checked for numbers either, and a Key of "TBD" passes, yet the tutor marks from the Key. | `bad/N2_cardnums.md` (card answer "exactly 4821"), `bad/N_cards.md` (no valid card), `bad/L2_keyTBD.md`: all PASS. | Run the number check on Keys and cards; require at least one parsed card and a Key per step that names the scoring rule. |
| 16 | check_unit jargon | major | The jargon check accepts any sentence containing "is", "are" or "(" as an explanation; the watchlist has no kappa, tokenizer, temperature, p50, median, FSRS, sampling; the check silently turns off if `check_lesson_script` cannot be imported. kappa is the evaluation bar (INTEGRATED 3: "taught before it is used"; E7). | `bad/M2_jargon_is.md` ("The pipeline is slow and latency is high.") PASS; the same words without "is" FAIL. | Require the explaining clause to follow the term; add every spec term to the watchlist; fail if the import fails. |
| 17 | runs/ provenance (demo.py, record.py, check_unit) | major | Any JSON placed in `runs/` is trusted as measured. `runs/llm02-cost-by-language.json` (the $1,500 and $2,700 figures in llm-02) is `"kind": "check", "computed_by": "python3"` with no program or command: not produced by demo.py or record.py. demo.py's own file names (`YYYYmmdd-...-kind.json`) do not match any run a unit cites, so the cited runs were renamed by hand. INTEGRATED 2.8: "every number produced by running code". | File contents; demo.py `save()`. | Runs must carry the command that made them; a small verifier re-runs offline runs (code/, arithmetic checks) and fails on mismatch. |
| 18 | engine + units: confidence | major | Confidence (1 to 5, or sure/unsure) is asked in LLM steps but never recorded, so the floor's "confident wrong answer" rule (INTEGRATED 2.5) and review 7d's "sure/unsure per item in eval and LLM" cannot run. | `done` has no confidence field. | Record per-step correctness and confidence with `done`, derive the confident-wrong flag. |
| 19 | SKILL.md: the part template | major | INTEGRATED 2.8: "the part template where a step explains something". The rulebook never mentions it and check_unit does not check it. His record: 80% with the template vs 27% without (A12, A13; review 5a). The v1 checks for C34 (context of 4+ sentences) and C36 (no read-back questions) were dropped too. | SKILL.md has no template section; check_unit has no such rule. | Define which steps "explain" (for example Wrong idea fixed, the Key's given answer) and check them for the template parts. |
| 20 | Other teaching surfaces | major | Teaching instructions still live outside the rulebook and contradict it; `check_teaching_system.py` only greps for old phrases, so it misses all of them. `faiz-drill`: a second FSRS queue (`faizos_review_queue`) and drills "to be typed as real code" (against "one queue" and C24 "I will never need to write code"). `faiz-hint`: a 4-rung hint ladder (assertion, region, rule, line) that is not the stuck order, plus "teach the language grammar in every lesson file" (C17, C29). `faiz-learn`: "Apply its insights", its own term and reveal rules, and "each lesson ends in a build ... (faiz-teach skill)", which v2 removed. ai-tutoring 4g guard 1: "one source of teaching rules". | `.claude/commands/faiz-drill.md`, `faiz-hint.md`, `faiz-learn.md`, `faiz-build.md`. | Retire or redirect these commands to the v2 flow; add a check that no command defines recall, hints or teaching rules. |
| 21 | SKILL.md Feedback | major | "Give the answer when he asks" is missing. C19, C23, C28 and the ledger's resolved conflict 3 ("when he asks, or after the second failed hint, give it with the reason"); ai-tutoring 4b.2 says the same. The rulebook's path is: wrong, one reframe, one hint, then a 4-move stuck order, so the answer arrives after 5 moves. "ik this / move on" is covered, "give me the answer" is not. | SKILL.md lines 43-46; learning-evidence.md line 120. | Add: on request, or after the second failed hint, give the answer with a one-line reason, then his one-line explain-back. |
| 22 | SKILL.md vs his standing rules | major | Rules the evidence file marks "standing; in faiz-teach 'The build'" or "Investigation mode" (C30, C31, C32, C35, C39, C41, C42) point to sections v2 deleted. They are neither kept nor marked superseded, so the "his latest words win" line has nothing to apply. | learning-evidence.md lines 99-111; SKILL.md has no Build or Investigation section. | Mark each as superseded by INTEGRATED (with the reason) or restate it in v2 terms (design "Choices" step, staged whole tasks). |
| 23 | SKILL.md change rule | major | Two change rules collide. "A rule he states: ... change this file in the same turn" and "his latest words win" vs "Method changes (step order, formats, bars): none for 8 weeks" (INTEGRATED 2.9). If in week 3 he asks for a format change, the file supports both answers. | SKILL.md lines 11, 61-64. | Say which wins: his stated rule changes delivery at once; format, step order and bar changes wait for week 8 and are logged as pending. |
| 24 | SKILL.md scoring details | major | Undefined cases a tutor will meet in the first session: how skipped steps (the Key's skip rule, "move on") are scored; whether a right answer after one hint counts; how the cold score is computed (cards plus one problem, with what weights). Each changes the mastery number. | SKILL.md lines 31-39; llm-02 Key: "skip to New case". | Define: skipped by the skip rule = right; after a hint = wrong; cold score = the cold item's own bar. |
| 25 | engine CLI robustness | minor | Tracebacks on a mistyped id: `review nope 3` gives KeyError, `done nope ...` gives StopIteration. No range check: `done code-02 250 --predicted -40` is recorded. Missing `skill:` header crashes `cards_of`. | Test t2. | Validate ids and 0-100 ranges with a clear message. |
| 26 | engine cold listing | minor | Recording a unit twice creates two cold checks for the same unit and date. | Test t2: two `cold_due` 2026-10-06 entries for code-01. | Keep one cold check per unit, from the latest session. |
| 27 | engine week number | minor | Before the start date `today` prints "Week 0" (negative later). LLM drops to one unit *in* week 8 (`w < 8`); review 7c says "1 a week after week 8". | `today` on 2026-09-24 printed "Week 0". | Refuse before start; confirm the week-8 boundary. |
| 28 | engine Close line | minor | INTEGRATED 1: his Close line "goes into the shared recall queue". Only the prepared cards do; there is no way to add his own line. | Keys say "His line goes into the recall queue"; no command does it. | `engine.py close <unit> "<line>"` adding one card. |
| 29 | facts.md | minor | INTEGRATED 2.7: "the date on every line"; only the header is dated. OpenAI and Google rows were "read through a summarising fetch; spot-check before use", yet check_unit treats every number in facts.md as verified for every unit. | facts.md lines 3-9. | Date each row; mark unverified rows and exclude them from `known` until checked. |
| 30 | SKILL.md recall | minor | The tutor rates the card ("4 instant"), which a text chat cannot time; llm-behaviour.md has him grade himself. The "lapsed card is flagged for its unit's refutation" rule is missing. | SKILL.md line 27. | He grades; the tutor records it; flag lapses. |
| 31 | SKILL.md stuck order | minor | Step 0 of ai-tutoring 4d is missing: if he says he does not understand the whole step, rebuild it with fewer new things before asking its question (D8 2/2). Units are fixed, so there is also nothing to rebuild from. | SKILL.md line 44. | Add step 0 with a prepared simpler version per explaining step. |
| 32 | Units vs C11/C18 | minor | "Pick and say why" gives A to D options first. C11: "stop prompting me/ giving me guesses in the chat option it ruins all the learning"; review 4 kept options on E12's evidence. Probably C11 means the chat-bar option buttons, but that is not recorded. | llm-02 "Pick and say why". | Ask him and log the answer in the evidence file. |
| 33 | session-start.sh, check_teaching_system | minor | The session prompt omits the cold check and the prediction. `check_teaching_system.py --quiet 2>/dev/null` prints nothing if the script itself crashes (for example if `faizos-core/src/server.ts` is missing), so a broken gate looks like a clean one. It checks no engine behaviour (cards due, id uniqueness, guard wiring to check_unit). | session-start.sh lines 7-16; check_teaching_system.py line 57. | Print a line on non-zero exit with no output; add engine and guard self-tests to the gate. |

Counts: **3 blockers, 21 major, 9 minor.**

## Research alignment of the machinery (item 2 of the brief)

- **FSRS settings.** `desired_retention=0.9` matches llm-behaviour.md and review 2a. `learning_steps=()` and
  `relearning_steps=()` give, for a new card: Again 1 day, Hard 1 day, Good 2 days, Easy 6 days; successive
  Good 2, 13, 51, 168, 521 days; a lapse after the first Good returns in 1 day. Reasonable. The fault is the
  entry time (finding 6), not the parameters.
- **10 minutes vs 5 minutes.** INTEGRATED wins (one 10-minute slot); llm-behaviour's 5-minute cap is correctly
  superseded, but no cap of any size is enforced (finding 9).
- **Interleaving.** Not done (finding 7).
- **Cold checks test new items.** Not done; the rulebook re-uses the cards (finding 2).
- **ai-tutoring.md:** answer withheld until commit: yes (one step per message, Key hidden), but the guard
  lets Key text through (finding 3). Step-level feedback: yes (per step). Stuck order: matches 4d steps 1 to 4,
  step 0 missing (31). Give on request / after second hint: missing (21). Stop questioning once understood: the
  line exists, but the fixed sequence and undefined scoring of skips work against it (24). No invented content:
  enforced only for numbers in prose, with bypasses (13 to 17); feedback, pictures and given answers are
  unchecked by design. Fixed sequence enforced by the system: not enforced (3).

## Spec items and status

Key: **done** = implemented as specified; **differs** = implemented differently; **missing** = not implemented.

### INTEGRATED 2, the shared layer
| Item | Status | Note |
|---|---|---|
| 2.1 One FSRS recall queue | done | one `queue.json`, FSRS 0.9 |
| 2.1 About 10 minutes a day | differs | printed, not capped (9) |
| 2.1 Mixed across all five skills | missing | blocked by unit (7) |
| 2.1 Number and code items with new surfaces | missing | (8) |
| 2.2 Prediction before every check, gap logged | differs | asked before the last step; not before cold checks by rule; abs gap (10) |
| 2.2 (review 7d) sure/unsure per item in eval and LLM | missing | (18) |
| 2.3 Commit, Check, Compare, Close frame | done | in the step lists; Close line not queued (28) |
| 2.4 One stuck order | differs | steps 1-4 present; step 0 and "on request" missing (21, 31) |
| 2.5 Bar on 2 sessions in a row | differs | any two latest sessions, same unit allowed (4) |
| 2.5 Same bar cold at 7 days | differs | no 7-day check, same items (2) |
| 2.5 Up one rung after 2 at bar | missing | (4) |
| 2.5 Down one rung after 2 below bar minus 20 | missing | (4) |
| 2.5 Confident wrong answer counts as below floor | missing | (4, 18) |
| 2.6 Dashboard, three numbers per skill | done | main = last session only |
| 2.7 Dated fact sheet | differs | dated header, not every line; unverified rows trusted (29) |
| 2.8 One step per message | differs | rule stated; guard allows several (3) |
| 2.8 Part template where a step explains | missing | (19) |
| 2.8 Plain words, terms explained at first use | differs | weak check (16) |
| 2.8 Every number produced by running code | differs | bypasses and untraced runs (13, 14, 15, 17) |
| 2.9 Change rule (8-week freeze, trials only, on cold score) | differs | stated; conflicts with "latest words win" (23); relies on the untrustworthy cold score (2) |

### INTEGRATED 3, mastery bars
| Skill | Bar | Status |
|---|---|---|
| Code | 90% of trace cells; tests pass within 2 attempts | differs: 90% of steps (1) |
| LLM | right answer with right reason on 2 cases | differs: 90% of steps (1) |
| Production | 9 of 10 on a mixed set | differs: 90% of steps; no units yet (1) |
| Evaluation | kappa 0.70+, no missed failure, 24+ traces pooled | differs: 70% of steps, no kappa, no pooling (1) |
| Design | 70/100 rubric, every brief number met | differs: 70% of steps (1) |
| Trial bars (trace pace, 90-s pace, rapid round, 80 for level 3) | missing | nothing recorded to review them at week 8 |

### INTEGRATED 4, start order
| Item | Status |
|---|---|
| Code and LLM week 1 | done |
| Production week 3 | done (scheduling); no units prepared yet |
| Evaluation week 4 after a placement check | differs: scheduled, no placement check (12) |
| Design week 6, "guess the architect's move" first | differs: scheduled Wed + Sat, no variant (12) |
| First full design session weeks 7-8 | missing |
| Start order reviewed at week 8 as a trial | missing (no record of the trial) |

### INTEGRATED 5, the week
| Item | Status |
|---|---|
| Recall every day | done |
| Mon evaluation unit | done (from week 4) |
| Mon, Thu, Sun rapid round 8 | missing |
| Tue code + LLM | done |
| Two LLM units a week before week 8 (second on Thu) | done; drops in week 8, not after (27) |
| Wed design session | done (from week 6) |
| Thu code unit | done |
| Fri production unit | done (from week 3) |
| Fri and Sun design drill 15 | missing |
| Sat design session | done (from week 6) |
| Sat whole task, A-D rotation | missing; the only Saturday message is unreachable (12) |

### INTEGRATED 6, trials
| Item | Status |
|---|---|
| Items marked trial, measured and adjustable after 8 weeks | missing: no trial flag or measure stored; rapid-round, warm-up gate, revote and fading data are not recorded |

### INTEGRATED 7, measures
| Measure | Status |
|---|---|
| 7-day cold score per skill | differs (2) |
| Cold 10+ below session alarm | missing (11) |
| Prediction gap, 10 or less after 4 weeks, alarm above 20 | differs: last-4 abs gap, no alarm (10, 11) |
| Outside tasks at the bar | missing (11) |
| Early warning: high in-session, low cold | missing (11) |

## Test scripts

In the session scratchpad (`t/harness.py`, `t1.py` week plan, `t2.py` flows and FSRS, `t3.py` cold checks and
mastery, `gtest.py` guard, `bad/*.md` checker cases). They run against a copy; nothing in the repo was changed
except this file.
