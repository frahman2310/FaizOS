# The FaizOS course — complete content record

Everything covered, what was built, and how it was taught.

**20 modules · 44 builds · 66 skills · 52 revision notes.** Every project written from scratch in
plain Python — no PyTorch, no NumPy, no frameworks. Starting point: could not explain a transformer,
had never written working Python.

---

# Part I — How it was taught

## The Brick Method

The core teaching loop, established in the first sessions and never abandoned:

> **one tiny concept → ask a small question → WAIT for the answer → reveal the answer *and the reasoning* → next brick**

Rules that made it work:

1. **Start below the floor.** Begin one level simpler than the topic seems to need. The matmul lesson
   started at *"adding 2+5+9 is how many steps?"*
2. **One idea per message.** If a concept has two parts, that's two bricks.
3. **He does the doing.** Every answer is generated, not watched. Reveal only after an attempt.
4. **Define every term in one sentence + an analogy.** Never more. Over-explaining jargon was an
   identified failure mode.
5. **Anchor to what he already shipped.** Every new topic is framed as *"the thing you built, plus
   one addition."* This is why attention landed easily (it's a dot product + a softmax + a weighted
   sum, all previously built).
6. **On a wrong answer:** say what was right first, correct gently, give the one-line reason,
   re-check with a small variation before moving on.

## Walk the code

Added mid-course at his request (*"explain the code better, be simpler and more precise"*). Before
filling any blank, the build file is walked in 3–6 chunks, top to bottom:

- one plain sentence per chunk: what it does, then why
- **every unfamiliar Python token defined** as `token → meaning`
- every variable named in plain English
- the blank pointed at last, with a variable table and the answer's **return type**

Measured effect: blank errors dropped from "English phrase pasted as code" to zero across the next
three builds.

## The blank

Each build is a real, runnable file with **one to four blanks** — the conceptual heart, never
boilerplate. Everything fiddly (closures, `zip`, index arithmetic, formatting) is written for him
with explanation; he writes the line that *is* the idea. Every file ends with `assert`-based
self-checks and prints a real result.

## The consolidated format

From Module 16 onward, to cover ground faster: one build per **module** rather than per skill —
3–4 concepts, each carrying **its own worked number**, questions batched, one file with one blank per
concept, one module-level revision note.

**A hard limit was found and proven twice in one session:** nine concepts → 1 of 5 blanks correct;
three concepts an hour later → 3 of 3, zero corrections. **Four concepts is the cap.**

## The system running it

FaizOS is a Claude Code plugin: a local MCP server (TypeScript + SQLite) holding skills, mastery,
missions, streak, lessons, insights and revisions; slash commands; and session hooks.

- **`faizos_lesson_start`** loads accumulated teaching insights *before* each lesson
- **`faizos_record_lesson`** distils 1–2 new insights *after* it
- The loop closes: an insight recorded in one lesson changes how the next is taught

Deterministic artifacts, regenerated from the database with no model in the loop:
`REVISIONS.md` (per-lesson notes) · `REVISION.md` (study guide by module) · `SUMMARY.md` (coverage +
build index) · `SESSIONS.md` (session log) · `CAPSTONE.md` (portfolio audit).

---

# Part II — The content, module by module

