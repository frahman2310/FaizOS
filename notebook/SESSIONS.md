# FaizOS — Session Log
_Auto-written after every session by the Stop hook. Newest first._

<!-- session 2026-08-12T11:56:44.943Z -->
## 2026-08-12 — 3 ships
**Shipped:** Quantization: run a model in 4 bits · Inference internals: paged KV, continuous batching, speculative decoding · Serving stacks: prefill vs decode, throughput vs latency
**Learned:** LoRA — fine-tune 0.8% of the parameters · Quantization — run a model in 4 bits · Inference internals — paged KV, continuous batching, speculative decoding · Serving stacks — prefill vs decode, throughput vs latency
**🏁 Milestones:** Module 14 Complete — Fine-tuning &amp; inference
**Coverage:** 55% · 9/20 modules complete · 35 total ships
<!-- /session 2026-08-12T11:56:44.943Z -->

<!-- session 2026-08-11T11:06:56.391Z -->
## 2026-08-11 — 3 ships
**Shipped:** FSDP / ZeRO: shard the whole training state · Pipeline schedules: GPipe vs 1F1B · Fault-tolerant checkpointing: the optimal interval
**Learned:** Collectives — all-reduce, reduce-scatter, all-gather · FSDP / ZeRO — shard the whole training state · Pipeline schedules — GPipe vs 1F1B · Fault-tolerant checkpointing — the optimal interval
**🏁 Milestones:** Module 13 Complete — Distributed training
**Coverage:** 50% · 8/20 modules complete · 31 total ships
<!-- /session 2026-08-11T11:06:56.391Z -->

<!-- session 2026-08-11T09:22:47.735Z -->
## 2026-08-11 — 2 ships
**Shipped:** Profiling: Amdahl&#39;s law &amp; finding the real bottleneck · Parallelism axes: data, tensor, pipeline
**Learned:** torch.compile &amp; CUDA graphs · Profiling — Amdahl&#39;s law &amp; the real bottleneck · Parallelism axes — data, tensor, pipeline
**🏁 Milestones:** Module 12 Complete — Compile, profile &amp; parallelism
**Coverage:** 45% · 7/20 modules complete · 27 total ships
<!-- /session 2026-08-11T09:22:47.735Z -->

<!-- session 2026-08-10T14:31:14.815Z -->
## 2026-08-10 — 9 ships
**Shipped:** SwiGLU: a gated FFN upgrade · GQA: grouped-query attention (cheaper KV) · SSM / Mamba: a running-state token mixer · Scaling laws: predict loss + Chinchilla-optimal sizing · Held-out eval: perplexity from scratch · MLA: latent-compressed KV cache · GPU memory hierarchy & MFU · Triton: a fused softmax kernel · FlashAttention: tiled attention with online softmax
**Learned:** SwiGLU — a gated FFN upgrade · GQA — grouped-query attention · SSM / Mamba — a running-state token mixer · Scaling laws — predict loss + Chinchilla sizing · Held-out eval — perplexity · MLA — Multi-head Latent Attention · GPU memory hierarchy & MFU · Triton — a fused softmax kernel · FlashAttention — tiled attention with online softmax
**🏁 Milestones:** Module 8 Complete — FFN, GQA & state-space models · Module 10 Complete — Scaling, MLA & evaluation · Module 11 Complete — GPU kernels (Triton, FlashAttention)
**Coverage:** 40% · 6/20 modules complete · 24 total ships
<!-- /session 2026-08-10T14:31:14.815Z -->

<!-- session 2026-08-10T11:35:06.154Z -->
## 2026-08-10 — 4 ships
**Shipped:** Transformer block: residuals + stacking · Train attention: a learned attention weight · BPE tokenizer from scratch · KV cache: O(n^2) -> O(n) generation
**Learned:** Transformer block — residuals + stacking · Train attention — a learned attention weight · BPE tokenizer from scratch · KV cache — fast generation
**🏁 Milestones:** Module 9 Complete — Build a GPT (nanoGPT → Llama)
**Coverage:** 24% · 3/20 modules complete · 15 total ships
<!-- /session 2026-08-10T11:35:06.154Z -->

<!-- session 2026-08-10-earlier -->
## 2026-08-10 (earlier) — 5 ships
**Shipped:** an MLP that learns XOR · self-attention from scratch · QKV attention (scaled dot-product) · RoPE — rotary positions · RMSNorm
**Learned:** MLP & XOR · self-attention · QKV scaled dot-product · RoPE (rotary positions) · RMSNorm
**🏁 Milestones:** Module 7 Complete — Attention & modern block basics
**Coverage:** 19% · 2/20 modules complete · 11 total ships (at the time)
<!-- /session 2026-08-10-earlier -->

