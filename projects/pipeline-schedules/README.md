# Pipeline schedules — GPipe vs 1F1B

**The conflict:** more microbatches shrink the bubble, but every forward must SAVE activations until its backward runs.

- **GPipe**: all forwards, then all backwards -> peak activations = M (microbatches).
- **1F1B**: once the pipeline is full, alternate one forward / one backward. Each backward frees a set as the next forward takes one -> peak = P (stages), independent of M.

**Same bubble, different memory.** 4 stages at 128 microbatches: bubble 2.3% either way, but GPipe needs 192 GB of activations vs 1F1B's flat 6 GB.

Run: `python3 schedules.py` -> PASS. Module 13 skill `pipeline-schedules`.
