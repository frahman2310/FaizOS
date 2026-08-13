# Reward modeling — preferences, proxies and reward hacking

**When there is nothing to verify** ("write a helpful reply"), you cannot use RLVR. Humans are bad at absolute scores but good at COMPARISONS, so you collect pairs and train a reward model.

**Bradley-Terry:** `P(A beats B) = sigmoid(score_A - score_B)` — only the GAP matters (3 vs 1 and 5 vs 3 give the same answer; equal scores give 0.50).

**Reward hacking:** the reward model is a PROXY, and RL optimises proxies until it finds their flaws. A leak of +0.1 per sentence is enough to make a padded 5/10 answer (proxy 9.0) beat a good 8/10 one (proxy 8.3). Goodharts law.

**The defence:** `reward_used = rm_score - beta * drift` — charge the policy for moving away from the reference model. More drift, smaller reward.

Run: `python3 reward_model.py` -> PASS. Module 15 skill `reward-modeling-verifiers`. Completes Module 15.
