# FaizOS — Revision Notebook

> Auto-compiled from every lesson. 11 entries, newest first.

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

