"""Parallelism axes (FaizOS build) — Module 12.

When one GPU is not enough, HOW you split decides whether it works:
  DATA     parallel — every GPU keeps a FULL copy, splits the batch.   Buys throughput, not capacity.
  TENSOR   parallel — split each weight MATRIX across GPUs.            Shards memory; chatty, same node.
  PIPELINE parallel — split the LAYERS across GPUs.                    Shards memory; cheap comms, but bubbles.

Fill the ONE blank, then run:  python3 parallel.py
"""

BYTES_PER_PARAM = 2                 # bf16


def model_gb(n_params):
    return n_params * BYTES_PER_PARAM / 1e9


def mem_per_gpu_data(total_gb, n_gpus):
    """Data parallel REPLICATES: each GPU holds the whole model, however many GPUs you add."""
    return total_gb


def mem_per_gpu_sharded(total_gb, n_gpus):
    """Tensor / pipeline parallel SHARD: the model is divided across the GPUs."""
    # Unlike the data-parallel function above, this one really does divide the model up.
    return total_gb / n_gpus                     # TODO: the model split evenly across the GPUs


def bubble_fraction(stages, microbatches):
    """Share of pipeline time wasted waiting for the line to fill and drain."""
    return (stages - 1) / (microbatches + stages - 1)


if __name__ == "__main__":
    total = model_gb(70e9)
    gpu_gb, n = 80.0, 8
    print(f"model: {total:.0f} GB   |   {n} x {gpu_gb:.0f} GB GPUs\n")

    for name, fn in (("data parallel", mem_per_gpu_data), ("tensor/pipeline parallel", mem_per_gpu_sharded)):
        per = fn(total, n)
        print(f"  {name:<24} {per:6.1f} GB/GPU   {'FITS' if per <= gpu_gb else 'DOES NOT FIT'}")

    print("\npipeline bubble (4 stages) — add microbatches to keep the line full:")
    for m in (1, 2, 8, 32):
        print(f"  {m:>2} microbatch(es): {bubble_fraction(4, m):5.1%} of the cluster idle")

    assert mem_per_gpu_data(total, 8) == total, "data parallel does not reduce per-GPU memory"
    assert abs(mem_per_gpu_sharded(140.0, 8) - 17.5) < 1e-9, "140 GB over 8 GPUs = 17.5 GB"
    assert abs(bubble_fraction(4, 1) - 0.75) < 1e-9, "4 stages, 1 microbatch -> 3 of 4 idle"
    assert bubble_fraction(4, 32) < 0.1, "many microbatches -> small bubble"
    print("\nPASS ✅  data parallel = throughput; tensor/pipeline = capacity; microbatches kill the bubble.")
