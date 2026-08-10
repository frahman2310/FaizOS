"""QKV attention — scaled dot-product (FaizOS build).

Each item is projected into a Query, Key, Value (via weight matrices). Then: score = Q·K / sqrt(d)
-> softmax -> weighted sum of Values. Fill the ONE blank (the 1/sqrt(d) scaling), then run.
"""
from math import sqrt
from softmax import softmax


def dot(a, b):
    s = 0.0
    for i in range(len(a)):
        s = s + a[i] * b[i]
    return s


def project(vec, W):
    # W is a list of rows; output[k] = dot(row_k, vec)  (a matrix-vector product)
    return [dot(row, vec) for row in W]


# a tiny sequence of 2D items
items = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1]]
d = 2

# learned weight matrices (fixed here for the demo)
Wq = [[1.0, 0.0], [0.0, 1.0]]     # Query projection
Wk = [[1.0, 0.0], [0.0, 1.0]]     # Key projection
Wv = [[0.0, 1.0], [1.0, 0.0]]     # Value projection (swaps dims, so V differs from the item)

# project every item into its Key and Value
K = [project(it, Wk) for it in items]
V = [project(it, Wv) for it in items]

# use item 0's Query
q = project(items[0], Wq)

# score each item, then SCALE by 1/sqrt(d)
scores = []
for k in K:
    raw = dot(q, k)               # relevance = Query · Key
    scores.append(raw / sqrt(d))            # TODO: scale the raw score by 1/sqrt(d)  ->  raw / sqrt(d)

weights = softmax(scores)

# output = weighted sum of the Values
out = [0.0] * d
for j in range(len(items)):
    for c in range(d):
        out[c] = out[c] + weights[j] * V[j][c]

print("scores :", [round(s, 3) for s in scores])
print("weights:", [round(w, 3) for w in weights], "  (sum =", round(sum(weights), 3), ")")
print("output :", [round(o, 3) for o in out])
