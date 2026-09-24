# Learning evidence: how Faiz actually learns

Evidence only. No instructions live here; the method is `.claude/skills/faiz-teach/SKILL.md`, and
every rule in it cites a finding ID from this file (A1, B3, D2...).

**Sources.** The full session transcript `2025914d-d872-4036-beab-57a2edc117ed.jsonl`
(2026-08-06 to 2026-09-14, 400 typed messages from him; the only session file for this project),
the `insights` (114 rows, all still `active=1`), `lessons` (47 rows) and `errors` (8 rows) tables in
`faizos-core/data/faiz.db`, `docs/how-faiz-learns.md`, `docs/teaching-analysis.md`, the memory notes.
The earlier analyses were re-counted from the transcript, not copied. Where my count differs from
theirs, both are shown.

**Scoring.** "Right first try" means his first reply to that question was correct and complete. A
half answer (right value, missing the label asked for) counts as not first try. "DU" means a message
from him saying he does not understand the teaching (not an "idk" on a single question).

---

## A. Every teaching format, measured

| ID | Format (dates) | Questions right first try | Code he produced | DU | His words |
|---|---|---|---|---|---|
| A1 | v1 Brick Method: one concept, one question per message, answer revealed after (08-06 to 08-11) | **100 / 115 (87%)**, almost all compute or apply-a-rule on ML concepts | one-blank files: 18 / 27 (67%) | 4 | "Yes that did land for me" (08-07); later "group more bricks together" (09-03) |
| A2 | v1 Brick plus "walk the code" line by line before the blank (08-11 to 08-13) | 30 / 35 (86%) | blanks: **6 / 11 (55%)**; errors moved to syntax and copying the adjacent line | 2 ("explain this concept again", "explain what these mean") | asked for it: "explain the code better... simpler and more precise" (08-11) |
| A3 | v1 consolidated module: 3-4 concepts taught, questions batched at end, one file with several blanks (08-13) | 19 / 22 (86%) | blanks 11 / 19; **9-concept sweep 1 / 5** vs 3-concept M18 and M20 **3 / 3 each** | 0 | "cover the next 40% in one session format" (08-13) |
| A4 | v3 write-from-empty: brief + tests, he builds a package from nothing (08-22 to 08-23) | 3 / 3 warm-up | none produced | 2 | "I don't understand a single word in your output message" (08-23) |
| A5 | One big self-explaining .py file with a YOUR TURN zone (08-24 to 08-26) | 2 / 2 | L1: passed after 2 corrections; L2 Task 1 three wrong attempts, Task 2 "no idea" | 2 | "I like this method of teaching commit this" (08-26), then "I have zero experience with python" (08-26) |
| A6 | Teaching in chat in grouped blocks, then a file task (09-03) | **10 / 17 (59%)**; cold why-questions **0 / 4** | L1 9/9 first submission; L2 Task 2 failed 4 times, answer supplied | 5 | "you're not explaining this properly... not just give me a skeleton shape to copy" (09-03) |
| A7 | Drill file + L3 opener in chat (09-03 to 09-04) | opener 1 / 3 | drill 2 of 6 tasks done | 2 | "You haven't explained the drill well at all" (09-04) |
| A8 | 300-line trace file (09-04 to 09-05) | not attempted | none | 1 | "hate long fucking files with so much information, mundane and long" (09-05) |
| A9 | 10-round Python bootcamp in chat: plain words, tiny generic code, 5-10 short questions per round (09-11) | **69 / 88 (78%)** (how-faiz-learns.md counted 71 / 89) | write-it-yourself after tracing the same idea: 4 / 5 first try | **0** (6 single-question "idk") | "this bootcamp was very successful, this is exactly what I needed" (09-11) |
| A10 | L3 as 2 big rounds, several parts per message, 7-16 questions each (09-11 to 09-12) | 35 / 45 (78%) | in-chat writes 2 / 6; blank-function build file **0 / 3** | 3 (incl. "give me the answers for all the wrong ones") | "I will never need to write code, I just need to know how to read and understand code very well" (09-12) |
| A11 | One huge read-and-judge message (10,440 chars, 51 questions) and the original Part B with ~8 new things on real file lines (09-12, 09-14) | hook 5 / 5; **Part B answered 0 of 8, twice** | none | 2 | "Divide these 5 parts (send them one by one)"; "reframe part B, i don't understand anything" (09-14) |
| A12 | One part per message, **template**: problem, fix, tiny generic example, picture, paths as bullets, 5 questions (09-14: B, C, D, E, H rebuilt, Round 2 A) | **24 / 30 (80%)** | none asked | **0** | "this one was better" (09-14) |
| A13 | One part per message, **real-file lines without** problem, picture or paths (09-14: F, G, H original) | **3 / 11 (27%)**; H original not answered | none asked | 1 | "you're breaking the skill again, idon't understand any of these at all" (09-14) |

