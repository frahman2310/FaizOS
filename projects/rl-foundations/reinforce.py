"""RL foundations — REINFORCE, baselines and PPO clipping (FaizOS build) — Module 15.

Supervised learning has a TARGET (how far off were you). RL only has a SCORE: you act, you get a
reward, and nobody tells you what the best action was. So the only rule available is:

    do more of what scored ABOVE AVERAGE, less of what scored below.

    advantage = reward - baseline          # baseline = the average reward
    ratio     = new_prob / old_prob        # how much the policy moved
    PPO clips that ratio so one noisy sample cannot wreck the policy.

Fill the ONE blank, then run:  python3 reinforce.py
"""

CLIP = 0.2                      # PPO allows the policy to move by +/- 20% in one step


def baseline(rewards):
    """The average reward — what 'doing OK' looks like for this batch."""
    return sum(rewards) / len(rewards)


def advantages(rewards):
    """How much better or worse than average each action was."""
    b = baseline(rewards)
    # Above average must come out POSITIVE, below average NEGATIVE.
    return [r - b for r in rewards]        # how far this reward is above or below average


def clipped_ratio(new_prob, old_prob, clip=CLIP):
    """PPO: measure how far the policy moved, and refuse to let it move more than +/- clip."""
    ratio = new_prob / old_prob
    return min(max(ratio, 1 - clip), 1 + clip)


def update(prob, adv, lr=0.1):
    """Nudge a probability by its advantage: positive pushes up, negative pushes down."""
    return prob + lr * adv


if __name__ == "__main__":
    rewards = [5.0, 7.0, 9.0]
    probs = [0.30, 0.30, 0.40]
    print(f"rewards   : {rewards}   baseline {baseline(rewards):.1f}")
    print(f"advantages: {advantages(rewards)}")

    print("\nwhat happens to each action's probability:")
    for r, p, a in zip(rewards, probs, advantages(rewards)):
        direction = "UP  " if a > 0 else ("DOWN" if a < 0 else "same")
        print(f"  reward {r:.0f}, advantage {a:+.1f}  ->  {direction}  {p:.2f} -> {update(p, a):.2f}")

    print("\nPPO clipping (limit +/- 20%):")
    for new, old in ((0.45, 0.30), (0.33, 0.30), (0.15, 0.30)):
        print(f"  {old:.2f} -> {new:.2f}: raw ratio {new/old:.2f}, allowed {clipped_ratio(new, old):.2f}")

    assert baseline([5, 7, 9]) == 7
    assert advantages([5, 7, 9]) == [-2, 0, 2], "worst reward must give the most NEGATIVE advantage"
    assert sum(advantages([5, 7, 9])) == 0, "advantages always sum to zero around the mean"
    assert clipped_ratio(0.45, 0.30) == 1.2, "raw 1.5 gets clipped down to 1.2"
    assert clipped_ratio(0.15, 0.30) == 0.8, "raw 0.5 gets clipped up to 0.8"
    assert clipped_ratio(0.33, 0.30) == 1.1, "a small move is left alone"
    print("\nPASS ✅  above average up, below average down, and never move too far at once.")
