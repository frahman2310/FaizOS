import Database from 'better-sqlite3';
import { skillsSeed } from './skills-seed.js';

export type DB = Database.Database;

const SCHEMA = `
CREATE TABLE IF NOT EXISTS skills (
  id            TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  phase         INTEGER NOT NULL,
  must_know     INTEGER NOT NULL DEFAULT 0,
  build_hint    TEXT DEFAULT '',
  mastery       REAL NOT NULL DEFAULT 0,
  confidence    REAL NOT NULL DEFAULT 0,
  last_seen     TEXT,
  on_curriculum INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS missions (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  title      TEXT NOT NULL,
  idea       TEXT DEFAULT '',
  repo_path  TEXT,
  status     TEXT NOT NULL DEFAULT 'active',   -- active | shipped | abandoned
  created_at TEXT NOT NULL,
  shipped_at TEXT,
  ship_url   TEXT
);
CREATE TABLE IF NOT EXISTS journey_log (
  id     INTEGER PRIMARY KEY AUTOINCREMENT,
  ts     TEXT NOT NULL,
  kind   TEXT NOT NULL,
  detail TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT
);
CREATE TABLE IF NOT EXISTS lessons (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  ts              TEXT NOT NULL,
  topic           TEXT NOT NULL,
  mission_id      INTEGER,
  skills          TEXT DEFAULT '[]',   -- JSON: skill ids touched
  struggles       TEXT DEFAULT '[]',   -- JSON: where he struggled
  worked          TEXT DEFAULT '[]',   -- JSON: what worked
  difficulty_felt TEXT                 -- too_easy | right | too_hard
);
CREATE TABLE IF NOT EXISTS insights (
  id     INTEGER PRIMARY KEY AUTOINCREMENT,
  ts     TEXT NOT NULL,
  note   TEXT NOT NULL UNIQUE,         -- deduped teaching insight
  weight INTEGER NOT NULL DEFAULT 1,   -- reinforced count
  active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS revisions (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  ts      TEXT NOT NULL,
  topic   TEXT NOT NULL,
  note_md TEXT NOT NULL                -- full revision-note markdown
);
`;

const DEFAULT_META: Record<string, string> = {
  streak: '0',
  best_streak: '0',
  last_active_date: '',
  current_mission_id: '',
  journey_repo: '',      // git remote URL for the private "journey" repo (empty = local commits only)
  github_user: '',
  projects_dir: 'projects',
};

export function openDb(path: string): DB {
  const db = new Database(path);
  db.pragma('journal_mode = WAL');
  db.exec(SCHEMA);

  const skillCount = (db.prepare('SELECT COUNT(*) c FROM skills').get() as { c: number }).c;
  if (skillCount === 0) {
    const ins = db.prepare('INSERT INTO skills (id,name,phase,must_know,build_hint) VALUES (?,?,?,?,?)');
    db.transaction(() => {
      for (const s of skillsSeed) ins.run(s.id, s.name, s.phase, s.must_know ? 1 : 0, s.build_hint);
    })();
  }
  const mIns = db.prepare('INSERT OR IGNORE INTO meta (key,value) VALUES (?,?)');
  for (const [k, v] of Object.entries(DEFAULT_META)) mIns.run(k, v);
  return db;
}

export function getMeta(db: DB, key: string): string {
  return (db.prepare('SELECT value FROM meta WHERE key=?').get(key) as { value: string } | undefined)?.value ?? '';
}
export function setMeta(db: DB, key: string, value: string): void {
  db.prepare('INSERT INTO meta (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run(key, value);
}
export function logEvent(db: DB, ts: string, kind: string, detail: string): void {
  db.prepare('INSERT INTO journey_log (ts,kind,detail) VALUES (?,?,?)').run(ts, kind, detail);
}
