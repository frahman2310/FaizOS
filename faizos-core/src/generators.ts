// v2 artefact generators. Deterministic: read the database, write markdown. No model anywhere.
//
//   tsx src/generators.ts all [--db <path>] [--out <dir>]
//   tsx src/generators.ts experiments | errors | ventures | frontier | capstone
//
// CAPSTONE.md is auto scored: a rung counts only when database rows back it. The scoring rules
// are printed inside the file so the score is auditable.
import Database from 'better-sqlite3';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DB = join(HERE, '..', 'data', 'faiz.db');
const REPO_ROOT = join(HERE, '..', '..');

type Row = Record<string, unknown>;
const s = (v: unknown): string => (v === null || v === undefined ? '' : String(v));
const n = (v: unknown): number | null => (typeof v === 'number' ? v : null);

// ---- EXPERIMENTS.md ------------------------------------------------------------------------

export function renderExperiments(db: Database.Database): string {
  const systems = db
    .prepare('SELECT id, title, kind, status, metric_name, metric_value, baseline_value FROM systems ORDER BY id')
    .all() as Row[];
  const expBySystem = db.prepare(
    'SELECT seed, metric_name, metric_value, gpu_type, gpu_hours, cost_usd, notes, created_at FROM experiments WHERE system_id = ? ORDER BY id',
  );
  const lines: string[] = [
    '# Experiments',
    '',
    'Every run, with cost and seed spread. Generated from the database; do not edit by hand.',
    'A result is real only if the gain clears the spread against a compute matched baseline.',
    '',
  ];
  let totalCost = 0;
  let totalHours = 0;
  let any = false;
  for (const sys of systems) {
    const runs = expBySystem.all(sys.id) as Row[];
    if (runs.length === 0) continue;
    any = true;
    lines.push(`## ${s(sys.title)} (system ${s(sys.id)}, ${s(sys.kind)})`);
    lines.push('');
    lines.push('| run | seed | metric | value | gpu | hours | cost usd | notes |');
    lines.push('|---|---|---|---|---|---|---|---|');
    runs.forEach((r, i) => {
      totalCost += n(r.cost_usd) ?? 0;
      totalHours += n(r.gpu_hours) ?? 0;
      lines.push(
        `| ${i + 1} | ${s(r.seed)} | ${s(r.metric_name)} | ${s(r.metric_value)} | ${s(r.gpu_type)} | ${s(r.gpu_hours)} | ${s(r.cost_usd)} | ${s(r.notes)} |`,
      );
    });
    const byMetric = new Map<string, number[]>();
    for (const r of runs) {
      const key = s(r.metric_name);
      const v = n(r.metric_value);
      if (v === null) continue;
      const arr = byMetric.get(key) ?? [];
      arr.push(v);
      byMetric.set(key, arr);
    }
    for (const [metric, values] of byMetric) {
      if (values.length >= 3) {
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const lo = Math.min(...values);
        const hi = Math.max(...values);
        lines.push('');
        lines.push(
          `Seed spread for ${metric}: n=${values.length}, mean ${mean.toFixed(4)}, min ${lo}, max ${hi}, spread ${(hi - lo).toFixed(4)}.`,
        );
        const base = n(sys.baseline_value);
        if (base !== null) {
          const gain = Math.abs(mean - base);
          const verdict = gain > hi - lo ? 'clears the spread' : 'INSIDE THE NOISE';
          lines.push(`Against baseline ${base}: gap ${gain.toFixed(4)}, which ${verdict}.`);
        } else {
          lines.push('No baseline recorded. A gain over nothing is not a gain.');
        }
      } else {
        lines.push('');
        lines.push(`${metric}: ${values.length} run(s). Three or more seeds before any claim counts.`);
      }
    }
    lines.push('');
  }
  if (!any) lines.push('No experiment runs recorded yet. The first real GPU run lands here.');
  lines.push('');
  lines.push(`Total logged: ${totalHours.toFixed(2)} GPU hours, ${totalCost.toFixed(2)} USD.`);
  return lines.join('\n') + '\n';
}

// ---- ERRORS.md -----------------------------------------------------------------------------

