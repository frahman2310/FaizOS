# The 20 lessons

Every one of the 133 skills, assigned exactly once, across 20 lessons. Each lesson is ONE
runnable file, produces ONE number, and ships an artifact worth showing.

Built from: the 133-skill curriculum, 6,964 scraped job descriptions (Grigorev), Hamel Husain's
eval methodology, Chip Huyen's *AI Engineering*, 12-factor-agents, and Hugging Face's MCP and
Context courses. Instagram (scaledojo.dev) is not yet folded in; see the note at the end.

## How coverage actually works

A flat 5% slice would cut across natural boundaries and produce a lesson that is half Postgres
and half distributed training. Instead each lesson owns an **artifact**, and every skill is
tagged as one of two kinds:

- **PRIMARY** — new, taught from zero, with the Python grammar it needs. ~67 production skills.
- **APPLIED** — he already understands it from the 44 v1 builds, so the lesson does not teach it
  again. It gets *used and measured*, which is what converts understanding into evidence. ~66 ML
  skills.

That distinction is the whole reason 20 lessons can hold 133 skills honestly.

---

## Phase 1 · Foundations and the eval spine (L1–L8)

Evals come before retrieval and agents on purpose. Huyen gives evaluation two chapters and puts
them before prompting; Grigorev's reviewers call starting without evals a red flag. Everything in
Phases 2–5 is scored against the harness built here.

| # | Lesson | PRIMARY | APPLIED | Number | Python taught |
|---|---|---|---|---|---|
| **1** ✅ | **tokencost** — what a feature costs | cost-modeling, token-budgeting, prompt-caching | — | $/day at 100k users | `name = work`, `return`, named lines |
| **2** ✅ | **ratecard** — pick the cheapest model | model-routing, batch-api | — | cheapest model per workload | dicts, lists, `for`, `if`, `None` |
| **3** | **meter** — an instrumented LLM client | uv-project-setup, pytest-fundamentals, ruff-lint-format, type-checking-python, git-workflow | python-craft, data-structures, profiling, dev-setup | p50/p95 latency, $/call | files, JSON, `try/except` |
| **4** | **contract** — structured output that never breaks | retries-backoff, llm-timeouts, circuit-breakers | floating-point-logsumexp | % schema-valid, before vs after repair | dataclasses, type hints |
| **5** | **synth** — build the eval set | eval-set-construction | probability-covariance, ml-lifecycle-leakage | N cases, coverage per dimension | comprehensions, sets |
| **6** | **harness** — the assertion runner + CI gate | deterministic-assertions, ci-eval-gate | heldout-eval, research-method | pass rate on 100 cases | modules, imports, exit codes |
| **7** | **triage** — error analysis on 100+ traces | error-analysis, failure-taxonomy | double-descent | failure taxonomy with counts | sorting, `Counter`, CLI input |
| **8** | **judge** — an LLM judge you can trust | llm-judge-design, judge-validation, statistical-gating | scaling-laws, paper-reproduction | **TPR, TNR, Cohen's κ on held-out labels** | slicing, random seeds |

**Why L8 matters most:** validating a judge against human labels is repeatedly named the single
highest-signal thing a candidate can show, and almost nobody does it. Your finance background is
a genuine edge here.

---

## Phase 2 · Retrieval (L9–L12)

RAG is in 39.8% of AI-engineering postings and 40%+ of take-homes.

| # | Lesson | PRIMARY | APPLIED | Number |
|---|---|---|---|---|
| **9** | **bm25** — lexical retrieval from scratch, no library | retrieval-metrics, retrieval-decision | tokenizer-bpe, linalg-matmul | Recall@5, MRR |
| **10** | **embed** — vector index + chunking sweep | chunking-strategies, contextual-retrieval | svd-lowrank, pca-svd, highdim-geometry, attention, rope, rmsnorm | Recall@k curve vs chunk size |
| **11** | **hybrid** — RRF fusion + cross-encoder rerank | hybrid-retrieval, reranking, metadata-filtering | rag-production, vit-clip-siglip, vlm-fusion, diffusion-flow-matching | ΔRecall@10, worst-segment recall |
| **12** | **grounded** — citations, abstention, injection defence | abstention | ai-security, alignment-methods, interpretability-sae | groundedness %, **attack success before vs after** |

**The corpus is Pakistani tax and corporate regulation (FBR/SECP/SBP)** — decided in the v3 spec.
Rule numbers like `150Q` are the canonical case where dense embeddings fail and BM25 is mandatory,
you know the domain cold, and it feeds venture candidate #1.

---

## Phase 3 · Agents (L13–L15)

Agents are in 41.6% of postings, MCP in 14.1%.

