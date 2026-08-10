# SSM / Mamba — a running-state token mixer

**Goal:** mix tokens WITHOUT attention, via a state-space recurrence scanned left-to-right.

**Mechanism:** `state = a*state + b*x ; y = c*state`. A fading running memory: `a` = how much past to keep, `b` = how much new input to add, `c` = readout. O(n) time, O(1) memory per step (no growing KV cache).

**Result:** impulse response fades (a=0.9 -> 1,0.9,0.81,...; a=0.99 remembers far longer). Run: `python3 ssm.py` -> PASS.

Module 8 skill `ssm-mamba`. Completes Module 8 (FFN, GQA & state-space models).