export function renderErrors(db: Database.Database): string {
  const open = db
    .prepare('SELECT category, description, rule_broken, occurrences, last_seen FROM errors WHERE resolved = 0 ORDER BY occurrences DESC, category')
    .all() as Row[];
  const resolved = db
    .prepare('SELECT category, occurrences, last_seen FROM errors WHERE resolved = 1 ORDER BY last_seen DESC')
    .all() as Row[];
  const lines: string[] = [
    '# Error taxonomy',
    '',
    'Open categories weight the next rules card. Generated from the database; do not edit by hand.',
    '',
    '## Open',
    '',
  ];
  if (open.length === 0) lines.push('Nothing open.');
  else {
    lines.push('| category | occurrences | last seen | the rule it breaks |');
    lines.push('|---|---|---|---|');
    for (const e of open) lines.push(`| ${s(e.category)} | ${s(e.occurrences)} | ${s(e.last_seen)} | ${s(e.rule_broken)} |`);
    lines.push('');
    lines.push('### Detail');
    for (const e of open) {
      lines.push('');
      lines.push(`**${s(e.category)}** (${s(e.occurrences)}): ${s(e.description)}`);
    }
  }
  lines.push('');
  lines.push('## Resolved');
  lines.push('');
  if (resolved.length === 0) lines.push('None yet. A category resolves after three clean builds in a row.');
  else for (const e of resolved) lines.push(`- ${s(e.category)} (${s(e.occurrences)} occurrences, last ${s(e.last_seen)})`);
  return lines.join('\n') + '\n';
}

// ---- VENTURES.md (gitignored by default; evidence stays local) -----------------------------

export function renderVentures(db: Database.Database): string {
  const ventures = db
    .prepare('SELECT id, title, thesis, stage, weighted_score, v0_metric, v0_deadline, outcome, postmortem, created_at FROM ventures ORDER BY id')
    .all() as Row[];
  const evidence = db.prepare(
    'SELECT source_family, source_url, excerpt, jtbd, importance, dissatisfaction FROM evidence WHERE venture_id = ? ORDER BY id',
  );
  const unattached = (db.prepare('SELECT COUNT(*) AS c FROM evidence WHERE venture_id IS NULL').get() as { c: number }).c;
  const lines: string[] = [
    '# Venture pipeline',
    '',
    'Evidence first, one active venture maximum, a 14 day kill review. Generated from the database.',
    'This file is gitignored: venture evidence stays local until a deliberate publish decision.',
    '',
  ];
  const active = ventures.filter((v) => s(v.stage) === 'active');
  lines.push(`State: ${ventures.length} ventures tracked, ${active.length} active (limit 1, database enforced), ${unattached} unclassified or ungrouped evidence rows.`);
  lines.push('');
  for (const v of ventures) {
    lines.push(`## ${s(v.id)}. ${s(v.title)} [${s(v.stage)}]`);
    if (s(v.thesis)) lines.push(`Thesis: ${s(v.thesis)}`);
    if (v.weighted_score !== null) lines.push(`Weighted score: ${s(v.weighted_score)}`);
    if (s(v.v0_metric)) lines.push(`v0 metric: ${s(v.v0_metric)} by ${s(v.v0_deadline)}`);
    if (s(v.outcome)) lines.push(`Outcome: ${s(v.outcome)}`);
    if (s(v.postmortem)) lines.push(`Post mortem: ${s(v.postmortem)}`);
    const ev = evidence.all(v.id) as Row[];
    if (ev.length) {
      lines.push('');
      lines.push('| family | importance | dissatisfaction | job to be done | source |');
      lines.push('|---|---|---|---|---|');
      for (const e of ev) lines.push(`| ${s(e.source_family)} | ${s(e.importance)} | ${s(e.dissatisfaction)} | ${s(e.jtbd)} | ${s(e.source_url)} |`);
    }
    lines.push('');
  }
  if (ventures.length === 0) lines.push('No ventures yet. /faiz-venture ingest starts the evidence engine.');
  return lines.join('\n') + '\n';
}

// ---- FRONTIER.md ---------------------------------------------------------------------------

