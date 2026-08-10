# Transformer block: residuals + stacking

**Goal:** assemble RMSNorm + self-attention + MLP into one block wired with residual connections, then stack N deep.

**Acceptance:** a 30-block stack keeps the signal alive (RMS stays O(1)); the no-residual version vanishes toward 0. Run: `python3 block.py` → PASS.

Maps to curriculum skill `nanogpt-llama-block` (Module 9: Build a GPT). The one new idea: `out = x + layer(norm(x))` — the residual/skip connection.
