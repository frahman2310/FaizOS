# RoPE — rotary positional embeddings

Built in **FaizOS**. Plain attention is **order-blind** (a bag of items). RoPE injects *position* by
**rotating** each item's Query and Key by an angle proportional to its position — so attention
scores become **relative-position aware**. A small add-on to your QKV attention. *(Module 7.)*

## Acceptance (verifiable)
- Rotating Q and K by position makes the attention score between positions i and j depend on their
  distance (i−j), so identical items at different positions attend differently.

## Run
```bash
python3 rope.py
```
