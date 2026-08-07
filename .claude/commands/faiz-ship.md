---
description: Ship the current build (deploy/public/merge), update the streak, record the journey
argument-hint: (optional) ship URL
---
Shipping is the **celebrated moment**. Keep it crisp and rewarding.

1. Confirm the build actually works / meets its acceptance criteria. If not, say what's left and stop — don't ship vapor.
2. **Record the journey to GitHub (seamless once configured):**
   - Always `git add -A && git commit` the project locally.
   - Check `faizos_config` for `journey_repo`. If the project repo has an `origin` remote → `git push`. If `journey_repo` is set, also push the FaizOS journey (the auto-compiled `notebook/REVISIONS.md` + timeline) to it.
   - **Any push/publish is outward-facing** — only push to an **already-configured** remote. If nothing is configured, commit locally and give him the one-time setup: `faizos_config({ set: { journey_repo } })` + `git remote add`, or `gh repo create <name> --private --source . --push` (needs his go-ahead).
3. Call `faizos_ship` with the mission id (or none = current) and `ship_url` if there is one.
4. Celebrate briefly from the result: 🚢 title · 🔥 new streak (note if `best_streak` was beaten; if `grace_used`, mention a missed day was forgiven — positively) · shipped count.
5. Tell him to run `/faiz-analyze` to bank the skills, and tease the suggested next.
