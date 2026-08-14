---
description: The open error taxonomy, ranked, with the rule each breaks.
---
Call `faizos_error_report`. Render:

1. **Open categories**, ranked by occurrences: category, occurrences, last seen, and the rule
   it breaks in one line. Note that the top three weight the next rules card automatically.
2. **Resolved categories**, one line each, as the progress record.
3. If a category has not recurred in its last three builds' worth of lessons, offer to mark
   it resolved (update `errors.resolved` via a direct suggestion, executed only on his yes).

Keep it under fifteen lines. This is a mirror, never a lecture.
