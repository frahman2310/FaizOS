# FaizOS — Content & Build Summary
_Auto-generated from your progress after every lesson/module (Stop hook). Do not edit by hand._

**80% coverage** · 14/20 modules complete · 42 builds shipped · 51/66 skills touched

```
OVERALL  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░ 80%
```

## Modules
### 🔄 Module 1 — Math: numbers, softmax, matmul (67%)
- **skills:** · Dev setup: uv, ruff, one Python, CI · ✓ Numerically stable softmax & log-sum-exp · ✓ Matmul, shapes & FLOP cost
- **builds:** #2 Matmul FLOP estimator · #8 self-attention from scratch · #23 Triton: a fused softmax kernel · #32 LoRA: fine-tune 0.1% of the parameters

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
- **builds:** #8 self-attention from scratch · #9 QKV attention (scaled dot-product) · #10 RoPE — rotary positions · #11 RMSNorm · #12 Transformer block: residuals + stacking · #13 Train attention: a learned attention weight · #24 FlashAttention: tiled attention with online softmax

### ✅ Module 8 — FFN, GQA & state-space models (100%)
- **skills:** ✓ SwiGLU gated FFN · ✓ Grouped-Query Attention · ✓ SSM / Mamba (linear-time)
- **builds:** #16 SwiGLU: a gated FFN upgrade · #17 GQA: grouped-query attention (cheaper KV) · #18 SSM / Mamba: a running-state token mixer

### ✅ Module 9 — Build a GPT (nanoGPT → Llama) (100%)
- **skills:** ✓ Build a Llama-style block · ✓ KV cache for fast generation · ✓ BPE tokenizer
- **builds:** #12 Transformer block: residuals + stacking · #14 BPE tokenizer from scratch · #15 KV cache: O(n^2) -> O(n) generation

### ✅ Module 10 — Scaling, MLA & evaluation (100%)
- **skills:** ✓ Scaling laws (inference-optimal) · ✓ Multi-head Latent Attention · ✓ Held-out evaluation harness
- **builds:** #19 Scaling laws: predict loss + Chinchilla-optimal sizing · #20 Held-out eval: perplexity from scratch · #21 MLA: latent-compressed KV cache

### ✅ Module 11 — GPU kernels (Triton, FlashAttn) (100%)
- **skills:** ✓ GPU memory hierarchy & MFU · ✓ Triton kernels from zero · ✓ FlashAttention (tiled attention kernel)
- **builds:** #22 GPU memory hierarchy & MFU · #23 Triton: a fused softmax kernel · #24 FlashAttention: tiled attention with online softmax

### ✅ Module 12 — Compile, profile & parallelism (100%)
- **skills:** ✓ torch.compile & CUDA graphs · ✓ Profiling with Nsight / torch profiler · ✓ Parallelism: data/tensor/pipeline/expert/sequence/context
- **builds:** #25 torch.compile &amp; CUDA graphs · #26 Profiling: Amdahl&#39;s law &amp; finding the real bottleneck · #27 Parallelism axes: data, tensor, pipeline

### ✅ Module 13 — Distributed training (100%)
- **skills:** ✓ FSDP multi-GPU training run · ✓ Pipeline schedules (1F1B, zero-bubble, DualPipe) · ✓ NCCL collectives & interconnect · ✓ Async & fault-tolerant checkpointing
- **builds:** #28 Collectives: all-reduce, reduce-scatter, all-gather · #29 FSDP / ZeRO: shard the whole training state · #30 Pipeline schedules: GPipe vs 1F1B · #31 Fault-tolerant checkpointing: the optimal interval

### ✅ Module 14 — Fine-tuning & inference (100%)
- **skills:** ✓ PEFT: LoRA / QLoRA / DoRA · ✓ Quantization (GPTQ/AWQ/GGUF/FP8/FP4, KV-quant) · ✓ Inference internals: paged KV, continuous batching, speculative decoding · ✓ Serving: vLLM / SGLang / TensorRT-LLM / Dynamo
- **builds:** #32 LoRA: fine-tune 0.1% of the parameters · #33 Quantization: run a model in 4 bits · #34 Inference internals: paged KV, continuous batching, speculative decoding · #35 Serving stacks: prefill vs decode, throughput vs latency

### ✅ Module 15 — RL foundations (100%)
- **skills:** ✓ RL foundations: MDP, policy gradient, PPO · ✓ RLVR & GRPO (Dr.GRPO/DAPO/GSPO) · ✓ Reward models & verifiers (PRM vs ORM)
- **builds:** #36 RL foundations: REINFORCE, baselines and PPO clipping · #37 GRPO: group-relative RL with verifiable rewards · #38 Reward modeling: preferences, proxies and reward hacking

