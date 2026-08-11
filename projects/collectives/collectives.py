"""Collectives — how GPUs combine their work (FaizOS build) — Module 13.

Data-parallel GPUs each compute DIFFERENT gradients, then must all end up with the SAME combined
result. Three operations do the sharing:
  all-reduce     : everyone contributes, everyone gets the whole result
  reduce-scatter : everyone contributes, each keeps only its own piece
  all-gather     : each holds a piece, everyone ends up with all the pieces

And the identity that FSDP is built on:  all-reduce = reduce-scatter + all-gather.
Fill the ONE blank, then run:  python3 collectives.py
"""

def all_reduce(gpus):
    """Every GPU ends up holding the element-wise SUM of all the GPUs' vectors."""
    n = len(gpus[0])
    total = [sum(g[i] for g in gpus) for i in range(n)]
    return [list(total) for _ in gpus]


def reduce_scatter(gpus):
    """Sum across GPUs, but each GPU keeps only its own slice of the summed vector."""
    n_gpus, n = len(gpus), len(gpus[0])
    per = n // n_gpus
    pieces = []
    for rank in range(n_gpus):
        lo, hi = rank * per, (rank + 1) * per
        pieces.append([sum(g[i] for g in gpus) for i in range(lo, hi)])
    return pieces


def all_gather(pieces):
    """Each GPU holds one piece; afterwards every GPU holds all the pieces joined together."""
    whole = [x for piece in pieces for x in piece]
    return [list(whole) for _ in pieces]


def all_reduce_via_pieces(gpus):
    """The FSDP route: reduce-scatter first, then all-gather. Must match all_reduce exactly."""
    pieces = reduce_scatter(gpus)
    return all_gather(pieces)        # spread those pieces to every GPU


def ring_bytes_per_gpu(data_bytes, n_gpus):
    """Ring algorithm: each GPU sends and receives about twice the data, whatever n_gpus is."""
    return 2 * data_bytes * (n_gpus - 1) / n_gpus


def seconds(bytes_moved, bytes_per_sec):
    return bytes_moved / bytes_per_sec


if __name__ == "__main__":
    gpus = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]]
    print("each GPU's gradients:", gpus)
    print("all_reduce            ->", all_reduce(gpus))
    print("reduce_scatter pieces ->", reduce_scatter(gpus))
    print("via pieces            ->", all_reduce_via_pieces(gpus))

    GB = 1e9
    for name, bw in (("NVLink (in node)", 100 * GB), ("Ethernet (across nodes)", 10 * GB)):
        moved = ring_bytes_per_gpu(1 * GB, n_gpus=4)
        print(f"{name:<24} 1 GB all-reduce moves {moved/GB:.2f} GB -> {seconds(moved, bw)*1000:6.1f} ms")

    assert all_reduce(gpus) == all_reduce_via_pieces(gpus), "the identity must hold exactly"
    assert reduce_scatter(gpus) == [[10], [10], [10], [10]], "each GPU keeps one summed element"
    assert abs(ring_bytes_per_gpu(1e9, 4) - 1.5e9) < 1, "2 * 1GB * 3/4 = 1.5 GB"
    print("\nPASS ✅  all-reduce = reduce-scatter + all-gather; the wire speed sets the cost.")
