# ForgeOS

An AI operating system for becoming an elite AI engineer — a **Claude Code plugin** that turns
learning into a **build-and-ship loop**. You build real AI projects; ForgeOS teaches you what you
need *as you build*, reads what you shipped, and tracks your growing skills.

This is the **MVP**: the core `build → ship → learn` loop. Gamification chrome, the AI Opportunity
Radar, mobile, and the weekly audit come later (see `docs/` and the plan).

## How it works

- **`forgeos-core/`** — a local MCP server (TypeScript + SQLite): the deterministic brain. Holds the
  skills map (audited curriculum Phases 1–6), mastery scores, missions, streak, and the journey log.
  All the math runs here as code, so the model is only used for teaching and judgment (keeps tokens low).
- **`.claude/commands/`** — the `/forge*` slash commands (the UX).
- **`.mcp.json`** — registers `forgeos-core` with Claude Code.
- **`projects/`** — your real built repos live here (each its own git repo). Git-ignored by this repo.

## Setup (one time)

1. Deps are already installed (`forgeos-core/node_modules`). If you move the folder, update the
   absolute paths in `.mcp.json`.
2. **Restart Claude Code** in this folder so it loads `.mcp.json` (approve the `forgeos-core` server
   when prompted). Check it with `/mcp` — you should see `forgeos-core` connected.

## The loop

| Command | What it does |
|---|---|
| `/forge` | Dashboard: streak, current build, weakest skills, and the one recommended next step. |
| `/forge-build <idea>` | Scaffold a real repo and pair-build it; theory delivered just-in-time. |
| `/forge-ship` | Ship it (deploy/public/merge), update your streak, celebrate. |
| `/forge-analyze` | Read what you built → bank the skills → teach the one gap. |
| `/forge-review` | A short retrieval check on the must-know fundamentals. |

## Dev

```bash
cd forgeos-core
npm test              # pure-logic self-checks (mastery, streak)
npx tsx src/smoke.ts  # end-to-end: drives the server through the whole loop
```

State lives in `forgeos-core/data/forge.db` (SQLite). Delete it to reset.
