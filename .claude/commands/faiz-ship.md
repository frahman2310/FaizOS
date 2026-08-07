---
description: Ship the current build (deploy/public/merge), update the streak, record the journey
argument-hint: (optional) ship URL
---
Shipping is the **celebrated moment**. Keep it crisp and rewarding.

1. Confirm the build actually works / meets its acceptance criteria. If not, say what's left and stop — don't ship vapor.
2. **Ship to GitHub (auto-push is ON).** `git add -A && git commit && git push` — the journey repo (`journey_repo`, `origin`) is configured, so this pushes everything (the build + `notebook/REVISIONS.md` + timeline) to Faiz's **private** repo. He authorized constant auto-push, so push without asking. (Only a brand-new *public* repo would need his go-ahead.)
3. Call `faizos_ship` with the mission id (or none = current) and `ship_url` if there is one.
4. Celebrate briefly: 🚢 title · 🔥 new streak (note if `best_streak` beaten; if `grace_used`, a missed day was forgiven — positively) · shipped count.
5. **Auto-close the loop immediately — do NOT wait for him to ask:**
   - Analyze the build: `faizos_analyze` (read the repo, bank the skills, teach the one gap).
   - Post the Revision Note and save it: `faizos_save_revision`.
   - `faizos_record_lesson` with 1–2 `new_insights` (this clears the pending flag).
   - `git add -A && git commit && git push` the journey. Then tease the suggested next build.
