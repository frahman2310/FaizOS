# Quantization — run a model in 4 bits

**Idea:** fp16 gives ~65,000 values per weight; you do not need that. Per GROUP of weights, store min + step and encode each weight as WHICH LEVEL it is nearest.

```
step = (max - min) / (levels - 1)
q    = round((x - lo) / step)     # encode: an integer 0..levels-1
back = lo + q * step              # decode: start at lo, climb q steps
```

**Bits -> levels:** each bit doubles. 4 bits = 16 levels, 8 bits = 256.

**Error:** bounded by half a step. 8-bit 0.002, 4-bit 0.063, 2-bit 0.330 (collapses - distinct weights merge).

**Memory (7B):** 16-bit 14 GB -> 8-bit 7 GB -> 4-bit 3.5 GB. 4-bit is the practical floor.

Run: `python3 quantize.py` -> PASS. Module 14 skill `quantization`.
