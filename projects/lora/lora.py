"""LoRA — Low-Rank Adaptation (FaizOS build) — Module 14.

Full fine-tuning trains every weight: 16 bytes per parameter of memory. LoRA freezes the base weight
matrix W and trains only a skinny pair B (d x r) and A (r x d) added alongside it:

    output = W @ x  +  (B @ A) @ x          W frozen, only A and B learn

B @ A has the same shape as W (d x d), but stores only 2*d*r numbers instead of d*d.
Fill the ONE blank, then run:  python3 lora.py
"""

def matmul(X, Y):
    """Standard matrix multiply: result[i][j] = row i of X dotted with column j of Y."""
    rows, inner, cols = len(X), len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def shape(M):
    return (len(M), len(M[0]))


def full_finetune_params(d):
    """Full fine-tuning trains every entry of the d x d weight matrix."""
    return d * d


def lora_params(d, r):
    """LoRA trains only B (d rows, r columns) and A (r rows, d columns)."""
    # B holds d*r numbers and A holds r*d numbers, and you train BOTH.
    return d * r + r * d                  # B has d*r numbers, A has r*d, and both are trained


def trainable_bytes_gb(n_params):
    return n_params * 16 / 1e9            # 16 bytes per TRAINED parameter (Adam, mixed precision)


if __name__ == "__main__":
    # --- the shape check, small enough to verify by hand ---
    B = [[1, 0], [0, 1], [1, 1]]          # 3 x 2
    A = [[1, 2, 3], [4, 5, 6]]            # 2 x 3
    print(f"B is {shape(B)}, A is {shape(A)}  ->  B@A is {shape(matmul(B, A))}")
    print("B@A =", matmul(B, A))

    # --- the parameter saving on one 1000x1000 layer ---
    d = 1000
    print(f"\none {d}x{d} layer:")
    print(f"  full fine-tune : {full_finetune_params(d):>10,} trainable")
    for r in (1, 4, 16, 64):
        p = lora_params(d, r)
        print(f"  LoRA rank {r:<3}  : {p:>10,} trainable   ({p / full_finetune_params(d):6.2%} of full)")

    # --- what it means for a 7B model ---
    print(f"\n7B model, full fine-tune : {trainable_bytes_gb(7e9):>6.0f} GB")
    print(f"7B model, LoRA (~0.1%)   : {trainable_bytes_gb(7e9 * 0.001):>6.1f} GB  (base weights still loaded, but frozen)")

    assert shape(matmul(B, A)) == (3, 3), "3x2 @ 2x3 -> 3x3: inner dims cancel"
    assert lora_params(1000, 4) == 8000, "4*1000 + 1000*4 = 8000"
    assert lora_params(1000, 4) / full_finetune_params(1000) < 0.01, "under 1% of the weights"
    assert lora_params(1000, 500) == full_finetune_params(1000), "at r = d/2 LoRA stops saving anything"
    print("\nPASS ✅  train 0.8% of the weights; B@A keeps W's shape while storing 2*d*r numbers.")