export function renderFrontier(db: Database.Database): string {
  const tracks = db.prepare('SELECT id, code, title, current_as_of FROM tracks ORDER BY position').all() as Row[];
  const items = db.prepare(
    'SELECT title, url, summary, ingested_at, actioned FROM frontier WHERE affects_track_id = ? ORDER BY ingested_at DESC LIMIT 10',
  );
  const general = db
    .prepare('SELECT area, title, url, summary, ingested_at FROM frontier WHERE affects_track_id IS NULL ORDER BY ingested_at DESC LIMIT 10')
    .all() as Row[];
  const lines: string[] = [
    '# Frontier',
    '',
    'Rolling ingest, grouped by the track it affects. Generated from the database.',
    'A track older than 60 days is flagged: its content may have drifted.',
    '',
  ];
  const today = new Date();
  for (const t of tracks) {
    const rows = items.all(t.id) as Row[];
    const asOf = s(t.current_as_of);
    let flag = '';
    if (asOf) {
      const age = Math.floor((today.getTime() - new Date(asOf).getTime()) / 86400000);
      if (age > 60) flag = `  DRIFTED (${age} days since ${asOf})`;
    }
    lines.push(`## ${s(t.code)} ${s(t.title)}${flag}`);
    if (rows.length === 0) lines.push('No ingested items yet.');
    for (const r of rows) lines.push(`- ${s(r.title)} (${s(r.ingested_at).slice(0, 10)}) ${s(r.summary)} ${s(r.url)}`);
    lines.push('');
  }
  if (general.length) {
    lines.push('## General');
    for (const r of general) lines.push(`- [${s(r.area)}] ${s(r.title)} (${s(r.ingested_at).slice(0, 10)}) ${s(r.url)}`);
  }
  return lines.join('\n') + '\n';
}

// ---- CAPSTONE.md, auto scored --------------------------------------------------------------

interface RungResult {
  rung: number;
  title: string;
  status: 'SOLID' | 'PARTIAL' | 'MISSING';
  evidence: string;
  rule: string;
}

