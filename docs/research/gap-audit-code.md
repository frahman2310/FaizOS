# Gap audit: how the code track dropped what its own research says

Written 2026-09-25, after the voided first code session (C49). The question is not "what do experts do"
(the research base already says that) but "where did the build stop doing it". Each expert practice
recorded in the research base is traced through the chain:

research base (`docs/research/recommended-method.md`, `curricula/*.md`, `private/research-base/`) →
design (`structures/code.md`) → spec (`structures/INTEGRATED.md`) → rulebook (`.claude/skills/faiz-teach/SKILL.md`)
→ machinery (`learn/engine.py`, `learn/check_unit.py`, `hooks/teaching-guard.py`) → units (`learn/units/code/0*.md`).

The companion file `curricula/code-teaching-experts-v2.md` holds the expert practice in full, the corrected
unit template and a worked sample of the first unit. Grades: **strong** (replicated or meta-analytic),
**moderate** (consistent studies or large platform practice), **weak** (one study or stated practice).

## The one-paragraph answer

The research base says, in four separate files, that a novice meets a new code pattern as a **worked
example he studies first**, with one self-explanation prompt, then a **completion problem with the last
steps blank**, and only from the third problem attempts on his own. The code design replaced this with
PRIMM's "Predict" as step 1 and a full blank memory table as step 2, and the machinery then made the
worked example impossible to send: every step must end in a question, and every step is sent verbatim
with nothing added. The session failed exactly where the research predicted: a question on code he had
not been taught, then a 40-cell table with no model shown.

## Where it was lost, in one table

| # | Expert practice (research base file) | Grade | Design `code.md` | Spec `INTEGRATED.md` | Rulebook `SKILL.md` | Machinery | Units |
|---|---|---|---|---|---|---|---|
| 1 | Worked example studied before any practice | strong | dropped (step 3 "Trace" is a task, not a study step) | dropped (line 15) | named (C45, l.17) but no procedure | impossible (check_unit l.26, l.155) | none |
| 2 | Teacher models, thinks aloud, before learners try | strong | dropped | dropped | contradicted (l.30 to 34) | impossible (guard: verbatim step only) | none |
| 3 | No question on an untaught rule | moderate | contradicted (l.75) | contradicted (l.30) | silent | not checked | contradicted (all 4 Predict steps) |
| 4 | First two problems of a type are worked; attempt first only from the third | moderate | contradicted | contradicted (l.30 "Commit first") | silent | not checked | contradicted |
| 5 | Backward fading: completion before full problems | moderate | dropped | dropped | silent | not checked | contradicted (full blank tables) |
| 6 | Tracing technique taught by modelling first | moderate | misread (l.40 to 43) | 90% of blank cells is the bar (l.50) | silent | bar enforced (engine l.15, l.41) | contradicted |
| 7 | One self-explanation prompt on the key step | strong | dropped | dropped | silent | not checked | absent |
| 8 | Small steps, one new element at a time | strong | kept in words | kept (l.42) | kept in words (l.60) | glossary words only | contradicted (5+ new rules per Trace) |
| 9 | Subgoal labels shown first, then examples, then practice with a reference sheet | moderate | kept in words (l.38) | silent | silent | not checked | labels only as comments inside question code |
| 10 | Correct examples before erroneous ones for true novices | moderate | contradicted (bug items in unit 1) | silent | silent | not checked | contradicted (code-02 Predict is a bug) |
| 11 | Placement by a 90-second first-step test | moderate | kept in words (l.85) | silent | silent | not built | absent |
| 12 | Tiny generic example first, then the real case | moderate (his record B1) | kept only as a failure fallback | silent | "Simpler" after failure (l.54) | not checked | "Simpler" in Keys only |
| 13 | ~80% success during guided practice | moderate | silent | silent | silent | not measured | first items built to be missed |
| 14 | Formative check: short, one concept, distractors that diagnose | moderate | partly (label items) | silent | silent | not checked | Predict is predict plus classify, scored |
| 15 | Every term explained where first used | his rule C1, C49 | kept | kept (l.42) | kept (l.60) | weakened: house words count as taught | "sticker", "machine", "slot" unexplained |
| 16 | Spaced, interleaved review | strong | kept | kept | kept | kept (FSRS) | kept (cards) |
| 17 | Feedback that explains, at most 3 points, stuck order | strong | kept | kept | kept | n/a | kept |
| 18 | Every output from a real run | his rule | kept | kept | kept | kept | kept |

