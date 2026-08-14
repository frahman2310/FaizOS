// Migration 001: the FaizOS v2 schema. Additive only, exactly spec section 9.1 plus:
//   - builds table (user approved home for the PreToolUse guard state), with test_path so the
//     dashboard can point at the failing tests
//   - evidence.jtbd column, required by spec 8.3 stage 2 (each record stores its job to be done)
// No pre-existing table, column or row is modified.
import type { Database } from 'better-sqlite3';

export const version = 1;
export const name = 'v2_schema';

export function up(db: Database): void {
  // --- ALTERs on existing tables (additive columns with constant defaults) ---
  db.exec(`
    ALTER TABLE lessons  ADD COLUMN mode TEXT DEFAULT 'course';
    ALTER TABLE lessons  ADD COLUMN depth TEXT DEFAULT 'explain';
    ALTER TABLE lessons  ADD COLUMN track_id INTEGER;
    ALTER TABLE lessons  ADD COLUMN hint_max_rung INTEGER DEFAULT 0;
    ALTER TABLE lessons  ADD COLUMN student_wrote INTEGER DEFAULT 1;
    ALTER TABLE skills   ADD COLUMN track_id INTEGER;
    ALTER TABLE skills   ADD COLUMN source TEXT DEFAULT 'syllabus';
    ALTER TABLE insights ADD COLUMN mode TEXT;
  `);

  // --- New tables ---
  db.exec(`
    CREATE TABLE tracks (
      id              INTEGER PRIMARY KEY AUTOINCREMENT,
      code            TEXT NOT NULL UNIQUE,
      title           TEXT NOT NULL,
      position        INTEGER NOT NULL,
      status          TEXT NOT NULL DEFAULT 'pending',   -- pending | active | complete
      prereq_codes    TEXT NOT NULL DEFAULT '[]',
      completion_test TEXT NOT NULL DEFAULT '',
      current_as_of   TEXT
    );

    CREATE TABLE systems (
      id             INTEGER PRIMARY KEY AUTOINCREMENT,
      track_id       INTEGER,
      title          TEXT NOT NULL,
      repo_url       TEXT,
      kind           TEXT NOT NULL,                      -- trained_model | serving_stack | kernel | product | study
      status         TEXT NOT NULL DEFAULT 'planned',
      metric_name    TEXT,
      metric_value   REAL,
      baseline_value REAL,
      deployed_url   TEXT,
      created_at     TEXT NOT NULL,
      shipped_at     TEXT
    );

    CREATE TABLE experiments (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      system_id    INTEGER,
      config_json  TEXT NOT NULL DEFAULT '{}',
      seed         INTEGER,
      metric_name  TEXT,
      metric_value REAL,
      gpu_type     TEXT,
      gpu_hours    REAL,
      cost_usd     REAL,
      notes        TEXT NOT NULL DEFAULT '',
      created_at   TEXT NOT NULL
    );

    CREATE TABLE errors (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      lesson_id    INTEGER,
      category     TEXT NOT NULL,
      description  TEXT NOT NULL DEFAULT '',
      code_excerpt TEXT NOT NULL DEFAULT '',
      rule_broken  TEXT NOT NULL DEFAULT '',
      resolved     INTEGER NOT NULL DEFAULT 0,
      occurrences  INTEGER NOT NULL DEFAULT 1,
      last_seen    TEXT
    );

    CREATE TABLE code_reviews (
      id                INTEGER PRIMARY KEY AUTOINCREMENT,
      lesson_id         INTEGER,
      student_code      TEXT NOT NULL DEFAULT '',
      reference_code    TEXT NOT NULL DEFAULT '',
      diff_summary      TEXT NOT NULL DEFAULT '',
      correctness_diffs TEXT NOT NULL DEFAULT '[]',
      taste_diffs       TEXT NOT NULL DEFAULT '[]',
      created_at        TEXT NOT NULL
    );

    CREATE TABLE ventures (
      id             INTEGER PRIMARY KEY AUTOINCREMENT,
      title          TEXT NOT NULL,
      thesis         TEXT NOT NULL DEFAULT '',
      stage          TEXT NOT NULL DEFAULT 'candidate',  -- candidate | corroborated | scored | active | parked | killed
      score_json     TEXT NOT NULL DEFAULT '{}',
      weighted_score REAL,
      wip_lock       INTEGER NOT NULL DEFAULT 1,
      v0_metric      TEXT,
      v0_deadline    TEXT,
      outcome        TEXT,
      postmortem     TEXT,
      created_at     TEXT NOT NULL
    );

    CREATE TABLE evidence (
      id              INTEGER PRIMARY KEY AUTOINCREMENT,
      venture_id      INTEGER,                           -- NULL until stage 3 groups it
      source_family   TEXT NOT NULL,
      source_url      TEXT NOT NULL,
      excerpt         TEXT NOT NULL,
      jtbd            TEXT NOT NULL DEFAULT '',
      importance      INTEGER,
      dissatisfaction INTEGER,
      captured_at     TEXT NOT NULL
    );

    CREATE TABLE frontier (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,
      area             TEXT NOT NULL,
      title            TEXT NOT NULL,
      url              TEXT NOT NULL DEFAULT '',
      summary          TEXT NOT NULL DEFAULT '',
      affects_track_id INTEGER,
      ingested_at      TEXT NOT NULL,
      actioned         INTEGER NOT NULL DEFAULT 0
    );

    CREATE TABLE builds (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      lesson_id     INTEGER,
      solution_path TEXT NOT NULL,
      test_path     TEXT NOT NULL DEFAULT '',
      state         TEXT NOT NULL DEFAULT 'awaiting_student',  -- awaiting_student | in_review | done | unlocked
      created_at    TEXT NOT NULL,
      unlocked_at   TEXT
    );
  `);

  // --- Indexes. The partial unique index is load bearing: the database itself refuses a
  // second active venture. wip_lock is always 1, so at most one row may have stage='active'.
  db.exec(`
    CREATE UNIQUE INDEX idx_ventures_wip ON ventures(wip_lock) WHERE stage = 'active';
    CREATE INDEX idx_systems_track      ON systems(track_id);
    CREATE INDEX idx_experiments_system ON experiments(system_id);
    CREATE INDEX idx_errors_category    ON errors(category);
    CREATE INDEX idx_evidence_venture   ON evidence(venture_id);
    CREATE INDEX idx_frontier_track     ON frontier(affects_track_id);
    CREATE INDEX idx_builds_state       ON builds(state);
  `);
}