| # | Lesson | PRIMARY | APPLIED | Number |
|---|---|---|---|---|
| **13** | **loop** — an agent in ~150 lines, no framework | agent-bare-loop, tool-design, tool-errors | tool-calling | success on 20 tasks, mean steps, $/task |
| **14** | **control** — budgets, resume, human approval | pass-k-reliability, context-engineering, durable-vs-checkpoint, agent-frameworks | agent-memory, agentic-rl, agent-evals-tracing | **pass@1 vs pass^5**, % needing approval |
| **15** | **mcp** — a server on the 2026-07-28 spec | mcp-server-2026 | oss-contribution | tools exposed, p95 per tool, working in a real client |

L15 doubles as the FaizOS migration from the v3 spec, and as the OSS on-ramp.

---

## Phase 4 · The service (L16–L18)

Docker is in 1,700 postings, CI/CD in 2,560, AWS in 40.3%. This is the 78% you are missing.

| # | Lesson | PRIMARY | APPLIED | Number |
|---|---|---|---|---|
| **16** | **service** — async FastAPI that does not block | async-taskgroup, async-exceptiongroup, blocking-the-loop, httpx-pooling, fastapi-structure, fastapi-di-lifespan, provider-abstraction | — | RPS and p95 under load, blocking vs async |
| **17** | **store** — Postgres, pgvector, real SQL | sqlalchemy-async, alembic-migrations, sql-joins-aggregation, sql-window-functions, explain-analyze, pgvector-limits, async-lazy-loading, redis-caching | — | query p95 before/after index, cache hit rate |
| **18** | **ship-it** — Docker, deploy, CI with OIDC, streaming | docker-multistage, docker-uv-cache, paas-deploy, health-readiness, github-actions, oidc-keyless-deploy, iam-trust-scoping, sse-streaming, client-disconnect, proxy-buffering, otel-tracing | serving-stacks | **a live URL**, build time, cold start |

SQL was the fastest-rising skill in the dataset (9.8% → 34.8% in four months). L17 is not optional.

---

## Phase 5 · Evidence and ship (L19–L20)

| # | Lesson | PRIMARY | APPLIED | Number |
|---|---|---|---|---|
| **19** | **prove** — the ML evidence sprint, all local on the M4 | — | peft-lora, rlhf-dpo, rlvr-grpo, rl-foundations, reward-modeling-verifiers, reasoning-distillation, quantization, kv-cache, inference-internals, flash-attention, triton-basics, roofline-cost-model, gpu-memory-hierarchy, torch-compile, torch-compile-cuda-graphs, profiling-nsight, fsdp-run, collectives-interconnect, pipeline-schedules, fault-tolerant-checkpointing, parallelism-axes, optimization-adam, init-normalization, autograd-backprop, matrix-calculus-vjp, pytorch-basics, regression-from-scratch, nanogpt-llama-block, gqa, mla, swiglu, ssm-mamba | **QLoRA Δ vs baseline on the L6 eval set; a fused Metal kernel vs the MLX reference; a reproduction within seed spread** |
| **20** | **capstone** — one domain, shipped, with a public results table | icp-jtbd, distribution-channel, pricing-unit-economics, user-feedback-loop | capstone-portfolio | one table: pass rate, Recall@10, groundedness, κ, p95, $/query, attack success |

**L19 is the one lesson that is pure conversion.** Every skill in it is already understood; the
lesson runs it, measures it, and files the row. Soup (`~/tools/Soup`) on the MLX backend does the
fine-tune, `mx.fast.metal_kernel` does the kernel. **No rented GPU.** It closes capstone rungs
3, 4 and 5 in one sitting.

---

## Coverage check

| Group | Skills | Where |
|---|---|---|
| P0–P10 production | 67 | L1–L18, L20 — all PRIMARY |
| T0–T10 ML | 66 | applied across L3–L12 and L19 |
| **Total** | **133** | every skill assigned exactly once |

Capstone rungs: **2** (L18 live URL) · **3, 4, 5** (L19) · **6** (L15 OSS) · **7** (L8 judge) ·
**8** (L20 product with a metric). All eight reachable, none needing rented hardware.

## Advanced building skills, explicitly

Per the request that this "inculcate advanced building skills", these are threaded through rather
than bolted on: writing a retrieval engine with no library (L9), an agent loop with no framework
(L13), an MCP server on a three-week-old spec (L15), a fused GPU kernel (L19), an eval gate that
blocks a merge (L6), and a documented prompt-injection result (L12). The last two are the rarest
things in a candidate repo.

## What the format stays

Unchanged from what works: one self-contained `.py` file per lesson, everything explained inside
it in `#` comments, one loudly marked YOUR TURN zone, a THE PYTHON YOU NEED block, self-running
PASS/FAIL checks, and a one-line Task 1 before the real Task 2.

## Not yet included

**scaledojo.dev** — Instagram blocks profile enumeration without a logged-in browser session.
Individual posts are readable and `/watch` (now installed globally) can read the videos, not just
the captions. Either connect the OpenCLI Chrome extension, or paste 10–15 post URLs, and this plan
gets a revision pass against their reasoning.
