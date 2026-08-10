# KV cache — O(n^2) -> O(n) generation

**Goal:** cache past Keys/Values during autoregressive generation so each new token computes only its OWN K,V.

**Idea:** a past token's K,V never change, so recomputing them every step is waste. Cache them; compute one new entry per step.

**Result:** counting KV computations — no-cache = n(n+1)/2 (O(n^2)), with-cache = n (O(n)). n=100 -> 5050 vs 100 = 50.5x. Run: `python3 kvcache.py` -> PASS.

Module 9 skill `kv-cache`. Completes Module 9 (Build a GPT).
