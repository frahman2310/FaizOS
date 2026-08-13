"""Foundations sweep (FaizOS build) — backfill for Modules 1-6.

The maths and engineering underneath everything already built. Most of this NAMES what you have
already done:
  SVD/low-rank  -> why LoRA and MLA work        expectation   -> the GRPO baseline
  regression    -> your neuron without the tanh  high-dim geom -> where attention's 1/sqrt(d) comes from
  init scaling  -> the same disease residuals and RMSNorm treat

Fill the FIVE blanks (all return NUMBERS), then run:  python3 foundations.py
"""
from math import sqrt


# --- 1. SVD & low-rank: how much does the top-k keep? --------------------

def energy(singular_values):
    """A matrix's 'energy' is the sum of the SQUARES of its singular values."""
    return sum(s * s for s in singular_values)


def energy_kept(singular_values, k):
    """Keeping the top k pieces gives the best possible rank-k approximation. How much survives?"""
    top = energy(singular_values[:k])        # [:k] takes the first k items (they are sorted biggest first)
    total = energy(singular_values)
    # Returns a NUMBER between 0 and 1: the share of the energy the top k carry.
    return top / total                       # part divided by whole


# --- 2. probability ------------------------------------------------------

def mean(xs):
    return sum(xs) / len(xs)


def variance(xs):
    """Average SQUARED distance from the mean."""
    m = mean(xs)
    squared_distances = [(x - m) ** 2 for x in xs]
    # Returns a NUMBER: the average of those squared distances.
    return sum(squared_distances) / len(squared_distances)   # their average


def covariance(xs, ys):
    """Do the two move together? Positive yes, negative opposite, zero unrelated."""
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / len(xs)


# --- 3. high-dimensional geometry ---------------------------------------

def attention_scale(d):
    """Random d-dimensional dot products have a typical size of about sqrt(d), so divide by it."""
    # Returns a NUMBER: the divisor that brings random scores back to a sane range.
    return sqrt(d)                           # typical size of a random d-dim dot product


# --- 4. regression & the bias-variance tradeoff -------------------------

def fit_line(xs, ys):
    """Least-squares line: your neuron without the tanh."""
    w = covariance(xs, ys) / variance(xs)
    b = mean(ys) - w * mean(xs)
    return w, b


def total_error(bias, var):
    """Classic decomposition: the bias is SQUARED, the variance is not."""
    # Returns a NUMBER: bias squared, plus variance.
    return bias ** 2 + var                   # the bias is SQUARED, the variance is not


# --- 5. complexity, profiling, initialisation ---------------------------

def lookup_checks(n_items, structure):
    """A list must be scanned; a dict hashes straight to the slot."""
    return n_items if structure == "list" else 1


def rank_by_time(profile):
    """What cProfile does: sort functions by cumulative time, biggest first (Amdahl again)."""
    return sorted(profile.items(), key=lambda kv: kv[1], reverse=True)


def init_std(fan_in):
    """Xavier: keep each layer's output scale equal to its input scale."""
    # Returns a NUMBER: one divided by the square root of the incoming connections.
    return 1 / sqrt(fan_in)                  # Xavier: preserve the signal scale per layer


if __name__ == "__main__":
    sv = [10, 6, 2, 1, 0.5]
    print("1. SVD / low-rank")
    for k in (1, 2, 4):
        print(f"   top {k} of {len(sv)} pieces keep {energy_kept(sv, k):.1%} of the energy")
    print("   -> this is exactly why LoRA (low-rank) and MLA (latent compression) work")

    print("\n2. PROBABILITY")
    print(f"   [2,4,6]: mean {mean([2,4,6]):.1f}, variance {variance([2,4,6]):.2f}")
    print(f"   covariance of [1,2,3] with [2,4,6] = {covariance([1,2,3],[2,4,6]):.2f} (they move together)")

    print("\n3. HIGH-DIM GEOMETRY")
    for d in (64, 128):
        print(f"   d={d}: random scores are typically +/-{attention_scale(d):.0f}, so divide by {attention_scale(d):.0f}")

    print("\n4. REGRESSION & BIAS-VARIANCE")
    w, b = fit_line([1, 2, 3], [3, 5, 7])
    print(f"   fitting y=2x+1 through (1,3),(2,5),(3,7) -> w={w:.1f}, b={b:.1f}")
    for bias, var in ((2, 2), (4, 1), (1, 4)):
        print(f"   bias {bias}, variance {var} -> total error {total_error(bias, var):.0f}")

    print("\n5. ENGINEERING")
    print(f"   find 1 of 1,000,000 -> list {lookup_checks(1_000_000,'list'):,} checks, "
          f"dict {lookup_checks(1_000_000,'dict')} check")
    print(f"   profile ranked: {rank_by_time({'attention': 42.0, 'mlp': 11.0, 'norm': 4.0})[0]}")
    print(f"   fan_in 100 -> initial weight std {init_std(100):.2f}")

    assert abs(energy_kept([10,6,2,1,0.5], 2) - 136/141.25) < 1e-9, "top-2 carry 96%"
    assert abs(variance([2,4,6]) - 8/3) < 1e-9
    assert abs(covariance([1,2,3],[2,4,6]) - 4/3) < 1e-9
    assert attention_scale(64) == 8.0, "sqrt(64) = 8 — the 1/sqrt(d) from Module 7"
    assert fit_line([1,2,3],[3,5,7]) == (2.0, 1.0), "recovers y = 2x + 1 exactly"
    assert total_error(2,2) == 6 and total_error(4,1) == 17, "bias is SQUARED, variance is not"
    assert lookup_checks(1_000_000,'list') == 1_000_000 and lookup_checks(1_000_000,'dict') == 1
    assert init_std(100) == 0.1, "1/sqrt(100)"
    print("\nPASS ✅  low-rank, expectation, sqrt(d), the tradeoff, and O(1) — all named at last.")
