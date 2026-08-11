# Parallelism axes — data, tensor, pipeline

**Goal:** decide how to split a model that does not fit on one GPU.

- **Data parallel** REPLICATES the model, splits the batch -> buys throughput, NOT capacity.
- **Tensor parallel** splits each weight matrix -> shards memory; chatty (every layer), needs fast intra-node links.
- **Pipeline parallel** splits the layers -> shards memory; cheap comms, but BUBBLES.

**Bubble:** `(stages-1)/(microbatches+stages-1)`. 4 stages, 1 microbatch = 75% idle; 32 microbatches = 8.6%.

**Result:** 70B model = 140 GB. Data parallel 140 GB/GPU (does not fit); tensor/pipeline 17.5 GB/GPU on 8 GPUs (fits). Run: `python3 parallel.py` -> PASS.

Module 12 skill `parallelism-axes`. Completes Module 12.
