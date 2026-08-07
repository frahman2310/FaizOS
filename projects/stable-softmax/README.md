# Numerically stable softmax

Built in **ForgeOS**. Softmax + cross-entropy from scratch (no numpy), showing why the naive
definition overflows and how the max-subtraction / log-sum-exp trick fixes it.

## Acceptance criteria (verifiable)
- `naive_softmax` **overflows** on large logits (e.g. `[1000, 1001, 1002]`).
- `softmax` returns a valid distribution (**sums to 1**) on the same input.
- stable `cross_entropy` matches `-log(softmax[target])` to `1e-12`.

## Run
```bash
python3 softmax.py
```
