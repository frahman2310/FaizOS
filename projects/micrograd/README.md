# micrograd — autograd from scratch

Built in **FaizOS**. A tiny automatic-differentiation engine: a `Value` class that wraps a number,
records the operations done to it, and computes gradients by backpropagation — the exact machinery
that lets neural nets learn.

## Acceptance criteria (verifiable)
- A `Value` supports `+` and `*`.
- Calling `.backward()` fills in `.grad` on every input.
- For a small expression, the gradients match hand-derivatives (and PyTorch) to `1e-6`.

## Run
```bash
python3 micrograd.py
```
