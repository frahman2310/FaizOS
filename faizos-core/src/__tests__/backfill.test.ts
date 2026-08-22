// Phase 2 backfill tests. Hermetic half: run the backfill against a fresh migrated temp
// database with synthetic missions and lessons. Live half: read only assertions that the real
// database ended up in the expected state.
import Database from 'better-sqlite3';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import {
  backfillSystems,
  ERROR_SEEDS,
  mapLessonTracks,
  mapSkillTracks,
  seedErrors,
  seedTracks,
  SKILL_TRACK,
  TRACKS,
} from '../backfill.js';
import { openDb } from '../db.js';
import { migrateUp } from '../migrate.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const LIVE = join(HERE, '..', '..', 'data', 'faiz.db');

let dir: string;
let dbPath: string;

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-backfill-'));
  dbPath = join(dir, 'test.db');
  const db = openDb(dbPath); // v1 schema + 66 seeded skills
  db.prepare(
    "INSERT INTO missions (title, idea, repo_path, status, created_at, shipped_at, ship_url) VALUES ('m1', '', 'projects/m1', 'shipped', '2026-01-01', '2026-01-02', 'https://example.test/m1')",
  ).run();
  db.prepare(
    "INSERT INTO lessons (ts, topic, mission_id, skills) VALUES ('2026-01-02', 'l1', 1, '[\"attention\"]')",
  ).run();
  db.prepare("INSERT INTO lessons (ts, topic, skills) VALUES ('2026-01-03', 'no-skill lesson', '[]')").run();
  db.close();
  migrateUp(dbPath);
});

afterAll(() => {
  rmSync(dir, { recursive: true, force: true });
});

describe('backfill on a fresh migrated database', () => {
  it('mapping covers exactly the 66 curriculum skills, no dangling entries', () => {
    expect(Object.keys(SKILL_TRACK)).toHaveLength(66);
    const codes = new Set(TRACKS.map((t) => t.code));
    for (const code of Object.values(SKILL_TRACK)) expect(codes).toContain(code);
  });

  it('seeds 11 tracks idempotently', () => {
    const db = new Database(dbPath);
    expect(seedTracks(db)).toBe(11);
    expect(seedTracks(db)).toBe(0); // second run adds nothing
    const c = (db.prepare("SELECT COUNT(*) AS c FROM tracks WHERE code LIKE 'T%'").get() as { c: number }).c;
    db.close();
    expect(c).toBe(11);
  });

  it('maps every seeded skill and reports nothing unmapped', () => {
    const db = new Database(dbPath);
    const r = mapSkillTracks(db);
    const unmappedCount = (db.prepare('SELECT COUNT(*) AS c FROM skills WHERE track_id IS NULL').get() as { c: number }).c;
    db.close();
    expect(r.mapped).toBe(66);
    expect(r.unmappedSkillIds).toHaveLength(0);
    expect(r.danglingMappings).toHaveLength(0);
    expect(unmappedCount).toBe(0);
  });

  it('maps lessons from their first mappable skill and leaves skill-less lessons NULL', () => {
    const db = new Database(dbPath);
    const r = mapLessonTracks(db);
    const l1 = db.prepare("SELECT track_id FROM lessons WHERE topic = 'l1'").get() as { track_id: number | null };
    const t3 = db.prepare("SELECT id FROM tracks WHERE code = 'T3'").get() as { id: number };
    const noSkill = db.prepare("SELECT track_id FROM lessons WHERE topic = 'no-skill lesson'").get() as {
      track_id: number | null;
    };
    db.close();
    expect(r.mapped).toBe(1);
    expect(r.unmapped).toBe(1);
    expect(l1.track_id).toBe(t3.id); // 'attention' maps to T3
    expect(noSkill.track_id).toBeNull();
  });

  it('backfills missions to study systems truthfully and idempotently', () => {
    const db = new Database(dbPath);
    expect(backfillSystems(db)).toBe(1);
    expect(backfillSystems(db)).toBe(0); // idempotent
    const s = db.prepare('SELECT title, kind, status, metric_name, metric_value, repo_url FROM systems').get() as {
      title: string;
      kind: string;
      status: string;
      metric_name: string | null;
      metric_value: number | null;
      repo_url: string;
    };
    db.close();
    expect(s.kind).toBe('study');
    expect(s.status).toBe('shipped');
    expect(s.metric_name).toBeNull(); // no invented metrics
    expect(s.metric_value).toBeNull();
    expect(s.repo_url).toBe('https://example.test/m1'); // ship_url preferred over repo_path
  });

  it('seeds the error taxonomy idempotently', () => {
    const db = new Database(dbPath);
    expect(seedErrors(db)).toBe(ERROR_SEEDS.length);
    expect(seedErrors(db)).toBe(0);
    const cats = (db.prepare('SELECT category FROM errors ORDER BY category').all() as Array<{ category: string }>).map(
      (r) => r.category,
    );
    db.close();
    expect(cats).toContain('ordering-pairing'); // the user-approved added category
    expect(cats).toHaveLength(ERROR_SEEDS.length);
  });
});

describe('live database backfill state (read only)', () => {
  it('has 11 tracks, 66 mapped skills, 44 study systems, 8 error seeds', () => {
    const db = new Database(LIVE, { readonly: true, fileMustExist: true });
    const tracks = (db.prepare("SELECT COUNT(*) AS c FROM tracks WHERE code LIKE 'T%'").get() as { c: number }).c;
    const skills = (db.prepare("SELECT COUNT(*) AS c FROM skills WHERE track_id IS NOT NULL AND source = 'syllabus'").get() as { c: number }).c;
    const systems = (db.prepare("SELECT COUNT(*) AS c FROM systems WHERE kind = 'study'").get() as { c: number }).c;
    const errors = (db.prepare('SELECT COUNT(*) AS c FROM errors WHERE lesson_id IS NULL').get() as { c: number }).c;
    const noMetric = (
      db.prepare("SELECT COUNT(*) AS c FROM systems WHERE kind = 'study' AND metric_value IS NOT NULL").get() as {
        c: number;
      }
    ).c;
    db.close();
    expect(tracks).toBe(11);
    expect(skills).toBe(66);
    expect(systems).toBe(44);
    expect(errors).toBe(8);
    expect(noMetric).toBe(0); // study builds never carry invented metrics
  });
});
