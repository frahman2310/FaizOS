// The venture evidence engine. Five stages, split so that everything deterministic lives here
// and everything semantic (classification, grouping, axis judgment) happens in session with the
// model, written back through tools.
//
//   stage 1 ingest       deterministic fetch from free tier sources     (cron or tool)
//   stage 2 extract      model classifies pending evidence in session   (tools below)
//   stage 3 corroborate  deterministic: >= 2 INDEPENDENT source families
//   stage 4 score        model judges the axes; the weighting is fixed here
//   stage 5 gate         WIP limit 1 (database enforced) + the 14 day kill review
//
//   tsx src/venture.ts ingest [--db <path>]     stage 1 only, for the daily cron
import Database from 'better-sqlite3';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DB = join(HERE, '..', 'data', 'faiz.db');
const now = (): string => new Date().toISOString();

// ---- stage 1: sources ----------------------------------------------------------------------

export interface RawEvidence {
  source_family: string;
  source_url: string;
  excerpt: string;
}

export type FetchLike = (url: string, init?: { headers?: Record<string, string> }) => Promise<{
  ok: boolean;
  status: number;
  text(): Promise<string>;
}>;

const UA = 'FaizOS-venture-research faiz.rahman.research@proton.me'; // SEC EDGAR requires a real UA

const clip = (t: string, n = 400): string => t.replace(/\s+/g, ' ').trim().slice(0, n);

async function jsonOf(f: FetchLike, url: string, headers?: Record<string, string>): Promise<unknown> {
  const res = await f(url, { headers });
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return JSON.parse(await res.text()) as unknown;
}

// Complaint-mining queries, fixed so ingest stays deterministic in shape.
const COMPLAINT_QUERIES = ['"I wish there was a tool"', '"is there a tool that"', '"so tedious" AI'];

export async function fetchHackerNews(f: FetchLike): Promise<RawEvidence[]> {
  const out: RawEvidence[] = [];
  for (const q of COMPLAINT_QUERIES.slice(0, 2)) {
    const data = (await jsonOf(
      f,
      `https://hn.algolia.com/api/v1/search_by_date?query=${encodeURIComponent(q)}&tags=comment&hitsPerPage=10`,
    )) as { hits?: Array<{ objectID: string; comment_text?: string; story_title?: string }> };
    for (const h of data.hits ?? []) {
      if (!h.comment_text) continue;
      out.push({
        source_family: 'hackernews',
        source_url: `https://news.ycombinator.com/item?id=${h.objectID}`,
        excerpt: clip(`${h.story_title ?? ''}: ${h.comment_text}`),
      });
    }
  }
  return out;
}

export async function fetchGitHub(f: FetchLike): Promise<RawEvidence[]> {
  const headers: Record<string, string> = { Accept: 'application/vnd.github+json' };
  const token = process.env.GITHUB_TOKEN;
  if (token) headers.Authorization = `Bearer ${token}`;
  const data = (await jsonOf(
    f,
    'https://api.github.com/search/issues?q=%22feature+request%22+label%3A%22help+wanted%22+language%3Apython+state%3Aopen&sort=reactions&per_page=10',
    headers,
  )) as { items?: Array<{ html_url: string; title: string; body?: string | null }> };
  return (data.items ?? []).map((i) => ({
    source_family: 'github',
    source_url: i.html_url,
    excerpt: clip(`${i.title}: ${i.body ?? ''}`),
  }));
}

export async function fetchSecEdgar(f: FetchLike): Promise<RawEvidence[]> {
  const data = (await jsonOf(
    f,
    'https://efts.sec.gov/LATEST/search-index?q=%22manual%20reconciliation%22&dateRange=custom&forms=10-K',
    { 'User-Agent': UA },
  )) as { hits?: { hits?: Array<{ _id: string; _source?: { display_names?: string[] } }> } };
  return (data.hits?.hits ?? []).slice(0, 10).map((h) => ({
    source_family: 'sec_edgar',
    source_url: `https://www.sec.gov/Archives/edgar/data/${h._id}`,
    excerpt: clip(`10-K mentions manual reconciliation: ${(h._source?.display_names ?? []).join(', ')}`),
  }));
}

