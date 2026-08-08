"""a layer of neurons (FaizOS build).

A layer = several neurons side by side, all reading the same inputs, each producing its own output.
Neuron A is written for you; write neuron B (same shape, with the b_ knobs), then run.
"""
from micrograd import Value

# the shared inputs — BOTH neurons read these
x1 = Value(2.0)
x2 = Value(3.0)

# neuron A — its own weights + bias
a_w1 = Value(0.5)
a_w2 = Value(-1.0)
a_b = Value(0.0)

# neuron B — its own weights + bias
b_w1 = Value(1.0)
b_w2 = Value(0.5)
b_b = Value(-1.0)

# each neuron's output = tanh(weighted sum + bias)
out_a = (a_w1 * x1 + a_w2 * x2 + a_b).tanh()
out_b = (b_w1 * x1 + b_w2 * x2 + b_b).tanh()          # TODO: same shape as out_a, but with the b_ knobs

print("layer outputs (one per neuron):", round(out_a.data, 4), round(out_b.data, 4))
