// faizos-core — the deterministic brain. All state + math lives here so the model is only
// invoked for judgment (teaching, analysis). Tools are consumed by the /faiz* slash commands.
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { openDb, getMeta, setMeta, logEvent, type DB } from './db.js';
import { updateMastery, bumpConfidence, type EvidenceKind } from './mastery.js';
import { advanceStreak, todayISO } from './streak.js';
import { compileNotebook } from './notebook.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = process.env.FAIZOS_HOME || join(HERE, '..', 'data');
const PROJECT_ROOT = process.env.FAIZOS_PROJECT || join(HERE, '..', '..');
const NOTEBOOK_PATH = process.env.FAIZOS_NOTEBOOK || join(PROJECT_ROOT, 'notebook', 'REVISIONS.md');
mkdirSync(DATA_DIR, { recursive: true });
const db: DB = openDb(join(DATA_DIR, 'faiz.db'));

const now = () => new Date().toISOString();
const ok = (obj: unknown) => ({ content: [{ type: 'text' as const, text: JSON.stringify(obj, null, 2) }] });
const slugify = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 50) || 'build';
const titleFromIdea = (idea: string) => idea.trim().split(/\s+/).slice(0, 8).join(' ').slice(0, 80) || 'Untitled build';
const humanize = (id: string) => id.replace(/-/g, ' ');

interface SkillRow { id: string; name: string; phase: number; must_know: number; build_hint: string; mastery: number; confidence: number; last_seen: string | null; on_curriculum: number; }

function activeMission() {
  const id = getMeta(db, 'current_mission_id');
  if (!id) return null;
  return db.prepare('SELECT id,title,idea,repo_path,created_at FROM missions WHERE id=? AND status=?').get(Number(id), 'active') ?? null;
}

const server = new McpServer({ name: 'faizos-core', version: '0.1.0' });

// ---- faizos_state: everything the /faiz dashboard needs ----
server.registerTool('faizos_state', {
  title: 'FaizOS state',
  description: 'Dashboard state: streak, current build, last shipped, weakest skills, and the single recommended next action. Call this first for /faiz.',
  inputSchema: {},
}, async () => {
  const streak = Number(getMeta(db, 'streak') || 0);
  const best = Number(getMeta(db, 'best_streak') || 0);
  const current = activeMission() as any;
  const lastShipped = db.prepare("SELECT id,title,ship_url,shipped_at FROM missions WHERE status='shipped' ORDER BY shipped_at DESC, id DESC LIMIT 1").get() ?? null;
  const shippedCount = (db.prepare("SELECT COUNT(*) c FROM missions WHERE status='shipped'").get() as { c: number }).c;
  const weakest = db.prepare('SELECT id,name,phase,mastery,must_know FROM skills WHERE on_curriculum=1 ORDER BY mastery ASC, must_know DESC LIMIT 6').all();
  const recentlyMoved = db.prepare('SELECT id,name,mastery,last_seen FROM skills WHERE last_seen IS NOT NULL ORDER BY last_seen DESC LIMIT 4').all();
  const avg = (db.prepare('SELECT AVG(mastery) a FROM skills WHERE on_curriculum=1').get() as { a: number }).a ?? 0;

  let recommended;
  if (current) {
    recommended = { action: 'continue', label: `Continue "${current.title}" — then /faiz-ship when it runs.`, mission_id: current.id };
  } else {
    const target = db.prepare('SELECT id,name,build_hint FROM skills WHERE on_curriculum=1 AND must_know=1 ORDER BY mastery ASC LIMIT 1').get() as any;
    recommended = { action: 'build', label: `Build something that exercises "${target?.name}".`, skill: target?.id, build_hint: target?.build_hint };
  }

  return ok({
    streak, best_streak: best, last_active_date: getMeta(db, 'last_active_date') || null,
    current_build: current,
    last_shipped: lastShipped,
    shipped_count: shippedCount,
    skills: { total: (db.prepare('SELECT COUNT(*) c FROM skills').get() as { c: number }).c, avg_mastery: Number(avg.toFixed(3)), weakest, recently_moved: recentlyMoved },
    recommended_next: recommended,
    menu: ['/faiz-build <idea>', '/faiz-ship', '/faiz-analyze', '/faiz-review'],
  });
});

