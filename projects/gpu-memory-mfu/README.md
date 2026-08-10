# GPU memory hierarchy & MFU

**Goal:** understand why GPU speed is governed by data movement, not math.

**Arithmetic intensity** = math ops / numbers moved. Below the machine ridge point (peak FLOPs / memory bandwidth, ~600 here) you are MEMORY-bound; above it, COMPUTE-bound.

**MFU** = achieved FLOPs/s / peak FLOPs/s. Real training runs hit 35-50%.

**Result:** vector add AI 0.33 (memory-bound), matmul N=300 AI 200 (still memory-bound!), matmul N=1500 AI 1000 (compute-bound). Run: `python3 gpu.py` -> PASS.

Module 11 skill `gpu-memory-hierarchy`.
