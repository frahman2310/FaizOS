# FSDP / ZeRO — shard the whole training state

**The hidden cost:** training memory is ~16 bytes per parameter, not 2 — weight 2 + grad 2 + fp32 master 4 + Adam m 4 + Adam v 4. A 1B model needs 16 GB/GPU, 8x the weights.

**ZeRO stages:** ZeRO-1 shards optimizer states (12 B), ZeRO-2 adds gradients, ZeRO-3 (FSDP) adds the weights. 1B params on 8 GPUs: 16 -> 5.5 -> 3.75 -> 2.00 GB/GPU.

**The price:** all-gather weights (forward+backward) + reduce-scatter gradients = ~1.5x DDP communication. 8x memory for 1.5x comms.

Run: `python3 fsdp.py` -> PASS. Module 13 skill `fsdp-run`.
