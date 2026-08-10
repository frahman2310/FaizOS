# Train attention — a learned attention weight

**Goal:** make an attention weight LEARNABLE (not hardcoded) and train it with gradient descent to attend to the relevant token.

**Setup:** two value-tokens (A=1.0, B=5.0), one learnable score `g`, weight `wB = sigmoid(g)` (built from micrograd `tanh`), output = blend, loss = (output-5)^2.

**Result:** loss 4.0 -> 0.002, wB 0.5 -> 0.99, output 3.0 -> 4.96. The model learned to attend to token B. Run: `python3 train.py` -> PASS.

Reuses the micrograd `Value` engine (Module 5). Training loop: forward -> loss -> backward -> update.
