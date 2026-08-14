# FaizOS v1 audit

Written at Phase 0 of the v2 migration, 14 August 2026, on branch `faizos-v2`. This is the record of what exists before anything changes. Row counts here are the invariants every later phase is checked against.

## 1. Database

File: `faizos-core/data/faiz.db` (SQLite, WAL mode, gitignored). Schema is created by `faizos-core/src/db.ts` with `CREATE TABLE IF NOT EXISTS` plus idempotent seeding (`INSERT OR IGNORE` for skills and meta). There is no migration mechanism in v1. There are no indexes beyond primary keys and no foreign keys.

### Tables and columns

| Table | Columns | Rows |
|---|---|---|
| `skills` | id TEXT PK, name TEXT, phase INTEGER, must_know INTEGER dflt 0, build_hint TEXT dflt '', mastery REAL dflt 0, confidence REAL dflt 0, last_seen TEXT, on_curriculum INTEGER dflt 1 | 66 |
| `missions` | id INTEGER PK AI, title TEXT, idea TEXT dflt '', repo_path TEXT, status TEXT dflt 'active', created_at TEXT, shipped_at TEXT, ship_url TEXT | 44 |
| `journey_log` | id INTEGER PK AI, ts TEXT, kind TEXT, detail TEXT dflt '' | 271 |
| `meta` | key TEXT PK, value TEXT | 10 |
| `lessons` | id INTEGER PK AI, ts TEXT, topic TEXT, mission_id INTEGER, skills TEXT dflt '[]', struggles TEXT dflt '[]', worked TEXT dflt '[]', difficulty_felt TEXT | 44 |
| `insights` | id INTEGER PK AI, ts TEXT, note TEXT UNIQUE, weight INTEGER dflt 1, active INTEGER dflt 1 | 79 |
| `revisions` | id INTEGER PK AI, ts TEXT, topic TEXT, note_md TEXT | 52 |
| `reviews` | skill_id TEXT PK, stability REAL, difficulty REAL, last TEXT, due TEXT, reps INTEGER dflt 1 | 0 |
| `radar` | id INTEGER PK AI, ts TEXT, title TEXT, market TEXT dflt '', feasibility TEXT dflt '', roi_note TEXT dflt '', buildable_as TEXT dflt '' | 0 |

Machine readable copy of the counts: `docs/v1-rowcounts.json`.

### Meta keys (10)

Seven seeded defaults: `streak`, `best_streak`, `last_active_date`, `current_mission_id`, `journey_repo`, `github_user`, `projects_dir`. Three written at runtime: `pending_close`, `session_start_ts`, `session_start_mid`.

### Two corrections to the execution contract's table list

1. `mastery` is a column on `skills` (plus `confidence`), never a table. `streak` is a set of meta keys, never a table. The protection rule is applied to the data wherever it lives.
2. The contract's protected list omits `journey_log`, `meta`, `reviews` and `radar`, all of which exist. The broader reading applies: every pre-existing table and every pre-existing row is protected. `radar` (0 rows) is superseded in spirit by the v2 `ventures` tables but stays untouched.

## 2. MCP tool surface (16 tools, `faizos-core/src/server.ts`, 370 lines)

`faizos_state`, `faizos_start_build`, `faizos_ship`, `faizos_analyze`, `faizos_list_skills`, `faizos_config`, `faizos_review_queue`, `faizos_record_review`, `faizos_radar_save`, `faizos_radar_list`, `faizos_lesson_start`, `faizos_record_lesson`, `faizos_save_revision`, `faizos_notes`, `faizos_curriculum`, `faizos_progress`.

Registered via `.mcp.json`, which runs `node_modules/.bin/tsx src/server.ts` over stdio.

## 3. Hook wiring (`.claude/settings.json` plus `hooks/`)

| Event | Script | What it does |
|---|---|---|
| SessionStart | `hooks/session-start.sh` | Stamps the session window (`session-log.ts --start`), prints the dashboard prompt telling the model to call `faizos_state`. |
| Stop | `hooks/session-stop.sh` | Regenerates `SESSIONS.md`, `SUMMARY.md`, `REVISION.md` deterministically, auto commits and pushes them if changed. Then blocks session close with a JSON decision if `pending_close` is set, guarded by `stop_hook_active`. |

Known interaction for v2: the Stop hook creates artefact commits on whatever branch is checked out. These are separate from the one commit per phase rule and are left as they are.

## 4. Slash commands (7)

`/faiz`, `/faiz-build`, `/faiz-ship`, `/faiz-analyze`, `/faiz-review`, `/faiz-notes`, `/faiz-radar`. All in `.claude/commands/`. `/faiz-build` carries the v1 teaching protocol (Brick Method, walk the code, blank filling), which v2 replaces with the eight step loop.

## 5. Artefact generators (deterministic, no model in the loop)

| Generator | Writes | Reads |
|---|---|---|
| `src/notebook.ts` (via `faizos_save_revision`) | `notebook/REVISIONS.md` | `revisions` |
| `src/session-log.ts` | `notebook/SESSIONS.md` | `missions`, `revisions`, `skills`, meta session window keys |
| `src/build-summary.ts` | `notebook/SUMMARY.md` | `skills`, `missions`, `lessons`, curriculum MODULES |
| `src/revision-compile.ts` | `notebook/REVISION.md` | `revisions`, `lessons`, curriculum MODULES |

`CAPSTONE.md` and `COURSE.md` were written by hand in v1. v2 Phase 5 makes `CAPSTONE.md` generated and auto scored.

## 6. Test and build tooling at Phase 0

- `npm test` now runs `vitest run` followed by the four v1 self check files (`mastery.ts`, `streak.ts`, `notebook.ts`, `fsrs.ts`). All green at Phase 0.
- `npx tsx src/smoke.ts` spins up the real MCP server over stdio against a temp database and walks the full v1 loop. Green at Phase 0.
- `vitest` added at Phase 0 with `vitest.config.ts`. New v2 code gets vitest tests.
- `tsconfig.json` (strict) added at Phase 0 with an `npm run typecheck` script. Legacy v1 files predate strict mode and are held to it only when touched. New v2 code is written strict clean with no `any`.
- Backup tool `src/backup.ts` uses the SQLite online backup API (WAL safe) and verifies per table row counts. Phase 0 backup: `~/faizos-backups/faiz-2026-08-14T00-32-33-640Z.db`, all nine tables verified matching.

## 7. Known duplicate skill ids

`torch-compile` (module 6) and `torch-compile-cuda-graphs` (module 12) cover the same topic and were both banked during v1. Both map to track T4 in the Phase 2 backfill. No row is touched.

## 8. Repository state at Phase 0

Branch `faizos-v2` cut from `main` at `ea0e860`, upstream set. Working tree clean apart from Phase 0 additions. Remote: `https://github.com/frahman2310/FaizOS.git` (public). Spec copied to repo root as `FaizOS-v2-Research-and-Spec.md`; execution contract copied to `docs/v2-execution-prompt.md`.
