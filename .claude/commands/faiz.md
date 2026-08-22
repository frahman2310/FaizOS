---
description: FaizOS dashboard, build heavy. The active build and venture lead; stats trail.
---
Call `faizos_state` first. Render a dashboard the user can read in five seconds, in this order:

1. **Active build** (if any): state, `solution_path`, `test_path`, deepest hint rung so far. This is HIS file to write. One line: "run the tests, ask /faiz-hint if stuck, /faiz-review when green."
2. **Active venture** (if any): title, v0 metric, days left to the 14 day review.
3. **Current track**: code, title, and its completion test in one line.
4. **Open error categories** (top 3): category and the rule it breaks. These weight the next rules card.
5. **Student-wrote ratio**: written vs unlocked builds. State it plainly, no judgment.
6. Streak, ships, and ONE recommended next step.

Menu: `/faiz-learn [track|next]` · `/faiz-build "<thing>"` · `/faiz-spec` · `/faiz-hint` · `/faiz-review` · `/faiz-run` · `/faiz-errors` · `/faiz-drill` · `/faiz-venture` · `/faiz-frontier` · `/faiz-ship`

Never lecture on the dashboard. If there is an active build, everything else is secondary.

**v3 additions to the dashboard, in this order:**

1. **A rebuild that has come due outranks everything.** If `rebuilds_due` is non-empty, that is
   the recommended next action: blank the file, no reference, no hints. It is provisional until
   he does it.
2. **Mode** — `course` (the P0-P7 spine, in order), `venture` (the active venture picks the
   build), or `free`. Show the reason the tool gives, not just the label.
3. **Guidance** for the active build: whether the guard is on, in five words.
4. **Cost drill record** as a single line: attempts and hit rate.
