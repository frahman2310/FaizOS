// The audited Frontier-AI curriculum as a MAP (Phases 0–15) you free-build within — never a
// forced march. PHASES names the map; MISSION_TEMPLATES are the canonical shippable projects
// (each ends in a verifiable number). Suggestions come from here; you can always build anything.

export const PHASES: Record<number, string> = {
  0: 'Setup',
  1: 'Mathematics',
  2: 'Programming & CS',
  3: 'Classical ML',
  4: 'Deep Learning',
  5: 'Sequence & the Transformer',
  6: 'Building a Modern GPT',
  7: 'GPU Programming & Kernels',
  8: 'Distributed Training',
  9: 'Fine-tuning & Inference',
  10: 'RL & Post-training',
  11: 'Agents & Retrieval',
  12: 'Multimodal',
  13: 'Safety & Interpretability',
  14: 'Frontier Research',
  15: 'Capstone & Portfolio',
};

export interface MissionTemplate { id: string; title: string; phase: number; skills: string[]; acceptance: string; }

// The project spine (audit's roadmap + 8-rung portfolio ladder). Ordered by phase.
export const MISSION_TEMPLATES: MissionTemplate[] = [
  { id: 'stable-softmax', title: 'Numerically stable softmax + cross-entropy', phase: 1, skills: ['floating-point-logsumexp'], acceptance: 'naive overflows; stable sums to 1; CE matches -log softmax' },
  { id: 'matmul-flops', title: 'Matmul FLOP + roofline estimator', phase: 2, skills: ['linalg-matmul', 'roofline-cost-model'], acceptance: 'correct 2·M·N·K + compute/memory-bound verdicts' },
  { id: 'micrograd', title: 'micrograd: autograd from scratch', phase: 4, skills: ['autograd-backprop'], acceptance: 'trains a tiny net; grads match PyTorch' },
  { id: 'llama-block', title: 'nanoGPT → Llama-style block (RoPE+RMSNorm+SwiGLU+GQA+KV cache)', phase: 6, skills: ['nanogpt-llama-block', 'rope', 'kv-cache'], acceptance: 'loss curve + ablation of RoPE vs learned positions' },
  { id: 'triton-attention', title: 'Triton FlashAttention kernel', phase: 7, skills: ['triton-basics', 'flash-attention'], acceptance: 'correct vs SDPA + a speed/memory number' },
  { id: 'fsdp-run', title: 'Multi-GPU FSDP training run', phase: 8, skills: ['fsdp-run'], acceptance: 'MFU % + a scaling plot across GPU counts' },
  { id: 'inference-engine', title: 'Minimal inference engine (paged KV + continuous batching)', phase: 9, skills: ['inference-internals'], acceptance: 'tokens/s vs a naive baseline' },
  { id: 'reasoning-distill', title: 'Reasoning: distillation vs GRPO', phase: 10, skills: ['reasoning-distillation', 'rlvr-grpo'], acceptance: 'AIME/MATH-500 score per variant, with variance' },
  { id: 'agentic-rl', title: 'Agentic-RL agent', phase: 11, skills: ['agentic-rl'], acceptance: 'tau-bench / SWE-bench Verified number vs a baseline' },
  { id: 'real-sae', title: 'Real SAE on a model + feature steering', phase: 13, skills: ['interpretability-sae'], acceptance: 'an interpretable, steerable feature (ideally on Neuronpedia)' },
  { id: 'paper-repro', title: 'Reproduce a paper to a public number + a merged PR', phase: 14, skills: ['paper-reproduction', 'oss-contribution'], acceptance: 'matched metric + a merge link' },
];
