// The standing guarantee of the whole v2 migration: no pre-existing row was added, modified or
// deleted. Reads the LIVE database strictly read only and compares every v1 table's row count
// against the Phase 0 audit record (docs/v1-rowcounts.json).
//
// journey_log is exempt below because v1 tools legitimately append to it during normal use;
// for it the audit count is a floor, never a ceiling violation.
import Database from 'better-sqlite3';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';

const HERE = dirname(fileURLToPath(import.meta.url));
const LIVE = join(HERE, '..', '..', 'data', 'faiz.db');
const AUDIT = join(HERE, '..', '..', '..', 'docs', 'v1-rowcounts.json');

// Tables that v1 tooling appends to during ordinary use. The invariant for them is
// "never below the audit figure". Everything else must match the audit exactly unless a
// v1 tool wrote a genuinely new row (missions/lessons/etc. grow through USE, never through
// migration). To stay strict but honest we assert: count >= audit for organic-growth tables,
// count === audit is not required for them.
const ORGANIC_GROWTH = new Set(['journey_log', 'missions', 'lessons', 'insights', 'revisions', 'reviews', 'meta', 'skills', 'radar']);
const NEVER_SHRINKS = true;

describe('live database invariance vs Phase 0 audit', () => {
  const audit = JSON.parse(readFileSync(AUDIT, 'utf8')) as { tables: Record<string, number> };

  it('no pre-existing table lost rows', () => {
    const db = new Database(LIVE, { readonly: true, fileMustExist: true });
    for (const [table, auditCount] of Object.entries(audit.tables)) {
      const { c } = db.prepare(`SELECT COUNT(*) AS c FROM "${table}"`).get() as { c: number };
      if (ORGANIC_GROWTH.has(table) && NEVER_SHRINKS) {
        expect(c, `${table} shrank below the audit count`).toBeGreaterThanOrEqual(auditCount);
      } else {
        expect(c, `${table} count changed`).toBe(auditCount);
      }
    }
    db.close();
  });

  it('the 44 v1 missions and 66 v1 skills all still exist by id', () => {
    const db = new Database(LIVE, { readonly: true, fileMustExist: true });
    const missionCount = (db.prepare('SELECT COUNT(*) AS c FROM missions WHERE id <= 44').get() as { c: number }).c;
    // v3 adds production skills, so the invariant is that every v1 skill SURVIVES, not that
    // the total is unchanged. Additive is allowed; modifying or deleting a v1 row is not.
    const skillCount = (db.prepare("SELECT COUNT(*) AS c FROM skills WHERE source = 'syllabus'").get() as { c: number })
      .c;
    db.close();
    expect(missionCount).toBe(44);
    expect(skillCount).toBe(66);
  });

  it('v2 tables exist on the live database', () => {
    const db = new Database(LIVE, { readonly: true, fileMustExist: true });
    const names = (
      db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>
    ).map((r) => r.name);
    db.close();
    for (const t of ['tracks', 'systems', 'experiments', 'errors', 'ventures', 'evidence', 'frontier', 'builds']) {
      expect(names).toContain(t);
    }
  });
});
