"""Triton: a fused softmax kernel (FaizOS build) — Module 11.

A kernel is one recipe the GPU chef runs. Chaining PyTorch ops means one recipe PER STEP, and every
recipe walks to HBM and back. FUSING puts all the steps between a single load and a single store.

Triton needs an NVIDIA GPU, so REAL_KERNEL below is the reference you'd run on an H100, and the code
under it is a runnable model that (a) counts the HBM trips saved and (b) computes a real fused softmax.
Fill the ONE blank, then run:  python3 triton_softmax.py
"""
from math import exp

REAL_KERNEL = '''
import triton, triton.language as tl

@triton.jit
def softmax_kernel(out_ptr, in_ptr, n_cols, BLOCK_SIZE: tl.constexpr):
    pid  = tl.program_id(0)                     # which row is MY job
    offs = tl.arange(0, BLOCK_SIZE)             # the slots in my block
    mask = offs < n_cols                        # ignore slots past the end of the row

    x = tl.load(in_ptr + pid * n_cols + offs, mask=mask, other=-float("inf"))   # 1. WALK (one trip)

    x = x - tl.max(x, axis=0)                   # 2. CHOP: all five softmax steps happen here,
    e = tl.exp(x)                               #    on the countertop, with no warehouse trips
    y = e / tl.sum(e, axis=0)

    tl.store(out_ptr + pid * n_cols + offs, y, mask=mask)                       # 3. WALK BACK (one trip)

# launch one program per row:  softmax_kernel[(n_rows,)](out, x, n_cols, BLOCK_SIZE=1024)
'''

SOFTMAX_STEPS = 5           # max, subtract, exp, sum, divide


def hbm_trips_unfused(n_steps):
    """Each step is its own kernel: read the data, do one op, write it back."""
    return 2 * n_steps


def hbm_trips_fused(n_steps):
    """One kernel: load once, do every step on the countertop, store once."""
    # The cost is one read plus one write, and it does NOT depend on how many steps you fuse.
    return 2                                     # one read + one write, regardless of n_steps


def grid(n_elements, block_size):
    """How many parallel programs to launch (round UP so a partial block still gets one)."""
    return -(-n_elements // block_size)


def fused_softmax_row(row):
    """What one program computes: load the row, then all five steps before storing."""
    m = max(row)                                 # 1. max
    shifted = [v - m for v in row]               # 2. subtract
    e = [exp(v) for v in shifted]                # 3. exp
    s = sum(e)                                   # 4. sum
    return [v / s for v in e]                    # 5. divide


if __name__ == "__main__":
    print("The kernel you would run on a real GPU:")
    print(REAL_KERNEL)

    un = hbm_trips_unfused(SOFTMAX_STEPS)
    fu = hbm_trips_fused(SOFTMAX_STEPS)
    print(f"softmax HBM trips  unfused: {un}   fused: {fu}   -> {un // fu}x fewer trips")

    print(f"grid for 8192 elements, block 1024: {grid(8192, 1024)} programs")
    print(f"grid for 4096 elements, block  512: {grid(4096, 512)} programs")
    print(f"grid for 5000 elements, block 1024: {grid(5000, 1024)} programs (rounded up, last one masked)")

    out = fused_softmax_row([1.0, 2.0, 3.0])
    print(f"fused softmax([1,2,3]) = {[round(v, 4) for v in out]}  (sums to {round(sum(out), 6)})")

    assert fu == 2, "a fused kernel is one read + one write"
    assert un // fu == 5, "5 steps unfused vs 1 fused -> 5x fewer trips"
    assert grid(8192, 1024) == 8 and grid(4096, 512) == 8
    assert grid(5000, 1024) == 5, "round UP so the leftover elements still get a program"
    assert abs(sum(out) - 1.0) < 1e-9, "softmax must sum to 1"
    print("PASS ✅  fusion: one load, many chops, one store — the core Triton win.")
