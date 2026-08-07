"""Matmul FLOP + roofline estimator (ForgeOS build).

Fill in the three functions marked TODO, then run `python3 flops.py`.
When the acceptance checks at the bottom pass, you've shipped.
"""

DTYPE_BYTES = {"fp32": 4, "bf16": 2, "fp16": 2, "fp8": 1}


def matmul_flops(M, N, K):
    """FLOPs for C[M,N] = A[M,K] @ B[K,N].

    Each output element is a dot product of length K: K multiplies + K adds = 2*K FLOPs.
    There are M*N output elements.

    TODO: return the total FLOP count.
    """
    return 2 * M * N * K


def matmul_bytes(M, N, K, dtype_bytes=2):
    """Bytes moved to/from memory: read A (M*K elems) + read B (K*N elems) + write C (M*N elems),
    each element `dtype_bytes` bytes.

    TODO: return the total bytes moved.
    """
    return (M * K + K * N + M * N) * dtype_bytes


def roofline_verdict(M, N, K, dtype_bytes, hw_flops_per_byte):
    """Arithmetic intensity = FLOPs / bytes moved. If that intensity exceeds the machine's
    FLOP:byte ratio, the op is limited by math throughput (compute-bound); otherwise it is
    limited by memory bandwidth (memory-bound).

    TODO: return the string "compute-bound" or "memory-bound".
    """
    intensity = matmul_flops(M, N, K) / matmul_bytes(M, N, K, dtype_bytes)
    if intensity > hw_flops_per_byte:
        return "compute-bound"
    else:
        return "memory-bound"


def _acceptance():
    # 1) FLOPs of a tiny matmul: (2x4) @ (4x3) -> 2 * M * N * K
    assert matmul_flops(2, 3, 4) == 48, f"got {matmul_flops(2, 3, 4)}"
    # 2) a real-ish linear layer: batch 1024, 4096 -> 4096
    assert matmul_flops(1024, 4096, 4096) == 2 * 1024 * 4096 * 4096
    # 3) bytes for that layer in bf16 (2 bytes/elem)
    assert matmul_bytes(1024, 4096, 4096, 2) == (1024 * 4096 + 4096 * 4096 + 1024 * 4096) * 2
    # 4) roofline on an H100-ish machine (~990 TFLOP/s bf16 / ~3.35 TB/s ≈ 295 FLOP/byte):
    #    a big square matmul is compute-bound; a skinny GEMV (M=1, like token-by-token decode)
    #    is memory-bound.
    assert roofline_verdict(4096, 4096, 4096, 2, 295) == "compute-bound"
    assert roofline_verdict(1, 4096, 4096, 2, 295) == "memory-bound"
    print("ALL ACCEPTANCE CHECKS PASSED — ship it 🚢")


if __name__ == "__main__":
    _acceptance()