export async function fetchCompaniesHouse(f: FetchLike): Promise<RawEvidence[]> {
  const key = process.env.COMPANIES_HOUSE_KEY;
  if (!key) return []; // no key, skip gracefully; the briefing notes the gap
  const data = (await jsonOf(f, 'https://api.company-information.service.gov.uk/advanced-search/companies?sic_codes=62012&size=10', {
    Authorization: `Basic ${Buffer.from(key + ':').toString('base64')}`,
  })) as { items?: Array<{ company_number: string; company_name: string }> };
  return (data.items ?? []).map((c) => ({
    source_family: 'companies_house',
    source_url: `https://find-and-update.company-information.service.gov.uk/company/${c.company_number}`,
    excerpt: clip(`UK software company: ${c.company_name}`),
  }));
}

export async function fetchYcRfs(f: FetchLike): Promise<RawEvidence[]> {
  const res = await f('https://www.ycombinator.com/rfs');
  if (!res.ok) throw new Error(`rfs -> ${res.status}`);
  const html = await res.text();
  const headings = [...html.matchAll(/<h[23][^>]*>([^<]{8,120})<\/h[23]>/g)].map((m) => m[1] ?? '');
  return headings.slice(0, 12).map((h) => ({
    source_family: 'yc_rfs',
    source_url: 'https://www.ycombinator.com/rfs',
    excerpt: clip(`YC Request for Startups: ${h}`),
  }));
}

export async function fetchMcpRegistry(f: FetchLike): Promise<RawEvidence[]> {
  const data = (await jsonOf(f, 'https://registry.modelcontextprotocol.io/v0/servers?limit=20')) as {
    servers?: Array<{ name?: string; description?: string }>;
  };
  return (data.servers ?? []).map((srv) => ({
    source_family: 'mcp_registry',
    source_url: 'https://registry.modelcontextprotocol.io',
    excerpt: clip(`MCP server exists: ${srv.name ?? ''} ${srv.description ?? ''}`),
  }));
}

export async function fetchProductHunt(f: FetchLike): Promise<RawEvidence[]> {
  const token = process.env.PRODUCT_HUNT_TOKEN;
  if (!token) return []; // no token, skip gracefully
  const res = await f('https://api.producthunt.com/v2/api/graphql', {
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
  });
  if (!res.ok) throw new Error(`producthunt -> ${res.status}`);
  const data = JSON.parse(await res.text()) as {
    data?: { posts?: { edges?: Array<{ node?: { name?: string; tagline?: string; url?: string } }> } };
  };
  return (data.data?.posts?.edges ?? []).map((e) => ({
    source_family: 'producthunt',
    source_url: e.node?.url ?? 'https://www.producthunt.com',
    excerpt: clip(`${e.node?.name ?? ''}: ${e.node?.tagline ?? ''}`),
  }));
}

export async function fetchArxiv(f: FetchLike): Promise<RawEvidence[]> {
  const res = await f(
    'http://export.arxiv.org/api/query?search_query=cat:cs.SE+AND+abs:%22developer%20pain%22&max_results=5',
  );
  if (!res.ok) throw new Error(`arxiv -> ${res.status}`);
  const xml = await res.text();
  const entries = [...xml.matchAll(/<entry>[\s\S]*?<id>([^<]+)<\/id>[\s\S]*?<title>([^<]+)<\/title>[\s\S]*?<summary>([\s\S]*?)<\/summary>[\s\S]*?<\/entry>/g)];
  return entries.map((m) => ({
    source_family: 'arxiv',
    source_url: (m[1] ?? '').trim(),
    excerpt: clip(`${(m[2] ?? '').trim()}: ${(m[3] ?? '').trim()}`),
  }));
}