Headline: the same learner scored 80% (A12) and 27% (A13) on the same day, same lesson, same
message length (1,550-2,120 chars). The difference was the template, not him.

---

## B. Features of a message that predict understanding

| ID | Feature | With it | Without it | Notes |
|---|---|---|---|---|
| B1 | Tiny generic example (≤8 lines, `ask_ai`, `prices`) before any real lesson code | bootcamp 78%, template parts 80% | real-file-first parts 27% (A13); ~8-new-thing real-file Part B 0 answered (A11) | Strongest single predictor seen |
| B2 | One everyday picture per idea | template parts 24 / 30; v1 sustained analogies (kitchen, chef) 12 / 12 on GPU, parallelism, collectives | F, G 3 / 11 | Confounded with B1 and B3 on 09-14 |
| B3 | Every path spelled out (if it works these lines run; if it fails this line is skipped) | H rebuilt with receipt-book paths 3 / 5 | H original, same lines, no paths: not answered, DU | |
| B4 | "The problem" stated first (what breaks in a real app) | A12 80% | A13 27% | he asked for problem-first framing himself for revision notes (08-21) |
| B5 | New things per part (keywords, machines, domain words) | 1 new thing: A12 80%; L1 code task with 1 new thing 9 / 9 | ~8 new things: 0 answered twice (A11); L2 code task with 9 new things failed 4 times; 9-concept sweep 1 / 5 blanks | Inside the bootcamp, rounds with ≤2 new things scored 26 / 33 (79%) vs ≥3 new things 43 / 55 (78%) when each was taught with a tiny example. The count matters most at the extreme and for code he must produce |
| B6 | Every rule a question relies on was stated in that part | bootcamp questions on stated rules | 6 misses traced to rules never said: `return` stops the machine, the hallway rule, `5 = 5`, bias, square vs round brackets, and/or/not | See E7 |
| B7 | Code shown in chat vs "go find it in the file" | bootcamp and template parts: in chat, 0 DU | file-based work produced complaints on 08-23 ("no direct links to files"), 08-24 ("haphazard files"), 09-04, 09-05 ("hate long files"), 09-12 (build file), 09-14 ("flaw in your teaching when it comes to code files"); navigation hints ("scroll up, read the def line") made him change a correct line (09-03) | His words: "I don't want code in files where I have to spend 30 minutes looking for the right part" |
| B8 | Message length | 700-2,100 chars: bootcamp 78%, template 80% | ≥3,300 chars: 16-question messages 78% but 2 "idk", a request for all answers and an overnight gap; 3,413 and 10,440 chars: rejected | Length alone did not separate A12 from A13 |
| B9 | Questions per message | 5: 80% (A12); 6-10: 78% (A9) | 1: 87% but he called it too slow ("group more bricks", 09-03; "add more questions in every part it helps", 08-10); 16: see B8; 51: not answered | |
| B10 | Question type | compute a number: v1 ~88%, 09-14 6 / 8, hooks 12 / 12; trace which lines run or what a sticker holds, short answer: 09-14 11 / 13; classify (caught or crash, legal or not): bootcamp 88% (how-faiz-learns), 09-14 4 / 6 | cold why-question: **0 / 4**; write code from a blank: 0 / 3 (L3 build), 0 / 1 (v3); predict broken code: see B11 | |
| B11 | "Someone broke it" format | label only (crash / quietly wrong / fine) inside a template part: **5 / 6** | simulating the broken code in a fill-in table: **0 / 4** first try (stopwatch, `log = []` in loop, F5 attempts table, G5); in real-file parts 0 / 2 | Tables of WORKING code: 5 / 6 |
| B11b | Label wording | L4: 8 / 10 first try with a label; both misses answered "wrong" instead of a label (R2-A Q5 for quietly wrong, R2-C Q5 for fine) | labels were never defined inside the question |
| B12 | Answer given away in my text (confirming half, numbers to plug in, a hint implying the answer) | | he flagged it 4 times: 08-22, 09-03 07:26, 07:32, 08:05 ("i wont say this again") | |
| B13 | Worked example whose parts do not transfer | shopping-bill example with the exact same shape: Task 2 structurally right first try (08-26), 9 / 9 (09-03) | `longest_word` used `len()` and `>` for a cheapest search: he copied both, then "the example you gave was horrible" (09-03) | |
| B14 | Build decision states each option's effect on the target number, with the chain | not yet tested (L4 build gave only per-call costs) | L4: 4 / 5 picks sound; decision 5 "no deadline" chosen though timeouts were taught in L3, prediction 736 ms vs 1,753 ms measured. Per-call cost ("a 2 s wait each time") was given, the effect on p95 (hangs above 5% of calls set p95) was not. He asked twice for deeper explanation (C31, C32) |

