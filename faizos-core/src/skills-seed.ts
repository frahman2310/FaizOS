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
];
