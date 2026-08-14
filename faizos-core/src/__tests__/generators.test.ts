// Phase 5 tests: the artefact generators, hermetic. The capstone scorer is the important one:
// it must never award a rung without backing rows, and must award one the moment rows exist.
import Database from 'better-sqlite3';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { seedErrors, seedTracks } from '../backfill.js';
import { openDb } from '../db.js';
import {
  renderCapstone, renderErrors, renderExperiments, renderFrontier, renderVentures, scoreCapstone,
} from '../generators.js';
import { migrateUp } from '../migrate.js';
import { logExperiment } from '../v2.js';

let dir: string;
let db: Database.Database;

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-gen-'));
  const dbPath = join(dir, 'test.db');
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

describe('capstone auto scoring', () => {
  it('starts with everything missing on an empty systems table', () => {
    const rungs = scoreCapstone(db);
    expect(rungs).toHaveLength(8);
    expect(rungs.every((r) => r.status === 'MISSING')).toBe(true);
  });

  it('rung 1 turns solid only at 20 study systems', () => {
    const ins = db.prepare("INSERT INTO systems (title, kind, status, created_at) VALUES (?, 'study', 'shipped', 'now')");
    for (let i = 0; i < 19; i++) ins.run(`study ${i}`);
    expect(scoreCapstone(db).find((r) => r.rung === 1)?.status).toBe('PARTIAL');
    ins.run('study 19');
    expect(scoreCapstone(db).find((r) => r.rung === 1)?.status).toBe('SOLID');
  });

  it('rung 3 needs a metric AND three seeds; rung 5 needs the mean inside the spread', () => {
    const info = db.prepare(
      "INSERT INTO systems (title, kind, status, metric_name, metric_value, baseline_value, created_at) VALUES ('nanochat speedrun', 'trained_model', 'shipped', 'CORE', 0.255, 0.256, 'now')",
    ).run();
    const sysId = Number(info.lastInsertRowid);
    expect(scoreCapstone(db).find((r) => r.rung === 3)?.status).toBe('PARTIAL'); // metric, no seeds
    logExperiment(db, { system_id: sysId, metric_name: 'CORE', metric_value: 0.254, seed: 1 });
    logExperiment(db, { system_id: sysId, metric_name: 'CORE', metric_value: 0.256, seed: 2 });
    logExperiment(db, { system_id: sysId, metric_name: 'CORE', metric_value: 0.257, seed: 3 });
    const after = scoreCapstone(db);
    expect(after.find((r) => r.rung === 3)?.status).toBe('SOLID');
    // mean 0.2557, spread 0.003, |mean - 0.256| = 0.0003 <= spread: a reproduction within noise
    expect(after.find((r) => r.rung === 5)?.status).toBe('SOLID');
    // CORE is an eval-family metric, so rung 7 rides on the same honest rows
    expect(after.find((r) => r.rung === 7)?.status).toBe('SOLID');
  });

  it('rung 4 needs a kernel beating its baseline; rung 6 needs a merged PR row', () => {
    expect(scoreCapstone(db).find((r) => r.rung === 4)?.status).toBe('MISSING');
    db.prepare(
      "INSERT INTO systems (title, kind, status, metric_name, metric_value, baseline_value, created_at) VALUES ('fused softmax', 'kernel', 'shipped', 'tokens_per_sec', 1500, 1200, 'now')",
    ).run();
    expect(scoreCapstone(db).find((r) => r.rung === 4)?.status).toBe('SOLID');
    expect(scoreCapstone(db).find((r) => r.rung === 6)?.status).toBe('MISSING');
    db.prepare(
      "INSERT INTO systems (title, kind, status, repo_url, created_at) VALUES ('PR: vllm-project/vllm docstring fix', 'study', 'shipped', 'https://github.com/vllm-project/vllm/pull/1', 'now')",
    ).run();
    expect(scoreCapstone(db).find((r) => r.rung === 6)?.status).toBe('SOLID');
  });

  it('rungs 2 and 8: a product, then a product with a number', () => {
    db.prepare(
      "INSERT INTO systems (title, kind, status, repo_url, created_at) VALUES ('FaizOS', 'product', 'shipped', 'https://github.com/frahman2310/FaizOS', 'now')",
    ).run();
    let rungs = scoreCapstone(db);
    expect(rungs.find((r) => r.rung === 2)?.status).toBe('SOLID');
    expect(rungs.find((r) => r.rung === 8)?.status).toBe('PARTIAL'); // product, no metric
    db.prepare("UPDATE systems SET metric_name = 'users', metric_value = 1 WHERE title = 'FaizOS'").run();
    rungs = scoreCapstone(db);
    expect(rungs.find((r) => r.rung === 8)?.status).toBe('SOLID');
  });
});

describe('the other generators render without a model in the loop', () => {
  it('experiments includes spread and the noise verdict', () => {
    const md = renderExperiments(db);
    expect(md).toContain('Seed spread for CORE');
    expect(md).toContain('baseline');
  });

  it('errors renders open categories ranked', () => {
    const md = renderErrors(db);
    expect(md).toContain('ordering-pairing');
    expect(md).toContain('| category | occurrences |');
  });

  it('ventures renders the WIP statement even when empty', () => {
    const md = renderVentures(db);
    expect(md).toContain('limit 1, database enforced');
  });

  it('frontier renders every track section', () => {
    const md = renderFrontier(db);
    expect(md).toContain('## T0 ');
    expect(md).toContain('## T10 ');
  });

  it('capstone prints its own scoring rules', () => {
    const md = renderCapstone(db);
    expect(md).toContain('Scoring rule:');
    expect(md).toContain('auto scored');
  });
});
