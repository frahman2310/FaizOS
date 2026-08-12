# GRPO & RLVR — group-relative RL with verifiable rewards

**RLVR:** the reward comes from an automatic VERIFIER (is the maths right? do the tests pass?) scored 1/0. No humans, unlimited scale — which is why reasoning models are trained on maths and code.

**GRPO:** PPO trains a CRITIC network (another model the size of the policy) to predict the baseline. GRPO skips it — sample a GROUP of answers to the same prompt and use the group mean as the baseline. 7B critic -> 0B.

**The failure mode:** a group only teaches something if its answers DISAGREE. rewards [1,1,1,1] or [0,0,0,0] -> mean equals every reward -> all advantages zero -> wasted compute. (DAPO filters these groups.)

**Result:** mixed group [1,0,0,1] -> advantages [+0.5,-0.5,-0.5,+0.5] (learns); uniform groups -> all zeros (wasted).

Run: `python3 grpo.py` -> PASS. Module 15 skill `rlvr-grpo`.
