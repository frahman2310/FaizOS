"""Inference internals (FaizOS build) — Module 14.

Three tricks that make serving fast, all fixing the same disease: a wasted GPU.
  1. PAGED KV          - hand out small fixed pages on demand instead of reserving the max length
  2. CONTINUOUS BATCH  - evict a finished sequence and admit a new one instead of waiting for all
  3. SPECULATIVE DECODE- a small draft model proposes k tokens, the big model verifies them in ONE pass

Fill the ONE blank, then run:  python3 serving.py
"""

PAGE = 16                       # tokens per KV page


def naive_kv_waste(max_len, actual_len):
    """Reserve the maximum a request could need; everything unused is wasted."""
    return max_len - actual_len


def paged_kv_waste(actual_len, page=PAGE):
    """Hand out whole pages on demand: only the last partial page is wasted."""
    pages = -(-actual_len // page)            # divide and round UP
    return pages * page - actual_len


def static_batch_idle(lengths):
    """Static batching runs until the SLOWEST sequence finishes; short ones idle after they end."""
    longest = max(lengths)
    return sum(longest - n for n in lengths)


def continuous_batch_idle(lengths):
    """A finished slot is refilled immediately, so no slot sits idle."""
    return 0


def tokens_per_big_pass(accepted):
    """Speculative decoding: the accepted draft tokens PLUS the one the verifier itself produces."""
    # The verification pass also computes the big model's own next token, which is free and always
    # valid, so you keep one more than the draft got right.
    return accepted + 1                       # the accepted drafts, plus the verifier's own token


if __name__ == "__main__":
    print("1. PAGED KV  (2048 reserved, 200 actually used)")
    print(f"   naive waste : {naive_kv_waste(2048, 200):>5} tokens")
    print(f"   paged waste : {paged_kv_waste(200):>5} tokens   (pages of {PAGE})")

    lengths = [100, 100, 100, 1000]
    print(f"\n2. CONTINUOUS BATCHING  (answer lengths {lengths})")
    print(f"   static idle     : {static_batch_idle(lengths):>5} slot-steps")
    print(f"   continuous idle : {continuous_batch_idle(lengths):>5} slot-steps")

    print("\n3. SPECULATIVE DECODING  (draft proposes 4)")
    for accepted in (0, 3, 4):
        t = tokens_per_big_pass(accepted)
        print(f"   {accepted} accepted -> {t} tokens per big pass   ({t}x vs plain decoding)")

    assert naive_kv_waste(2048, 200) == 1848
    assert paged_kv_waste(200) == 8, "13 pages of 16 = 208, minus 200 = 8"
    assert static_batch_idle([100, 100, 100, 1000]) == 2700, "three slots idle 900 steps each"
    assert tokens_per_big_pass(3) == 4, "3 accepted + 1 from the verifier"
    assert tokens_per_big_pass(0) == 1, "even with everything rejected you never do worse than normal"
    print("\nPASS ✅  stop reserving, stop waiting, stop decoding one token at a time.")