export const SOURCES: Array<{ family: string; fetch: (f: FetchLike) => Promise<RawEvidence[]> }> = [
  { family: 'hackernews', fetch: fetchHackerNews },
  { family: 'github', fetch: fetchGitHub },
  { family: 'sec_edgar', fetch: fetchSecEdgar },
  { family: 'companies_house', fetch: fetchCompaniesHouse },
  { family: 'yc_rfs', fetch: fetchYcRfs },
  { family: 'mcp_registry', fetch: fetchMcpRegistry },
  { family: 'producthunt', fetch: fetchProductHunt },
  { family: 'arxiv', fetch: fetchArxiv },
];

const sleep = (ms: number): Promise<void> => new Promise((r) => setTimeout(r, ms));

export async function ingest(
  db: Database.Database,
  fetchImpl: FetchLike,
  delayMs = 1100, // sequential with a polite gap; free tier rate limits stay respected
): Promise<{ inserted: number; perFamily: Record<string, number>; failures: Record<string, string> }> {
  const insert = db.prepare(
    `INSERT INTO evidence (venture_id, source_family, source_url, excerpt, jtbd, importance, dissatisfaction, captured_at)
     SELECT NULL, ?, ?, ?, '', NULL, NULL, ?
     WHERE NOT EXISTS (SELECT 1 FROM evidence WHERE source_url = ? AND excerpt = ?)`,
  );
  const perFamily: Record<string, number> = {};
  const failures: Record<string, string> = {};
  let inserted = 0;
  for (const src of SOURCES) {
    try {
      const rows = await src.fetch(fetchImpl);
      let count = 0;
      for (const r of rows) {
        const res = insert.run(r.source_family, r.source_url, r.excerpt, now(), r.source_url, r.excerpt);
        count += res.changes;
      }
      perFamily[src.family] = count;
      inserted += count;
    } catch (e) {
      failures[src.family] = e instanceof Error ? e.message : String(e);
    }
    if (delayMs > 0) await sleep(delayMs);
  }
  return { inserted, perFamily, failures };
}

// ---- stage 2: classification (model in session; deterministic writes) ----------------------

export function pendingClassification(db: Database.Database, limit = 25): Array<Record<string, unknown>> {
  return db
    .prepare('SELECT id, source_family, source_url, excerpt FROM evidence WHERE importance IS NULL ORDER BY id LIMIT ?')
    .all(limit) as Array<Record<string, unknown>>;
}

export interface Classification {
  evidence_id: number;
  jtbd: string;
  importance: number;      // 1..5
  dissatisfaction: number; // 1..5
  venture_title?: string;  // group this evidence under a candidate venture
}

export function saveClassifications(db: Database.Database, items: Classification[]): { classified: number; ventures_created: number } {
  const findVenture = db.prepare('SELECT id FROM ventures WHERE title = ?');
  const createVenture = db.prepare("INSERT INTO ventures (title, stage, created_at) VALUES (?, 'candidate', ?)");
  const update = db.prepare('UPDATE evidence SET jtbd = ?, importance = ?, dissatisfaction = ?, venture_id = COALESCE(?, venture_id) WHERE id = ?');
  let classified = 0;
  let venturesCreated = 0;
  const tx = db.transaction(() => {
    for (const item of items) {
      let ventureId: number | null = null;
      if (item.venture_title) {
        const existing = findVenture.get(item.venture_title) as { id: number } | undefined;
        if (existing) ventureId = existing.id;
        else {
          ventureId = Number(createVenture.run(item.venture_title, now()).lastInsertRowid);
          venturesCreated += 1;
        }
      }
      const clampScore = (v: number): number => Math.max(1, Math.min(5, Math.round(v)));
      update.run(item.jtbd, clampScore(item.importance), clampScore(item.dissatisfaction), ventureId, item.evidence_id);
      classified += 1;
    }
  });
  tx();
  return { classified, ventures_created: venturesCreated };
}

// ---- stage 3: corroboration (deterministic, the gate that matters) -------------------------

