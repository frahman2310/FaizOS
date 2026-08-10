"""RoPE — rotary positions (FaizOS build).

Rotate the Query (at position i) and Key (at position j) by (position * theta), then score them.
The score depends only on the distance (i - j). Fill the ONE blank, then run.
"""
from math import cos, sin


def dot(a, b):
    s = 0.0
    for i in range(len(a)):
        s = s + a[i] * b[i]
    return s


def rotate(vec, angle):
    # spin a 2D vector by `angle` radians (a 2D rotation)
    x, y = vec[0], vec[1]
    return [x * cos(angle) - y * sin(angle), x * sin(angle) + y * cos(angle)]


theta = 1.0          # base angle per position step
q = [1.0, 0.0]       # a Query vector
k = [1.0, 0.0]       # an identical Key vector


def score(i, j):
    # rotate the Query by its position i, the Key by its position j, then dot them
    q_rot = rotate(q, i * theta)       # rotate the Query by ITS OWN position i (not j)
    k_rot = rotate(k, j * theta)
    return dot(q_rot, k_rot)


print("q@0, k@0  (distance 0):", round(score(0, 0), 4))
print("q@2, k@0  (distance 2):", round(score(2, 0), 4))
print("q@5, k@3  (distance 2):", round(score(5, 3), 4))
print("q@1, k@0  (distance 1):", round(score(1, 0), 4))
