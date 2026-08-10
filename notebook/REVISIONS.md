# FaizOS — Revision Notebook

> Auto-compiled from every lesson. 20 entries, newest first.

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

