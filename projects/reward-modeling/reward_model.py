"""Reward modeling — preferences, proxies and reward hacking (FaizOS build) — Module 15.

Some tasks cannot be verified ("write a helpful reply"). Humans are bad at absolute scores but good
at COMPARISONS, so you collect pairs and train a reward model whose numbers agree with the winners:

    P(A beats B) = sigmoid(score_A - score_B)        # only the GAP matters

But that reward model is a PROXY, and RL optimises proxies relentlessly until it finds their flaws
(reward hacking). The standard defence is a penalty for drifting away from the reference model:

    reward_used = rm_score - beta * drift

Fill the ONE blank, then run:  python3 reward_model.py
"""
from math import exp


def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))


def prob_a_preferred(score_a, score_b):
    """Bradley-Terry: how often the reward model expects answer A to be chosen over B."""
    return sigmoid(score_a - score_b)


def penalised_reward(rm_score, drift, beta=0.5):
    """Keep the proxy honest: charge the policy for moving away from the reference model."""
    # More drift must make the final number SMALLER, so the penalty is taken away.
    return rm_score - beta * drift              # pay a penalty proportional to the drift


# --- a deliberately flawed proxy: it quietly rewards length ---
def flawed_rm(quality, n_sentences):
    """A reward model that mostly tracks quality but leaks +0.1 per extra sentence."""
    return quality + 0.1 * n_sentences


if __name__ == "__main__":
    print("Bradley-Terry — only the gap matters:")
    for a, b in ((3, 1), (1, 1), (1, 3)):
        print(f"  scores {a} vs {b}  (gap {a-b:+d})  ->  P(A preferred) = {prob_a_preferred(a, b):.2f}")

    print("\nreward hacking — the policy discovers the length leak:")
    print(f"  {'answer':<28} {'true quality':>13} {'proxy score':>12}")
    for label, quality, n in (("short and good", 8.0, 3), ("padded rambling", 5.0, 40)):
        print(f"  {label:<28} {quality:>13.1f} {flawed_rm(quality, n):>12.1f}")
    print("  -> the WORSE answer scores higher on the proxy. That is Goodhart's law.")

    print("\nKL penalty pulls it back (beta = 0.5):")
    for drift in (0.0, 2.0, 6.0):
        print(f"  proxy 9.0, drift {drift:.1f}  ->  used reward {penalised_reward(9.0, drift):.1f}")

    assert abs(prob_a_preferred(1, 1) - 0.5) < 1e-9, "equal scores -> no preference"
    assert prob_a_preferred(3, 1) > 0.85 and prob_a_preferred(1, 3) < 0.15
    assert prob_a_preferred(3, 1) == prob_a_preferred(5, 3), "only the GAP matters, not the absolute scores"
    assert flawed_rm(5.0, 40) > flawed_rm(8.0, 3), "the flawed proxy prefers the worse, longer answer"
    assert penalised_reward(9.0, 0.0) == 9.0, "no drift, no penalty"
    assert penalised_reward(9.0, 6.0) < penalised_reward(9.0, 2.0), "more drift must score LOWER"
    print("\nPASS ✅  preferences give scores; proxies get gamed; the KL penalty is the leash.")
