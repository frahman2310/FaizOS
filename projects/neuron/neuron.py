"""a real neuron (FaizOS build).

A neuron with 2 inputs, 2 weights, and a bias, squished by tanh, learns (by gradient descent on
your micrograd engine) to output a target value. Fill the 3 update blanks (same rule as your tiny
net, once per knob), then run.
"""
from micrograd import Value

# two fixed inputs, and the target we want the neuron to output
x1 = Value(1.0)
x2 = Value(-2.0)
target = 0.5

# the 3 knobs (start at some values)
w1 = Value(0.5)
w2 = Value(-0.5)
b = Value(0.0)
lr = 0.1

for step in range(60):
    # brick 1 — weighted sum + bias,  then  brick 2 — the tanh squish
    s = w1 * x1 + w2 * x2 + b
    out = s.tanh()
    # brick 4 — loss = (out - target)^2   ("- target" as "+ (-target)")
    diff = out + Value(-target)
    loss = diff * diff
    # reset the 3 gradients, then backward fills each knob's gradient
    w1.grad = 0.0
    w2.grad = 0.0
    b.grad = 0.0
    loss.backward()
    # brick 3 — update EACH knob:  new = old - (lr * that knob's gradient)
    w1.data = w1.data - lr * w1.grad        # TODO
    w2.data = w2.data - lr * w2.grad        # TODO
    b.data = b.data -lr * b.grad         # TODO

    print(f"step {step:2d}:  out = {out.data:.4f}   loss = {loss.data:.4f}")

print(f"\nneuron output = {out.data:.4f}   (target: {target})")
