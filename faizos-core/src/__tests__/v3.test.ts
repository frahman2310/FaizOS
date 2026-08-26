// v3: the production spine, the per-domain guidance switch, the reveal step, the rebuild gate,
// modes, the OSS track and the cost drill. No network anywhere.
import Database from 'better-sqlite3';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { seedTracks } from '../backfill.js';
import { openDb } from '../db.js';
import { migrateUp } from '../migrate.js';
import { currentTrack, recordReview } from '../v2.js';
import {
  addOssTarget, completeRebuild, costDrillRecord, currentMode, guidanceFor, hasRevealed,
  markProvisional, ossStatus, P_SKILLS, P_TRACKS, rebuildsDue, recordReveal, scoreCostDrill,
  seedPSkills, seedPTracks, setMode, updateOssTarget, ventureNextBuild,
} from '../v3.js';

let dir: string;
let db: Database.Database;

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-v3-'));
  const dbPath = join(dir, 'test.db');
  openDb(dbPath).close();
  migrateUp(dbPath);
  db = new Database(dbPath);
  seedTracks(db);
  seedPTracks(db);
  seedPSkills(db);
});

afterAll(() => {
  db.close();
  rmSync(dir, { recursive: true, force: true });
});

describe('migration 002', () => {
  it('adds the v3 columns and tables without touching anything else', () => {
    const trackCols = (db.prepare('PRAGMA table_info(tracks)').all() as Array<{ name: string }>).map((c) => c.name);
    expect(trackCols).toContain('kind');
    expect(trackCols).toContain('guidance_policy');
    const buildCols = (db.prepare('PRAGMA table_info(builds)').all() as Array<{ name: string }>).map((c) => c.name);
    expect(buildCols).toEqual(expect.arrayContaining(['rebuild_due', 'reveal_notes', 'revealed_at']));
    const sysCols = (db.prepare('PRAGMA table_info(systems)').all() as Array<{ name: string }>).map((c) => c.name);
    expect(sysCols).toEqual(expect.arrayContaining(['p95_ms', 'cost_per_1k']));
    const tables = (db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>).map((t) => t.name);
    expect(tables).toEqual(expect.arrayContaining(['oss_targets', 'cost_drills']));
  });
});

describe('the production spine', () => {
  it('seeds 11 P-tracks and the production skills, idempotently', () => {
    expect(P_TRACKS).toHaveLength(11);
    expect(seedPTracks(db)).toBe(0); // already seeded in beforeAll
    expect(seedPSkills(db)).toBe(0);
    const kinds = db.prepare('SELECT kind, COUNT(*) c FROM tracks GROUP BY kind').all() as Array<{ kind: string; c: number }>;
    const byKind = Object.fromEntries(kinds.map((k) => [k.kind, k.c]));
    expect(byKind.production).toBe(10);
    expect(byKind.ship).toBe(1);
    expect(byKind.ml).toBe(11);
    const pSkills = (db.prepare("SELECT COUNT(*) c FROM skills WHERE source = 'v3-production'").get() as { c: number }).c;
    expect(pSkills).toBe(P_SKILLS.length);
  });

  it('makes the production spine outrank the ML tracks', () => {
    // deployment is 78.3% of postings; self-hosting is 2.5%. P0 must come before T0.
    expect(currentTrack(db)?.code).toBe('P0');
  });

  it('gives every production skill a track and a real hint', () => {
    const orphans = P_SKILLS.filter((s) => !P_TRACKS.some((t) => t.code === s.track));
    expect(orphans).toEqual([]);
    expect(P_SKILLS.every((s) => s.hint.length > 10)).toBe(true);
  });
});

