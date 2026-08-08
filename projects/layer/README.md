# a layer of neurons

Built in **FaizOS**. A "layer" is just several neurons side by side — all reading the same inputs,
each producing its own output. Reuses your neuron + micrograd engine (with `tanh`).

## Acceptance
- Given one set of inputs, the layer produces **one output per neuron** (N neurons → N outputs).

## Run
```bash
python3 layer.py
```
