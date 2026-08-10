"""Numerically stable softmax + cross-entropy from scratch (no numpy).

The naive definition exp(x_i) / sum(exp(x_j)) overflows for large logits, because
exp(1000) is inf. Subtracting max(x) first is mathematically identical (the constant
cancels top and bottom) but keeps every exp() in a safe range. The same shift underlies
log-sum-exp and a numerically stable cross-entropy.
"""
from math import exp, log


def naive_softmax(xs):
    es = [exp(x) for x in xs]          # exp(1000) -> OverflowError
    s = sum(es)
    return [e / s for e in es]


def softmax(xs):
    m = max(xs)                        # shift by the max: exp(x - m) lands in (0, 1]
    es = [exp(x - m) for x in xs]
    s = sum(es)
    return [e / s for e in es]


def log_sum_exp(xs):
    m = max(xs)
    return m + log(sum(exp(x - m) for x in xs))


def cross_entropy(logits, target):
    """-log p[target], computed stably via log-sum-exp (no explicit softmax)."""
    return log_sum_exp(logits) - logits[target]


def _demo():
    big = [1000.0, 1001.0, 1002.0]

    # 1) the naive version blows up; the stable one does not
    try:
        naive_softmax(big)
        naive_overflowed = False
    except OverflowError:
        naive_overflowed = True
    assert naive_overflowed, "naive softmax should overflow on large logits"

    p = softmax(big)
    assert abs(sum(p) - 1.0) < 1e-12, "softmax must sum to 1"
    assert p[2] > p[1] > p[0], "largest logit should get the largest probability"

    # 2) stable cross-entropy matches -log(softmax[target])
    logits = [2.0, 1.0, 0.1]
    ce = cross_entropy(logits, 0)
    ce_ref = -log(softmax(logits)[0])
    assert abs(ce - ce_ref) < 1e-12, "log-sum-exp CE must match -log softmax"

    print("naive_softmax([1000,1001,1002]) -> OverflowError (as expected)")
    print("stable  softmax([1000,1001,1002]) ->", [round(x, 4) for x in p], "| sum =", round(sum(p), 12))
    print("cross_entropy([2,1,0.1], target=0) ->", round(ce, 6))
    print("ALL ACCEPTANCE CHECKS PASSED")


if __name__ == "__main__":
    _demo()
