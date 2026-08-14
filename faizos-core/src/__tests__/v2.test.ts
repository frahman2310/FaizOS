// Phase 3 tests: the v2 helper logic behind every new MCP tool, on a hermetic migrated database.
import Database from 'better-sqlite3';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { seedErrors, seedTracks } from '../backfill.js';
import { openDb } from '../db.js';
import { migrateUp } from '../migrate.js';
import {
  activeBuild, activeVenture, currentTrack, grantHint, logExperiment, recordErrors,
  recordReview, specBuild, studentWroteRatio, topOpenErrors, trackStatus, unlockBuild,
} from '../v2.js';

let dir: string;
let dbPath: string;
let db: Database.Database;

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-v2-'));
  dbPath = join(dir, 'test.db');
  openDb(dbPath).close();
  migrateUp(dbPath);
  db = new Database(dbPath);
  seedTracks(db);
  seedErrors(db);
});

afterAll(() => {
  db.close();
  rmSync(dir, { recursive: true, force: true });
});

describe('spec_build and the build lifecycle', () => {
  it('creates a lesson and an awaiting_student build with derived paths', () => {
    const r = specBuild(db, { topic: 'Rotary embeddings from empty', mode: 'course', depth: 'explain', track_code: 'T3' });
    expect(r.solution_path).toBe('projects/rotary-embeddings-from-empty/rotary_embeddings_from_empty.py');
    expect(r.test_path).toBe('projects/rotary-embeddings-from-empty/test_rotary_embeddings_from_empty.py');
    expect(r.track).toEqual({ code: 'T3', title: 'Modern architecture, as of 2026' });
    expect(r.open_error_categories.length).toBeGreaterThan(0);
    const b = activeBuild(db);
    expect(b?.id).toBe(r.build_id);
    expect(b?.state).toBe('awaiting_student');
    const lesson = db.prepare('SELECT mode, depth, track_id FROM lessons WHERE id = ?').get(r.lesson_id) as {
      mode: string; depth: string; track_id: number;
    };
    expect(lesson.mode).toBe('course');
    expect(lesson.depth).toBe('explain');
  });

  it('review records the three passes, classifies errors, and closes the build', () => {
    const b = activeBuild(db);
    expect(b).not.toBeNull();
    const before = topOpenErrors(db, 10).find((e) => e.category === 'off-by-one')?.occurrences ?? 0;
    const r = recordReview(db, {
      build_id: b!.id,
      student_code: 'def rotate(v, angle): ...',
      reference_code: 'def rotate(vec, angle): ...',
      diff_summary: 'one correctness difference, two taste differences',
      correctness_diffs: ['loop stop excluded the final pair'],
      taste_diffs: ['shorter parameter names', 'inline the helper'],
      errors: [{ category: 'off-by-one', description: 'range stop excluded the final pair', rule_broken: 'the stop value is always excluded' }],
    });
    expect(r.errors_recorded).toBe(1);
    const after = topOpenErrors(db, 10).find((e) => e.category === 'off-by-one')?.occurrences ?? 0;
    expect(after).toBe(before + 1); // aggregate incremented, no duplicate rows
    expect(activeBuild(db)).toBeNull(); // build is done
    const review = db.prepare('SELECT correctness_diffs FROM code_reviews WHERE id = ?').get(r.review_id) as {
      correctness_diffs: string;
    };
    expect(JSON.parse(review.correctness_diffs)).toHaveLength(1);
  });

  it('a brand new error category inserts as its own aggregate row', () => {
    const n = recordErrors(db, [{ category: 'broadcasting', description: 'first broadcasting slip', rule_broken: 'trailing dims align' }]);
    expect(n).toBe(1);
    const row = db.prepare("SELECT occurrences FROM errors WHERE category = 'broadcasting'").get() as { occurrences: number };
    expect(row.occurrences).toBe(1);
  });
});