// ---- faizos_start_build ----
server.registerTool('faizos_start_build', {
  title: 'Start a build',
  description: 'Begin a new build mission from an idea (or a recommended skill). Creates the mission record, sets it current, returns a repo path and the skills it will likely exercise.',
  inputSchema: { idea: z.string().describe('what the user wants to build'), title: z.string().optional(), repo_path: z.string().optional() },
}, async ({ idea, title, repo_path }) => {
  const t = title || titleFromIdea(idea);
  const projectsDir = getMeta(db, 'projects_dir') || 'projects';
  const rp = repo_path || `${projectsDir}/${slugify(t)}`;
  const info = db.prepare('INSERT INTO missions (title,idea,repo_path,status,created_at) VALUES (?,?,?,?,?)').run(t, idea, rp, 'active', now());
  const missionId = Number(info.lastInsertRowid);
  setMeta(db, 'current_mission_id', String(missionId));
  logEvent(db, now(), 'build_start', `#${missionId} ${t}`);
  const likely = db.prepare('SELECT id,name,build_hint FROM skills WHERE on_curriculum=1 AND must_know=1 ORDER BY mastery ASC LIMIT 4').all();
  return ok({ mission_id: missionId, title: t, idea, repo_path: rp, likely_skills: likely, note: `Scaffold a real repo at ${rp} (git init + README), then pair-build. Teach only the theory needed for the next step.` });
});

// ---- faizos_ship ----
server.registerTool('faizos_ship', {
  title: 'Ship a build',
  description: 'Mark a build shipped (deployed/public/merged). Updates the forgiving streak and clears it as the current build. Celebrate, then suggest /faiz-analyze.',
  inputSchema: { mission_id: z.number().optional(), ship_url: z.string().optional() },
}, async ({ mission_id, ship_url }) => {
  const cur = activeMission() as any;
  const id = mission_id ?? cur?.id;
  if (!id) return ok({ error: 'No active build to ship. Start one with /faiz-build.' });
  const m = db.prepare('SELECT id,title FROM missions WHERE id=?').get(id) as any;
  if (!m) return ok({ error: `No mission #${id}.` });

  const today = todayISO();
  db.prepare("UPDATE missions SET status='shipped', shipped_at=?, ship_url=? WHERE id=?").run(today, ship_url ?? null, id);
  if (String(id) === getMeta(db, 'current_mission_id')) setMeta(db, 'current_mission_id', '');

  const s = advanceStreak({ streak: Number(getMeta(db, 'streak') || 0), best: Number(getMeta(db, 'best_streak') || 0), lastActive: getMeta(db, 'last_active_date') || null }, today);
  setMeta(db, 'streak', String(s.streak)); setMeta(db, 'best_streak', String(s.best)); setMeta(db, 'last_active_date', today);
  logEvent(db, now(), 'ship', `#${id} ${m.title}${ship_url ? ' ' + ship_url : ''}`);

  const shippedCount = (db.prepare("SELECT COUNT(*) c FROM missions WHERE status='shipped'").get() as { c: number }).c;
  return ok({ shipped: { mission_id: id, title: m.title, ship_url: ship_url ?? null }, streak: s.streak, best_streak: s.best, grace_used: s.graceUsed, shipped_count: shippedCount, next: 'Run /faiz-analyze to bank the skills you just built.' });
});

// ---- faizos_analyze: learn-from-what-you-built ----
server.registerTool('faizos_analyze', {
  title: 'Analyze a build & update skills',
  description: 'Record which skills a finished build exercised (with an outcome 0..1) and any gaps. Updates mastery deterministically, mints off-curriculum skills as needed, and returns the one gap to teach next. The model infers the skills/outcomes by reading the repo; this tool banks them.',
  inputSchema: {
    mission_id: z.number().optional(),
    skills: z.array(z.object({ id: z.string(), outcome: z.number().min(0).max(1), kind: z.enum(['ship', 'build', 'explain', 'review', 'quiz']).optional() })).describe('skills exercised, with how well (outcome) and evidence kind'),
    gaps: z.array(z.string()).optional().describe('concepts the build should have used but did not, or used incorrectly'),
    notes: z.string().optional(),
  },
}, async ({ mission_id, skills, gaps, notes }) => {
  const today = todayISO();
  const updated: Array<{ id: string; name: string; from: number; to: number }> = [];
  const upd = db.prepare('UPDATE skills SET mastery=?, confidence=?, last_seen=? WHERE id=?');
  const insOff = db.prepare("INSERT INTO skills (id,name,phase,must_know,build_hint,on_curriculum) VALUES (?,?,?,?,?,0)");
  db.transaction(() => {
    for (const s of skills) {
      let row = db.prepare('SELECT id,name,mastery,confidence FROM skills WHERE id=?').get(s.id) as any;
      if (!row) { insOff.run(s.id, humanize(s.id), 0, 0, ''); row = { id: s.id, name: humanize(s.id), mastery: 0, confidence: 0 }; }
      const kind = (s.kind ?? 'build') as EvidenceKind;
      const to = updateMastery(row.mastery, s.outcome, kind);
      upd.run(to, bumpConfidence(row.confidence, kind), today, s.id);
      updated.push({ id: s.id, name: row.name, from: Number(row.mastery.toFixed(3)), to: Number(to.toFixed(3)) });
    }
    for (const g of gaps ?? []) logEvent(db, now(), 'gap', g);
    logEvent(db, now(), 'analyze', notes || `${skills.length} skills, ${(gaps ?? []).length} gaps`);
  })();
  return ok({ mission_id: mission_id ?? null, updated, gaps: gaps ?? [], teach_next: gaps?.[0] ?? null, note: 'Teach teach_next now (just what is needed), then suggest a short follow-up build.' });
});

