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
