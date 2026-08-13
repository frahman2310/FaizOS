# FaizOS — Revision Notebook

> Auto-compiled from every lesson. 47 entries, newest first.

---

## Module 16 Complete — Post-training &amp; tools (distillation vs RL, DPO, tool calling)
_2026-08-13_

**Why it matters:** A raw pretrained model is a text-continuation engine, not an assistant. Post-training is what turns it into one — and tool calling is what turns an assistant into an **agent**.

**What you built:**
```python
distilled_ceiling(t) = t                    # a copier cannot pass the copied
rl_ceiling(t)        = None                 # no teacher, no ceiling
RLHF: 2 stages, 3 models  |  DPO: 1 stage, 2 models
run_tool_call: if name not in tools: refuse ;  else tools[name](args)
```

**Concept 1 — distillation vs RL**
- **Distillation**: a strong teacher solves thousands of problems *showing its working*; you train a student on those traces. Ordinary supervised learning — there **is** a target. Cheap, fast, very effective.
- **The catch**: the student is **copying**, so it climbs toward the teacher's score and stops. Teacher 70% → student ceiling **70%**.
- **RL**: no teacher, so **no ceiling**. Slower and far more compute-hungry, but the only route to a model better than anything that trained it.
- **In practice both**: distil to get a good starting point cheaply, then RL to go past it.

**Concept 2 — RLHF vs DPO**
- **RLHF**: preference pairs → train a **reward model** → RL the policy against it. **2 training stages, 3 models** (policy, reward model, frozen reference).
- **DPO**: if the reward model only ever says "prefer A over B," skip it — optimise the pair **directly**, pushing the chosen answer up and the rejected one down relative to the frozen reference. **1 stage, 2 models.**
- Simpler, cheaper, no proxy to hack — which is why most open fine-tunes use DPO.

**Concept 3 — tool calling**
- The model is a **text predictor**. It cannot execute anything. It emits text that *looks like* a call: `{"tool": "calculator", "args": {...}}`.
- **Your code** reads it, checks it against an approved registry, runs it, and writes the result back into the conversation.
- **That gate is the entire safety story.** In the demo the model asked for `delete_file` on `/` — **refused**, because it isn't in `TOOLS`. Not a model property; four lines of your code.
- Exactly what **MCP** standardises — and how `faizos-core` works: the model emits a call, the server runs it.

**Key rules:**
```
distilled ceiling = teacher's score      RL ceiling = none
RLHF = 2 stages / 3 models               DPO = 1 stage / 2 models
tool loop = model asks -> code gates -> code runs -> result fed back
```

**Python you met here — and one important rule:**
- **`[ ]` looks up · `( )` runs.** `tools[name]` *finds* the function; `tools[name](args)` *runs* it. Finding someone in your contacts isn't the same as phoning them.
- Functions can be **stored in a dictionary** — that's what a tool registry is.
- `None` → "no value", used deliberately to mean *no ceiling exists* (different from zero).
- `PIPELINE["DPO"]["stages"]` → nested lookup, read left to right.
- `eval(s, {"__builtins__": {}})` → run a string as Python with everything dangerous stripped out.

**Gotchas / what to watch:**
- **The model never executes.** It asks. (The single most important idea in the module.)
- **Distillation's ceiling is real** — a distilled model can look excellent and still be structurally incapable of passing its teacher.
- **DPO removes the reward model, not the reference model** — you still need something to measure drift against.

**Where it sits + next:** Module 16 skills `reasoning-distillation`, `rlhf-dpo`, `tool-calling` — **completes Module 16**. Next: **Module 17, Agents & retrieval**.

---

## Module 15 Complete — RL foundations
_2026-08-13_

## 🏁 MODULE 15 COMPLETE — RL foundations

Modules 5–14 all trained against a **target**. Module 15 is the shift to learning from a **score** — the mechanism that turns a raw pretrained model into a chat model or a reasoning model.

### The through-line — score → group → proxy
1. **REINFORCE + PPO** — the core rule: do more of what beat the average, and never move too far at once.
2. **GRPO + RLVR** — let a verifier give the score and let the group be its own baseline; delete the critic.
3. **Reward modeling** — what to do when nothing can be verified, and why that's dangerous.