---

## C. Every rule he stated about how to teach him, in order

S = later superseded by his own words. B = broken by Claude after he said it (count).

| # | Date | His words (short) | Status |
|---|---|---|---|
| C1 | 08-06 | "tell me what each word means" | B ×4: micrograd jargon 08-07, P0 terms 08-23, "Again... fancy jargon" 09-05, "provider" undefined 09-14, L5 Part A prompt/ship/summariser/eval set 09-15 (now ×5) |
| C2 | 08-06 | "complete beginner... jargon explanation too detailed... simple analogies... start simpler" | standing |
| C3 | 08-07 | "build it slowly brick by brick... answer small parts THEN reveals the right answer... keep the lessons small and compact" | S: one-question-per-message by C17 (09-03); size by C6, C22 |
| C4 | 08-07 | "the revision should include the background/context and the reasoning" | standing (revision notes) |
| C5 | 08-07 | "you're confusing me with ur jargon"; "the python jargon threw me off" | standing, restates C1 |
| C6 | 08-08 | "you can make the lessons longer" | S by C22 (09-11) and C27 (09-14) |
| C7 | 08-10 | "add more questions in every part it helps" | standing; restated as C23 |
| C8 | 08-10 | "summary logged in after every session NON NEGOTIATABLE" | standing (session log) |
| C9 | 08-11 | "explain the code better... simpler and more precise" | standing; narrowed by C29 (only the lines needed, in chat) |
| C10 | 08-21 | notes must say "what problem they're targeting and how they are solving it" | standing |
| C11 | 08-22 | "stop prompting me/ giving me guesses in the chat option it ruins all the learning" | B ×3 (he restated 09-03 three times) |
| C12 | 08-22 | "whenever i give a wrong answer... say wrong, try again with a small reframe and hints" | standing, with C19 as the exit |
| C13 | 08-23 | "no direct instructions, no direct links to files" | S by C29 (code comes to him in chat) |
| C14 | 08-23 | dials: I write working code, he modifies; long, engaging, build-focused lessons | S by C18 (in chat), C21 (hates long files), C24 (reads, not writes) |
| C15 | 08-24 | "I need one file... fully explained within the file in hashtags... exact area to be marked" | S by C16 ("Not inside the file", 09-03) and C21 |
| C16 | 08-26 | "you've done this twice now never do it again... check my actual code" | B ×2 same day before it was fixed; standing |
| C17 | 09-03 | "explain and teach me the concept and the code before you test me"; "Not inside the file"; "group more bricks together" | B ×3: untaught why-questions 09-03, drill 09-04, real-file parts F-H 09-14 |
| C18 | 09-03 | "stop showing me the answers in chat bar (i wont say this again)" | standing (restates C11) |
| C19 | 09-03 | "if it's still wrong give me the actual answer explaining each line" | standing; restated 09-04, 09-11, 09-12, 09-14 |
| C20 | 09-03 | "i'm a beginner, you need to explain and TEACH, not just give me a skeleton shape to copy" | standing |
| C21 | 09-05 | "ur using fancy jargon"; "hate long fucking files with so much information"; teach Python "simple, interactive and fun" | standing |
| C22 | 09-11 | "you should ask more questions"; "ik this dont repeat, move onto next session"; "Each lesson should have 2 rounds (they can be much bigger in size)" | standing |
| C23 | 09-11 | "give and explain the answer" (on idk) | standing, same as C19 |
| C24 | 09-12 | "I will never need to write code, I just need to know how to read and understand code very well... develop engineering logic... explain what each part of the file and code does" | standing; supersedes C14's "he modifies" |
| C25 | 09-14 | "Divide these 5 parts (send them one by one)" | standing; supersedes "one message per round" from C22 and C3's pacing |
| C26 | 09-14 | "never structure it like that, going against the record" | standing |
| C27 | 09-14 | "i just don't like repitition and the need to repeat something again and again. Fix the way you teach code(this one was better)" | standing |
| C28 | 09-14 | "give me the answer for 4 and move on"; "The method is inconsistent, you keep deviating, its incoherent and haphazard" | standing |
| C29 | 09-14 | "I don't want code in files where I have to spend 30 minutes looking for the right part"; patterns go "continuously" into the feedback loop "without conflicting instructions" | standing |
| C30 | 09-14 | "Each lesson can still have a build (just needs to be one I understand and build through my concepts and decisionmaking rather than my code writing)" | standing; in faiz-teach "The build" |
| C31 | 09-15 | "decision 3 and 4 depend on where the majority of my users are which is unknown so correct that for the future and also explain these questions more throughly" | standing; in faiz-teach "The build" |
| C32 | 09-15 | "I liked the build part, i want it to be more throughly explained (the implications of my decisions and the choices should be explained much better)"; "parse this lesson, add to the feedback loop and improve the next lessons (make this automatic)" | standing; in faiz-teach "The build" and "How this file changes" |
| C33 | 09-15 | "Rephrase this, I don't understand what this is saying. You need to explain the jargon you throw" (L5 Part A used prompt, ship, summariser, eval set undefined) | standing; enforced by docs/glossary.md in the checker |
| C34 | 09-17 | "Explain the problem with the right context and background so I can fully understand and develop my thought process. Commit this to the lesson dev" | standing; faiz-teach template step 1, checker requires 4+ sentences |
| C35 | 09-18 | "Option C obviously (decisions cannot be this obvious)" on L5 build decisions 1 and 2 | standing; faiz-teach "The build", checker rejects an option that rules out nothing |
| C36 | 09-18 | "You need to improve the quality of your questions too, make them so they improve my understanding" (L6 Part B Q1, Q2 only read back numbers printed in the part) | standing; faiz-teach Questions, checker flags read-back answers |
| C37 | 09-22 | "Idw predict, just build" (L6 build, at the prediction step) | superseded by C39 (09-22) |
| C38 | 09-22 | "This lesson was better, but the quality needs to be improved... improve the quality of the questions, make them more analytical and thought provoking. The explanations need to be more specific and MUCH clearer with all the background/context and necessary details." Asked for a research agent (best teaching methods, catching and keeping attention) and an adapter agent (fit them to his way of learning) | standing; in progress 09-22 |
| C39 | 09-22 | "I don't mind predicting if I'm given all the data I need to make my prediction there. The decisions need to be harder, more like actual engineering decisions and more realistic" | standing; faiz-teach "The build" steps 2-3 |
| C40 | 09-23 | "My issue with this project is it is not utilising my cognitive abilities. The AI is trying to teach me, but my brain works much better than the AI. I need you to suggest radical changes to this program that fully engage my cognitive thinking and utilize my brain with a fully supported system." | pilot: faiz-teach "Investigation mode", case-01 (real FBR corpus, lab, case checker, devils-advocate agent) |
| C41 | 09-24 | On case-01: "What am I supposed to do here"; then "You need to redefine the whole problem. Rephrase the original prompt including the clear job description (commit this)" | standing; faiz-teach Investigation mode step 1, check_case.py requires the sections |
| C42 | 09-24 | After 4 open moves in case-01: "I don't understand this exercise we're doing. seems unstructured and pointless" | standing; faiz-teach Investigation mode step 2: fixed diagnostic stages with evidence laid out |
| C43 | 09-24 | On case-01 Stage 1 (restated twice): "i don't understand this at all"; then "stop this crap now. this is wasting my time, makes no sense. I want you to push all my completed lessons to github and then we'll reframe" | investigation pilot stopped; reframe pending |
| C44 | 09-24 | Handwritten notes (docs/research/curricula/faiz-notes-2026-09-24.jpg): the five AI-engineering skills are different kinds of skill and need different methods. Evaluation = logic + understanding + methods (CORE); LLM behaviour = learning/understanding; system design = logic build-up + cognitive development (CORE); production = maths + quality control (applied); code = understand, steer and write, "code needs to be learnt" (CORE; specifying, reading and judging, debugging, small edits). "The previous system was suppressing the use and development of my cognitive ability." | open; plan proposed 09-24 |
| C45 | 09-24 | "For all applied parts (code, evaluation, system design), worked examples and detailed workings of sample questions are a good reference point to develop an understanding." Asked to revise the expert research on these findings, build a proven system optimised for him; bought ScaleDojo Architect, "scrape everything"; use Khan Academy and other resources too | open |

