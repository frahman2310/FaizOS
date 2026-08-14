---
description: Serve exactly one hint rung for the active build. Never skips, never volunteers rung 4.
---
Serve one hint rung, no more.

1. Call `faizos_hint` with the next rung (the tool knows the ladder state; request
   `previous_max + 1` unless he asked to re hear an earlier rung).
2. If the tool refuses, tell him which rung is actually next and stop.
3. If it grants, author the hint STRICTLY within the returned frame:
   - Rung 1: which assertion failed and what it checks, in English. Nothing about his code.
   - Rung 2: which region of his file the bug is in. The region, never the line.
   - Rung 3: the concept or Python rule he broke, stated as a rule, with no reference to
     his code.
   - Rung 4: the line, with the reasoning.
4. One rung per invocation. He must ask again for the next one. Rung 4 is never given
   unprompted, never given first, and never bundled with rung 3.

If he burns to rung 4 on more than a third of a track's builds, record an insight via
`faizos_record_lesson`: the concept density for that track is too high and should drop.
