# LoRA — fine-tune 0.8% of the parameters

**The problem:** full fine-tuning costs 16 bytes/param. A 7B model = 112 GB just for optimizer state.

**The idea:** freeze W. Train only a skinny pair added alongside it: `output = W@x + (B@A)@x`, where B is d x r and A is r x d.

**Shapes:** `B(d x r) @ A(r x d)` -> `d x d`, the same shape as W (inner r cancels). Stores `2*d*r` numbers but produces a `d*d` grid.

**Result (1000x1000 layer):** full = 1,000,000 trainable; LoRA rank 4 = 8,000 (0.80%). 7B model: 112 GB -> 0.1 GB of trainable state.

**The catch:** B@A can only produce LOW-RANK updates — fine, because fine-tuning changes are small and structured. At r = d/2 the saving disappears entirely.

Run: `python3 lora.py` -> PASS. Module 14 skill `peft-lora`.