**Contradictions resolved by his most recent statement**
1. Lesson size: small (C3) → longer (C6, C14) → hates long files (C21) → 2 big rounds (C22) → one part per message (C25). Resolved: a lesson is 2 rounds of several parts; each message carries one short part.
2. Pace: one concept per message (C3) → group bricks (C17) → more questions (C22) → one part per message (C25). Resolved: one part, one new idea, about 5 questions, per message.
3. Never reveal (C12) vs give me the answer (C19, C23, C28). Resolved: never reveal unasked; when he asks, or after the second failed hint, give it with the reason.
4. Where teaching lives: inside one file (C15) → chat, "Not inside the file" (C17) → no hunting in files (C29). Resolved: all teaching and all code he must read is in chat.
5. Who writes code: he modifies working code (C14), learns Python by writing (C15) → never needs to write code (C24). Resolved: he reads and judges; no write-from-blank.
6. Walk every line (C9) vs "30 minutes looking for the right part" (C29). Resolved: walk only the lines the part needs, pasted in chat.
7. Not stated by him but live in the system: 114 `insights` rows are all `active=1`, including obsolete ones ("THE ONE-FILE LESSON FORMAT IS THE ONE THAT WORKS", "one tiny concept per message", "every lesson has exactly 2 rounds... all in ONE message"). They are a second, contradicting instruction source.

