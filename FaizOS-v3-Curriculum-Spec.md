# FaizOS v3 — The Curriculum

**Purpose:** take Faiz from *deep understanding with zero evidence* to *hireable, shipping, GTM-ready AI engineer*.
**Written:** 2026-08-22, from five parallel research streams (~570k tokens) plus the AI-startup roles market document.
**Status:** draft for review. Nothing gets built until this is signed off.

---

## Part I — The diagnosis

### The measured gap

v1 taught 66 skills across 44 builds. Against 4,894 AI-engineering job descriptions (Grigorev field guide, scraped Feb–Jun 2026):

| Responsibility | % of postings | Faiz |
|---|---|---|
| Building AI systems | 98.1% | partial |
| **Deployment** | **78.3%** | **none** |
| Infrastructure / platform | 69.2% | none |
| **Evaluation & quality** | **68.5%** | ML eval only |
| **Monitoring** | **64.3%** | none |
| API / service integration | 62.4% | none |
| Perf / latency / cost | 57.2% | theory only |
| Fine-tuning | 13.8% | concepts |
| **Self-hosting (vLLM/Triton)** | **2.5%** | concepts |

**The thing he's good at is 13.8% of the job. The thing he's missing is 78%.**

Worse, the trend runs against him. Feb→Jun 2026 deltas: PyTorch 22.0→16.4, fine-tuning 8.2→5.6, RLHF 1.8→0.9, inference/serving 11.4→6.4 — **all falling**. Rising: SQL 9.8→**34.8** (fastest riser), prompt engineering 32.7→47.6, CI/CD 29.8→37.7, MCP 8.0→13.0.

Zero of his 66 skills cover async Python, LLM API integration, vector DBs, FastAPI, SQL, Docker, cloud, CI/CD, observability, or production reliability.

### The blunt risk

> *"Deep internals + zero deployments is the profile most likely to be respected and rejected."*

The from-scratch work is **near-decisive** for inference-infra / research-engineer / frontier-lab tracks, and **near-zero direct value** on a product AI-Engineer screen, where transformer internals are classed as "specialized topics, not asked by default." It converts three ways only:

1. Measured benchmarks against a reference implementation
2. Written artifacts (blog, ADRs, spec-fluent writeups)
3. A merged PR in a repo where that knowledge is load-bearing

### The three assets he already owns and isn't counting

1. **FaizOS itself** — 4,636 lines of TypeScript, 59 tests, 30 MCP tools, 3 hooks, SQLite, migrations. This is capstone Rung 2 ("a working system others can run") minus a README, a deploy, and one user.
2. **A statistics background.** The single highest-signal skill in LLM evaluation — validating an LLM judge against human labels with TPR/TNR/Cohen's κ and a bias correction — is one most AI engineers cannot do. Clustered SEs, paired bootstrap, power calculations. This is his home turf and almost nobody entering the field has it.
3. **Spec-reading depth.** MCP went stateless on **2026-07-28** (sessions removed, `initialize` gone, `server/discover` added, Sampling/Roots/Logging deprecated). Every MCP tutorial written before August describes a dead protocol. Publishing an MCP server is worth little — ~9,400 exist. *Migrating one to the new spec with OAuth 2.1 and server-minted handles* is worth a lot, because almost nobody has.

### What we're optimizing for

Two destinations, one path:
- **Employability** — UK (incl. Global Talent) and US-remote AI Engineer / LLM Engineer roles.
- **The venture** — one shipped AI product with real users.

They converge: both are gated on *evidence of production judgement*, not more theory.

---

## Part II — The operating system

### The core correction to v2: guidance must vary by domain

v2 applies write-from-empty universally via the PreToolUse guard. **That is wrong for half of v3**, and the evidence is specific.

**Expertise reversal effect** (robust, repeatedly replicated): worked examples beat minimally-guided problem solving for *novices*; the advantage disappears and then *reverses* as domain knowledge grows, because redundant guidance becomes extraneous cognitive load.

Faiz's expertise is split, so the policy must be too:

| Domain | His level | Policy |
|---|---|---|
| ML internals (T-tracks) | past novice | **Write from empty.** Guard ON. |
| Production engineering (P-tracks) | genuine novice | **Worked example first**, then modify, then write from empty. Guard OFF for rungs 1–2. |

