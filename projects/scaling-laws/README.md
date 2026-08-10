# Scaling laws — predict loss + Chinchilla sizing

**Goal:** predict a model's loss from its size (power law) and size it compute-optimally.

**Power law:** `L(N) = A * N^(-alpha)` — loss falls as a power of parameters; straight line on a log-log plot, so you can extrapolate from small models. Diminishing returns (each 100x size = 10x loss cut here).

**Chinchilla:** compute `C ~ 6*N*D`; optimal is ~20 tokens per parameter. 10B params -> 200B tokens.

Run: `python3 scaling.py` -> PASS. Module 10 skill `scaling-laws`.
