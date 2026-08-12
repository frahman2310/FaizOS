"""Quantization — run a model in 4 bits (FaizOS build) — Module 14.

An fp16 weight uses 16 bits (~65,000 possible values). That precision is not needed: round the
weights onto a coarse grid and the model still works. For each small GROUP of weights, store the
group's min and step, and store each weight as WHICH LEVEL it is nearest (a tiny integer).

    step = (max - min) / (levels - 1)
    q    = round((x - min) / step)          # an integer 0 .. levels-1
    back = lo + q * step                    # what you get when you decode

Fill the ONE blank, then run:  python3 quantize.py
"""

def levels_for(bits):
    """How many distinct values fit in this many bits: each bit doubles the count."""
    return 2 ** bits


def quantize_group(weights, bits):
    """Round a group of weights onto a grid of 2**bits levels. Returns the decoded values."""
    lo, hi = min(weights), max(weights)
    n_levels = levels_for(bits)
    step = (hi - lo) / (n_levels - 1)                  # the gap between neighbouring levels
    out = []
    for x in weights:
        q = round((x - lo) / step)                     # which level is x nearest (an integer)
        out.append(lo + q * step)                      # decode: start at lo, climb q steps
    return out


def max_error(weights, bits):
    """The worst any single weight can be off: half a step."""
    lo, hi = min(weights), max(weights)
    return (hi - lo) / (levels_for(bits) - 1) / 2


def model_gb(n_params, bits):
    return n_params * (bits / 8) / 1e9                 # 8 bits make one byte


if __name__ == "__main__":
    group = [-1.0, -0.42, -0.05, 0.31, 0.67, 1.0, 0.12, -0.88]
    print("original :", group)
    for bits in (8, 4, 2):
        got = quantize_group(group, bits)
        worst = max(abs(a - b) for a, b in zip(group, got))
        print(f"{bits:>2}-bit   : {[round(v, 3) for v in got]}")
        print(f"          {levels_for(bits):>3} levels, worst error {worst:.3f} (bound {max_error(group, bits):.3f})")

    print("\n7B model memory:")
    for bits in (16, 8, 4):
        print(f"  {bits:>2}-bit : {model_gb(7e9, bits):>5.1f} GB")

    assert levels_for(4) == 16 and levels_for(8) == 256
    assert abs(model_gb(7e9, 4) - 3.5) < 1e-9, "7e9 * 0.5 bytes = 3.5 GB"
    # decoding must never drift further than half a step from the original
    for bits in (8, 4, 2):
        assert all(abs(a - b) <= max_error(group, bits) + 1e-9
                   for a, b in zip(group, quantize_group(group, bits)))
    # the endpoints survive exactly, whatever the bit width
    assert abs(quantize_group(group, 2)[0] - (-1.0)) < 1e-9, "the group minimum is always exact"
    print("\nPASS ✅  fewer bits, coarser grid, bounded error — 14 GB becomes 3.5 GB.")
