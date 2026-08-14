// Phase 1 migration tests. Hermetic: builds a fresh seeded database in a temp directory,
// applies the migration there, and exercises the constraints. Never touches the live database.
import Database from 'better-sqlite3';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { openDb } from '../db.js';
import { migrateDown, migrateUp, migrationStatus } from '../migrate.js';

const V2_TABLES = [
  'tracks',
  'systems',
  'experiments',
  'errors',
  'code_reviews',
  'ventures',
  'evidence',
  'frontier',
  'builds',
];

let dir: string;
let dbPath: string;

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-migration-'));
  dbPath = join(dir, 'test.db');
  // openDb creates the v1 schema and seeds 66 skills + meta defaults, mirroring a real v1 db.
  const db = openDb(dbPath);
  db.prepare(
    "INSERT INTO lessons (ts, topic, skills) VALUES ('2026-01-01T00:00:00Z', 'pre-existing lesson', '[]')",
  ).run();
  db.close();
});

afterAll(() => {
  rmSync(dir, { recursive: true, force: true });
});

describe('migration 001', () => {
  it('applies cleanly and reports status', () => {
    const ran = migrateUp(dbPath);
    expect(ran).toEqual(['1 v2_schema']);
    const status = migrationStatus(dbPath);
    expect(status).toEqual([{ version: 1, name: 'v2_schema', applied: true }]);
  });

  it('creates every v2 table', () => {
    const db = new Database(dbPath, { readonly: true });
    const names = (
      db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>
    ).map((r) => r.name);
    db.close();
    for (const t of V2_TABLES) expect(names).toContain(t);
    expect(names).toContain('schema_migrations');
  });

  it('does not change pre-existing row counts', () => {
    const db = new Database(dbPath, { readonly: true });
    const skills = (db.prepare('SELECT COUNT(*) AS c FROM skills').get() as { c: number }).c;
    const lessons = (db.prepare('SELECT COUNT(*) AS c FROM lessons').get() as { c: number }).c;
    db.close();
    expect(skills).toBe(66);
    expect(lessons).toBe(1);
  });

  it('gives existing rows the new columns with correct defaults', () => {
    const db = new Database(dbPath, { readonly: true });
    const lesson = db
      .prepare('SELECT mode, depth, track_id, hint_max_rung, student_wrote FROM lessons LIMIT 1')
      .get() as { mode: string; depth: string; track_id: number | null; hint_max_rung: number; student_wrote: number };
    const skill = db.prepare('SELECT track_id, source FROM skills LIMIT 1').get() as {
      track_id: number | null;
      source: string;
    };
    db.close();
    expect(lesson).toEqual({ mode: 'course', depth: 'explain', track_id: null, hint_max_rung: 0, student_wrote: 1 });
    expect(skill).toEqual({ track_id: null, source: 'syllabus' });
  });

  it('physically rejects a second active venture and allows unlimited non-active ones', () => {
    const db = new Database(dbPath);
    db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('one', 'active', 'now')").run();
    expect(() =>
      db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('two', 'active', 'now')").run(),
    ).toThrow(/UNIQUE/);
    db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('three', 'candidate', 'now')").run();
    db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('four', 'parked', 'now')").run();
    db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('five', 'killed', 'now')").run();
    const total = (db.prepare('SELECT COUNT(*) AS c FROM ventures').get() as { c: number }).c;
    db.close();
    expect(total).toBe(4);
  });

  it('a parked venture can be re-activated once the slot is free', () => {
    const db = new Database(dbPath);
    db.prepare("UPDATE ventures SET stage = 'parked' WHERE title = 'one'").run();
    db.prepare("UPDATE ventures SET stage = 'active' WHERE title = 'three'").run();
    expect(() => db.prepare("UPDATE ventures SET stage = 'active' WHERE title = 'four'").run()).toThrow(/UNIQUE/);
    db.close();
  });

  it('down() reverts to the exact v1 surface and up() re-applies', () => {
    const reverted = migrateDown(dbPath);
    expect(reverted).toBe('1 v2_schema');
    const db = new Database(dbPath, { readonly: true });
    const names = (
      db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>
    ).map((r) => r.name);
    const lessonCols = (db.prepare('PRAGMA table_info(lessons)').all() as Array<{ name: string }>).map(
      (c) => c.name,
    );
    db.close();
    for (const t of V2_TABLES) expect(names).not.toContain(t);
    expect(lessonCols).toEqual(['id', 'ts', 'topic', 'mission_id', 'skills', 'struggles', 'worked', 'difficulty_felt']);
    expect(migrateUp(dbPath)).toEqual(['1 v2_schema']);
  });
});