export function scoreCapstone(db: Database.Database): RungResult[] {
  const studyCount = (db.prepare("SELECT COUNT(*) AS c FROM systems WHERE kind = 'study' AND status = 'shipped'").get() as { c: number }).c;
  const products = db.prepare("SELECT id, title, repo_url, deployed_url, metric_name, metric_value FROM systems WHERE kind = 'product' AND status = 'shipped'").all() as Row[];
  // v3: a deployed service is only finished when it carries a latency and a cost number.
  const instrumented = (db.prepare(
    'SELECT COUNT(*) AS c FROM systems WHERE p95_ms IS NOT NULL OR cost_per_1k IS NOT NULL',
  ).get() as { c: number }).c > 0;

  const trained = db.prepare("SELECT id, title, metric_name, metric_value, baseline_value FROM systems WHERE kind = 'trained_model' AND metric_value IS NOT NULL").all() as Row[];
  const kernels = db.prepare("SELECT id, title, metric_value, baseline_value FROM systems WHERE kind = 'kernel' AND metric_value IS NOT NULL AND baseline_value IS NOT NULL").all() as Row[];
  const serving = db.prepare("SELECT id, title, metric_name, metric_value FROM systems WHERE kind = 'serving_stack' AND metric_value IS NOT NULL").all() as Row[];
  const evalSystems = db.prepare(
    "SELECT id, title, metric_name, metric_value FROM systems WHERE metric_value IS NOT NULL AND (metric_name LIKE '%perplexity%' OR metric_name LIKE '%pass@%' OR metric_name LIKE '%pass^%' OR metric_name LIKE '%accuracy%' OR metric_name LIKE '%recall%' OR metric_name LIKE '%precision%' OR metric_name LIKE '%CORE%' OR metric_name LIKE '%kappa%' OR metric_name LIKE '%ndcg%' OR metric_name LIKE '%mrr%' OR metric_name LIKE '%faithful%')",
  ).all() as Row[];
  const prRows = db.prepare("SELECT id, title, repo_url FROM systems WHERE status = 'shipped' AND title LIKE 'PR:%'").all() as Row[];

  const seedCount = db.prepare('SELECT COUNT(DISTINCT seed) AS c FROM experiments WHERE system_id = ? AND metric_name = ? AND seed IS NOT NULL');
  const spreadFor = (systemId: unknown, metric: unknown): { nSeeds: number; withinNoise: boolean | null } => {
    const c = (seedCount.get(systemId, metric) as { c: number }).c;
    const values = (db.prepare('SELECT metric_value FROM experiments WHERE system_id = ? AND metric_name = ? AND metric_value IS NOT NULL').all(systemId, metric) as Array<{ metric_value: number }>).map((r) => r.metric_value);
    if (values.length < 3) return { nSeeds: c, withinNoise: null };
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const spread = Math.max(...values) - Math.min(...values);
    const sys = db.prepare('SELECT baseline_value FROM systems WHERE id = ?').get(systemId) as { baseline_value: number | null };
    if (sys.baseline_value === null) return { nSeeds: c, withinNoise: null };
    return { nSeeds: c, withinNoise: Math.abs(mean - sys.baseline_value) <= spread };
  };

  const results: RungResult[] = [];

  results.push({
    rung: 1, title: 'From scratch fundamentals',
    status: studyCount >= 20 ? 'SOLID' : studyCount > 0 ? 'PARTIAL' : 'MISSING',
    evidence: `${studyCount} shipped study systems`,
    rule: '20 or more shipped study systems',
  });

  const product = products[0];
  results.push({
    rung: 2, title: 'A working system others can run',
    status: product ? (s(product.deployed_url) || s(product.repo_url) ? 'SOLID' : 'PARTIAL') : 'MISSING',
    evidence: product
      ? `${s(product.title)} (${s(product.deployed_url) || s(product.repo_url)})${instrumented ? ' — instrumented' : ' — no p95 or cost recorded yet'}`
      : 'no shipped product system row',
    rule: "a shipped systems row of kind 'product' with a repo or deployed URL (v3: record p95_ms and cost_per_1k on it)",
  });

  const trainedWithSeeds = trained.map((t) => ({ t, sp: spreadFor(t.id, t.metric_name) })).filter((x) => x.sp.nSeeds >= 3);
  results.push({
    rung: 3, title: 'A trained model with a reported metric',
    status: trainedWithSeeds.length > 0 ? 'SOLID' : trained.length > 0 ? 'PARTIAL' : 'MISSING',
    evidence: trainedWithSeeds.length > 0 ? `${s(trainedWithSeeds[0]?.t.title)} with ${trainedWithSeeds[0]?.sp.nSeeds} seeds` : trained.length > 0 ? `${s(trained[0]?.title)} has a metric but fewer than 3 seeds` : 'no trained_model system with a metric',
    rule: 'a trained_model system with a metric and 3 or more seeded experiment runs',
  });

  const winningKernel = kernels.find((k) => (n(k.metric_value) ?? 0) > (n(k.baseline_value) ?? Infinity) || (n(k.metric_value) ?? Infinity) < (n(k.baseline_value) ?? 0));
  results.push({
    rung: 4, title: 'A measured performance win',
    status: winningKernel ? 'SOLID' : kernels.length > 0 ? 'PARTIAL' : 'MISSING',
    evidence: winningKernel ? `${s(winningKernel.title)}: ${s(winningKernel.metric_value)} vs baseline ${s(winningKernel.baseline_value)}` : 'no kernel system with metric and baseline',
    rule: 'a kernel system whose measured metric differs from its reference baseline',
  });

  const reproduced = trained.map((t) => ({ t, sp: spreadFor(t.id, t.metric_name) })).find((x) => x.sp.withinNoise === true);
  results.push({
    rung: 5, title: 'A reproduction of a published result',
    status: reproduced ? 'SOLID' : 'MISSING',
    evidence: reproduced ? `${s(reproduced.t.title)}: mean within spread of published ${s(reproduced.t.baseline_value)}` : 'no system whose seeded mean matches its published baseline within the spread',
    rule: 'a system with 3 or more seeds whose mean metric sits within the seed spread of its recorded published baseline',
  });

  results.push({
    rung: 6, title: 'A merged open source contribution',
    status: prRows.length > 0 ? 'SOLID' : 'MISSING',
    evidence: prRows.length > 0 ? `${s(prRows[0]?.title)}` : "no shipped systems row titled 'PR: <repo>' (ship one when a PR merges)",
    rule: "a shipped systems row titled 'PR: <repo>' with the PR URL as repo_url",
  });

  results.push({
    rung: 7, title: 'An eval harness with results',
    status: evalSystems.length > 0 ? 'SOLID' : 'MISSING',
    evidence: evalSystems.length > 0 ? `${s(evalSystems[0]?.title)}: ${s(evalSystems[0]?.metric_name)} = ${s(evalSystems[0]?.metric_value)}` : 'no system with a measured eval metric (perplexity, pass@k, accuracy, recall, precision, CORE)',
    rule: 'a system carrying a real measured eval family metric',
  });

  const capstoneProduct = products.find((p) => s(p.metric_name) !== '' && p.metric_value !== null);
  results.push({
    rung: 8, title: 'A capstone artifact with a number',
    status: capstoneProduct ? 'SOLID' : products.length > 0 ? 'PARTIAL' : 'MISSING',
    evidence: capstoneProduct ? `${s(capstoneProduct.title)}: ${s(capstoneProduct.metric_name)} = ${s(capstoneProduct.metric_value)}` : products.length > 0 ? 'a product exists with no metric attached' : 'no product system',
    rule: 'a shipped product system carrying a real metric (users, revenue, installs)',
  });

  return results;
}

