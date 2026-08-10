"""Scaling laws (FaizOS build) — Module 10.

Predict a model's loss from its size with a POWER LAW, and size a model compute-optimally
(Chinchilla: ~20 training tokens per parameter). Fill the ONE blank (the power law), then run:
python3 scaling.py
"""

def predicted_loss(N, A=100.0, alpha=0.5):
    """Power law: loss falls as a power of model size N.  L(N) = A * N^(-alpha)."""
    # N ** (-alpha) means N to the power negative alpha, i.e. 1 / N^alpha (a shrinking factor as N grows)
    return A * N ** (-alpha)                          # TODO: A * N ** (-alpha)

def chinchilla_tokens(N):
    return 20 * N                       # ~20 training tokens per parameter (the Chinchilla ratio)

def compute_flops(N, D):
    return 6 * N * D                    # ~6 FLOPs per parameter per token

if __name__ == "__main__":
    print("Predicted loss vs model size (A=100, alpha=0.5):")
    for N in (100, 10_000, 1_000_000):
        print(f"  N={N:>10,}  ->  loss {predicted_loss(N):.4f}")

    N = 10_000_000_000                  # a 10-billion-parameter model
    D = chinchilla_tokens(N)
    print(f"\nChinchilla-optimal for {N:,} params: train on {D:,} tokens")
    print(f"compute needed: {compute_flops(N, D):.2e} FLOPs")

    assert abs(predicted_loss(100) - 10.0) < 1e-9, "100/sqrt(100) = 10"
    assert abs(predicted_loss(10_000) - 1.0) < 1e-9, "100/sqrt(10000) = 1"
    assert chinchilla_tokens(10_000_000_000) == 200_000_000_000, "20 tokens/param"
    print("PASS ✅  scaling law predicts loss; Chinchilla sizes the model compute-optimally.")
