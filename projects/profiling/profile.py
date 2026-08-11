"""Profiling — Amdahl's law & finding the real bottleneck (FaizOS build) — Module 12.

A profiler (Nsight, torch.profiler) tells you two things: which kernels eat the time, and how much
time the GPU spent IDLE. Amdahl's law then tells you what a given optimization is actually worth,
so you spend your week on the right kernel. Fill the ONE blank, then run:  python3 profile.py
"""

def amdahl(fraction, speedup):
    """End-to-end speedup when a part that is `fraction` of the runtime gets `speedup` times faster.

    The optimized part shrinks from `fraction` to `fraction / speedup`; the rest, (1 - fraction),
    is untouched. Total speedup is 1 divided by the new total time.
    """
    new_total_time = (1 - fraction) + fraction / speedup
    return 1 / new_total_time        # shorter new time -> bigger speedup, so it goes on the bottom


def analyze(profile, step_ms):
    """profile: {kernel name: milliseconds}. Ranks kernels and reports GPU idle time."""
    busy = sum(profile.values())
    idle = step_ms - busy
    ranked = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    return ranked, busy, idle


if __name__ == "__main__":
    print("Amdahl's law — what an optimization is really worth:")
    print(f"  make a 10% part INFINITELY faster : {amdahl(0.10, 1e9):.2f}x   (a perfect week, 11%)")
    print(f"  make an 80% part just 2x faster   : {amdahl(0.80, 2):.2f}x   (a lazy win, 67%)")
    print(f"  make an 80% part 10x faster       : {amdahl(0.80, 10):.2f}x")

    step_ms = 100.0
    prof = {"attention": 42.0, "ffn_matmul": 11.0, "layernorm": 4.0, "elementwise": 3.0}
    ranked, busy, idle = analyze(prof, step_ms)

    print(f"\nProfile of a {step_ms:.0f} ms step:")
    for name, ms in ranked:
        print(f"  {name:<14} {ms:5.1f} ms   {ms / step_ms:5.1%} of the step")
    print(f"  {'GPU IDLE':<14} {idle:5.1f} ms   {idle / step_ms:5.1%}  <- CPU could not keep up")

    top_name, top_ms = ranked[0]
    print(f"\nbiggest kernel: {top_name} ({top_ms / step_ms:.0%}) -> 2x on it gives "
          f"{amdahl(top_ms / step_ms, 2):.2f}x end-to-end")
    print(f"killing ALL idle time gives {amdahl(idle / step_ms, 1e9):.2f}x  <- the real headline here")

    assert abs(amdahl(0.10, 1e9) - 1 / 0.9) < 1e-6, "infinite speedup on 10% caps at 1.11x"
    assert abs(amdahl(0.80, 2) - 1 / 0.6) < 1e-9, "2x on 80% -> 1.67x"
    assert abs(amdahl(0.5, 1) - 1.0) < 1e-9, "no speedup -> 1x"
    assert abs(idle - 40.0) < 1e-9, "60 ms of kernels in a 100 ms step -> 40 ms idle"
    print("\nPASS ✅  measure first: the biggest share wins, and idle time is often the real bug.")
