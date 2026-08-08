# an MLP that learns XOR

Built in **FaizOS**. A multi-layer perceptron: two layers of neurons stacked, trained to learn
**XOR** — a nonlinear pattern a *single* neuron cannot solve. Runs on your micrograd engine.

## Acceptance (verifiable)
- After training, the MLP outputs ~**1** for `(0,1)` and `(1,0)`, and ~**0** for `(0,0)` and `(1,1)`.
- The loss across the 4 XOR examples drops toward 0.

## Run
```bash
python3 mlp.py
```
