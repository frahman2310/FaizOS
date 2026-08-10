# BPE tokenizer from scratch

**Goal:** turn text into integer tokens by repeatedly merging the most frequent adjacent pair (Byte-Pair Encoding — how GPT tokenizes).

**Mechanism:** `get_stats` counts adjacent pairs, `merge` replaces the top pair with a new token id, repeat N times. Merges stack (256=aa, 257=aaa, 258=aaab).

**Result:** `"aaabdaaabac"` compresses 11 -> 5 tokens over 3 merges. Run: `python3 bpe.py` -> PASS.

Module 9 skill `tokenizer-bpe`.
