# FaizOS — Revision Notebook

> Auto-compiled from every lesson. 2 entries, newest first.

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

