"""GQA — grouped-query attention (FaizOS build) — Module 8.

The KV cache (your Module 9 build) stores K and V for every token — and for every K/V HEAD.
Many query heads can SHARE fewer K/V heads, shrinking the cache. MHA (K/V=Q heads) -> GQA (a few)
-> MQA (1). Fill the ONE line that decides what the cache scales with, then run: python3 gqa.py
"""

def kv_cache_bytes(seq_len, n_q_heads, n_kv_heads, head_dim, bytes_per_num=2):
    """Bytes to cache K and V for a whole sequence, one transformer layer."""
    # The cache stores K and V (that's the 2), one head_dim-sized vector per token, PER head.
    # Key question: does it scale with the number of QUERY heads or the number of KEY/VALUE heads?
    heads_that_count = n_kv_heads          # TODO: n_q_heads or n_kv_heads ? (which one drives the KV cache)
    return 2 * seq_len * heads_that_count * head_dim * bytes_per_num

if __name__ == "__main__":
    seq_len, n_q, head_dim = 4096, 8, 128        # a long context, 8 query heads
    mb = lambda b: b / (1024 * 1024)

    mha = kv_cache_bytes(seq_len, n_q, n_kv_heads=8, head_dim=head_dim)   # 1 K/V per query head
    gqa = kv_cache_bytes(seq_len, n_q, n_kv_heads=2, head_dim=head_dim)   # 8 query heads share 2 K/V
    mqa = kv_cache_bytes(seq_len, n_q, n_kv_heads=1, head_dim=head_dim)   # all share 1 K/V

    print(f"MHA (8 K/V heads): {mb(mha):6.2f} MB/layer")
    print(f"GQA (2 K/V heads): {mb(gqa):6.2f} MB/layer   -> {mha/gqa:.0f}x smaller")
    print(f"MQA (1 K/V head) : {mb(mqa):6.2f} MB/layer   -> {mha/mqa:.0f}x smaller")
    assert mha / gqa == 4, "GQA with 2 of 8 K/V heads should be 4x smaller"
    assert mha / mqa == 8, "MQA with 1 of 8 K/V heads should be 8x smaller"
    print("PASS ✅  GQA shrinks the KV cache by sharing K/V heads across query heads.")
