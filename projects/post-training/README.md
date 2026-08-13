# Post-training — distillation vs RL, DPO, tool calling

Three ways a raw pretrained model becomes useful.

**1. Distillation vs RL.** Distillation copies a strong teacher's reasoning traces (supervised, cheap, effective) — but the student is CAPPED at the teacher (70% teacher -> 70% ceiling). RL discovers its own solutions from reward: expensive, but no teacher means no ceiling. That is how a model surpasses everything that trained it.

**2. RLHF vs DPO.** RLHF = train a reward model, then RL against it: 2 stages, 3 models. DPO optimises the preference pair directly: 1 stage, 2 models. Simpler and cheaper — most open fine-tunes use it.

**3. Tool calling.** The model only EMITS text that looks like a call. YOUR code reads it, decides whether to run it, and feeds the result back. The model never executes anything — which is the entire safety story of agents (and what MCP standardises). Demo: `delete_file` is refused because it is not in the approved registry.

**Python rule learned:** square brackets `[ ]` LOOK UP, round brackets `( )` RUN. `tools[name](args)` = find the function, then call it.

Run: `python3 post_training.py` -> PASS. Module 16 skills `reasoning-distillation`, `rlhf-dpo`, `tool-calling`. Completes Module 16.
