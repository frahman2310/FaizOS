# Frontier

Rolling ingest, grouped by the track it affects. Generated from the database.
A track older than 60 days is flagged: its content may have drifted.

## T0 Python and engineering for machine learning
No ingested items yet.

## T1 PyTorch fluency
No ingested items yet.

## T2 Train a real model, and learn how to know whether it worked
- Muon is confirmed at frontier scale (2026-08-14) DeepSeek V4 discloses Muon in production, the first frontier scale disclosure. No evidence of Shampoo, SOAP or true second order methods in production runs. modded-nanogpt already uses it; it lands in T2 as a working component. https://github.com/KellerJordan/modded-nanogpt

## T3 Modern architecture, as of 2026
- MoE went extremely sparse (2026-08-14) Active fractions of 3 to 5 percent (DeepSeek V4-Pro 3.1, Kimi K3 3.7, Qwen3.5 4.3). Expert counts to 896 with top-16. LatentMoE appeared at Moonshot and NVIDIA independently: routing and compute in a reduced latent dimension. Consumer consequence: a 35B-A3B MoE at 4 bit beats a 27B dense at 4 bit on memory and speed. https://huggingface.co/models
- Residual stream engineering became a thing (2026-08-14) Manifold constrained hyper-connections restore the identity mapping that plain hyper-connections break, shipped in DeepSeek V4. Kimi K3 Attention Residuals is a parallel thread. Direct descendant of the residual lesson: 30 blocks gave RMS 27.7 with residuals versus 0.07 without. https://arxiv.org/list/cs.LG/recent
- The attention consensus collapsed (2026-08-14) The GQA/MLA monoculture is gone. Qwen3.5 runs Gated DeltaNet linear attention 3:1, Kimi K3 runs KDA plus Gated MLA, GLM-5 layers DeepSeek Sparse Attention on MLA, MiniMax M2.5 deliberately runs full MHA, Gemma 4 runs sliding window plus global, Nemotron 3 runs Mamba-2 with attention anchors. RoPE, GQA and MLA builds stay correct as the baseline the variations are measured against. https://huggingface.co/models

## T4 Kernels and the hardware
- Kernels: bottleneck moved off matmul, Python became competitive (2026-08-14) FlashAttention 4 is the reference text: Blackwell scales tensor cores but not the other units, so softmax and exponentials become the bottleneck. Written in CuTe DSL in Python, 20 to 30x faster compiles. With Inductor CuTe backend and Helion, C++ templates are no longer the entry fee for state of the art kernels. That fact makes T4 feasible. https://arxiv.org/abs/2501.01005

## T5 Inference and serving
- Inference: the interesting layer moved above the engine (2026-08-14) Prefix caching is default on; the work moved to tiered KV storage and disaggregated prefill/decode (RDMA required for production). Decode context parallelism: 6091 tok/s/GPU at 512 concurrency on MLA models. Speculative decoding moved to parallel drafting (P-EAGLE, DFlash); MTP heads ship in weights so speculation needs no drafter. https://docs.vllm.ai
- Precision fell to four bits in production (2026-08-14) FP8 is the floor. FP4 shipped: DeepSeek V4 FP4 experts, Kimi K3 MXFP4 weights via QAT, Nemotron 3 trained in NVFP4. Decision rule on Blackwell: NVFP4 for weights at 30B and above, MXFP4 where the checkpoint ships it, FP8 elsewhere. NVFP4 recovery improves with scale, 99 percent at 70B but 95 to 98 at 7 to 14B. https://arxiv.org/list/cs.LG/recent

## T6 Post-training and RL
- Post-training moved past plain GRPO (2026-08-14) The 2026 default is a GRPO family recipe: clip-higher, dynamic sampling, sequence level or reshaped importance ratio, off policy. DAPO, GSPO, CISPO, VESPO are shipped loss types. ScaleRL: RL compute curves are sigmoidal, recipe choices split into asymptote movers and efficiency movers. Length bias impossibility: no weighting is both gradient unbiased and length invariant. https://arxiv.org/list/cs.LG/recent

## T7 Agents, harnesses and evaluation
- Agents: the verification gap and the context ceiling (2026-08-14) Marginal test time compute is better spent on a better verifier or selector than on more samples or longer traces. OSWorld 2.0: best model 20.6 percent on long horizon computer use. ARC-AGI-3: frontier models at 0.5 percent where humans hit 100. Computer use and novel interactive environments are the open research ground. https://os-world.github.io

## T8 Multimodal and retrieval
No ingested items yet.

## T9 Safety, interpretability and evaluation as a discipline
No ingested items yet.

## T10 Ship
No ingested items yet.

## General
- [6.10] Who publishes: the open weight frontier is Chinese plus Gemma (2026-08-14) https://huggingface.co/google/gemma-4-27b-it
