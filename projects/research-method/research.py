"""Research method (FaizOS build) — Module 20.

Three checks that decide whether a result is real:
  1. SEEDS      - identical code, different seed, different number. Report mean +/- spread over >=3
                  runs, and only claim gains that clear the spread.
  2. COMPUTE    - if your method used more compute, give the BASELINE the same budget before comparing.
  3. ABLATIONS  - remove one component at a time to find which one actually caused the gain.

Fill the THREE blanks, then run:  python3 research.py
"""

# --- 1. seeds: is the improvement bigger than the noise? -----------------

def mean(xs):
    return sum(xs) / len(xs)


def spread(xs):
    """A simple, honest spread: how far the runs reach from best to worst."""
    return max(xs) - min(xs)


def is_real_improvement(baseline_runs, new_score):
    """A claim is only real if it beats the baseline by MORE than the baseline's own variation."""
    gain = new_score - mean(baseline_runs)
    noise = spread(baseline_runs)
    # Returns True or False: the gain must be larger than the noise to count.
    return gain > noise                       # only counts if it clears the baseline's own spread


# --- 2. compute-matched baselines ---------------------------------------

def real_gain(method_score, baseline_same_compute):
    """Compare against the baseline given the SAME budget, not the cheap one."""
    # Returns a NUMBER: your score minus the fairly-funded baseline.
    return method_score - baseline_same_compute   # compare against the FAIRLY funded baseline


# --- 3. ablations: which component did the work? -------------------------

def contribution(full_score, score_without):
    """How much a component was worth: what you lose when you remove it."""
    # Returns a NUMBER: the drop caused by removing that one piece.
    return full_score - score_without         # what you lose by removing that piece


def blame(full_score, ablations):
    """ablations: {component: score with that component REMOVED}. Biggest drop = the real cause."""
    scored = {c: contribution(full_score, s) for c, s in ablations.items()}
    return max(scored, key=scored.get), scored


if __name__ == "__main__":
    baseline = [71.2, 68.9, 70.4]
    print("1. SEEDS")
    print(f"   baseline runs {baseline} -> mean {mean(baseline):.1f}, spread {spread(baseline):.1f}")
    for claim in (70.9, 74.5):
        verdict = "REAL" if is_real_improvement(baseline, claim) else "inside the noise"
        print(f"   new score {claim} -> {verdict}")

    print("\n2. COMPUTE-MATCHED BASELINE")
    print(f"   method 10h 74.0 vs baseline 5h 70.2  -> looks like +{74.0-70.2:.1f}")
    print(f"   method 10h 74.0 vs baseline 10h 73.5 -> really  +{real_gain(74.0, 73.5):.1f}")

    print("\n3. ABLATIONS (full system scores 74.0)")
    culprit, scores = blame(74.0, {"new loss": 73.8, "new schedule": 73.6, "extra data": 70.3})
    for comp, worth in scores.items():
        print(f"   removing {comp:<14} costs {worth:>4.1f} points")
    print(f"   -> the real cause was: {culprit}")

    assert abs(spread([71.2, 68.9, 70.4]) - 2.3) < 1e-9, "71.2 - 68.9 = 2.3"
    assert abs(mean(baseline) - 70.166666666666) < 1e-6
    assert is_real_improvement(baseline, 70.9) is False, "0.7 gain vs 2.3 noise: not real"
    assert is_real_improvement(baseline, 74.5) is True, "4.3 gain clears the noise"
    assert abs(real_gain(74.0, 73.5) - 0.5) < 1e-9, "compute-matched, the gain nearly vanishes"
    assert abs(contribution(74.0, 70.3) - 3.7) < 1e-9
    assert blame(74.0, {"new loss": 73.8, "new schedule": 73.6, "extra data": 70.3})[0] == "extra data"
    print("\nPASS ✅  clear the noise, match the compute, and ablate before you claim anything.")
