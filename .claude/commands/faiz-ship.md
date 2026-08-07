---
description: Ship the current build (deploy/public/merge), update the streak, record the journey
argument-hint: (optional) ship URL
---
Shipping is the **celebrated moment**. Keep it crisp and rewarding.

1. Confirm the build actually works / meets its acceptance criteria. If not, say what's left and stop — don't ship vapor.
2. Ship it appropriately: commit, and if it's meant to be public, push. **Any push/publish is outward-facing** — only push to an **already-configured remote** (check `faizos_config`). If none is set, commit locally and tell him how to add one (or run `gh repo create`, which needs his go-ahead).
3. Call `faizos_ship` with the mission id (or none = current) and `ship_url` if there is one.
4. Celebrate briefly from the result: 🚢 title · 🔥 new streak (note if `best_streak` was beaten; if `grace_used`, mention a missed day was forgiven — positively) · shipped count.
5. Tell him to run `/faiz-analyze` to bank the skills, and tease the suggested next.