Applying one uniform rule is the design error to avoid.

### The build loop, corrected

Every build, both modes:

1. **Problem statement** — what breaks without this. (Carried over from the v1 revision format; it works.)
2. **Design brief** — plain English, no code.
3. **Rules card** — 3–6 rules weighted by his open error categories.
4. **Failing tests** — the finish line, written first.
5. **Attempt** — write-from-empty *or* worked-example-then-modify, per the table above.
6. **REVEAL AND CONTRAST — mandatory, new.** Read the reference implementation, diff it against his reasoning, write one line on each difference.
7. **Three-pass review** — correctness, taste, his recurring error patterns.
8. **Record** — skills, errors, metrics.

**Step 6 is not optional.** Productive Failure is *generate then instruct*; the consolidation phase is where cognitive load drops and learning consolidates. Write-from-empty with no reveal step is not what the evidence supports.

### Completion criterion: the delayed rebuild

A build is **not done** when tests pass. In the controlled study, **3 of 9 students who succeeded on the day failed the same task two weeks later** — the authors call it *"unproductive success": the illusion of transfer without authentic learning.*

**A build reaches `done` only after an unaided rebuild 14+ days later.** Until then it is `provisional`. FSRS already schedules this; v3 wires it to build state.

### Learning-science weights (effect sizes, meta-analysis n=169,179)

| Technique | d | Weight in v3 |
|---|---|---|
| Spaced practice | **0.85** | pillar — FSRS drives the schedule |
| Retrieval practice | **0.74** | pillar — every concept re-produced from memory |
| Self-explanation | 0.54 | the reveal-and-contrast step |
| Interleaving | 0.47 (n=972) | **not a pillar** — statistically indistinguishable from re-reading |

**Concepts per session: 1–3 genuinely *interacting* concepts.** Load scales with interaction, not count — "3 new API names" is cheap; "3 concepts you must hold simultaneously to reason about one system" is expensive. v1 proved 9 concepts → 1/5 blanks, 3 concepts → 3/3.

### Individualization

The deliberate-practice literature's one surviving requirement: practice targeted at *this learner's specific logged failures*, with immediate feedback. Generic drilling is the version the meta-analyses found weak. FaizOS already logs 8 error categories with occurrence counts. **Every rules card is generated from the top 3 open categories.** That loop already exists and is the thing to lean on.

### The three modes

**MODE 1 — Course Mode (the spine).** P0→P7 in order, non-negotiable sequence. Structured, worked-examples-first. This is the critical path and it is not skippable, because every later mode assumes a deployable service exists.

**MODE 2 — Venture Mode (unlocks after P7).** The active venture decides *what* gets built. FaizOS picks the track and skills at the intersection of **what the venture needs** and **where he is weakest**. This is the feedback loop he asked for: venture pulls, weakness steers, evidence accumulates.

**MODE 3 — Free Build (available always).** He brings an idea; the system scopes it, teaches just-in-time, and enforces the same floor: a failing test, an eval harness, a deployed URL, a measured number. No idea ships without those four.

**Mode contract, all three:** every build produces (a) a passing test, (b) an eval case, (c) a number, (d) a row in `systems` or `experiments`. No exceptions — this is what makes the capstone auto-score honest.

---

## Part III — The curriculum

### P-tracks: the production spine (the critical path)

These are new. They are the 78%.

---

**P0 — The engineering floor** · ~1 week
*Problem: he has never shipped code anyone else could run.*
`uv` (src layout, `uv.lock`, `uv sync --locked`), `ruff` (`extend-select`, not `select`), `pytest` from `pyproject.toml`, pyrefly or mypy, git workflow, GitHub Actions running the tests.
**Completion test:** new project → dependency → failing test → passing → green CI, in 15 minutes, no lookups.
*This is the phase he will want to skip. It is the phase that is missing.*

---

