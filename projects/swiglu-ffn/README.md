# SwiGLU — a gated FFN upgrade

**Goal:** upgrade the transformer FFN from `W2 @ relu(W1 @ x)` to SwiGLU `W2 @ (swish(W1 @ x) ⊙ (W3 @ x))` — the gated feed-forward used in Llama/PaLM.

**Idea:** two linear branches — a swish-activated GATE (smooth dimmer switches) multiplied element-wise into a CONTENT branch, then projected out. Learned, smooth gating instead of ReLU's hard on/off.

**Result:** keeps negative-input channels alive (SwiGLU -0.238 where ReLU gives 0). Run: `python3 swiglu.py` -> PASS.

Module 8 skill `swiglu`.