### Build-by-build recap
- **`rl-foundations/`** — a 7/10 tells you nothing about the 10/10 answer, so the only rule available is *more of what scored above average*. `advantage = reward − mean`: rewards `5,7,9` → **−2, 0, +2** (worst goes down, best goes up, always summing to zero). PPO then clips `new_prob/old_prob` to **±20%** so one noisy sample can't wreck the policy: `1.5 → 1.2`, `0.5 → 0.8`.
- **`grpo/`** — **RLVR**: for maths and code a checker gives a perfect 1/0 reward, free and infinite (poetry can't be verified — hence why reasoning models train on maths and code). **GRPO**: sample a group of answers to one prompt and use the group's mean as the baseline, deleting PPO's critic network (**7B → 0B**). Failure mode: a uniform group (`1,1,1,1` or `0,0,0,0`) gives all-zero advantages and teaches **nothing**.
- **`reward-modeling/`** — humans compare better than they score, so train a reward model on pairs: `P(A beats B) = sigmoid(gap)`. But it's a **proxy**: a leak of `+0.1/sentence` makes a padded 5/10 answer score **9.0** against a good 8/10 answer's **8.3**. Goodhart's law. Defence: `reward − beta × drift` from the reference model.

### Key formulas — one place
```
advantage   = reward - baseline            (sums to zero)
PPO clip    = min(max(new/old, 1-eps), 1+eps)
GRPO        = baseline is the GROUP mean   (no critic)
usable group <=> max(rewards) != min(rewards)
Bradley-Terry = sigmoid(score_A - score_B) (gap only)
KL leash    = rm_score - beta * drift
```

### The big gotchas
- **Pair each reward with its own advantage** — worst reward → most negative.
- **A uniform group is wasted compute**, not a small inefficiency — the gradient is exactly zero.
- **Tiny proxy flaws become huge** under optimization pressure.
- **Only expressions go in a `return`** — no `=` (this caught you three times across modules; worth a permanent note).
- **Signed formulas: compute the penalty first, then subtract it.**

### How it assembles
A modern post-training pipeline uses **all three**: verifiable tasks (maths, code) get **GRPO with a verifier** because the reward is free and unhackable; unverifiable tasks (helpfulness, tone) get a **reward model from human preferences**; and both are held on a **KL leash** to the reference model so the policy improves without drifting into gibberish or gaming the proxy. The reason reasoning models exploded in 2024–25 is precisely that RLVR removed the human from the loop.

### Coverage now
**60% of the course · 10 of 20 modules complete · 38 ships.** Remaining: post-training & tools (M16), agents & retrieval, multimodal, safety & interpretability, frontier research, and the capstone.

---

## Reward modeling — preferences, proxies and reward hacking
_2026-08-13_

**Why it matters:** RLVR only works where a checker exists. For everything else — helpfulness, tone, judgment — the reward must be *learned* from humans. And a learned reward is a **proxy**, which is where alignment gets genuinely hard.

**What you built + the core mechanism:**
```python
prob_a_preferred(a, b) = sigmoid(a - b)              # Bradley-Terry: only the GAP matters
flawed_rm(quality, n)  = quality + 0.1 * n           # a proxy with a length leak
penalised_reward(...)  = rm_score - beta * drift     # the KL leash
```

**The concept chain — every brick, in order:**
1. **Comparisons beat scores.** Humans are inconsistent at "rate this out of 100" but reliable at "which of these two is better." So preference data is collected in **pairs**.
2. **Turning pairs into numbers.** Train a reward model to output a score per answer such that the winner scores higher. `P(A beats B) = sigmoid(score_A − score_B)`.
3. **Only the gap matters.** `3 vs 1` and `5 vs 3` give the identical 0.88. Equal scores → `sigmoid(0) = 0.5` → no preference.
4. **The reward model is a proxy**, not the real goal — trained on finite data, with flaws.
5. **RL finds the flaws.** A leak of `+0.1 per sentence` is enough: a padded 5/10 answer scores **9.0** while a genuinely good 8/10 answer scores **8.3**. **The worse answer wins.** That's **Goodhart's law** — when a measure becomes a target, it stops being a good measure.
6. **The defence: a leash.** `reward_used = rm_score − beta × drift`. Moving further from the reference model costs you. `beta` sets the leash length. Same spirit as PPO clipping — *don't go too far*.

**Key formulas / rules:**
```
P(A preferred) = sigmoid(score_A - score_B)     # gap only; sigmoid(0) = 0.5
penalised      = rm_score - beta * drift        # more drift -> lower reward
```

**Gotchas / what to watch:**
- **No `=` inside a `return`.** `return` already means "hand this back" — only an expression follows. (Same shape as `residual = seq[i] + attn[i]` earlier.)
- **Build a signed formula in two steps:** compute the penalty (`beta * drift`), *then* subtract it. Cheaper than getting the whole line right at once.
- **A tiny proxy flaw is not a tiny problem** — RL amplifies it until it dominates.
- **The best defence is a verifier, not a bigger reward model** — which is why maths/code RL scaled so much faster than RLHF.

**Where it sits + next:** Module 15 skill `reward-modeling-verifiers` — **completes Module 15 (RL foundations)**. Not covered: DPO (skips the reward model entirely), constitutional/rubric rewards, LLM-as-judge.

---

## GRPO &amp; RLVR — group-relative RL with verifiable rewards
_2026-08-12_

**Why it matters:** This is the algorithm behind DeepSeek-R1 and modern reasoning models. It's the REINFORCE baseline taken one step further — and it deletes an entire neural network in the process.

**What you built + the core mechanism:**
```python
verify(answer, correct)   = 1.0 if answer == correct else 0.0   # RLVR: no human
group_advantages(rewards) = [r - mean(rewards) for r in rewards] # the group IS the baseline
has_signal(rewards)       = max(rewards) != min(rewards)         # uniform group = wasted
```

**The concept chain — every brick, in order:**
1. **RLVR — let a machine score it.** Human ratings are slow, costly, noisy, and charmable. For **maths** and **code**, a checker gives a perfect **1/0** reward instantly and infinitely. (Poetry can't be verified — which is exactly why reasoning models are trained on maths and code.)
2. **PPO's hidden cost.** It trains a **critic** network to predict the baseline — another model the size of the policy.
3. **GRPO's trick.** Sample a **group** of answers to the **same** prompt; use the group's own mean as the baseline. **Critic: 7B → 0B.**
4. **The advantage is unchanged** from REINFORCE — only the source of the baseline moved. Group `1, 0, 0, 1` → mean **0.5** → correct **+0.5**, wrong **−0.5**.
5. **The failure mode.** If every answer scores the same, the mean *equals* every reward, so **every advantage is 0** and the group teaches nothing. True for all-correct (too easy) *and* all-wrong (too hard).
6. **So difficulty must be tuned.** A group is only useful when its answers **disagree** — which is what DAPO fixes by filtering uniform groups and resampling.

**Key formulas / rules:**
```
reward     = 1 if verifier passes else 0
baseline   = mean of the GROUP (no critic network)
advantage  = reward - group mean
useful group  <=>  max(rewards) != min(rewards)
```

**Gotchas / what to watch:**
- **Pair each reward with its own advantage** — correct → positive, wrong → negative. (The table format is worth reusing whenever values must match sources.)
- **A uniform group is wasted compute**, not a mild inefficiency — the gradient is exactly zero.
- **Too easy and too hard fail identically** — both give a flat group.
- **The verifier must be hard to game** — a weak checker gets exploited (reward hacking).

**Python you met here:**
- `==` compares, `=` assigns, `!=` means "not equal"
- `1.0 if test else 0.0` → a one-line if-expression
- `max(list)` / `min(list)` → biggest and smallest
- `[0.0] * 4` → repeats a list · `{a!r}` → show a value with its quotes

**Where it sits + next:** Module 15 skill `rlvr-grpo`. Not covered: Dr.GRPO's length-bias fix, the KL penalty against a reference model, DAPO's dynamic sampling. **One skill left in Module 15: reward modeling & verifiers** — what to do when the task *can't* be auto-checked.

---

## RL foundations — REINFORCE, baselines and PPO clipping
_2026-08-12_

**Why it matters:** Everything up to now trained against a **target**. Every modern chat model is finished with **RL**, where there is no target — only a score. This is the mechanism behind RLHF, GRPO, and reasoning models.

**What you built + the core mechanism:**
```python
b   = sum(rewards) / len(rewards)          # baseline: the average
adv = [r - b for r in rewards]             # advantage: better or worse than typical
ratio = new_prob / old_prob                # how far the policy moved
clipped = min(max(ratio, 0.8), 1.2)        # PPO: never move too far at once
```

**The concept chain — every brick, in order:**
1. **Score, not target.** A 7/10 on your poem doesn't tell you what the 10/10 poem was. You can't compute a distance to the right answer, because none was given.
2. **So the only available rule** is: do more of what scored well, less of what scored badly.
3. **The policy** is the model's probability distribution over actions (for an LLM: probability of each next token). "Do more of it" = raise those probabilities.
4. **Raw rewards don't work.** If all rewards are positive (5, 7, 9), every probability rises — you learn nothing about which is *better*.
5. **The baseline fixes it.** `advantage = reward − mean`. Rewards `5, 7, 9` → mean **7** → advantages **−2, 0, +2**. The worst goes **down**, the best goes **up**.
   - **sign** = which way to push · **size** = how hard
   - Advantages always **sum to zero** — the policy shifts *between* actions instead of drifting.
6. **PPO's safety catch.** The advantage came from a small, noisy sample. Too big a step wrecks the policy permanently. So measure `new_prob / old_prob` and **clip to ±20%**: `0.45/0.30 = 1.5 → 1.2`, `0.15/0.30 = 0.5 → 0.8`, while `1.1` passes untouched.

**Key formulas / rules:**
```
baseline  = mean(rewards)
advantage = reward - baseline          (sums to zero)
update    = prob + lr * advantage      (positive advantage pushes UP)
ratio     = new_prob / old_prob
clipped   = min(max(ratio, 1-eps), 1+eps)      eps ~ 0.2
```

**Gotchas / what to watch:**
- **Pair each reward with its OWN advantage.** Lowest reward → most **negative**. Listing `2, 0, −2` for rewards `5, 7, 9` would push the model toward the *worst* answer.
- **Subtracting the mean is what creates meaning** — 5 isn't "bad" in the abstract, it's bad *next to 7 and 9*.
- **Advantage is added, not subtracted**, in the update — positive advantage means "more of this."
- **The clip works both ways** — it stops collapses as well as spikes.

**Python you met here:**
- `[r - b for r in rewards]` → `r` takes each reward in turn; the expression runs once per item and the results become a new list
- `min(max(x, lo), hi)` → the standard "keep `x` between `lo` and `hi`" idiom
- `clip=CLIP` → a default argument, filled in unless you override it

**Where it sits + next:** Module 15 skill `rl-foundations`. Not covered: the MDP formalism, multi-step credit assignment, and a learned critic as the baseline. Next: **RLVR & GRPO** — where the baseline becomes a *group* of sampled answers and the reward comes from a **verifier** instead of a human.

---

## Module 14 Complete — Fine-tuning &amp; inference
_2026-08-12_

## 🏁 MODULE 14 COMPLETE — Fine-tuning & inference

Modules 5–13 were about **building and training** a model. Module 14 is the pivot to **using** one: adapt it cheaply, shrink it, and serve it to real users. This is the most directly employable module so far.

### The through-line — adapt → shrink → serve
1. **LoRA** — adapt a model by training 0.8% of it.
2. **Quantization** — shrink the weights themselves to 4 bits.
3. **Inference internals** — stop wasting the GPU while serving.
4. **Serving stacks** — the two-phase structure that tells you *which* optimization matters.

### Build-by-build recap
- **`lora/`** — freeze `W`, train `B(d×r) @ A(r×d)` beside it. `B@A` keeps W's shape (the inner `r` cancels) while storing only `2·d·r` numbers. A 1000×1000 layer: **1,000,000 → 8,000** trainable at rank 4. For 7B: **112 GB → 0.1 GB** of trainable state. Catch: only **low-rank** updates (4 stencils, not any mural) — fine, because fine-tuning is a small structured nudge.
- **`quantization/`** — per group, `step = (max−min)/(levels−1)`; encode `round((x−lo)/step)`, decode `lo + q*step`. Error bounded by **half a step**. 8-bit 0.002, **4-bit 0.063**, 2-bit 0.330 (distinct weights collapse together). 7B: **14 → 3.5 GB**.
- **`inference-internals/`** — **paged KV** (waste 1848 → **8** tokens), **continuous batching** (idle 2700 → **0** slot-steps), **speculative decoding** (`accepted + 1` tokens per big pass; 3 accepted → **4×**, never worse than 1×, output identical).
- **`serving-stack/`** — **prefill is compute-bound** (TTFT 14 ms), **decode is memory-bound** (7 ms/step *regardless of batch*). Batching is free: **143 → 18,286** tokens/s while each user still sees a steady **143**.

### Key formulas — one place
```
LoRA params   = 2 * d * r          (vs d*d)      shape: (d x r)@(r x d) -> d x d
quant step    = (max - min) / (levels - 1)       decode: lo + q*step,  error <= step/2
bytes/weight  = bits / 8                         levels = 2 ** bits
paged waste   = ceil(n/page)*page - n
spec decoding = accepted + 1 tokens per big pass
decode step   = weights_bytes / bandwidth        (independent of batch)
throughput    = batch * 1000 / step_ms
```

### The big gotchas
- **"Stored" ≠ "produced"** — LoRA stores 8,000 numbers that produce a 1,000,000-entry grid.
- **Decode is `lo + q*step`** — start at the bottom and *add* steps, don't multiply.
- **`accepted + 1`** — the verifier's own token is free.
- **A duration is not a rate** — to get tokens/sec, the time goes on the **bottom**.
- **Optimize decode, not prefill** — decode is ~99% of a request (Amdahl).

### How it assembles
Take a base model → **quantize** it to 4 bits so it fits on one GPU → attach a **LoRA** adapter and fine-tune it for your task on a single card (that combination is **QLoRA**) → serve it with **paged KV**, **continuous batching** and **speculative decoding** → and know from the **prefill/decode** split which knob to turn when it's too slow. That is a complete, deployable product path — and it's exactly what a small team shipping on open models does.

### Coverage now
**55% of the course · 9 of 20 modules complete (5, 7, 8, 9, 10, 11, 12, 13, 14) · 35 ships.** Remaining: RL & post-training, agents & retrieval, multimodal, safety & interpretability, frontier research, and the capstone.

---

## Serving stacks — prefill vs decode, throughput vs latency
_2026-08-12_

**Why it matters:** This is where a model becomes a product. Understanding the two phases tells you *which* optimizations matter, what to promise users, and what it costs to run.

**What you built + the core mechanism:**
```python
decode_step_ms(batch)    = WEIGHTS_GB / BANDWIDTH_GB * 1000    # same for ANY batch size
decode_throughput(batch) = batch * 1000 / decode_step_ms(batch)
latency = prefill_ms(prompt) + (output_tokens - 1) * decode_step_ms(batch)
```

**The concept chain — every brick, in order:**
1. **Two phases, opposite bottlenecks.** **Prefill** pushes the whole prompt through at once → lots of math per weight read → **compute-bound**. **Decode** makes one token at a time, each reading every weight → **memory-bound**.
2. **The decode step is a fixed cost.** 14 GB ÷ 2000 GB/s = **7 ms**, whether you serve 1 user or 128 — you read the weights once either way.
3. **So batching is free.** One read → one token *per user*. Batch 32 gives 32 tokens for the same 7 ms.
4. **Throughput scales, per-user speed doesn't move.** 143 → 4,571 → 18,286 tokens/s total, while every user still sees a steady **143 tokens/s**.
5. **Latency = TTFT + decode.** A 500-token prompt prefills in **14 ms**; 200 output tokens take **1393 ms** more. Decode is ~99% of the request.
6. **Which is why** paged KV, continuous batching and speculative decoding all target **decode** — optimizing prefill would be optimizing the 1% (Amdahl, Module 12).

**Key formulas / rules:**
```
decode step   = weights_bytes / bandwidth        (independent of batch)
throughput    = batch * 1000 / step_ms           (tokens/sec, all users)
prefill FLOPs = 2 * n_params * prompt_tokens
latency       = TTFT + (output_tokens - 1) * step_ms
```

**Gotchas / what to watch:**
- **A duration is not a rate.** `decode_step_ms(...)` gives 7 ms *per step*; tokens/sec needs `1000 / step`, then `× batch`. If an improvement should make the number *bigger*, the time belongs on the **bottom**. (Same inversion as the Amdahl blank.)
- **Call functions with brackets.** `decode_step_ms` names it; `decode_step_ms(batch)` runs it.
- **`batch` is deliberately unused** in `decode_step_ms` — that *is* the insight.
- **`output_tokens - 1`** because prefill already produced the first token.
- **What really caps batch size is KV-cache memory**, not compute — exactly what paged KV relieved.

**Where it sits + next:** Module 14 skill `serving-stacks` — **completes Module 14 (Fine-tuning & inference)**.

---

## Inference internals — paged KV, continuous batching, speculative decoding
_2026-08-12_

**Why it matters:** Training a model is one problem; **serving** it to thousands of users is another. These three tricks are the difference between an expensive demo and a viable product — together, roughly 10× the throughput on the same hardware. This is what vLLM is.

**What you built + the core mechanism:**
```python
paged_kv_waste(n)      = ceil(n/PAGE)*PAGE - n    # pages on demand, not max reservation
static_batch_idle(ls)  = sum(max(ls) - n for n in ls)   # continuous batching makes this 0
tokens_per_big_pass(a) = a + 1                    # accepted drafts + the verifier's own token
```

**The concept chain — every brick, in order:**
1. **The KV reservation problem.** You must allocate cache *before* knowing the answer's length, so naive serving reserves the max: **2048 reserved, 200 used → 1848 wasted (~90%)**.
2. **PagedAttention.** Hand out small **fixed pages** (16 tokens) on demand, like an OS gives memory pages. 200 tokens → **13 pages**, only **8** wasted. Waste 1848 → 8.
3. **The batching problem.** Static batching runs until the **slowest** sequence ends. Lengths `[100,100,100,1000]` → three slots idle **900 steps each** = **2700** wasted slot-steps.
4. **Continuous batching.** Evict a finished sequence and admit a waiting one **immediately** → idle = **0**.
5. **Why speculative decoding is possible.** Generating one token reads **every weight** to produce **one number** — deeply memory-bound (Module 11). Since the GPU is starved anyway, verifying *many* tokens in one pass costs barely more than one.
6. **How it works.** A small **draft** model proposes k tokens; the big model **verifies all of them in a single pass** and keeps the longest correct prefix — **plus one free token** the verifier produced itself. 3 accepted → **4 tokens per pass**.
7. **It's safe.** Output is **identical** to plain decoding, and with 0 accepted you still get 1 — never slower.

**Key formulas / rules:**
```
naive KV waste  = max_len - actual_len
paged KV waste  = ceil(n/page)*page - n        (only the last partial page)
static idle     = sum(longest - n for each n)
continuous idle = 0
tokens per pass = accepted + 1
```

**Gotchas / what to watch:**
- **It's `accepted + 1`, not `accepted`.** The verification pass computes the big model's own prediction at the position after the last accepted token — correct by construction, so it's free.
- **A partial page costs a whole page** — round up, always.
- **Speculative decoding doesn't change the output**, only the speed. It is not an approximation.
- **The real speedup depends on the acceptance rate** — a bad draft model gets rejected often and gains little.

**Python you met here:**
- `-(-a // b)` → divide and **round up** (`//` rounds down; negating twice flips it)
- `page=PAGE` → a **default argument**: omit it and it fills itself in
- `sum(expr for x in list)` → build values and add them in one line

**Where it sits + next:** Module 14 skill `inference-internals`. Not covered: prefix caching, chunked prefill, and how draft quality sets the acceptance rate. **One skill left in Module 14: serving stacks.**

---

## Quantization — run a model in 4 bits
_2026-08-12_

**Why it matters:** LoRA shrank the *trainable* state; quantization shrinks the **weights themselves**. It's why a 7B model runs on a laptop, and combined with LoRA (that's **QLoRA**) it's why you can fine-tune one there too.

**What you built + the core mechanism:**
```python
step = (hi - lo) / (n_levels - 1)      # gap between neighbouring levels
q    = round((x - lo) / step)          # ENCODE: which level is x nearest
back = lo + q * step                   # DECODE: start at lo, climb q steps
```

**The concept chain — every brick, in order:**
1. **Bits → levels.** Each bit **doubles** the count: 1→2, 2→4, 3→8, **4→16**, 8→256. fp16 gives ~65,000 values per weight.
2. **That precision is unnecessary.** Round weights onto a coarse grid and the model still works — 65,000 paint shades vs 16; nobody sees the difference on most walls.
3. **Per-group mapping.** Take ~64 weights, find their `min` and `max`, and slice that range into `2**bits` evenly spaced levels. Small groups keep the range tight, which keeps the step small.
4. **The step.** `(max − min)/(levels − 1)`. For −1.0 to 1.0 with 5 levels → step **0.5**, levels `−1, −0.5, 0, 0.5, 1`. It's `levels − 1` because 5 fenceposts have 4 gaps.
5. **Encode then decode.** Encode: how far above `lo`, divided by `step`, rounded. Decode: `lo + q*step`. The `round` is the only lossy operation.
6. **Error is bounded by half a step** — you always round to the nearer side.
7. **The memory.** `bits/8` bytes per weight. 7B: **14 GB → 7 GB → 3.5 GB** at 16/8/4 bits.

**The degradation curve:** 8-bit error 0.002 (invisible) · **4-bit 0.063** (fine) · 2-bit **0.330** — at 2-bit, `−0.42` and `−0.05` both collapse to `−0.333`. **Distinct weights become the same number.** That's why 4-bit is the practical floor.

**Key formulas / rules:**
```
levels     = 2 ** bits
step       = (max - min) / (levels - 1)
encode     = round((x - lo) / step)
decode     = lo + q * step
max error  = step / 2
bytes/wt   = bits / 8
```

**Gotchas / what to watch:**
- **Decode is `lo + q*step`, not `lo * q * step`.** You *start* at the bottom of the range and *add* steps. A multiply would scale the range instead of offsetting into it.
- **`lo`, not `min`.** `min` is Python's built-in for finding a smallest value; the group's minimum is stored in `lo`.
- **`levels − 1`, not `levels`** — count gaps, not posts.
- **The endpoints are always exact** — `lo` and `hi` land on levels at every bit width.
- **Per-group, not per-tensor** — one outlier would stretch the whole range and blow up the step.

**Python you met here:** `2 ** bits` → to the power of · `round(x)` → nearest whole number · `min(list)`/`max(list)` → smallest/largest · `zip(a, b)` → walk two lists in pairs · `abs(x)` → size ignoring sign.

**Where it sits + next:** Module 14 skill `quantization`. Not covered: outlier handling, GPTQ/AWQ calibration, activation quantization, and **QLoRA** (4-bit frozen base + a LoRA adapter — the last two builds combined). Next: **inference internals** — paged KV, continuous batching, speculative decoding.

---

## LoRA — fine-tune 0.8% of the parameters
_2026-08-12_

**Why it matters:** Full fine-tuning a 7B model needs 112 GB — out of reach. LoRA makes it fit on one consumer GPU, and it's how essentially all open-model fine-tuning is done today.

**What you built + the core mechanism:**
```python
output = W @ x  +  (B @ A) @ x       # W frozen; only A and B are trained
lora_params(d, r) = d * r + r * d    # vs full fine-tuning's d * d
```

**The concept chain — every brick, in order:**
1. **Full fine-tuning is unaffordable.** 16 bytes per parameter (Module 13) × 7B = **112 GB**.
2. **Freeze the base.** No gradients, no optimizer state for `W`. It still gets *loaded* (2 bytes each) but costs none of the other 14.
3. **Train a skinny add-on** instead: `B` is `d×r`, `A` is `r×d`, and `r` (the **rank**) is small.
4. **The shape rule.** `B(1000×4) @ A(4×1000)` → the inner 4s **match and cancel**, leaving **1000×1000** — the same shape as `W`, so it can be added.
5. **Stored vs produced — the key distinction.** You *store* `2·d·r` = **8,000** numbers, but they *produce* a `d×d` = **1,000,000** grid. You keep the recipe, not the result.
6. **The honest catch.** Those 8,000 numbers can only produce **low-rank** updates — like painting a huge mural with 4 stencils. It works because fine-tuning is a small structured nudge, not a rebuild.

**Key formulas / rules:**
```
full fine-tune params = d * d
LoRA params           = d*r + r*d = 2*d*r
shape                 = B(d x r) @ A(r x d) -> d x d      (inner r cancels)
saving disappears at r = d/2
```

**The numbers (1000×1000 layer):** rank 1 → 0.20% · rank 4 → **0.80%** · rank 16 → 3.20% · rank 64 → 12.80%. For 7B: **112 GB → 0.1 GB** of trainable state.

**Gotchas / what to watch:**
- **"How many stored" ≠ "what shape is produced."** 8,000 stored, 1,000,000 produced. Different questions.
- **The LoRA count must contain `r`.** If the expression doesn't use the rank, it isn't LoRA — that's how you catch accidentally writing `d*d`.
- **Matrix shapes: keep the outside, cancel the inside.** `(3×2) @ (2×3)` → `3×3`.
- **Rank must stay small** — at `r = d/2` you're back to full fine-tuning.
- **The frozen base still occupies memory** — LoRA saves *optimizer* state, not the weights themselves.

**Python you met here:**
- `len(Y)` → number of **rows**; `len(Y[0])` → number of **columns**
- nested `[[... for j ...] for i ...]` → build a grid: outer loop makes rows, inner makes cells
- `{p:>10,}` → right-align with thousands commas; `{x:6.2%}` → percentage, 2 decimals

**Where it sits + next:** Module 14 skill `peft-lora` (also raised `linalg-matmul`). Not covered: QLoRA (4-bit frozen base), the alpha scaling factor, and merging `B@A` into `W` for zero-latency inference. Next in Module 14: **quantization**.

---

## Module 13 Complete — Distributed training
_2026-08-11_

## 🏁 MODULE 13 COMPLETE — Distributed training

Module 12 gave you the *theory* of splitting work across GPUs. Module 13 is what actually happens on a real cluster: how GPUs talk, how the training state is sharded, how the pipeline is scheduled, and how the run survives constant hardware failure.

### The through-line — talk → shard → schedule → survive
1. **Collectives** — the primitives GPUs use to combine work, and the identity everything else is built on.
2. **FSDP / ZeRO** — shard the *whole training state*, not just the weights.
3. **Pipeline schedules** — get a full pipeline without paying for it in memory.
4. **Fault-tolerant checkpointing** — finish a 40-day run on hardware that crashes every 10 hours.

### Build-by-build recap
- **`collectives/`** — **all-reduce** (everyone gets the full result), **reduce-scatter** (each keeps a slice), **all-gather** (slices become the whole). The identity **all-reduce = reduce-scatter + all-gather**, verified exactly. Ring cost `2·data·(n−1)/n`: a 1 GB all-reduce = 1.5 GB moved → **15 ms on NVLink, 150 ms on Ethernet**.
- **`fsdp-zero/`** — training costs **16 bytes per parameter** (weight 2 + grad 2 + fp32 master 4 + Adam m 4 + Adam v 4), not 2. ZeRO-1/2/3 shard progressively: 1B params on 8 GPUs → 16 / 5.5 / 3.75 / **2.0 GB per GPU**. Price: all-gather weights + reduce-scatter grads ≈ **1.5× comms for 8× memory**.
- **`pipeline-schedules/`** — GPipe holds **M** sets of activations, 1F1B holds **P** (one per stage, capped by depth). Same bubble; at 128 microbatches that's **192 GB vs a flat 6 GB**.
- **`checkpointing/`** — cluster MTBF = `gpu_mtbf / n_gpus` (10,000 h / 1000 = **10 h**). Overhead `write/T + (T/2)/mtbf`, minimised at `sqrt(2·write·mtbf)` = **77 min**, where writing 6.5% ≈ rework 6.4%, total **12.9%**.

### Key formulas — one place
```
all-reduce      = reduce-scatter + all-gather
ring bytes/GPU  = 2 * data * (n-1)/n
training bytes  = 16 per parameter (Adam, mixed precision)
ZeRO-3 memory   = 16 * n_params / n_gpus
GPipe peak      = M sets      |   1F1B peak = P sets
cluster MTBF    = gpu_mtbf / n_gpus
checkpoint opt  = sqrt(2 * write_cost * mtbf)
```

### The big gotchas
- **"all" in a collective name means everyone ends with the full result** — reduce-scatter has no "all" for a reason.
- **Weights are a small fraction of training memory** — the optimizer is 12 of the 16 bytes.
- **Backward frees activations, it doesn't store more** — don't double the count.
- **Sharding storage ≠ sharding compute** — FSDP still gathers the full layer to run it.
- **Even perfect checkpointing costs ~13%** of a large run.

### How it assembles
A real training job stacks all of it: **FSDP** shards the state across GPUs in a node, **pipeline parallel** (on a **1F1B** schedule) splits layers across nodes, every step moves gradients with **reduce-scatter** and weights with **all-gather** over the interconnect, and a **checkpoint** every ~77 minutes means a crash costs an hour instead of a month. Modules 11–13 together are the complete answer to *"how do you actually train a frontier model?"*

### Coverage now
**50% of the course · 8 of 20 modules complete (5, 7, 8, 9, 10, 11, 12, 13) · 31 ships.** Halfway. The entire *build-and-train* stack is done. Remaining: fine-tuning & inference (M14), RL & post-training, agents & retrieval, multimodal, safety, and the capstone.

---

## Fault-tolerant checkpointing — the optimal interval
_2026-08-11_

**Why it matters:** At scale, hardware failure isn't an edge case — it's the *normal operating condition*. A 40-day run on 1000 GPUs will crash ~96 times. Checkpointing is the only reason such runs ever finish.

**What you built + the core mechanism:**
```python
cluster_mtbf = gpu_mtbf / n_gpus
overhead     = write_min/interval + (interval/2)/mtbf     # writing + rework
optimal      = sqrt(2 * write_min * mtbf_min)             # where the two balance
```

**The concept chain — every brick, in order:**
1. **More GPUs, more failures.** One GPU fails every 10,000 h; **1000** GPUs → a crash every **10 h**. And since training is synchronous, **one dead GPU kills the whole job**.
2. **Checkpointing** saves the full training state; on a crash you reload and resume. Everything since the last save is **rework**.
3. **Expected rework = T/2.** A crash lands at a random point in the interval, so on average you lose **half** of it (60-min interval → 30 min lost).
4. **Two opposing costs.** Small T → tiny rework but constant writing. Large T → cheap writing but expensive crashes.
5. **The overhead curve:** `write/T + (T/2)/mtbf`. U-shaped: 100.4% at 5 min, **12.9%** at 77 min, 50.8% at 600 min.
6. **The optimum is where the costs are equal** — at 77 min, writing 6.5% ≈ rework 6.4%. That's exactly what `sqrt(2·write·mtbf)` finds.

**Key formulas / rules:**
```
cluster MTBF  = gpu_mtbf / n_gpus
rework share  = (T / 2) / mtbf          # half an interval, per crash-interval
writing share = write_cost / T
optimal T     = sqrt(2 * write_cost * mtbf)     (Young/Daly)
```

**Gotchas / what to watch:**
- **Failure rate scales with GPU count** — a "reliable" GPU is irrelevant at 1000×.
- **You lose half an interval, not the whole one** — crashes are uniformly distributed.
- **Keep units consistent.** The code converts everything to minutes; mixing hours and minutes gives a silently wrong answer.
- **Even optimal checkpointing costs ~13%** — the tax on scale. (Async checkpointing, overlapping writes with compute, is how real systems shrink it.)

**Python you met here:**
- `10_000` → just `10000`; underscores are allowed in long numbers for readability
- `n_gpus=1000` → passing an argument **by name** so it's unambiguous
- `sqrt(x)` → square root, from `math`
- `(a / 2) / b` == `a / (2 * b)` → dividing twice is the same as dividing by the product

**Where it sits + next:** Module 13 skill `fault-tolerant-checkpointing` — **completes Module 13 (Distributed training)**.

---

## Pipeline schedules — GPipe vs 1F1B
_2026-08-11_

**Why it matters:** Module 12 said microbatches shrink the bubble. It left out the catch: microbatches cost **memory**. The schedule you pick decides whether you can actually afford a full pipeline.

**What you built + the core mechanism:**
```python
peak_activations_gpipe(stages, m) = m         # one set per microbatch
peak_activations_1f1b(stages, m)  = stages    # one set per stage — flat in m
bubble_fraction(stages, m) = (stages-1)/(m+stages-1)   # same for both
```

**The concept chain — every brick, in order:**
1. **Forwards cost memory.** Every forward must **save its activations** so the backward can compute gradients. They're freed only when that microbatch's backward runs.
2. **GPipe** runs *all* forwards, then all backwards → at peak it holds **M** sets (8 microbatches → 8; 32 → 32).
3. **The conflict.** The bubble wants M **big**; memory wants M **small**. GPipe forces you to choose.
4. **1F1B** — once the pipeline is full, **alternate** one forward with one backward. Each backward **frees** a set exactly as the next forward takes one, so holdings stop growing.
5. **Why the cap is `stages`.** A microbatch is "**in flight**" from its forward until its backward. The pipeline has **one slot per stage**, so at most `stages` microbatches are in flight → at most `stages` sets of activations. **Depth caps memory, not microbatch count.**
6. **The payoff.** 4 stages, 128 microbatches: bubble **2.3%** for both — but GPipe needs **192 GB** of activations, 1F1B needs a flat **6 GB**.

**Key formulas / rules:**
```
bubble        = (P - 1) / (M + P - 1)      # identical for GPipe and 1F1B
GPipe peak    = M sets                     # grows with microbatches
1F1B peak     = P sets                     # flat — set by pipeline depth
activation GB = sets_held * gb_per_set
```

**Gotchas / what to watch:**
- **Backward does not add storage — it frees it.** Don't double the count for forward+backward. Peak = sets *saved and not yet consumed*. (This caught you twice: 16 for 8, and 8 for 4.)
- **1F1B's peak is independent of M** — that's its entire reason to exist.
- **Both schedules have the same bubble** — 1F1B buys memory, not speed.
- **`stages` is unused in the GPipe function** on purpose, so both take the same arguments.

**Python you met here:**
- `(4, 8, 32, 128)` → a **tuple**: a fixed list you don't intend to change
- `for m in (...)` → run the loop once per value, with `m` taking each in turn
- `:>7.1%` → format as a percentage with 1 decimal; `:>10.1f` → right-align, 1 decimal. Formatting only.

**Where it sits + next:** Module 13 skill `pipeline-schedules`. Not covered: **interleaved/virtual stages** (each GPU owns several non-contiguous stages, shrinking the bubble further) and zero-bubble schedules. One skill left in Module 13: **fault-tolerant checkpointing**.

---

## FSDP / ZeRO — shard the whole training state
_2026-08-11_

**Why it matters:** In the parallelism lesson we counted only weights. Real training memory is **8× that**, and it's why large models don't fit. FSDP is how every serious training run today makes them fit — built from the two collectives from the previous build.

**What you built + the core mechanism:**
```python
for name, b in BYTES.items():
    if name in SHARDED[stage]:  total += b / n_gpus   # split across GPUs
    else:                       total += b            # every GPU keeps it whole
```

**The concept chain — every brick, in order:**
1. **The hidden 16 bytes.** Per parameter, training with Adam in mixed precision stores: weight 2 + gradient 2 + fp32 master 4 + Adam `m` 4 + Adam `v` 4 = **16 bytes**. A 1B model = **16 GB/GPU** — 8× the 2 GB of weights.
2. **The optimizer is the problem**, not the model — 12 of those 16 bytes are optimizer state.
3. **ZeRO shards in stages:** ZeRO-1 = optimizer states; ZeRO-2 = + gradients; **ZeRO-3 = FSDP** = + the weights themselves.
4. **The numbers (1B params, 8 GPUs):** 16 → 5.50 → 3.75 → **2.00 GB/GPU**. ZeRO-1 alone does most of the work.
5. **The price is communication.** Each GPU stores only 1/N of a layer, so before computing it must **all-gather** the full weights, compute, then free them; on the way back it **reduce-scatters** the gradients.
6. **The trade:** ~**8× less memory for ~1.5× more communication** (4 → 6 GB/step). Worth it when memory is the blocker — which it usually is.

**Key formulas / rules:**
```
training bytes/param = 2 + 2 + 4 + 4 + 4 = 16      (bf16 weights & grads, Adam, fp32 master)
per-GPU bytes        = sum( b/n_gpus if sharded else b )
ZeRO-3 memory        = 16 * n_params / n_gpus
FSDP comms           ~ 1.5x DDP  (all-gather fwd+bwd + reduce-scatter)
```

**Python you met here:**
- `{"a": 1}` → **dictionary** (name → value); `{"a", "b"}` → **set** (a bag you ask "is it in here?")
- `set()` → an *empty* set — `{}` would mean an empty dictionary
- `.items()` → walk a dictionary as name-and-value pairs
- `in` → "is it present in this collection?" → True/False
- `+=` → add to a running total · `1e9` → 1 followed by nine zeros
- `:>12.2f` in an f-string → formatting only (width 12, 2 decimals), no logic

**Gotchas / what to watch:**
- **Weights are a small fraction** of training memory — always count optimizer state.
- **Sharded ⇒ divide by `n_gpus`; replicated ⇒ full cost.** That one line *is* ZeRO.
- **FSDP still needs the full layer to compute** — it gathers, computes, then frees. Sharding storage ≠ sharding compute.
- **Memory savings are paid for in bandwidth** — on slow interconnect FSDP can be *slower* than fitting a smaller model.
- **Activations aren't in this model** and are often the biggest term at long sequence length (fixed with activation checkpointing).

**Where it sits + next:** Module 13 skill `fsdp-run`. Two skills left in Module 13: **pipeline schedules** (GPipe vs 1F1B) and **fault-tolerant checkpointing**.

---

## Collectives — all-reduce, reduce-scatter, all-gather
_2026-08-11_

**Why it matters:** Multi-GPU training is mostly *communication*. These three operations are how GPUs combine work, and the identity between them is what makes FSDP possible. On slow interconnect, communication — not math — becomes the bottleneck.

**What you built + the core mechanism:**
```python
all_reduce(gpus)            # everyone ends with the full sum
reduce_scatter(gpus)        # everyone contributes, each keeps ONE slice
all_gather(pieces)          # each holds a slice -> everyone holds all slices
all_reduce_via_pieces(gpus) = all_gather(reduce_scatter(gpus))   # the identity
```

**The concept chain — every brick, in order:**
1. **Why talk at all.** Data-parallel GPUs hold identical models but train on different batch slices, so each measures a *different* gradient. They must average and all apply the **same** correction, or the copies drift apart. (+2,+4,+6,+8 → average **5**, and **all 4** GPUs need it.)
2. **all-reduce** — everyone contributes, everyone leaves with the whole result. The workhorse of data-parallel training.
3. **reduce-scatter** — everyone contributes, but each GPU keeps only **its own piece** (1 of 4 numbers).
4. **all-gather** — each GPU holds one piece; afterwards **everyone holds all pieces**.
5. **The identity:** `all-reduce = reduce-scatter + all-gather`. Verified exactly — both routes gave `[10,10,10,10]` on every GPU. FSDP is built on this.
6. **The cost.** The ring algorithm moves `2 × data × (n−1)/n` per GPU — about 2×, roughly **independent of GPU count**. A 1 GB all-reduce moves 1.5 GB: **15 ms** on NVLink (100 GB/s), **150 ms** on Ethernet (10 GB/s).

**Key formulas / rules:**
```
all-reduce      = reduce-scatter + all-gather
ring bytes/GPU  = 2 * data * (n_gpus - 1) / n_gpus     (~2x data)
time            = bytes_moved / bandwidth
```

**Python you met here:**
- `len(x)` → how many items · `//` → divide and drop the remainder
- `sum(g[i] for g in gpus)` → walk every GPU, take position `i`, add them
- `_` in a loop → "I don't need this value, just repeat"
- `list(total)` → make a **fresh copy** (so GPUs don't share one object)
- `[x for piece in pieces for x in piece]` → **flatten**: each piece, then each item in it
- `rank` → a GPU's ID number (standard distributed-training word)
- `all_gather(pieces)` → names take **underscores, not spaces**; **round brackets call** the function

**Gotchas / what to watch:**
- **All GPUs need the result**, not just one — that's why it's *all*-reduce, not plain reduce.
- **Reduce-scatter alone leaves each GPU with only a slice** — useless by itself; it's half of the pair.
- **The ring factor is `(n−1)/n`, slightly under 2×** — 1.5 GB for 4 GPUs, approaching 2 GB as GPUs grow.
- **Cost barely depends on GPU count, but hugely on the wire** — 10× between NVLink and Ethernet.

**Where it sits + next:** Module 13 skill `collectives-interconnect`. Next: **FSDP** — use exactly these two halves to shard a model across GPUs and still train it.

---

## Module 12 Complete — Compile, profile &amp; parallelism
_2026-08-11_

## 🏁 MODULE 12 COMPLETE — Compile, profile & parallelism

Module 11 gave you the hand tools (write a fast kernel). Module 12 gives you the **engineering practice** around them: let the compiler do it, measure before you optimize, and scale past one GPU.

### The through-line — automate → measure → scale
1. **torch.compile & CUDA graphs** — *automate* the fusion you hand-wrote in Triton, and kill launch overhead.
2. **Profiling & Amdahl** — *measure*, so you optimize the thing that actually matters.
3. **Parallelism axes** — *scale* when one GPU isn't enough.

The kitchen analogy completes here: the compiler is a **sous-chef** who reads the whole recipe list ahead; the profiler is the **stopwatch on the pass**; parallelism is **more kitchens** (identical / shared-dish / assembly-line).

### Build-by-build recap
- **`torch-compile/`** — graph capture enables automatic fusion: `trips = 2 × n_graphs`, **not** `2 × n_ops`. A graph break (print, `.item()`, data-dependent `if`) splits the graph and fusion can't cross it: 6 ops → 12 trips eager, 2 compiled, 4 with one break, **6 with two breaks (nothing gained)**. CUDA graphs replay a recorded launch sequence: 1000 × 5 µs = **5000 µs → 5 µs**.
- **`profiling/`** — Amdahl: `speedup = 1/((1−f) + f/s)`. Infinite speedup on a 10% part caps at **1.11×**; a lazy 2× on an 80% part gives **1.67×**. Profiles also expose **idle time**: attention was the biggest kernel (42% → 1.27×) but 40% GPU idle → **1.67×** was the real win.
- **`parallelism/`** — 70B = 140 GB won't fit in 80 GB. **DP replicates** (throughput, not capacity); **TP/PP shard** → 17.5 GB/GPU on 8 GPUs. Pipeline bubble `(P−1)/(M+P−1)`: 75% idle at 1 microbatch → **8.6%** at 32.

### Key formulas — one place
```
compiled trips  = 2 * n_graphs           (n_graphs = breaks + 1)
launch overhead = n_kernels * ~5us       -> CUDA graph: one replay
Amdahl          = 1 / ((1-f) + f/s)      ceiling for size-f part = 1/(1-f)
idle            = step_time - sum(kernel_times)
mem/GPU         : DP = total ;  TP/PP = total / n
bubble          = (P-1) / (M+P-1)
```

### The big gotchas
- **Count graphs, not ops** — and breaks are silent (`TORCH_LOGS=graph_breaks`).
- **Speedup puts time in the denominator** — if an improvement yields < 1, you've inverted it.
- **The biggest kernel isn't always the biggest win** — idle time often is.
- **Data parallel does not reduce per-GPU memory.** The most common misconception in the field.
- Weights are only part of memory: gradients, optimizer states (~2× params), activations usually dominate.

### How it assembles — the full performance loop
**Profile** → read the shape of the timeline → pick the cure: one fat kernel → *fuse it* (Triton/compile); many small kernels + gaps → *CUDA graphs*; low arithmetic intensity → *tiling* (FlashAttention); doesn't fit or too slow → *shard it* (TP/PP) or *replicate it* (DP). Modules 11 + 12 together are one skill: **make a model actually run fast on real hardware.**

### Coverage now
**45% of the course · 7 of 20 modules complete (5, 7, 8, 9, 10, 11, 12) · 27 ships.** The entire build-and-optimize stack is done. Remaining frontier: distributed training runs (FSDP), fine-tuning & PEFT/LoRA, inference engines, RL & post-training, agents & retrieval, multimodal, safety, and the capstone.

---

## Parallelism axes — data, tensor, pipeline
_2026-08-11_

**Why it matters:** Frontier models don't fit on one GPU — not close. *How* you split across a cluster decides whether training is possible at all, and whether your expensive GPUs are busy or idle.

**What you built + the core mechanism:**
```python
mem_per_gpu_data(total_gb, n)    = total_gb            # DP replicates
mem_per_gpu_sharded(total_gb, n) = total_gb / n        # TP/PP shard
bubble_fraction(P, M)            = (P - 1) / (M + P - 1)
```

**The concept chain — every brick, in order:**
1. **The problem.** 70B params × 2 bytes = **140 GB**. An H100 holds 80 GB. It doesn't fit.
2. **Data parallel (DP)** — many *identical kitchens*, each cooking different orders (batch slices), then averaging gradients. Every GPU keeps a **full copy** → buys **throughput, not capacity**. Adding GPUs does *not* make the model fit.
3. **Tensor parallel (TP)** — several chefs share *one dish*: split each weight **matrix** across GPUs. 140/8 = **17.5 GB/GPU → fits.** But they communicate every layer, so they need fast links (NVLink, same node).
4. **Pipeline parallel (PP)** — an *assembly line*: split the **layers** across GPUs. Also shards memory, and only communicates at stage boundaries, so it works **across nodes**.
5. **The pipeline bubble.** With 4 stages and one batch in flight, GPU1 works while **3 of 4 idle** = **75% waste** — the line is filling and draining.
6. **Microbatches fix it.** Split the batch so the line stays full: `(P−1)/(M+P−1)` → 4 stages gives 75% (M=1) → 27% (M=8) → **8.6%** (M=32).

**Key formulas / rules:**
```
model bytes     = n_params * bytes_per_param        (70B bf16 = 140 GB)
data parallel   : mem/GPU = total          (replicate)
tensor/pipeline : mem/GPU = total / n      (shard)
bubble fraction = (P - 1) / (M + P - 1)
```

**Gotchas / what to watch:**
- **DP does not reduce per-GPU memory** — the most common misconception. It splits *data*, not the *model*.
- **TP is chatty** (every layer) → keep it inside a node; **PP is cheap** → use it across nodes.
- **More stages = a bigger bubble** — `P−1` is in the numerator, so deep pipelines need many microbatches.
- **Weights aren't the whole story** — gradients, Adam optimizer states (~2× params) and activations usually dominate real memory. This model counted weights only.
- Real clusters combine axes ("3D parallelism": TP within a node × PP across nodes × DP over replicas).

**Where it sits + next:** Module 12 skill `parallelism-axes` — **completes Module 12** and the systems arc. Not yet covered: expert (MoE), sequence/context parallelism, and ZeRO/FSDP sharding of optimizer states.

---

## Profiling — Amdahl&#39;s law &amp; the real bottleneck
_2026-08-11_

**Why it matters:** Every optimization in Modules 11–12 assumed you knew where the time went. Profiling is how you find out — and Amdahl's law is how you decide whether an optimization is worth your week.

**What you built + the core mechanism:**
```python
new_total_time = (1 - fraction) + fraction / speedup
return 1 / new_total_time          # shorter time -> bigger speedup, so time goes on the bottom
```

**The concept chain — every brick, in order:**
1. **The trap.** A 100 ms step; you make a **10%** kernel *infinitely* fast. New time = **90 ms**, so speedup = `100/90` = **1.11×**. That's the ceiling for a perfect week's work.
2. **Amdahl's law:** your speedup is capped by the part you **didn't** optimize.
3. **The contrast.** An **80%** kernel made a lazy **2×** faster: 80 → 40, plus the untouched 20 = **60 ms** → `100/60` = **1.67×**. A modest win on the big thing beats a miracle on the small thing.
4. **Profiles show gaps too.** If a 100 ms step contains only 60 ms of kernels, the GPU was **idle 40 ms** — the CPU couldn't keep it fed (launch overhead, or a graph break dropping into Python).
5. **The timeline tells you which cure to reach for:**
   - one kernel dominates → optimize/fuse *that* one
   - many small kernels + big gaps → launch-bound → **CUDA graphs**
   - kernels slow with low arithmetic intensity → memory-bound → **fusion / tiling**
6. **The payoff that surprises people:** attention was the biggest *kernel* (42%; 2× on it → only 1.27×), but **40% was idle time** (killing it → **1.67×**). The bottleneck wasn't a kernel at all.

**Key formulas / rules:**
```
Amdahl : speedup = 1 / ( (1 - fraction) + fraction / s )
ceiling: making a part of size f infinitely fast caps at 1/(1-f)
idle   = step_time - sum(kernel_times)
```

**Gotchas / what to watch:**
- **Speedup puts time in the denominator** — `1 / new_time`. Shorter time must give a *bigger* number; if your formula returns < 1 after an improvement, you've inverted it.
- **Rank by share of runtime**, not by how slow a kernel "feels."
- **Idle time is invisible in a kernel list** — you only see it by comparing the kernel sum to the wall-clock step.
- **The biggest kernel is not always the biggest win** (attention 1.27× vs idle 1.67×).

**Where it sits + next:** Module 12 skill `profiling-nsight`. Last skill of the module (and of the systems arc): **parallelism axes** — what to do when one GPU isn't enough.

---

## torch.compile &amp; CUDA graphs
_2026-08-11_

**Why it matters:** In Module 11 you hand-wrote a fused kernel in Triton. You can't do that for every op in a model. `torch.compile` does it automatically — and CUDA graphs fix a *second*, unrelated cost that fusion can't touch.

**What you built + the core mechanism:**
```python
trips_eager(n_ops)       = 2 * n_ops        # every op round-trips HBM
trips_compiled(n_graphs) = 2 * n_graphs     # fusion is free INSIDE a graph
launch_overhead          = n_kernels * 5us  ->  CUDA graph: 5us total
```

**The concept chain — every brick, in order:**
1. **Eager mode is blind.** Each op runs the instant Python reaches it, with no knowledge of what comes next — so it *cannot* fuse. `x.relu().mul(2).add(1)` = 3 kernels = **6** trips.
2. **Graph capture.** `torch.compile` traces your Python and records the ops as one connected **graph**. Only then can it emit a fused kernel → **2** trips (a 3× win, for free).
3. **Graph breaks.** A `print()`, `.item()`, or data-dependent `if` can't be traced. The compiler compiles what it has, drops to Python, and starts a **new graph**. **Fusion cannot cross a break.**
4. **Cost scales with graphs, not ops:** `2 × n_graphs`. For 6 ops — 0 breaks → 2 trips; 1 break → 4; **2 breaks → 6, exactly what eager cost.** Compilation bought nothing.
5. **A second, separate cost:** every kernel launch takes the CPU ~**5 µs**. A step firing 1000 kernels burns `1000 × 5 = 5000 µs = 5 ms` of CPU overhead — the GPU idles waiting for order slips ("launch-bound").
6. **CUDA graphs:** record the entire launch sequence **once**, replay with a single call → 5000 µs → **5 µs** (1000×). Fixes overhead, not memory traffic.

**Key formulas / rules:**
```
eager trips     = 2 * n_ops
compiled trips  = 2 * n_graphs        # n_graphs = breaks + 1
launch overhead = n_kernels * ~5us
CUDA graph      = one replay, overhead paid once
```

**Gotchas / what to watch:**
- **The 2 never goes away.** Every graph still reads its input and writes its output; fusion only removes trips *between* ops inside it.
- **Count graphs, not ops** — that's the whole point of compiling.
- **`n_graphs = breaks + 1`** — 2 breaks means 3 graphs.
- **Breaks are silent.** Nothing errors; you just quietly lose the speedup. Hunt them with `TORCH_LOGS=graph_breaks`.
- **Two costs, two cures:** fusion fixes *memory traffic*; CUDA graphs fix *launch overhead*. Neither substitutes for the other.

**Where it sits + next:** Module 12 skill `torch-compile-cuda-graphs`. Every number here assumed you *knew* where the time went — next is **profiling**, the tool that tells you.

---

## Module 11 Complete — GPU kernels (Triton, FlashAttention)
_2026-08-10_

## 🏁 MODULE 11 COMPLETE — GPU kernels (Triton, FlashAttention)

Every module before this was about **what** a model computes. This one is about **how fast the hardware actually runs it** — the discipline that separates people who use models from people who make them fast.

### The through-line — diagnose → cure → apply
1. **Memory hierarchy & MFU** — *diagnose*: speed is bounded by data movement, not math. Measure it with arithmetic intensity; grade the run with MFU.
2. **Triton** — *cure*: write your own kernel so many operations happen per trip to memory (fusion).
3. **FlashAttention** — *apply*: use tiling + online softmax to fix the worst offender in a transformer.

One analogy runs through all three: the GPU is a **chef** (superhumanly fast at chopping) beside a **huge warehouse** (HBM: 80 GB, far) with a **tiny countertop** (SRAM: 20 MB, instant). Fetching costs ~1000× a chop. All GPU engineering is *"do more chops per walk."*

### Build-by-build recap
- **`gpu-memory-mfu/`** — arithmetic intensity = `FLOPs / numbers moved`. Vector add 0.33 (memory-bound); matmul `2N/3` → N=300 gives 200 (**still** memory-bound!), N=1500 gives 1000 (compute-bound). Ridge point = `peak FLOPs / bandwidth` ≈ 600. MFU = `achieved/peak` → 400/1000 TFLOP/s = 40%.
- **`triton-softmax/`** — a kernel is one recipe; `load → all the math → store`. Softmax unfused = 5 kernels = 10 HBM trips; fused = **2**, independent of step count (5× fewer). Programs & blocks: `grid = ceil(n/BLOCK_SIZE)`, `pid` picks your block, `mask` handles the remainder.
- **`flash-attention/`** — never build the `n×n` matrix. Tile the K/V, carry a running `(max, sum, output)`, and rescale by `exp(m_old − m_new)` when the max grows. Exact match to naive attention at every tile size; peak score-numbers **64,000,000 → 2**.

### Key formulas — one place
```
arithmetic intensity = FLOPs / numbers moved      (matmul: 2N/3)
ridge point          = peak FLOPs / bandwidth     (below = memory-bound)
MFU                  = achieved FLOPs-per-sec / peak
fused HBM trips      = 2        (vs 2 * n_steps unfused)
grid                 = ceil(n_elements / BLOCK_SIZE)
online softmax       = rescale acc & sum by exp(m_old - m_new), then fold in the tile
```

### The big gotchas
- **Small matmuls are memory-bound too** — being "a matmul" isn't enough; size decides.
- **Round the grid UP and mask** the leftover slots.
- **Rescale before folding a new tile in**, and correct **both** the sum and the value accumulator.
- **Fusion and tiling change speed, not math** — outputs are bit-for-bit the same.
- Powers of two: verify by doubling. Units belong in comments, not code.

### How it assembles
The three fit together as one skill: *measure* whether you're memory-bound (intensity/MFU) → *fuse* to cut trips (Triton) → *tile with a running accumulator* when the data can't fit (FlashAttention). That last pattern — a running `(max, sum, acc)` — is the same running-state idea as your SSM build, now used to defeat quadratic memory.

### Coverage now
**40% of the course · 6 of 20 modules complete (Modules 5, 7, 8, 9, 10, 11) · 24 ships.** You can now build a modern LLM, size it, evaluate it, **and make it fast on real hardware**. Next: Module 12 (compile, profile & parallelism) — then distributed training, fine-tuning/RLHF, agents, safety.

---

## FlashAttention — tiled attention with online softmax
_2026-08-10_

**Why it matters:** The most important kernel in modern AI. It made long context affordable — *without changing a single output value*. It's the payoff of everything in Module 11: memory hierarchy → fusion → tiling.

**What you built + the core mechanism:** attention that never materializes the `n×n` matrix.
```python
for each tile of K/V:
    m_new      = max(m, max(tile_scores))       # running max
    correction = exp(m - m_new)                 # rescale what's accumulated
    s   *= correction;  acc = [a*correction for a in acc]
    for score, v in tile:                       # fold in this tile
        p = exp(score - m_new);  s += p;  acc += p*v
    m = m_new
out = acc / s
```

**The concept chain — every brick, in order:**
1. **The problem is size.** Attention scores every token against every other → an `n×n` matrix. n=1000 → **1,000,000** entries; n=2000 → **4,000,000** (**quadratic** — double the context, quadruple the matrix); n=8000 → 64M ≈ 128 MB, versus ~20 MB of SRAM.
2. **Standard attention's cost:** it can't fit, so it writes the whole matrix to HBM, reads it back for softmax, reads it *again* for the value multiply — O(n²) memory **and** traffic.
3. **Tiling:** take one block of Keys/Values, compute only *that* block's scores on the countertop, fold them into a **running output**, discard, repeat. The full matrix never exists.
4. **The obstacle:** softmax needs the max and sum over the **whole** row, but a tile shows only part of it.
5. **Online softmax:** carry a **running max** `m`, **running sum** `s`, and **running output** `acc`. When a tile brings a bigger max, everything accumulated was measured against the *old* max — so rescale it by `exp(m − m_new)`, which is **< 1** (scaled **down**, because you're now subtracting a bigger number).
6. **Same pattern as your SSM** (`state = a·state + b·x`): a running accumulator updated block by block.

**Key formulas / rules:**
```
score matrix     = n × n            (quadratic in context length)
m_new            = max(m, max(tile_scores))
correction       = exp(m - m_new)   # < 1 when the max grows
s, acc          *= correction       # rebase, THEN add the new tile
out              = acc / s
peak memory      : naive O(n^2)  ->  flash O(tile)
```

**Gotchas / what to watch:**
- **Rescale before folding in the new tile** — rebase the old accumulator onto the new max first, or the sums are on mismatched scales.
- **Both `s` and `acc` get corrected** — the sum *and* the weighted-value accumulator, or the final divide is wrong.
- **Start `m` at `-inf`** so the first correction `exp(-inf − m_new) = 0` cleanly zeroes an empty accumulator.
- **It's exact, not approximate** — verified identical to naive attention at tile sizes 1, 2, 3, and 6. Tile size affects speed/memory only.

**The payoff:** identical output, peak score-numbers **64,000,000 → 2**. Long-context models exist because of this.

**Where it sits + next:** Module 11 skill `flash-attention` (also raised `attention` to 0.60) — **completes Module 11 (GPU kernels)**.

---

## Triton — a fused softmax kernel
_2026-08-10_

**Why it matters:** The previous lesson diagnosed the disease (memory-bound kernels). This is the cure. Fusion is the single biggest lever in GPU performance, and Triton is how you write it in Python instead of CUDA C++.

**What you built + the core mechanism:** Every Triton kernel is three moves:
```python
x = tl.load(in_ptr + pid * n_cols + offs, mask=mask)        # 1. WALK — one trip from HBM
x = x - tl.max(x, 0); e = tl.exp(x); y = e / tl.sum(e, 0)   # 2. CHOP — all steps in SRAM
tl.store(out_ptr + pid * n_cols + offs, y, mask=mask)       # 3. WALK BACK — one trip
```

**The concept chain — every brick, in order:**
1. **A kernel = one recipe** the GPU runs. `torch.softmax` is a pre-made recipe; Triton lets you write your own.
2. **The cost of not fusing.** Softmax has 5 steps (max, subtract, exp, sum, divide). As 5 separate kernels that's **5 round trips** = 10 HBM accesses. Fused: **1 trip** = 2 accesses → **5× fewer**.
3. **Programs & blocks.** You never loop over the data. You write the recipe for **one block**; the GPU launches many **programs** in parallel, and `pid = tl.program_id(0)` tells each which block is its job. (1000 chefs, same recipe card, each with a number.)
4. **The grid** = number of programs = `ceil(n_elements / BLOCK_SIZE)`. 8192/1024 = 8; 4096/512 = 8; 5000/1024 = **5** (rounded up).
5. **The mask.** Rounding up means the last program has slots past the end of the data — `mask = offs < n_cols` makes it ignore them. Without it you read garbage.
6. **Fusion rule:** put as many steps as possible **between the load and the store**.

**Key formulas / rules:**
```
unfused HBM trips = 2 * n_steps        # each step reads + writes
fused HBM trips   = 2                  # independent of n_steps  <- the whole point
grid              = ceil(n_elements / BLOCK_SIZE)
```

**Gotchas / what to watch:**
- **Round the grid UP**, never down — 7 programs for 8192/1024 leaves 1024 elements unprocessed.
- **Always mask** when the block doesn't divide the data evenly.
- **Powers of two**: verify by doubling (1024 → 2048 → 4096 → 8192 = ×8).
- **Python syntax**: units belong in comments, not code — `return 2`, never `return 2 trips`.
- Fusion changes **speed, not math** — the fused softmax still sums to exactly 1.0.

**The payoff:** fusion works when everything fits on the countertop. But attention's `n×n` score matrix **doesn't fit** — exactly the problem FlashAttention solves.

**Where it sits + next:** Module 11 skill `triton-basics` (also raised `floating-point-logsumexp` from mission #1). Next: **FlashAttention** — the last skill of Module 11.

---

## GPU memory hierarchy & MFU
_2026-08-10_

**Why it matters:** Every module so far was about *what* a model computes. This is about *how fast the hardware actually runs it* — and the answer is almost never "limited by math." It's limited by **moving data**. This one idea explains FlashAttention, kernel fusion, and why GPU bills look the way they do.

**What you built + the core mechanism:**
```python
intensity = flops / numbers_moved            # math per number fetched
RIDGE     = PEAK_FLOPS / NUMBERS_PER_SEC     # ~600 on an H100-ish machine
mfu       = achieved_flops_per_sec / PEAK_FLOPS
```

**The concept chain — every brick, in order:**
1. **The hierarchy.** A GPU is a chef in a tiny kitchen next to a huge warehouse. **HBM** = the warehouse (~80 GB, slow, far). **SRAM** = the countertop (~20 MB, instant, tiny). Every number must be walked from warehouse to countertop before use.
2. **The gap.** The chef does ~**1000 chops** in the time one ingredient is fetched. Fetching, not chopping, sets the pace.
3. **The instinct.** Once a number is on the countertop, **reuse it for as much math as possible**.
4. **Arithmetic intensity** = `math ÷ numbers moved`. Vector add: 100 additions ÷ 300 numbers = **0.33** (terrible). Matmul: `2N³ ÷ 3N² = 2N/3` — grows with N because each number is reused N times.
5. **Ridge point** = `peak FLOPs ÷ memory bandwidth` (~600 here). Below → **memory-bound** (math units starved). Above → **compute-bound** (good).
6. **MFU** = `achieved ÷ peak` FLOPs/sec. 400 of 1000 TFLOP/s = **40%**. Frontier runs hit 35–50%.

**Key formulas / rules:**
```
arithmetic intensity = FLOPs / numbers moved
matmul intensity     = 2N^3 / 3N^2 = 2N/3
ridge point          = peak FLOPs / memory bandwidth
MFU                  = achieved FLOPs-per-sec / peak FLOPs-per-sec
```

**Gotchas / what to watch:**
- **Intensity is a ratio, not a speed** — it says nothing about job size, only how well each fetch is exploited.
- **Size decides the verdict:** matmul N=300 → AI 200 → *still memory-bound*. Only N=1500 (AI 1000) crosses the ridge. Small matmuls waste the GPU.
- **MFU can't reach 100%** — some movement is unavoidable; 50% is excellent.
- Counting in *numbers* vs *bytes* changes the ridge value (bf16 = 2 bytes/number). Be consistent.

**The payoff:** the fix for memory-bound work is always the same — **fuse operations and tile the data** so one trip to the warehouse feeds many chops. That is exactly what Triton lets you write and what FlashAttention does to attention.

**Where it sits + next:** Module 11 skill `gpu-memory-hierarchy` (also raised `roofline-cost-model` from mission #2). Next: **Triton** (write a fused kernel), then **FlashAttention**.

---

## Module 10 Complete — Scaling, MLA & evaluation
_2026-08-10_

## 🏁 MODULE 10 COMPLETE — Scaling, MLA & evaluation

You can now build a modern model (Modules 7–9). Module 10 is how you **plan, measure, and cheapen** it — the engineering discipline around the model.

### The through-line
Three questions every lab asks about a model: **How good will it be before I build it?** (scaling laws), **How good is it, really?** (held-out eval), **How do I serve it cheaply?** (MLA).

### Build-by-build recap
- **`scaling-laws/`** — `L(N) = A·N^(−α)`: loss falls predictably with size (straight line on log-log → extrapolate). Diminishing returns (100× size = 10× loss cut). Chinchilla: `C ≈ 6·N·D`, ~20 tokens/param → 10B params want 200B tokens.
- **`heldout-eval/`** — perplexity = `exp(mean(−ln p))` on unseen data. Reads as the effective number of choices the model is torn among (coin flip = 2, GPT-2 ≈ 20). Held-out because training-set scores reward memorization.
- **`mla-attention/`** — compress K/V to a small latent (down-proj), cache only the latent, reconstruct via up-proj. 32× smaller cache (2048→64).

### Key formulas — one place
```
scaling  : L(N) = A * N^(-alpha) ;  C ≈ 6*N*D ;  D_opt ≈ 20*N
eval     : perplexity = exp(mean(-ln p))          # lower better, ≥ 1
MLA      : c = W_down @ x (cache) ;  K/V = W_up @ c (rebuild)
```

### The big gotchas
- **Diminishing returns are multiplicative** — equal loss drops cost exponentially more compute.
- **exp undoes ln** — perplexity `exp(-ln p)` puts the score back in "number of choices."
- **Never evaluate on training data** (leakage) — the score becomes meaningless.
- **Cache the latent, not K/V** (MLA), and reconstruction is approximate by design.

### How it assembles — the KV-cache trilogy
Three ways to tame the KV cache, now all yours: **KV cache** (M9, don't recompute) → **GQA** (M8, share heads, 4×) → **MLA** (M10, compress to a latent, 32×). Plus scaling laws to size the model and perplexity to grade it.

### Coverage now
**35% of the course · 5 of 20 modules complete (Modules 5, 7, 8, 9, 10) · 21 ships.** You've now covered the entire core of building, upgrading, sizing, and evaluating a modern LLM. Remaining frontier: GPU kernels (Modules 11–12), distributed training, fine-tuning/RLHF, agents, safety.

---

## MLA — Multi-head Latent Attention
_2026-08-10_

**Why it matters:** The KV cache is the memory bottleneck for long contexts. GQA shrank it by sharing; MLA shrinks it further by **compression** — it's how DeepSeek serves very long contexts cheaply. Upgrade #3 to the attention you built.

**What you built + the core mechanism:**
```python
c      = compress(x, W_down)      # token -> small latent  (down-projection)  [CACHE THIS]
K/V    = reconstruct(c, W_up)     # latent -> approx K/V    (up-projection, on the fly)
```

**The concept chain — every brick, in order:**
1. **Two levers to shrink the cache:** GQA *shares* K/V heads; MLA *compresses* K/V.
2. **The thumbnail idea:** squeeze each token's full Key+Value into a small **latent** vector `c`, cache only `c`. When attention needs K/V, blow the thumbnail back up. Works because K/V are **low-rank / redundant**.
3. **Two projections:** `W_down` compresses (x → c), `W_up` reconstructs (c → K/V). Both are `matvec`.
4. **Cache only the latent `c`** — never the reconstructed K/V. Cache/token = latent dim, not `2·n_heads·head_dim`.

**Key formulas / rules:**
```
compress    : c = W_down @ x            # big -> small latent
reconstruct : K = W_up  @ c             # small latent -> approx K (and V)
cache/token : d_latent    (vs full 2*n_heads*head_dim)
```

**Gotchas / what to watch:**
- **Cache the latent, not K/V.** Storing reconstructed K/V would defeat the point.
- Reconstruction is **approximate** — you accept a little error for a big memory win (fine because K/V are redundant).
- Real MLA folds the up-projection into the query so it never materializes full K/V at all (the speed trick); the toy here materializes them for clarity.

**Result:** token `[1,2,3,4]` → latent `[2,3]` (cached) → reconstructed `[2,3,2,3]`; at scale 2048 → 64 = **32× smaller cache**.

**Where it sits + next:** Module 10 skill `mla` — **completes Module 10**. The KV-cache trilogy is now yours: KV cache (M9) → GQA (M8) → MLA (M10).

---

## Held-out eval — perplexity
_2026-08-10_

**Why it matters:** You can build and train a model — but is it any *good*? Perplexity on held-out data is the standard, honest answer, reported in every LLM paper. Without a held-out set, a great score can just be memorization.

**What you built + the core mechanism:**
```python
surprises     = [-log(p) for p in true_probs]     # surprise per token = -ln(p)
mean_surprise = sum(surprises) / len(surprises)
perplexity    = exp(mean_surprise)
```

**The concept chain — every brick, in order:**
1. **Held-out:** measuring on training data rewards memorization (like testing a student on the exact questions they studied). Hold out unseen data; a big train-vs-held-out gap = **overfitting**.
2. **Per-token signal:** the model gives a probability to the TRUE next token. High p = good prediction; low p = bad. (0.8 beats 0.2.)
3. **Surprise:** `−ln(p)`. Perfect `p=1` → 0 surprise; small p → large surprise.
4. **Perplexity:** `exp(mean surprise)`. Reads as **the effective number of equally-likely options the model is torn among**. Perfect = 1; uniform guess over K words = K; GPT-2 on English ≈ 20.
5. **Worked case:** true word always p=0.5 → surprise `−ln(0.5)=0.693` → perplexity `exp(0.693)=2` → a 2-way coin flip. exp and ln are inverses.

**Key formulas / rules:**
```
surprise    = -ln(p)
perplexity  = exp( mean(-ln p) )          # lower is better
uniform over K options -> perplexity K
```

**Gotchas / what to watch:**
- **exp and ln are inverses**: `exp(ln 2) = 2`. Perplexity undoes the log so the score is in "number of choices," not log units.
- Use the probability of the **true** token, not the model's max probability.
- **Never** evaluate on data the model trained on — that's leakage, and the score becomes meaningless.
- Lower perplexity = better; it can never go below 1.

**Result:** good model 1.14, bad model 5.61, coin-flip model exactly 2.00.

**Where it sits + next:** Module 10 skill `heldout-eval` (also nudged `ml-lifecycle-leakage`). Last piece of Module 10: **MLA** (Multi-head Latent Attention) — compress the KV cache even further than GQA.

---

## Scaling laws — predict loss + Chinchilla sizing
_2026-08-10_

**Why it matters:** This is how labs decide what to build *before* spending millions. Scaling laws let you predict a giant model's loss from small runs, and Chinchilla tells you how to split a compute budget between model size and data. It's the economics of frontier AI.

**What you built + the core mechanism:**
```python
predicted_loss(N)   = A * N ** (-alpha)     # power law: loss vs size
chinchilla_tokens(N)= 20 * N                # ~20 tokens per parameter
compute_flops(N, D) = 6 * N * D             # ~6 FLOPs per param per token
```

**The concept chain — every brick, in order:**
1. **The surprise:** make a model bigger + train on more data → loss drops **smoothly and predictably**. You can forecast a huge model's loss from small ones.
2. **Power law:** `L(N) = A · N^(−α)`, α ≈ 0.07 for real LLMs. Negative exponent → bigger N, smaller L. On a **log-log plot it's a straight line** — that's why you can extrapolate.
3. **Diminishing returns:** improvement is a fixed *fraction* per 10×, not a fixed *amount*. With α=0.5, every **100×** in size = **10×** cut in loss (10 → 1 → 0.1). Equal drops cost exponentially more compute.
4. **Two levers:** loss depends on size `N` AND data `D`. Compute `C ≈ 6·N·D`.
5. **Chinchilla:** for a fixed compute budget, scale N and D **together** — ~**20 tokens per parameter**. Early models (GPT-3) were too big / under-trained; same compute, smaller model + more data = better.

**Key formulas / rules:**
```
L(N)  = A * N^(-alpha)         # power law, straight line on log-log
C     ≈ 6 * N * D              # training FLOPs
D_opt ≈ 20 * N                 # Chinchilla-optimal tokens
```

**Gotchas / what to watch:**
- **Negative exponent** = shrinking: `N^(-α) = 1/N^α`. In Python: `N ** (-alpha)`.
- Real laws add an **irreducible loss** `L∞` (a floor you can't beat): `L = L∞ + A·N^(-α)`.
- Chinchilla is about **compute-optimal training**; for cheap *inference* you may deliberately over-train a smaller model (e.g. Llama).

**Result:** predicted loss 10 → 1 → 0.1 across N=100 → 10k → 1M; a 10B model wants 200B tokens and ~1.2×10²² FLOPs.

**Where it sits + next:** Module 10 skill `scaling-laws`. Next in Module 10: **held-out evaluation** (perplexity — how you actually measure a trained model), then **MLA** (compress the KV cache further).

---

## Module 8 Complete — FFN, GQA & state-space models
_2026-08-10_

## 🏁 MODULE 8 COMPLETE — FFN, GQA & state-space models

You upgraded your vanilla transformer block into a modern (Llama-style) one, and met the main alternative to attention.

### The through-line
Module 9 gave you a *vanilla* transformer block. Module 8 is the set of **upgrades that modernize it**, plus one rival architecture:
1. **SwiGLU** — a better FFN (gated, smooth) replacing the ReLU MLP.
2. **GQA** — cheaper attention (share K/V heads) shrinking the KV cache.
3. **SSM / Mamba** — a non-attention token mixer that's O(n) by design.

Together with RoPE + RMSNorm (Module 7), SwiGLU + GQA are exactly what turn a textbook transformer into a Llama block.

### Build-by-build recap
- **`swiglu-ffn/`** — `W2 @ (swish(W1@x) ⊙ (W3@x))`. Two branches: a swish-activated **gate** (dimmer switches) multiplied element-wise into a **content** branch. Smooth, learned gating vs ReLU's hard on/off; keeps negative channels alive.
- **`gqa-attention/`** — KV cache scales with **K/V heads, not query heads**. 8 Q heads sharing 2 K/V = 4× smaller cache (MHA→GQA→MQA spectrum). 16→4→2 MB/layer.
- **`ssm-mamba/`** — `state = a·state + b·x; y = c·state`, scanned left-to-right. A fading running memory, O(n), no growing cache. `a` controls memory length.

### Key formulas — one place
```
SwiGLU : W2 @ ( swish(W1@x) ⊙ (W3@x) ) ,  swish(n)=n*sigmoid(n)
GQA    : KV cache = 2*seq_len*n_kv_heads*head_dim*bytes ;  saving = n_q/n_kv
SSM    : state = a*state + b*x ;  y = c*state           (O(n) scan)
```

### The big gotchas
- **`⊙` is element-wise**, not a dot product (SwiGLU gate).
- **KV cache scales with n_kv_heads**, the whole reason GQA saves memory.
- **SSM: `a` multiplies the state, `b` the input**; step 0 the state = the input (old state is 0).

### How it assembles
A modern **Llama block** = RMSNorm → GQA attention (with RoPE) → residual → RMSNorm → **SwiGLU** FFN → residual. You now own every one of those pieces (Modules 7, 8, 9). SSM/Mamba is the parallel track that swaps attention for an O(n) recurrence.

### Coverage now
**29% of the course · 4 of 20 modules complete (Modules 5, 7, 8, 9) · 18 ships.** Next: **Module 10** (scaling laws, MLA & evaluation) — how you measure and scale the model you can now build.

---

## SSM / Mamba — a running-state token mixer
_2026-08-10_

**Why it matters:** Attention is O(n²) — it chokes on very long sequences. State-space models (Mamba) mix tokens in O(n) with constant memory per step, making million-token contexts feasible. The main competitor to attention.

**What you built + the core mechanism:** A minimal SSM scanned over a sequence.
```python
for x in xs:
    state = a * state + b * x     # update the fading memory
    ys.append(c * state)          # read it out
```

**The concept chain — every brick, in order:**
1. **A different mixer:** attention has every token look at every other (O(n²)). An SSM reads the sequence like a stream, carrying ONE running state, updated per token — like keeping a running summary instead of re-reading the whole book each page.
2. **O(n):** constant work per token × n tokens = linear. No n² pairs, no growing KV cache.
3. **The recurrence:** `state = a·state + b·x`, `y = c·state`. `a` = how much old memory to keep, `b` = how much new input to add, `c` = readout.
4. **First-step subtlety:** `a` multiplies the OLD state (which is 0 at the start), `b` multiplies the input → step 0 makes state = the input. The decay only bites once there's memory to carry.
5. **Fading memory:** impulse `[1,0,0,…]` → `1, 0.9, 0.81, 0.729…` with a=0.9. Bigger `a` = longer memory (a=0.99 stays ~0.95 after 5 steps).
6. **Mamba's twist:** make `a, b, c` **input-dependent** (selective) so the model chooses what to remember — but the core is this recurrence.

**Key formulas / rules:**
```
state_t = a * state_{t-1} + b * x_t
y_t     = c * state_t
memory length ~ controlled by a  (closer to 1 = longer)
```

**Gotchas / what to watch:**
- **`a` hits the state, `b` hits the input** — not the other way round. (You got this right first try.)
- Step 0: state = input, because the old state is 0.
- This scalar version is the skeleton; real Mamba is multi-dimensional and *selective* (input-dependent knobs), and uses a parallel scan for GPU speed.

**Result:** impulse response fades geometrically; a=0.9 → 0.59 by step 5, a=0.99 → 0.95 — one knob controls memory length.

**Where it sits + next:** Module 8 skill `ssm-mamba` — **completes Module 8**. Next: Module 10 (scaling laws & evaluation) or wire these upgrades (SwiGLU/GQA) back into your Module 9 block.

---

## GQA — grouped-query attention
_2026-08-10_

**Why it matters:** The KV cache (your Module 9 build) is the #1 memory cost for long contexts. GQA shrinks it by letting query heads share K/V heads — it's why Llama 2/3 can hold long conversations. Upgrade #2 toward a modern block.

**What you built + the core mechanism:** A model of KV-cache memory across the MHA→GQA→MQA spectrum.
```python
kv_cache_bytes = 2 * seq_len * n_kv_heads * head_dim * bytes_per_num
#                ^K & V        ^scales with K/V heads, NOT query heads
```

**The concept chain — every brick, in order:**
1. **Heads:** real attention runs several in parallel (e.g. 8), each with its OWN Q, K, V, learning to track different things. You built one head; multi-head is many.
2. **The cost:** the KV cache stores K,V per head → 8 heads = 8× the cache. For long chats this dominates GPU memory.
3. **The GQA fix:** you need many *Query* heads (they look for different things) but not as many *K/V* heads — several Q heads can share one K/V. E.g. 8 Q heads, 2 K/V heads → groups of 4 share → 4× smaller cache.
4. **The spectrum (8 Q heads):**
   - **MHA**: 8 K/V heads — biggest cache, most expressive.
   - **GQA**: 2 K/V heads — 4× smaller (the modern default).
   - **MQA**: 1 K/V head — 8× smaller, slight quality loss.
5. **Key fact:** the cache scales with **n_kv_heads**, not n_q_heads. That's why sharing K/V is the lever.

**Key formulas / rules:**
```
KV cache/layer = 2 * seq_len * n_kv_heads * head_dim * bytes_per_num
saving factor  = n_q_heads / n_kv_heads     # MHA=1x, GQA(8->2)=4x, MQA(8->1)=8x
```

**Gotchas / what to watch:**
- The cache depends on **K/V head count**, not query-head count — the whole point. Using n_q_heads misses the savings.
- The "2" is because you cache **both** K and V.
- GQA doesn't reduce the number of Query heads (expressiveness is kept); it only reduces distinct K/V heads.

**Result:** 8 Q heads, seq 4096, head_dim 128 → MHA 16 MB, GQA 4 MB (4×), MQA 2 MB (8×) per layer. Over ~80 layers: 1.28 GB → 320 MB.

**Where it sits + next:** Module 8 skill `gqa`. Last piece of Module 8: a **state-space model (Mamba)** — a non-attention way to mix tokens that's O(n) by design.

---

## SwiGLU — a gated FFN upgrade
_2026-08-10_

**Why it matters:** The feed-forward network is ~2/3 of a transformer's parameters. Llama/PaLM replaced the plain ReLU FFN you built with **SwiGLU**, a gated version that routes information better. This is upgrade #1 that turns your vanilla block into a modern one.

**What you built + the core mechanism:** An FFN with a learned, smooth gate.
```python
gate    = swish(W1 @ x)      # dimmer settings (smooth, learnable)
content = W3 @ x             # raw brightness
hidden  = ewmul(gate, content)   # apply the dials, feature by feature
out     = W2 @ hidden
```

**The concept chain — every brick, in order:**
1. **The old FFN:** `W2 @ relu(W1 @ x)`. ReLU = `max(0, n)`: keep positives, hard-zero negatives. `[3,-2,0,5,-1] → [3,0,0,5,0]`.
2. **ReLU is crude:** negatives become *exactly* 0 → dead neurons, dead gradient there.
3. **Swish (SiLU):** `swish(n) = n·sigmoid(n)`. Smooth: ≈ ReLU for big positives, but a small live dip for negatives (gradient everywhere). `swish(2) = 2·0.88 = 1.76`.
4. **The gate (GLU):** two projections of x — a **content** branch and a **gate** branch — multiplied **element-wise** (`⊙`). The gate is a row of dimmer switches: `0` blocks a feature, `1` passes it fully, in between is partial. `[2,4,6] ⊙ [0.5,1,0] = [1,4,0]`. The dials are computed from the input and **learned**.
5. **SwiGLU = GLU with a swish gate:** `W2 @ (swish(W1@x) ⊙ (W3@x))`. Three matrices (W1, W3 in; W2 out) vs the plain FFN's two.

**Key formulas / rules:**
```
relu(n)   = max(0, n)
swish(n)  = n * sigmoid(n)             # sigmoid(n) = 1/(1+e^-n)
GLU gate  = A ⊙ G  (element-wise / Hadamard)
SwiGLU    = W2 @ ( swish(W1@x) ⊙ (W3@x) )
```

**Gotchas / what to watch:**
- **`⊙` is element-wise, NOT a dot product** — `[a0*b0, a1*b1, ...]`, same length in and out. (Used the `ewmul` helper, like `add` in the transformer-block build.)
- Gate value `0` = feature blocked; `1` = fully open. It's a *per-feature volume knob*, not a single on/off.
- Real SwiGLU uses a **larger hidden dim** (~8/3·d) so the 3-matrix version keeps a similar parameter count to the old 2-matrix FFN.

**Result:** on input `-2`, ReLU FFN gives `0` (dead) but SwiGLU gives `-0.238` (alive) — information keeps flowing.

**Where it sits + next:** Module 8 skill `swiglu` — upgrade #1 toward a Llama block. Next in Module 8: **GQA** (grouped-query attention — cheaper attention), then a **state-space model (Mamba)** taste to complete the module.

---

## Module 9 Complete — Build a GPT (nanoGPT → Llama)
_2026-08-10_

## 🏁 MODULE 9 COMPLETE — Build a GPT (nanoGPT → Llama)

You now own every core piece of a working language model: the block that thinks, the training that teaches it, the tokenizer that feeds it, and the cache that makes it fast.

### The through-line (how the builds connect into a real GPT)
A GPT is a pipeline: **text → tokens → stacked transformer blocks → next-token prediction**, generated one token at a time. This module built the parts that pipeline needs, plus proved they can *learn*:
1. **Transformer block** (mission #12) — the repeating compute unit (attention + MLP + residuals), stacked deep.
2. **Training** (mission #13) — gradient descent makes those blocks *learn* their weights from a goal.
3. **BPE tokenizer** (mission #14) — turns raw text into the integer tokens the block eats.
4. **KV cache** (mission #15) — makes one-token-at-a-time generation fast (O(n²)→O(n)).

### Build-by-build recap (each ship + its core mechanism)
- **`transformer-block-residuals-stacking/`** — `x = x + attn(norm(x)); x = x + mlp(norm(x))`, stacked N deep. Residuals (`+ x`) keep the signal alive so deep stacks train. Proof: 30 blocks, RMS 27.7 with residuals vs 0.07 without.
- **`train-attention/`** — a learnable attention weight `wB = sigmoid(g)`, trained with the loop `forward → loss=(out−target)² → backward → g -= lr·g.grad`. Loss 4.0→0.002, wB 0.5→0.99. First component that *learned* instead of being hardcoded.
- **`bpe-tokenizer/`** — count adjacent pairs (`get_stats`), merge the most frequent (`max(stats, key=stats.get)`) into a new token, repeat. Merges stack (aa→aaa→aaab). Compressed 11→5 tokens.
- **`kv-cache/`** — cache past K,V; compute only the new token's K,V each step. `n(n+1)/2` computes → `n`. 50.5× at n=100.

### Key formulas / rules — one place
```
block      : x = x + attn(norm(x)) ;  x = x + mlp(norm(x))
stack      : for _ in range(N): x = block(x)
train loop : forward -> loss=(out-target)**2 -> backward -> p.data -= lr*p.grad
sigmoid    : 0.5 + 0.5*tanh(0.5*g)          # raw score -> weight in (0,1)
BPE        : best = max(stats, key=stats.get) ; merge ; repeat
KV cache   : cache.append(compute_kv(step))  # only the new token -> O(n) not O(n^2)
```

### The big gotchas across this module
- **`+ x` is load-bearing** — remove residuals and a deep stack vanishes to ~0.
- **`lr` scales the gradient, not the parameter:** `p - lr*grad`, never `p*lr - grad` (hidden when lr=1).
- **Reset grads each step** or slopes accumulate.
- **`max(dict, key=dict.get)`** returns the winning KEY, not its count.
- **KV cache = compute only the new token** — looping over the past is the exact waste you're removing.

### How it all assembles (the payoff)
Everything now connects: **BPE** turns a prompt into tokens → embeddings run through **stacked transformer blocks** (attention + MLP + RoPE + RMSNorm, Modules 7 & 9) → the top predicts the next token → the **KV cache** makes each step cheap → and the **training loop** (Modules 5, 6, 9) is how the whole thing learned its weights. That's a GPT. You have hand-built every conceptual piece.

### Coverage now
**24% of the course · 3 of 20 modules complete (Modules 5, 7, 9 at 100%) · 15 ships.** Next options: **Module 8** (SwiGLU / GQA / Mamba — modern component upgrades) or **Module 10** (scaling laws, MLA & evaluation).

---

## KV cache — fast generation
_2026-08-10_

**Why it matters:** This is what makes generation *fast enough to use*. Without it, a long chat gets quadratically slower; with it, each new token costs the same. It's why ChatGPT streams smoothly.

**What you built + the core mechanism:** A model of autoregressive generation that counts K,V computations with and without a cache. The heart:
```python
cache = []
for step in range(n):
    cache.append(compute_kv(step))   # compute ONLY the new token; the past is already cached
```

**The concept chain — every brick, in order:**
1. **Autoregressive generation:** a GPT writes one token at a time, feeding each output back in. To predict a new token, attention needs the Key & Value of every token so far.
2. **The naive waste:** recompute K,V for ALL tokens each step → step costs `1, 2, 3, …, n`. Total = `1+2+…+n = n(n+1)/2` → **O(n²)**.
3. **The key fact:** a past token's K,V **never change**. Recomputing them is redundant.
4. **The cache:** store each token's K,V once; each step compute only the NEW token's K,V and append. Total = `n` computes → **O(n)**.
5. **Attention still reads the whole cache** — you just stopped *recomputing* the old entries.

**Key numbers / rules:**
```
no cache : n(n+1)/2 computes   (O(n^2))
cache    : n computes          (O(n))
n=100    : 5050 vs 100  = 50.5x
```

**Gotchas / what to watch:**
- **Don't loop over the past in the cached version.** `range(step+1)` re-does all previous tokens — that IS the waste you're removing. Compute only `step`.
- The cache **grows** by one entry per token — real systems bound it with a sliding window / eviction for very long contexts.
- The cache stores **K and V**, not Q — the new token brings its own Query; it needs the *past* Keys/Values to attend to.

**Result:** no-cache `n(n+1)/2` vs cache `n` → **50.5× at n=100**, matching the `15 vs 5` you computed by hand at n=5.

**Where it sits + next:** Module 9 skill `kv-cache` — and this **completes Module 9 (Build a GPT)**. Next gap: wire the cache into a real tensor attention forward pass. Or move to Module 8 (SwiGLU/GQA/Mamba) or Module 10 (scaling & evaluation).

---

## BPE tokenizer from scratch
_2026-08-10_

**Why it matters:** This is step 1 of *every* language model — text must become integer tokens before the network can touch it. BPE is the exact scheme GPT/Llama use, and now you've built it.

**What you built + the core mechanism:** A tokenizer that learns its own vocabulary by merging frequent pairs. The heart of the train loop:
```python
stats = get_stats(ids)              # {pair: count} for every adjacent pair
best  = max(stats, key=stats.get)   # the MOST FREQUENT pair  <- the whole idea
ids   = merge(ids, best, new_id)    # replace it with one new token, repeat
```

**The concept chain — every brick, in order:**
1. **Why tokenize:** nets do math on numbers, not letters. Turn text → list of ints.
2. **Char tokens are wasteful** (sequences too long); **word tokens** need a huge vocab and break on unseen words. BPE is the middle ground.
3. **The merge:** find the most frequent adjacent pair, replace every occurrence with ONE new token. `"aaabdaaabac"` (11) → merge `aa` → `Z a b d Z a b a c` (9). Greedy left-to-right: `aaa` → `Z a`, not `a Z`.
4. **Repeat:** each merge adds one vocab token and shortens the sequence. Real GPT ≈ 50k merges.
5. **Merges stack:** `256=(a,a)`, `257=(256,a)="aaa"`, `258=(257,b)="aaab"` — a merge can build on an earlier merge, so common multi-char chunks become single tokens automatically.

**Key ideas / rules:**
```
get_stats : count every adjacent pair          -> {pair: count}
best pair : max(stats, key=stats.get)           # highest count
merge     : replace pair with new_id (greedy, left to right)
new ids   : start at 256 (after the 256 byte values), then 257, 258, ...
```

**Gotchas / what to watch:**
- **`max(dict, key=dict.get)`** returns the KEY with the biggest value — not the value. That's what you want (the pair, not its count).
- **Greedy, non-overlapping merge:** after merging a pair, skip BOTH tokens (`i += 2`); don't re-use the second one.
- Ties (two pairs with equal count) are broken by whichever `max` sees first — fine for learning.
- New token ids must not collide with the 0–255 byte values → start at 256.

**Result:** `"aaabdaaabac"` compressed 11 → 5 tokens in 3 merges, learning `aa → aaa → aaab`.

**Where it sits + next:** Module 9 skill `tokenizer-bpe`. Gaps: add a `decode()` (ids → text) and train on a real corpus. Next: the **KV cache** — the last Module 9 skill — to make generation fast.

---

## Train attention — a learned attention weight
_2026-08-10_

**Why it matters:** Until now every model you built used *fixed* numbers. This is the first time a transformer-family component **learned** its own weights from a goal, by gradient descent — the thing that makes a real network intelligent. It proves the block you assembled is *trainable*.

**What you built + the core mechanism:** A tiny attention model with ONE learnable parameter `g`, trained until it learns to attend to the relevant token. The heart is the 4-step loop repeated 100×:
```python
output, wB = forward()               # 1. forward:  blend the tokens by their attention weight
loss = (output - target)**2          # 2. loss:     how wrong (squared error)
g.grad = 0.0; loss.backward()        # 3. backward: fill g.grad (your micrograd)
g.data = g.data - lr * g.grad        # 4. update:   step g downhill
```

**The concept chain — every brick, in order:**
1. **The training loop** = forward → loss → **backward** → update, repeated. (backward = backpropagation = your `Value.backward()` handing every weight its slope.)
2. **What's learnable:** the attention weight. Before, it came from a fixed softmax; now a raw score `g` is a *parameter* gradient descent tunes.
3. **The blend:** `output = wA·vA + wB·vB`, with `wA + wB = 1`. Worked example: `wB=0.9` → `0.1·1 + 0.9·5 = 4.6`. 50/50 → `3.0` (both terms count!).
4. **Score → valid weight:** a raw `g` can be any number, but a weight must be in [0,1] — squish with **sigmoid** (S-curve: −∞→0, 0→0.5, +∞→1). Built from your tanh: `sigmoid(g) = 0.5 + 0.5·tanh(0.5·g)` — no new autograd rule needed.
5. **The loss:** `(output − target)²`. Squares to stay positive and punish big misses. `(3−5)² = 4` at the start.
6. **The update:** `g.data = g.data − lr·g.grad`. `lr` scales the STEP (the gradient), not the parameter. Downhill = minus the slope.

**Key formulas / rules:**
```
sigmoid(g) = 0.5 + 0.5*tanh(0.5*g)         # any number -> (0,1)
loss       = (output - target)**2           # squared error
update     : p.data = p.data - lr * p.grad  # gradient descent step
```

**Gotchas / what to watch:**
- **`lr` multiplies the gradient, not the current value.** `g.data - lr*g.grad`, NOT `g.data*lr - g.grad`. (With lr=1 both happen to match — which hides the bug. It breaks for any other lr.)
- **Reset the grad each step** (`g.grad = 0.0`) before `backward()`, or slopes accumulate across steps and the update goes haywire. (Intermediate Values are rebuilt each forward pass, so only the persistent parameter needs manual reset.)
- **Both blend terms count** — 50/50 of {1, 5} is 3.0, not 0.5.
- Downhill = **minus** the slope. Plus would climb the loss.

**The result:** loss `4.0 → 0.002`, `wB 0.5 → 0.99`, output `3.0 → 4.96`. Nobody told it `wB` should be high — it *discovered* that from the gradient. That's learning.

**Where it sits + next:** Reinforces `autograd-backprop` (Module 5) + `attention` (Module 7); first step into training. Gaps to close next: (1) real attention learns whole **Q/K/V weight matrices**, not one scalar gate; (2) this used plain SGD with lr=1 — next is a real optimizer (Adam) + schedule. Immediate next build: **finish Module 9** — a tokenizer + KV cache to turn a forward pass into real text generation.

---

## Transformer block — residuals + stacking
_2026-08-10_

**Why it matters:** This is the first thing that looks like a *real model*. A GPT is nothing but this one block, stacked dozens of times. It ties together everything you built (attention, MLP, RMSNorm) with the one piece of glue that makes deep networks trainable: the **residual connection**.

**What you built + the core mechanism:** A transformer block that stacks 30 deep and keeps its signal alive. The whole block is two residual-wrapped sub-layers:
```python
x = x + attention(norm(x))    # sub-layer 1: tokens talk to each other
x = x + mlp(norm(x))          # sub-layer 2: each token thinks alone
```
Stacking is just: `for _ in range(N): x = block(x)`.

**The concept chain — every brick, in order:**
1. **Vanishing signal.** A layer that does `x → 0.5·x`, stacked 10 deep, gives `0.5¹⁰ ≈ 0.001` — the signal (and the gradient) vanishes. Deep naive stacks are untrainable.
2. **The residual fix.** Wrap each layer: `out = x + layer(x)`. The original `x` flows straight through; the layer only computes a small *edit* on top. Like "track changes" — keep the original, layer edits on top.
3. **Why it works.** With `+ x`, the default behavior is "do nothing" (`out = x + 0 = x`). Signal always has a clear path. Example: 10 layers each adding `+0.1` → `1.0 + 10×0.1 = 2.0`, no vanishing.
4. **Two sub-layers.** attention = tokens talk to each other (cross-token mixing, your QKV build). MLP = each token thinks alone (same net applied per-position, no cross-token talk). Delete attention → token #5 can never depend on token #2.
5. **Pre-norm.** `norm(x)` (your RMSNorm) goes *inside* each residual, before the heavy layer: `x = x + layer(norm(x))`. This is what Llama/GPT use.
6. **Stacking.** Each block's output is the next block's input: `x = block(x)`, N times. That's depth.

**Key formulas / rules:**
```
residual   : out = x + layer(norm(x))
block      : x = x + attn(norm(x)) ;  x = x + mlp(norm(x))
stack      : for _ in range(N): x = block(x)
```

**Gotchas / what to watch:**
- **`+` on Python lists CONCATENATES, it doesn't add.** `[1,2]+[3,4]` → `[1,2,3,4]`, not `[4,6]`. Use an `add()` helper for elementwise vector addition — this is the residual in code.
- **A list comprehension holds an expression, not an assignment** — `[add(a,b) for ...]`, never `[x = add(a,b) for ...]`.
- **The stacking blank is `seq = block(seq)`** inside the loop — reassign so each block feeds the next; `return seq` comes after the loop.
- attention = cross-token, MLP = per-token. Easy to flip; don't.

**Proof it works:** 30 blocks deep — WITH residuals RMS stayed `27.7` (alive); WITHOUT residuals it fell to `0.07` (vanishing). Same layers, only the `+ x` differs. That single addition is why GPT can be 96 layers deep.

**Where it sits + next:** Curriculum skill `nanogpt-llama-block` (Module 9: Build a GPT). Next gaps: (1) train the block end-to-end with gradients (you have autograd from Module 5), (2) add a tokenizer + KV cache to turn the forward pass into real text generation. Or double back to Module 8's modern component upgrades (SwiGLU, GQA, Mamba).

---

## Module 7 Complete — Attention & the modern block
_2026-08-10_

## 🏁 MODULE 7 COMPLETE — Attention & the modern block basics

You just finished a whole module (self-attention → QKV → RoPE → RMSNorm). This is the milestone recap — read only this and you can rebuild the guts of a transformer's core.

### The through-line (how the 4 builds are ONE idea)
A transformer's job at each step: **let every token look at every other token, decide who's relevant, and mix in their information.** These 4 builds ARE that pipeline, in order:
1. **Self-attention** — score relevance with a dot product, softmax it into weights, blend.
2. **QKV** — don't compare tokens raw; first *project* each into a Query (what I'm looking for), Key (what I offer), Value (what I hand over). Scale scores by 1/√d so softmax stays sane.
3. **RoPE** — inject *word order* by rotating Q and K by their position; the score then depends only on the **distance** between tokens.
4. **RMSNorm** — before/after these steps, rescale each vector to a standard size so nothing blows up as layers stack.

Stack that block N times and you have the engine inside GPT.

### Build-by-build recap (each ship + its core mechanism)
- **`attention/`** — self-attention. Core: `weights = softmax([dot(q,k) for k in keys]); out = Σ weights[i]·value[i]`. Bigger dot product = same direction = more relevant. Softmax turns raw scores into weights that sum to 1.
- **`qkv-attention/`** — scaled dot-product attention. Core: `score = (Q·K)/√d → softmax → Σ w·V`. Q, K, V come from **learned** weight matrices (`project(vec, W)`). The `/√d` keeps big-dimension dot products from making softmax spiky (one weight ≈ 1, rest ≈ 0).
- **`rope/`** — rotary positions. Core: `rotate(vec, pos·θ)` on both Q and K, then dot. Because rotating both and dotting cancels the absolute angles, `score(i,j)` depends only on `i − j` (the **distance**). Query rotates by ITS OWN position `i`, Key by `j`.
- **`rmsnorm/`** — root-mean-square normalization. Core: `rms(x)=√(mean(xᵢ²)); out = x / rms(x)`. Rescales any vector so its RMS ≈ 1 — a standard "loudness" — keeping values stable as the block repeats.

### Key formulas — all in one place
```
attention  : out = Σ softmax(scores)ᵢ · valueᵢ
score      : scoreᵢ = q · kᵢ
scaled     : score = (Q · K) / √d
Q,K,V      : Q = Wq·x,  K = Wk·x,  V = Wv·x     (Wq,Wk,Wv are learned)
RoPE       : score(i,j) = rotate(q, i·θ) · rotate(k, j·θ)   → depends on (i − j)
rotate     : [x·cosθ − y·sinθ,  x·sinθ + y·cosθ]
RMSNorm    : out = x / √(mean(xᵢ²))
```

### The big gotchas across this module
- **Softmax holds the weights, not the raw scores.** Raw scores are just relevance; softmax converts them into the actual mixing weights (positive, sum to 1).
- **Scale by 1/√d, not 1/d.** Standard deviation of a d-dim dot product grows like √d, so you divide by √d to undo it. Forgetting it → over-spiky softmax → the model can only look at one token.
- **RoPE: Query uses ITS OWN position.** Writing `rotate(q, j·θ)` (Key's position) collapses every score to the same value — the classic bug you hit. Q gets `i`, K gets `j`.
- **RoPE encodes distance, not absolute spot.** Two tokens 2 apart score the same whether they're at (5,3) or (2,0). That's the feature, not a bug.
- **RMSNorm divides by RMS, not by the max or the sum.** RMS is the "typical size"; dividing by it makes the typical size 1.

### How it all assembles (the payoff)
One transformer block ≈ **RMSNorm → QKV attention (with RoPE positions) → add back → RMSNorm → a small MLP → add back.** Notice the pieces you now own: attention (Module 7), the MLP (Module 5's neuron→layer→MLP), gradients to train it (Module 5's autograd), Adam to optimize it (Module 6). You are genuinely most of the way to hand-building a mini-GPT block — the remaining glue is the residual "add back" and stacking.

### Coverage now
**19% of the course · 2 of 20 modules complete (Modules 5 & 7 at 100%).** Foundations M1–M3, M6 are partially covered from earlier builds. **Next up: Module 8** — assemble these parts into a full transformer block (residual connections + stacking), the first thing that looks like a real model.

---

## RMSNorm
_2026-08-10_

**📝 Revision — RMSNorm**

**Why it matters:** as vectors flow through many layers their magnitude drifts (explodes or vanishes), wrecking training. **Normalization** keeps them at a stable size. RMSNorm is the simple, modern version used in Llama & most current transformers. *(Completes Module 7.)*

**What you built + the core mechanism:**
```python
def rms(vec):                       # root-mean-square = "size" of the vector
    return sqrt(sum(x*x for x in vec) / len(vec))
def rmsnorm(vec):
    r = rms(vec)
    return [x / r for x in vec]     # divide every element by the RMS -> new RMS ~ 1
```

**The concept chain (with examples):**
- **A vector's "size" = its RMS** — square each number, average, square-root. Ex: `RMS([3,4]) = √(25/2) ≈ 3.54`.
- **RMSNorm divides every element by the RMS** — this shrinks the whole vector by factor `r`, and its RMS shrinks by the same factor → **new RMS = r/r = 1**. Ex: `[3,4]` → `[0.85, 1.13]`, RMS `1.0`.
- Result: every vector comes out at a **standard size**, regardless of how big/small it started → stable numbers deep in the network.

**Key rule:** `rmsnorm(x) = x / rms(x)`, where `rms(x) = √(mean(x²))`. (Real RMSNorm also multiplies by a learned per-dim gain.)

**Gotchas:** RMS uses the **mean** of squares (÷ length), then a square root; dividing by it forces the output RMS to exactly 1.

**The payoff:** normalization is what makes deep networks trainable at all. RMSNorm + your RoPE + your QKV attention = the core of a modern transformer block.

**Where it sits + next:** **Module 7 COMPLETE** ✅ (attention + RoPE + RMSNorm). Next → multi-head attention, then assemble the full **transformer block** (attention + RMSNorm + MLP + residual) → then a working GPT.

---

## RoPE — rotary positions
_2026-08-10_

**📝 Revision — RoPE (rotary positional embeddings)**

**Why it matters:** plain attention is **order-blind** — it can't tell "dog bites man" from "man bites dog." RoPE injects word *order/position*, and it's what Llama, GPT-NeoX and most modern LLMs use. *(Module 7.)*

**What you built + the core mechanism:**
```python
def rotate(vec, angle):                 # spin a 2D vector
    x, y = vec
    return [x*cos(angle) - y*sin(angle), x*sin(angle) + y*cos(angle)]
score(i, j) = dot(rotate(q, i*theta), rotate(k, j*theta))   # depends only on (i - j)
```

**The concept chain (with examples):**
- **Attention ignores order** — reorder the items, same result. Bad for language.
- **RoPE rotates Q and K by position × θ** — position 0 → no spin; position p → `p·θ` (like a clock hand turning more each step).
- **Dot of rotated vectors depends on the angle *between* them** = `(i−j)·θ`. So the score depends only on the **distance** `i−j`. Ex: `(q@5,k@3)` = `(q@2,k@0)` = `−0.4161` (both distance 2).

**Key rules:** rotate the Query by **`i·θ`** (its own position `i`), the Key by **`j·θ`**; score depends on **`i − j`**; `rotate([x,y],a) = [x cos a − y sin a, x sin a + y cos a]`.

**Gotchas / what to watch:**
- The Query rotates by **`i`** (its own position), the Key by **`j`** — don't mix `i`/`j` (using `j` for both makes every score 1.0).
- Position 0 = no rotation. (Real RoPE rotates many 2D sub-pairs across the full vector; here it was one 2D pair.)

**The payoff:** relative position **for free**, and it generalizes to longer sequences than seen in training. Universal in modern transformers.

**Where it sits + next:** Module 7 → **RMSNorm** is the final piece to complete the module. Then multi-head attention + the full transformer block.

---

## QKV attention (scaled dot-product)
_2026-08-10_

**📝 Revision — QKV attention (scaled dot-product)**

**Why it matters:** this is the *actual* attention inside every transformer — the real mechanism GPT uses, upgrading basic self-attention with learned Query/Key/Value projections and `√d` scaling. *(Module 7 — Attention & modern block basics.)*

**What you built + the core mechanism:**
```python
q  = project(item0, Wq)                    # this item's Query
K  = [project(it, Wk) for it in items]     # every item's Key
V  = [project(it, Wv) for it in items]     # every item's Value
scores  = [dot(q, k) / sqrt(d) for k in K] # score, scaled
weights = softmax(scores)
out     = Σ weights[j] * V[j]              # blend the Values
```

**The concept chain (with examples):**
- **Q / K / V roles** — Query = what an item *seeks*; Key = what it *advertises*; Value = what it *delivers*. (Library: your request / each book's label / each book's content.)
- **Made via learned weight matrices** `Wq, Wk, Wv` — `project(item, W)` = the item through a matrix = **a stack of dot products** (learned weights, but the operation is your dot product).
- **Scale by `1/√d`** — `score = Q·K ÷ √d`. Ex: `d=16` → divide by 4. *Why:* big `d` → big dot products → softmax gets too spiky; the scale keeps it balanced.
- **softmax → weighted sum of the Values** — the blend uses the Values (not the Keys).

**Key formulas / rules:**
- `attention = softmax( (Q·Kᵀ) / √d ) · V`.
- three separate **learned** projections (Wq, Wk, Wv); weights sum to 1; blend the **Values**.

**Gotchas / what to watch:**
- Blend the **Values**, not the Keys or raw items.
- Scale by **√d** (d = vector length) — forgetting it makes softmax spiky and training unstable.
- `project` is built from the **dot product** (the weights being learned is separate from the operation).

**The payoff:** this exact formula — with **many heads** in parallel and **stacked layers** — *is* the transformer. GPT runs this billions of times per forward pass. You built the real thing.

**Where it sits + next:** Module 7. To **complete** the module: **RoPE** (rotary positions — how the model knows word *order*) + **RMSNorm** (a normalization). Then multi-head attention, then the full transformer block.

---

## self-attention from scratch
_2026-08-10_

**📝 Revision — self-attention from scratch**

**Why it matters:** attention is **THE** core mechanism of the transformer — and therefore of GPT and nearly every modern AI model. Everything else in a transformer is scaffolding around this one idea. *(Phase 5 — Sequence & the Transformer.)*

**What you built + the core mechanism:** for a query and a set of items, produce a **relevance-weighted blend** of the items.
```python
scores  = [dot(query, item) for item in items]   # relevance of each item to the query
weights = softmax(scores)                         # turn scores into weights that sum to 1
out     = sum(weights[i] * items[i])              # blend the items, weighted by attention
```

**The concept chain (with examples):**
- **Attention = focus on relevant items, not all equally.** Ex: in *"…the animal… because **it** was tired,"* "it" attends most to "animal."
- **Relevance = similarity = the dot product.** Bigger dot product = vectors point the same way = more relevant. Ex: `[1,0]·[1,0]=1` (aligned), `[1,0]·[0,1]=0` (perpendicular).
- **Scores → weights via softmax** (your own shipped code) — positive, summing to 1. Ex: `softmax([1,0]) ≈ [0.73, 0.27]`.
- **Output = weighted sum of the items** using those weights. 100% weight on one item → output *is* that item; otherwise a blend. Ex: weights `[0.44, 0.16, 0.40]` on 3 items → `[0.798, 0.202]`.

**Key rules:**
- `attention(query, items)` = `weighted_sum(items, softmax([dot(query, item) for item in items]))`.
- attention weights **always sum to 1**; the **softmax output** (not the raw scores) does the blending.

**Gotchas / what to watch:**
- The blend uses the **softmax weights**, not the raw scores (scores are just softmax's input).
- Each item is turned into a **vector** first — you can't dot-product raw words.
- (This version used items as their own keys/values — the full version adds learned Q/K/V projections + a `1/√d` scale.)

**The payoff:** this is the beating heart of GPT. Every token attends to every other token, blending in what's relevant — that's how a model "uses context." Scale it up, add learned projections and many heads, and you have a transformer.

**Where it sits + next:** Phase 5 — a **major milestone**. Next → add learned **Query/Key/Value** weight matrices + the `1/√d` scaling (full scaled dot-product attention), then **multi-head** attention, then assemble attention + an MLP into a **transformer block**.

---

## an MLP that learns XOR
_2026-08-10_

**📝 Revision — an MLP that learns XOR**

**Why it matters:** an MLP (multi-layer perceptron) is a *real* neural network — layers of neurons stacked. It can learn things a single neuron provably cannot. This is the leap from "one unit" to "a network," and it's the shape underneath deep learning. *(Phase 4 — Deep Learning.)*

**What you built + the core mechanism:** a **2-2-1** network (2 inputs → 2 hidden neurons → 1 output neuron), trained on the 4 XOR examples until it solved them.
```python
def forward(x1, x2):
    inp = [Value(x1), Value(x2)]
    hA = neuron(inp, a_w, a_b)          # hidden neuron A
    hB = neuron(inp, b_w, b_b)          # hidden neuron B
    return neuron([hA, hB], o_w, o_b)   # output neuron reads the hidden outputs
# train: sum loss over the 4 examples → backward → step all 9 knobs (p.data -= lr*p.grad)
```

**The concept chain (with examples):**
- **XOR** = "exclusive or": output 1 when the two inputs **differ**, 0 when they **agree**. Ex: `(1,1)` → agree → 0; `(0,1)` → differ → 1. (Like a hallway light with two switches.)
- **Why one neuron can't** — a neuron draws **one straight fence** and calls one side 1, the other 0. XOR's corners **alternate** (🔴🔵🔴🔵 around the square), and one straight fence can't separate alternating corners. *Contrast:* OR is 🔴🔴🔴🔵 (one corner off) → one fence works.
- **Stacking fixes it** — layer 1's neurons each draw a fence (a feature); layer 2 **combines** them into a bent boundary. 2 hidden neurons → 2 fences → XOR solvable.
- **Lists + loops (Python)** — a `list` is a row of things, positions start at **0** (`[10,20,30][2]` = 30). A `for` loop repeats over each item. `range(n)` gives `0..n-1` (**n** passes — off-by-one: `range(5)` stops before 5).
- **A neuron as a function** — `def neuron(inputs, weights, bias):` sums `weights[i]*inputs[i]` in a loop, adds bias, returns `.tanh()`. One line makes a neuron.
- **Stacking = feeding forward** — the hidden outputs `[hA, hB]` become the **inputs** to the output neuron. One `total.backward()` sends gradients to **all 9 knobs**; each steps by `p.data -= lr*p.grad`.

**Key formulas / rules:**
- MLP output = `outNeuron( [ hiddenA, hiddenB ] )`, where each hidden = `tanh(weighted sum + bias)`.
- update, per knob: **`p.data = p.data − lr * p.grad`** (old value = `p.data`, gradient = `p.grad`).

**Gotchas / what to watch:**
- **XOR + `tanh` wants targets `−1/+1`, not `0/1`** — with `0/1` it got stuck at loss ~0.64; `−1/+1` (matching tanh's range) dropped it to ~0.
- `range(n)` runs **n** times at positions `0..n-1` (not `1..n`).
- **"old" isn't a variable** — in the update it means the knob's *current* value, `p.data`.
- Reset every knob's `.grad` to 0 each step before `backward()`.

**The payoff:** this is a genuine neural network. Make the layers bigger and stack more of them and the same code learns images, language, anything. GPT is this idea, scaled to billions of knobs. You built the real thing.

**Where it sits + next:** Phase 4 (Deep Learning) — this is a milestone. Next → either refactor into clean reusable `Layer`/`MLP` pieces (more Python), train on a richer dataset, or start toward the **transformer** path (attention).

---

## a layer of neurons
_2026-08-08_

**📝 Revision — a layer of neurons**

**Why it matters:** a layer is the next building block up from a single neuron — and a neural *network* is just layers stacked. Every "dense"/"linear" layer, including the ones inside GPT, has this shape. *(Phase 4 — Deep Learning.)*

**What you built + the core mechanism:** 2 neurons side by side, both reading the same inputs, each producing its own output.
```python
out_a = (a_w1*x1 + a_w2*x2 + a_b).tanh()
out_b = (b_w1*x1 + b_w2*x2 + b_b).tanh()   # same shape, its OWN knobs
```

**The concept chain (with examples):**
- **A layer = several neurons side by side.** *Ex:* 4 neurons → 4 outputs. *Why:* each neuron can learn to detect a different feature of the input.
- **Shared inputs, separate knobs.** Every neuron reads the same `x`s, but has its own weights + bias → its own output. *Ex:* shared inputs `(2,3)` → neuron A = `tanh(0.5·2 − 1·3 + 0) = tanh(−2) = −0.964`; neuron B = `tanh(1·2 + 0.5·3 − 1) = tanh(2.5) = 0.987`.
- **Inside each neuron is unchanged** — weighted sum + bias + `tanh`, exactly what you already built.

**Key rules:**
- a layer's output = **the list of its neurons' outputs**; **N neurons → N outputs**.
- neurons **share inputs** but **not knobs** — each has its own weights + bias.

**Gotchas / what to watch:**
- Don't let the neurons share weights — each needs its **own** `w`s and `b` (that's why they give different outputs).
- This build was **forward-only** (no training yet) — training a layer is the same per-knob gradient descent, just with more knobs.

**The payoff:** a layer turns your raw inputs into several **features**. Stack layers (each feeding the next) and the network can learn genuinely complex, nonlinear patterns. You've built the horizontal piece; stacking is the vertical piece.

**Where it sits + next:** Phase 4. Next → **train** the layer, then **stack two layers into an MLP** that learns a nonlinear function like XOR — a real neural network. (And a gentle Python step: a list + loop so you're not copy-pasting neurons.)

---

## a real neuron (weighted sum + bias + tanh)
_2026-08-08_

**📝 Revision — a real neuron (weighted sum + bias + tanh)**

**Why it matters:** a neuron is the fundamental building block of *every* neural network — stack and layer them and you get everything from image classifiers to GPT. You've now built one from scratch and trained it. *(Curriculum: Phase 4 — Deep Learning.)*

**What you built + the core mechanism:** a single neuron — 2 inputs, 2 weights, a bias, a `tanh` squish — that learns by gradient descent on your micrograd engine.
```python
s   = w1*x1 + w2*x2 + b     # weighted sum + bias
out = s.tanh()              # squish into (-1, 1)
loss = (out - target)**2    # wrongness
loss.backward()             # micrograd fills each knob's gradient
# then step each knob:  knob.data -= lr * knob.grad
```

**The concept chain (each with an example):**
- **Weighted sum + bias** — each input × its own weight, summed, plus a baseline. *Ex:* inputs `[1,4]`, weights `[2,3]`, bias `1` → `1·2 + 4·3 + 1 = 15`. *Why:* lets the neuron weigh inputs differently.
- **The bias** — one extra number added at the end; a learnable baseline. *Ex:* inputs both `0`, bias `2` → sum is `2` (without a bias, zero inputs force the output to 0). *Why:* frees the neuron to output non-zero even at zero input — like a line's y-intercept / a fixed cost.
- **`tanh` squish** — bends the raw sum into `(−1, +1)`; big positive → ~`+1`. *Why:* without a nonlinearity, any stack of neurons is still just a straight line; `tanh` lets networks bend and learn curves.
- **Knobs = weights + bias** — every adjustable number. 2 weights + 1 bias = **3 knobs**. *Why:* these are exactly what the neuron learns.
- **Learning = per-knob gradient descent** — each knob steps opposite *its own* gradient every step: `knob = knob − lr·knob.grad`. 3 knobs → 3 gradients → 3 updates. *Why:* each knob independently moves to lower the loss.

**Key formulas / rules:**
- neuron output = **`tanh(w1·x1 + w2·x2 + b)`**
- per-knob update = **`knob − (lr × knob.gradient)`**, for every knob
- `tanh`'s local slope = **`1 − tanh(x)²`** (the new op's derivative)

**Gotchas / what to watch:**
- **The bias is a knob** — it gets a gradient and an update just like the weights (easy to forget).
- **Reset every knob's `.grad` to 0 before `backward()`** each step — gradients accumulate otherwise.
- Without the `tanh`, a neuron can only fit straight lines.

**The payoff:** this is *the* unit of deep learning. A "layer" is just many neurons side by side; a network is layers stacked. GPT is millions of these with the same math. You now hold the atom.

**Where it sits + next:** Phase 4 (Deep Learning). Next → stack a few neurons into a **layer**, then layers into an **MLP** (multi-layer perceptron) that learns a nonlinear dataset — a real little neural network.

---

## a tiny net that learns (gradient descent)
_2026-08-08_

**📝 Revision — a tiny net that learns (gradient descent)**

**Why it matters:** this is how *every* neural network trains — a model adjusts its weights to shrink a loss, step by step, using gradients. You just ran the real training loop; GPT's is the same loop, scaled up.

**Built:** a one-weight "net" that learns `w*3 = 6` → `w = 2` by gradient descent on your micrograd engine. Loss dropped `9 → 0` in a few steps. Shipped ✅

**The bricks (what + why):**
- **Learning = turn a knob (weight) to reduce wrongness.** *Why:* a model *is* its weights; learning = adjusting them.
- **Which way = opposite the gradient** (slope of loss w.r.t. the weight). *Why:* the gradient points uphill in loss; you go downhill.
- **How far = − learning_rate × gradient** (a small step). *Why:* big steps overshoot; small steps converge.
- **Loss = (guess − target)².** *Why:* always positive, punishes big misses, and is smooth to minimize.
- **The loop:** guess → loss → `backward()` (gradient) → step `w` → repeat. *Why:* repeating drives loss to ~0.

**Remember:** **new w = old w − (learning_rate × gradient)**, repeated in a loop. That one line, looped, *is* training.

**The payoff:** this exact loop trains every model, including GPT — just with millions of weights instead of one. You've built and run it end to end.

**Your gap → next:** a real neuron (multiple inputs + a bias + a nonlinearity like `tanh`), then stack a few into an actual multi-layer net.

---

## micrograd — autograd from scratch
_2026-08-07_

**📝 Revision — micrograd (autograd from scratch)**

**Why it matters:** automatic differentiation (autograd) is how *every* neural network learns — it computes the slope of the output with respect to each input, then nudges the inputs to improve. Build it once from scratch and you understand the engine under PyTorch and all of deep learning.

**Built:** a working `Value` autograd engine — a box that holds a number, records its operations, and computes gradients by backprop. Gradients match a numeric check (`a→4, b→3, c→1`, your hand-math). Shipped ✅

**The bricks (what + why):**
- **Gradient = slope:** how much the output moves when you nudge an input a hair. *Why:* it's the signal telling a network which way to adjust.
- **Chain rule:** slopes multiply along a path (`x→y→z`: slope = slope(z←y) × slope(y←x)). *Why:* lets an effect flow through many operations.
- **Local slopes:** `add` passes the slope through ×1 to each input; `multiply` gives each input the OTHER input's value. *Why:* these two rules + the chain rule literally *are* backprop.
- **The graph:** each `Value` remembers its parents + a "note" for how to pass its slope back. *Why:* so we can walk backward automatically.
- **`backward()`:** walk from the output back to the inputs, running each note. *Why:* the chain rule, automated — fills every input's `.grad`.

**Remember:** a gradient is a slope; **add → 1, multiply → the other value**, and **slopes multiply along the chain**. `backward()` walks the graph applying these.

**The payoff:** this exact machinery, scaled up, is how GPT and every model trains. You understand the engine now, not just the API.

**Your gap → next:** closures (a function that remembers its inputs) are the next gentle Python step — then a tiny neural net that actually *learns* using this engine.

---

## the cost of a matrix multiply
_2026-08-07_

**📝 Revision — the cost of a matrix multiply**

**Why it matters:** an AI model like GPT is mostly a giant pile of matrix multiplications; cost out one and you can reason about any model's speed, memory, and price. Bedrock skill.

**Built:** `flops.py` — estimates a matmul's operations, its memory traffic, and whether it's compute- or memory-bound (shipped ✅)

**The bricks (what + why):**
- Work = counting operations (adds & multiplies). *Why:* the hardware does these one at a time, so the count estimates effort.
- Dot product ≈ 2K ops: multiply K pairs + add them. *Why:* the single move underneath all of it.
- Matmul = many dot products; each answer cell = row-from-left · column-from-top, where they cross. *Why:* that's the definition, arranged so "what to multiply where" is automatic.
- Total math = (M×N cells) × 2K = **2·M·N·K**. *Why:* cost = cells × cost-per-cell.
- Memory = (M·K + K·N + M·N) numbers moved × bytes each. *Why:* moving data is a separate bottleneck from doing math.
- Compute- vs memory-bound = math-per-byte vs the machine's ratio. *Why:* a task is capped by its slower resource (chopping vs delivery).

**Remember:** a matmul costs **2·M·N·K** operations and moves **(M·K + K·N + M·N)·bytes**; it's **memory-bound** when it does little math per byte (e.g. generating one token at a time).

**The payoff:** decoding one token at a time makes M=1 → almost no math per byte → LLM generation is limited by memory bandwidth, not compute.

**Your gap → next:** Python syntax/indentation is still shaky → next ship is a tiny pure-Python warmup.