export function corroborate(db: Database.Database): {
  advanced: Array<{ id: number; title: string; families: number }>;
  failed: Array<{ id: number; title: string; families: number; reason: string }>;
} {
  const candidates = db.prepare("SELECT id, title FROM ventures WHERE stage = 'candidate'").all() as Array<{
    id: number;
    title: string;
  }>;
  const familyCount = db.prepare('SELECT COUNT(DISTINCT source_family) AS c FROM evidence WHERE venture_id = ?');
  const advance = db.prepare("UPDATE ventures SET stage = 'corroborated' WHERE id = ?");
  const advanced: Array<{ id: number; title: string; families: number }> = [];
  const failed: Array<{ id: number; title: string; families: number; reason: string }> = [];
  for (const v of candidates) {
    const c = (familyCount.get(v.id) as { c: number }).c;
    if (c >= 2) {
      advance.run(v.id);
      advanced.push({ id: v.id, title: v.title, families: c });
    } else {
      failed.push({
        id: v.id,
        title: v.title,
        families: c,
        reason: c === 0 ? 'no evidence attached' : 'all evidence from one source family. Multiple hits within one family do not count.',
      });
    }
  }
  return { advanced, failed };
}

// ---- stage 4: scoring (model judges the axes; the weights are fixed here) ------------------

export const AXES: Array<{ key: string; weight: number }> = [
  { key: 'opportunity_gap', weight: 2 },
  { key: 'distribution_reachability', weight: 3 },
  { key: 'lab_absorption_risk_inverted', weight: 3 },
  { key: 'buildable_14d', weight: 3 },
  { key: 'teaches_curriculum', weight: 1 },
  { key: 'regulatory_feasibility', weight: 2 },
];

export function scoreVenture(db: Database.Database, ventureId: number, axes: Record<string, number>): { weighted_score: number } {
  const v = db.prepare('SELECT id, stage FROM ventures WHERE id = ?').get(ventureId) as { id: number; stage: string } | undefined;
  if (!v) throw new Error(`no venture #${ventureId}`);
  if (v.stage !== 'corroborated' && v.stage !== 'scored') {
    throw new Error(`venture #${ventureId} is '${v.stage}'. Only corroborated ventures get scored; the gate is not optional.`);
  }
  let total = 0;
  let weightSum = 0;
  for (const a of AXES) {
    const raw = axes[a.key];
    if (typeof raw !== 'number') throw new Error(`missing axis ${a.key}`);
    const score = Math.max(1, Math.min(5, raw));
    total += score * a.weight;
    weightSum += 5 * a.weight;
  }
  const weighted = Number(((total / weightSum) * 5).toFixed(2)); // normalised back to a 0..5 scale
  db.prepare("UPDATE ventures SET score_json = ?, weighted_score = ?, stage = 'scored' WHERE id = ?").run(
    JSON.stringify(axes),
    weighted,
    ventureId,
  );
  return { weighted_score: weighted };
}

// ---- stage 5: the gate ---------------------------------------------------------------------