export function down(db: Database): void {
  db.exec(`
    DROP INDEX IF EXISTS idx_builds_state;
    DROP INDEX IF EXISTS idx_frontier_track;
    DROP INDEX IF EXISTS idx_evidence_venture;
    DROP INDEX IF EXISTS idx_errors_category;
    DROP INDEX IF EXISTS idx_experiments_system;
    DROP INDEX IF EXISTS idx_systems_track;
    DROP INDEX IF EXISTS idx_ventures_wip;
    DROP TABLE IF EXISTS builds;
    DROP TABLE IF EXISTS frontier;
    DROP TABLE IF EXISTS evidence;
    DROP TABLE IF EXISTS ventures;
    DROP TABLE IF EXISTS code_reviews;
    DROP TABLE IF EXISTS errors;
    DROP TABLE IF EXISTS experiments;
    DROP TABLE IF EXISTS systems;
    DROP TABLE IF EXISTS tracks;
    ALTER TABLE insights DROP COLUMN mode;
    ALTER TABLE skills   DROP COLUMN source;
    ALTER TABLE skills   DROP COLUMN track_id;
    ALTER TABLE lessons  DROP COLUMN student_wrote;
    ALTER TABLE lessons  DROP COLUMN hint_max_rung;
    ALTER TABLE lessons  DROP COLUMN track_id;
    ALTER TABLE lessons  DROP COLUMN depth;
    ALTER TABLE lessons  DROP COLUMN mode;
  `);
}
