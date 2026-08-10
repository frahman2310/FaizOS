# MLA — Multi-head Latent Attention

**Goal:** shrink the KV cache by COMPRESSION (vs GQA's sharing).

**Mechanism:** down-project each token to a small latent `c` (compress), cache ONLY `c`, and up-project to reconstruct K,V on the fly. Works because K/V are low-rank (redundant).

**Result:** latent 2 numbers vs token 4; at scale full K/V 2048 -> latent 64 = 32x smaller. Run: `python3 mla.py` -> PASS.

Module 10 skill `mla`. Completes Module 10 (Scaling, MLA & evaluation).