## Modules 1–6 · Foundations
*Built first as needed, then backfilled properly in the foundations sweep (build #43).*

| build | what it establishes |
|---|---|
| **#1 Numerically stable softmax** | subtract the max before `exp` or large inputs overflow |
| **#2 Matmul FLOP estimator** | `2·M·N·K` — the cost model behind everything |
| **#3 micrograd** | autograd from scratch: `Value` with `+`, `*`, `tanh`, and `backward()` |
| **#4 tiny net that learns** | the training loop: forward → loss → backward → update |
| **#5 a real neuron** | weighted sum + bias + tanh |
| **#6 a layer of neurons** | many neurons over one input |
| **#7 MLP that learns XOR** | depth solves what one layer cannot (targets −1/+1 to match tanh) |

**The backfill (#43)** named the theory underneath:

- **SVD & low-rank** — any matrix = a sum of rank-1 pieces ordered by importance. Singular values
  `[10,6,2,1,0.5]`: the top **2 of 5 carry 96.3%** of the energy. *This is why LoRA works, why MLA
  works, and what PCA is.*
- **Probability** — expectation (the GRPO baseline is one), variance (`[2,4,6]` → 2.67), covariance
- **High-dimensional geometry** — random vectors in high dimensions are nearly perpendicular, which
  makes superposition possible; and a random `d`-dim dot product has typical size **√d**.
  **This is the origin of attention's `1/√d`** — a rule learned 30 builds earlier, explained here.
- **Regression** — `y = w·x + b` is the neuron without the tanh. `w = cov(x,y)/var(x)`
- **Bias–variance & double descent** — `error ≈ bias² + variance`; the classic U-curve, then the
  modern surprise that error falls *again* past the interpolation threshold
- **Complexity** — dict `O(1)` vs list `O(n)`: 1 check vs 1,000,000
- **Initialization** — Xavier `1/√fan_in`; the same disease residuals and RMSNorm treat
- **Profiling & dev setup** — cProfile ranks by cumulative time; `uv` + `ruff` + pinned Python + CI

---

## Module 7 · Attention & the modern block

| build | core mechanism |
|---|---|
| **#8 self-attention** | `weights = softmax([dot(q,k)]); out = Σ w·v` |
| **#9 QKV attention** | `score = (Q·K)/√d` — Q, K, V from learned matrices |
| **#10 RoPE** | rotate Q by `i·θ` and K by `j·θ` → score depends only on distance `i−j` |
| **#11 RMSNorm** | `x / √(mean(x²))` — rescale to a standard size |

**The through-line:** every token looks at every other token, decides who's relevant, and mixes in
their information. Bigger dot product = same direction = more relevant.

**Bug fixed in the process:** wrote `rotate(q, j·θ)` — the Query must rotate by **its own** position
`i`. Every score came out identical until corrected.

---

## Module 9 · Build a GPT

| build | core mechanism |
|---|---|
| **#12 Transformer block** | `x = x + attn(norm(x))`, `x = x + mlp(norm(x))`, stacked N deep |
| **#13 Train attention** | a learnable weight `wB = sigmoid(g)`, trained by gradient descent |
| **#14 BPE tokenizer** | merge the most frequent adjacent pair, repeat |
| **#15 KV cache** | cache past K,V; compute only the new token |

**Proof that residuals matter:** 30 blocks deep, signal RMS **27.7 with** residuals vs **0.07
without**. Same layers; the only difference is `+ x`.

**Training worked:** loss 4.0 → 0.002, `wB` 0.5 → 0.99. The model *discovered* it should attend to
the relevant token — nobody told it.

**BPE learned stacked merges:** `256=aa`, `257=aaa`, `258=aaab` — a 4-character chunk became one
token, unprompted.

**KV cache:** `n(n+1)/2 → n`. At n=100 that's **5050 → 100 computations, 50.5×**.

---

## Module 8 · Modern block upgrades

- **#16 SwiGLU** — `W2 @ (swish(W1@x) ⊙ (W3@x))`. Two branches: a smooth **gate** multiplied
  element-wise into a **content** branch. Taught with the dimmer-switch analogy after the formula
  alone didn't land. Keeps negative channels alive (−0.238) where ReLU zeroes them.
- **#17 GQA** — the KV cache scales with **K/V heads, not query heads**. 8 Q heads sharing 2 K/V →
  16 MB → 4 MB per layer. MHA → GQA → MQA is one dial.
- **#18 SSM / Mamba** — `state = a·state + b·x`, a fading running memory scanned in **O(n)**.
  Impulse response `1.0, 0.9, 0.81…`; bigger `a` = longer memory.

**A modern Llama block** = RMSNorm → GQA attention (with RoPE) → residual → RMSNorm → SwiGLU →
residual. Every piece built by hand.

---

## Module 10 · Scaling, evaluation, MLA

- **#19 Scaling laws** — `L(N) = A·N^(−α)`; a straight line on log-log, so you can extrapolate.
  Diminishing returns: every 100× in size buys a 10× cut in loss. **Chinchilla:** `C ≈ 6·N·D`,
  ~**20 tokens per parameter** (10B params → 200B tokens).
- **#20 Held-out eval** — `perplexity = exp(mean(−ln p))`, and it reads as *the effective number of
  choices the model is torn among*. Coin-flip model = exactly 2.00.
- **#21 MLA** — compress K/V into a small latent, cache only that, reconstruct on the fly.
  2048 → 64 numbers per token: **32× smaller**.

**The KV-cache trilogy:** KV cache (don't recompute) → GQA (share, 4×) → MLA (compress, 32×).

---

## Module 11 · GPU kernels

One sustained analogy: the GPU is a **chef** (superhumanly fast) beside a **warehouse** (HBM, 80 GB,
far) with a **tiny countertop** (SRAM, 20 MB, instant). A fetch costs ~1000 chops.

- **#22 Memory hierarchy & MFU** — `arithmetic intensity = FLOPs / numbers moved`. Vector add 0.33
  (memory-bound); matmul `2N/3` → **N=300 gives 200, still memory-bound**; N=1500 gives 1000
  (compute-bound). Ridge point ≈ 600. `MFU = achieved / peak` → 40% is a *good* run.
- **#23 Triton fused softmax** — a kernel is one recipe: `load → all the math → store`. Softmax
  unfused = 5 kernels = **10 HBM trips**; fused = **2**, independent of step count.
  `grid = ceil(n/BLOCK)`, `pid` picks the block, `mask` handles the remainder.
- **#24 FlashAttention** — the `n×n` score matrix doesn't fit (n=8000 → 64M entries). Tile the K/V,
  carry a running `(max, sum, output)`, and **rescale by `exp(m_old − m_new)`** when the max grows.
  **Output identical at every tile size; peak score-numbers 64,000,000 → 2.**

---

## Module 12 · Compile, profile, parallelism

- **#25 torch.compile & CUDA graphs** — fusion cost scales with **graphs, not ops**:
  `2 × n_graphs`. A graph break (a `print`, `.item()`, a data-dependent `if`) splits it. 6 ops:
  12 trips eager → 2 compiled → 4 with one break → **6 with two breaks (nothing gained)**.
  CUDA graphs replay a recorded launch sequence: **5000 µs → 5 µs**.
- **#26 Profiling & Amdahl** — `speedup = 1/((1−f) + f/s)`. Infinite speedup on a 10% part caps at
  **1.11×**; a lazy 2× on an 80% part gives **1.67×**. And the payoff: attention was the biggest
  *kernel* (42% → 1.27×) but **40% was idle time** (→ 1.67×). The bottleneck wasn't a kernel.
- **#27 Parallelism axes** — 70B = 140 GB won't fit in 80 GB. **Data parallel replicates**
  (throughput, not capacity); **tensor/pipeline shard** → 17.5 GB/GPU on 8. Pipeline bubble
  `(P−1)/(M+P−1)`: 75% idle at 1 microbatch → **8.6% at 32**.

---

## Module 13 · Distributed training

- **#28 Collectives** — **all-reduce** (everyone gets the whole result), **reduce-scatter** (each
  keeps a slice), **all-gather** (slices → everyone). The identity **all-reduce = reduce-scatter +
  all-gather**, derived by him and verified exactly. Ring cost `2·data·(n−1)/n`: a 1 GB all-reduce
  moves 1.5 GB → **15 ms on NVLink, 150 ms on Ethernet**.
- **#29 FSDP / ZeRO** — training costs **16 bytes per parameter** (weight 2 + grad 2 + fp32 master 4
  + Adam m 4 + Adam v 4), not 2. A 1B model = 16 GB/GPU. ZeRO-1/2/3 shard progressively:
  **16 → 5.5 → 3.75 → 2.0 GB**. Price: ~1.5× communication for 8× memory.
- **#30 Pipeline schedules** — GPipe holds **M** sets of activations; **1F1B holds P** (one per
  stage, capped by depth). Same bubble. At 128 microbatches: **192 GB vs a flat 6 GB**.
