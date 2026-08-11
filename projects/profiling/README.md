# Profiling — Amdahl's law & finding the real bottleneck

**Goal:** measure before optimizing, and know what an optimization is actually worth.

**Amdahl:** `speedup = 1 / ((1-fraction) + fraction/speedup)`. Infinite speedup on a 10% part caps at 1.11x; a lazy 2x on an 80% part gives 1.67x. Optimize the BIGGEST share.

**Profiles show two things:** which kernels eat time, and GPU IDLE gaps (CPU could not keep up -> CUDA graphs / remove graph breaks).

**Result:** in a 100ms step, attention is the biggest kernel (42%, 2x -> 1.27x) but 40% is GPU idle (killing it -> 1.67x). The real bug is starvation, not attention. Run: `python3 profile.py` -> PASS.

Module 12 skill `profiling-nsight`.
