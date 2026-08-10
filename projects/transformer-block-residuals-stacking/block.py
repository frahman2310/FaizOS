"""Transformer block (FaizOS build) — Module 8.

Assemble the pieces you already built — RMSNorm, self-attention, an MLP — into ONE block,
wired together with RESIDUAL connections (out = x + layer(norm(x))), then STACK the block N times.
This is the first thing that looks like a real model (a mini-GPT stack).

Fill the 3 blanks marked TODO, then run:  python3 block.py
"""
from math import sqrt, exp

# ---------------------------------------------------------------------------
# The pieces you already built in earlier modules (given here so you can reuse them)
# ---------------------------------------------------------------------------

def rms_norm(vec):                       # Module 7: rescale a vector to a standard size (RMS ~ 1)
    r = sqrt(sum(x * x for x in vec) / len(vec)) or 1.0
    return [x / r for x in vec]

def softmax(xs):                         # Module 1: turn scores into weights that sum to 1
    m = max(xs)
    es = [exp(x - m) for x in xs]
    s = sum(es)
    return [e / s for e in es]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def add(a, b):                           # elementwise add of two vectors  (the residual "add back")
    return [x + y for x, y in zip(a, b)]

def attention(seq):                      # Module 7: each token attends to every token
    d = len(seq[0])
    out = []
    for q in seq:
        w = softmax([dot(q, k) / sqrt(d) for k in seq])          # relevance -> weights
        out.append([sum(w[j] * seq[j][c] for j in range(len(seq))) for c in range(d)])
    return out

# a tiny fixed MLP (Module 5): same little net applied to EACH token independently
_W1 = [[0.2, -0.1, 0.0, 0.1], [0.1, 0.2, -0.1, 0.0], [0.0, 0.1, 0.2, -0.1], [-0.1, 0.0, 0.1, 0.2]]
_W2 = [[0.3, 0.0, -0.1, 0.1], [0.0, 0.3, 0.1, -0.1], [-0.1, 0.1, 0.3, 0.0], [0.1, -0.1, 0.0, 0.3]]

def _matvec(W, v):
    return [dot(row, v) for row in W]

def mlp(vec):                            # per-token "think alone" step: W2 @ relu(W1 @ vec)
    h = [x if x > 0 else 0.0 for x in _matvec(_W1, vec)]   # relu hidden layer
    return _matvec(_W2, h)

# ---------------------------------------------------------------------------
# YOUR job: wire the pieces together with residuals, then stack.
# ---------------------------------------------------------------------------

def block(seq):
    """One transformer block: attention sub-layer, then MLP sub-layer, each wrapped in a residual."""
    # sub-layer 1 — attention, with pre-norm + residual
    attn = attention([rms_norm(t) for t in seq])            # norm each token, then mix across tokens
    seq = [add(seq[i], attn[i]) for i in range(len(seq))]   # residual: original + attention's work

    # sub-layer 2 — MLP, with pre-norm + residual
    mlp_out = [mlp(rms_norm(t)) for t in seq]               # norm each token, then think per-token
    seq = [add(seq[i], mlp_out[i]) for i in range(len(seq))]                    # TODO blank 2: residual = seq[i] + mlp_out[i]  (use add())
    return seq


def forward(seq, n_layers):
    """Stack the block n_layers times — the output of one block is the input to the next."""
    for _ in range(n_layers):
        seq = block(seq)                                    # stacking: each block's output feeds the next
    return seq


# ---------------------------------------------------------------------------
# Acceptance check: with residuals, a DEEP stack keeps the signal alive (RMS stays ~O(1)).
# The no-residual version vanishes. If yours stays bounded over 30 layers, the block works.
# ---------------------------------------------------------------------------
def rms_of(seq):
    return round(sum(sqrt(sum(x * x for x in t) / len(t)) for t in seq) / len(seq), 4)

if __name__ == "__main__":
    seq0 = [[1.0, 0.5, -0.5, 0.2], [0.3, -0.2, 0.4, 0.1], [-0.4, 0.6, 0.1, -0.3]]
    print("input token-RMS :", rms_of(seq0))
    out = forward(seq0, n_layers=30)
    print("after 30 blocks :", rms_of(out))
    assert all(all(abs(x) < 1e6 for x in t) for t in out), "signal exploded"
    assert rms_of(out) > 0.5, "signal vanished — residuals not wired?"
    print("PASS ✅  30-deep stack stayed alive — residuals + stacking work.")
