// Phase 7 tests. Zero network: fetchFrontier runs against a fixture Atom feed.
import Database from 'better-sqlite3';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { seedTracks } from '../backfill.js';
import { openDb } from '../db.js';
import { driftedTracks, fetchFrontier, FRONTIER_SEEDS, seedFrontier } from '../frontier.js';
import { migrateUp } from '../migrate.js';
import type { FetchLike } from '../venture.js';

let dir: string;
let db: Database.Database;

const FEED =
  '<feed><entry><id>http://arxiv.org/abs/2608.001</id><title>A new attention variant</title><summary>we vary attention</summary></entry>' +
  '<entry><id>http://arxiv.org/abs/2608.002</id><title>Sparse experts revisited</title><summary>sparser is better</summary></entry></feed>';

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-frontier-'));
  const dbPath = join(dir, 'test.db');
  openDb(dbPath).close();
  migrateUp(dbPath);
  db = new Database(dbPath);
  seedTracks(db);
});

afterAll(() => {
  db.close();
  rmSync(dir, { recursive: true, force: true });
});

describe('spec section 6 seeds', () => {
  it('seeds one row per subsection, idempotently, with resolved track ids', () => {
    expect(FRONTIER_SEEDS).toHaveLength(10);
    expect(seedFrontier(db)).toBe(10);
    expect(seedFrontier(db)).toBe(0);
    const t3 = db.prepare("SELECT id FROM tracks WHERE code = 'T3'").get() as { id: number };
    const attention = db.prepare("SELECT affects_track_id FROM frontier WHERE area = '6.1'").get() as { affects_track_id: number };
    expect(attention.affects_track_id).toBe(t3.id);
    const publishes = db.prepare("SELECT affects_track_id FROM frontier WHERE area = '6.10'").get() as { affects_track_id: number | null };
    expect(publishes.affects_track_id).toBeNull();
  });
});

describe('weekly fetch, fully mocked', () => {
  it('fetches for the current and next track, dedupes, and records failures', async () => {
    const mockFetch: FetchLike = async () => ({ ok: true, status: 200, text: async () => FEED });
    const r1 = await fetchFrontier(db, mockFetch, 0);
    // two target tracks, same fixture feed, dedup on url+title: first track inserts 2, second 0
    expect(r1.inserted).toBe(2);
    expect(Object.keys(r1.perTrack)).toHaveLength(2);
    const r2 = await fetchFrontier(db, mockFetch, 0);
    expect(r2.inserted).toBe(0);
    const failing: FetchLike = async () => ({ ok: false, status: 500, text: async () => 'boom' });
    const r3 = await fetchFrontier(db, failing, 0);
    expect(r3.inserted).toBe(0);
    expect(Object.keys(r3.failures)).toHaveLength(2);
    const row = db.prepare("SELECT area, summary FROM frontier WHERE title = 'A new attention variant'").get() as { area: string; summary: string };
    expect(row.area).toBe('weekly');
    expect(row.summary).toBe('we vary attention');
  });
});

describe('drift flagging', () => {
  it('flags tracks whose current_as_of is older than 60 days', () => {
    expect(driftedTracks(db)).toHaveLength(0); // seeded today
    db.prepare("UPDATE tracks SET current_as_of = '2026-01-01' WHERE code = 'T4'").run();
    const drifted = driftedTracks(db);
    expect(drifted).toHaveLength(1);
    expect(drifted[0]!.code).toBe('T4');
    expect(drifted[0]!.days).toBeGreaterThan(60);
  });
});
