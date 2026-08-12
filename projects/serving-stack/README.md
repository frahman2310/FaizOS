# Serving stacks — prefill vs decode, throughput vs latency

**Two phases, opposite bottlenecks:**
- **Prefill** — the whole prompt at once, lots of math per weight read -> COMPUTE-bound. Fast (TTFT 14 ms for a 500-token prompt).
- **Decode** — one token at a time, each reading every weight -> MEMORY-bound. Slow, and it dominates total latency.

**The free lunch:** because decode is memory-bound, one weight read serves the whole batch. 14 GB at 2000 GB/s = 7 ms per step, regardless of batch size.

| batch | tokens/s total | tokens/s per user |
|---|---|---|
| 1 | 143 | 143 |
| 32 | 4,571 | 143 |
| 128 | 18,286 | 143 |

128x throughput, identical per-user speed. This is why serving batches aggressively, and why every inference optimization targets DECODE.

Run: `python3 serving_stack.py` -> PASS. Module 14 skill `serving-stacks`. Completes Module 14.