export function renderCapstone(db: Database.Database): string {
  const results = scoreCapstone(db);
  const solid = results.filter((r) => r.status === 'SOLID').length;
  const partial = results.filter((r) => r.status === 'PARTIAL').length;
  const missing = results.filter((r) => r.status === 'MISSING').length;
  const mark = (st: RungResult['status']): string => (st === 'SOLID' ? 'SOLID' : st === 'PARTIAL' ? 'PARTIAL' : 'MISSING');
  const lines: string[] = [
    '# Capstone audit, auto scored',
    '',
    'Scored from the systems and experiments tables. A rung counts only when database rows back',
    'it, and every rung prints the rule it was scored by. Regenerated on every session close;',
    'hand editing is pointless and the generator will not flatter.',
    '',
    `**${solid} solid, ${partial} partial, ${missing} missing.**`,
    '',
  ];
  for (const r of results) {
    lines.push(`## Rung ${r.rung}: ${r.title} [${mark(r.status)}]`);
    lines.push(`- Evidence: ${r.evidence}`);
    lines.push(`- Scoring rule: ${r.rule}`);
    lines.push('');
  }
  lines.push('v3 paths, all runnable on the M4 with no rented hardware:');
  lines.push('- Rungs 3 and 5: a QLoRA fine-tune and a small reproduction through Soup on the MLX backend.');
  lines.push('- Rung 4: a fused Metal kernel via mx.fast.metal_kernel, benchmarked against the MLX reference.');
  lines.push('- Rung 7: the P6 eval harness, with judge-vs-human agreement reported.');
  lines.push('- Rung 6: a merged PR (see /faiz-oss for the measured repo guidance).');
  lines.push('- Rungs 2 and 8: the P2 service deployed, instrumented with p95 and cost, and one real user.');
  return lines.join('\n') + '\n';
}

// ---- CLI -----------------------------------------------------------------------------------

export function writeArtefacts(db: Database.Database, outDir: string, which: string): string[] {
  const targets: Array<{ name: string; file: string; render: (d: Database.Database) => string }> = [
    { name: 'experiments', file: join(outDir, 'notebook', 'EXPERIMENTS.md'), render: renderExperiments },
    { name: 'errors', file: join(outDir, 'notebook', 'ERRORS.md'), render: renderErrors },
    { name: 'ventures', file: join(outDir, 'notebook', 'VENTURES.md'), render: renderVentures },
    { name: 'frontier', file: join(outDir, 'notebook', 'FRONTIER.md'), render: renderFrontier },
    { name: 'capstone', file: join(outDir, 'CAPSTONE.md'), render: renderCapstone },
  ];
  const written: string[] = [];
  for (const t of targets) {
    if (which !== 'all' && which !== t.name) continue;
    mkdirSync(dirname(t.file), { recursive: true });
    writeFileSync(t.file, t.render(db));
    written.push(t.file);
  }
  return written;
}

const invokedDirectly = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (invokedDirectly) {
  const which = process.argv[2] ?? 'all';
  const dbFlag = process.argv.indexOf('--db');
  const outFlag = process.argv.indexOf('--out');
  const dbPath = dbFlag !== -1 && process.argv[dbFlag + 1] ? (process.argv[dbFlag + 1] as string) : DEFAULT_DB;
  const outDir = outFlag !== -1 && process.argv[outFlag + 1] ? (process.argv[outFlag + 1] as string) : REPO_ROOT;
  const db = new Database(dbPath, { readonly: true, fileMustExist: true });
  const written = writeArtefacts(db, outDir, which);
  db.close();
  for (const f of written) console.log(`wrote ${f}`);
}
