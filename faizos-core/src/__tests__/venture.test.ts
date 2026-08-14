// Phase 6 tests. Zero network: every fetcher runs against fixture responses through the
// injectable FetchLike. The corroboration gate and the WIP lifecycle are the load-bearing parts.
import Database from 'better-sqlite3';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { openDb } from '../db.js';
import { migrateUp } from '../migrate.js';
import {
  activateVenture, corroborate, ingest, pendingClassification, reviewVenture,
  saveClassifications, scoreVenture, seedVentures, type FetchLike,
} from '../venture.js';

let dir: string;
let db: Database.Database;

const FIXTURES: Record<string, string> = {
  'hn.algolia.com': JSON.stringify({
    hits: [
      { objectID: '101', comment_text: 'I wish there was a tool that reconciled invoices automatically', story_title: 'Ask HN' },
      { objectID: '102', comment_text: 'manually fixing API breakage every month is so tedious', story_title: 'Ask HN' },
    ],
  }),
  'api.github.com': JSON.stringify({
    items: [
      { html_url: 'https://github.com/x/y/issues/1', title: 'Feature request: auto-fix breaking API changes', body: 'our client breaks every release' },
    ],
  }),
  'efts.sec.gov': JSON.stringify({ hits: { hits: [{ _id: '123', _source: { display_names: ['ACME CORP'] } }] } }),
  'www.ycombinator.com': '<html><h2>AI native compliance infrastructure</h2><h2>Self maintaining APIs</h2></html>',
  'registry.modelcontextprotocol.io': JSON.stringify({ servers: [{ name: 'io.example/demo', description: 'a demo server' }] }),
  'export.arxiv.org': '<feed><entry><id>http://arxiv.org/abs/1</id><title>Developer pain points</title><summary>a study</summary></entry></feed>',
};

const mockFetch: FetchLike = async (url) => {
  const host = new URL(url).host;
  const body = FIXTURES[host];
  if (body === undefined) return { ok: false, status: 404, text: async () => 'not found' };
  return { ok: true, status: 200, text: async () => body };
};

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), 'faizos-venture-'));
  const dbPath = join(dir, 'test.db');
  openDb(dbPath).close();
  migrateUp(dbPath);
  db = new Database(dbPath);
});

afterAll(() => {
  db.close();
  rmSync(dir, { recursive: true, force: true });
});

describe('stage 1 ingest, fully mocked', () => {
  it('inserts evidence from every reachable source, skips keyless ones, and is idempotent', async () => {
    const r1 = await ingest(db, mockFetch, 0);
    expect(r1.inserted).toBeGreaterThanOrEqual(6);
    expect(r1.perFamily.hackernews).toBe(2);
    expect(r1.perFamily.github).toBe(1);
    expect(r1.perFamily.companies_house).toBe(0); // no key: skipped gracefully, no failure
    expect(r1.failures.companies_house).toBeUndefined();
    const r2 = await ingest(db, mockFetch, 0);
    expect(r2.inserted).toBe(0); // same fixtures, nothing new
  });

  it('records a failure per source instead of dying', async () => {
    const failing: FetchLike = async () => ({ ok: false, status: 500, text: async () => 'boom' });
    const r = await ingest(db, failing, 0);
    expect(r.inserted).toBe(0);
    expect(Object.keys(r.failures).length).toBeGreaterThan(0);
  });
});

describe('stage 2 classification', () => {
  it('classifies pending rows and groups them into candidate ventures', () => {
    const pending = pendingClassification(db, 50);
    expect(pending.length).toBeGreaterThanOrEqual(6);
    const invoiceRow = pending.find((p) => String(p.excerpt).includes('reconciled invoices'));
    const apiRow1 = pending.find((p) => String(p.excerpt).includes('API breakage'));
    const apiRow2 = pending.find((p) => String(p.excerpt).includes('auto-fix breaking API'));
    const r = saveClassifications(db, [
      { evidence_id: Number(invoiceRow!.id), jtbd: 'reconcile invoices without manual work', importance: 4, dissatisfaction: 4, venture_title: 'Invoice reconciliation' },
      { evidence_id: Number(apiRow1!.id), jtbd: 'keep clients working across breaking API changes', importance: 5, dissatisfaction: 4, venture_title: 'Self maintaining APIs test' },
      { evidence_id: Number(apiRow2!.id), jtbd: 'keep clients working across breaking API changes', importance: 5, dissatisfaction: 5, venture_title: 'Self maintaining APIs test' },
    ]);
    expect(r.classified).toBe(3);
    expect(r.ventures_created).toBe(2);
  });
});

