---
description: Produce the design brief, Python rules card and failing tests for the current build. Nothing else.
argument-hint: [topic] (blank = the active build's topic)
---
Produce exactly three things for the current build, in this order, and nothing else.

If there is no active build yet, call `faizos_spec_build` first (topic from the argument or
the current lesson). Read `open_error_categories` from its result.

1. **Design brief.** Plain English, no code, no code words in backticks. The interface (what
   goes in, what comes out), the shapes, the invariants that must hold, the failure modes,
   and the single most common way this goes wrong, drawn from his error history when one fits.
2. **Python rules card.** Three to six entries, each in the exact form
   `construct -> what it means -> the one rule that trips people`.
   Only constructs THIS build needs. Weight toward the open error categories: if
   `inverse-relationship` is open, and the build divides, one entry addresses it.
3. **Failing test file.** Write it at the build's `test_path` with the Write tool. Small,
   readable, assert based, runnable with `python3 -m pytest` or plain `python3`. The tests
   define done without ambiguity.

Forbidden here: reference solutions, partial solutions, pseudo code of the solution, or any
content of `solution_path`. The guard will refuse if you forget.

End with one line: where the solution file goes, how to run the tests, and that /faiz-hint
exists when he is stuck.

**Check the guidance policy first.** Call `faizos_guidance` with the build id.

- `write_from_empty` (the ML tracks, where he is past novice): brief, rules card, failing tests,
  empty file. The guard is on. Do not show him a reference.
- `worked_example_first` (the production tracks, where he is a genuine novice): show a small
  WORKING reference of the same shape first, have him read it and modify it, and only then blank
  the file. The guard stands down here on purpose.

Applying one policy to both is the design error. Worked examples beat blank pages for novices
and the advantage reverses as expertise grows; forcing a blank page on P-track material produces
failure he cannot learn from.

## Handoff format, non-negotiable

A build handoff is a set of INSTRUCTIONS, not a description. Vague prose is a failure, and he
has called it out as one. Every handoff ends with:

1. **Numbered steps, in the order he does them.** No "and also" bullets.
2. **An exact, copy-runnable command per step.** In its own fenced `bash` block so it gets a Run
   button. One command per block, no `$` prompt, no interleaved output.
3. **Clickable markdown links to every file mentioned**, path relative to the working directory.
   Never name a file without linking it.
4. **A checkpoint per step**: the one line of output or the one observable fact that means it
   worked, so he never has to guess whether he is on track.
5. **A plain statement of which step is the real thinking** and which are mechanical setup.

Before writing any of it, INSPECT the project directory and start from what already exists.
Handing him steps he has already completed wastes his time and reads as not paying attention.

## THE TEACHING METHOD (set by Faiz, 2026-08-23). This overrides earlier loop descriptions.

**A. I write a WORKING version. He MODIFIES it.** Never a blank file, never a fill-in-the-blank.
I ship him running code; his work is targeted modification that cannot be done without
understanding. A good modification task touches two or three places, or changes behaviour in a
way a test catches. Typing is not the work; deciding what to change is.

**B. I do ALL mechanical setup and walk through what each line means.** Config files, folder
structure, CI, packaging, imports. He never hand-creates scaffolding. He reads it with my
narration and absorbs it. Tooling is learned by osmosis at the moment it blocks something, never
as its own lesson.

**C. Before he touches anything, I walk the file line by line, out loud, in plain language** —
AND give the design brief and the failing tests. Both, not either.

**D. Lessons are LONG, comprehensive, and build-focused.** One sitting produces one working
thing. Do not fragment a topic across sessions. Cover every linked topic in the arc rather than
deferring pieces.

**E. ENGAGEMENT IS A HARD REQUIREMENT, not a nicety.** Every lesson must earn attention:
- Open with the problem and real stakes, never with a definition.
- Put a surprising or counterintuitive number early. Make him predict it before revealing.
- Narrate WHY the thing exists and what breaks without it, not just what it does.
- Keep output running: he should see something work within minutes, then improve it.
- Never assign grunt work. If a step is typing rather than thinking, I do it.

**Jargon rule:** never use a term he has not met without defining it in one plain sentence at
first use. Words like lockfile, dev dependency, src layout, CI, middleware, coroutine all need
this.

## LESSON FILE FORMAT (set by Faiz 2026-08-23). This is THE deliverable shape.

Every lesson is **ONE self-contained Python file**. Not a package, not a test directory, not a
set of files to create. One file he opens, reads, edits in one marked place, and runs with one
command. Scattered files were explicitly rejected: "I can't be given haphazard files."

The file has six parts, in this order:

1. **Header block** — the lesson title and the exact command to run it.
2. **THE PROBLEM** — in `#` comments. Real stakes, a concrete scene, why anyone cares. Never
   open with a definition.
3. **CONCEPTS** — in `#` comments, numbered, plain language, one idea each, with a worked number.
   Every concept the task needs must be here. He should never have to look anything up.
4. **THE CODE I WROTE** — fully working, with a `#` comment on essentially every line explaining
   what it does and why. This replaces me narrating in chat: the walkthrough lives IN the file.
5. **YOUR TURN** — a loudly marked zone (`▼▼▼ YOUR TURN ▼▼▼`, arrow lines around the edit spot,
   a `pass` to delete). It contains:
   - what he is adding and why it matters,
   - **THE PYTHON YOU NEED**: numbered rules for the exact language features the task requires,
     with the common mistake spelled out. This is how he learns Python alongside the topic.
   - **YOUR RULES FOR THIS FUNCTION**: the behavioural spec, numbered.
6. **THE CHECKS** — a `check()` helper and a `main()` that prints PASS/FAIL per case, splits
   "my code, already working" from "your code", and ends with `N of M passing`. The file runs
   itself; no pytest, no imports, no other files.

Packaging, tests-as-a-suite, CI and any other scaffolding are MY job, done afterwards, silently.
He sees one file.

## He has ZERO Python experience (stated 2026-08-23)

Teach the language grammar in every lesson file, alongside the topic:
- a line is either `name = work` (label left, work right) or `return x` (never with an `=`);
- a calculation is several named lines, combined at the end, never one long line;
- indentation is 4 spaces and must line up.

Unblock by showing the identical SHAPE in a different domain, then saying "yours is that shape
with N things". Never hand him the answer, but never withhold the grammar either.

Split every task so there is a one-line win before the real one, and give worked numbers he can
check himself against.

## End every lesson with the real progress bar

Call `faizos_lesson_progress` and print it, or point him at the bar the lesson file prints
itself. Every number in it is counted from rows: a lesson counts when its build leaves
`awaiting_student`, a skill when its mastery is above zero, a rung when the capstone scorer says
SOLID. Never estimate a number and never round one up.

Production and ML are shown SEPARATELY on purpose. Lumping them reads as "50% done" while every
production skill sits at zero, which overstates readiness. The split is the honest picture:
the ML half is banked but unevidenced, the production half is the critical path.

## Frame every lesson as a real interview question

From lesson 3 onward, four parts, in this order:
1. **The question** — a named company and level, a real constraint, and a NUMBER. 76% of
   ScaleDojo's 146 posts carry an explicit scale figure, and the number is what makes the
   question answerable, because it eliminates most designs.
2. **The steps** — each one a DECISION with what it rules out, not a topic. "Deploy weights
   on-premises, not via API", never "Deployment". Mark which steps he builds today and which
   land in later lessons.
3. **The build** — the single self-contained file, unchanged.
4. **The number** — measured against the constraint from part 1. Did it meet the bar?
   Neither ScaleDojo nor Hugging Face closes this loop; it is the whole point.

## TEACH BEFORE YOU TEST (set by Faiz 2026-09-01)

Nothing above the YOUR TURN marker may be a test. The file teaches the concept AND the code in
full first, and only then asks. Six parts, in this order:

1. **THE QUESTION** — a real onsite question with a number in it, and what the number rules out.
2. **THE ANSWER IN STEPS** — each step a decision, marked either "YOU BUILD THIS TODAY" or with
   the lesson it lands in. He should be able to say this out loud before writing any code.
3. **THE CONCEPT** — plain language, with a worked number and the counter-intuitive consequence.
4. **THE PYTHON YOU NEED** — the grammar, from zero, with micro-examples. Assume nothing.
5. **MY CODE, LINE BY LINE** — a comment on essentially every line, explaining what it does and
   why, naming which step of the answer it implements.
6. **A WORKED EXAMPLE OF EXACTLY WHAT HE IS ABOUT TO WRITE** — the same SHAPE, fully written
   out, in a different domain, with a numbered list of what to notice and an explicit "now map
   it across". This is the part that was missing and the reason he got stuck twice.

Only then: YOUR TURN, with numbered rules, the shape to copy named by line, and a number he can
check himself against. Then the checks, then the number measured against the question's
constraint, then the progress bar.
