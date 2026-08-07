# FaizOS — Revision Notebook

> Auto-compiled from every lesson. 1 entry, newest first.

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

