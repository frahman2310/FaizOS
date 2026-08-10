"""self-attention from scratch (FaizOS build).

The 3 steps you learned: score each item by relevance (dot product) -> softmax into weights ->
weighted blend of the items. Fill the ONE blank in `dot`, then run.
"""
from softmax import softmax   # your numerically-stable softmax, reused


def dot(a, b):
    # relevance score = multiply matching numbers and add them up (a dot product)
    s = 0.0
    for i in range(len(a)):
        s = s + a[i] * b[i]                      # TODO: add a[i]*b[i] to the running total (the dot product)
    return s


def attention(query, items):
    # 1) score each item by relevance (dot product with the query)
    scores = []
    for item in items:
        scores.append(dot(query, item))
    # 2) softmax the scores -> attention weights (sum to 1)
    weights = softmax(scores)
    # 3) output = weighted blend of the items
    dim = len(items[0])
    out = [0.0] * dim
    for i in range(len(items)):          # each item
        for d in range(dim):             # each dimension
            out[d] = out[d] + weights[i] * items[i][d]
    return scores, weights, out


# a tiny example: the query points like item 0
query = [1.0, 0.0]
items = [
    [1.0, 0.0],   # item 0: same direction as query  -> most relevant
    [0.0, 1.0],   # item 1: perpendicular            -> least relevant
    [0.9, 0.1],   # item 2: similar-ish              -> fairly relevant
]

scores, weights, out = attention(query, items)
print("scores :", [round(s, 3) for s in scores])
print("weights:", [round(w, 3) for w in weights], "  (sum =", round(sum(weights), 3), ")")
print("output :", [round(o, 3) for o in out])
