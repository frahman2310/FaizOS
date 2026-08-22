---
description: The merged-PR track. Measured repo guidance, issue hunt, PR state.
---
The bar is a MERGED pull request, not an opened one. It is also one of the three evidence
currencies for the UK Global Talent route, alongside writing and recognition.

1. Call `faizos_oss` with `action: "status"`. Render current targets by state, then the
   measured repo guidance the tool returns. The short version, from GitHub API counts:
   - **vllm-project/vllm** — best target. 23 open good-first-issues, 62% of merges external,
     and his FlashAttention/KV-cache work is load-bearing there. Anything over 500 LOC needs
     an RFC issue first, and p75 time-to-merge is about 11 days.
   - **huggingface/transformers** — best hidden value. Zero open good-first-issues but 39
     unclaimed "Good Second Issue" items, which is exactly the shelf beginners cannot reach
     and he can.
   - **trl** and **litellm** are traps. 5% of TRL merges are external; 95 of litellm's last
     100 closed PRs were closed unmerged. Say so if he proposes either.
2. If he has no candidate, help him pick ONE issue and record it with `action: "add"`.
3. As it moves, record state with `action: "update"`: claimed, pr_open, merged. Log every
   review cycle, because the cycle count is the honest picture of what review costs.
4. On merge, the tool writes the systems row that closes capstone rung 6. Say so.

Realistic timeline: 2 to 6 weeks to a first small merge, 1 to 3 months for a substantive vLLM
PR including RFC discussion. Small and merged beats ambitious and ignored.
