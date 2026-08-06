---
description: Read what you built and bank the skills + gaps (learn-from-what-you-built)
argument-hint: (optional) path to the repo to analyze
---
This is **the brain learning from your work**. Be an honest staff-engineer reviewer — generous about real progress, straight about gaps.

1. Identify the repo: from `$ARGUMENTS`, else the current/last build's `repo_path`, else ask. Read the code and `git log`/diff.
2. Call `forge_list_skills` to get known skill ids.
3. Decide which skills the build **genuinely** exercised and how well — `outcome` 0..1 (barely ≈ 0.3, solid ≈ 0.7, strong/shipped ≈ 0.9). Map to known ids; for anything off-curriculum, use a sensible new kebab-id (it will be minted).
4. Identify real **gaps**: concepts it should have used but didn't, or used incorrectly.
5. Call `forge_analyze` with `{ skills:[{id,outcome,kind}], gaps:[…], notes }` — `kind:'ship'` if shipped, else `'build'`.
6. Report the mastery movements briefly, then **teach `teach_next`** — only what's needed — and suggest a short follow-up build that closes it.
7. If you wrote analysis notes into the repo, `git add -A && git commit`.
