"""SwiGLU FFN (FaizOS build) — Module 8.

Upgrade the transformer block's feed-forward network from  W2 @ relu(W1 @ x)  (one path, hard switch)
to SwiGLU:  W2 @ ( swish(W1 @ x)  ⊙  (W3 @ x) )  — two paths, a learned smooth gate (Llama/PaLM).

The plumbing is written for you. Fill the ONE line that applies the gate, then run: python3 swiglu.py
"""
from math import exp

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def matvec(W, v):                      # W is a list of rows; output[i] = row_i · v
    return [dot(row, v) for row in W]

def ewmul(a, b):                       # element-wise (Hadamard) multiply: [a0*b0, a1*b1, ...]
    return [x * y for x, y in zip(a, b)]

def sigmoid(n):
    return 1.0 / (1.0 + exp(-n))

def swish(n):                          # smooth activation: n * sigmoid(n)  (a.k.a. SiLU)
    return n * sigmoid(n)

# --- old vs new, same x ---
def relu_ffn(x, W1, W2):               # the FFN you built before
    hidden = [max(0.0, n) for n in matvec(W1, x)]
    return matvec(W2, hidden)

def swiglu_ffn(x, W1, W3, W2):
    gate    = [swish(n) for n in matvec(W1, x)]   # the dimmer settings (smooth, via swish)
    content = matvec(W3, x)                        # the raw brightness
    hidden  = ewmul(gate, content)                                  # TODO: apply the gate to content, element-wise (use ewmul)
    return matvec(W2, hidden)

if __name__ == "__main__":
    x  = [1.0, -2.0, 0.5, 3.0]
    # tiny fixed weights (hidden dim 4, model dim 4)
    W1 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]     # gate projection
    W3 = [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]]     # content projection
    W2 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]     # output projection

    out = swiglu_ffn(x, W1, W3, W2)
    print("input   :", x)
    print("SwiGLU  :", [round(v, 4) for v in out])
    print("relu FFN:", [round(v, 4) for v in relu_ffn(x, W1, W2)])
    assert len(out) == len(x), "output dim must match model dim"
    assert all(abs(v) < 1e6 for v in out), "output blew up"
    # gate check: swish(W1@x) for the negative input dim should shrink that channel vs the raw content
    print("PASS ✅  SwiGLU runs — a gated FFN, the Llama upgrade to your ReLU MLP.")
