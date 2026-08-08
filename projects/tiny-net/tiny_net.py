"""tiny net that learns (FaizOS build).

One weight `w` learns to satisfy w*3 = 6 (so the right answer is w = 2), purely by gradient
descent on your micrograd engine. Fill the ONE blank (the update rule from brick 3), then run.
"""
from micrograd import Value

x = 3.0           # the input
target = 6.0      # the answer we want  (right weight is 2, since 2*3 = 6)
w = Value(1.0)    # the knob — starts wrong
lr = 0.05         # learning rate: how big a step each round

for step in range(15):
    # brick 1 — guess = w * x
    pred = w * Value(x)
    # brick 4 — loss = (guess - target)^2   ("- target" is written as "+ (-target)")
    diff = pred + Value(-target)
    loss = diff * diff
    # bricks 2+3 — get the gradient: micrograd fills w.grad with the slope of loss w.r.t. w
    w.grad = 0.0          # reset first (gradients accumulate)
    loss.backward()
    # THE LEARNING STEP — move w opposite its gradient:
    w.data = w.data - (lr * w.grad)        # TODO: new w = old w - (lr * gradient)   [gradient is w.grad]

    print(f"step {step:2d}:  w = {w.data:.3f}   loss = {loss.data:.4f}")

print(f"\nlearned w = {w.data:.3f}   (target: 2.0)")