- **#31 Fault-tolerant checkpointing** — cluster MTBF = `gpu_mtbf / n_gpus` (10,000 h / 1000 =
  **10 h**, so ~96 crashes in a 40-day run). Overhead `write/T + (T/2)/mtbf`, minimised at
  `√(2·write·mtbf)` = **77 min**, where writing 6.5% ≈ rework 6.4%, total **12.9%**.

---

## Module 14 · Fine-tuning & inference

- **#32 LoRA** — freeze `W`, train `B(d×r) @ A(r×d)` beside it. `B@A` keeps W's shape (inner `r`
  cancels) while storing `2·d·r`. A 1000×1000 layer: **1,000,000 → 8,000** trainable at rank 4.
  For 7B: **112 GB → 0.1 GB** of trainable state. *Stored ≠ produced* — 8,000 numbers generate a
  1,000,000-entry grid.
- **#33 Quantization** — per group, `step = (max−min)/(levels−1)`; encode `round((x−lo)/step)`,
  decode `lo + q·step`. Error bounded by half a step. 8-bit 0.002 · **4-bit 0.063** · 2-bit 0.330
  (distinct weights collapse together). 7B: **14 → 3.5 GB**.
- **#34 Inference internals** — **paged KV** (waste 1848 → **8** tokens), **continuous batching**
  (idle 2700 → **0** slot-steps), **speculative decoding** (`accepted + 1` tokens per big pass;
  3 accepted → **4×**, never worse than 1×, output identical).
