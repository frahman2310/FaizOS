"""Held-out evaluation — perplexity (FaizOS build) — Module 10.

Measure a language model on data it NEVER trained on. For each held-out token the model gives a
probability to the TRUE next word; perplexity = exp(mean surprise), surprise = -ln(p).
Perplexity reads as 'effective number of equally-likely options the model is torn between'.
Fill the ONE blank (perplexity from mean surprise), then run: python3 eval.py
"""
from math import log, exp

def perplexity(true_probs):
    """true_probs: the probability the model gave to each TRUE next token, on held-out data."""
    surprises = [-log(p) for p in true_probs]        # surprise per token = -ln(p)
    mean_surprise = sum(surprises) / len(surprises)  # average surprise
    return exp(mean_surprise)                                        # TODO: perplexity = exp(mean_surprise)

if __name__ == "__main__":
    # a confident, mostly-right model (high prob on the true words)
    good = [0.9, 0.8, 0.95, 0.85, 0.9]
    # a confused model (low prob on the true words)
    bad  = [0.2, 0.1, 0.3, 0.15, 0.2]
    # a "coin flip between 2 words" model
    coin = [0.5, 0.5, 0.5, 0.5]

    print(f"good model  perplexity: {perplexity(good):.2f}   (near 1 = barely confused)")
    print(f"bad model   perplexity: {perplexity(bad):.2f}   (torn among many words)")
    print(f"coin model  perplexity: {perplexity(coin):.2f}   (exactly 2 = a 2-way toss-up)")

    assert abs(perplexity(coin) - 2.0) < 1e-9, "p=0.5 each -> perplexity 2"
    assert perplexity(good) < perplexity(bad), "confident+right should have LOWER perplexity"
    print("PASS ✅  perplexity: a held-out score = effective number of choices the model is torn among.")
