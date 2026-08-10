# GQA — grouped-query attention

**Goal:** shrink the KV cache by letting multiple query heads share fewer key/value heads.

**Spectrum:** MHA (K/V heads = Q heads, biggest cache) -> GQA (a few shared K/V heads) -> MQA (1 K/V head). The KV cache scales with the number of K/V heads, NOT query heads.

**Result:** 8 Q heads — MHA 16 MB/layer, GQA (2 K/V) 4 MB (4x), MQA (1 K/V) 2 MB (8x). Run: `python3 gqa.py` -> PASS.

Module 8 skill `gqa`. Builds on the Module 9 KV cache.