- **#35 Serving stacks** — **prefill is compute-bound** (TTFT 14 ms); **decode is memory-bound**
  (7 ms/step *regardless of batch*). So batching is free: **143 → 18,286 tokens/s** while each user
  still sees a steady 143. Decode is ~99% of a request — which is why every optimization targets it.

---

## Module 15 · RL foundations

- **#36 REINFORCE, baselines, PPO clipping** — a 7/10 doesn't tell you what the 10/10 was, so the
  only rule is *more of what beat the average*. `advantage = reward − mean`: rewards `5,7,9` →
  **−2, 0, +2** (always summing to zero). PPO clips `new/old` to **±20%**: 1.5 → 1.2, 0.5 → 0.8.
- **#37 GRPO & RLVR** — **RLVR**: a verifier gives a perfect 1/0 reward for maths and code, free and
  infinite (poetry can't be verified — hence what reasoning models train on). **GRPO**: the sampled
  group is its own baseline, deleting PPO's critic network (**7B → 0B**). Failure mode: a uniform
  group (`1,1,1,1` or `0,0,0,0`) gives **all-zero advantages** and teaches nothing.
- **#38 Reward modeling** — humans compare better than they score, so train on pairs:
  `P(A beats B) = sigmoid(gap)`. But it's a **proxy**: a `+0.1/sentence` leak makes a padded 5/10
  answer score **9.0** against a good 8/10 answer's **8.3**. Goodhart's law, in four lines.
  Defence: `reward − beta × drift`.

---

## Module 16 · Post-training & tools

- **Distillation vs RL** — copying a teacher is cheap and effective but **capped at the teacher**
  (70% → 70%). RL has no teacher, so no ceiling. In practice: distil to a good start, then RL past it.
- **RLHF vs DPO** — RLHF = 2 training stages, 3 models. **DPO** optimizes the preference pair
  directly = **1 stage, 2 models**. Why most open fine-tunes use it.
- **Tool calling** — the model is a **text predictor**; it emits text that *looks like* a call.
  **Your code** reads it, gates it against a registry, runs it, feeds the result back. Demonstrated:
  the model asked for `delete_file` on `/` → **refused**, because it wasn't in `TOOLS`. Four lines of
  code, not a model property. This is what MCP standardises — and how `faizos-core` itself works.

---

## Module 17 · Agents & retrieval

- **Production RAG** — vector search finds *meaning*, keyword search finds *exact strings*
  (`XR-4471B`). Run **both** (hybrid), retrieve ~50 cheap candidates, **rerank** to ~5.
  **Recall then precision:** a chunk at rank 37 never reaches a top-5 context — retrieved and still
  lost. Reranking moves it to rank 2.
- **Agent memory** — the context window is big, finite, and **resets**. Keep a persistent store
  outside it; retrieve the relevant few. 10M-token history in a 200k window → retrieve 20 × 500 =
  10k. *FaizOS's own `insights` table is exactly this.*
- **Agentic RL** — many steps, one delayed reward. Credit the **whole trajectory**:
  `advantage = reward − group_mean`, applied identically to every step.
- **Agent evals** — **pass@1 = reliability, pass@k = capability.** pass@1 40% / pass@8 75% (gap 35%)
  → retries and verification. pass@1 35% / pass@8 38% (gap 3%) → you need a better model.
  **Same low pass@1, opposite fixes.** Plus tracing: "40%" isn't actionable; "failed at step 3" is.

---

## Module 18 · Multimodal

- **ViT & CLIP** — **no new architecture**: cut the image into patches, each patch is a token, run
  the same transformer. 224×224 with 16×16 patches → **196 tokens**; at 384px → **576** (quadratic).
  **CLIP** trains image and text encoders so matching pairs have a high **dot product** — the same
  scoring from Module 7 — putting both in one space. That's what makes zero-shot work
  (cat 1.02 vs car 0.02, no cat training data).
- **Diffusion & rectified flow** — turn generation back into a **supervised** problem: add known
  noise, train the model to predict *that noise*. To generate: start from noise, predict, subtract,
  repeat. The path is curved so it needs many steps; **rectified flow** straightens it:
  **50 → 4 steps, 12.5×**.
- **VLM fusion** — image → ViT → 196 patch vectors → projected into the LLM's token dimension →
  prepended like text. The LLM never sees an image. Cost is context:
  a 1000-token question + 5 images = **1,980 tokens** — the pictures outweigh the words.

---

## Module 19 · Safety & interpretability

- **Scalable oversight** — how do you supervise a model better than you? **RLAIF** (an AI judges;
  pushes the question back a level), **debate** (judging is easier than solving), **weak-to-strong**
  (`PGR = (weak_supervised − weak)/(ceiling − weak)` → 33.3%).
  **The key contrast:** distillation is capped at its teacher, but weak-to-strong **exceeds** it
  (70% > 60%) — because the strong model already knows it; the weak labels only **elicit**.
- **SAEs** — a neuron doesn't mean one thing. **Superposition**: ~10,000 concepts in 512 neurons ≈
  19.5 each. An SAE widens 512 → **16,384** and forces only ~**20 active (0.12%)**, so each unit can
  afford one meaning — readable and steerable.
- **Prompt injection** — a fetched page saying *"ignore your instructions"* works because to the
  model **your instructions and that page are the same tokens**. There is no instruction channel.
  **Not fixable by prompting** — more instructions are just more tokens in the same stream.
  The defence is architectural: gate the tools. Demonstrated: injection requested `delete_rows` →
  blocked; a human-confirmed request → allowed; an unknown tool → blocked even when confirmed.

---

## Module 20 · Research method & capstone

- **Seeds** — identical code, different seed, different number. Baseline `[71.2, 68.9, 70.4]` →
  mean 70.2, **spread 2.3**. A "new best" of 70.9 is a 0.7 gain against 2.3 of noise: **nothing was
  measured.** Report mean ± spread over ≥3 seeds.
- **Compute-matched baselines** — method 10 h scores 74.0 vs baseline 5 h at 70.2 → looks like +3.8.
  Give the baseline the same 10 h → 73.5 → **the real gain is +0.5**, inside the noise. The most
  common way results mislead, including in good faith.
- **Ablations** — remove one component at a time. New loss worth **0.2**, new schedule **0.4**,
  extra data **3.7**. The paper would have been called *"our novel loss."*
- **Reproduction & OSS** — the method for both; the acts themselves are his to perform.
- **`CAPSTONE.md`** — honest 8-rung audit: **2 solid, 3 partial, 3 missing**. Understanding is well
  ahead of evidence. **The bottleneck is compute** — one rented GPU hour unlocks four rungs.

---

# Part III — Python learned along the way

Never taught abstractly; each token was introduced the first time a build needed it.

| | |
|---|---|
| **operators** | `**` to the power of · `//` divide and drop the remainder · `+=` add to a running total · `-(-a//b)` divide and round **up** |
| **three operator families** | `+ - * /` combine **numbers** · `< > <= ==` compare, giving **True/False** · `and or not` combine **True/False** |
| **brackets** | **`[ ]` looks up · `( )` runs.** `tools[name]` finds the function; `tools[name](args)` calls it |
| **collections** | list · **dict** (name → value, `O(1)`) · **set** (`|` = union) · tuple (fixed) |
| **comprehensions** | `[f(x) for x in xs]` · nested `[[..] for ..]` builds a grid · `[x for p in ps for x in p]` flattens |
| **built-ins** | `len` `sum` `min` `max` `round` `sorted` `zip` `abs` `enumerate` |
| **idioms** | `min(max(x, lo), hi)` clamps · `key=lambda kv: kv[1]` ranks by value · `[v] * n` repeats · `_` = "I don't need this" |
| **structure** | `return` takes an **expression only** — never an `=` · default arguments · returning several values at once |

**Recurring frictions, all recorded and pre-empted by the system:**
inverse relationships (duration↔rate, `exp`↔`ln`) · assignments written where expressions belong ·
ordering/pairing values to their sources · bare function names without brackets ·
missing an implicit "+1 free" term in a count.

---

# Part IV — What the record looks like

| file | contents | maintained by |
|---|---|---|
| `REVISIONS.md` | 52 full revision notes, chronological | saved each lesson |
| `REVISION.md` | the same, reorganised by module as a study guide | regenerated by hook |
| `SUMMARY.md` | coverage, per-module skills, full build index | regenerated by hook |
| `SESSIONS.md` | per-session log with ships and milestones | regenerated by hook |
| `CAPSTONE.md` | honest 8-rung portfolio audit | written once |
| `COURSE.md` | this document | written once |

All in [github.com/frahman2310/FaizOS](https://github.com/frahman2310/FaizOS), public, with all 44
project repos.

---

# The arc, in one line

**softmax → autograd → a neuron → attention → a transformer → training it → making it fast →
scaling it across a cluster → shrinking it to a laptop → aligning it → giving it tools → giving it
eyes → making it safe → and learning how to tell whether any of it is actually true.**