describe('the per-domain guidance switch', () => {
  let mlBuild: number;
  let prodBuild: number;

  beforeAll(() => {
    const t3 = (db.prepare("SELECT id FROM tracks WHERE code = 'T3'").get() as { id: number }).id;
    const p1 = (db.prepare("SELECT id FROM tracks WHERE code = 'P1'").get() as { id: number }).id;
    const mk = (trackId: number, path: string): number => {
      const l = db.prepare("INSERT INTO lessons (ts, topic, skills, struggles, worked, track_id) VALUES ('now','t','[]','[]','[]',?)").run(trackId);
      return Number(
        db.prepare("INSERT INTO builds (lesson_id, solution_path, state, created_at) VALUES (?, ?, 'awaiting_student', 'now')")
          .run(Number(l.lastInsertRowid), path).lastInsertRowid,
      );
    };
    mlBuild = mk(t3, 'projects/ml/attn.py');
    prodBuild = mk(p1, 'src/service/main.py');
  });

  it('keeps the guard ON where he is already expert', () => {
    const g = guidanceFor(db, mlBuild);
    expect(g.policy).toBe('write_from_empty');
    expect(g.guard_active).toBe(true);
    expect(g.track_code).toBe('T3');
  });

  it('stands the guard DOWN where he is a novice', () => {
    // Expertise reversal: worked examples beat blank pages for novices and reverse for experts.
    const g = guidanceFor(db, prodBuild);
    expect(g.policy).toBe('worked_example_first');
    expect(g.guard_active).toBe(false);
    expect(g.reason).toContain('novice');
  });

  it('defaults to write_from_empty when a build has no track', () => {
    const id = Number(
      db.prepare("INSERT INTO builds (solution_path, state, created_at) VALUES ('x.py','awaiting_student','now')").run().lastInsertRowid,
    );
    expect(guidanceFor(db, id).policy).toBe('write_from_empty');
  });
});

describe('reveal and contrast', () => {
  let build: number;
  beforeAll(() => {
    build = Number(
      db.prepare("INSERT INTO builds (solution_path, state, created_at) VALUES ('r.py','in_review','now')").run().lastInsertRowid,
    );
  });

  it('refuses an empty reveal, because the contrast IS the step', () => {
    expect(recordReveal(db, build, '   ').recorded).toBe(false);
    expect(hasRevealed(db, build)).toBe(false);
  });

  it('records the diff and unblocks review', () => {
    const r = recordReveal(db, build, 'I mutated in place; the reference returned a new list.');
    expect(r.recorded).toBe(true);
    expect(hasRevealed(db, build)).toBe(true);
  });

  it('review lands the build in provisional, never done', () => {
    const res = recordReview(db, { build_id: build, student_code: 'x = 1' });
    expect(res.state).toBe('provisional');
    expect(res.rebuild_due).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    const state = (db.prepare('SELECT state FROM builds WHERE id = ?').get(build) as { state: string }).state;
    expect(state).toBe('provisional');
  });
});

describe('the delayed unaided rebuild', () => {
  let build: number;
  beforeAll(() => {
    build = Number(
      db.prepare("INSERT INTO builds (solution_path, state, created_at) VALUES ('d.py','in_review','now')").run().lastInsertRowid,
    );
    markProvisional(db, build);
  });

  it('does not come due before the delay', () => {
    expect(rebuildsDue(db).map((r) => r.id)).not.toContain(build);
  });

  it('comes due once the date passes', () => {
    db.prepare("UPDATE builds SET rebuild_due = '2020-01-01' WHERE id = ?").run(build);
    expect(rebuildsDue(db).map((r) => r.id)).toContain(build);
  });

  it('needing help reschedules instead of completing', () => {
    // 3 of 9 students who succeeded on the day failed two weeks later. Same-day success is not evidence.
    const r = completeRebuild(db, build, false);
    expect(r.state).toBe('provisional');
    expect(rebuildsDue(db).map((r2) => r2.id)).not.toContain(build);
  });

  it('an unaided rebuild is the only thing that marks it done', () => {
    db.prepare("UPDATE builds SET rebuild_due = '2020-01-01' WHERE id = ?").run(build);
    expect(completeRebuild(db, build, true).state).toBe('done');
    expect(completeRebuild(db, build, true).state).toBe('done'); // already done, refuses politely
  });
});

