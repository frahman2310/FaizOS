# Research method — seeds, ablations, compute-matched baselines

Three checks that decide whether a result is REAL. This is the module that separates people who report results from people whose results are true.

**1. Seeds.** Identical code, different seed, different number. Baseline runs [71.2, 68.9, 70.4] -> mean 70.2, spread 2.3. A "new best" of 70.9 is a 0.7 gain against 2.3 of noise: **you have measured nothing**. Never report a single run; report mean +/- spread over >=3 seeds and only claim gains that clear the spread.

**2. Compute-matched baselines.** Method at 10h scores 74.0; baseline at 5h scores 70.2 -> looks like +3.8. Give the baseline the SAME 10h and it scores 73.5 -> the real gain is **+0.5**, which is inside the noise. This is the most common way results mislead, including in good-faith papers.

**3. Ablations.** Three changes, +4 points — which one did it? Remove one at a time: new loss costs 0.2, new schedule costs 0.4, extra data costs **3.7**. The paper would have been called "our novel loss". The data did the work.

Run: `python3 research.py` -> PASS. Module 20 skill `research-method`.

See also [`CAPSTONE.md`](../../CAPSTONE.md) — an honest audit of all 43 builds against the 8-rung portfolio.