**Corrections he had to give more than once**: jargon ×4, telegraphing ×4, "explain/teach, I'm a beginner" ×4 (08-06, 08-26, 09-03, 09-04), long or scattered files ×3, template broken ×2 on 09-14, stale file read ×2.

---

## D. What recovers him when stuck

| ID | Move | Worked | Cases |
|---|---|---|---|
| D1 | Point at his own earlier answer, or a table of his own earlier numbers | **15 / 17** | v1 self-consistency tables ×4 (graph breaks, Amdahl, LoRA, quantization); bootcamp R3, R7, R9, R10; L3 R2 Q16; 09-14 F5; 09-14 R2 B1, B4, B5, C5, D5. Failed: L3 Part C Q7, 09-14 G4 |
| D2 | One new everyday picture | **8 / 10** | bias as a fixed cost, XOR fence, dimmer switch, parcel label vs contents, cashier closing the till, supermarket basket, house hallway, receipt book (09-14, fixed 2 questions). Failed: stopwatch race (09-11), torn-out notebook (09-12) |
| D3 | Enumerate line by line ("1 held, 2 held...") | 3 / 3 | GPipe activations, speculative decoding, powers of two by doubling |
| D4 | Shrink to a two-option question | 5 / 7 | bootcamp R4 Q3, R10 Q3; 09-14 D5 ("is the dashboard telling the truth?"), H4 (one per swipe or one per customer); v1 "2 knobs, how many updates". Failed: stopwatch sort-into-3-jobs, G4 two yes/no |
| D5 | Step table with the last cells blank (working-code trace) | 3 / 4 | bootcamp R6, R8; 09-14 F5. Failed: L3 Part C Q6 |
| D6 | Re-explaining in more prose, re-reading a rule, or navigation ("scroll up, read the def line") | **0 / 5** | XOR prose (08-10), bootcamp R9 Q2-3, R10 Q3, "scroll up" (09-03, broke a correct line), detailed fix instructions (09-03) |
| D7 | Giving the answer with explanation, when he asked | ends the stall 6 / 6; **retained later 1 / 3** | Retained: KeyError crashes (09-11 → 09-14 C3). Not retained: reset-inside-loop (answer 09-12 → F5 wrong 09-14); one record per call (answer G4 → H4 wrong in the next part) |
| D8 | Rebuilding the whole part from the template after "I don't understand" | 2 / 2 | Part B: 0 answered → 4 / 5; Part H: 0 answered → 3 / 5 |

