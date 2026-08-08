# a real neuron

Built in **FaizOS**. A single neuron: several inputs, each with its own weight, plus a bias, then a
`tanh` squish. It learns via gradient descent on the micrograd engine — the building block every
neural network is made of.

## Acceptance (verifiable)
- The neuron computes `tanh(w1*x1 + w2*x2 + ... + b)`.
- Trained toward a target, the loss drops to ~0 and the neuron outputs the right value.

## Run
```bash
python3 neuron.py
```
