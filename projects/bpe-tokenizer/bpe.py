"""BPE tokenizer (FaizOS build) — Module 9.

Turn text into integer tokens by repeatedly merging the most frequent adjacent pair.
The two helpers (get_stats, merge) are written for you; you fill the ONE line that IS the idea:
pick the most frequent pair. Then run:  python3 bpe.py
"""

def get_stats(ids):
    """Count how often each adjacent pair appears. Returns {pair: count}."""
    counts = {}
    for pair in zip(ids, ids[1:]):          # zip(ids, ids[1:]) walks every neighbour pair: (t0,t1),(t1,t2)...
        counts[pair] = counts.get(pair, 0) + 1   # add 1 to this pair's tally
    return counts

def merge(ids, pair, new_id):
    """Replace every occurrence of `pair` with the single token `new_id` (greedy, left to right)."""
    out, i = [], 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(new_id); i += 2     # found the pair -> emit the merged token, skip both
        else:
            out.append(ids[i]); i += 1     # no match -> keep this token, move on
    return out

def train(text, num_merges):
    ids = list(text.encode("utf-8"))       # text -> numbers 0..255 (one per byte; for letters, its ASCII code)
    merges = {}
    for step in range(num_merges):
        stats = get_stats(ids)
        best = max(stats, key=stats.get)                         # TODO: the MOST FREQUENT pair. Hint: max(stats, key=stats.get)
        new_id = 256 + step                 # new tokens get fresh ids: 256, 257, 258, ...
        ids = merge(ids, best, new_id)
        merges[best] = new_id
        print(f"merge {step}: {best} -> {new_id}   (sequence now {len(ids)} tokens)")
    return ids, merges

if __name__ == "__main__":
    text = "aaabdaaabac"
    start = len(text.encode("utf-8"))
    ids, merges = train(text, num_merges=3)
    print(f"\nstart: {start} tokens  ->  end: {len(ids)} tokens   ({len(merges)} merges learned)")
    assert len(ids) < start, "tokenizer did not compress the sequence"
    assert len(merges) == 3
    print("PASS ✅  BPE learned its merges and compressed the text.")
