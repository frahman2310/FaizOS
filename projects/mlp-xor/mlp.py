"""an MLP that learns XOR (FaizOS build).

A 2-2-1 network: 2 inputs -> a hidden layer of 2 neurons -> 1 output neuron. Trained on the 4 XOR
examples with gradient descent on micrograd. Fill the ONE update blank, then run.
"""
from micrograd import Value
import random
random.seed(42)


def neuron(inputs, weights, bias):
    s = bias
    for i in range(len(inputs)):
        s = s + weights[i] * inputs[i]
    return s.tanh()


def rnd():
    return Value(random.uniform(-1, 1))


# --- the network's knobs (weights + biases) ---
# hidden layer: neuron A and neuron B, each reads the 2 inputs
a_w = [rnd(), rnd()]; a_b = Value(0.0)
b_w = [rnd(), rnd()]; b_b = Value(0.0)
# output layer: one neuron, reads the 2 hidden outputs
o_w = [rnd(), rnd()]; o_b = Value(0.0)

params = a_w + [a_b] + b_w + [b_b] + o_w + [o_b]     # all 9 knobs, one flat list


def forward(x1, x2):
    inp = [Value(x1), Value(x2)]
    hA = neuron(inp, a_w, a_b)           # hidden neuron A
    hB = neuron(inp, b_w, b_b)           # hidden neuron B
    return neuron([hA, hB], o_w, o_b)    # output neuron combines them


data = [([0, 0], -1), ([0, 1], 1), ([1, 0], 1), ([1, 1], -1)]   # XOR (same = -1, differ = +1)
lr = 0.3

for epoch in range(3000):
    total = Value(0.0)                   # loss summed over the 4 examples
    for (x, y) in data:
        out = forward(x[0], x[1])
        diff = out + Value(-y)
        total = total + diff * diff
    for p in params:                     # reset gradients
        p.grad = 0.0
    total.backward()                     # gradients for all 9 knobs at once
    for p in params:                     # update each knob
        p.data = p.data - lr * p.grad    # your rule, per knob (old value = p.data, gradient = p.grad)
    if epoch % 500 == 0:
        print(f"epoch {epoch:4d}   loss {total.data:.4f}")

print("\nfinal predictions (want: -1, +1, +1, -1):")
for (x, y) in data:
    print(f"  {x} -> {forward(x[0], x[1]).data:+.3f}   (want {y})")
