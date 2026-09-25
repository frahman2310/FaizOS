# Gap audit: the LLM-behaviour skill, from research base to what Faiz receives

Written 2026-09-25, after his first-session complaint (C49): the plan was built on how experts teach each
skill, but the build bypassed it; no worked example, overloaded at once, questions that made no sense.
This audit follows the whole chain for one skill and asks, at every link, what the research says experts do
and what survived:

research base (`docs/research/curricula/*`, `recommended-method.md`, `postmortem.md`, `teaching-methods.md`,
`private/research-base/learning-methods/*`, `private/research-base/production-and-llm-behaviour/*`)
-> `docs/research/structures/llm-behaviour.md` -> `docs/research/structures/INTEGRATED.md`
-> `.claude/skills/faiz-teach/SKILL.md` -> `learn/engine.py`, `learn/check_unit.py`, `hooks/teaching-guard.py`
-> `learn/units/llm/01` to `04`, read message by message as he would get them.

File references are `file:line`. "His record" means `docs/learning-evidence.md` (A, B, C, D, E IDs).

---

## 1. Verdict

**The LLM units do what the structure file says, and the structure file is where the expert method was
lost.** `llm-behaviour.md` decided that this skill gets "No worked example" and that his "first act"
is to "commit to an answer with a reason and confidence, before any teaching" (`llm-behaviour.md:92-93`).
It rests on a misread source: Chen, Kalyuga and Sweller 2015, cited everywhere as "answering first beats
worked examples for simple material", tested students who **studied** the material for 10 minutes and
**then** recalled it. That is retrieval after teaching, not answering before it. Every expert the
structure itself names (Karpathy, Huyen, the Hugging Face course, ScaleDojo, 3Blue1Brown, the
skill-methods "mechanism card") shows the mechanism with real numbers first, or asks one ungraded
pre-question and reveals the answer at once.

The later links then made it worse. The engine grades the before-teaching question as half of the pass
rule, with no hints allowed. The Stop hook blocks the stuck-help and the expert explanation, because both
sit in the answer Key. The checker checks formatting and numbers but none of the teaching rules. So what he
receives is: a first message with 5 to 8 new ideas and no goal; a graded multiple-choice question on a
mechanism nobody has shown him; a guess with no data; a "why" question about something never explained;
and the first plain statement of the idea in message 6 of 8.

What survived and is sound: real runs instead of invented outputs, small-model caveats, contrasting rows in
the opening (Loibl's "contrasting cases"), refutation texts that use his own run as evidence, cards with
varied surfaces, and a new-surface cold check.

**Counts: 5 blockers, 20 major, 10 minor (35 findings).**

---

## 2. Findings, in chain order

### 2.1 Research base (errors that everything downstream inherited)

**F1. Blocker. Chen, Kalyuga and Sweller 2015 is misread as support for "answer before any teaching".**
- Where: `curricula/skill-methods.md:34`, `:114-116`, `:244`, `:255`; `curricula/method-effectiveness.md:51`,
  `:122`, `:156`; `recommended-method.md:55`, `:65`; `curricula/curriculum-map.md:33`;
  `private/research-base/learning-methods/INDEX.md:180` ("generate, do not show"); `postmortem.md` cause 2;
  `structures/llm-behaviour.md:77`, `:276`, `:287`; `structures/review.md:130`.
- What the source says: in Experiment 1, "The first booklet contained eleven basic geometry formulae ... and
  was common to both conditions" and students studied it for 10 minutes; only then did the generation group
  "generate all of the formulae they had studied in the first booklet" while the other group re-read them
  (`chen-kalyuga-sweller-2015-element-interactivity.md`, study, generation and test stages, about lines
  427-466). The "low element interactivity" material was memorising single formulas, where "the interacting
  element count is 1". Tests were same-session only (INDEX.md correction 3).
- What was built instead: "His first act ... commits to an answer ... before any teaching" (`llm-behaviour.md:93`);
  "Answer-first placement, no worked examples ... Chen, Kalyuga, Sweller 2015" (`:276`).
- Fix: correct the citation in every file listed. What Chen supports for this skill is "study, then
  retrieve" (the cards), and worked examples for novices on material with interacting parts. Nothing in the
  base supports graded answering before teaching for a novice.

**F2. Major. The skill is called "simple material" and "the hardest kind of change" at the same time.**
- `llm-behaviour.md:18-25` and `:38` classify the core ideas as conceptual change, with "the model is a
  database I query" as a Chi category mistake, "the hardest". `:276` and `:287` then exempt the skill from
  worked examples because the material is low in interacting parts. `skill-methods.md:53` calls it
  "Recurrent facts".
- Research: Chen 2015 defines element interactivity relative to the learner; for a novice even `x + 5 = 8`
  has about 9 interacting elements (Chen, about lines 146-157). "The wording changes the model's chances for
  the next piece, learned from training text" involves tokens, a probability over every piece, training
  text and the prompt shape at once.
- Fix: split the skill in two kinds, as the structure's own section 1 does: facts (prices, ratios, digit
  rules: taught once, then cards) and mechanisms (next-piece prediction, sampling, statelessness: worked
  demonstration first, for a novice).

