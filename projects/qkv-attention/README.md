# QKV attention (scaled dot-product)

Built in **FaizOS**. The *real* transformer attention: each item is projected into a **Query**, a
**Key**, and a **Value**. Scores = `query·key / √d` → softmax → weighted sum of the **Values**.
Upgrades your basic self-attention. *(Module 7.)*

## Acceptance (verifiable)
- Each item produces a query, a key, and a value (via learned weight matrices).
- Output = `softmax(Q·K / √d)` weighted sum of `V`; attention weights sum to 1.

## Run
```bash
python3 qkv.py
```
