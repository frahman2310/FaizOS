# Triton — a fused softmax kernel

**Goal:** write a GPU kernel that fuses all softmax steps into ONE trip to HBM.

**Model:** a kernel = one recipe. Chaining PyTorch ops = one recipe per step, each walking to HBM and back (2 trips each). Fusing = load once, do every step in SRAM, store once (2 trips total, independent of step count).

**Programs & blocks:** you write the recipe for ONE block; the GPU launches `grid = ceil(n_elements/BLOCK_SIZE)` programs in parallel, each with a `pid` telling it which block is its job. Partial blocks are handled with a `mask`.

**Result:** softmax unfused 10 HBM trips vs fused 2 -> 5x fewer. Run: `python3 triton_softmax.py` -> PASS.

Contains the real Triton kernel as reference (needs an NVIDIA GPU) plus a runnable model. Module 11 skill `triton-basics`.