describe('modes', () => {
  it('holds course mode while the spine is unfinished', () => {
    const m = currentMode(db);
    expect(m.mode).toBe('course');
    expect(m.next_track).toBe('P0');
    expect(m.reason).toContain('spine');
  });

  it('hands over to the venture once the spine is done and one is active', () => {
    db.prepare("UPDATE tracks SET status = 'complete' WHERE kind = 'production' AND position <= 7").run();
    db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('Test venture', 'active', 'now')").run();
    const m = currentMode(db);
    expect(m.mode).toBe('venture');
    expect(m.reason).toContain('Test venture');
  });

  it('free mode is explicit and overrides', () => {
    setMode(db, 'free');
    expect(currentMode(db).mode).toBe('free');
    setMode(db, 'course');
  });

  it('venture mode picks the intersection of venture need and weakness', () => {
    db.prepare("UPDATE skills SET mastery = 0.9 WHERE id = 'tool-design'").run();
    db.prepare("UPDATE skills SET mastery = 0.1 WHERE id = 'hybrid-retrieval'").run();
    const picks = ventureNextBuild(db, ['tool-design', 'hybrid-retrieval']);
    expect(picks[0]?.id).toBe('hybrid-retrieval'); // weakest of what the venture needs, first
  });
});

describe('the OSS track', () => {
  it('records a target and closes rung 6 on merge', () => {
    const id = addOssTarget(db, { repo: 'vllm-project/vllm', issue_url: 'https://github.com/vllm-project/vllm/issues/1', issue_title: 'fix docstring' });
    expect(updateOssTarget(db, id, { state: 'pr_open', pr_url: 'https://github.com/vllm-project/vllm/pull/2', review_cycles: 2 }).ok).toBe(true);
    const merged = updateOssTarget(db, id, { state: 'merged', pr_url: 'https://github.com/vllm-project/vllm/pull/2' });
    expect(merged.reason).toContain('rung 6');
    const row = db.prepare("SELECT title, kind, status FROM systems WHERE title = 'PR: vllm-project/vllm'").get() as { title: string; kind: string; status: string };
    expect(row.kind).toBe('product');
    expect(row.status).toBe('shipped');
  });

  it('reports the measured repo guidance, traps included', () => {
    const st = ossStatus(db);
    expect(st.merged).toBe(1);
    const trl = st.repos.find((r) => r.repo === 'huggingface/trl');
    expect(trl?.verdict).toContain('TRAP');
    const vllm = st.repos.find((r) => r.repo === 'vllm-project/vllm');
    expect(vllm?.verdict).toContain('Best target');
  });
});

describe('the cost drill', () => {
  it('accepts an answer within 20% and rejects one outside', () => {
    expect(scoreCostDrill(db, '100k users', { usd_per_day: 13000 }, { usd_per_day: 12000 }).correct).toBe(true);
    const off = scoreCostDrill(db, '100k users', { usd_per_day: 13000 }, { usd_per_day: 2000 });
    expect(off.correct).toBe(false);
    expect(off.off_by_ratio).toBeLessThan(0.5);
  });

  it('treats a missing number as the failure mode it is', () => {
    const none = scoreCostDrill(db, 'no number', { usd_per_day: 100 }, {});
    expect(none.correct).toBe(false);
    expect(none.reason).toContain('without a number');
  });

  it('keeps the running record', () => {
    const rec = costDrillRecord(db);
    expect(rec.attempts).toBe(3);
    expect(rec.correct).toBe(1);
  });
});

describe('the teaching feedback loop', () => {
  it('refuses an insight too short to teach anything next session', async () => {
    const { recordInsight } = await import('../v3.js');
    expect(recordInsight(db, 'too short').recorded).toBe(false);
  });

  it('records an insight and reinforces it on a repeat', async () => {
    const { recordInsight } = await import('../v3.js');
    const note = 'He has zero Python experience, so teach the grammar of a line alongside the topic.';
    expect(recordInsight(db, note, 3).recorded).toBe(true);
    recordInsight(db, note, 3);
    const row = db.prepare('SELECT weight FROM insights WHERE note = ?').get(note) as { weight: number };
    expect(row.weight).toBe(4); // deduped on the text, weight raised
  });

  it('reports a gap when the newest lesson is newer than the newest insight', async () => {
    const { insightGap } = await import('../v3.js');
    db.prepare("INSERT INTO lessons (ts, topic, skills, struggles, worked) VALUES ('2099-01-01T00:00:00Z','future','[]','[]','[]')").run();
    expect(insightGap(db).gap).toBe(true);   // a lesson ran and nothing was learned about teaching it
  });
});
