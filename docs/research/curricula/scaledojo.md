# ScaleDojo: the platform behind the Instagram account

Fetched 2026-09-24 from https://scaledojo.dev (public pages). The Instagram account (146 posts, analysed
2026-09-01 in docs/project-reasoning.md) is the marketing arm of this platform: every post is a real
onsite interview question answered in numbered steps, and the platform is where you practise them.

## What it is
An interactive system-design practice platform, Indian-priced. Tagline: "Stop Reading About System Design.
Start Building It." You design by dragging components onto a canvas (no code), stress it in a failure
simulator ("Murphy's Lab": crashes, partitions, traffic spikes, live latency and error rate), and get an
AI critique of the design. Tracks: HLD (100 levels), LLD (80), API design (50), GenAI Systems (50 plus 8
tutorial levels), algorithms (76), AI Lab (72), SQL (50 cases).

## How the AI Engineering course works (scaledojo.dev/genai/learn/welcome/how-this-course-works)
- Tiers → modules → chapters of 2 to 4 minutes' reading each; read in order.
- A chapter is passed by reading it or scoring 70%+ on its quiz; module completion gives XP.
- Phase 1 has no lab work. In Phase 2 nearly every module ends with links into GenAI Lab levels.
- Lessons are readable free without login (about 700-800 words, one short code block, a worked
  example with named data, an interactive demo). The quiz and "interview signal" are Pro only.

## The course, in order (scaledojo.dev/genai/learn)
**Phase 1 · AI/ML foundations** (47 chapters): welcome (3) · what is intelligence (3) · how machines
learn: supervised, unsupervised, RL, self-supervised (4) · the math you actually need: vectors,
probability, loss, optimisation without calculus, similarity/softmax/attention scores, norms, entropy
and KL (7) · classical ML toolbox (6) · neural networks from first principles: perceptron to
backprop, optimisers, training stability, preview of transformers (8) · data, training and the ML
pipeline, including train/validation/test splits (5) · evaluation and failure modes: precision,
recall, ROC-AUC, over/underfitting, bias-variance, regularisation (4) · ethics, safety, responsible AI
(4) · bridge to generative AI (3).

**Phase 2 · Generative AI and LLM engineering** (55 chapters):
1. Welcome (2)
2. Tokens, embeddings and memory (3): tokenisation, embeddings, context windows
3. Prompting and model behaviour (4): prompting, temperature and sampling, the economics of LLM calls, streaming and latency
4. Safety, model choice and first agents (3)
5. Document ingestion and chunking (2)
6. Vector search fundamentals (3): vector databases, hybrid search, reranking
7. Building the RAG pipeline (3): context assembly, citations and grounding, multimodal retrieval
8. Conversational RAG and evaluation (2): follow-ups, faithfulness and relevance
9. Giving LLMs tools (2): function calling, ReAct
10. Planning and agent memory (2)
11. Multi-agent systems and execution (3): collaboration, sandboxed code, human-in-the-loop
12. Hardening agents (3): retries, agent evaluation, orchestration
13. Serving, caching and gateways (3)
14. Fine-tuning and evaluation at scale (2): fine-tune vs prompt, offline and online evals
15. Guardrails, cost and observability (3)
16. Testing and resilience in production (2): A/B tests, disaster recovery and failover
17. Capstone: designing full GenAI systems (7): a method for any GenAI design, 5 worked examples, graduation checklist
18. Transformers under the hood (4): attention, masking and positions, RMSNorm and a block, scaling laws, quantisation, MoE
19. Reinforcement learning for LLMs (4): RL basics, policy gradients, PPO/RLHF and reasoning models, DPO and test-time compute
20. Diffusion and multimodal generation (3)

## The GenAI Systems Lab, in order (scaledojo.dev/genai)
Each level is a named company with a constraint; you design the system on the canvas.
- **Act 0, tutorial (−8 to −1):** LLM basics, system prompts, memory, embeddings, chunking, guardrails, cost, first RAG pipeline.
- **Act 1 (1-10):** tokens and cost, embeddings, context limits, temperature, prompt design, cost optimisation and tiered routing, streaming, safety net, model routing, first agent.
- **Act 2 (11-20):** document ingestion (PDF, OCR), chunking, vector DB indexing (HNSW vs IVF), hybrid BM25+vector, reranking, context assembly, citations and hallucination detection, multimodal retrieval, conversational RAG, RAG evaluation.
- **Act 3 (21-30):** tool design, ReAct, planning, agent memory, multi-agent, code execution, human-in-the-loop, error handling, agent evaluation, orchestration.
- **Act 4 (31-40):** serving (vLLM/TGI, batching, KV cache), gateways, semantic caching, LoRA fine-tuning, benchmarking and human eval, guardrails, cost control, observability, A/B testing, disaster recovery.
- **Act 5 (41-50):** full systems: enterprise RAG, support, code assistant, moderation, AI search, AI tutor, trading agent, multimodal, AI OS, "AGI scaffold".

## Access and price (scaledojo.dev pricing, INR)
- Free: 12 HLD levels, GenAI primer levels, lesson text, 20 credits then 5 a day.
- Pro ₹4,999 (₹3,499 yearly): 40 GenAI levels, quizzes, mock interviews, 800 AI credits.
- Architect ₹6,999 (₹4,899 yearly): all 486 challenges, 3,000 credits.
- 7-day full refund.

## Fit for Faiz
- Design by dragging and judging, not coding: matches his stated way of working (C30, 09-12).
- 2 to 4 minute chapters, one idea each: matches what worked (B5, B8) and the bootcamp's short rhythm.
- Every level is a named company plus a constraint: the same frame he asked for in September.
- Weakness: it is an interview-prep product, so depth varies and the AI feedback is a black box;
  Phase 1 has no practice. Lessons carry one Python block each, readable at his level.
- Already covered by L1-L7 (mapping): Phase 2 modules 2-3 (tokens, cost, sampling), 6 in part
  (BM25, embeddings, chunk size), 8 and 14 in part (evals, judges), 12 in part (retries), 13 in part
  (deploying a service). Not yet: hybrid search and reranking, citations, tools and agents, memory,
  serving internals, caching, guardrails, observability, A/B testing, fine-tuning.
