// The contract's Phase 3 requirement: "Test it by actually attempting a blocked write and
// asserting the failure." These tests pipe real PreToolUse JSON through the real hook script
// against a hermetic database and assert the deny decision, plus every allow case.
import Database from 'better-sqlite3';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { openDb } from '../db.js';
import { migrateUp } from '../migrate.js';
import { specBuild, unlockBuild } from '../v2.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(HERE, '..', '..', '..');
const GUARD = join(REPO_ROOT, 'hooks', 'pre-tool-guard.sh');

let dir: string;
let dbPath: string;
let solutionAbs: string;
let buildId: number;

function runGuard(input: object): string {
  return execFileSync('bash', [GUARD], {
    input: JSON.stringify(input),
    env: { ...process.env, FAIZOS_GUARD_DB: dbPath },
    encoding: 'utf8',
  });
}

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-guard-'));
  dbPath = join(dir, 'test.db');
  openDb(dbPath).close();
  migrateUp(dbPath);
  const db = new Database(dbPath);
  const r = specBuild(db, { topic: 'guard target build' });
  buildId = r.build_id;
  solutionAbs = join(REPO_ROOT, r.solution_path);
  db.close();
});

afterAll(() => {
  rmSync(dir, { recursive: true, force: true });
});

describe('PreToolUse write guard', () => {
  it('DENIES a Write to the awaiting_student solution path', () => {
    const out = runGuard({ tool_name: 'Write', tool_input: { file_path: solutionAbs } });
    expect(out).toContain('"permissionDecision":"deny"');
    expect(out).toContain('/faiz-hint');
    expect(out).toContain('/faiz-unlock');
  });

  it('DENIES an Edit to the same path', () => {
    const out = runGuard({ tool_name: 'Edit', tool_input: { file_path: solutionAbs } });
    expect(out).toContain('"permissionDecision":"deny"');
  });

  it('allows writes to any other path, including the test file', () => {
    const testFile = solutionAbs.replace(/([^/]+)\.py$/, 'test_$1.py');
    expect(runGuard({ tool_name: 'Write', tool_input: { file_path: testFile } })).toBe('');
    expect(runGuard({ tool_name: 'Write', tool_input: { file_path: join(REPO_ROOT, 'README.md') } })).toBe('');
  });

  it('ignores non-write tools', () => {
    expect(runGuard({ tool_name: 'Read', tool_input: { file_path: solutionAbs } })).toBe('');
  });

  it('stands down after /faiz-unlock', () => {
    const db = new Database(dbPath);
    unlockBuild(db, buildId);
    db.close();
    expect(runGuard({ tool_name: 'Write', tool_input: { file_path: solutionAbs } })).toBe('');
  });

  it('stands down on a production track, where he is a novice', () => {
    // Expertise reversal: worked examples beat blank pages for novices and reverse for experts.
    // Blocking a P-track write would produce failure he cannot learn from, so the guard reads
    // the policy off the track instead of firing unconditionally.
    const db = new Database(dbPath);
    db.prepare("INSERT INTO tracks (code, title, position, prereq_codes, completion_test, kind, guidance_policy) VALUES ('P1x','Async and FastAPI',1,'[]','','production','worked_example_first')").run();
    const trackId = (db.prepare("SELECT id FROM tracks WHERE code = 'P1x'").get() as { id: number }).id;
    const lesson = db.prepare("INSERT INTO lessons (ts, topic, skills, struggles, worked, track_id) VALUES ('now','svc','[]','[]','[]',?)").run(trackId);
    const prodPath = 'projects/service/main.py';
    db.prepare("INSERT INTO builds (lesson_id, solution_path, state, created_at) VALUES (?, ?, 'awaiting_student', 'now')")
      .run(Number(lesson.lastInsertRowid), prodPath);
    db.close();
    // newest awaiting_student build wins, and its policy is worked_example_first
    expect(runGuard({ tool_name: 'Write', tool_input: { file_path: join(REPO_ROOT, prodPath) } })).toBe('');
  });

  it('fails open on malformed input', () => {
    const out = execFileSync('bash', [GUARD], {
      input: 'not json at all',
      env: { ...process.env, FAIZOS_GUARD_DB: dbPath },
      encoding: 'utf8',
    });
    expect(out).toBe('');
  });
});
