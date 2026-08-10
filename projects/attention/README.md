# self-attention from scratch

Built in **FaizOS**. The core mechanism of the transformer (and GPT): each item looks at all the
others and blends in their information, **weighted by relevance**. Built as: similarity scores →
softmax into weights → weighted sum. Reuses your numerically-stable softmax.

## Acceptance (verifiable)
- Given a query and a few items, attention produces weights that **sum to 1** and **focus on the
  most relevant item**, then outputs the relevance-weighted blend.

## Run
```bash
python3 attention.py
```
