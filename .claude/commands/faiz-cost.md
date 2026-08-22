---
description: The cost drill. Every design answer ends with a number.
---
Cost awareness is repeatedly named the thing that separates production thinkers from
prototype thinkers. One engineer showed a 70% spend reduction and had an offer the next day.
This drill builds the reflex.

1. Pose ONE scenario, sized like a real interview question. Rotate the shape:
   - traffic to tokens to dollars per day (`100k users x 10 interactions x 2k tokens`)
   - the same workload with prompt caching at a stated hit rate
   - batch versus interactive for an eval run
   - self-host break-even against a serverless per-token rate
   - what a context-tier boundary crossing does to the bill
2. He answers with a number. No formula-only answers, no "it depends".
3. Compute the expected figure yourself, then call `faizos_cost_drill` with the scenario,
   your expected value and his. Within 20% counts.
4. Report the verdict and, if he was off, the one arithmetic step that moved him off.
5. Close with the ranking he should be able to recite cold, cheapest certainty first:
   **batch (-50%, contractual) > prompt caching (-70-85% on prefix-heavy traffic) >
   context trimming across a tier boundary > routing (30-55%) > semantic caching (marginal).**
   Most teams do these in exactly the reverse order.

One scenario per invocation. Keep it under twelve lines. The habit is the point, not precision.
