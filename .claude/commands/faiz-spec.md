---
description: Produce the design brief and a complete working file with planted checks for the current build, taught the faiz-teach way.
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

## How to teach

Load the `faiz-teach` skill before any teaching message and follow it. It is the single source of truth for how Faiz is taught and overrides anything in this file. He reads and judges complete working code; he never gets a blank file or a YOUR TURN zone.

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
3. **The code** — a complete working file he reads and judges (see the faiz-teach skill).
4. **The number** — measured against the constraint from part 1. Did it meet the bar?
   Neither ScaleDojo nor Hugging Face closes this loop; it is the whole point.

