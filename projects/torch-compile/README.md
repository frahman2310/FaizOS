# torch.compile & CUDA graphs

**Goal:** get the Triton fusion win automatically, and kill kernel-launch overhead.

**torch.compile:** captures a GRAPH of your ops, then generates fused kernels. Cost scales with the number of GRAPHS, not ops: `trips = 2 * n_graphs`. A GRAPH BREAK (print, .item(), data-dependent branch) splits the graph and fusion cannot cross it.

**CUDA graphs:** every kernel launch costs the CPU ~5us. Record the whole launch sequence once and replay it as ONE launch.

**Result (6 ops):** eager 12 trips; compiled 2; +1 break 4; +2 breaks 6 (compilation bought nothing). Launch overhead 5000us -> 5us (1000x). Run: `python3 compile.py` -> PASS.

Module 12 skill `torch-compile-cuda-graphs`.