**P1 — Async Python + FastAPI** · ~2 weeks
*Problem: an LLM service is I/O fan-out; blocking code caps you at ~10 req/s instead of ~500.*
`asyncio.TaskGroup` + `asyncio.timeout` + `Semaphore` (not bare `gather`), `ExceptionGroup`/`except*`, one long-lived `httpx.AsyncClient` in lifespan with tuned `Limits` (default `max_connections=100` is the silent LLM bottleneck), FastAPI structure, `Depends`, pydantic-settings, providers behind one interface.
**The four mistakes that get flagged in review:** blocking the loop; sync SDK inside `async def`; CPU work in a handler; declaring `async def` then blocking (strictly worse than declaring `def`).
**Completion test:** write the blocking version, load-test it, watch p99 collapse, fix it, show the before/after.

---

**P2 — Docker + one real deploy** · ~1 week
*Problem: nothing is real until it has a URL.*
Multi-stage Dockerfile with the canonical uv cache-mount pattern, non-root, pinned base. Deploy to **Cloud Run or Fly** — not Kubernetes. `/health` (liveness) vs `/ready` (readiness).
**Completion test:** it loads on his phone.
*This is the psychological turning point. Everything after is refinement.*

---

**P3 — CI/CD with OIDC** · ~3 days
*Problem: long-lived cloud keys in repo secrets are the junior tell.*
Actions workflow that tests → builds → deploys with **zero static credentials**. Scope the IAM trust policy's `sub` claim to the exact repo and ref, not a wildcard.
**Completion test:** "CI builds an image and deploys it to Cloud Run in under 3 minutes, no static keys."

---

**P4 — Postgres and the data layer** · ~2 weeks
*Problem: SQL was the fastest-rising skill in the dataset (9.8% → 34.8%) and he has none of it.*
SQLAlchemy 2.0 async + asyncpg + Alembic (`async_sessionmaker(expire_on_commit=False)`; lazy-loading *raises* in async — `selectinload`, which is N+1 in disguise). Window functions (`ROW_NUMBER() OVER (PARTITION BY…)`), CTEs, index types, `EXPLAIN (ANALYZE, BUFFERS)` on a deliberately bad query. pgvector: the 2,000-dim `vector` limit, ~6KB per 1536-dim row, HNSW not reclaiming space on delete, and **the p99 cliff when the index exceeds RAM** — that, not row count, is the real ceiling.
**Completion test:** diagnose a slow query from `EXPLAIN` output alone, and state where pgvector's ceiling sits for a given corpus.

---

**P5 — Streaming and reliability** · ~1 week
*Problem: streaming works on localhost and dies behind a proxy.*
FastAPI's **native SSE** (shipped 0.135.0 — this postdates essentially every tutorial online and obsoletes the `sse-starlette` advice). SSE over WebSockets, and why. Client disconnect in three layers, including **`asyncio.shield()` on the post-stream billing write** — skip it and you stop billing exactly the requests users abandon. Then break it deliberately: nginx with default `proxy_buffering on` holds the whole response for 60s. Retries with `stamina`, circuit breaker per `(provider, model)` tripping on 5xx/529 but **never on 429**, TTFT and inter-token-gap timeouts instead of a meaningless total timeout for a 128k generation.
**Completion test:** kill the client mid-stream and prove the usage row still wrote.

---

**P6 — Observability and evals** · ~2 weeks · **THE DIFFERENTIATOR**
*Problem: "Red flag if the candidate doesn't start with evals" — named the single biggest differentiator by every source.*