describe('hint ladder', () => {
  let buildId: number;
  beforeAll(() => {
    const r = specBuild(db, { topic: 'hint ladder build' });
    buildId = r.build_id;
  });

  it('serves rungs strictly in order and refuses skips', () => {
    expect(grantHint(db, buildId, 3).granted).toBe(false); // skip refused
    expect(grantHint(db, buildId, 1).granted).toBe(true);
    expect(grantHint(db, buildId, 3).granted).toBe(false); // still refuses skipping 2
    expect(grantHint(db, buildId, 2).granted).toBe(true);
    expect(grantHint(db, buildId, 1).granted).toBe(true); // re-serving an earned rung is fine
    expect(grantHint(db, buildId, 4).granted).toBe(false); // rung 4 only after 3
    expect(grantHint(db, buildId, 3).granted).toBe(true);
    expect(grantHint(db, buildId, 4).granted).toBe(true);
  });

  it('records the deepest rung on the lesson', () => {
    const lesson = db.prepare('SELECT hint_max_rung FROM lessons ORDER BY id DESC LIMIT 1').get() as {
      hint_max_rung: number;
    };
    expect(lesson.hint_max_rung).toBe(4);
  });

  it('unlock marks the build and the lesson honestly', () => {
    const u = unlockBuild(db, buildId);
    expect(u.unlocked).toBe(true);
    const b = db.prepare('SELECT state, unlocked_at FROM builds WHERE id = ?').get(buildId) as {
      state: string; unlocked_at: string | null;
    };
    expect(b.state).toBe('unlocked');
    expect(b.unlocked_at).not.toBeNull();
    const lesson = db.prepare('SELECT student_wrote FROM lessons ORDER BY id DESC LIMIT 1').get() as {
      student_wrote: number;
    };
    expect(lesson.student_wrote).toBe(0);
    const ratio = studentWroteRatio(db);
    expect(ratio.unlocked).toBe(1);
    expect(ratio.written).toBe(1); // the reviewed build from the earlier test
  });
});

describe('experiments', () => {
  let systemId: number;
  beforeAll(() => {
    const info = db
      .prepare("INSERT INTO systems (title, kind, status, created_at) VALUES ('nanogpt run', 'trained_model', 'planned', 'now')")
      .run();
    systemId = Number(info.lastInsertRowid);
  });

  it('returns no spread below three runs, then mean/min/max/spread at three', () => {
    const a = logExperiment(db, { system_id: systemId, metric_name: 'val_loss', metric_value: 3.31, seed: 1 });
    expect(a.seed_spread).toBeNull();
    const b = logExperiment(db, { system_id: systemId, metric_name: 'val_loss', metric_value: 3.28, seed: 2 });
    expect(b.seed_spread).toBeNull();
    const c = logExperiment(db, { system_id: systemId, metric_name: 'val_loss', metric_value: 3.34, seed: 3 });
    expect(c.seed_spread).not.toBeNull();
    expect(c.seed_spread!.n).toBe(3);
    expect(c.seed_spread!.min).toBeCloseTo(3.28);
    expect(c.seed_spread!.max).toBeCloseTo(3.34);
    expect(c.seed_spread!.spread).toBeCloseTo(0.06);
  });
});

describe('tracks and ventures', () => {
  it('currentTrack is T0 while nothing is active', () => {
    expect(currentTrack(db)?.code).toBe('T0');
  });

  it('an active track wins over pending order', () => {
    db.prepare("UPDATE tracks SET status = 'active' WHERE code = 'T1'").run();
    expect(currentTrack(db)?.code).toBe('T1');
    db.prepare("UPDATE tracks SET status = 'pending' WHERE code = 'T1'").run();
  });

  it('trackStatus aggregates systems, skills and frontier notes', () => {
    const t3 = db.prepare("SELECT id FROM tracks WHERE code = 'T3'").get() as { id: number };
    db.prepare(
      "INSERT INTO frontier (area, title, url, summary, affects_track_id, ingested_at) VALUES ('attention', 'the consensus collapsed', 'https://example.test', 's', ?, 'now')",
    ).run(t3.id);
    const s = trackStatus(db, 'T3');
    expect(s).not.toBeNull();
    expect(s!.frontier_notes).toHaveLength(1);
    expect(s!.track.completion_test.length).toBeGreaterThan(0);
  });

  it('activeVenture reflects the single active row', () => {
    expect(activeVenture(db)).toBeNull();
    db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('test venture', 'active', 'now')").run();
    expect(activeVenture(db)?.title).toBe('test venture');
    db.prepare("UPDATE ventures SET stage = 'killed' WHERE title = 'test venture'").run();
  });
});