**F3. Major. Productive failure is used without its boundary conditions.**
- Research: productive failure needs (a) a problem that "accommodate[s] various solution approaches" where
  students "should be able to make progress" and "should not be frustrated", (b) a problem "for which
  students have some prior knowledge and ideas", and (c) consolidation where "the teacher first consolidated
  by comparing and contrasting student-generated solutions with each other, and then modeled and worked
  through the canonical solution" (Kapur and Roll chapter, lines 83-95 and 300; Loibl, Roll, Rummel 2017,
  lines 1266-1270). Without contrasting cases or instruction built on the student's solutions: "no or
  negative effects" (Loibl 2017, lines 1197-1201). Kapur 2016: in-session failure is a poor guide, so the
  generation phase is not graded (INDEX.md, kapur-2016 entry).
- What was built: a single four-option pick with one right answer (not generation), graded, on every
  concept, including concepts where he has no intuitive ideas to activate (temperature in llm-03, the
  tokenizer's chunk list in llm-02). Consolidation is a fixed 3-line "right idea" at step 6 that does not
  build on his answer (see F14 for why the expert version cannot be shown).
- Met: contrasting cases in the openings of llm-01 and llm-02 (two wordings, two tokenizers), and real
  intuitive ideas for llm-01 (search) and llm-04 (memory).
- Fix: keep a pre-question only where he has intuitive ideas; never grade it; consolidate immediately with
  the canonical mechanism and a prepared line on each option he might pick.

**F4. Minor. ConcepTests are used as the first act; in Peer Instruction they follow a short presentation.**
- `llm-behaviour.md:32-33` cites Crouch and Mazur for ConcepTests and the 35 to 70% first-vote band. In Peer
  Instruction each ConcepTest follows a brief presentation on the point (Crouch and Mazur 2001, the PDF
  linked at `:32`; this paper is not saved in the research base, so verify before relying on it). A 35 to
  70% band also means 30 to 65% of first answers are expected to be wrong, against his measured working
  level of about 80% (A9, A12) and Khan's "Familiar" band of 70 to 85% (`skill-methods.md:64`).
- Fix: save the Crouch and Mazur PDF to the base and quote the sequence; if confirmed, a ConcepTest comes
  after the worked demonstration, as the check.

### 2.2 `structures/llm-behaviour.md`

**F5. Blocker. The structure removes the worked demonstration that every named expert uses.**
- Where: `llm-behaviour.md:61-73` (Break-it unit: Puzzle, ConcepTest first vote, Predict, Run, Explain,
  Refute, Transfer, Keep) and `:92-93` ("No worked example ... before any teaching").
- What the experts do, from the base:
  - Karpathy (the source the unit quotes): shows tokens in the Tiktokenizer, then the network's next-token
    probabilities with numbers ("4% ... 2% ... 3%"), then sampling as a "biased coin", then the base model
    as "a glorified autocomplete" (`karpathy-deep-dive-...-transcript.md` lines 33, 43-47, 61, 95). He
    explains, then shows the odd behaviour.
  - skill-methods C2's own "mechanism card": Claim, Predict, Demonstration, **Why: the mechanism in three
    to five lines**, Consequence, Where it breaks, Recall (`skill-methods.md:118-125`).
  - teaching-structure Part B, every segment: "(a) Predict or pick first, one question ... (b) Explanation
    under 250 words with one worked example using named data and numbers. (c) One check question"
    (`teaching-structure.md:151`).
  - teaching-craft's worked temperature part: hook, pick first, the score table, the rule, and "The answer
    was (c)" in the same part (`teaching-craft.md:181-213`).
  - ai-tutoring 1d: "Tell facts, names and rules he cannot work out alone. Asking about them only produces
    guesses" (`ai-tutoring.md:68-71`).
- Fix: see the template in section 4. A pre-question may come first; the worked demonstration and the
  answer come in the next message; the first scored question comes after.

**F6. Major. The "Why" moved from the tutor to him.**
- Research: skill-methods C2 step 4 gives him the mechanism in 3 to 5 lines (`skill-methods.md:123`); the
  "full context" rule puts Mechanism second, "shown on one concrete case with real numbers"
  (`teaching-methods.md:156-163`). Crouch 2004's point (`llm-behaviour.md:34`) is that the explanation must
  be written and "checked against the source".
- Built: step 5 "Explain" asks him to write why the result happened, before anyone has told him
  (`llm-behaviour.md:70`). His record: cold why-questions 0 / 4 (B10).
- Fix: the tutor states the mechanism from the named source; his "why" is a self-explanation prompt on the
  key step of that explanation (method-effectiveness row 8, g = 0.55, "focused prompt on the key step").

**F7. Major. The one worked example the structure did plan was dropped.**
- `llm-behaviour.md:114` plans concept 3's demonstration as "Huyen's [1, 3] logits by hand, then 20 runs";
  card D has a "Worked number" lens (`:165`); teaching-craft T9 "Sweep one knob: one run, then a table
  across a knob" (`teaching-craft.md:113`) and its worked temperature table (`:189-194`).
- Built: llm-03 never shows how temperature reshapes the chances. He sees outputs at 0, 0.7 and 1.5, but
  no table of picking chances at different temperatures, and no card with a worked number.
- Fix: add the Huyen [1, 3] table (or the run's Apple/Orange chances) at T = 0.5, 1 and 2 as the worked
  demonstration in llm-03, before any scored question.

**F8. Minor. Concept order puts next-piece prediction before tokens.**
- `llm-behaviour.md:105-108` says order follows Karpathy's deep dive ("data, tokens, network, inference");
  the table puts next-token (1) before tokens (2). So llm-01 must use "token" before it is taught
  ("the next unit is about these", `01:14`).
- Fix: either swap units 1 and 2, or keep the order and define "piece of text" fully in llm-01 without
  the word token.

**F9. Minor. The structure's own checks on question difficulty were not built.**
- `llm-behaviour.md:182-201` (LBCI baseline) and `:256` (first-vote band 35 to 70%, "under 35%: prerequisite
  missing") are the only way to see that a question is too hard. No inventory exists; confidence per step
  is not recorded (engine takes only a `--confident-wrong` count).
- Fix: record per scored step: right or wrong, reason right or wrong, confidence. Report first-try rate per
  unit and alarm under 70%.

### 2.3 `structures/INTEGRATED.md`

**F10. Major. The part template was narrowed so it never reaches this skill.**
- The review said: "any new idea inside any unit arrives in the part template: problem, fix, tiny example,
  picture, paths, about 5 questions" (`review.md:150`), from A12 80% vs A13 27% on the same day.
- INTEGRATED 2.8 keeps it only "where a step explains something" (`INTEGRATED.md:41-42`). The LLM steps
  never explain before asking, so the template is never triggered.
- Fix: restore the review's wording: every new idea arrives in the template before it is questioned.

**F11. Major. The "right reason" gate was promoted from trial to fixed bar.**
- The review marked the reason gate as a trial, "with the run in view", because of cold why-questions
  0 / 4 and Crouch's 30% explanation rate (`review.md:154`).
- INTEGRATED lists "right answer with a right one-line reason, on 2 different cases" as the fixed bar
  (`INTEGRATED.md:51`), and the engine enforces it on the pre-teaching item (F16).
- Fix: move the reason requirement to the trial column; score the answer, track the reason.

### 2.4 `.claude/skills/faiz-teach/SKILL.md`

**F12. Major. Wrong answers to the pre-teaching question get "one reframe, one hint".**
- `SKILL.md:51` applies to every step, including "Pick and say why", which comes before any teaching.
  The structure says the tutor "Logs all three; says nothing" at the first vote (`llm-behaviour.md:67`).
  A hint on an untaught rule produces guessing (ai-tutoring.md 1d; E7 6+ cases).
- Fix: pre-questions are never hinted; the next message gives the answer and the worked demonstration.

**F13. Blocker. The stuck order cannot run.**
- `SKILL.md:54-56`: step (0) "send the step's prepared simpler version (its Key's `Simpler:` block) before
  its question", then his earlier answer, two options, a picture.
- `hooks/teaching-guard.py:103-105` blocks any message containing "your answer" in which a Key line of 25+
  characters appears, so a Simpler block sent with its question is blocked. `:131-132` blocks re-sending a
  step already sent. `:118-119` blocks any "?" in feedback before a step, which rules out the "two options"
  move and the say-back after a given answer (C19).
- Also, `Simpler:` exists only for Explain and Wrong idea fixed (`01:84`, `:102`; `02:87`, `:106`;
  `03:85`, `:103`; `04:105`, `:123`). The scored steps, where he is most likely to stall, have none.
- Research: D8 (rebuilt part, 2 / 2), D1 (own earlier answer, 15 / 17), D4 (two options, 5 / 7), Khan's
  step hints ending in a worked solution (`teaching-craft.md:24`).
- Fix: move Simpler versions and the two-option rewording into the step body as a labelled
  "If stuck" block the guard recognises, write one for every scored step, and let the guard allow a
  re-send of the current step after stuck help.

**F14. Major. The expert explanation lives in the secret Key, so he never sees it.**
- `SKILL.md:29` "never show him ... Keys"; the guard enforces it (`teaching-guard.py:103-105`) and caps
  feedback at 400 characters (`:120-121`).
- In every unit, the only quoted expert explanation of the mechanism (Karpathy in `01:83`, Hugging Face
  and the OpenAI cookbook in `02:86`, Huyen in `03:84`, Anthropic in `04:104`) sits in the Explain Key.
  The structure says the tutor "Compares with the source's explanation, quoted and named"
  (`llm-behaviour.md:70`). Loibl and Kapur say consolidation is what makes the attempt pay off. Postmortem
  cause 4: expert material, prepared and checked, not improvised.
- Built: consolidation shrinks to 400 characters of tutor paraphrase.
- Fix: the source explanation goes in a step body (the worked demonstration), quoted and named. Keys
  keep only marking rules.

**F15. Minor. Small SKILL.md drift.** `SKILL.md:11` cites C1 to C46 (C47 to C49 exist). `:29-31` asks for his
score prediction before the first scored step, which is message 2, before he knows what the unit covers.
The Pick Keys say "Record the confidence" but no command records it. Fix: update the range; ask the
prediction after the worked demonstration; record confidence per step.

### 2.5 `learn/engine.py`, `learn/check_unit.py`, `hooks/teaching-guard.py`

**F16. Blocker. The pass rule grades the before-teaching question, with no hints allowed.**
- `engine.py:43-44`: LLM pass = "Pick and say why" right AND "New case" right. `SKILL.md:35-36`: right
  only after a hint counts 0.
- So a wrong first guess on an untaught mechanism fails the unit, however well he does afterwards. At the
  structure's own expected band (35 to 70% right first vote, `llm-behaviour.md:33`, `:256`), 30 to 65% of
  units fail by design. A failed unit is never served again (`engine.py:181-186`); no parallel LLM unit
  exists, so the track stops with "prepare a parallel unit". A confident wrong first vote counts as below
  the floor (`engine.py:154`), and two of those move him down a rung.
- Research: Kapur 2016 (do not judge by in-session failure during generation); structure `:75-78` uses
  the first vote for placement, and `:207` sets the concept bar on the **transfer** revote "twice in a
  row, on two different surfaces".
- Fix: `passes("llm")` = New case right (answer; reason tracked, see F11); mastery = that plus the Cold
  item at 7 days, which is the second surface. The pre-question is never in `scored:`.

**F17. Major. The checker enforces none of the teaching rules the research sets.**
- `check_unit.py:6-14`, `:153-186` check step names and order, `**Your answer.**`, a Key, a Score line,
  numbers traced to runs, prose under 2,500 characters per step, watchlist jargon, cards. C48's "How this
  code works" rule applies only when `skill == "code"` (`:164`).
- Not checked, though the research sets each one: a goal line in the first step (C34, C41;
  `teaching-structure.md:149`); a worked demonstration before the first scored step
  (`teaching-structure.md:151`; `skill-methods.md:118-125`); at most 3 new ideas per step, at most one new
  term per explanation (`teaching-craft.md:148`; B5); under 150 words before his first answer
  (`teaching-craft.md:157`); every rule a scored item or card needs appears in an earlier step body, not
  only in a Key (B6, E7); a "How this works" line under any output block with markup (`04:24-30`).
- Fix: add these as checks (section 3, item 6).

**F18. Major. The skip rule skips content that the Cold item and the cards test.**
- Every Pick Key says "right reason, confidence 4 or 5: go straight to New case" (`01:44`, `02:45`,
  `03:45`, `04:55`), which skips Predict, Run, Explain and Wrong idea fixed. Skipped steps count as right
  (`SKILL.md:35`).
- But `02:95` (digits are cut by a fixed rule) is taught only in the skipped Wrong idea fixed and is the
  right answer of the Cold item (`02:146`); `03:91-93` (a provider does not guarantee the same output at
  0) is taught only there and is the Cold answer (`03:137`); cards quote runs he never saw (`01:154`
  told-her 45.0%, `03:152`).
- Fix: Cold items and cards may use only content from steps that are never skipped; placement skips only
  the demonstration of a mechanism he already stated correctly, never a new fact.

**F19. Minor. The jargon gate has holes.** `docs/glossary.md` lists "token", "model" and "prompt" as taught,
so their explanation is never checked; "call", "training", "system", "chat template", "provider's servers",
"picking chances" are not on the watchlist. Fix: add them; mark a term taught only after he has been
taught it in a unit that passed.

### 2.6 The units, read as he receives them

Each row is one message. "New ideas" counts things he has not been taught before (from the ledger's
"Taught" list and earlier units). The research limit used is about 3 per step (his record B5: 1 new thing
80%, about 8 new things 0 answered twice; teaching-craft: at most one new term per explanation).

**llm-01, "Capital of Pakistan"**

| # | Step | New ideas | Problems |
|---|---|---|---|
| 1 | Odd result (`01:10-25`) | 8: a named demo model; "0.5 billion parts (numbers it learned in training)"; small vs large model effects; text sent "with no chat around it" so it "carries on the text"; token; a chance for every possible next piece; a top-five table; a fill-in blank line as a "piece"; the Q:/A: shape | No goal. First word he reads is `given:`. 219 words before his first answer (limit 150). "Training" and "no chat around it" used before explained |
| 2 | Pick and say why (`01:30-39`), **scored** | the mechanism itself, only inside option A | Graded before any teaching (F16). He is asked to recognise an explanation nobody has given |
| 3 | Predict (`01:46-54`) | 1 | A percentage with no data to base it on and no reason asked: a coin flip (teaching-methods 1d; C39) |
| 4 | Run (`01:59-71`) | 0 | Fine |
| 5 | Explain (`01:76-80`) | 0 in the question, but the answer is the untaught mechanism | Cold why-question; the Karpathy quote that answers it is in the Key (F14) |
| 6 | Wrong idea fixed (`01:86-98`) | 3: the right idea (first time it is stated plainly), "support assistant", "at risk" | First plain statement of the mechanism, in message 6. "Work it out" is 1,000 / 5, a read-back (C36). "Name one place in a real product" has no marking standard |
| 7 | New case (`01:104-116`), **scored** | 2: an answer is written one piece after another; "the likeliest next piece" | Tests a rule never taught in this unit: that a multi-piece answer is produced piece by piece with no check (the unit only showed one next-piece table). "Likeliest" assumes the temperature-0 rule from llm-03 (E7) |
| 8 | Close (`01:121-126`) | 0 | Fine |

**llm-02, "Strawberry and Urdu"**

| # | Step | New ideas | Problems |
|---|---|---|---|
| 1 | Odd result (`02:10-27`) | 8: tokenizer; tokens; "OpenAI's public o200k tokenizer (from the GPT-4o era)"; Qwen's tokenizer; two tokenizers cut differently; digits cut in groups; "strawberry" in pieces; letter counting fails; small-model effect | No goal. Two questions in one; "in which form does 'strawberry' reach the model?" is hard to parse for a novice |
| 2 | Pick and say why (`02:31-40`), **scored** | a chunk list built from lots of text (option D) | Graded before teaching; the frequency idea behind D was never shown |
| 3 | Predict (`02:47-55`) | 1 | Urdu token count with no basis (he has not been told why languages differ) |
| 4 | Run (`02:60-74`) | 1: Roman Urdu | Fine |
| 5 | Explain (`02:79-83`) | 0 | Cold why; HF and cookbook answer only in the Key |
| 6 | Wrong idea fixed (`02:89-101`) | 4: the fixed chunk list; rare text breaks into more; the digit rule ("groups of up to 3"); pay per token | Over the limit. The digit rule appears here once and is the Cold answer (F18). The Key adds Sonnet 4.6 vs 5 and "30% more tokens", which a card then tests (see F27) |
| 7 | New case (`02:108-120`), **scored** | 0 | Fine: the rarity rule was stated in step 6 |

**llm-03, "Same answer five times"**

| # | Step | New ideas | Problems |
|---|---|---|---|
| 1 | Odd result (`03:10-25`) | 5: temperature, "a setting that controls how the model picks from its chances" (circular: how it picks is never shown); temperature 0; a first-piece chance table; the model computes chances before writing; small-model effect | No goal |
| 2 | Pick and say why (`03:29-40`), **scored** | the "always takes its likeliest piece" rule, only inside option B | Graded before teaching on a rule he cannot work out alone (ai-tutoring 1d). Two questions in the step body |
| 3 | Predict (`03:47-54`) | 3: temperatures above 0; "App" as the start of "Apple" (23.4% + 49.9% = 73.3%); off-topic answers | Three answers in one step, none with data: what temperature does above 0 was never shown |
| 4 | Run (`03:58-72`) | 2: "no cut-off"; "services usually cut off the rarest pieces" (top-p) | A side idea not needed for this unit |
| 5 | Explain (`03:77-81`) | 0 | Cold why; the answer ("evens out the picking chances") and Huyen's quote are only in the Key |
| 6 | Wrong idea fixed (`03:87-99`) | 3: "picking chances" vs "model's chances" (used, never defined in the body); provider servers are not fully deterministic; checking against the truth | "Picking chances" is a new term with no definition in any step body; defined only in the Explain Key (`03:84`) |
| 7 | New case (`03:105-116`), **scored** | 0 | Right answer D needs "a high setting raises the picking chances of rare pieces", which no step body states (only the Explain Key and Simpler) (E7) |
| Cold | (`03:131-146`) | | Option D's rejection needs the two kinds of chances, never defined in a body |

**llm-04, "A name it was never told"**

| # | Step | New ideas | Problems |
|---|---|---|---|
| 1 | Odd result (`04:10-37`) | 6: "call"; chat software adds lines by itself; a system line; `<|im_start|>` / `<|im_end|>` markers; the roles system, user, assistant; a model inventing an answer | The output block has markup with no "How this works" line (C48 applies only to code units, F17). No goal |
| 2 | Pick and say why (`04:41-50`), **scored** | "each call starts fresh" (option D) | Graded before teaching |
| 3 | Predict (`04:57-78`) | 0 | The answer is in the text sent, so the outcome is near-certain and teaches nothing (flagged as `audit-units.md` #36, still unfixed). 13 lines to read for one number |
| 4 | Run (`04:82-93`) | 0 | Fine |
| 5 | Explain (`04:97-101`) | 0 | Asks how chat apps "seem to remember"; the answer (the app re-sends the whole chat) has never been said. Cold why |
| 6 | Wrong idea fixed (`04:107-119`) | 3: keeps nothing between calls; context window; re-sent text is paid again | At the limit; fine |
| 7 | New case (`04:125-136`), **scored** | 1: app "memory" features that store notes | The right answer relies on a product feature never mentioned (minor, partly inferable) |

Findings drawn from the tables:

**F20. Blocker. In all four units the first question comes before any teaching, and the mechanism is
first stated plainly in message 6 of 8.** Research: F5. His words: "you didn't show me a worked example,
you're overloading me immediately" (C49); "explain and teach me the concept ... before you test me" (C17,
broken 3 times before). Fix: section 4 template.

**F21. Major. Every opening carries 5 to 8 new ideas** (tables above). Research: teaching-craft "At most one
new term" (`teaching-craft.md:148`), "Several new ideas in one explanation" is avoided by the best
resources (`:233`); Math Academy knowledge points (`:37`); his B5. Fix: one mechanism per opening; move the
small-model caveat to the Run step where the odd result is shown; drop side ideas (top-p cut-off, GPT-4o era).

**F22. Major. No unit states its goal.** Research: goal card (`teaching-structure.md:149`); "Goal: what
problem this solves, in money or risk terms" first (`teaching-methods.md:158`); C34, C41 ("every unit
states its goal in its first step"); 3Blue1Brown's 30-second rule (`teaching-craft.md:32`). Built: the
first line is `given: the demo model is Qwen2.5-0.5B` in all four. Fix: first line "By the end you can
decide X. Why it matters: Y costs Z."

**F23. Major. Predict steps are guesses without data or reasons, or near-certain.** Research: "Backfires: if
the prediction is a coin flip with no reasoning ... Ask for the prediction and a one-line reason"
(`teaching-methods.md:58-60`); method-effectiveness row 15: "Weakens when coin-flip guesses"; C39 "if I'm
given all the data I need". Built: `01:52`, `02:53`, `03:51` ask for numbers he has no basis for; none asks
for a reason; `04:75` is near-certain. Fix: predict only after the mechanism is shown, on a new input where
the taught mechanism gives a direction, with a one-line reason.

**F24. Major. The Explain step is a cold why-question in every unit.** Research: F6; B10 cold
why-questions 0 / 4; ai-tutoring 1d. Fix: replace with a focused self-explanation prompt on the key line of
the worked demonstration ("In the table, which number moved when the wording changed?").

**F25. Major. The answer to the pick is withheld for four messages.** Research: method-effectiveness row 15
"answer shown at once"; "Weakens when ... answer delayed" (`method-effectiveness.md:68`); teaching-methods
1d "If the answer is never revealed quickly, the benefit is lost". Built: Pick at step 2, refutation at step
6. Fix: the answer opens the next message.

**F26. Major. Scored items test rules never stated in a step body.** llm-01 New case (piece-by-piece writing,
`01:112`); llm-03 New case (rare pieces gain picking chance, `03:114`); llm-03 Cold option D (two kinds of
chances). Research: B6, E7 (6+ misses traced to rules never said); ai-tutoring 1d; `method-effectiveness.md:180`
4d "Not allowed: new items that test untaught rules". Fix: state each rule in the worked demonstration;
checker rule in F17.

**F27. Major. Cards test content he was never shown.** llm-02 card 5 first variant (Sonnet 4.6 to Sonnet 5,
30% more tokens, about $867, `02:160`) exists only in a Key (`02:105`); llm-01 card 4 ("retrieval",
`01:156`) only in a Key (`01:101`); llm-03 card 1 uses "picking chances", defined only in a Key. Research:
Wozniak rule 1, "understand before memorizing", adopted as card rule 1 (`llm-behaviour.md:215`). Fix: every
card answer must appear in a step body that is always sent.

**F28. Major. No everyday picture in any unit.** Research: B2 and D2 (8 / 10 as stuck help); T24 "Short
analogy with a break point", with a temperature example (`teaching-craft.md:128`); the structure allows
"autocomplete trained on the internet" (`llm-behaviour.md:81-83`); Karpathy's own pictures: "glorified
autocomplete", "biased coin". Fix: one picture per mechanism, one sentence plus where it breaks.

**F29. Major. Expert explanations exist in the base but are not used; the explanations are Claude-written.**
`curriculum-map.md:33` and M1 (`:69`) name ScaleDojo GenAI modules 2 and 3 and HF LLM Course chapter 1 as the
primary reading; `recommended-method.md:75` says ScaleDojo chapters are "read after his first attempt, as
the explanation". Saved and unused: `private/scaledojo/learn/genai/tokens-embeddings-and-memory/how-llms-see-text-tokenization.md`,
`.../prompting-and-model-behavior/temperature-and-sampling-controls.md`,
`.../tokens-embeddings-and-memory/conversation-memory-and-context-windows.md`,
`.../prompting-and-model-behavior/the-economics-of-llm-calls-tokens-and-pricing.md`. No unit lists them in
`sources:`. Postmortem cause 4 and `curriculum-map.md` Part 3: "Worked examples come from experts, not from
Claude". Fix: build each worked demonstration from one named source passage plus the real run.

**F30. Minor. Options come first on every scored item.** Research: method-effectiveness row 1b rule "short
answer or free recall first, then the options as a check" (`method-effectiveness.md:49`, `:125`). The
review kept ConcepTest options first on purpose because his direction questions went 0 / 3 open to 3 / 3
with two options (`review.md:134`, E12). Fix: keep options for direction questions; for "why" items, ask a
one-line answer first and show options only if he stalls (this is also the stuck order's "two options").

**F31. Minor. Machine markup and repetition in what he reads.** Each unit opens with the literal checker
prefix `given:` and the same two-sentence caveat (`01:12`, `02:12`, `03:12`, `04:12`). C27: "i just don't
like repitition". Fix: let the checker read `given:` lines but strip the prefix before sending; state the
caveat once in llm-01 and then only the unit-specific line.

**F32. Minor. "What it costs" is mostly read-back arithmetic.** `01:96` (1,000 / 5), `03:97` (5% of 1,000).
C36 asked for questions that "improve my understanding". Fix: ask for the decision the number drives (for
example, "which is cheaper per month: re-sending the chat or a 300-token summary, and what does the summary
risk?").

**F33. Minor. One question per message.** His record resolved to "one part, one new idea, about 5 questions,
per message" (learning-evidence contradiction 2; B9: 1 question per message 87% but "too slow"). INTEGRATED
2.8 chose one step per message. Fix: after the worked demonstration, group 2 or 3 short checks on it in one
message.

**F34. Major. Terms used before they are explained** (C1 broken 5 times, C33):
- "training" (`01:12`, `01:34`), "no chat around it" (`01:14`), "token" in llm-01 before llm-02 (`01:14`).
- "o200k", "GPT-4o era" (`02:14`).
- "temperature" defined circularly as how the model "picks from its chances" (`03:14`); "picking chances"
  and "model's chances" (`03:93`) never defined in a step body; "cut-off" (`03:68`); "provider's servers"
  and "deterministic" by quotation only (`03:91`).
- `<|im_start|>`, `<|im_end|>`, "system", "user", "assistant" (`04:25-30`); "chat software" (`04:22`).
- "retrieval" (Key and card only, `01:101`, `01:156`).

**F35. Minor. Questions a novice could not parse or mark:**
- `02:24` "in which form does 'strawberry' reach the model?" (what counts as a "form"?).
- `01:96` "name one place in a real product where that would matter most" (no standard for marking).
- `03:51` three predictions in one step, one of them "Will the answers at 1.5 all be real fruit?" with no
  way to reason about it yet.
- `03:49` "App 23.4% (most likely the start of Apple too; together 73.3%)": sub-word arithmetic inside a
  prediction prompt.
- `04:99` "how does a chat app make the model seem to remember what you said five messages ago?" (untaught).

---

## 3. Prioritised fixes

Do these in order; 1 to 4 unblock teaching, 5 to 7 bring the units to the research standard.

1. **Stop grading the pre-teaching question** (F16, F12). `engine.py:43-44`: LLM pass = New case right;
   mastery = New case plus the Cold item at 7 days (two surfaces, `llm-behaviour.md:207`). Remove "Pick and
   say why" from every `scored:` line. No hints on a pre-question.
2. **Put the worked demonstration before the first scored question, in every unit** (F5, F20, F24, F25,
   F26). Rewrite llm-01 to 04 to the template in section 4: goal, optional pre-question, then the answer and
   the mechanism shown on the real run, quoted from a named source, with one picture; checks after that.
3. **Correct the Chen 2015 citation everywhere** (F1, F2) and change "No worked example" in
   `llm-behaviour.md:92`, `recommended-method.md:65`, `method-effectiveness.md:122`, `:156`,
   `skill-methods.md:114`, `:244`, `:255`, `curriculum-map.md:33`, `review.md:130` to: "Mechanisms: worked
   demonstration first (novice); facts: taught once, then retrieval cards".
4. **Make stuck help and consolidation deliverable** (F13, F14). Move each unit's source explanation and
   its Simpler and two-option versions out of the Key into step bodies; teach the guard to allow a labelled
   "If stuck" block and a re-send of the current step; allow one question mark in stuck help.
5. **Cut every step to 3 new ideas or fewer and add a goal line** (F21, F22, F31, F34). Strip `given:`
   before sending.
6. **Add research checks to `check_unit.py`** (F17, F18, F26, F27): goal sentence in step 1; a
   demonstration step before the first scored step; new-term count per step against the glossary (warn
   above 3); words before the first question (warn above 150); every scored Key's answer terms and every
   card answer found in a non-skippable step body; Cold and cards may not depend on skippable steps;
   "How this works" under any output block with markup.
7. **Use the saved expert chapters** (F29, F7, F28): llm-02 from the ScaleDojo tokenization chapter and HF
   ch. 2; llm-03 from Huyen's [1, 3] worked table plus the ScaleDojo temperature chapter; llm-04 from the
   ScaleDojo context-window chapter and Anthropic's context-window page; one picture per unit.
8. **Record what the structure measures** (F9, F15): per scored step, answer right, reason right,
   confidence; first-try rate per unit with an alarm under 70%.
9. **Minor clean-ups** (F4, F8, F19, F30, F32, F33, F35): save and quote Crouch and Mazur 2001; fix the
   concept order or define "piece" in llm-01; widen the watchlist; short answer first on why-items; decision
   questions instead of read-backs; group 2 or 3 checks after the demonstration; rewrite the five questions
   in F35.

---

## 4. Corrected unit step template for LLM behaviour

Built only from the research base. Each step names its source. One mechanism per unit. Each numbered item
is one message. Nothing below adds a new method; it restores the order the named experts use.

| # | Step (plain name) | What he receives | Rules | Source |
|---|---|---|---|---|
| 1 | **Goal and odd result** | One line: what he will be able to decide by the end, and why it costs money or risk. Then one real odd result from a run: two contrasting rows that differ in one thing. Then **one** pre-question on the core idea: two options or a one-line answer, plus a one-line reason. | At most 3 new ideas, each explained in the sentence where it first appears. Under 150 words before the question. Not scored, no confidence, no hints. Skip the pre-question when he has no intuitive idea to use (for example, temperature). | Goal card `teaching-structure.md:149`; full context `teaching-methods.md:156-163`; contrasting cases Loibl 2017; pre-questions g = 0.66 `teaching-methods.md:170`; PF prior-knowledge condition Loibl 1266-1270 |
| 2 | **How it works (worked demonstration)** | Opens with the answer to the pre-question and one line on the option he chose (prepared for each option). Then the mechanism in 3 to 5 lines, quoted or closely adapted from a **named** expert source, shown on the same real run with its numbers (a table, and a sweep across one setting where there is one). One everyday picture in one sentence, plus where it breaks. Ends with one focused self-explanation question on the key line of the table, answerable from what is on screen. | Under 250 words of explanation. No new idea that is not needed for the checks below. The picture must not plant the category mistake ("a brain", "a search engine" are not allowed). | Karpathy deep dive (explain, then show) lines 43-47, 61, 95; skill-methods C2 claim and why `:118-125`; Kapur consolidation (compare his answer, then the canonical one) chapter line 300; teaching-craft T4, T8, T9, T24; self-explanation on the key step, method-effectiveness row 8 |
| 3 | **Predict** | A new input where the mechanism just taught gives a direction. All data he needs is given. He writes a direction, a rough number and a one-line reason. | The outcome must be uncertain enough to be worth predicting, and derivable from step 2. Not scored. | teaching-methods 1d `:56-60`; method-effectiveness row 15; C39 |
| 4 | **Run and compare** | The real output at once. He says how far off he was and which part of the step 2 mechanism explains the gap (short answer). Small-model caveat here, one line, only if this result is a small-model effect. | Answer shown in this message, not later. | method-effectiveness row 15 ("answer shown at once"); structure recorded-output rule `llm-behaviour.md:85-86` |
| 5 | **Wrong idea fixed** | Refutation: the wrong idea, "this is wrong", why (his run as evidence), the right idea in the words used in step 2, then one decision priced at scale that he works out (not a read-back). | Only ideas already taught in steps 2 to 4. | Refutation text g = 0.41 `teaching-methods.md:151-154`; Posner (pay-off) `llm-behaviour.md:37`; T21 price at scale |
| 6 | **Checks** | 2 or 3 short questions in one message on the same mechanism with new surfaces: one direction question (two options), one "why" with a one-line answer first, options only if he stalls. | Every rule needed is in a step body above. About 80% first-try is the working target (A9, A12). | Retrieval with feedback, method-effectiveness row 1 and 1b; B9; E12 (two options for direction) |
| 7 | **New case (scored)** | A transfer item on a new surface: a real failure or product situation. One-line answer and reason, then his confidence. | The only scored step in the session. Stuck order applies: his own earlier answer, two options, one picture, then the answer with a reason; a hinted answer is marked as hinted. | Butler 2010 transfer `llm-behaviour.md:45`; bar on transfer `llm-behaviour.md:207`; stuck order `INTEGRATED.md:32-33` |
| 8 | **Close** | "Next time I see X, I do Y." Goes into the recall queue. | Not scored. | `INTEGRATED.md:21-22` |
| Cold | **7-day cold item** | A new surface of the same mechanism, same format as step 7. | Only content from steps that are always sent. | mastery with delayed recheck, method-effectiveness row 7 |
| Cards | **Cards** | 4 to 6, each answer found word for word in a step body; at least one why card and one boundary card; dated facts carry date and source. | First return next day. | Card rules `llm-behaviour.md:214-225`; Wozniak rule 1 |

**Placement (replaces the old skip rule).** If his pre-question answer and reason are right, he still gets
step 2 (it carries the facts the checks and cards use), but steps 3 and 4 may be skipped. After two units
of a level passed cold, the next unit may open with the step 7 item as a first-step test; right with a
right reason goes straight to step 5 (Kalyuga first-step test, `skill-methods.md:238-239`).

**Scoring.** Scored: step 7 and the Cold item only. Tracked but not gating: pre-question answer, reason
quality, confidence, first-try rate per step (for the 70% alarm in F9).

**Stuck help.** Stored in the step body under a fixed label, one per question: a simpler rewording, a
two-option version, one picture. Never a longer re-explanation (D6, 0 / 5).
