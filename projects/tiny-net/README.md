# tiny net that learns

Built in **FaizOS**. The smallest possible "learning": a single weight `w` that adjusts itself
(using the micrograd engine) until it fits a target. This is **gradient descent** — the loop every
neural network trains with.

## Acceptance (verifiable)
- Start with a wrong `w`; after a handful of steps the **loss drops to ~0**.
- `w` **learns** the correct value (e.g. learns `w ≈ 2` so that `w*3 ≈ 6`).

## Run
```bash
python3 tiny_net.py
```
