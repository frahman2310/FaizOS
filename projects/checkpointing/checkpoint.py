"""Fault-tolerant checkpointing (FaizOS build) — Module 13.

Thousands of GPUs in lockstep means the cluster fails often, and one dead GPU kills the whole job.
Checkpointing saves the training state so a crash only costs the work done since the last save.
Checkpoint too often and you spend all your time writing; too rarely and each crash is expensive.
Fill the ONE blank, then run:  python3 checkpoint.py
"""
from math import sqrt


def cluster_failure_interval(gpu_mtbf_hours, n_gpus):
    """How often SOME GPU dies: one GPU's lifetime divided by how many are running."""
    return gpu_mtbf_hours / n_gpus


def overhead_fraction(interval_min, write_min, mtbf_min):
    """Share of total time lost to checkpointing + rework, for a given checkpoint interval."""
    writing = write_min / interval_min          # you pause `write_min` out of every `interval_min`
    # A crash loses half an interval on average, and crashes arrive every `mtbf_min`.
    rework = (interval_min / 2) / mtbf_min       # half an interval lost, per crash-interval
    return writing + rework


def optimal_interval(write_min, mtbf_min):
    """The interval where writing and rework balance (the Young/Daly result)."""
    return sqrt(2 * write_min * mtbf_min)


if __name__ == "__main__":
    mtbf_hours = cluster_failure_interval(10_000, n_gpus=1000)
    mtbf_min = mtbf_hours * 60
    write_min = 5.0
    print(f"1000 GPUs, each failing every 10,000 h -> a crash every {mtbf_hours:.0f} h")
    print(f"checkpoint write cost: {write_min:.0f} min\n")

    print(f"  {'interval (min)':>15} {'writing':>9} {'rework':>8} {'total':>8}")
    for t in (5, 20, 77, 240, 600):
        w = write_min / t
        r = overhead_fraction(t, write_min, mtbf_min) - w
        print(f"  {t:>15} {w:>8.1%} {r:>7.1%} {overhead_fraction(t, write_min, mtbf_min):>7.1%}")

    best = optimal_interval(write_min, mtbf_min)
    print(f"\noptimal interval: {best:.0f} min   -> total overhead {overhead_fraction(best, write_min, mtbf_min):.1%}")

    assert cluster_failure_interval(10_000, 1000) == 10, "10,000 h / 1000 GPUs = 10 h"
    assert abs(overhead_fraction(60, 5, 600) - (5 / 60 + 60 / 1200)) < 1e-9
    assert abs(optimal_interval(5, 600) - sqrt(6000)) < 1e-9, "sqrt(2*5*600) ~ 77 min"
    # the optimum really is the minimum: no nearby interval does better
    assert all(overhead_fraction(best, 5, 600) <= overhead_fraction(t, 5, 600) for t in (5, 20, 40, 120, 240, 600))
    print("PASS ✅  balance write cost against rework; ~77 min is the sweet spot here.")