He asked for answers 6 times (09-03, 09-04, 09-11 ×2, 09-12, 09-14), always after two failed hints on
one question or inside a message with 7+ questions.

---

## E. Recurring weak spots in the material

| ID | Weak spot | Count | Examples |
|---|---|---|---|
| E1 | Crash vs runs-and-quietly-wrong: says "crash" for quiet code or "nothing" for a crash, or gives the value without the label | **11** | slots in the wrong order (said crash), `total = 0` in loop (idk), missing dict key (said "nothing"), append onto a full list ("you cant do that"), misplaced stopwatch, `log = []` in loop, Round 2 Q15 (no label), 09-14 D5 ("fine"), F5 ("crash"), G6 (no label), L2 tracker at 0 (idk) |
| E2 | A start line (`total = 0`, `log = []`, `attempts = 0`, the clock) moved inside a loop | 4 of 5 missed first try | only Round 2 Q15 (switch never trips) right first try |
| E3 | Counting one record per call vs one per try; things around a repeated or paired step | 09-14: 3 in two parts (G4 said 4 then 3 records, H3 "inside", H4 "2 receipts"); v1: 4 (graph-break phantom cost, GPipe doubled twice, speculative +1) | counts the visible events, misses what the mechanism collapses or adds |
| E4 | Which kind of stuff a sticker holds: the list vs one item, a dict vs the number inside, the kind vs the note | **12** | `cost_for(MODELS)` ×3, `model = cost_for(...)`, `prices` "on 110", `total + c` with a dict, quotes on numbers, `fails_in_a_row.append()`, 09-14 E1 (`RuntimeError` for the note), E2 ("sticker" for the kind); DB `api-misuse` 7, `ordering-pairing` 4 |
| E5 | Name vs the text of the name (quotes) | 4 | `"pricey_model"`, `"110"`, `{"model": "m", "cost": "c"}`, `Price` vs `price` |
| E6 | Misreading a symbol or position | 6 | 2nd vs 3rd item, `sorted[times]`, `lines` vs `line`, BACKOFF list misread (F2, F3), missing closing quote |
| E7 | A rule never stated, then tested | 6+ | `return` stops the machine, the hallway rule, `5 = 5`, bias, square vs round brackets, and/or/not; cold why-questions 0 / 4 |
| E8 | Copying a visible pattern that does not apply | 4 | KV cache `range(step+1)` from the version above, LoRA `d * d` from the adjacent function, math in a comment pasted as code, `longest_word`'s `len()` and `>` |
| E9 | Inverse relationships and expression vs statement (v1 era, DB) | 3 + 3 | rate vs duration, exp/ln; `return 2 trips`, `rm_score = drift * -beta` |
| E10 | Arithmetic slips (not a concept gap) | 3 | 6500 ms for 0.65 × 1000, a dropped zero, 12x for 12.5x |
| E11 | A saving or difference computed from one side only (the new cost, or the part saved per unit) instead of before minus after | L4 0 / 2 first try | R2-B Q2 answered 4 x 30 = 120 (right: (20 - 4) x 30 = 480); R2-C Q3 answered 1,760 (right: 90 x 20 = 1,800). Both fixed by pointing at his own two numbers (2 / 2) |
| E12 | Which way a wrong number bends a decision, or what a number proves | L6 R2 0 / 3 first try | R2-A Q4 (300 PASS proves only the judge's view), R2-B Q4 (70% catch bends toward passing, said failing), R2-C Q4 (best of five reads high). Two fixed on one hint, one answer given; L7 R1-A, C, E: 0 / 3 first try even with a Worked chain, 3 / 3 once reworded as two options (higher or lower, toward or away) |

---

## Session ledger

One row per teaching session. Questions = questions asked; right = right first try.

| date | lesson/part | questions | right first try | stuck points | his feedback |
|---|---|---|---|---|---|
| 2026-08-06/07 | v1 M1 matmul FLOPs (Brick) | 15 | 13 | rows vs columns, dropped zero, indentation | "Yes that did land for me" |
| 2026-08-07 | v1 micrograd | 8 | 7 | Python jargon in a 60-line file | "you're confusing me with ur jargon"; "the python jargon threw me off" |
| 2026-08-08 | v1 tiny net, neuron, layer | 11 | 10 | bias (what and why) | "i'm unclear on the concept"; "you can make the lessons longer" |
| 2026-08-08/10 | v1 MLP / XOR | 10 | 9 | XOR geometry in prose, off-by-one range | "i don't understand this part"; "add more questions in every part it helps" |
| 2026-08-10 | v1 attention, QKV, RoPE, RMSNorm | 16 | 13 | purpose vs mechanic, i/j positions; blanks 3/4 | none |
| 2026-08-10 | v1 transformer block, train attention, BPE, KV cache | 15 | 12 | copied comment math, "token 1" ambiguity, copied line above; blanks 2/6 | none |
| 2026-08-10 | v1 SwiGLU, GQA, SSM, scaling, perplexity, MLA | 19 | 17 | the gate (dimmer fixed it), a·state step 0, exp/ln; blanks 6/6 | "( 1, 4, 0 ), but i don't understand this concept" |
| 2026-08-10/11 | v1 GPU memory, Triton, FlashAttention, compile, Amdahl, parallelism | 21 | 19 | powers of two, units in code, phantom cost, inverted ratio; blanks 3/6 | "explain the code better... simpler and more precise" |
| 2026-08-11 | v1 collectives, FSDP, pipeline, checkpointing (walk the code) | 13 | 11 | English in code, doubled activations; blanks 3/4 | none |
| 2026-08-11/12 | v1 LoRA, quantization, inference, serving | 13 | 11 | stored count vs shape, adjacent copy, docstring leak, brackets; blanks 1/4 | "explain this concept again" |
| 2026-08-12/13 | v1 RL, GRPO, reward modeling | 9 | 8 | reward/advantage pairing, assignment in return; blanks 2/3 | "explain what these mean" |
| 2026-08-13 | v1 M16-M20 consolidated + foundations sweep | 22 | 19 | 9-concept sweep blanks 1/5; brackets, and/or/not; blanks 11/19 | "cover the next 40% in one session format" |
| 2026-08-22/23 | v3 P0 packaging, write-from-empty | 3 | 3 | undefined terms, no clear steps, build not attempted | "I don't understand a single word in your output message" |
| 2026-08-24/26 | L1 tokencost, one self-explaining file | 1 | 1 | Python grammar, names from the brackets; passed after 2 fixes | "I have zero experience with python"; "I like this method of teaching commit this" |
| 2026-08-26 | L2 ratecard, one file | 1 | 1 | dividing text, passing whole list; Task 2 "no idea"; stale read ×2 | "you've done this twice now never do it again" |
| 2026-09-03 | L1 rebuilt, chat blocks + file | 10 | 6 | cold why-questions, telegraphing; tasks 9/9 | "Not inside the file"; "group more bricks together"; "i wont say this again" |
| 2026-09-03 | L2 rebuilt, chat blocks + file | 7 | 4 | why-questions, `longest_word` example, navigation; Task 2 supplied | "the example you gave was horrible"; "not just give me a skeleton shape to copy" |
| 2026-09-04 | drill file + L3 opener | 3 | 1 | drill 2/6; for-line never taught | "You haven't explained the drill well at all"; "leaves the concepts incomplete in my mind" |
| 2026-09-05 | L3a 300-line trace file | 0 | 0 | rejected unopened | "hate long fucking files" |
| 2026-09-11 | Python bootcamp R1-R10 (chat) | 88 | 69 | crash vs quiet ×4, unstated rules (return stops, hallway, 5 = 5) | "ask more questions"; "ik this dont repeat"; "this is exactly what I needed" |
| 2026-09-11/12 | L3 Round 1 + Round 2, big multi-part messages | 45 | 35 | writes 2/6, reset in loop, quotes on stickers; build file 0/3 | "Each lesson should have 2 rounds"; "give me the answers for all the wrong ones"; "I will never need to write code" |
| 2026-09-12 | L3 read-and-judge, one 51-question message | 5 | 5 | Part B (~8 new things) never answered | "Divide these 5 parts (send them one by one)" |
| 2026-09-14 | L3 R1 parts B (rebuilt), C, D, E (template) | 20 | 16 | kind vs note, sticker vs kind, "fine" vs quietly wrong | "reframe part B, i don't understand anything"; "this one was better"; "i just don't like repitition" |
| 2026-09-14 | L3 R1 parts F, G, H (real-file lines, no template) | 11 | 3 | misread BACKOFF, 1 record vs tries, reset in loop; H unanswered | "give me the answer for 4 and move on"; "you're breaking the skill again" |
| 2026-09-14 | L3 R1 H rebuilt (receipt book) + R2 Part A (closed-until sign) | 10 | 8 | failed record inside vs after loop, receipts per swipe; R2 Part B unanswered | "how many more of these rounds are left"; "The method is inconsistent, you keep deviating" |
| 2026-09-14 | L3 R2 parts B-E, first lesson taught from a validated script | 20 | 15 | whole dict vs one label, the works path resets the streak, value from a broken line, "trips" read as crash, p50 of mostly zeros; all 5 resolved by pointing at his own earlier answer (5/5) | "explain number 5" |
| 2026-09-14/15 | L4 live: R1 A-D, R2 A-E (validated script) + decision build | 45 + build | 41 | the gap saved vs a whole time (R2-B Q2, R2-C Q3), a redone step redoes the rest (R2-C Q2), "wrong" for slow-but-correct (R2-C Q5), all fixed on one hint; build: picked no deadline, predicted 736 ms, measured 1,753, changed decision 5, 500-call rerun 802 ms vs 2,066 | "decision 3 and 4 depend on where the majority of my users are which is unknown"; "explain these questions more throughly" |
| 2026-09-17/18 | L5 evals: R1 A-D, R2 A-D, build D1-D5 + predictions | 40 + build | 31 | always-true assert, absolute bar vs baseline, the baseline moving after a change lands, least access; 2 of my questions were worded abstractly ("does the list notice", "how many setups") | "You need to explain the jargon you throw"; "Explain the problem with the right context and background"; "decisions cannot be this obvious" |
| 2026-09-18/22 | L6 judge: R1 A-E (SQL), R2 A-C, build D1-D4 | 40 + build | 31 | complement count (36 of 40 agreed, said 6 disagreed), GROUP BY one pile vs many, a duplicate row joining twice, all three R2 direction questions (E12); build: two cost-adding picks together broke $5 ($7.36), changed D3 to plain C, met target (catch 93%, clear 95%, 4.4 h, $4.80) | "improve the quality of your questions"; "explain and answer 4 then proceed"; "Idw predict, just build" |

**Taught and answered right, do not re-teach** (as of 2026-09-14): six kinds of stuff, stickers,
quotes, machines and slots, left and right of `=`, colon and push right, `return` stops the machine,
lists and positions, `for`, piling up a total, dicts and `KeyError`, `if` and comparisons, the hallway
rule, average vs p50/p95, the stopwatch, one record per call, try/except, named kinds, several kinds in
brackets, `as err` and `str(err)`, the L3 retry loop (lines 76-90), success record (69-87), failure
record after the loop (92-96), the closed-until sign, changing a value under a dict label, `>=` and the trip, which calls a number counts
(successes only), finding a one-word planted bug from a real report. Lesson 3 complete.
L5: test cases, assert, cases from real failures, list size vs the smallest visible change, the gate,
the baseline, the fresh computer that runs it, short-lived passes. Build: a gate that blocks a 5 point
fall and allows a 3 point gain, $0.54 a run.
L6: failure names and counts, SQL WHERE/COUNT, GROUP BY, JOIN (drops unmatched, duplicates double),
ROW_NUMBER over a PARTITION, a judge with one checkable rule, catch rate (TPR) and clear rate (TNR),
the wobble 2*sqrt(p(1-p)/n) and square-root scaling. Not yet taught: Cohen's kappa. Build: judge at
catch 93%, clear 95%, $4.80 a week. Open: L7 search.
L4: a URL, the @app.get tag, health checks, one socket for AI companies, the image box, two stages,
reused build steps, cold starts, travel time; decision build shipped in a local container. Open: L5 evals.
