"""FlashAttention — tiled attention with online softmax (FaizOS build) — Module 11.

Attention's n x n score matrix is too big for SRAM, so standard attention writes it to HBM and reads
it back: O(n^2) memory and traffic. FlashAttention never builds it. It walks the Keys/Values in TILES,
keeping a RUNNING output — the same running-state pattern as your SSM build.

The catch: softmax needs the max/sum over the WHOLE row, but a tile only shows part of it. So we keep
a running max and running sum, and rescale the accumulator whenever a bigger max shows up.
Fill the ONE blank (the rescale factor), then run:  python3 flash.py
"""
from math import exp, sqrt

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def attention_naive(q, K, V):
    """Reference: build ALL the scores at once (this is the n x n matrix we want to avoid)."""
    d = len(q)
    scores = [dot(q, k) / sqrt(d) for k in K]          # the whole row lives in memory
    m = max(scores)
    e = [exp(s - m) for s in scores]
    total = sum(e)
    return [sum(e[j] * V[j][c] for j in range(len(V))) / total for c in range(len(V[0]))]


def attention_flash(q, K, V, tile=2):
    """Tiled: one block of keys at a time, carrying a running (max, sum, output)."""
    d = len(q)
    m = float("-inf")                 # running max seen so far
    s = 0.0                           # running sum of exp(score - m)
    acc = [0.0] * len(V[0])           # running weighted sum of values

    for start in range(0, len(K), tile):
        K_tile, V_tile = K[start:start + tile], V[start:start + tile]
        scores = [dot(q, k) / sqrt(d) for k in K_tile]     # only THIS tile's scores exist
        m_new = max(m, max(scores))                        # the max including this tile

        # Everything accumulated so far was measured against the OLD max. Bring it onto the new
        # scale before adding this tile. Use exp(), the old max m, and the new max m_new.
        correction = exp(m - m_new)                                  # TODO: the rescale factor

        s *= correction
        acc = [a * correction for a in acc]

        for score, v in zip(scores, V_tile):               # fold in this tile
            p = exp(score - m_new)
            s += p
            acc = [a + p * vi for a, vi in zip(acc, v)]

        m = m_new                                          # carry the running max forward

    return [a / s for a in acc]


def peak_numbers_naive(n):
    return n * n                      # the whole score matrix must exist
def peak_numbers_flash(n, tile=2):
    return tile                       # only one tile of scores is ever alive


if __name__ == "__main__":
    q = [1.0, 0.5]
    K = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1], [0.2, 0.8], [1.5, 0.3], [0.1, 0.1]]
    V = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [9.0, 1.0], [2.0, 3.0]]

    ref = attention_naive(q, K, V)
    fla = attention_flash(q, K, V, tile=2)
    print("naive attention:", [round(v, 6) for v in ref])
    print("flash attention:", [round(v, 6) for v in fla])

    for t in (1, 2, 3, 6):            # any tile size must give the SAME answer
        out = attention_flash(q, K, V, tile=t)
        assert all(abs(a - b) < 1e-9 for a, b in zip(out, ref)), f"tile={t} disagreed"
    print("all tile sizes (1,2,3,6) match the reference exactly ✓")

    for n in (1000, 8000):
        print(f"n={n:5d}  peak score-numbers  naive: {peak_numbers_naive(n):>12,}   flash: {peak_numbers_flash(n):>6,}")

    print("PASS ✅  same math, O(n) memory instead of O(n^2) — tiling + online softmax.")