// ---- faizos_list_skills: for the analyze command to map a repo to known skill ids ----
server.registerTool('faizos_list_skills', {
  title: 'List skills',
  description: 'List skills (optionally filtered) so the model can map a repo to known skill ids before calling faizos_analyze.',
  inputSchema: { phase: z.number().optional(), must_know_only: z.boolean().optional() },
}, async ({ phase, must_know_only }) => {
  let q = 'SELECT id,name,phase,must_know,mastery,confidence,last_seen,on_curriculum,build_hint FROM skills WHERE 1=1';
  const args: any[] = [];
  if (phase !== undefined) { q += ' AND phase=?'; args.push(phase); }
  if (must_know_only) q += ' AND must_know=1';
  q += ' ORDER BY phase, mastery';
  return ok({ skills: db.prepare(q).all(...args) });
});

// ---- faizos_config: journey repo / github / projects dir ----
server.registerTool('faizos_config', {
  title: 'Get/set config',
  description: 'Read or update config: journey_repo (git remote for auto-push, empty = local commits only), github_user, projects_dir.',
  inputSchema: { set: z.object({ journey_repo: z.string().optional(), github_user: z.string().optional(), projects_dir: z.string().optional() }).optional() },
}, async ({ set }) => {
  if (set) {
    for (const k of ['journey_repo', 'github_user', 'projects_dir'] as const) if (set[k] !== undefined) setMeta(db, k, set[k]!);
    logEvent(db, now(), 'config', JSON.stringify(set));
  }
  return ok({ journey_repo: getMeta(db, 'journey_repo'), github_user: getMeta(db, 'github_user'), projects_dir: getMeta(db, 'projects_dir') || 'projects' });
});

// ---- light retrieval: keep the few must-knows fresh ----
server.registerTool('faizos_review_queue', {
  title: 'Review queue (must-knows)',
  description: 'Return the must-know fundamentals most in need of a short retrieval check (low mastery / not seen lately).',
  inputSchema: { limit: z.number().optional() },
}, async ({ limit }) => {
  const items = db.prepare('SELECT id,name,build_hint,mastery,last_seen FROM skills WHERE must_know=1 ORDER BY mastery ASC, (last_seen IS NULL) DESC, last_seen ASC LIMIT ?').all(limit ?? 5);
  return ok({ items, note: 'Ask the user to recall each (no notes), grade briefly, then call faizos_record_review.' });
});
server.registerTool('faizos_record_review', {
  title: 'Record review results',
  description: 'Record short-review outcomes (0..1) for must-know skills. Updates mastery with review-weight evidence.',
  inputSchema: { results: z.array(z.object({ id: z.string(), outcome: z.number().min(0).max(1) })) },
}, async ({ results }) => {
  const today = todayISO();
  const updated: any[] = [];
  const upd = db.prepare('UPDATE skills SET mastery=?, confidence=?, last_seen=? WHERE id=?');
  db.transaction(() => {
    for (const r of results) {
      const row = db.prepare('SELECT mastery,confidence,name FROM skills WHERE id=?').get(r.id) as any;
      if (!row) continue;
      const to = updateMastery(row.mastery, r.outcome, 'review');
      upd.run(to, bumpConfidence(row.confidence, 'review'), today, r.id);
      updated.push({ id: r.id, name: row.name, from: Number(row.mastery.toFixed(3)), to: Number(to.toFixed(3)) });
    }
  })();
  return ok({ updated });
});

// ================= Memory + self-improving feedback loop =================

const LEARNING_PROFILE =
  'Teach with the Brick Method: start below the floor, ONE tiny concept per step, ask a small ' +
  'question, WAIT for his answer, then reveal the answer + the reasoning. Define each term in one ' +
  'sentence + an analogy. He does the doing. No fluff. Small lessons. End with a rich revision note.';

