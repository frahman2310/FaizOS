---
description: Three-pass review of HIS code, then record it. Runs after tests pass or he gives up.
---
Run the three passes in order, then record. Only run this after his tests pass or he has
explicitly given up. Never before he has attempted.

**Pass 1, his code, line by line, in plain English.** For each line: what it does, what each
variable holds at that point, and its type. This is the walk-the-code format applied to his
own file. No judgment in this pass, only accuracy.

**Pass 2, diff against reference.** Write the reference version yourself now (never earlier).
For each difference, classify it out loud as exactly one of:
- correctness: his version gives a wrong answer somewhere. Show the input that breaks it.
- clarity: both correct; one is easier to read. Say why in one sentence.
- taste: both fine. Say "taste" and move on.
Most differences are taste. Saying so matters; otherwise he learns to write your code
instead of learning to write.

**Pass 3, error classification.** Every genuine mistake gets a category from the taxonomy
(expression-vs-statement, off-by-one, type-confusion, mutation-vs-copy, shape-mismatch,
inverse-relationship, missing-call-brackets, state-in-wrong-scope, broadcasting, api-misuse,
silent-truncation, ordering-pairing). Correctness diffs are errors; taste diffs are not.

**Record.** Call `faizos_review_code` with build_id, his code, your reference, the diff
summary, the classified lists, and the errors. This marks the build done. Then finish the
lesson: `faizos_record_lesson` (with the same errors) and a posted revision note via
`faizos_save_revision`.
