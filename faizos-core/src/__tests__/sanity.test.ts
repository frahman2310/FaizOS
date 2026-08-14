// Phase 0 sanity: the live database opens READ ONLY and contains exactly the nine v1 tables.
// Nothing here writes anything, anywhere.
import Database from 'better-sqlite3';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';

const HERE = dirname(fileURLToPath(import.meta.url));
const LIVE = join(HERE, '..', '..', 'data', 'faiz.db');

const V1_TABLES = [
  'insights',
  'journey_log',
  'lessons',
  'meta',
  'missions',
  'radar',
  'reviews',
  'revisions',
  'skills',
];

describe('v1 database sanity', () => {
  it('live database exists and opens read only', () => {
    expect(existsSync(LIVE)).toBe(true);
    const db = new Database(LIVE, { readonly: true, fileMustExist: true });
    const one = db.prepare('SELECT 1 AS x').get() as { x: number };
    db.close();
    expect(one.x).toBe(1);
  });

  it('contains every v1 table', () => {
    const db = new Database(LIVE, { readonly: true, fileMustExist: true });
    const rows = db
      .prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
      .all() as Array<{ name: string }>;
    db.close();
    const names = rows.map((r) => r.name);
    for (const t of V1_TABLES) expect(names).toContain(t);
  });
});