Rows 16 to 18 survived intact. Rows 1 to 15 are the findings below.

---

## Findings

### G1. The worked example step does not exist anywhere in the code chain (blocker)

- **Research says.** `recommended-method.md` l.46: step 4 is "Worked example: an expert's solution showing
  the reason at every decision ... he writes one line explaining the key step". `curricula/skill-methods.md`
  section C: "Common ladder ... 1 study a worked example → 2 completion problem (last steps blank) → 3 faded
  example ... 4 independent problem". C5 gives the anatomy of a code worked example (goal, code with
  subgoal labels, trace table, why each block, the check, wrong turns) and its ladder starts "Worked example
  → predict the output before running". `method-effectiveness.md` 4a: minutes 5 to 13 are "worked example
  with one focused why on the key step (new type)". External: Rosenshine's most effective teachers spent
  about 23 of 40 minutes presenting and working examples, the least effective 11
  ([Rosenshine 2012, American Educator](https://www.aft.org/sites/default/files/Rosenshine.pdf), principle 2);
  worked examples g = 0.48 (`method-effectiveness.md` row 3). Grade: strong.
- **Built instead.** `structures/code.md` l.72 to 80: Warm reps, Predict, Trace, Explain, Change, Break,
  Steer. Step 3 is called "the real 15 to 30 line worked example", but what the learner does in it is fill a
  memory table: it is a problem, not an example. `INTEGRATED.md` l.15: "Predict, Trace, Change, Find the bug,
  Tell the AI". `check_unit.py` l.26 fixes those steps and rejects any other.
  `learn/units/code/01` to `04`: no step shows a solved example before asking.
- **Fix.** Add a study step ("Show") before any Predict or Trace, in the design, the spec, the
  checker's step list and every unit. Template in `code-teaching-experts-v2.md` section (e).

### G2. The machinery makes modelling impossible (blocker)

- **Research says.** Rosenshine principle 3: model and think aloud; "the teacher modeled and thought
  aloud" before students practised each step (same source). PRIMM's own theory: "Students need teachers,
  as More Knowledgeable Others, to show them (model)" (`private/research-base/code/research/sentance-2019-primm.md`
  l.360). Khan Academy: "After a student watches a talkthrough, we encourage them to start a challenge"
  ([Khan Academy CS blog, 2013](https://cs-blog.khanacademy.org/2013/08/introducing-programming-challenges.html)).
  Grade: strong for modelling in general, moderate for code specifically.
- **Built instead.** `check_unit.py` l.155 to 156: every step "must end with **Your answer.**", so a step
  that only shows and explains fails the check. `SKILL.md` l.30 to 34: "Send each `## Step:` verbatim, one
  step per message, with nothing after it", and the Stop hook (`hooks/teaching-guard.py`) blocks any other
  text. Together these forbid the tutor from modelling anything that is not already inside a question.
- **Fix.** Allow a `## Show:` block type (worked example plus one self-explanation prompt), checked like a
  step (code from a run, "How this code works" present, terms explained) but scored never. The guard
  accepts it verbatim like a step.

### G3. The first question is on code that was never taught, and it is scored (blocker)

- **Research says.** `curricula/ai-tutoring.md` 4b.4: "Never withhold a fact or rule ... A question built
  on an untaught rule is not productive struggle; it is a guess." The craft standard's own predict-first
  rule has the exception "Skipped only for untaught facts" (`curricula/teaching-craft.md` l.143). His record
  E7: "A rule never stated, then tested", 6+ times; cold why-questions 0 of 4. PRIMM's Predict is on code
  the class has been taught to read, and "shouldn't be an assessed exercise" and must be "low stakes"
  ([Raspberry Pi Foundation, Pedagogy Quick Read: PRIMM](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf)).
  A PRIMM teacher asked for "an introduction section with vocabulary and the basics and then starting PRIMM"
  (`sentance-2019-primm.md` l.1292). Grade: moderate.
- **Built instead.** `code.md` l.75: step 2 Predict is the first teaching step, output plus a crash / quiet /
  fine label. Every unit header: `scored: Predict, ...` (code-01 to 04, l.8). code-01 l.11 to 46 asks him to
  predict a `KeyError` from a dict lookup inside a function before dicts, lookups, functions or KeyError are
  shown in the unit. code-02 l.11 opens on a planted E2 bug before loops are shown.
- **Fix.** Predict moves after the worked example, on a program of the same shape, and is never scored.
  Crash / quiet / fine labels are taught with an example of each before they are asked.

### G4. The judgement-skill "commit first" frame was applied to code novices (major)

- **Research says.** `method-effectiveness.md` section 3, conflict "Worked examples vs productive failure":
  "First two problems of a new type: worked example. From the third: he attempts first." Loibl, Roll and
  Rummel's review: problem solving before instruction has "no clear benefits for procedural knowledge"
  (`private/research-base/learning-methods/loibl-roll-rummel-2017-when-problem-solving-first.md` l.1223),
  and it works only with contrasting cases or instruction built on student solutions (abstract). Kirschner,
  Sweller and Clark: minimal guidance is less effective for novices (local copy
  `kirschner-sweller-clark-2006-minimal-guidance.md`; restated in Wilson's
  [Teaching Tech Together](https://teachtogether.tech/en/index.html), chapter 4). Grade: strong.
- **Built instead.** `INTEGRATED.md` l.30 to 31: "One frame inside every unit. Commit (his answer first,
  with a reason), Check, Compare, Close", for all five skills. Code inherited attempt-first for every unit,
  including the first unit of every pattern.
- **Fix.** INTEGRATED 2.3 gets one clause: for a new pattern in code (and production, evaluation method),
  the frame starts with Study; Commit applies from the third problem of that pattern.

### G5. No backward fading: the first practice is a full problem (major)

- **Research says.** Renkl and Atkinson: fade the last solution step first, then the last two
  (`private/research-base/learning-methods/renkl-2002-smooth-transitions-fading.md` l.1855 to 1857; backward
  fading drives transfer, `recommended-method.md` l.47). Wilson's faded example: a full solution, then the
  same kind with some blanks, then more blanks, then the whole problem
  ([Teaching Tech Together](https://teachtogether.tech/en/index.html), chapter 4, "Faded Examples"). His record
  D5: a step table of working code with **the last cells blank** 3 of 4. Grade: moderate.
- **Built instead.** code-01 l.82: "Fill every cell" of an 8-column, 5-row table (40 cells, all blank) as
  his first contact with the program. Same in 02 l.86, 03 l.90, 04 l.91.
- **Fix.** Tables go: fully filled and talked through (Show) → last row blank → last two rows blank →
  all blank on a new program (independent). Scored only at the last stage.

### G6. Tracing tables were required before tracing was taught (major)

- **Research says.** Xie et al. taught the memory-table strategy in the introduction, explaining how code
  runs "one line at a time from top to bottom, left to right", before any tracing practice
  (`private/research-base/code/research/xie-2019-theory-of-instruction.md` l.614 to 623, l.664). PLTutor
  shows the machine stepping and "interleave[s] conceptual instruction about semantics throughout the
  program's execution" before hiding values (`nelson-2017-pltutor-comprehension-first.md` l.382). Cunningham
  et al. conclude that "all students should be taught a tracing sketch technique"
  ([Cunningham et al. 2017, ICER](https://www.gvu.gatech.edu/sites/default/files/related_project_files/p164-cunningham.pdf),
  discussion section). Grade: moderate.
- **Built instead.** `code.md` l.40 to 42 turned these into "He always traces with a memory table", "The
  trace table must be complete; half tables are marked incomplete", "Trace items hide values; he fills
  them". code-01 l.113: "a blank cell is wrong, as a half table is as weak as none: Cunningham". The
  Cunningham finding is observational, about students' **own** half-finished sketches after a CS1 course; it
  says nothing about handing a novice a large blank table. The same paper found that on a code-ordering problem
  only 3% sketched and both groups scored about 97% (section 5.3.2): a table is a tool for hard tracing, not a
  default task.
- **Fix.** Teach the table in a Show step on a 3-line program, filled by the tutor, one row per line, with
  a think-aloud sentence per row. Only then faded tables. Drop "blank cell is wrong" from Keys until the
  independent stage.

### G7. Sorva was used to forbid showing the machine (major)

- **Research says.** Sorva's point (cited at `code.md` l.43) is that learners gain when they engage with a
  visualisation, not when they watch passively. PLTutor, which `code.md` also cites, shows every state
  change with explanation first (G6). Carpentries live coding: the instructor explains every line while the
  learner follows ([Nederbragt et al. 2020, PLOS Comp Bio](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1008090)).
  Grade: moderate.
- **Built instead.** `code.md` l.43 "no watch-only animations" and l.235 "the memory table does that" became
  a rule that he always fills tables himself and never sees one filled first.
- **Fix.** A shown table plus a self-explanation prompt (G8) is engagement, not passive watching. Keep the
  ban on long unprompted animations only.

### G8. No self-explanation prompt on any example (major)

- **Research says.** Self-explanation prompts g = 0.55 (`method-effectiveness.md` row 8); "Ask for the
  reason on the key step only, and aim it at a target" (`ai-tutoring.md` 4c.1); the worked-example step
  ends "he writes one line explaining the key step" (`recommended-method.md` l.46). Grade: strong.
- **Built instead.** None: there are no examples to explain. The nearest item, code-01 Trace Q4 ("what is
  `call` for?"), is unscored and comes after a 40-cell table.
- **Fix.** Every Show ends with one targeted prompt ("Why does the second print show curly brackets?").

### G9. Five or more new rules per step (major)

- **Research says.** Rosenshine principle 2: "Only present small amounts of new material at any time".
  Craft standard item 5: "At most one new term" per part (`teaching-craft.md` l.148). Math Academy splits a
  lesson into 3 to 4 knowledge points, each one worked example then 2 to 5 questions (`skill-methods.md` B).
  Element interactivity decides whether examples or generation help (Chen, Kalyuga, Sweller 2015, local
  `chen-kalyuga-sweller-2015-element-interactivity.md`). His record A11: about 8 new things at once, 0
  answered. Grade: strong.
- **Built instead.** code-01 Trace introduces a stand-in provider, `time.time()`, `round(..., -2)`, a log
  passed into a function, a record dict, and a dict inside a dict (`rate`). code-02 Trace (l.40 to 84)
  introduces `pop(0)`, `raise`, `try`/`except ... as err`, `return` inside a loop and `RuntimeError` in one
  32-line program. The checker counts only glossary words, not new constructs (`check_unit.py` l.137 to 150).
- **Fix.** One new construct per knowledge point. Add a `new:` header line listing the constructs a unit
  introduces; the checker fails a unit with more than 3, and fails any Show that uses a construct not
  in `new:` or in a taught list.

### G10. House words counted as taught, so they were never explained (major)

- **Research says.** His rule C1 and C49: every term explained where it first appears; CS50P uses the real
  terms from the first lecture ("A variable is just a container for a value",
  `private/research-base/code/cs50p/notes/lecture-0.md` l.66). Grade: his stated rule.
- **Built instead.** `docs/glossary.md` l.9 to 11 lists "sticker", "machine", "slot" as Taught, so
  `check_unit.py` l.141 to 142 skips them. He said the word "sticker" was never explained.
- **Fix.** Move the house words out of Taught. Use the real words (variable, function, argument, return
  value, dict, key) because the goal is reading real code and real docs; explain each in the sentence where
  it first appears in each unit until he has passed a cold card on it.

### G11. "How this code works" describes code; it does not model reading it (major)

- **Research says.** CS50P builds each program one change at a time and runs it after each change
  (lecture 0 l.40 to 80: `print`, then `input`, then a variable, then the bug `print("hello, name")`); for
  API replies Malan prints the whole JSON, admits "it can be quite dizzying", pretty-prints it, then pulls one
  key (lecture 4 l.226 to 263). Khan talk-throughs have the instructor type and talk while the result
  appears. Grade: moderate.
- **Built instead.** C48 was implemented as a paragraph above a question (`SKILL.md` l.62; `check_unit.py`
  l.164 to 165), which summarises the whole program at once.
- **Fix.** In a Show, the explanation follows the code line by line in run order, naming the value each
  line leaves behind, and shows the output after each small change.

### G12. The tiny generic example exists only as a failure fallback (major)

- **Research says.** `ai-tutoring.md` 4a.3: "Tiny and generic first, then the real case (B1: 78 to 80% with
  it, 27% without)". His record B1 calls it the "strongest single predictor seen". Grade: moderate (his own
  data, repeated).
- **Built instead.** `SKILL.md` l.54 to 55: stuck step (0) sends "the step's prepared simpler version" only
  after he fails. The simpler programs sit in the Keys (code-01 l.115, 02 l.119, 03 l.125, 04 l.125).
- **Fix.** The simpler program becomes the first Show. The only unit that already does this is code-04
  (l.13 to 21: "Two rules first ... A tiny example"), which should be the pattern for all.

### G13. Subgoal labels were never presented as labels (moderate)

- **Research says.** The CS1 Subgoals project: present the labels before or right after explaining the
  concept, then one or more labelled worked examples, then practice with a reference sheet of the labels.
  "We highly encourage you to either present the worked examples in class"; when students were told to watch
  them alone, "many students completely skip" them
  (`private/research-base/code/research/subgoals-how-do-i-use-subgoals.md`). Grade: moderate.
- **Built instead.** After audit finding 18 the labels were added as comments inside the Trace code, which
  is itself a question.
- **Fix.** The labels open the unit as a short list (the pattern's steps), sit on the Show example, and are
  repeated as a reference line under every practice item.

### G14. Bug-finding and broken code came before any correct example (moderate)

- **Research says.** Learners with no prior knowledge did better on correct examples only; wrong examples
  helped learners with a little knowledge (Große and Renkl 2007, `skill-methods.md` A2). `skill-methods.md`
  C5 ladder: "find the bug (after 2 correct examples)". His record B11: simulating broken code in a table 0
  of 4; a label only, 5 of 6. Grade: moderate.
- **Built instead.** code-01 has Find the bug as its fourth step; code-02 Predict is itself a planted bug
  (l.11 to 38).
- **Fix.** Planted bugs only after two correct worked examples of the same pattern, and first as a
  label-only item, labelled as broken before it is shown (craft item 11).

### G15. The placement test is described but not built (moderate)

- **Research says.** A 90-second first-step test decides whether to show the worked example (Kalyuga 2007,
  local `kalyuga-2007-expertise-reversal-rapid-assessment.md`; `skill-methods.md` D2). Grade: moderate.
- **Built instead.** `code.md` l.85 describes it; `code.md` l.135 assumes his bootcamp covered T1 to T3 and
  starts him at level 1 on T2; units have no first-step item; `engine.py` only lists a per-skill
  "placement check before the first unit". Nothing decided that code-01 could skip teaching.
- **Fix.** Each unit gets a `## First step` item. After C49 his placement on T1 is "not yet": start at Show.

### G16. The mastery bar rewards the blank table, not independent skill (moderate)

- **Research says.** Rosenshine principle 7: a success rate of about 80% during guided practice; mastery
  bars 90% plus on the check with retest on new items (`method-effectiveness.md` row 7). Grade: moderate.
- **Built instead.** `INTEGRATED.md` l.50 and `engine.py` l.15, l.41 to 42: pass = 90% of trace cells in the
  unit's own table, plus the Change test.
- **Fix.** Guided items are unscored with a target of about 80% right first time (alarm if lower: the steps
  are too big). The pass bar applies only to the independent item and the 7-day cold item.

### G17. The first formative checks are not diagnostic (moderate)

- **Research says.** Wiliam's hinge questions take "no more than two minutes to respond", and are built so
  that "students with the right thinking and those with the wrong thinking give different answers"
  ([Wiliam, ASCD](https://www.ascd.org/el/articles/designing-great-hinge-questions)). Wilson: a one- or
  two-minute check every 10 to 15 minutes ([Teaching Tech Together](https://teachtogether.tech/en/index.html),
  chapter 2). Short answer first, then options with an explanation per option (`method-effectiveness.md` 1b).
  Grade: moderate.
- **Built instead.** The first check is a scored predict-plus-classify on two lines; the second is a 40-cell
  table plus three questions, about 10 minutes of work in one message.
- **Fix.** After each Show, one hinge item whose options each map to a named wrong idea (E4: "the whole
  dict" vs "the value"; "the key's name"; "KeyError").

### G18. The earlier audit pushed the tables the wrong way (minor, but it compounded G5 and G6)

- `docs/research/audit-units.md` finding 17 asked for more columns ("add the missing columns") on
  Cunningham's grounds. That made the first practice larger. Withdraw it: the full table belongs to the
  independent stage only.

### G19. The design misread his own record (minor)

- `code.md` l.59 to 60 cites "step tables of working code 3 of 4 (D5)" as support for full memory tables.
  D5 is a table **with the last cells blank**, which is backward fading. The same paragraph notes "simulating
  broken code in a table 0 of 4 (B11)", which should have kept planted bugs out of tables.

### G20. The rulebook's freeze blocked the fix (process)

- `SKILL.md` l.73 to 77 defers any format or step-order change for 8 weeks. The missing worked example was a
  build error against the research, not a trial to measure; it needed C49's explicit override to fix. Add:
  "a step that the research base requires and the build omitted is a defect, fixed at once, not a format
  change".

---

## Fix list, in the order to do it

1. `check_unit.py`: add `Show` blocks (no question, never scored); step list for code becomes
   First step, Show, Try with me, Check, Your turn, Close (then Change, Find the bug, Tell the AI in later
   units of a pattern); add the `new:` construct cap (G1, G2, G9).
2. `hooks/teaching-guard.py`: accept a Show block verbatim like a step (G2).
3. `SKILL.md`: session order "Show → Try with me → Check → Your turn"; Predict only after a Show; guided
   items unscored; the Simpler program is the first Show, not a fallback; add the defect rule (G3, G12, G20).
4. `INTEGRATED.md` 2.3 and section 3: Study before Commit for a new pattern; code bar on independent and
   cold items only (G4, G16).
5. `engine.py`: pass rule reads `Your turn` and `Cold`, not `Trace` cells (G16).
6. `docs/glossary.md`: remove sticker, machine, slot from Taught (G10).
7. `structures/code.md`: rewrite section 2 to the template in `code-teaching-experts-v2.md` (e); correct the
   Cunningham, Sorva and D5 readings (G6, G7, G19).
8. Rebuild code-01 to code-04 from the template; each current unit splits into two or three (G9).

Evidence limits: no study tests this sequence with one adult learning to read AI-engineering code from an AI
tutor. The sequence rests on classroom and lab research (Rosenshine, Renkl, Xie, Margulieux) plus his own
record, which points the same way (B1, D5, B11, E7, A11).
