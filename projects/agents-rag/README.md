# Agents & retrieval — RAG, memory, agentic RL, evals

**1. Production RAG.** Vector search finds MEANING but is blind to exact strings (`XR-4471B`); keyword search (BM25) is the reverse. Run both (HYBRID), retrieve ~50 cheap candidates, then RERANK to ~5 with a slow accurate model. Recall then precision: a chunk at rank 37 never reaches a top-5 context; reranking moves it to rank 2.

**2. Agent memory.** The context window is big but finite and it RESETS. Keep facts in a persistent store outside it and retrieve only what is relevant (10M-token history, 200k window -> retrieve 20 items x 500 tokens = 10k). FaizOS's own `insights` table is exactly this.

**3. Agentic RL.** An agent takes many steps and gets ONE reward at the end — the credit assignment problem. Blunt answer: credit the whole TRAJECTORY. advantage = reward - group_mean (GRPO again); every step gets the same value. Trajectory scoring 1.0 against a 0.4 group mean -> +0.6 on all 10 steps.

**4. Agent evals.** Agents are stochastic, so measure twice: pass@1 = RELIABILITY, pass@k = CAPABILITY. pass@1 40%/pass@8 75% (gap 35%) is a reliability problem — retries and verification. pass@1 35%/pass@8 38% (gap 3%) is a capability problem — you need a better model. Same low pass@1, opposite fixes. Plus TRACING: without per-step logs, a score tells you nothing actionable.

**Python rule learned:** comparison operators (`<=`, `>`) answer yes/no; arithmetic (`-`) gives a size.

Run: `python3 agents.py` -> PASS. Module 17 skills `rag-production`, `agent-memory`, `agentic-rl`, `agent-evals`. Completes Module 17.
