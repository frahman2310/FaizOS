# FaizOS — Revision Notebook

> Auto-compiled from every lesson. 4 entries, newest first.

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