describe('stage 3 corroboration, the gate that matters', () => {
  it('advances only ventures with evidence from 2+ INDEPENDENT families', () => {
    const gate = corroborate(db);
    const passed = gate.advanced.map((v) => v.title);
    const failed = gate.failed.map((v) => v.title);
    // Self maintaining APIs test: hackernews + github = 2 families -> advances
    expect(passed).toContain('Self maintaining APIs test');
    // Invoice reconciliation: only hackernews -> fails, with the one-family reason
    expect(failed).toContain('Invoice reconciliation');
    const reason = gate.failed.find((v) => v.title === 'Invoice reconciliation')!.reason;
    expect(reason).toContain('one source family');
  });

  it('multiple hits within one family do not count', () => {
    // Both API rows came from different families; build a same-family-only venture to prove the rule
    db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES ('same family only', 'candidate', 'now')").run();
    const vid = (db.prepare("SELECT id FROM ventures WHERE title = 'same family only'").get() as { id: number }).id;
    db.prepare("INSERT INTO evidence (venture_id, source_family, source_url, excerpt, jtbd, captured_at) VALUES (?, 'hackernews', 'u1', 'e1', 'j', 'now'), (?, 'hackernews', 'u2', 'e2', 'j', 'now'), (?, 'hackernews', 'u3', 'e3', 'j', 'now')").run(vid, vid, vid);
    const gate = corroborate(db);
    expect(gate.failed.map((v) => v.title)).toContain('same family only');
  });
});

describe('stages 4 and 5: score, WIP gate, kill review', () => {
  let ventureId: number;

  it('refuses to score an uncorroborated venture', () => {
    const vid = (db.prepare("SELECT id FROM ventures WHERE title = 'Invoice reconciliation'").get() as { id: number }).id;
    expect(() => scoreVenture(db, vid, { opportunity_gap: 5, distribution_reachability: 5, lab_absorption_risk_inverted: 5, buildable_14d: 5, teaches_curriculum: 5, regulatory_feasibility: 5 })).toThrow(/gate/);
  });

  it('scores a corroborated venture with the fixed weights', () => {
    ventureId = (db.prepare("SELECT id FROM ventures WHERE title = 'Self maintaining APIs test'").get() as { id: number }).id;
    const r = scoreVenture(db, ventureId, { opportunity_gap: 4, distribution_reachability: 3, lab_absorption_risk_inverted: 4, buildable_14d: 5, teaches_curriculum: 5, regulatory_feasibility: 5 });
    // (4*2+3*3+4*3+5*3+5*1+5*2)/(5*14)*5 = (8+9+12+15+5+10)/70*5 = 59/70*5 = 4.21
    expect(r.weighted_score).toBeCloseTo(4.21, 2);
  });

  it('activates with a 14 day deadline and refuses a second activation via the database', () => {
    const a = activateVenture(db, ventureId, '3 repos auto-fixed with passing tests');
    expect(a.activated).toBe(true);
    expect(a.milestone_spine).toHaveLength(5);
    // score another and try to activate it
    db.prepare("UPDATE ventures SET stage = 'scored' WHERE title = 'Invoice reconciliation'").run();
    const vid2 = (db.prepare("SELECT id FROM ventures WHERE title = 'Invoice reconciliation'").get() as { id: number }).id;
    const b = activateVenture(db, vid2, 'anything');
    expect(b.activated).toBe(false);
    expect(b.reason).toContain('WIP limit is 1');
  });

  it('kill requires a post mortem and writes it into the insight loop', () => {
    const noNote = reviewVenture(db, 'kill', '   ');
    expect(noNote.done).toBe(false);
    const killed = reviewVenture(db, 'kill', 'acceptance rate too low; the fix window is smaller than the breakage window');
    expect(killed.done).toBe(true);
    const insight = db.prepare("SELECT note FROM insights WHERE note LIKE 'Venture post mortem%'").get() as { note: string };
    expect(insight.note).toContain('acceptance rate too low');
    expect((db.prepare("SELECT COUNT(*) c FROM ventures WHERE stage = 'active'").get() as { c: number }).c).toBe(0);
  });
});

describe('spec 8.7 seeds', () => {
  it('seeds four candidate ventures with evidence attached, idempotently', () => {
    expect(seedVentures(db)).toBe(4);
    expect(seedVentures(db)).toBe(0);
    const einvoicing = db.prepare("SELECT id FROM ventures WHERE title = 'Pakistani e-invoicing compliance'").get() as { id: number };
    const ev = (db.prepare('SELECT COUNT(*) c FROM evidence WHERE venture_id = ?').get(einvoicing.id) as { c: number }).c;
    expect(ev).toBe(2); // regulator + yc_rfs: two independent families, ready for the gate
  });
});
