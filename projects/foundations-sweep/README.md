# Foundations sweep — the maths and engineering underneath everything

Backfill for Modules 1-6. Most of this NAMES what was already built.

**SVD & low-rank.** Any matrix = a sum of rank-1 pieces ordered by importance (singular values). Keeping the top k is the BEST possible rank-k approximation. Singular values [10,6,2,1,0.5]: top 1 keeps 70.8%, top 2 keeps **96.3%**. That is why LoRA (low-rank updates) and MLA (latent compression) work — and PCA is SVD applied to data.

**Probability.** Expectation = the long-run average (the GRPO baseline IS one). Variance = average squared distance from the mean ([2,4,6] -> 2.67). Covariance = do two things move together.

**High-dimensional geometry.** In high dimensions random vectors are almost always nearly perpendicular — which is what makes superposition possible. And the typical size of a random d-dim dot product is ~sqrt(d): **that is where attention's 1/sqrt(d) comes from** (d=64 -> divide by 8).

**Regression.** `y = w*x + b` is a neuron without the tanh. Closed form: `w = cov(x,y)/var(x)`, `b = mean(y) - w*mean(x)`. Recovers y=2x+1 exactly.

**Bias-variance & double descent.** total error ~ bias^2 + variance. Classically a U-curve. DOUBLE DESCENT: push the model past the point of perfectly fitting the training data and test error falls AGAIN — which is why enormous models work at all.

**Complexity.** List lookup O(n) = 1,000,000 checks; dict O(1) = 1. (Why `stats` in the BPE build and `TOOLS` in the safety build are dicts.)

**Profiling.** cProfile ranks by cumulative time — Amdahl again: measure, then fix the biggest share.

**Initialisation.** Each layer scales the signal by ~fan_in * weight_variance; 50 layers later it explodes or vanishes. Xavier: std = 1/sqrt(fan_in) (0.1 for fan_in 100). The same disease residuals and RMSNorm treat.

**Dev setup.** uv + ruff + one pinned Python + CI on every push. Reproducibility over cleverness.

Run: `python3 foundations.py` -> PASS. Backfills Modules 1, 2, 3, 4 and 6.
