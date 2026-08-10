"""SSM / Mamba-style token mixer (FaizOS build) — Module 8.

A non-attention way to mix tokens: scan the sequence left-to-right, carrying ONE running state.
  state = a*state + b*x     # update the fading memory
  y     = c*state           # read it out
O(n) time, O(1) memory per step (no growing KV cache). Fill the ONE recurrence line, then run.
"""

def ssm_scan(xs, a, b, c):
    """Scan a sequence, carrying a running state. Returns the output at each step."""
    state = 0.0
    ys = []
    for x in xs:
        state = a * state + b * x # TODO: the recurrence -> keep a*state, add b*x
        ys.append(c * state)
    return ys

if __name__ == "__main__":
    # impulse response: one spike then silence -> shows the state REMEMBERS then fades
    impulse = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ys = ssm_scan(impulse, a=0.9, b=1.0, c=1.0)
    print("impulse response (a=0.9):", [round(y, 4) for y in ys])

    # bigger a = longer memory
    slow = ssm_scan(impulse, a=0.99, b=1.0, c=1.0)
    print("impulse response (a=0.99):", [round(y, 4) for y in slow])

    # each output depends on ALL past inputs, computed in ONE linear pass (O(n))
    assert abs(ys[0] - 1.0) < 1e-9, "first step: state becomes the input"
    assert all(ys[t + 1] < ys[t] for t in range(len(ys) - 1)), "memory should fade after the spike"
    assert slow[3] > ys[3], "bigger a should remember longer"
    print("PASS ✅  an SSM: a fading running memory, O(n) — the non-attention token mixer.")
