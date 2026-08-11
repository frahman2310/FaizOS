# Collectives — all-reduce, reduce-scatter, all-gather

**Goal:** the operations GPUs use to combine work, and what they cost.

- **all-reduce**: everyone contributes, everyone gets the whole result (how data-parallel GPUs sync gradients).
- **reduce-scatter**: everyone contributes, each keeps only its own slice.
- **all-gather**: each holds a slice, everyone ends up with all of them.
- **Identity:** `all-reduce = reduce-scatter + all-gather` (verified exactly) — the basis of FSDP.

**Cost:** ring algorithm moves `2 * data * (n-1)/n` per GPU (~2x, roughly independent of n). 1 GB all-reduce = 1.5 GB moved: 15 ms on NVLink (100 GB/s) vs 150 ms on Ethernet (10 GB/s).

Run: `python3 collectives.py` -> PASS. Module 13 skill `collectives-interconnect`.
