---
description: Log an experiment run against a system. Reports seed spread, warns on missing baselines.
argument-hint: [system id or title fragment]
---
Log one run, honestly.

1. Identify the system (`faizos_track_status` or ask). Gather: metric name and value, seed,
   config, GPU type, GPU hours, cost in USD.
2. Call `faizos_log_experiment`.
3. Report back:
   - The recorded run.
   - The seed spread if returned (n, mean, min, max, spread). If n < 3, say how many more
     seeds are needed before any claim counts.
   - If the system has no `baseline_value` and the run has no compute matched baseline noted,
     WARN in one line: a gain over a cheaper baseline is not a gain.
4. The standing rule, once, at the end: a result is real only if it clears the spread against
   a compute matched baseline. Anything else is inside the noise.
