"""FSDP / ZeRO — shard the whole training state (FaizOS build) — Module 13.

Training memory is far bigger than the weights. Per parameter, with Adam in mixed precision:
    weight 2 + grad 2 + fp32 master 4 + adam m 4 + adam v 4 = 16 bytes
ZeRO shards those components across GPUs in stages; ZeRO-3 (FSDP) shards everything.
The price is communication: all-gather the weights to compute, reduce-scatter the gradients.
Fill the ONE blank, then run:  python3 fsdp.py
"""

BYTES = {"weight": 2, "grad": 2, "master_fp32": 4, "adam_m": 4, "adam_v": 4}   # per parameter

SHARDED = {                       # which components each stage splits across the GPUs
    "DDP":    set(),                                                     # nothing is split
    "ZeRO-1": {"master_fp32", "adam_m", "adam_v"},                        # optimizer states
    "ZeRO-2": {"master_fp32", "adam_m", "adam_v", "grad"},                # + gradients
    "ZeRO-3": {"master_fp32", "adam_m", "adam_v", "grad", "weight"},      # + the weights (FSDP)
}


def bytes_per_param(stage, n_gpus):
    """How many bytes ONE GPU holds per parameter at this stage."""
    total = 0.0
    for name, b in BYTES.items():
        if name in SHARDED[stage]:
            total += b / n_gpus          # sharded: this GPU pays only its share
        else:
            total += b                   # replicated: this GPU keeps the whole thing
    return total


def mem_gb(stage, n_params, n_gpus):
    return bytes_per_param(stage, n_gpus) * n_params / 1e9


def comm_bytes_per_step(stage, n_params):
    """Extra collective traffic per GPU per step, in bytes (2 bytes per param, bf16)."""
    p = 2 * n_params
    if stage == "DDP":
        return 2 * p                     # all-reduce the gradients (~2x the data)
    return 2 * p + 1 * p                 # FSDP: all-gather weights (fwd+bwd) + reduce-scatter grads


if __name__ == "__main__":
    n_params, n_gpus = 1e9, 8
    print(f"{n_params/1e9:.0f}B parameters, {n_gpus:.0f} GPUs, Adam mixed precision\n")
    print(f"  {'stage':<8} {'bytes/param':>12} {'GB/GPU':>9} {'comm GB/step':>14}")
    for stage in ("DDP", "ZeRO-1", "ZeRO-2", "ZeRO-3"):
        print(f"  {stage:<8} {bytes_per_param(stage, n_gpus):>12.2f} "
              f"{mem_gb(stage, n_params, n_gpus):>9.2f} {comm_bytes_per_step(stage, n_params)/1e9:>14.1f}")

    assert bytes_per_param("DDP", 8) == 16, "nothing sharded -> the full 16 bytes"
    assert abs(mem_gb("ZeRO-3", 1e9, 8) - 2.0) < 1e-9, "16 GB over 8 GPUs = 2 GB"
    assert bytes_per_param("ZeRO-1", 8) == 4 + 12 / 8, "weights+grads whole, optimizer split"
    assert mem_gb("ZeRO-3", 1e9, 8) < mem_gb("ZeRO-2", 1e9, 8) < mem_gb("ZeRO-1", 1e9, 8)
    print("\nPASS ✅  ZeRO trades communication for memory; ZeRO-3 (FSDP) shards everything.")
