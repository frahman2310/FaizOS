# The lesson plan: 11 lessons

Replaced the 20-lesson plan on 2026-09-11. Lessons 1-2 are done; the remaining 18 are now 9.
Every one of the 133 skills is still assigned exactly once. Nothing was dropped.

How each lesson is taught lives in `docs/how-faiz-learns.md`: bootcamp-style rounds in chat,
then one small build file with a PASS/FAIL checker.

## What changed and why

**1. Adjacent lessons merged along natural seams.** Old L3+L4 were both "one reliable LLM
call"; L5+L6 were both "the eval set and what runs it"; and so on. A merged lesson is longer, not
denser: it has more rounds and more tasks, and each task still asks for one or two new things.

**2. The live URL moved from lesson 18 to lesson 4.** Deployment is in 78.3% of AI-engineering
job postings, the most demanded skill in the dataset. In the old plan he would have deployed
once, at the end. Now he deploys in L4 and every lesson after it ships onto the same live
service, so he repeats the most valuable skill seven times instead of once. It also gets
capstone rung 2 in lesson 4.

**3. SQL moved from lesson 17 to lesson 6.** SQL was the fastest-rising skill in the dataset
(9.8% to 34.8% in four months). Error analysis on 100+ traces is exactly what SQL is for, and
SQLite needs no setup. Postgres arrives in L7 for vectors and is deepened in L10.

**4. One new piece of Python grammar per lesson, at most.** The bootcamp covered the core. Each
lesson adds its libraries as "machines someone else built", plus at most one new piece of the
language, listed below.

## The lessons

| # | Lesson | New Python | Number it produces |
|---|---|---|---|
| **1** ✅ | **tokencost**: what an AI feature costs | stickers, `return` | $/day at 100k users |
| **2** ✅ | **ratecard**: pick the cheapest model | dicts, lists, `for`, `if` | cheapest model per workload |
| **3** | **meter**: a measured, reliable LLM call | `try` / `except` | p50/p95 latency, $/call, % valid output before vs after repair |
| **4** | **live**: your first live URL | `@` on top of a machine | **a live URL**, cold start, p95 over the internet |
| **5** | **evals**: the eval set and the gate that blocks bad merges | `assert` | pass rate on 100 cases, one merge blocked |
| **6** | **judge**: error analysis in SQL and a judge you can trust | SQL (its own round) | failure counts, **TPR, TNR, Cohen's κ** |
| **7** | **search**: retrieval from scratch, then vectors | slots filled by name | Recall@5, MRR, recall vs chunk size |
| **8** | **grounded**: hybrid search, citations, streaming | `yield` | groundedness %, **attack success before vs after** |
| **9** | **agent**: an agent loop, reliability, and an MCP server | `while` | **pass@1 vs pass^5**, $/task, tools working in a real client |
| **10** | **scale**: async, Postgres, caching under load | `async` / `await` | RPS and p95 under load, query time before vs after index |
| **11** | **capstone**: the ML evidence sprint and the product | none | one public results table |

The corpus for L7-L8 is Pakistani tax and corporate regulation (FBR/SECP/SBP), as decided in the
v3 spec.

## Skills per lesson

PRIMARY = new, taught from zero. APPLIED = already understood from v1, now used and measured.

| # | PRIMARY | APPLIED |
|---|---|---|
| 3 meter | uv-project-setup, pytest-fundamentals, ruff-lint-format, type-checking-python, git-workflow, retries-backoff, llm-timeouts, circuit-breakers | python-craft, data-structures, profiling, dev-setup, floating-point-logsumexp |
| 4 live | fastapi-structure, provider-abstraction, docker-multistage, docker-uv-cache, paas-deploy, health-readiness | serving-stacks |
| 5 evals | eval-set-construction, deterministic-assertions, ci-eval-gate, github-actions, oidc-keyless-deploy, iam-trust-scoping | probability-covariance, ml-lifecycle-leakage, heldout-eval, research-method |
| 6 judge | error-analysis, failure-taxonomy, sql-joins-aggregation, sql-window-functions, llm-judge-design, judge-validation, statistical-gating | double-descent, scaling-laws, paper-reproduction |
| 7 search | retrieval-metrics, retrieval-decision, chunking-strategies, contextual-retrieval, pgvector-limits | tokenizer-bpe, linalg-matmul, svd-lowrank, pca-svd, highdim-geometry, attention, rope, rmsnorm |
| 8 grounded | hybrid-retrieval, reranking, metadata-filtering, abstention, sse-streaming, client-disconnect, proxy-buffering | rag-production, vit-clip-siglip, vlm-fusion, diffusion-flow-matching, ai-security, alignment-methods, interpretability-sae |
| 9 agent | agent-bare-loop, tool-design, tool-errors, pass-k-reliability, context-engineering, durable-vs-checkpoint, agent-frameworks, mcp-server-2026, otel-tracing | tool-calling, agent-memory, agentic-rl, agent-evals-tracing, oss-contribution |
| 10 scale | async-taskgroup, async-exceptiongroup, blocking-the-loop, httpx-pooling, fastapi-di-lifespan, sqlalchemy-async, alembic-migrations, explain-analyze, async-lazy-loading, redis-caching | none |
| 11 capstone | icp-jtbd, distribution-channel, pricing-unit-economics, user-feedback-loop | capstone-portfolio, plus the 32 ML skills of the evidence sprint: peft-lora, rlhf-dpo, rlvr-grpo, rl-foundations, reward-modeling-verifiers, reasoning-distillation, quantization, kv-cache, inference-internals, flash-attention, triton-basics, roofline-cost-model, gpu-memory-hierarchy, torch-compile, torch-compile-cuda-graphs, profiling-nsight, fsdp-run, collectives-interconnect, pipeline-schedules, fault-tolerant-checkpointing, parallelism-axes, optimization-adam, init-normalization, autograd-backprop, matrix-calculus-vjp, pytorch-basics, regression-from-scratch, nanogpt-llama-block, gqa, mla, swiglu, ssm-mamba |

## Coverage check

| Group | Skills | Where |
|---|---|---|
| Production, PRIMARY | 67 | L1 (3), L2 (2), L3 (8), L4 (6), L5 (6), L6 (7), L7 (5), L8 (7), L9 (9), L10 (10), L11 (4) |
| ML, APPLIED | 66 | L3 (5), L4 (1), L5 (4), L6 (3), L7 (8), L8 (7), L9 (5), L11 (33) |
| **Total** | **133** | each assigned exactly once |

## Capstone rungs

| Rung | Old plan | New plan |
|---|---|---|
| 2, a live system | L18 | **L4** |
| 7, a validated judge | L8 | L6 |
| 6, an OSS contribution | L15 | L9 |
| 3, 4, 5, ML evidence on the M4 | L19 | L11 |
| 8, a product with a metric | L20 | L11 |

All eight still reachable, none needing rented hardware: Soup on the MLX backend for the
fine-tune, `mx.fast.metal_kernel` for the kernel.

## Honest weight

L10 (10 new skills) and L11 (the whole ML evidence sprint) are the heaviest. Both will run over
more than one sitting. L11 is almost entirely running tools on things he already understands,
so it is long rather than hard.
