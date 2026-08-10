# FlashAttention — tiled attention with online softmax

**Goal:** compute attention without ever materializing the n x n score matrix.

**Problem:** the score matrix is O(n^2) (1000 tokens -> 1M entries; 8000 -> 64M) and does not fit in SRAM, so standard attention round-trips it through HBM.

**Fix:** walk the K/V in TILES with a running (max, sum, output). Because softmax needs the whole-row max, keep a running max and rescale the accumulator by `exp(m_old - m_new)` whenever a bigger max appears (online softmax).

**Result:** output identical to naive attention at every tile size; peak score-numbers 64,000,000 -> 2. Run: `python3 flash.py` -> PASS.

Module 11 skill `flash-attention`. Completes Module 11 (GPU kernels).
