"""Pipeline schedules — GPipe vs 1F1B (FaizOS build) — Module 13.

More microbatches shrink the pipeline bubble, but every forward must SAVE its activations until its
backward runs. GPipe does all forwards first, so it holds M sets at peak. 1F1B alternates one
forward with one backward once the pipeline is full, so each backward frees a set as the next
forward takes one — peak holdings level off at the number of STAGES, not microbatches.
Same bubble, far less memory. Fill the ONE blank, then run:  python3 schedules.py
"""

def bubble_fraction(stages, microbatches):
    """Share of pipeline time wasted filling and draining (same for both schedules)."""
    return (stages - 1) / (microbatches + stages - 1)


def peak_activations_gpipe(stages, microbatches):
    """GPipe runs every forward before any backward, so nothing is freed until the end."""
    return microbatches


def peak_activations_1f1b(stages, microbatches):
    """1F1B keeps only the microbatches still IN FLIGHT, and the pipeline has one slot per stage."""
    # A microbatch is in flight from its forward until its backward. The pipeline depth caps how
    # many can be in flight at once, so this does NOT grow with the number of microbatches.
    return stages                     # one slot per stage caps how many are in flight


def activation_gb(sets_held, gb_per_set):
    return sets_held * gb_per_set


if __name__ == "__main__":
    stages, gb_per_set = 4, 1.5
    print(f"{stages} pipeline stages, {gb_per_set} GB of activations per microbatch\n")
    print(f"  {'microbatches':>12} {'bubble':>8} {'GPipe GB':>10} {'1F1B GB':>9}")
    for m in (4, 8, 32, 128):
        g = activation_gb(peak_activations_gpipe(stages, m), gb_per_set)
        f = activation_gb(peak_activations_1f1b(stages, m), gb_per_set)
        print(f"  {m:>12} {bubble_fraction(stages, m):>7.1%} {g:>10.1f} {f:>9.1f}")

    assert peak_activations_gpipe(4, 32) == 32, "GPipe holds one set per microbatch"
    assert peak_activations_1f1b(4, 32) == 4, "1F1B holds one set per stage"
    assert peak_activations_1f1b(8, 64) == 8, "still one per stage, not per microbatch"
    assert bubble_fraction(4, 32) == bubble_fraction(4, 32), "the schedules share the same bubble"
    print("\nPASS ✅  1F1B: same bubble as GPipe, memory capped by depth instead of microbatches.")
