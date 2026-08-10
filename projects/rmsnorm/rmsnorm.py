"""RMSNorm (FaizOS build). Rescale a vector to a standard size (RMS ~ 1). Fill the blank, then run."""
from math import sqrt


def rms(vec):
    # root-mean-square: square each number, average them, take the square root
    total = 0.0
    for x in vec:
        total = total + x * x
    return sqrt(total / len(vec))


def rmsnorm(vec):
    r = rms(vec)
    out = []
    for x in vec:
        out.append(x / r)          # TODO: divide the element x by the RMS r  ->  x / r
    return out


v = [3.0, 4.0]
out = rmsnorm(v)
print("input     :", v, "  RMS =", round(rms(v), 4))
print("normalized:", [round(o, 4) for o in out], "  RMS =", round(rms(out), 4))
