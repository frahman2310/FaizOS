"""micrograd — a tiny autograd engine (FaizOS build).

You built the forward half together (the box + add + multiply). This adds the slope half:
each operation remembers how to pass its slope back to its inputs, and backward() walks it.
Every slope line below is a rule you already know.
"""


class Value:
    def __init__(self, data, _parents=()):
        self.data = data                # the number
        self.grad = 0.0                 # the slope (filled in by backward)
        self._parents = _parents        # the boxes that made this one
        self._backward = lambda: None   # a note: "how to hand my slope to my inputs"

    def __add__(self, other):
        out = Value(self.data + other.data, (self, other))

        def _backward():
            # ADD rule (yours): pass the slope straight through to each input, ×1
            self.grad += 1 * out.grad
            other.grad += 1 * out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other))

        def _backward():
            # MULTIPLY rule (yours): each input gets the OTHER input's value × the slope
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def backward(self):
        # Put the boxes in order so we always handle a box before its inputs, then walk
        # from the output back to the inputs, letting each box hand its slope to its parents.
        order, seen = [], set()

        def visit(v):
            if id(v) not in seen:
                seen.add(id(v))
                for p in v._parents:
                    visit(p)
                order.append(v)
        visit(self)
        self.grad = 1.0                 # the output's slope with respect to itself is 1
        for v in reversed(order):
            v._backward()


def _acceptance():
    def f(a, b, c):
        return a * b + c                # d = a*b + c

    a, b, c = Value(3.0), Value(4.0), Value(5.0)
    d = f(a, b, c)
    d.backward()

    # ground truth: nudge each input a hair, measure d's change (this IS the definition of slope)
    def numeric(i, h=1e-6):
        vals = [3.0, 4.0, 5.0]
        up = vals.copy(); up[i] += h
        dn = vals.copy(); dn[i] -= h
        return (f(*[Value(x) for x in up]).data - f(*[Value(x) for x in dn]).data) / (2 * h)

    for name, box, i in [("a", a, 0), ("b", b, 1), ("c", c, 2)]:
        n = numeric(i)
        assert abs(box.grad - n) < 1e-4, f"d/d{name}: yours {box.grad} vs numeric {n}"
        print(f"  d/d{name}: micrograd={box.grad:.4f}   numeric={n:.4f}   ✓")
    print("ALL GRADIENTS MATCH — ship it 🚢")


if __name__ == "__main__":
    _acceptance()
