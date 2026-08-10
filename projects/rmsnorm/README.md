# RMSNorm

Built in **FaizOS**. A normalization that keeps each vector at a consistent size: divide every
element by the vector's RMS (root-mean-square). Keeps the numbers flowing through a deep network
stable. Used in Llama & most modern transformers. *(Completes Module 7.)*

## Acceptance (verifiable)
- Given any vector, RMSNorm outputs a vector whose RMS is ~1 (consistent scale), regardless of the
  input's original size.

## Run
```bash
python3 rmsnorm.py
```