export function activateVenture(db: Database.Database, ventureId: number, v0Metric: string): {
  activated: boolean;
  reason: string;
  v0_deadline?: string;
  milestone_spine?: string[];
} {
  const v = db.prepare('SELECT id, title, stage FROM ventures WHERE id = ?').get(ventureId) as
    | { id: number; title: string; stage: string }
    | undefined;
  if (!v) return { activated: false, reason: `no venture #${ventureId}` };
  if (v.stage !== 'scored' && v.stage !== 'parked') {
    return { activated: false, reason: `venture #${ventureId} is '${v.stage}'. Score it first; the pipeline order is not optional.` };
  }
  const deadline = new Date(Date.now() + 14 * 86400000).toISOString().slice(0, 10);
  try {
    db.prepare("UPDATE ventures SET stage = 'active', v0_metric = ?, v0_deadline = ?, outcome = NULL WHERE id = ?").run(
      v0Metric,
      deadline,
      ventureId,
    );
  } catch (e) {
    if (e instanceof Error && /UNIQUE/.test(e.message)) {
      const current = db.prepare("SELECT id, title FROM ventures WHERE stage = 'active'").get() as { id: number; title: string };
      return {
        activated: false,
        reason: `the WIP limit is 1 and the database enforced it. Venture #${current.id} (${current.title}) is active. Finish, park or kill it first.`,
      };
    }
    throw e;
  }
  return {
    activated: true,
    reason: 'active. Fourteen days to the kill review.',
    v0_deadline: deadline,
    milestone_spine: [
      `M1 (day 1-2): the walking skeleton. The thinnest end-to-end path that touches the real problem.`,
      `M2 (day 3-5): the core mechanism, tested.`,
      `M3 (day 6-9): the v0 metric instrumented: "${v0Metric}" must be measurable, not guessed.`,
      `M4 (day 10-13): put it in front of one real person from the evidence trail.`,
      `M5 (day 14): kill review with the number. Continue, park, or kill. No fourth option.`,
    ],
  };
}

export function reviewVenture(
  db: Database.Database,
  outcome: 'continue' | 'park' | 'kill',
  note: string,
  newMetric?: string,
): { done: boolean; reason: string } {
  const active = db.prepare("SELECT id, title, v0_metric, v0_deadline FROM ventures WHERE stage = 'active'").get() as
    | { id: number; title: string; v0_metric: string | null; v0_deadline: string | null }
    | undefined;
  if (!active) return { done: false, reason: 'no active venture to review' };
  if (outcome === 'continue') {
    if (!newMetric) return { done: false, reason: 'continue requires a NEW 14 day metric' };
    const deadline = new Date(Date.now() + 14 * 86400000).toISOString().slice(0, 10);
    db.prepare("UPDATE ventures SET v0_metric = ?, v0_deadline = ?, outcome = ? WHERE id = ?").run(
      newMetric,
      deadline,
      `continued: ${note}`,
      active.id,
    );
    return { done: true, reason: `continued with new metric "${newMetric}" to ${deadline}` };
  }
  if (outcome === 'park') {
    db.prepare("UPDATE ventures SET stage = 'parked', outcome = ? WHERE id = ?").run(`parked: ${note}`, active.id);
    return { done: true, reason: 'parked with a written reason. The WIP slot is free.' };
  }
  // kill: the post mortem is mandatory and feeds the insight loop
  if (!note.trim()) return { done: false, reason: 'a kill requires a post mortem, and it is not optional' };
  db.prepare("UPDATE ventures SET stage = 'killed', outcome = 'killed', postmortem = ? WHERE id = ?").run(note, active.id);
  db.prepare('INSERT INTO insights (ts, note, weight, mode) VALUES (?, ?, 1, ?) ON CONFLICT(note) DO UPDATE SET weight = weight + 1').run(
    now(),
    `Venture post mortem (${active.title}): ${note}`,
    'build',
  );
  return { done: true, reason: 'killed. The post mortem is in the insight loop; the slot is free.' };
}

// ---- seeds from spec 8.7 -------------------------------------------------------------------

