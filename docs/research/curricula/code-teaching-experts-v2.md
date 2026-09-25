# How experts teach a new piece of code to a novice, and the unit Faiz should get

Written 2026-09-25 after the voided first code session (C49). Plain English; every claim names its source.
Local sources are in `private/research-base/` (private study copies); web sources are linked. Quotes are
under 15 words. Grades: **strong** (replicated or meta-analytic), **moderate** (consistent studies or large
platform practice), **weak** (one study or one program's stated practice).

The gap audit that traces each practice through the design, rulebook, machinery and units is
`docs/research/gap-audit-code.md` (findings G1 to G20). Section (d) here is its summary.

What this file does **not** cover, because it was not researched this pass: MIT 6.100L, Code.org, Scrimba,
Launch School's lesson anatomy, Exercism mentoring sessions, and Guzdial's and Hermans' books in full. No
claim below rests on them.

---

## (a) The consensus lesson for a new code concept

Every source below agrees on the order; they differ in medium (lecture, video, text, tutor). The order is:
**explain and show, then try together with support, then check, then try alone, then review later.**

| Min | Stage | What happens | Sources | Grade |
|---|---|---|---|---|
| 0 to 3 | Review | A few spaced questions on old material, including what today's concept needs | Rosenshine principle 1 (daily review of 5 to 8 minutes); `recommended-method.md` step 1 | strong |
| 3 to 4 | Goal and names | What the new code is for, in one line; the pattern's steps named (subgoal labels); new words explained | CS1 Subgoals project (labels before or right after the concept); Xie 2019 (connect to what is known, relatable example, then define); PRIMM teachers' "introduction section with vocabulary" | moderate |
| 4 to 12 | **I do: worked example** | The teacher shows a tiny, correct program, runs it, and reads it line by line aloud, saying what each line leaves behind; then the real-sized version of the same shape. One self-explanation prompt on the key line | Rosenshine principles 2, 3, 4; Xie 2019 section 4.1.1; CS50P lectures 0 and 4; Khan talk-throughs; MOOC.fi text; Margulieux 2016; Renkl and Atkinson | strong |
| 12 to 14 | Hinge check | One 1 to 2 minute question whose wrong options each match a known wrong idea | Wiliam (hinge questions); Wilson (a check every 10 to 15 min) | moderate |
| 14 to 22 | **We do: completion** | Same shape, new surface; the last step (or last row of the trace) blank; then the last two; feedback after each | Renkl and Atkinson backward fading; Wilson faded examples; Rosenshine principle 5 (guided practice) and 8 (scaffolds) | moderate |
| 22 to 27 | **You do: independent** | A new program of the same shape, done alone; this is the scored item | Rosenshine principle 9; PRIMM Modify; Khan challenges after the talk-through | strong |
| 27 to 30 | Close | One line to remember; the item joins spaced review | Rosenshine principle 10 (weekly and monthly review) | strong |

Four rules sit on top of the order:

1. **Nothing is asked before it is taught.** Predicting output is a check on what was shown, not a first
   contact. PRIMM's predict stage is low stakes and not assessed, on code the class can already read
   ([Raspberry Pi Foundation PRIMM quick read](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf)).
   Problem solving before instruction has "no clear benefits for procedural knowledge" (Loibl, Roll and Rummel
   2017, local `learning-methods/loibl-roll-rummel-2017-when-problem-solving-first.md` l.1223). Grade: moderate.
2. **Small steps, about 80% right while practising.** "Only present small amounts of new material at any
   time"; the best success rate during practice "appears to be about 80 percent"
   ([Rosenshine 2012](https://www.aft.org/sites/default/files/Rosenshine.pdf)). Grade: moderate (correlational
   classroom studies, widely replicated in direct-instruction research).
3. **Tracing is taught, then practised.** Xie et al. teach how code runs "one line at a time from top to
   bottom" and a memory-table method before any tracing questions (local `code/research/xie-2019-theory-of-instruction.md`
   l.614 to 623, l.664). Cunningham et al.: "all students should be taught a tracing sketch technique"
   ([ICER 2017](https://www.gvu.gatech.edu/sites/default/files/related_project_files/p164-cunningham.pdf)). Grade: moderate.
4. **Correct examples before broken ones.** True novices learn more from correct examples only; wrong
   examples help once some knowledge exists (Große and Renkl 2007, in `skill-methods.md` A2). Grade: moderate.

When to stop showing examples: as knowledge grows, worked examples stop helping and solving helps more
(expertise reversal, Kalyuga 2007, local `learning-methods/kalyuga-2007-expertise-reversal-rapid-assessment.md`).
A short first-step test decides it per pattern (`skill-methods.md` D2). For the first units of a new pattern,
examples come first. Grade: moderate.

---

## (b) How each program does it

### Harvard CS50P (David Malan)
- **Lecture: live coding, one change at a time, run after each.** Lecture 0 starts from a one-line
  `print`, adds `input`, then a variable, then shows the bug `print("hello, name")` and fixes it
  (local `code/cs50p/notes/lecture-0.md` l.40 to 80). The first definition: "A variable is just a container
  for a value" (l.66). Arguments are named on the first function: `"hello, world"` is "the argument"
  (l.45).
- **Reading an API reply** is taught exactly the way Faiz needs it: request, print the whole reply, admit
  "it can be quite dizzying", pretty-print it, find the list called `results`, then loop and pull one key,
  `trackName` (lecture 4, l.226 to 263). Dicts come two weeks earlier, introduced by contrast with lists
  (lecture 2, l.228 to 256).
- **After lecture:** 3 to 10 minute shorts on one idea, then 4 to 6 problem set programs, each with a spec,
  "How to Test" inputs and outputs, then check50 (local `code/INDEX.md`, "CS50P, week by week"). Campus
  sections are not part of the free version.
- Grade: moderate (the course's own design; no controlled study of its lessons).

### Raspberry Pi Foundation / Sue Sentance: PRIMM
- Predict, Run, Investigate, Modify, Make. Predict is done in pairs, away from the computer, about what the
  program does (its function), and "shouldn't be an assessed exercise"; Investigate uses "tracing,
  annotating, questioning"; Modify moves in small steps from "not mine" to "partly mine"
  ([PRIMM quick read](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf)).
- The teacher is the "More Knowledgeable Other" who must "show them (model)" (Sentance, Waite and Kallia
  2019, local `code/research/sentance-2019-primm.md` l.360). The paper does not say what is taught before a
  predict task; a study teacher asked for "an introduction section with vocabulary and the basics" first
  (l.1292), and another varied "how much detail I went into with the starter" by class (l.1451).
- Evidence: one quasi-experiment, 493 students, PRIMM ahead, small effect (r = .13). Grade: weak to
  moderate for the order; PRIMM itself names reading before writing, talk, and small scaffolded steps as its
  core, not "predict before teaching".

### Xie, Nelson and Ko: theory of instruction (University of Washington)
- Four skills in order per construct: read semantics (trace), write semantics, read templates, write
  templates. Each construct is introduced by connecting it to what is known, a relatable example, a
  definition, an explained example, an annotated example showing which lines run, **then** tracing
  practice (local `xie-2019-theory-of-instruction.md` section 4.1.1, l.688 to 717).
- The memory-table tracing method is taught up front, in the introduction (l.614 to 623).
- Grade: moderate (small studies; the 2018 tracing strategy study had n = 24).

### PLTutor (Nelson, Xie, Ko 2017)
- Starts with conceptual content, then steps through execution showing the machine's state, and
  "interleave[s] conceptual instruction about semantics throughout the program's execution"; only then asks
  the learner to fill hidden values (local `nelson-2017-pltutor-comprehension-first.md` l.326, l.382).
- Grade: weak to moderate (one small lab study against Codecademy).

### Khan Academy computing (Pamela Fox's courses)
- A talk-through (the instructor types and talks, the learner can pause and edit), then a step-by-step
  challenge with hints: "After a student watches a talkthrough, we encourage them to start a challenge"
  ([Khan Academy CS blog](https://cs-blog.khanacademy.org/2013/08/introducing-programming-challenges.html)).
- Khan hints reveal one step at a time; all hints together make a worked example
  (`skill-methods.md` B, Khan row).
- Grade: moderate (large platform practice; Khan's mastery results in `learning-methods/khan-*`).

### University of Helsinki MOOC.fi Python
- Text-first: the variables page gives the syntax, then several complete examples each with its printed
  output, before the first exercise; for example, "The value stored in a variable can change"
  ([MOOC.fi part 1, section 3](https://programming-24.mooc.fi/part-1/3-more-about-variables)). A web summary
  counted seven examples with output before the first exercise; this count was not checked by hand.
- Grade: moderate (widely used; design evidence from the course team not read here).

### Carpentries and Greg Wilson, *Teaching Tech Together*
- Live coding: go slowly, explain every line, make and fix mistakes in front of learners
  ([Nederbragt et al. 2020, Ten quick tips for participatory live coding](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1008090)).
- Faded examples: a full worked solution, then the same kind with some steps blank, then more blanks,
  then a whole problem; minimal guidance is less effective for novices; a quick check every 10 to 15 minutes
  "to make sure that your learners are actually learning"
  ([Teaching Tech Together](https://teachtogether.tech/en/index.html), chapters 2 and 4).
- Grade: moderate (practice guides built on the cognitive-load research).

### CS1 Subgoals project (Margulieux, Morrison, Decker)
- Labels first or right after the concept, then labelled worked examples, then practice with a
  reference sheet of the labels. "We highly encourage you to either present the worked examples in class";
  left to watch alone, "many students completely skip" them (local `code/research/subgoals-how-do-i-use-subgoals.md`).
- Labelled examples: 61% vs 45% problems solved in the lab (Margulieux 2016); over a semester, better
  quizzes but not better exams (Margulieux 2020, in `structures/code.md`). Grade: moderate.

### Math Academy (non-code, but the closest one-to-one analogue)
- Each lesson is 3 to 4 knowledge points; each is one worked example, then 2 to 5 practice questions of the
  same type; fail twice and it reviews the prerequisite (`skill-methods.md` B, from *The Math Academy Way*).
  Grade: moderate.

### Brilliant
- Problem before procedure, one concept per 5 to 15 minute lesson (`skill-methods.md` B). This is
  generation-first; it suits low-complexity material. For code, with many interacting parts, the research
  base sides with examples first (Chen, Kalyuga, Sweller 2015; `method-effectiveness.md` section 3).
  Grade: weak as a model for code.

### Felienne Hermans (reading code aloud)
- School students (n = 49) who read code aloud remembered syntax better; understanding-level scores did not
  differ ([TU Delft record of Swidan and Hermans 2019](https://research.tudelft.nl/en/publications/the-effect-of-reading-code-aloud-on-comprehension-an-empirical-st/)).
  Use: the worked example reads each line in words ("look up the key balance in row") so he has words for the
  code; do not expect it to build understanding by itself. Grade: weak.

---

## (c) Testing and feedback practice

**Question types by stage** (from the sources above, and `code/INDEX.md` section 2):

| Stage | Question type | How hard | Source |
|---|---|---|---|
| Right after a worked example | One self-explanation prompt on the key line ("why does this line give a number, not a dict?") | should be answerable from what was just shown | Rosenshine; Bisra 2018 g = 0.55 (`method-effectiveness.md` row 8) |
| Hinge | Multiple choice, 3 or 4 options, each wrong option a named wrong idea; 1 to 2 minutes | most learners right; the wrong ones tell you which idea failed | [Wiliam, ASCD](https://www.ascd.org/el/articles/designing-great-hinge-questions) |
| Guided practice | Completion: fill the last line or the last row of a trace table; Parsons with one distractor | about 80% right first time | Renkl; Rosenshine; Ericson (Parsons) |
| Predict output | Working code of the shape just taught, low stakes | about 80% | PRIMM quick read |
| Independent | Trace a new program in full; modify to meet a test; later, find a planted bug | the scored mastery item | Xie; PRIMM Modify; CS50P check50 |
| Delayed | Same kind, new surface, 7 days later | at the bar | `recommended-method.md` |

**Feedback.** Immediate after each item, explaining why, at most three points, about the task (elaborated
feedback g = 0.49 vs 0.05 for right/wrong only; `ai-tutoring.md` 4f). Short answer first, then options with
an explanation per option (`method-effectiveness.md` 1b). "Not yet" means new items of the same kind, not
the same items again (Khan, Launch School, in `teaching-structure.md` A4).

**Mastery.** High bar (91 to 100%) on the check, retest on new items (Kulik, `method-effectiveness.md` row
7); Khan levels move 70 to 85% to Familiar, then all right to Proficient and Mastered (`skill-methods.md` B).
The bar applies to independent and delayed items, not to guided ones.

**How hard the first questions are.** Low. Rosenshine's least effective teachers "passed out worksheets
and told students to solve the problems" after short explanations; the most effective checked every point
before moving on ([Rosenshine 2012](https://www.aft.org/sites/default/files/Rosenshine.pdf)). The first
question after a worked example should be one most learners get right.

---

## (d) Where the current design departs from expert practice (summary of `gap-audit-code.md`)

| # | Departure | Expert source | Where |
|---|---|---|---|
| G1 | No worked example step anywhere | Rosenshine; Renkl; Margulieux; `recommended-method.md` step 4 | `code.md` l.72 to 80; `INTEGRATED.md` l.15; `check_unit.py` l.26; all units |
| G2 | Machinery forbids a teaching-only message | Rosenshine modelling; PRIMM MKO; Khan talk-through | `check_unit.py` l.155; `SKILL.md` l.30 to 34; `hooks/teaching-guard.py` |
| G3 | Scored predict on untaught code as step 1 | `ai-tutoring.md` 4b.4; PRIMM "low stakes"; his E7 | `code.md` l.75; unit headers l.8; code-01 l.11 |
| G4 | Commit-first frame applied to new code patterns | `method-effectiveness.md` section 3; Loibl 2017 | `INTEGRATED.md` l.30 |
| G5 | Full blank table as first practice; no fading | Renkl; Wilson; his D5 | code-01 l.82, 02 l.86, 03 l.90, 04 l.91 |
| G6 | Tracing tables required before tracing is taught; Cunningham misread | Xie 2019; PLTutor; Cunningham discussion | `code.md` l.40 to 42; code-01 l.113 |
| G7 | Sorva used to ban showing a trace | PLTutor; live coding | `code.md` l.43, l.235 |
| G8 | No self-explanation prompts | Bisra; `ai-tutoring.md` 4c | all units |
| G9 | 5+ new constructs per step | Rosenshine; craft item 5; Math Academy; his A11 | code-01 Trace; code-02 l.40 to 84 |
| G10 | "sticker", "machine", "slot" counted as taught | his C1, C49; CS50P real terms | `docs/glossary.md` l.9 to 11 |
| G11 | Code explained as a summary, not read line by line | CS50P; Khan; Carpentries | `SKILL.md` l.62; all units |
| G12 | Tiny example only after failure | `ai-tutoring.md` 4a.3; his B1 | `SKILL.md` l.54 |
| G13 | Subgoal labels hidden in question code | CS1 Subgoals project | all units |
| G14 | Broken code before correct examples | Große and Renkl; his B11 | code-01 Find the bug; code-02 Predict |
| G15 | Placement test not built | Kalyuga | `code.md` l.85, l.135 |
| G16 | Bar on guided blank-table cells | Rosenshine 80%; Kulik | `INTEGRATED.md` l.50; `engine.py` l.15, l.41 |
| G17 | First checks not diagnostic, too long | Wiliam; Wilson | all units |
| G18 to G20 | Earlier audit enlarged tables; D5 misread; freeze blocked the fix | as above | `audit-units.md` #17; `code.md` l.59; `SKILL.md` l.73 |

---

## (e) The code unit template for Faiz, and a worked sample of unit 1

### The template (every code unit, first time a pattern appears)

About 30 minutes, 8 to 10 short messages, one per step. Each message 700 to 2,100 characters (his record
B8). Code in the chat. Every term explained where it first appears. Real terms (variable, function,
argument, return value, dict, key), not house words.

| # | Step | Scored? | What the message contains | Source |
|---|---|---|---|---|
| 0 | Recall | no (spaced queue) | 3 old cards | Rosenshine 1; FSRS queue |
| 1 | Goal and steps | no | The job in one line ("read the answer and the token count out of an AI reply"); the pattern's 2 to 4 step names; one line per new word | CS1 Subgoals; Xie 4.1.1 |
| 2 | **Show 1** (I do, tiny) | no | 2 to 4 line correct program, its real output, then each line read in words with the value it leaves; one self-explanation prompt | Rosenshine 3, 4; CS50P lecture 0; his B1 |
| 3 | **Try with me 1** (we do) | no, target about 80% | Same shape, new names; a filled trace table with the last row blank; one hinge MCQ | Renkl; Wiliam |
| 4 | **Show 2** (next knowledge point) | no | One new idea added to the same example; same reading line by line; prompt | Math Academy knowledge points; Xie "added complexity" |
| 5 | **Try with me 2** | no | Last two rows blank, or one line to complete | Renkl backward fading |
| 6 | **Show 3** (the real shape) | no | The real-sized version (up to about 10 lines), subgoal labels on it | Margulieux; CS50P lecture 4 |
| 7 | **Try with me 3** | no | Parsons with one distractor, or the last line to write | Ericson; Subgoals formative list |
| 8 | **Your turn** (you do) | **yes** | A new program of the same shape: full trace table or write the one line; then predict and label (crash / quietly wrong / fine) now that each label has been shown | Rosenshine 9; PRIMM Modify |
| 9 | Close | no | "Next time I see ..., I ..."; cards | Rosenshine 10 |
| Cold (7 days) | New surface, same shape | **yes** | | `recommended-method.md` |

Later units of the same pattern: Show shrinks to one, Try with me leaves more blank, then Change (edit to
pass a test), then Find the bug (label-only first), then Tell the AI. From the third problem of a pattern,
he attempts first and then sees the expert version (`method-effectiveness.md` section 3). A new pattern
starts again at Show (4C/ID saw-tooth, `skill-methods.md` D2).

Stuck order (unchanged): his own earlier answer, two options, an everyday picture, the answer with the
reason and a one-line say-back (`ai-tutoring.md` 4d).

### Worked sample: unit 1, "Calling an AI model and reading its reply dict"

Pattern steps (subgoal labels), used all unit:
**1. Call the function and keep what it returns. 2. Print the whole reply once to see its shape.
3. Go one key at a time to the value you want. 4. Check what kind of value you got.**
These follow CS50P lecture 4's order: request, print whole reply, find the key, pull the value.

All programs below were run on 2026-09-25 (scratch copies); before teaching, each goes into
`learn/code/code-01/` and is recorded with `code/record.py` so the checker can trace every output.
The reply shape (a `content` list, a `stop_reason`, a `usage` dict with `input_tokens` and `output_tokens`)
follows Anthropic's Messages API as shown in the saved docs (local
`production-and-llm-behaviour/production/anthropic-prompt-caching.md` l.843 to 850, l.905). The model is a
stand-in written in Python so it runs offline; no numbers are real prices.

---

**Message 1: Goal and steps (no question)**

> Today you learn to read an AI's reply in code. When your app calls a model, the reply comes back as a
> **dict**: a set of labelled values in curly brackets, like one row of a bank statement where each amount
> has a column name. Each label is called a **key**; what sits under it is its **value**.
>
> Four steps, the same every time:
> 1. Call the function and keep what it returns.
> 2. Print the whole reply once to see its shape.
> 3. Go one key at a time to the value you want.
> 4. Check what kind of value you got: a whole dict, or one value inside it.
>
> Step 4 is the one that catches the mistake of printing a whole dict when you wanted one number.

**Message 2: Show 1, a dict and one key (I do)**

> ```python
> row = {"account": "HBL-001", "balance": 5200}
> print(row["balance"])
> print(row)
> ```
> It prints:
> ```output
> 5200
> {'account': 'HBL-001', 'balance': 5200}
> ```
> **How this code works, line by line.**
> - Line 1 makes a dict with two keys, `"account"` and `"balance"`, and gives it the name `row`. A name
>   that holds a value is a **variable**. After this line, `row` holds the whole dict.
> - Line 2: `row["balance"]` means "in `row`, look up the key `balance`". Square brackets after a dict
>   name are how you look something up. It hands back one value, `5200`, and `print` shows it.
> - Line 3 prints `row` itself, so you see the whole dict, curly brackets and all.
>
> Why it is built this way: a reply carries many values, and you almost always want one of them; the
> square brackets pick it out.
>
> **One line from you:** why does the second print show curly brackets and the first does not?

(Key: the first prints the value under one key; the second prints the whole dict. Unscored.)

**Message 3: Try with me 1 (we do)**

> Same shape, new numbers:
> ```python
> row = {"account": "MCB-7", "balance": 900}
> b = row["balance"]
> print(b)
> ```
> | After line | `row` holds | `b` holds |
> |---|---|---|
> | 1 | `{'account': 'MCB-7', 'balance': 900}` | nothing yet |
> | 2 | the same dict | ? |
>
> 1. Fill the `?`.
> 2. What kind of value does `b` hold? A) the whole dict B) `900` C) the word `"balance"` D) nothing: it crashes

(Key: `900`; B. A = E4 (dict vs value inside); C = key confused with value; D = thinks lookups crash.
Target about 80% right; unscored. The program prints `900`.)

**Message 4: Show 2, a function hands back a dict (I do)**

> A **function** is a named piece of code you run by writing its name with round brackets. What you put
> inside the brackets is the **argument**. The function can hand a value back with `return`; that is its
> **return value**. Here a stand-in for an AI model (it runs offline, no internet):
> ```python
> def fake_model(prompt):
>     return {"text": "Hello, Faiz", "input_tokens": 5, "output_tokens": 3}
>
> reply = fake_model("Say hello")
> print(reply["text"])
> ```
> It prints:
> ```output
> Hello, Faiz
> ```
> **How this code works, in the order it runs.**
> - `def fake_model(prompt):` only defines the function; nothing runs yet. `prompt` is the name the
>   argument will have inside it.
> - `reply = fake_model("Say hello")` runs it: `"Say hello"` goes in as `prompt`, the `return` line hands
>   back the dict, and `reply` now holds that whole dict (step 1: call and keep).
> - `reply["text"]` looks up one key (step 3), giving the text `Hello, Faiz`.
>
> | After | `prompt` | `reply` |
> |---|---|---|
> | the call starts | `'Say hello'` | nothing yet |
> | the call returns | (gone: it only lived inside the function) | `{'text': 'Hello, Faiz', 'input_tokens': 5, 'output_tokens': 3}` |
> | `print` | | same dict; the screen shows `Hello, Faiz` |
>
> **One line from you:** after the call, does `reply` hold the text or the whole dict?

(Key: the whole dict; the text is one value inside it. Unscored.)

**Message 5: Try with me 2 (we do, last two rows blank)**

> ```python
> def fake_model(prompt):
>     return {"text": "Rs 280 per dollar", "input_tokens": 9, "output_tokens": 6}
>
> reply = fake_model("USD to PKR?")
> used = reply["output_tokens"]
> print(used)
> ```
> | After line | `reply` holds | `used` holds |
> |---|---|---|
> | `reply = ...` | ? | nothing yet |
> | `used = ...` | same as above | ? |
>
> Then: what does it print?

(Key: the dict `{'text': 'Rs 280 per dollar', 'input_tokens': 9, 'output_tokens': 6}`; `6`; prints `6`.
The exchange rate text is only a string the stand-in returns; it is not a fact. Unscored, target about 80%.)

**Message 6: Show 3, the real reply shape (I do)**

> Real replies nest: some values are themselves dicts or lists. A **list** is values in a row in square
> brackets; position `0` is the first. Here is the shape a real model reply has:
> ```python
> reply = {
>     "content": [{"type": "text", "text": "Islamabad"}],
>     "stop_reason": "end_turn",
>     "usage": {"input_tokens": 14, "output_tokens": 4},
> }
> print(reply["usage"])
> print(reply["usage"]["output_tokens"])
> print(reply["content"][0]["text"])
> ```
> It prints:
> ```output
> {'input_tokens': 14, 'output_tokens': 4}
> 4
> Islamabad
> ```
> **How this code works: one bracket at a time (step 3), checking the kind each time (step 4).**
> - `reply["usage"]` gives a dict (line 1 of the output). Not a number yet.
> - `reply["usage"]["output_tokens"]`: first `["usage"]` gives that dict, then `["output_tokens"]` looks
>   inside it and gives `4`.
> - `reply["content"]` gives a list; `[0]` takes its first item, a dict; `["text"]` gives `Islamabad`.
>   The text sits inside a list because a reply can hold several pieces.
>
> **One line from you:** why does the first print show curly brackets but the second shows `4`?

(Key: the first stops at the `usage` dict; the second goes one key further. Unscored.)

**Message 7: Try with me 3 (we do, write the last line)**

> ```python
> reply = {
>     "content": [{"type": "text", "text": "Karachi"}],
>     "stop_reason": "max_tokens",
>     "usage": {"input_tokens": 20, "output_tokens": 50},
> }
> print(reply["stop_reason"])
> ```
> This prints `max_tokens`. Write one more `print` line that shows the input token count, and say what it
> prints. Steps on hand: call and keep, print whole, one key at a time, check the kind.

(Key: `print(reply["usage"]["input_tokens"])` prints `20`. Common slip: `print(reply["input_tokens"])`,
which crashes with `KeyError`, because `input_tokens` sits inside `usage`. Unscored.)

**Message 8: Your turn (scored)**

> The three labels, each with one example you have now seen:
> - **crash**: stops with an error, like looking up a key the dict does not have (`KeyError`).
> - **quietly wrong**: runs, but shows the wrong thing, like printing a whole dict when you wanted a number.
> - **fine**: runs and shows what was wanted.
>
> ```python
> reply = {"content": [{"type": "text", "text": "Lahore"}], "usage": {"input_tokens": 8, "output_tokens": 2}}
> print(reply["text"])
> ```
> ```python
> reply = {"content": [{"type": "text", "text": "Lahore"}], "usage": {"input_tokens": 8, "output_tokens": 2}}
> print("output tokens:", reply["usage"])
> ```
> For each program: what does it show, which label, and the one fixed line.

(Key, from the runs: program A ends `KeyError: 'text'`, **crash**, fix `print(reply["content"][0]["text"])`;
program B prints `output tokens: {'input_tokens': 8, 'output_tokens': 2}`, **quietly wrong** (E4: the whole
dict, not the number), fix `print("output tokens:", reply["usage"]["output_tokens"])`. Score: 6 parts,
right parts over 6.)

**Message 9: Close**

> Finish in your own words: "Next time I read a value out of an AI reply, I ..."

(Key, like: "... go one key at a time and check whether I have a dict or the value inside it." Cards: a
new reply dict, "what kind of value does `reply["usage"]` hold?" with a second surface, per the queue rule.)

**Cold, 7 days later (scored):** a new reply with a different nesting (for example the text under
`["message"]["content"]`), asked as in Message 8: what it shows, the label, the fix.

What this sample deliberately leaves for unit 2 and later: the real API call over the internet (import,
client, key), timing, cost, logs and records, retries. Each arrives later as one new knowledge point on
top of this shape, which is what the old code-01 tried to teach in one step (G9).

---

## Evidence limits

- No study tests this sequence for one adult learning to read AI-engineering code from an AI tutor. It is
  carried over from classroom and lab research (Rosenshine, Renkl, Xie, Margulieux, PRIMM) and matches his
  own record (B1, D5, B11, E7, A11).
- Rosenshine's principles come mostly from correlational classroom studies plus cognitive research; the 80%
  figure is an average from those studies, not an experimental optimum.
- The 30-minute timing is a design choice from his message-size record (B8, B9), not from a study.
- MOOC.fi's example count came from a web summary, not a manual count.
- Programs not researched this pass (MIT 6.100L, Code.org, Scrimba, Launch School lessons, Exercism
  mentoring) are not used as evidence.