The workflow, in order, and the order is the lesson:
1. **Error analysis first, not metric selection.** Hand-label 100+ real traces. Open coding (free-text note per failure) → axial coding (cluster into a taxonomy) → **frequency counts in a pivot table**. Expect 60–80% of development time here.
2. Build evaluators only for the **top** categories. Deterministic code assertions for anything decidable; **one** LLM judge for the top subjective failure.
3. **Binary, not Likert** — the gap between 3 and 4 is inconsistent across annotators and runs.
4. **Validate the judge.** TPR/TNR (not raw accuracy — it's meaningless under class imbalance), Cohen's κ with Wilson intervals, then the bias correction for imperfect judge sensitivity. **This is his statistics edge and almost no candidate does it.**
5. **Statistical gating.** Binomial SE (`n=100, p=0.8 → ±8pp`; that eval *cannot* resolve a 4-point gain), **clustered SEs** (>3× the naive SE when items are grouped — near-universally ignored), paired bootstrap (item-difficulty correlation 0.3–0.7 buys a free ~2× effective sample size).
6. OTel spans → self-hosted **Langfuse**. Log model version pinned, TTFT split from total, p50/p95/p99, cost, prompt version, tool-call count, loop count.
7. **CI gate** — Promptfoo or DeepEval blocking on pass-rate regression.

**Completion test:** a documented regression that the gate caught, with the paired test proving the fix was real and not noise.

*Tooling note: the market consolidated in Q1 2026 — Langfuse→ClickHouse, Promptfoo→OpenAI, and **Helicone is in maintenance mode** (do not build on it). OTel GenAI conventions are **not stable** — deprecated from the main repo June 2026, moved to a repo with no tagged release. Teach the pattern, normalize into your own schema, don't build dashboards on `gen_ai.*` names.*

---

**P7 — Cost engineering** · ~1 week
*Problem: "cost awareness is a superpower" — one engineer showed a 70% spend reduction and had an offer the next day.*
Prompt caching arithmetic from the actual rate cards (Anthropic 5-min write 1.25×, read 0.1×; break-even on the *first* hit; **below the model's minimum cacheable prefix, caching is silently skipped with no error**). Batch APIs (−50%, contractual, the only number you can bank). Context trimming across OpenAI's short/long tier boundary — a **step function**, not linear. Routing: plan for 30–55%, not the 85% the papers claim.
**Ranked by certainty of return:** batch (−50%, guaranteed) > prompt caching (−70–85% on prefix-heavy traffic) > context trimming > routing (30–55%) > semantic caching (marginal and risky). **Most teams do these in exactly reverse order.**
**Completion test — the drill:** every design answer ends with a number. `100k users × 10 interactions × 2k tokens = 2B tokens/day ≈ $13k/day`. Out loud, unprompted.

---

**P8 — Retrieval, properly** · ~2 weeks
*Problem: RAG is in 40%+ of take-homes, and naive 2023 RAG is dead while RAG is not.*

**The decision framework first** — this is the senior answer:

| Corpus | Correct 2026 answer |
|---|---|
| Fits in context (<200k tok) | Don't retrieve. Stuff it, cache the prefix. |
| Small + structured (repo, wiki) | Lexical/grep + a loop. **No vector DB** — this is what Claude Code does. |
| Large, messy, high query volume | Hybrid + rerank. 8–82× cheaper than long context. |
| Large + multi-hop | Agentic loop *on top of* a good hybrid retriever. |

Then the mechanics: structural/page-level chunking (NVIDIA: best default, lowest variance), **contextual chunk prefixes** (Anthropic: −49% retrieval failures at ~$1.02/M doc tokens — the best cost/benefit in the whole pipeline and still underused), hybrid BM25 + dense with **RRF (k=60)**, **cross-encoder reranking** ("the highest value 5 lines of code you'll add", +14–20%).

**The diagnostic that replaces guessing: recall@50 vs recall@5.** Big gap → ranking problem, add a reranker. Both low → chunking/embeddings are broken and a reranker cannot save you.

**The failure nobody teaches: metadata filtering.** Post-filtering an HNSW index — ask for 10, get 3, **nothing errors**. Multi-tenant `WHERE tenant_id = ?` is the most common real filter and exactly where this bites.

**MTEB is contaminated.** jina-v3 beat text-embedding-3-large on *every* MTEB English task and lost on real W&B data (0.532 vs 0.602 recall@10). Run 3 candidates against your own golden set.

**Completion test:** the ablation table (below).

---

**P9 — Agents, tools, MCP** · ~2–3 weeks
*Problem: "Excessive Agency" jumped from #6 to #3 in OWASP's 2026 LLM Top 10 — the risk moved from "the model says something bad" to "the agent does something bad."*

Order matters and framework comes **last**:
1. **The bare loop, ~150 lines.** Messages, tool schemas, parse, dispatch, append, repeat. Provider SDK only. Everything else is a variation on this.
2. **Tool design.** Namespaced names, unambiguous params, **never return opaque UUIDs** (the model can't reason over `a3f9-…`), `ResponseFormat` enums (Anthropic's example: 206 tokens → 72 for the same call), **errors as prompts** (`"'tomorrow morning' is not an ISO date, provide e.g. 2026-01-09"` gets a correct retry; `400 Bad Request` gets a loop). **Consolidate** — expose `schedule_event`, not `list_users` + `list_events` + `create_event`.
3. **Failure handling.** Idempotency keys minted by the harness, budget caps, max-turns.
4. **Evaluation — before adding features.** **`pass^k`, not `pass@k`**: solved in *every* one of k tries. An agent at 70% pass@1 can be 25% pass^5. That distinction alone is worth a lesson.
5. **Context engineering.** Compaction with an external progress file, subagent context isolation, progressive tool disclosure (~85% token reduction on tool definitions). Measure the **context rot** curve on his own task — he has the ML background to do it properly.
6. **Durability + HITL.** A checkpointer is *not* durable execution: checkpointer = you own retry/resume/dedup; durable execution = the runtime does.
7. **MCP on the 2026-07-28 spec.** Then attack it — tool poisoning is now an OWASP-catalogued attack class (malicious instructions in tool *descriptions*, read at list time before any user input).
8. **A framework, last.** Pydantic AI, then LangGraph. By now he'll know exactly which hand-rolled part each replaces — the only honest way to evaluate one.

**Do not teach:** CrewAI, AutoGen (maintenance mode after the Microsoft Agent Framework merger), free-form agent swarms, hosted visual builders (OpenAI's Agent Builder went launch→sunset in 8 months).

**Multi-agent, honestly:** it buys *parallelism and context isolation*, not *intelligence*. Anthropic's research orchestrator beat single-agent by 90.2% — at **15× the tokens**. Single-agent matches or beats multi-agent on multi-hop reasoning at equal token budget. Default to one strong agent with excellent tools; reach for subagents only when you need a fresh context window.

---

**P10 — Ship and sell** · ongoing
See Part IV.

---

### T-tracks: repositioned

T0–T10 stay exactly as they are, but their **job changes**. They are no longer the critical path — they are the **evidence conversion layer** and the specialization ladder for inference-infra / research-engineer roles.

- **T2, T4, T6** get reactivated purely to produce capstone rungs 3, 4, 5. **All three run locally on the M4 — no GPU rental.**
- **T7, T8** are largely absorbed into P8/P9, which teach the same material with production depth.
- The rest is maintained by FSRS retrieval practice, not re-taught.

**Hardware: Apple M4, 16GB unified, 8 GPU cores.** This is sufficient for every remaining rung:

| Rung | Path | Tool |
|---|---|---|
| **3** — trained model + metric + 3 seeds | QLoRA fine-tune of a 1–8B model, before/after eval | **Soup** (`~/tools/Soup`), MLX backend |
| **4** — measured performance win | **A fused Metal kernel benchmarked against the MLX reference.** `mx.fast.metal_kernel()` takes a kernel body from Python and generates the signature; MLX's own docs show 8× and 40× fused speedups. | MLX |
| **5** — reproduction within seed spread | A small published result, 3+ seeds, compute-matched | Soup / MLX |

**Triton does not run on Metal**, so the T4 Triton work does not transfer as code. It transfers entirely as *concepts* — roofline, arithmetic intensity, fusion, tiling, online softmax are hardware-agnostic. Writing them in Metal instead of Triton is also **more differentiated**: a Triton FlashAttention is a common portfolio item; a benchmarked fused Metal kernel is not.

---

## Part IV — The evidence ladder

### The three flagship projects

Each is a capstone rung and a portfolio artifact. Built in this order.

**Domain, decided: Pakistani tax and corporate regulation (FBR / SECP / SBP).** Projects 1 and 2 share one corpus. The reasoning is not arbitrary:

- **He knows it cold.** Finance undergraduate, Pakistan-based. A failure taxonomy is only credible from someone who can tell a wrong answer from a right one, and this is the one corpus where he outranks almost any reviewer.
- **It is genuinely messy** — PDFs, tables, amendments superseding amendments, SROs, circulars. Parsing is 80% of real RAG work and this corpus refuses to be clean.
- **It is the canonical exact-token case.** Rule numbers (`150Q`), SRO numbers, section references — precisely where dense embeddings visibly fail and BM25 is mandatory. The hybrid-retrieval lesson lands with real stakes instead of as a tutorial.
- **Abstention matters here.** "That provision isn't in this corpus" is a legally meaningful answer. The research flags abstention correctness as "almost never measured, always broken" — this domain forces it.
- **It collapses the curriculum into the venture.** Venture candidate #1 is Pakistani e-invoicing compliance. Project 2's retrieval harness *is* that venture's core technology and its evidence trail. **This pulls Venture Mode forward from week 16 to roughly week 11.**
- **Nobody else has it.** A differentiated corpus produces a differentiated project. Every other candidate benchmarks on SEC 10-Ks or a Wikipedia dump.

---

**PROJECT 1 — "Boring feature, ruthlessly instrumented"** (after P6)

*One narrow LLM feature. ~200 lines of app code. **Deliberately not an agent** — trajectory complexity obscures the eval story.*

Structured extraction, a ticket classifier, or Q&A over a corpus he knows cold. Deliverables:

1. 50–100 hand-labeled traces → **published failure taxonomy with frequency counts**
2. Tiered evals mapped to that taxonomy
3. **Judge validation: TPR, TNR, Cohen's κ, Wilson intervals, bias-corrected pass rate**
4. **A power calculation in the README**, honored — refuse to claim wins below the detectable threshold
5. OTel → Langfuse; cost, TTFT, p95
6. CI gate on pass-rate regression
7. **The money shot:** a plausible-looking "improvement" that helps the headline metric and hurts a subgroup. CI catches it. Two-paragraph incident report.

**Claims Rung 7.** Item 7 is what ends an interview early in his favour.

---

**PROJECT 2 — "The retrieval ablation"** (after P8)

*Not a chatbot over PDFs — every candidate has one. **A retrieval eval harness with a published ablation table** over a real, messy corpus (5k–50k chunks).*

The centerpiece is a ~10-row table on **his** data: BM25 only / dense only (2 models) / hybrid+RRF / +rerank / +contextual prefixes / +multi-query / page vs 512-token chunks / **filtered-queries-only (the recall collapse demo)** / long-context baseline — each with R@5, R@20, NDCG@10, p95 ms, **$/1k queries**.

Plus a failure analysis of the 20 worst queries **including the fixes that didn't work**. Negative results are the strongest credibility signal available.

The one-line pitch he should be able to give:
> *"Reranking bought +14 points, semantic chunking bought nothing, and here's the filtered-query case where HNSW post-filtering silently dropped recall from 0.81 to 0.34."*

---

**PROJECT 3 — "FaizOS on the 2026 spec"** (after P9) · **local stdio, his call**

*The asset he already owns, converted.*

Migrate FaizOS's MCP server from SDK 1.30.0 to the **2026-07-28 spec**, staying local/stdio. What still applies to a stdio server:

- **`server/discover`** — servers MUST implement it (advertises versions, capabilities, identity)
- **The removed `initialize` / `notifications/initialized` handshake** — protocol version and client capabilities now ride in `_meta` on every request
- **MRTR** (multi-round-trip requests) replacing all server-initiated requests; every result carries a required `resultType`
- **First-class caching** — `ttlMs` + `cacheScope` on list/read results, and **deterministically ordered `tools/list` to improve prompt-cache hit rates**
- **Deprecated Sampling, Roots, Logging** (12-month window) — log to stderr/OTel instead
- OpenTelemetry trace-context propagation through `_meta`

**Dropped, because it stays local:** OAuth 2.1 / Client ID Metadata Documents, HTTPS deployment, and the session→handle migration (sessions were a remote/HTTP concern).

Then **write the migration up publicly** — including why Sampling was deprecated and what MRTR replaced. That writeup is the artifact: it proves spec fluency, which is the actual differentiator. Publishing a server is worth little (~9,400 exist); migrating one and explaining it is rare.

**Claims Rung 6-adjacent credibility and the "recognition" currency for the visa case.** Rung 2's deployed URL comes from the P2 service instead, which already has one by week 4.

---

### The OSS track (runs in parallel from week 4)

Measured on 2026-08-22 via the GitHub API, not guessed:

| Repo | Open good-first-issues | External share of merges | Verdict |
|---|---|---|---|
| **vllm-project/vllm** | **23** | **62%** | **Best target.** FlashAttention/KV-cache/paged-attention knowledge is load-bearing here. |
| **huggingface/transformers** | 0 GFI but **39 "Good Second Issue"** | 38% | **Best hidden value** — beginners picked the easy shelf clean; the harder ones sit unclaimed. |
| huggingface/trl | ~0 | **5%** | **Trap.** 60 of 66 merges were maintainers. |
| BerriAI/litellm | 0 | — | **Trap.** 95 of last 100 closed PRs closed *unmerged*. |
| MCP python-sdk | 6 | — | Low prestige, near-instant merges. Fine for breaking the seal. |

**Realistic timeline:** 2–6 weeks to a first merged small PR; **1–3 months** to a substantive vLLM PR including RFC discussion (any architectural change >500 LOC needs an RFC issue first) and 2–3 review cycles. vLLM merge latency: p50 43h, **p75 270h**.

**Claims Rung 6.**

### GTM — the light layer (his choice: ship-focused, not a second spine)

Four skills only, each attached to a project rather than taught separately:

1. **ICP and JTBD** — already in the venture engine's stage 2. One sentence: who, doing what job, dissatisfied how.
2. **Distribution** — pick *one* channel and test it. The MCP/desktop-extension route is the only lab distribution surface with no org gate.
3. **Pricing** — one number, defended with the cost model from P7. He knows unit economics from finance; this is the cheapest skill on the list for him.
4. **Evidence → customer** — the venture arm's corroboration trail *is* the customer-discovery artifact. Ten users on a real workflow beats zero; 600 beats 10; 600 vs 10,000 barely matters for hiring.

**Real users are a tiebreaker and a story-generator, not a filter.** Their true value is producing the artifacts that *are* filters — real latency percentiles, real cost curves, real failure taxonomies. You cannot write a credible post-mortem without traffic.

### The visa route as a design constraint

**UK Global Talent, Exceptional Promise**: no job offer, no sponsor, no salary floor, no degree requirement, targeted at <5 years' experience. Its three evidence currencies are **publications, notable open source, and recognition** — all three buildable from Pakistan with no employer, and all three are what this curriculum produces anyway.

This should be a **design constraint on curriculum output**, not a separate task: write up every project publicly, land the vLLM PR, and the visa case assembles itself. The Skilled Worker route requires a sponsor licence most startups don't hold; this one doesn't.

*(US-remote reality: sponsorship is essentially unavailable for remote roles; the mechanism is contractor or EOR. Pakistani contractor rates run 40–60% below US rates. Legitimate on-ramp for manufacturing production experience; not the destination.)*

---

## Part V — What we are deliberately NOT doing

Each of these was recommended by at least one source and rejected on evidence:

| Skip | Why |
|---|---|
| **Kubernetes** (as a skill) | 26.6% of postings, but juniors need to *read* a manifest and debug CrashLoopBackOff, not run a cluster. "Knows Kubernetes" on a junior CV is noise. |
| **Self-hosting vLLM/SGLang** | **2.5% of postings.** And the break-even: one H100 at ~$2.89/hr needs **~11 billion tokens/month sustained** to beat serverless open-model APIs. Cost is the *weakest* argument for self-hosting in 2026. |
| **Fine-tuning as a focus** | 13.8% and falling (8.2→5.6 in four months). Listed often, tested rarely. Do it once for Rung 3, via Soup. |
| **Semantic caching** | Marginal now that providers ship 90%-off prefix caching, and false-hit rates run 1–15%. GPTCache is effectively dead. |
| **Semantic chunking** | The most cargo-culted technique in the RAG stack. Largely obviated by late chunking. |
| **GraphRAG** | 6–8× indexing cost, 3× operating cost. Learn when it applies; don't build one. |
| **MTEB leaderboard chasing** | Contamination found across all 9 datasets tested. |
| **CrewAI / AutoGen / agent swarms** | AutoGen is in maintenance mode; OpenAI killed Swarm; 14 documented multi-agent failure modes. |
| **Learning RAG *through* LangChain** | Multiple production teams independently reported abandoning it for ~300 lines of their own code. |
| **Terraform/OpenTofu** | Not until there's a second environment. `gcloud run deploy` in a Makefile is fine. |
| **Free-threaded Python** | Know how to detect a silently-restored GIL. Ship on the GIL. |
| **Celery** | Go straight to a Postgres-backed queue or `arq`. |
| **Interleaving as a study strategy** | d=0.47 on n=972 — indistinguishable from re-reading. Spacing and retrieval are the pillars. |
| **Public agent leaderboards** | Saturated, and possibly reward-hackable end-to-end. His own eval set is the only trustworthy one. |

---

## Part VI — What has to change in FaizOS

Implementation follows sign-off. Ten changes:

1. **`tracks` gains the P-series** (P0–P10) alongside T0–T10, with a `kind` column (`production` | `ml` | `ship`).
2. **`skills` gains ~45 production skills**, mapped to P-tracks. (Currently zero cover the floor.)
3. **Guard policy becomes per-track.** `tracks.guidance_policy` = `write_from_empty` | `worked_example_first`. The PreToolUse hook reads it instead of blocking unconditionally.
4. **`builds` gains `state='provisional'`** and a `rebuild_due` date. `done` requires the 14-day unaided rebuild. Wire to FSRS.
5. **New step in the build loop: `faizos_reveal_contrast`** — records his diff against the reference implementation. Mandatory before review.
6. **Mode switch:** `faizos_state` returns `mode` = `course` | `venture` | `free`. Venture Mode selects the next build at the intersection of venture-need and weakness.
7. **`systems` gains cost/latency columns** — `p95_ms`, `cost_per_1k`. Every project carries a number.
8. **Capstone regrade:** rung evidence recognizes the P-track artifacts (eval harness → R7, deployed service → R2, ablation table → R7 supporting).
9. **`/faiz-cost`** — the drill. Given a scenario, he computes tokens/day and $/day out loud; the command scores it.
10. **`/faiz-oss`** — tracks the vLLM/transformers issue hunt, PR state, and review cycles.

---

## Timeline (aggressive, his choice)

| Weeks | Work | Evidence |
|---|---|---|
| 1 | P0 engineering floor | — |
| 2–3 | P1 async + FastAPI | — |
| 4 | P2 Docker + deploy · **OSS hunt starts** | first URL |
| 4.5 | P3 CI/CD + OIDC | — |
| 5–6 | P4 Postgres + SQL | — |
| 7 | P5 streaming + reliability | — |
| 8–9 | **P6 evals** → **Project 1** | **Rung 7** |
| 10 | P7 cost engineering | first merged PR (target) |
| 11–12 | **P8 retrieval** → **Project 2** (FBR corpus) · **Venture Mode opens** | ablation table |
| 13–15 | **P9 agents + MCP** → **Project 3** | spec-migration writeup |
| 16+ | **Venture Mode** — WIP=1, 14-day metric | **Rung 8**, **Rung 6** |
| any time after wk 8 | T6 → Soup/MLX fine-tune · T4 → fused Metal kernel · T2 → reproduction | **Rungs 3, 4, 5** |

**~16 weeks to hireable.** Nothing gates on rented hardware — rungs 3, 4 and 5 run on the M4 and can slot into any week after 8, ideally as the "rest day" work between production tracks.

---

## Decisions (resolved 2026-08-22)

1. **Domain:** Pakistani tax/corporate regulation (FBR / SECP / SBP). Rationale in Part IV.
2. **Compute: local only.** Soup + MLX on the M4 covers rungs 3 and 5; `mx.fast.metal_kernel()` covers rung 4. No GPU rental in the plan. Triton work does not port to Metal as code, only as concepts.
3. **Venture drives from ~week 11**, not 16 — Project 2's corpus *is* venture candidate #1's core technology, so the curriculum and the venture merge at that point rather than running sequentially.
4. **FaizOS MCP server stays local/stdio.** Project 3 is a spec migration plus a public writeup, not a remote deployment. Rung 2's URL comes from the P2 service.

## Still open

- **Which specific FBR/SECP corpus slice** to start with (Income Tax Ordinance + SROs? Sales Tax rules incl. 150Q e-invoicing? Companies Act?). Answer at P8, not now — it depends on what parses cleanly.
- **Whether to keep `/faiz-drill` FSRS separate** from the new 14-day rebuild gate, or merge them into one scheduler.