// ---- faizos_lesson_start: load what we've learned about teaching him ----
server.registerTool('faizos_lesson_start', {
  title: 'Start a lesson',
  description: 'Call at the START of a lesson/build. Returns the learning profile, accumulated teaching INSIGHTS to apply, weakest skills, and recent struggles. This is how FaizOS applies what it learned from past lessons.',
  inputSchema: { topic: z.string().optional() },
}, async ({ topic }) => {
  const insights = db.prepare('SELECT note, weight FROM insights WHERE active=1 ORDER BY weight DESC, ts DESC LIMIT 8').all();
  const weak = db.prepare('SELECT id,name,mastery,must_know FROM skills WHERE on_curriculum=1 ORDER BY mastery ASC, must_know DESC LIMIT 5').all();
  const recentStruggles = (db.prepare('SELECT struggles FROM lessons ORDER BY id DESC LIMIT 3').all() as Array<{ struggles: string }>)
    .flatMap((l) => { try { return JSON.parse(l.struggles); } catch { return []; } });
  return ok({
    topic: topic ?? null,
    learning_profile: LEARNING_PROFILE,
    insights_to_apply: insights,
    weak_skills: weak,
    recent_struggles: recentStruggles,
    current_build: activeMission(),
    note: 'Apply insights_to_apply + recent_struggles proactively. Teach one brick at a time.',
  });
});

// ---- faizos_record_lesson: store the lesson + distil new insights (improve) ----
server.registerTool('faizos_record_lesson', {
  title: 'Record a lesson',
  description: 'Call at the END of a lesson. Stores what happened and appends 1-2 new teaching INSIGHTS (distilled by you from how the lesson went) so the NEXT lesson improves. Insights are deduped; repeats get reinforced (weight++).',
  inputSchema: {
    topic: z.string(),
    mission_id: z.number().optional(),
    skills: z.array(z.string()).optional(),
    struggles: z.array(z.string()).optional(),
    worked: z.array(z.string()).optional(),
    new_insights: z.array(z.string()).optional().describe('1-2 concrete, reusable teaching adjustments for next time'),
    difficulty_felt: z.enum(['too_easy', 'right', 'too_hard']).optional(),
  },
}, async ({ topic, mission_id, skills, struggles, worked, new_insights, difficulty_felt }) => {
  const ts = now();
  db.prepare('INSERT INTO lessons (ts,topic,mission_id,skills,struggles,worked,difficulty_felt) VALUES (?,?,?,?,?,?,?)')
    .run(ts, topic, mission_id ?? null, JSON.stringify(skills ?? []), JSON.stringify(struggles ?? []), JSON.stringify(worked ?? []), difficulty_felt ?? null);
  const upsert = db.prepare('INSERT INTO insights (ts,note,weight) VALUES (?,?,1) ON CONFLICT(note) DO UPDATE SET weight=weight+1, ts=excluded.ts, active=1');
  for (const n of new_insights ?? []) if (n.trim()) upsert.run(ts, n.trim());
  logEvent(db, ts, 'lesson', `${topic} (+${(new_insights ?? []).length} insights)`);
  const active = db.prepare('SELECT note, weight FROM insights WHERE active=1 ORDER BY weight DESC LIMIT 8').all();
  return ok({ recorded: topic, new_insights: new_insights ?? [], active_insights: active, note: 'These load at the next faizos_lesson_start.' });
});

// ---- faizos_save_revision: store note + regenerate the compiled notebook ----
server.registerTool('faizos_save_revision', {
  title: 'Save a revision note',
  description: 'Call at lesson end with the full revision-note markdown. Stores it and REGENERATES the compiled notebook file (notebook/REVISIONS.md) from all revisions.',
  inputSchema: { topic: z.string(), note_md: z.string() },
}, async ({ topic, note_md }) => {
  db.prepare('INSERT INTO revisions (ts,topic,note_md) VALUES (?,?,?)').run(now(), topic, note_md);
  const all = db.prepare('SELECT ts, topic, note_md FROM revisions').all() as Array<{ ts: string; topic: string; note_md: string }>;
  mkdirSync(dirname(NOTEBOOK_PATH), { recursive: true });
  writeFileSync(NOTEBOOK_PATH, compileNotebook(all));
  return ok({ saved: topic, notebook_path: NOTEBOOK_PATH, entries: all.length });
});

// ---- faizos_notes: read the notebook ----
server.registerTool('faizos_notes', {
  title: 'Read the revision notebook',
  description: 'Return recent revision notes + the compiled notebook path. For /faiz-notes.',
  inputSchema: { limit: z.number().optional() },
}, async ({ limit }) => {
  const recent = db.prepare('SELECT ts, topic, note_md FROM revisions ORDER BY id DESC LIMIT ?').all(limit ?? 10);
  const count = (db.prepare('SELECT COUNT(*) c FROM revisions').get() as { c: number }).c;
  return ok({ notebook_path: NOTEBOOK_PATH, count, recent });
});

await server.connect(new StdioServerTransport());
