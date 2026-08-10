"""MLA — Multi-head Latent Attention (FaizOS build) — Module 10.

Compress each token's Key/Value into a small LATENT vector; cache ONLY the latent; reconstruct K,V
on the fly via an up-projection. Even smaller KV cache than GQA. Fill the ONE blank (reconstruct),
then run: python3 mla.py
"""

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def matvec(W, v):                      # W is a list of rows; output[i] = row_i · v
    return [dot(row, v) for row in W]

def compress(x, W_down):               # x (big) -> latent c (small).  down-projection.
    return matvec(W_down, x)

def reconstruct(c, W_up):              # latent c (small) -> approx K or V (big).  up-projection.
    return matvec(W_up, c)                         # TODO: project the latent back up -> matvec(W_up, c)

# --- KV cache size: full K/V vs MLA latent ---
def full_cache_per_token(n_heads, head_dim):
    return 2 * n_heads * head_dim      # cache K and V for every head
def mla_cache_per_token(d_latent):
    return d_latent                    # cache ONLY the compressed latent

if __name__ == "__main__":
    # mechanism demo: a 4-dim token squeezed to a 2-dim latent, then rebuilt
    x      = [1.0, 2.0, 3.0, 4.0]
    W_down = [[0.5, 0.0, 0.5, 0.0], [0.0, 0.5, 0.0, 0.5]]          # 4 -> 2  (compress)
    W_up   = [[1,0],[0,1],[1,0],[0,1]]                             # 2 -> 4  (reconstruct)
    c      = compress(x, W_down)
    approx = reconstruct(c, W_up)
    print("token x     :", x)
    print("latent c    :", c, " (cached — only", len(c), "numbers)")
    print("reconstructed:", approx)

    # cache size at scale
    full = full_cache_per_token(8, 128)      # 2048
    mla  = mla_cache_per_token(64)           # 64
    print(f"\nfull K/V cache/token: {full}")
    print(f"MLA latent cache/token: {mla}   -> {full // mla}x smaller")

    assert len(c) < len(x), "latent must be smaller than the token"
    assert full // mla == 32, "2048 / 64 = 32x"
    print("PASS ✅  MLA: cache a small latent, reconstruct K/V on the fly — the smallest KV cache.")
