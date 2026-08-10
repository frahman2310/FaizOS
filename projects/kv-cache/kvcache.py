"""KV cache (FaizOS build) — Module 9.

A GPT generates one token at a time; each new token's attention needs the Key & Value of every
past token. Naively you recompute ALL past K,V each step  -> O(n^2). But past K,V never change,
so cache them and compute only the NEW token's K,V each step -> O(n).

Fill the ONE blank (compute the new token's K,V and add it to the cache), then run: python3 kvcache.py
"""

def compute_kv(token):
    """Pretend this is the expensive projection of a token into its (Key, Value). We count the calls."""
    compute_kv.calls += 1
    return (f"K{token}", f"V{token}")
compute_kv.calls = 0

def generate_no_cache(n):
    """Naive: at every step, recompute K,V for EVERY token seen so far."""
    compute_kv.calls = 0
    for step in range(n):                       # producing token number `step`
        kv_all = [compute_kv(t) for t in range(step + 1)]   # recompute tokens 0..step  <- wasteful
    return compute_kv.calls

def generate_with_cache(n):
    """Cached: compute only the NEW token's K,V each step; reuse the rest from the cache."""
    compute_kv.calls = 0
    cache = []
    for step in range(n):                       # producing token number `step`
        cache.append(compute_kv(step))                    # compute K,V for ONLY the new token, reuse the rest from cache
        # attention would now read the whole `cache` (all past K,V) — but we only COMPUTED one new entry
    return compute_kv.calls

if __name__ == "__main__":
    for n in (5, 10, 100):
        no = generate_no_cache(n)
        yes = generate_with_cache(n)
        print(f"n={n:3d}   no-cache: {no:5d} KV-computes   with-cache: {yes:4d}   speedup {no/yes:.1f}x")
    assert generate_with_cache(100) == 100, "cache should compute exactly n KV pairs (one per step)"
    assert generate_no_cache(100) == 5050, "no-cache should be n(n+1)/2 = 5050"
    print("PASS ✅  KV cache turned O(n^2) work into O(n).")
