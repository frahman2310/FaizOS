# Capstone audit — the 8-rung portfolio

An honest assessment of 43 shipped builds against a hire-grade portfolio. The bar for each rung is
**an artifact someone else can verify**, ideally with a public number.

Status key: ✅ solid · ⚠️ partial · ❌ missing

---

## ✅ Rung 1 — From-scratch fundamentals

**Solid, and unusually deep.** A transformer built from nothing, in plain Python, no frameworks:
softmax → matmul cost → autograd → neuron → layer → MLP → self-attention → QKV → RoPE → RMSNorm →
transformer block → BPE tokenizer → KV cache. Then the modern upgrades: SwiGLU, GQA, SSM/Mamba, MLA.

Most candidates have used a transformer. Few have written every part of one and can explain why each
line exists. **This rung is genuinely strong.**

## ✅ Rung 2 — A working system others can run

**FaizOS itself** is the strongest single artifact here, and it is easy to undersell:
a Claude Code plugin with a local MCP server (TypeScript + SQLite), slash commands, session hooks,
a deterministic notebook compiler, FSRS spaced repetition, and auto-generated progress tracking.

It is a real piece of software with real users (one), real persistence, and no model in the loop for
any of its state. **Lead the portfolio with this.**

## ⚠️ Rung 3 — A trained model with a reported metric

**Partial.** Real training loops were written and run — the XOR MLP converged, and the learnable
attention weight went from loss 4.0 to 0.002. But these are toy scales. There is no trained model
with a metric anyone else would recognise.

**To close:** fine-tune a small open model (QLoRA on a 7B) on a real task and report a before/after
eval number.

## ⚠️ Rung 4 — A measured performance win

**Modeled, not measured.** The kernel and systems work is analytically correct — arithmetic intensity,
the roofline, FlashAttention's tiling, GQA's cache maths, the checkpoint optimum — but every number
was computed rather than benchmarked, because there is no NVIDIA GPU on this machine.

**To close:** rent an hour of A100/H100 time, run the Triton fused softmax against the PyTorch
baseline, and report the measured speedup.

## ❌ Rung 5 — A reproduction of a published result

**Missing.** The method is now understood (seeds, spread, compute-matched baselines, ablations) but
nothing has been reproduced.

**To close:** pick a small, well-specified result with a public number and match it within noise.
Report mean ± spread over ≥3 seeds. This is the single most credible artifact on the list, because
almost nobody does it and it cannot be faked.

## ❌ Rung 6 — A merged open-source contribution

**Missing, and only you can close it.** The bar is a **merged** PR, not an opened one.

**To close:** `vLLM`, `TRL`, `transformers` and `nanoGPT` all label beginner issues
(`good first issue`, `documentation`). Realistic first PRs: a docstring that is wrong, a missing type
hint, a failing edge case in a test. Small and merged beats ambitious and ignored.

## ⚠️ Rung 7 — An eval harness with results

**Partial.** Perplexity was implemented correctly from scratch (`exp(mean(-ln p))`) and the
capability-vs-reliability distinction (pass@1 vs pass@k) is understood — but neither has been run
against a real model on real held-out data.

**To close:** run the perplexity harness over a public dataset with two model sizes and plot the gap.

## ⚠️ Rung 8 — A capstone artifact

**Partial — and it already exists, it just needs framing.** FaizOS is the capstone. What it lacks is
a README written for a stranger rather than for you: what problem it solves, a 30-second demo, and
one number (43 builds, 20 modules, ~7 months of curriculum compressed).

---

## The honest summary

**2 solid · 3 partial · 3 missing.**

Depth of *understanding* is well ahead of depth of *evidence*. That is the opposite of the usual
problem, and it is the easier one to fix — you cannot fake understanding, but you can absolutely go
and generate evidence.

**The single bottleneck is compute.** Rungs 3, 4, 5 and 7 all need a real GPU. An hour of rented
A100 time (a few dollars) unlocks four rungs. That is the highest-leverage next action by a wide
margin.

**Suggested order:**
1. Frame FaizOS properly (rung 8) — free, today.
2. Rent a GPU, benchmark the Triton kernel (rung 4) — one afternoon, one real number.
3. QLoRA fine-tune with a before/after eval (rungs 3 + 7) — one weekend.
4. Reproduce one small published result (rung 5) — the credibility artifact.
5. Land one small merged PR (rung 6) — the public signal.
