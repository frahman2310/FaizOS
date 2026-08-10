"""GPU memory hierarchy & MFU (FaizOS build) — Module 11.

A GPU computes far faster than it can fetch. So what governs speed is ARITHMETIC INTENSITY:
how much math you do per number moved from HBM (the big slow warehouse) to SRAM (the tiny fast
countertop). Below the machine's ridge point you are MEMORY-BOUND; above it, COMPUTE-BOUND.
Fill the ONE blank, then run:  python3 gpu.py
"""

# --- an H100-ish machine, in round numbers ---
PEAK_FLOPS      = 1_000e12      # math ops per second the chips can do
NUMBERS_PER_SEC = 1.67e12       # numbers per second the memory can deliver (bf16, 2 bytes each)
RIDGE = PEAK_FLOPS / NUMBERS_PER_SEC       # ~600: the break-even math-per-number


def intensity(flops, numbers_moved):
    """How much math you get out of each number you fetched."""
    # Divide the math done by the numbers moved. Higher means each fetched number
    # was reused for more work, which is what keeps the math units busy.
    return flops / numbers_moved                              # TODO: flops divided by numbers_moved


def verdict(ai):
    return "COMPUTE-bound (good, math units busy)" if ai >= RIDGE else "MEMORY-bound (starved, waiting on fetches)"


def mfu(achieved_flops_per_sec):
    """Model FLOPs Utilization: the fraction of peak math throughput you actually reach."""
    return achieved_flops_per_sec / PEAK_FLOPS


if __name__ == "__main__":
    print(f"ridge point: {RIDGE:.0f} math ops per number moved\n")

    # vector add over n elements: read a, read b, write c = 3n numbers; n additions
    n = 100
    ai_add = intensity(flops=n, numbers_moved=3 * n)
    print(f"vector add        AI = {ai_add:8.2f}   {verdict(ai_add)}")

    # matmul N x N: 2*N^3 math, 3*N^2 numbers moved  ->  AI = 2N/3
    for N in (300, 1500):
        ai_mm = intensity(flops=2 * N**3, numbers_moved=3 * N**2)
        print(f"matmul N={N:<5}    AI = {ai_mm:8.2f}   {verdict(ai_mm)}")

    print(f"\ntraining run at 400 TFLOP/s  ->  MFU = {mfu(400e12):.0%}")

    assert abs(ai_add - 1 / 3) < 1e-9, "vector add: 100 math / 300 moved = 0.33"
    assert abs(intensity(2 * 300**3, 3 * 300**2) - 200) < 1e-9, "matmul N=300 -> 2N/3 = 200"
    assert abs(mfu(400e12) - 0.4) < 1e-9, "400/1000 = 40%"
    print("PASS ✅  arithmetic intensity decides memory- vs compute-bound; MFU grades the run.")
