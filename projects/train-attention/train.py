"""Train attention (FaizOS build) — the attention weight is LEARNED, not hardcoded.

One learnable parameter `g` (a raw score) is tuned by gradient descent until the model learns to
attend to the relevant token (token B = 5.0), driving loss -> 0. Reuses your micrograd Value
(+, *, tanh). Fill the ONE blank (the update step), then run:  python3 train.py
"""
from micrograd import Value

# two value-tokens (fixed): the model must LEARN which one to attend to
vA = Value(1.0)          # token A
vB = Value(5.0)          # token B  <- we want the model to focus here
target = Value(5.0)      # the output we want

# the ONE learnable parameter: a raw attention score. Start neutral (g = 0  ->  wB = 0.5).
g = Value(0.0)

def sigmoid(x):
    # squish any number into (0,1), built from YOUR tanh:  0.5 + 0.5*tanh(0.5*x)
    return Value(0.5) + Value(0.5) * (Value(0.5) * x).tanh()

def forward():
    wB = sigmoid(g)                          # attention weight on token B, in (0,1)
    wA = Value(1.0) + Value(-1.0) * wB       # wA = 1 - wB
    output = wA * vA + wB * vB               # the blended attention output
    return output, wB

lr = 1.0
for step in range(101):
    output, wB = forward()                             # 1. forward
    diff = output + Value(-1.0) * target               #    (output - target)
    loss = diff * diff                                 # 2. loss = squared error
    g.grad = 0.0                                        #    reset slope before backward
    loss.backward()                                    # 3. backward -> fills g.grad
    g.data = g.data - lr * g.grad                       # 4. update — step downhill: move by lr*grad, against the slope
    if step % 20 == 0:
        print(f"step {step:3d}   loss {loss.data:.4f}   wB {wB.data:.3f}   output {output.data:.3f}")

print(f"\nlearned wB = {wB.data:.3f}  (started 0.5)  ->  output {output.data:.3f}  (target {target.data})")
assert loss.data < 0.01, "loss did not converge — check the update step"
assert wB.data > 0.9, "model did not learn to attend to token B"
print("PASS ✅  the model LEARNED its attention weight by gradient descent.")
