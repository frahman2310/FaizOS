# FaizOS — Content & Build Summary
_Auto-generated from your progress after every lesson/module (Stop hook). Do not edit by hand._

**37% coverage** · 5/20 modules complete · 22 builds shipped · 22/66 skills touched

```
OVERALL  ▓▓▓▓▓▓▓░░░░░░░░░░░░░ 37%
```

## Modules
### 🔄 Module 1 — Math: numbers, softmax, matmul (67%)
- **skills:** · Dev setup: uv, ruff, one Python, CI · ✓ Numerically stable softmax & log-sum-exp · ✓ Matmul, shapes & FLOP cost
- **builds:** #2 Matmul FLOP estimator · #8 self-attention from scratch

### 🔄 Module 2 — Math: linear algebra & calculus (25%)
- **skills:** · SVD & low-rank (PCA, LoRA) · ✓ Backprop as vector-Jacobian products · · Probability, covariance & expectation · · High-dimensional geometry
- **builds:** #3 micrograd: autograd from scratch

### 🔄 Module 3 — Python & the cost model (50%)
- **skills:** ✓ Modern Python craft (uv, ruff, typing, CI) · · Core data structures & complexity · ✓ Arithmetic intensity & the roofline · · Profiling (cProfile, torch profiler)
- **builds:** #2 Matmul FLOP estimator · #3 micrograd: autograd from scratch · #4 tiny net that learns · #5 a real neuron · #6 a layer of neurons · #7 an MLP that learns XOR · #8 self-attention from scratch · #9 QKV attention (scaled dot-product) · #10 RoPE — rotary positions · #11 RMSNorm · #22 GPU memory hierarchy & MFU

### 🔄 Module 4 — Classical ML (25%)
- **skills:** · Regression from scratch · ✓ Leakage-safe ML pipeline · · Bias-variance & double descent · · PCA via SVD
- **builds:** #20 Held-out eval: perplexity from scratch

### ✅ Module 5 — Autograd from scratch (100%)
- **skills:** ✓ Autograd from scratch (micrograd) · ✓ PyTorch tensors & training loop
- **builds:** #3 micrograd: autograd from scratch · #4 tiny net that learns · #5 a real neuron · #6 a layer of neurons · #7 an MLP that learns XOR · #13 Train attention: a learned attention weight

### 🔄 Module 6 — Optimization & DL foundations (33%)
- **skills:** ✓ SGD, Adam & schedules · · Initialization & normalization · · torch.compile & CUDA graphs
- **builds:** #4 tiny net that learns · #5 a real neuron · #7 an MLP that learns XOR · #13 Train attention: a learned attention weight

### ✅ Module 7 — Attention & modern block basics (100%)
- **skills:** ✓ Self-attention from scratch · ✓ RoPE rotary positions · ✓ RMSNorm
- **builds:** #8 self-attention from scratch · #9 QKV attention (scaled dot-product) · #10 RoPE — rotary positions · #11 RMSNorm · #12 Transformer block: residuals + stacking · #13 Train attention: a learned attention weight

### ✅ Module 8 — FFN, GQA & state-space models (100%)
- **skills:** ✓ SwiGLU gated FFN · ✓ Grouped-Query Attention · ✓ SSM / Mamba (linear-time)
- **builds:** #16 SwiGLU: a gated FFN upgrade · #17 GQA: grouped-query attention (cheaper KV) · #18 SSM / Mamba: a running-state token mixer

### ✅ Module 9 — Build a GPT (nanoGPT → Llama) (100%)
- **skills:** ✓ Build a Llama-style block · ✓ KV cache for fast generation · ✓ BPE tokenizer
- **builds:** #12 Transformer block: residuals + stacking · #14 BPE tokenizer from scratch · #15 KV cache: O(n^2) -> O(n) generation

