# Fault-tolerant checkpointing — the optimal interval

**The problem:** 1000 GPUs each failing every 10,000 h means a crash every 10 h. One dead GPU kills the whole synchronous job.

**The tradeoff:** checkpoint often -> all your time goes to writing. Checkpoint rarely -> each crash costs a lot of rework (half an interval on average).

**The model:** `overhead = write/T + (T/2)/mtbf`, minimised at `T = sqrt(2 * write * mtbf)` (Young/Daly).

**Result:** write 5 min, crash every 10 h -> optimal interval 77 min, total overhead 12.9% (writing 6.5% ~ rework 6.4%, they balance). Run: `python3 checkpoint.py` -> PASS.

Module 13 skill `fault-tolerant-checkpointing`. Completes Module 13.
