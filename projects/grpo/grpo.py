"""GRPO & RLVR — group-relative RL with verifiable rewards (FaizOS build) — Module 15.

RLVR: the reward comes from an automatic VERIFIER (is the maths right? do the tests pass?), scored
1 or 0. No humans, unlimited scale.

GRPO: PPO needs a CRITIC network to predict the baseline - another model the size of the policy.
GRPO skips it: sample a GROUP of answers to the SAME prompt and use the group's own mean as the
baseline. Same advantage rule as REINFORCE, no extra network.

But a group only teaches you something if its answers DISAGREE: if every answer scores the same,
every advantage is zero and the group is wasted compute.
Fill the ONE blank, then run:  python3 grpo.py
"""

def verify(answer, correct_answer):
    """The verifier: 1 if the answer is right, 0 if not. No human, no opinion."""
    return 1.0 if answer == correct_answer else 0.0


def group_advantages(rewards):
    """Each answer measured against how the GROUP did — the group is its own baseline."""
    mean = sum(rewards) / len(rewards)
    return [r - mean for r in rewards]


def has_signal(rewards):
    """A group only teaches something if its answers disagree; identical rewards give zero advantage."""
    # There is signal when the best and worst rewards in the group are NOT the same value.
    return max(rewards) != min(rewards)    # differing rewards mean a usable gradient


def critic_params(policy_params, uses_critic):
    """PPO trains a critic the size of the policy; GRPO trains none."""
    return policy_params if uses_critic else 0


if __name__ == "__main__":
    groups = {
        "mixed (2 right, 2 wrong)": [1.0, 0.0, 0.0, 1.0],
        "all correct (too easy)  ": [1.0, 1.0, 1.0, 1.0],
        "all wrong (too hard)    ": [0.0, 0.0, 0.0, 0.0],
    }
    for name, rewards in groups.items():
        advs = group_advantages(rewards)
        mark = "learns" if has_signal(rewards) else "WASTED"
        print(f"  {name}  rewards {rewards}  ->  advantages {advs}   {mark}")

    print("\nverifier on a maths question (correct answer 42):")
    for a in ("42", "41"):
        print(f"  answered {a!r} -> reward {verify(a, '42'):.0f}")

    p = 7e9
    print(f"\nextra parameters to train, {p/1e9:.0f}B policy:")
    print(f"  PPO  (with critic) : {critic_params(p, True)/1e9:.0f}B")
    print(f"  GRPO (no critic)   : {critic_params(p, False)/1e9:.0f}B")

    assert group_advantages([1, 0, 0, 1]) == [0.5, -0.5, -0.5, 0.5], "correct -> +0.5, wrong -> -0.5"
    assert group_advantages([1, 1, 1, 1]) == [0.0] * 4, "a uniform group gives no gradient at all"
    assert has_signal([1, 0, 0, 1]) is True
    assert has_signal([1, 1, 1, 1]) is False, "too easy: nothing to learn"
    assert has_signal([0, 0, 0, 0]) is False, "too hard: nothing to learn"
    assert verify("42", "42") == 1.0 and verify("41", "42") == 0.0
    print("\nPASS ✅  the group is its own baseline — but only when its answers disagree.")