### ✅ Module 10 — Scaling, MLA & evaluation (100%)
- **skills:** ✓ Scaling laws (inference-optimal) · ✓ Multi-head Latent Attention · ✓ Held-out evaluation harness
- **builds:** #19 Scaling laws: predict loss + Chinchilla-optimal sizing · #20 Held-out eval: perplexity from scratch · #21 MLA: latent-compressed KV cache

### 🔄 Module 11 — GPU kernels (Triton, FlashAttn) (33%)
- **skills:** ✓ GPU memory hierarchy & MFU · · Triton kernels from zero · · FlashAttention (tiled attention kernel)
- **builds:** #22 GPU memory hierarchy & MFU

## All builds shipped (newest first)
| # | build | skills exercised | shipped |
|---|-------|------------------|---------|
| 22 | GPU memory hierarchy & MFU | GPU memory hierarchy & MFU, Arithmetic intensity & the roofline | 2026-08-10 |
| 21 | MLA: latent-compressed KV cache | Multi-head Latent Attention | 2026-08-10 |
| 20 | Held-out eval: perplexity from scratch | Held-out evaluation harness, Leakage-safe ML pipeline | 2026-08-10 |
| 19 | Scaling laws: predict loss + Chinchilla-optimal sizing | Scaling laws (inference-optimal) | 2026-08-10 |
| 18 | SSM / Mamba: a running-state token mixer | SSM / Mamba (linear-time) | 2026-08-10 |
| 17 | GQA: grouped-query attention (cheaper KV) | Grouped-Query Attention | 2026-08-10 |
| 16 | SwiGLU: a gated FFN upgrade | SwiGLU gated FFN | 2026-08-10 |
| 15 | KV cache: O(n^2) -> O(n) generation | KV cache for fast generation | 2026-08-10 |
| 14 | BPE tokenizer from scratch | BPE tokenizer | 2026-08-10 |
| 13 | Train attention: a learned attention weight | Autograd from scratch (micrograd), Self-attention from scratch, SGD, Adam & schedules | 2026-08-10 |
| 12 | Transformer block: residuals + stacking | Build a Llama-style block, Self-attention from scratch, RMSNorm | 2026-08-10 |
| 11 | RMSNorm | RMSNorm, Modern Python craft (uv, ruff, typing, CI) | 2026-08-10 |
| 10 | RoPE — rotary positions | RoPE rotary positions, Modern Python craft (uv, ruff, typing, CI) | 2026-08-10 |
| 9 | QKV attention (scaled dot-product) | Self-attention from scratch, Modern Python craft (uv, ruff, typing, CI) | 2026-08-10 |
| 8 | self-attention from scratch | Self-attention from scratch, Modern Python craft (uv, ruff, typing, CI), Numerically stable softmax & log-sum-exp | 2026-08-10 |
| 7 | an MLP that learns XOR | PyTorch tensors & training loop, Modern Python craft (uv, ruff, typing, CI), SGD, Adam & schedules, Autograd from scratch (micrograd) | 2026-08-10 |
| 6 | a layer of neurons | PyTorch tensors & training loop, Modern Python craft (uv, ruff, typing, CI) | 2026-08-08 |
| 5 | a real neuron | PyTorch tensors & training loop, SGD, Adam & schedules, Autograd from scratch (micrograd), Modern Python craft (uv, ruff, typing, CI) | 2026-08-08 |
| 4 | tiny net that learns | PyTorch tensors & training loop, SGD, Adam & schedules, Autograd from scratch (micrograd), Modern Python craft (uv, ruff, typing, CI) | 2026-08-08 |
| 3 | micrograd: autograd from scratch | Autograd from scratch (micrograd), Backprop as vector-Jacobian products, Modern Python craft (uv, ruff, typing, CI) | 2026-08-07 |
| 2 | Matmul FLOP estimator | Matmul, shapes & FLOP cost, Arithmetic intensity & the roofline, Numerically stable softmax & log-sum-exp | 2026-08-07 |
| 1 | Numerically stable softmax | — | 2026-08-06 |

