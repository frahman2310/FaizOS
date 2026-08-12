# Inference internals — paged KV, continuous batching, speculative decoding

Three tricks, one disease: a wasted GPU.

1. **Paged KV** — reserving max length wastes ~90% (2048 reserved, 200 used -> 1848 wasted). Hand out fixed 16-token PAGES on demand: 13 pages, only 8 tokens wasted.
2. **Continuous batching** — static batching runs until the slowest finishes; lengths [100,100,100,1000] leave 2700 idle slot-steps. Evict finished sequences and admit new ones -> 0.
3. **Speculative decoding** — a small draft model proposes k tokens, the big model verifies all of them in ONE pass. Tokens per pass = `accepted + 1` (the verifier also emits its own). 3 accepted -> 4x. Never worse than 1x, and the output is identical.

Run: `python3 serving.py` -> PASS. Module 14 skill `inference-internals`.
