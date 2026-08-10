# Held-out eval — perplexity from scratch

**Goal:** measure a language model honestly, on data it never trained on.

**Why held-out:** scoring on training data rewards memorization (overfitting). Hold out a vault of unseen data.

**Perplexity** = `exp(mean(-ln p))`, where p = probability the model gave the TRUE next token. Reads as the effective number of equally-likely options the model is torn among. Lower = better (1 = perfect; ~20 for GPT-2 on English).

**Result:** good model 1.14, bad 5.61, coin-flip 2.00. Run: `python3 eval.py` -> PASS. Module 10 skill `heldout-eval`.
