// Seed skills for the MVP: Phases 1–6 of the AUDITED curriculum (the foundations spine).
// Treated as a "skills you acquire by building" map, not a syllabus. `build_hint` is the
// canonical way to acquire the skill by building something real.
export interface SeedSkill { id: string; name: string; phase: number; must_know: boolean; build_hint: string; }

export const skillsSeed: SeedSkill[] = [
  // Phase 1 — Mathematics
  { id: 'floating-point-logsumexp', name: 'Numerically stable softmax & log-sum-exp', phase: 1, must_know: true, build_hint: 'Implement softmax + cross-entropy from scratch; make naive overflow, then fix with the max-subtraction trick.' },
  { id: 'linalg-matmul', name: 'Matmul, shapes & FLOP cost', phase: 1, must_know: true, build_hint: 'Write a matmul FLOP estimator; reason about arithmetic intensity for a real layer.' },
  { id: 'svd-lowrank', name: 'SVD & low-rank (PCA, LoRA)', phase: 1, must_know: false, build_hint: 'Compress a matrix with truncated SVD; measure reconstruction error vs rank.' },
  { id: 'matrix-calculus-vjp', name: 'Backprop as vector-Jacobian products', phase: 1, must_know: true, build_hint: 'Derive and code the VJP for a linear + softmax layer by hand.' },
  { id: 'probability-covariance', name: 'Probability, covariance & expectation', phase: 1, must_know: false, build_hint: 'Estimate a covariance matrix from samples; visualize the principal axes.' },
  { id: 'highdim-geometry', name: 'High-dimensional geometry', phase: 1, must_know: false, build_hint: 'Show near-orthogonality of random vectors as dimension grows; explain cosine similarity.' },

  // Phase 2 — Programming & CS
  { id: 'python-craft', name: 'Modern Python craft (uv, ruff, typing, CI)', phase: 2, must_know: true, build_hint: 'Set up a repo with uv + ruff + type hints + a GitHub Actions CI that runs tests.' },
  { id: 'data-structures', name: 'Core data structures & complexity', phase: 2, must_know: false, build_hint: 'Implement the few structures a real pipeline needs; reason about Big-O of the hot path.' },
  { id: 'roofline-cost-model', name: 'Arithmetic intensity & the roofline', phase: 2, must_know: true, build_hint: 'Estimate whether a kernel is compute- or memory-bound; sketch its roofline.' },
  { id: 'profiling', name: 'Profiling (cProfile, torch profiler)', phase: 2, must_know: false, build_hint: 'Profile a slow script, find the bottleneck, and make it measurably faster.' },

  // Phase 3 — Classical ML
  { id: 'regression-from-scratch', name: 'Regression from scratch', phase: 3, must_know: false, build_hint: 'Implement linear + logistic regression with gradient descent, no sklearn.' },
  { id: 'ml-lifecycle-leakage', name: 'Leakage-safe ML pipeline', phase: 3, must_know: true, build_hint: 'Build a scikit-learn pipeline on a real dataset with no train/test leakage.' },
  { id: 'double-descent', name: 'Bias-variance & double descent', phase: 3, must_know: false, build_hint: 'Reproduce a double-descent curve on a small model; explain the interpolation regime.' },
  { id: 'pca-svd', name: 'PCA via SVD', phase: 3, must_know: false, build_hint: 'Do PCA the stable way (via SVD); compare to the covariance-eigendecomposition route.' },

  // Phase 4 — Deep learning
  { id: 'autograd-backprop', name: 'Autograd from scratch (micrograd)', phase: 4, must_know: true, build_hint: 'Build a micrograd-style autograd engine, then re-derive the same net in PyTorch.' },
  { id: 'pytorch-basics', name: 'PyTorch tensors & training loop', phase: 4, must_know: true, build_hint: 'Write a clean training loop (data → forward → loss → backward → step) from scratch.' },
  { id: 'optimization-adam', name: 'SGD, Adam & schedules', phase: 4, must_know: false, build_hint: 'Implement Adam from the update rule; watch a loss curve respond to the schedule.' },
  { id: 'init-normalization', name: 'Initialization & normalization', phase: 4, must_know: false, build_hint: 'Break training with bad init, then fix it; compare LayerNorm vs RMSNorm behavior.' },
  { id: 'torch-compile', name: 'torch.compile & CUDA graphs', phase: 4, must_know: false, build_hint: 'Wrap a model in torch.compile; measure the speedup and where it comes from.' },

  // Phase 5 — Sequence modeling & the modern transformer
  { id: 'attention', name: 'Self-attention from scratch', phase: 5, must_know: true, build_hint: 'Implement scaled dot-product + multi-head attention by hand; verify shapes.' },
  { id: 'rope', name: 'RoPE rotary positions', phase: 5, must_know: true, build_hint: 'Add RoPE to attention; ablate it vs learned positions and read the length-generalization delta.' },
  { id: 'rmsnorm', name: 'RMSNorm', phase: 5, must_know: false, build_hint: 'Swap LayerNorm for RMSNorm in your block; confirm training still converges.' },
  { id: 'swiglu', name: 'SwiGLU gated FFN', phase: 5, must_know: false, build_hint: 'Replace the GELU FFN with a gated SwiGLU (8/3 width); compare loss.' },
  { id: 'gqa', name: 'Grouped-Query Attention', phase: 5, must_know: false, build_hint: 'Convert MHA to GQA; measure the KV-memory reduction.' },
  { id: 'ssm-mamba', name: 'SSM / Mamba (linear-time)', phase: 5, must_know: false, build_hint: 'Implement a minimal SSM scan; contrast its cost with attention.' },

  // Phase 6 — Building a modern GPT
  { id: 'nanogpt-llama-block', name: 'Build a Llama-style block', phase: 6, must_know: true, build_hint: 'Build nanoGPT, then modernize it: RoPE + RMSNorm + SwiGLU + GQA. Benchmark the delta.' },
  { id: 'kv-cache', name: 'KV cache for fast generation', phase: 6, must_know: true, build_hint: 'Add a KV cache to your generation loop; show it turns O(n^2) decoding into O(n).' },
  { id: 'scaling-laws', name: 'Scaling laws (inference-optimal)', phase: 6, must_know: false, build_hint: 'Fit a tiny scaling curve; explain why 2026 over-trains past Chinchilla for inference economics.' },
  { id: 'mla', name: 'Multi-head Latent Attention', phase: 6, must_know: false, build_hint: 'Sketch MLA latent-KV compression; contrast its KV footprint with GQA.' },
  { id: 'tokenizer-bpe', name: 'BPE tokenizer', phase: 6, must_know: false, build_hint: 'Train a small BPE tokenizer; inspect merges and vocab coverage.' },
  { id: 'heldout-eval', name: 'Held-out evaluation harness', phase: 6, must_know: true, build_hint: 'Build an eval harness: perplexity + one downstream task, reported as a real number.' },

  // Phase 0 — Setup
  { id: 'dev-setup', name: 'Dev setup: uv, ruff, one Python, CI', phase: 0, must_know: false, build_hint: 'Stand up a clean repo with uv + ruff + type hints + a passing GitHub Actions CI.' },

  // Phase 7 — GPU programming & kernels
  { id: 'gpu-memory-hierarchy', name: 'GPU memory hierarchy & MFU', phase: 7, must_know: true, build_hint: 'Compute a kernel’s Model-FLOPs-Utilization; explain SRAM vs HBM movement.' },
  { id: 'triton-basics', name: 'Triton kernels from zero', phase: 7, must_know: true, build_hint: 'Write a fused softmax kernel in Triton and beat the PyTorch baseline.' },
  { id: 'flash-attention', name: 'FlashAttention (tiled attention kernel)', phase: 7, must_know: true, build_hint: 'Implement a tiled attention kernel; match SDPA and report a speed/memory number.' },
  { id: 'torch-compile-cuda-graphs', name: 'torch.compile & CUDA graphs', phase: 7, must_know: false, build_hint: 'Wrap a model in torch.compile; measure the speedup and where it comes from.' },
  { id: 'profiling-nsight', name: 'Profiling with Nsight / torch profiler', phase: 7, must_know: false, build_hint: 'Profile a kernel, find the bottleneck, make it measurably faster.' },

  // Phase 8 — Distributed training
  { id: 'parallelism-axes', name: 'Parallelism: data/tensor/pipeline/expert/sequence/context', phase: 8, must_know: true, build_hint: 'Justify a parallelism plan for a given model + cluster on paper, then shard.' },
  { id: 'fsdp-run', name: 'FSDP multi-GPU training run', phase: 8, must_know: true, build_hint: 'Shard a small model across 2–8 rented GPUs; log MFU and a scaling plot.' },
  { id: 'pipeline-schedules', name: 'Pipeline schedules (1F1B, zero-bubble, DualPipe)', phase: 8, must_know: false, build_hint: 'Simulate a pipeline schedule; measure the bubble.' },
  { id: 'collectives-interconnect', name: 'NCCL collectives & interconnect', phase: 8, must_know: false, build_hint: 'Benchmark an all-reduce; reason about comm/compute overlap.' },
  { id: 'fault-tolerant-checkpointing', name: 'Async & fault-tolerant checkpointing', phase: 8, must_know: false, build_hint: 'Add resumable, async checkpointing to a training loop.' },

  // Phase 9 — Efficient fine-tuning & inference
  { id: 'peft-lora', name: 'PEFT: LoRA / QLoRA / DoRA', phase: 9, must_know: true, build_hint: 'Fine-tune a small model with QLoRA; report the eval delta.' },
  { id: 'quantization', name: 'Quantization (GPTQ/AWQ/GGUF/FP8/FP4, KV-quant)', phase: 9, must_know: false, build_hint: 'Quantize a model; measure size vs quality tradeoff.' },
  { id: 'inference-internals', name: 'Inference internals: paged KV, continuous batching, speculative decoding', phase: 9, must_know: true, build_hint: 'Build a minimal inference engine with a paged KV cache; report tokens/s vs a baseline.' },
  { id: 'serving-stacks', name: 'Serving: vLLM / SGLang / TensorRT-LLM / Dynamo', phase: 9, must_know: false, build_hint: 'Serve a model with vLLM; benchmark throughput at a stated batch/context.' },

  // Phase 10 — RL & post-training
  { id: 'rl-foundations', name: 'RL foundations: MDP, policy gradient, PPO', phase: 10, must_know: true, build_hint: 'Implement REINFORCE then PPO on a toy task; read the reward curve.' },
  { id: 'rlvr-grpo', name: 'RLVR & GRPO (Dr.GRPO/DAPO/GSPO)', phase: 10, must_know: true, build_hint: 'Run GRPO on a verifiable task; report the reward curve and a benchmark number.' },
  { id: 'reward-modeling-verifiers', name: 'Reward models & verifiers (PRM vs ORM)', phase: 10, must_know: false, build_hint: 'Train a reward model; demonstrate a reward hack and its fix.' },
  { id: 'reasoning-distillation', name: 'Reasoning distillation vs RL', phase: 10, must_know: true, build_hint: 'Compare R1-style distillation vs GRPO on AIME/MATH-500 with seeds + ablations.' },
  { id: 'rlhf-dpo', name: 'SFT, RLHF, DPO & variants', phase: 10, must_know: false, build_hint: 'Align a small model with DPO; show the preference win-rate.' },

  // Phase 11 — Agents, tools & retrieval
  { id: 'tool-calling', name: 'Tool calling (Responses API, Anthropic tool-use, MCP)', phase: 11, must_know: true, build_hint: 'Build an agent loop that calls real tools and traces its steps.' },
  { id: 'rag-production', name: 'Production RAG (hybrid + rerank + GraphRAG)', phase: 11, must_know: true, build_hint: 'Build hybrid retrieval + a cross-encoder reranker; eval on a public benchmark.' },
  { id: 'agent-memory', name: 'Agent memory (persistent: mem0/Letta)', phase: 11, must_know: false, build_hint: 'Give a long-horizon agent persistent memory.' },
  { id: 'agentic-rl', name: 'Agentic RL over multi-turn tool use', phase: 11, must_know: true, build_hint: 'Train a small agent with RL on tau-bench or SWE-bench Verified.' },
  { id: 'agent-evals-tracing', name: 'Agent evals (tau-bench, SWE-bench, GAIA) + tracing', phase: 11, must_know: false, build_hint: 'Evaluate an agent on a public benchmark with full tracing.' },

  // Phase 12 — Multimodal
  { id: 'vit-clip-siglip', name: 'ViT, CLIP & SigLIP', phase: 12, must_know: false, build_hint: 'Fine-tune a small CLIP; probe zero-shot accuracy.' },
  { id: 'diffusion-flow-matching', name: 'Diffusion & flow matching / rectified flow', phase: 12, must_know: true, build_hint: 'Train a small flow-matching image model; sample from it.' },
  { id: 'vlm-fusion', name: 'VLM fusion patterns', phase: 12, must_know: false, build_hint: 'Wire a vision encoder to an LLM; caption images.' },

  // Phase 13 — Safety, interpretability & security
  { id: 'alignment-methods', name: 'Alignment: RLAIF, scalable oversight, weak-to-strong, debate', phase: 13, must_know: false, build_hint: 'Reproduce a small Constitutional-AI / RLAIF loop.' },
  { id: 'interpretability-sae', name: 'Interpretability: SAEs + circuit tracing', phase: 13, must_know: true, build_hint: 'Train a real SAE on a model’s residual stream; find and steer a feature.' },
  { id: 'ai-security', name: 'Prompt-injection defenses & red-teaming', phase: 13, must_know: false, build_hint: 'Build a red-team suite; test injection defenses (CaMeL, constitutional classifiers).' },

  // Phase 14 — Frontier research
  { id: 'research-method', name: 'Research method: seeds, ablations, compute-matched baselines', phase: 14, must_know: true, build_hint: 'Run a compute-matched ablation with pinned seeds and a logged config.' },
  { id: 'paper-reproduction', name: 'Reproduce a paper to a public number', phase: 14, must_know: true, build_hint: 'Reproduce a recent result; match the reported metric within noise.' },
  { id: 'oss-contribution', name: 'Merged PR into vLLM/TRL/transformers', phase: 14, must_know: true, build_hint: 'Land a merged pull request in a major repo.' },

  // Phase 15 — Capstone
  { id: 'capstone-portfolio', name: 'Capstone: the 8-rung portfolio', phase: 15, must_know: true, build_hint: 'Assemble the 8 hire-grade artifacts, each with a public number.' },
];
