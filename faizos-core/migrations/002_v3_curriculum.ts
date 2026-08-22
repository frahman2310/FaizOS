// Migration 002: the v3 curriculum. Additive only.
//   - tracks.kind + tracks.guidance_policy: the per-domain guidance switch. Expertise reversal
//     says worked examples beat blank pages for novices and reverse for experts, so the guard
//     must read the policy off the track instead of blocking unconditionally.
//   - builds.rebuild_due / reveal_notes / revealed_at: the reveal-and-contrast step and the
//     14 day unaided rebuild that separates 'provisional' from 'done'.
//   - systems.p95_ms / cost_per_1k: every shipped thing carries a number.
//   - oss_targets: the merged-PR track. cost_drills: the "every answer ends with a number" drill.
// No pre-existing table, column or row is modified.
import type { Database } from 'better-sqlite3';

export const version = 2;
export const name = 'v3_curriculum';

export function up(db: Database): void {
  db.exec(`
    ALTER TABLE tracks  ADD COLUMN kind TEXT DEFAULT 'ml';               -- production | ml | ship
    ALTER TABLE tracks  ADD COLUMN guidance_policy TEXT DEFAULT 'write_from_empty';
    ALTER TABLE builds  ADD COLUMN rebuild_due TEXT;                     -- unaided rebuild date
    ALTER TABLE builds  ADD COLUMN reveal_notes TEXT;                    -- his diff vs reference
    ALTER TABLE builds  ADD COLUMN revealed_at TEXT;
    ALTER TABLE systems ADD COLUMN p95_ms REAL;
    ALTER TABLE systems ADD COLUMN cost_per_1k REAL;
  `);

  db.exec(`
    CREATE TABLE oss_targets (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      repo          TEXT NOT NULL,
      issue_url     TEXT NOT NULL DEFAULT '',
      issue_title   TEXT NOT NULL DEFAULT '',
      difficulty    TEXT NOT NULL DEFAULT 'first',   -- first | second | substantive
      state         TEXT NOT NULL DEFAULT 'candidate', -- candidate | claimed | pr_open | merged | abandoned
      pr_url        TEXT,
      review_cycles INTEGER NOT NULL DEFAULT 0,
      notes         TEXT NOT NULL DEFAULT '',
      created_at    TEXT NOT NULL,
      merged_at     TEXT
    );

    CREATE TABLE cost_drills (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      scenario      TEXT NOT NULL,
      expected_json TEXT NOT NULL DEFAULT '{}',
      answer_json   TEXT NOT NULL DEFAULT '{}',
      correct       INTEGER NOT NULL DEFAULT 0,
      off_by_ratio  REAL,
      created_at    TEXT NOT NULL
    );

    CREATE INDEX idx_oss_state    ON oss_targets(state);
    CREATE INDEX idx_builds_rebuild ON builds(rebuild_due);
  `);
}

export function down(db: Database): void {
  db.exec(`
    DROP INDEX IF EXISTS idx_builds_rebuild;
    DROP INDEX IF EXISTS idx_oss_state;
    DROP TABLE IF EXISTS cost_drills;
    DROP TABLE IF EXISTS oss_targets;
    ALTER TABLE systems DROP COLUMN cost_per_1k;
    ALTER TABLE systems DROP COLUMN p95_ms;
    ALTER TABLE builds  DROP COLUMN revealed_at;
    ALTER TABLE builds  DROP COLUMN reveal_notes;
    ALTER TABLE builds  DROP COLUMN rebuild_due;
    ALTER TABLE tracks  DROP COLUMN guidance_policy;
    ALTER TABLE tracks  DROP COLUMN kind;
  `);
}
