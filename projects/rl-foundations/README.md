# RL foundations — REINFORCE, baselines and PPO clipping

**The shift:** supervised learning has a TARGET (how far off were you). RL only has a SCORE — nobody tells you what the best action was. So the only rule available is: do more of what scored ABOVE AVERAGE, less of what scored below.

```
advantage = reward - baseline      # baseline = the average reward
ratio     = new_prob / old_prob    # how far the policy moved
PPO clips the ratio to [0.8, 1.2]  # one noisy sample cannot wreck the policy
```

**Why subtract the average:** a raw reward means nothing alone (is 5 good?). Subtracting the mean turns an absolute score into a COMPARISON. Sign = which way to push, size = how hard. Advantages always sum to zero.

**Result:** rewards [5,7,9] -> advantages [-2,0,+2] -> probabilities 0.30->0.10, 0.30->0.30, 0.40->0.60. Clipping: 1.50->1.20, 0.50->0.80, 1.10 untouched.

Run: `python3 reinforce.py` -> PASS. Module 15 skill `rl-foundations`.