### ✅ Module 16 — Post-training & tools (100%)
- **skills:** ✓ Reasoning distillation vs RL · ✓ SFT, RLHF, DPO & variants · ✓ Tool calling (Responses API, Anthropic tool-use, MCP)
- **builds:** #39 Post-training: distillation vs RL, DPO, and tool calling

### ✅ Module 17 — Agents & retrieval (RAG) (100%)
- **skills:** ✓ Production RAG (hybrid + rerank + GraphRAG) · ✓ Agent memory (persistent: mem0/Letta) · ✓ Agentic RL over multi-turn tool use · ✓ Agent evals (tau-bench, SWE-bench, GAIA) + tracing
- **builds:** #40 Agents &amp; retrieval: RAG, memory, agentic RL, evals

### ✅ Module 18 — Multimodal (100%)
- **skills:** ✓ ViT, CLIP & SigLIP · ✓ Diffusion & flow matching / rectified flow · ✓ VLM fusion patterns
- **builds:** #41 Multimodal: ViT/CLIP, diffusion &amp; flow matching, VLM fusion

### ✅ Module 19 — Safety & interpretability (100%)
- **skills:** ✓ Alignment: RLAIF, scalable oversight, weak-to-strong, debate · ✓ Interpretability: SAEs + circuit tracing · ✓ Prompt-injection defenses & red-teaming
- **builds:** #42 Safety &amp; interpretability: oversight, SAEs, prompt injection

## All builds shipped (newest first)
| # | build | skills exercised | shipped |
|---|-------|------------------|---------|
| 42 | Safety &amp; interpretability: oversight, SAEs, prompt injection | Alignment: RLAIF, scalable oversight, weak-to-strong, debate, Interpretability: SAEs + circuit tracing, Prompt-injection defenses & red-teaming | 2026-08-13 |
| 41 | Multimodal: ViT/CLIP, diffusion &amp; flow matching, VLM fusion | ViT, CLIP & SigLIP, Diffusion & flow matching / rectified flow, VLM fusion patterns | 2026-08-13 |
| 40 | Agents &amp; retrieval: RAG, memory, agentic RL, evals | Production RAG (hybrid + rerank + GraphRAG), Agent memory (persistent: mem0/Letta), Agentic RL over multi-turn tool use, agent-evals | 2026-08-13 |
| 39 | Post-training: distillation vs RL, DPO, and tool calling | Reasoning distillation vs RL, SFT, RLHF, DPO & variants, Tool calling (Responses API, Anthropic tool-use, MCP) | 2026-08-13 |
| 38 | Reward modeling: preferences, proxies and reward hacking | Reward models & verifiers (PRM vs ORM) | 2026-08-13 |
| 37 | GRPO: group-relative RL with verifiable rewards | RLVR & GRPO (Dr.GRPO/DAPO/GSPO) | 2026-08-13 |
| 36 | RL foundations: REINFORCE, baselines and PPO clipping | RL foundations: MDP, policy gradient, PPO | 2026-08-13 |
| 35 | Serving stacks: prefill vs decode, throughput vs latency | Serving: vLLM / SGLang / TensorRT-LLM / Dynamo | 2026-08-12 |
| 34 | Inference internals: paged KV, continuous batching, speculative decoding | Inference internals: paged KV, continuous batching, speculative decoding | 2026-08-12 |
| 33 | Quantization: run a model in 4 bits | Quantization (GPTQ/AWQ/GGUF/FP8/FP4, KV-quant) | 2026-08-12 |
| 32 | LoRA: fine-tune 0.1% of the parameters | PEFT: LoRA / QLoRA / DoRA, Matmul, shapes & FLOP cost | 2026-08-12 |
| 31 | Fault-tolerant checkpointing: the optimal interval | Async & fault-tolerant checkpointing | 2026-08-11 |
| 30 | Pipeline schedules: GPipe vs 1F1B | Pipeline schedules (1F1B, zero-bubble, DualPipe) | 2026-08-11 |
| 29 | FSDP / ZeRO: shard the whole training state | FSDP multi-GPU training run | 2026-08-11 |
| 28 | Collectives: all-reduce, reduce-scatter, all-gather | NCCL collectives & interconnect | 2026-08-11 |
| 27 | Parallelism axes: data, tensor, pipeline | Parallelism: data/tensor/pipeline/expert/sequence/context | 2026-08-11 |
| 26 | Profiling: Amdahl&#39;s law &amp; finding the real bottleneck | Profiling with Nsight / torch profiler | 2026-08-11 |
| 25 | torch.compile &amp; CUDA graphs | torch.compile & CUDA graphs | 2026-08-11 |
| 24 | FlashAttention: tiled attention with online softmax | FlashAttention (tiled attention kernel), Self-attention from scratch | 2026-08-10 |
| 23 | Triton: a fused softmax kernel | Triton kernels from zero, Numerically stable softmax & log-sum-exp | 2026-08-10 |
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