export function seedVentures(db: Database.Database): number {
  const seeds: Array<{ title: string; thesis: string; evidence: RawEvidence[] }> = [
    {
      title: 'Pakistani e-invoicing compliance',
      thesis: 'FBR Rule 150Q phases in mandatory e-invoicing; a compliance deadline creates non discretionary SME spend, it is a system of record integration, and it is invisible to frontier labs. Regulatory timing is the main risk; deadlines have slipped.',
      evidence: [
        { source_family: 'regulator', source_url: 'https://fbr.gov.pk', excerpt: 'FBR Rule 150Q mandatory e-invoicing, integration deadlines extended during 2026, draft 2026 rules contemplate CCTV at point of sale.' },
        { source_family: 'yc_rfs', source_url: 'https://www.ycombinator.com/rfs', excerpt: 'YC RFS: AI native compliance infrastructure.' },
      ],
    },
    {
      title: 'Tooling for USD earning Pakistani freelancers',
      thesis: 'Freelancer export earnings hit a record 1.76B USD in FY2025-26. This cohort already earns in dollars, which sidesteps the PKR willingness to pay ceiling and the payment rail friction.',
      evidence: [
        { source_family: 'regulator', source_url: 'https://www.sbp.org.pk', excerpt: 'Freelancer export earnings 1.76B USD FY2025-26 against total remittances of 41.6B. Note PSEB frames 1.1B on a different measurement basis.' },
      ],
    },
    {
      title: 'Self maintaining APIs',
      thesis: 'Agents that automatically update customer codebases when an API provider ships a breaking change. Narrow, technical, testable, no regulatory surface, dogfoodable on own repositories. Highest curriculum fit (T7).',
      evidence: [
        { source_family: 'yc_rfs', source_url: 'https://www.ycombinator.com/rfs', excerpt: 'YC RFS: agents that automatically update customer codebases when an API provider ships a breaking change.' },
      ],
    },
    {
      title: 'MCPB desktop extension channel',
      thesis: 'The Claude desktop extension route is the only lab distribution surface with no organisation plan gate, and the July 2026 stateless MCP spec cut hosting complexity. A channel to test, more than a product.',
      evidence: [
        { source_family: 'vendor_docs', source_url: 'https://modelcontextprotocol.io', excerpt: 'MCP specification 2026-07-28 went stateless; MCPB desktop extension submission has no org gate.' },
      ],
    },
  ];
  const findVenture = db.prepare('SELECT id FROM ventures WHERE title = ?');
  const createVenture = db.prepare("INSERT INTO ventures (title, thesis, stage, created_at) VALUES (?, ?, 'candidate', ?)");
  const insertEvidence = db.prepare(
    `INSERT INTO evidence (venture_id, source_family, source_url, excerpt, jtbd, importance, dissatisfaction, captured_at)
     SELECT ?, ?, ?, ?, '', NULL, NULL, ?
     WHERE NOT EXISTS (SELECT 1 FROM evidence WHERE venture_id = ? AND source_url = ? AND excerpt = ?)`,
  );
  let created = 0;
  for (const seed of seeds) {
    let id: number;
    const existing = findVenture.get(seed.title) as { id: number } | undefined;
    if (existing) id = existing.id;
    else {
      id = Number(createVenture.run(seed.title, seed.thesis, now()).lastInsertRowid);
      created += 1;
    }
    for (const e of seed.evidence) insertEvidence.run(id, e.source_family, e.source_url, e.excerpt, now(), id, e.source_url, e.excerpt);
  }
  return created;
}

// ---- CLI (stage 1 only, for the daily cron) ------------------------------------------------

const invokedDirectly = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (invokedDirectly) {
  const command = process.argv[2] ?? 'ingest';
  const flag = process.argv.indexOf('--db');
  const dbPath = flag !== -1 && process.argv[flag + 1] ? (process.argv[flag + 1] as string) : DEFAULT_DB;
  const db = new Database(dbPath, { fileMustExist: true });
  db.pragma('journal_mode = WAL');
  if (command === 'ingest') {
    const realFetch: FetchLike = (url, init) => fetch(url, init);
    ingest(db, realFetch)
      .then((r) => {
        console.log(`ingested ${r.inserted} new evidence rows`);
        for (const [fam, cnt] of Object.entries(r.perFamily)) console.log(`  ${fam}: ${cnt}`);
        for (const [fam, err] of Object.entries(r.failures)) console.log(`  ${fam} FAILED: ${err}`);
        db.close();
      })
      .catch((e) => {
        console.error(e);
        db.close();
        process.exit(1);
      });
  } else if (command === 'seed') {
    console.log(`seeded ${seedVentures(db)} spec 8.7 ventures`);
    db.close();
  } else {
    console.error(`unknown command: ${command} (use ingest | seed)`);
    db.close();
    process.exit(1);
  }
}
