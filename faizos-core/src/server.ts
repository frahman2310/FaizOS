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
import { PHASES, MISSION_TEMPLATES, MODULES } from './curriculum.js';
import { initCard, review as fsrsReview, gradeFromOutcome, type Card } from './fsrs.js';
import { migrateUp } from './migrate.js';
import {
  activeBuild, activeVenture, currentTrack, grantHint, logExperiment, recordErrors,
  recordReview, specBuild, studentWroteRatio, topOpenErrors, trackStatus, unlockBuild,
} from './v2.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = process.env.FAIZOS_HOME || join(HERE, '..', 'data');
const PROJECT_ROOT = process.env.FAIZOS_PROJECT || join(HERE, '..', '..');
const NOTEBOOK_PATH = process.env.FAIZOS_NOTEBOOK || join(PROJECT_ROOT, 'notebook', 'REVISIONS.md');
mkdirSync(DATA_DIR, { recursive: true });
const DB_PATH = join(DATA_DIR, 'faiz.db');
const db: DB = openDb(DB_PATH);
migrateUp(DB_PATH); // idempotent: brings any database (including fresh smoke-test ones) to the v2 schema

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

  // v2, build heavy: the active write-from-empty build and venture lead the dashboard.
  const build = activeBuild(db);
  const venture = activeVenture(db);
  const track = currentTrack(db);
  const ratio = studentWroteRatio(db);
  // v3: mode, the guidance policy for the current build, and any rebuild that has come due.
  const { currentMode, rebuildsDue, guidanceFor, costDrillRecord } = await import('./v3.js');
  const mode = currentMode(db);
  const due = rebuildsDue(db);
  const guidance = build ? guidanceFor(db, build.id) : null;

  return ok({
    active_build: build
      ? { ...build, note: 'He writes the solution file. The guard blocks anyone else. /faiz-hint for help, /faiz-unlock to hand it over (recorded).' }
      : null,
    active_venture: venture,
    mode,
    guidance,
    rebuilds_due: due,
    current_track: track
      ? { code: track.code, title: track.title, status: track.status, kind: track.kind, guidance_policy: track.guidance_policy, current_as_of: track.current_as_of }
      : null,
    open_errors: topOpenErrors(db, 3),
    student_wrote: ratio,
    streak, best_streak: best, last_active_date: getMeta(db, 'last_active_date') || null,
    pending_close: getMeta(db, 'pending_close') || null,
    current_build: current,
    last_shipped: lastShipped,
    shipped_count: shippedCount,
    skills: { total: (db.prepare('SELECT COUNT(*) c FROM skills').get() as { c: number }).c, avg_mastery: Number(avg.toFixed(3)), weakest, recently_moved: recentlyMoved },
    recommended_next: due.length
      ? { action: 'rebuild', label: `Rebuild "${due[0]?.topic ?? due[0]?.solution_path}" from empty, unaided. It is provisional until you do.`, build_id: due[0]?.id }
      : recommended,
    cost_drills: costDrillRecord(db),
    menu: ['/faiz-learn [track|next]', '/faiz-build <idea>', '/faiz-spec', '/faiz-hint', '/faiz-review', '/faiz-run', '/faiz-errors', '/faiz-cost', '/faiz-oss', '/faiz-ship'],
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
  inputSchema: {
    mission_id: z.number().optional(),
    ship_url: z.string().optional(),
    kind: z.enum(['trained_model', 'serving_stack', 'kernel', 'product', 'study']).optional().describe('v2: what kind of system this is. Defaults to study (no metric).'),
    metric_name: z.string().optional().describe('v2: the real measured metric, e.g. val_loss, tokens_per_sec'),
    metric_value: z.number().optional(),
    baseline_value: z.number().optional(),
    deployed_url: z.string().optional(),
    track_code: z.string().optional(),
  },
}, async ({ mission_id, ship_url, kind, metric_name, metric_value, baseline_value, deployed_url, track_code }) => {
  const cur = activeMission() as any;
  const id = mission_id ?? cur?.id;
  if (!id) return ok({ error: 'No active build to ship. Start one with /faiz-build.' });
  const m = db.prepare('SELECT id,title FROM missions WHERE id=?').get(id) as any;
  if (!m) return ok({ error: `No mission #${id}.` });

  const today = todayISO();
  db.prepare("UPDATE missions SET status='shipped', shipped_at=?, ship_url=? WHERE id=?").run(today, ship_url ?? null, id);
  if (String(id) === getMeta(db, 'current_mission_id')) setMeta(db, 'current_mission_id', '');

  // v2: every ship also lands in systems, the unit the capstone is scored from. Study builds
  // carry no metric, truthfully. Only real measured numbers belong in metric_value.
  const trackRow = track_code ? (db.prepare('SELECT id FROM tracks WHERE code=?').get(track_code) as { id: number } | undefined) : undefined;
  db.prepare(
    `INSERT INTO systems (track_id, title, repo_url, kind, status, metric_name, metric_value, baseline_value, deployed_url, created_at, shipped_at)
     VALUES (?, ?, ?, ?, 'shipped', ?, ?, ?, ?, ?, ?)`,
  ).run(trackRow?.id ?? null, m.title, ship_url ?? null, kind ?? 'study', metric_name ?? null, metric_value ?? null, baseline_value ?? null, deployed_url ?? null, now(), today);

  const s = advanceStreak({ streak: Number(getMeta(db, 'streak') || 0), best: Number(getMeta(db, 'best_streak') || 0), lastActive: getMeta(db, 'last_active_date') || null }, today);
  setMeta(db, 'streak', String(s.streak)); setMeta(db, 'best_streak', String(s.best)); setMeta(db, 'last_active_date', today);
  logEvent(db, now(), 'ship', `#${id} ${m.title}${ship_url ? ' ' + ship_url : ''}`);
  setMeta(db, 'pending_close', String(id)); // triggers auto-analyze + revision before the session ends

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
  title: 'Review queue (must-knows, FSRS)',
  description: 'Return must-know fundamentals that are DUE for a short retrieval check (FSRS-scheduled), plus new built-but-unscheduled must-knows. Keep it light — building is the main event.',
  inputSchema: { limit: z.number().optional() },
}, async ({ limit }) => {
  const today = todayISO();
  const n = limit ?? 5;
  const due = db.prepare(
    'SELECT s.id, s.name, s.build_hint, r.due, r.stability FROM reviews r JOIN skills s ON s.id=r.skill_id WHERE s.must_know=1 AND r.due<=? ORDER BY r.due ASC LIMIT ?',
  ).all(today, n) as Array<Record<string, unknown>>;
  const rest = n - due.length;
  const fresh = rest > 0
    ? db.prepare("SELECT id, name, build_hint FROM skills WHERE must_know=1 AND last_seen IS NOT NULL AND id NOT IN (SELECT skill_id FROM reviews) ORDER BY mastery ASC LIMIT ?").all(rest) as Array<Record<string, unknown>>
    : [];
  const items = [...due.map((d) => ({ ...d, status: 'due' })), ...fresh.map((f) => ({ ...f, status: 'new' }))];
  return ok({ items, note: 'Ask him to recall each (no notes), grade briefly, then faizos_record_review. Keep it short.' });
});
server.registerTool('faizos_record_review', {
  title: 'Record review results (FSRS)',
  description: 'Record short-review outcomes (0..1). Updates the FSRS card (schedules the next review) and bumps mastery with review-weight evidence.',
  inputSchema: { results: z.array(z.object({ id: z.string(), outcome: z.number().min(0).max(1) })) },
}, async ({ results }) => {
  const today = todayISO();
  const updated: Array<Record<string, unknown>> = [];
  const getCard = db.prepare('SELECT stability, difficulty, last, due, reps FROM reviews WHERE skill_id=?');
  const upsertCard = db.prepare('INSERT INTO reviews (skill_id,stability,difficulty,last,due,reps) VALUES (?,?,?,?,?,?) ON CONFLICT(skill_id) DO UPDATE SET stability=excluded.stability, difficulty=excluded.difficulty, last=excluded.last, due=excluded.due, reps=excluded.reps');
  const updSkill = db.prepare('UPDATE skills SET mastery=?, confidence=?, last_seen=? WHERE id=?');
  db.transaction(() => {
    for (const r of results) {
      const row = db.prepare('SELECT mastery,confidence,name FROM skills WHERE id=?').get(r.id) as { mastery: number; confidence: number; name: string } | undefined;
      if (!row) continue;
      const grade = gradeFromOutcome(r.outcome);
      const existing = getCard.get(r.id) as Card | undefined;
      const card = existing ? fsrsReview(existing, grade, today) : initCard(grade, today);
      upsertCard.run(r.id, card.stability, card.difficulty, card.last, card.due, card.reps);
      const to = updateMastery(row.mastery, r.outcome, 'review');
      updSkill.run(to, bumpConfidence(row.confidence, 'review'), today, r.id);
      updated.push({ id: r.id, name: row.name, from: Number(row.mastery.toFixed(3)), to: Number(to.toFixed(3)), next_due: card.due });
    }
  })();
  return ok({ updated });
});

// ================= AI Opportunity Radar (AI-only research -> buildable missions) =================
server.registerTool('faizos_radar_save', {
  title: 'Save radar opportunities',
  description: 'Store buildable AI opportunities found by /faiz-radar (AI-only; Pakistan-first + global remote/tech). Each has buildable_as = a concrete first shippable project.',
  inputSchema: { opportunities: z.array(z.object({ title: z.string(), market: z.string().optional(), feasibility: z.string().optional(), roi_note: z.string().optional(), buildable_as: z.string().optional() })) },
}, async ({ opportunities }) => {
  const ts = now();
  const ins = db.prepare('INSERT INTO radar (ts,title,market,feasibility,roi_note,buildable_as) VALUES (?,?,?,?,?,?)');
  const saved: Array<{ id: number; title: string }> = [];
  db.transaction(() => {
    for (const o of opportunities) {
      const info = ins.run(ts, o.title, o.market ?? '', o.feasibility ?? '', o.roi_note ?? '', o.buildable_as ?? '');
      saved.push({ id: Number(info.lastInsertRowid), title: o.title });
    }
  })();
  logEvent(db, ts, 'radar', `${opportunities.length} opportunities`);
  return ok({ saved, note: 'Offer to turn one into a mission with faizos_start_build({ idea: buildable_as }).' });
});
server.registerTool('faizos_radar_list', {
  title: 'List radar opportunities',
  description: 'Return recent AI opportunities found by the radar.',
  inputSchema: { limit: z.number().optional() },
}, async ({ limit }) => {
  return ok({ items: db.prepare('SELECT id,ts,title,market,feasibility,roi_note,buildable_as FROM radar ORDER BY id DESC LIMIT ?').all(limit ?? 10) });
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

  // v2, build heavy ordering: the thing he is WRITING comes first, then the error categories
  // that must weight the rules card, then track and frontier context. Teaching notes come last.
  const build = activeBuild(db);
  const track = currentTrack(db);
  const trackDetail = track ? trackStatus(db, track.code) : null;
  const dueReviews = db.prepare(
    'SELECT COUNT(*) c FROM reviews r JOIN skills s ON s.id=r.skill_id WHERE s.must_know=1 AND r.due<=?',
  ).get(todayISO()) as { c: number };

  return ok({
    active_build: build,
    open_error_categories: topOpenErrors(db, 3),
    current_track: trackDetail
      ? { code: trackDetail.track.code, title: trackDetail.track.title, status: trackDetail.track.status, completion_test: trackDetail.track.completion_test, current_as_of: trackDetail.track.current_as_of, frontier_notes: trackDetail.frontier_notes }
      : null,
    due_reviews: dueReviews.c,
    active_venture: activeVenture(db),
    topic: topic ?? null,
    learning_profile: LEARNING_PROFILE,
    insights_to_apply: insights,
    weak_skills: weak,
    recent_struggles: recentStruggles,
    current_build: activeMission(),
    note: 'Weight the Python rules card toward open_error_categories. He writes the whole solution file; hints only through /faiz-hint, one rung at a time.',
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
    mode: z.enum(['course', 'build']).optional(),
    depth: z.enum(['explain', 'flow', 'ship']).optional(),
    lesson_id: z.number().optional().describe('update an existing lesson row created by faizos_spec_build instead of inserting a new one'),
    errors: z.array(z.object({
      category: z.string().describe('taxonomy category, e.g. expression-vs-statement, inverse-relationship, ordering-pairing'),
      description: z.string(),
      code_excerpt: z.string().optional(),
      rule_broken: z.string().optional(),
    })).optional().describe('every genuine mistake this lesson, classified into the taxonomy'),
  },
}, async ({ topic, mission_id, skills, struggles, worked, new_insights, difficulty_felt, mode, depth, lesson_id, errors }) => {
  const ts = now();
  if (lesson_id !== undefined) {
    db.prepare('UPDATE lessons SET topic=?, mission_id=COALESCE(?, mission_id), skills=?, struggles=?, worked=?, difficulty_felt=?, mode=COALESCE(?, mode), depth=COALESCE(?, depth) WHERE id=?')
      .run(topic, mission_id ?? null, JSON.stringify(skills ?? []), JSON.stringify(struggles ?? []), JSON.stringify(worked ?? []), difficulty_felt ?? null, mode ?? null, depth ?? null, lesson_id);
  } else {
    db.prepare('INSERT INTO lessons (ts,topic,mission_id,skills,struggles,worked,difficulty_felt,mode,depth) VALUES (?,?,?,?,?,?,?,?,?)')
      .run(ts, topic, mission_id ?? null, JSON.stringify(skills ?? []), JSON.stringify(struggles ?? []), JSON.stringify(worked ?? []), difficulty_felt ?? null, mode ?? 'course', depth ?? 'explain');
  }
  const errorsRecorded = recordErrors(db, errors ?? []);
  const upsert = db.prepare('INSERT INTO insights (ts,note,weight,mode) VALUES (?,?,1,?) ON CONFLICT(note) DO UPDATE SET weight=weight+1, ts=excluded.ts, active=1');
  for (const n of new_insights ?? []) if (n.trim()) upsert.run(ts, n.trim(), mode ?? 'course');
  logEvent(db, ts, 'lesson', `${topic} (+${(new_insights ?? []).length} insights, ${errorsRecorded} errors classified)`);
  setMeta(db, 'pending_close', ''); // loop closed for this build
  const active = db.prepare('SELECT note, weight FROM insights WHERE active=1 ORDER BY weight DESC LIMIT 8').all();
  return ok({ recorded: topic, errors_recorded: errorsRecorded, new_insights: new_insights ?? [], active_insights: active, note: 'These load at the next faizos_lesson_start.' });
});

// ---- faizos_save_revision: store note + regenerate the compiled notebook ----
server.registerTool('faizos_save_revision', {
  title: 'Save a revision note',
  description: 'Call at lesson end with the full revision-note markdown. Stores it and REGENERATES the compiled notebook file (notebook/REVISIONS.md) from all revisions.',
  inputSchema: { topic: z.string(), note_md: z.string() },
}, async ({ topic, note_md }) => {
  db.prepare('DELETE FROM revisions WHERE topic=?').run(topic); // dedup by topic: re-saving replaces
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

// ---- faizos_curriculum: the map + suggested next builds (free-build anytime) ----
server.registerTool('faizos_curriculum', {
  title: 'Curriculum map & suggested builds',
  description: 'The full Phases 0–15 map with your mastery per phase, plus 2–3 suggested next missions from the roadmap (each ends in a verifiable number). You can always FREE-BUILD anything instead — describe it and it becomes a mission; the analyzer back-fills the skills.',
  inputSchema: {},
}, async () => {
  const rows = db.prepare('SELECT phase, AVG(mastery) avg, COUNT(*) n FROM skills WHERE on_curriculum=1 GROUP BY phase ORDER BY phase').all() as Array<{ phase: number; avg: number; n: number }>;
  const phases = rows.map((r) => ({ phase: r.phase, name: PHASES[r.phase] ?? `Phase ${r.phase}`, skills: r.n, avg_mastery: Number((r.avg ?? 0).toFixed(2)) }));
  const seen = new Set((db.prepare('SELECT id FROM skills WHERE last_seen IS NOT NULL').all() as Array<{ id: string }>).map((r) => r.id));
  const suggested = MISSION_TEMPLATES.filter((m) => !m.skills.every((s) => seen.has(s))).slice(0, 3);
  return ok({
    phases,
    frontier_phase: suggested[0]?.phase ?? 15,
    frontier_name: PHASES[suggested[0]?.phase ?? 15],
    suggested_missions: suggested,
    free_build: 'Build ANYTHING — describe it and it becomes a mission on the map; the analyzer back-fills the skills it exercised. The curriculum guides, it never forces.',
  });
});

// ---- faizos_progress: a course-wide progress bar (show it with the revision summary) ----
server.registerTool('faizos_progress', {
  title: 'Course progress bar',
  description: 'Course coverage across the 20 modules (~5% each): overall coverage %, modules complete, skills touched, avg mastery, missions shipped, and a rendered per-module progress bar. Show its `rendered` block with the revision summary.',
  inputSchema: {},
}, async () => {
  const skills = db.prepare('SELECT phase, mastery, last_seen FROM skills WHERE on_curriculum=1').all() as Array<{ phase: number; mastery: number; last_seen: string | null }>;
  const total = skills.length;
  const touched = skills.filter((s) => s.last_seen).length;
  const overall = total ? skills.reduce((a, s) => a + s.mastery, 0) / total : 0;
  const shipped = (db.prepare("SELECT COUNT(*) c FROM missions WHERE status='shipped'").get() as { c: number }).c;
  const byPhase = new Map<number, { sum: number; n: number }>();
  for (const s of skills) { const p = byPhase.get(s.phase) ?? { sum: 0, n: 0 }; p.sum += s.mastery; p.n++; byPhase.set(s.phase, p); }
  const bar = (f: number, w = 20) => { const x = Math.max(0, Math.min(1, f)); const k = Math.round(x * w); return '▓'.repeat(k) + '░'.repeat(w - k); };
  const pct = (f: number) => `${Math.round(f * 100)}%`;
  // Coverage = the course as 20 modules (~5% each). A module's coverage = its skills touched / total.
  const touchedIds = new Set((db.prepare('SELECT id FROM skills WHERE last_seen IS NOT NULL').all() as Array<{ id: string }>).map((r) => r.id));
  const mods = MODULES.map((m) => ({ id: m.id, name: m.name, cov: m.skills.filter((s) => touchedIds.has(s)).length / m.skills.length }));
  const coverage = mods.reduce((a, m) => a + m.cov, 0) / MODULES.length;
  const done = mods.filter((m) => m.cov >= 0.999).length;
  const modLines = mods.map((m) => `  ${String(m.id).padStart(2)}. ${m.name.padEnd(32).slice(0, 32)} ${bar(m.cov, 10)} ${pct(m.cov)}`);
  const rendered = [
    `Course coverage — 20 modules, ~5% each   (${done}/20 complete)`,
    `  OVERALL  ${bar(coverage)} ${pct(coverage)}   ·  ${done}/20 modules · ${touched} skills touched · avg mastery ${pct(overall)} · ${shipped} ships`,
    '',
    ...modLines,
  ].join('\n');
  return ok({ coverage_pct: Math.round(coverage * 100), modules_done: done, modules_total: 20, avg_mastery_pct: Math.round(overall * 100), skills_touched: touched, missions_shipped: shipped, rendered });
});

// ================= v2: the write-from-empty loop =================

// ---- faizos_track_status ----
server.registerTool('faizos_track_status', {
  title: 'Track status',
  description: 'One track (or the current one if no code given): position, status, completion test, its systems with metrics, skill coverage, and recent frontier notes affecting it.',
  inputSchema: { track_code: z.string().optional().describe('T0..T10; omit for the current track') },
}, async ({ track_code }) => {
  const code = track_code ?? currentTrack(db)?.code;
  if (!code) return ok({ error: 'no tracks seeded' });
  const status = trackStatus(db, code);
  if (!status) return ok({ error: `no track ${code}` });
  return ok(status);
});

// ---- faizos_spec_build: opens a write-from-empty build ----
server.registerTool('faizos_spec_build', {
  title: 'Spec a write-from-empty build',
  description: 'Creates the lesson row and the build row (state awaiting_student) and returns the solution/test paths plus the top open error categories to weight the Python rules card. After calling this: post the plain-English design brief, post the rules card, WRITE THE FAILING TEST FILE at test_path, and then the student writes solution_path from empty. The guard blocks anyone else writing it.',
  inputSchema: {
    topic: z.string(),
    slug: z.string().optional(),
    mode: z.enum(['course', 'build']).optional(),
    depth: z.enum(['explain', 'flow', 'ship']).optional(),
    track_code: z.string().optional(),
  },
}, async (args) => {
  const result = specBuild(db, args);
  logEvent(db, now(), 'spec_build', `#${result.build_id} ${args.topic} -> ${result.solution_path}`);
  return ok({
    ...result,
    contract: 'Design brief in plain English (no code). Rules card: 3-6 entries, construct -> meaning -> the one rule that trips people, weighted toward open_error_categories. Failing tests at test_path. Nothing else. He writes solution_path from an empty file.',
  });
});

// ---- faizos_hint: one rung, never skips ----
server.registerTool('faizos_hint', {
  title: 'Serve one hint rung',
  description: 'Grants exactly one hint rung for the active build, strictly in order (1..4). Rung 4 is never given unprompted. The tool returns the FRAME for what the hint may contain; you author the hint within that frame and nothing more.',
  inputSchema: { build_id: z.number().optional(), rung: z.number() },
}, async ({ build_id, rung }) => {
  const id = build_id ?? activeBuild(db)?.id;
  if (id === undefined) return ok({ granted: false, reason: 'no active build' });
  const result = grantHint(db, id, rung);
  if (result.granted) logEvent(db, now(), 'hint', `build #${id} rung ${result.rung}`);
  return ok(result);
});

// ---- faizos_review_code: the three-pass review, recorded ----
server.registerTool('faizos_review_code', {
  title: 'Record a code review',
  description: 'Call AFTER running the three-pass review of the STUDENT\'S code (1: his code line by line in plain English; 2: diff against reference classified correctness/clarity/taste; 3: error classification). Writes code_reviews and the error taxonomy, and lands the build in PROVISIONAL with a 14 day rebuild date. Requires faizos_reveal_contrast to have run first.',
  inputSchema: {
    build_id: z.number(),
    student_code: z.string(),
    reference_code: z.string().optional(),
    diff_summary: z.string().optional(),
    correctness_diffs: z.array(z.string()).optional(),
    taste_diffs: z.array(z.string()).optional(),
    errors: z.array(z.object({
      category: z.string(),
      description: z.string(),
      code_excerpt: z.string().optional(),
      rule_broken: z.string().optional(),
    })).optional(),
  },
}, async (args) => {
  const { hasRevealed } = await import('./v3.js');
  if (!hasRevealed(db, args.build_id)) {
    return ok({
      recorded: false,
      reason: 'Run faizos_reveal_contrast first. Productive failure is generate THEN instruct: he reads the reference, diffs it against his own reasoning, and writes down what differed. Skipping that step is not what the evidence supports.',
    });
  }
  const result = recordReview(db, args);
  logEvent(db, now(), 'review', `build #${args.build_id}: ${result.errors_recorded} errors classified`);
  return ok({ ...result, note: 'Most differences are taste. Say so, or he learns to write your code instead of learning to write.' });
});

// ---- faizos_log_experiment ----
server.registerTool('faizos_log_experiment', {
  title: 'Log an experiment run',
  description: 'Record one run against a system: config, seed, metric, hardware, cost. Returns the seed spread once the system+metric has 3 or more runs. A claim is only real if the gain clears the spread.',
  inputSchema: {
    system_id: z.number(),
    metric_name: z.string(),
    metric_value: z.number(),
    config_json: z.string().optional(),
    seed: z.number().optional(),
    gpu_type: z.string().optional(),
    gpu_hours: z.number().optional(),
    cost_usd: z.number().optional(),
    notes: z.string().optional(),
  },
}, async (args) => {
  const result = logExperiment(db, args);
  logEvent(db, now(), 'experiment', `system #${args.system_id} ${args.metric_name}=${args.metric_value}`);
  return ok(result);
});

// ---- faizos_error_report ----
server.registerTool('faizos_error_report', {
  title: 'Error taxonomy report',
  description: 'Open error categories ranked by occurrences, with the rule each breaks and when last seen. The top categories weight the next rules card.',
  inputSchema: {},
}, async () => {
  const open = db.prepare('SELECT category, description, rule_broken, occurrences, last_seen FROM errors WHERE resolved=0 ORDER BY occurrences DESC, category').all();
  const resolved = db.prepare('SELECT category, occurrences, last_seen FROM errors WHERE resolved=1 ORDER BY last_seen DESC').all();
  return ok({ open, resolved });
});

// ---- faizos_unlock_build: hand a build to the assistant, recorded honestly ----
server.registerTool('faizos_unlock_build', {
  title: 'Unlock the active build',
  description: 'Explicitly hands the current build to the assistant. Sets the build state to unlocked, marks student_wrote=0 on the lesson, and shows on the dashboard as a skipped build. Honest, not punitive.',
  inputSchema: { build_id: z.number().optional(), reason: z.string().optional() },
}, async ({ build_id, reason }) => {
  const id = build_id ?? activeBuild(db)?.id;
  if (id === undefined) return ok({ unlocked: false, reason: 'no active build' });
  const result = unlockBuild(db, id);
  if (result.unlocked) logEvent(db, now(), 'unlock', `build #${id}${reason ? ': ' + reason : ''}`);
  return ok(result);
});

// ================= v2: the venture evidence engine =================

server.registerTool('faizos_venture_ingest', {
  title: 'Venture ingest (stage 1)',
  description: 'Fetch fresh evidence from the free tier sources (HN, GitHub, SEC EDGAR, Companies House, YC RFS, MCP registry, Product Hunt, arXiv). Deterministic fetch; classification happens separately in session. Sources without configured keys are skipped and reported.',
  inputSchema: {},
}, async () => {
  const { ingest, realFetch } = await import('./venture.js');
  const result = await ingest(db, realFetch);
  logEvent(db, now(), 'venture_ingest', `${result.inserted} rows`);
  const pending = (db.prepare('SELECT COUNT(*) c FROM evidence WHERE importance IS NULL').get() as { c: number }).c;
  return ok({ ...result, pending_classification: pending, next: 'Call faizos_venture_pending, classify each item (jtbd, importance 1-5, dissatisfaction 1-5, optional venture_title to group), then faizos_venture_classify_save.' });
});

server.registerTool('faizos_venture_pending', {
  title: 'Pending evidence (stage 2 input)',
  description: 'Unclassified evidence rows. Classify each in session: the job to be done, importance 1-5, dissatisfaction 1-5, and an optional venture_title to group related evidence.',
  inputSchema: { limit: z.number().optional() },
}, async ({ limit }) => {
  const { pendingClassification } = await import('./venture.js');
  return ok({ pending: pendingClassification(db, limit ?? 25) });
});

server.registerTool('faizos_venture_classify_save', {
  title: 'Save classifications (stage 2)',
  description: 'Write the in-session classifications back. Grouping by venture_title creates candidate ventures. Every record keeps its source URL and raw excerpt.',
  inputSchema: {
    items: z.array(z.object({
      evidence_id: z.number(),
      jtbd: z.string(),
      importance: z.number().min(1).max(5),
      dissatisfaction: z.number().min(1).max(5),
      venture_title: z.string().optional(),
    })),
  },
}, async ({ items }) => {
  const { saveClassifications } = await import('./venture.js');
  const result = saveClassifications(db, items);
  logEvent(db, now(), 'venture_classify', `${result.classified} items, ${result.ventures_created} new candidates`);
  return ok(result);
});

server.registerTool('faizos_venture_score', {
  title: 'Corroborate and score (stages 3-4)',
  description: 'With no arguments: run the corroboration gate (2 or more INDEPENDENT source families advance; everything else fails with the reason). With venture_id + axes (each 1-5): compute the fixed-weight score for a corroborated venture. Axes: opportunity_gap(2), distribution_reachability(3), lab_absorption_risk_inverted(3), buildable_14d(3), teaches_curriculum(1), regulatory_feasibility(2).',
  inputSchema: {
    venture_id: z.number().optional(),
    axes: z.object({
      opportunity_gap: z.number(),
      distribution_reachability: z.number(),
      lab_absorption_risk_inverted: z.number(),
      buildable_14d: z.number(),
      teaches_curriculum: z.number(),
      regulatory_feasibility: z.number(),
    }).optional(),
  },
}, async ({ venture_id, axes }) => {
  const venture = await import('./venture.js');
  if (venture_id !== undefined && axes !== undefined) {
    try {
      const result = venture.scoreVenture(db, venture_id, axes);
      logEvent(db, now(), 'venture_score', `#${venture_id} -> ${result.weighted_score}`);
      return ok(result);
    } catch (e) {
      return ok({ error: e instanceof Error ? e.message : String(e) });
    }
  }
  const gate = venture.corroborate(db);
  logEvent(db, now(), 'venture_corroborate', `${gate.advanced.length} advanced, ${gate.failed.length} failed`);
  return ok({ ...gate, note: 'Present the failures with their reasons. They teach as much as the passes. Never recommend which venture to pick.' });
});

server.registerTool('faizos_venture_activate', {
  title: 'Activate a venture (stage 5, WIP limit 1)',
  description: 'Set one scored venture active with a falsifiable 14 day v0 metric. The database physically refuses a second active venture. Returns the milestone spine for Build Mode.',
  inputSchema: { venture_id: z.number(), v0_metric: z.string().describe('one falsifiable success metric for the 14 day v0') },
}, async ({ venture_id, v0_metric }) => {
  const { activateVenture } = await import('./venture.js');
  const result = activateVenture(db, venture_id, v0_metric);
  if (result.activated) logEvent(db, now(), 'venture_activate', `#${venture_id}: ${v0_metric}`);
  return ok(result);
});

server.registerTool('faizos_venture_review', {
  title: 'The 14 day kill review (stage 5)',
  description: 'Exactly three outcomes for the active venture: continue (requires a new metric), park (written reason), kill (mandatory post mortem, written into the insight loop). No fourth option.',
  inputSchema: {
    outcome: z.enum(['continue', 'park', 'kill']),
    note: z.string().describe('continue: what the number showed. park: the written reason. kill: the post mortem.'),
    new_metric: z.string().optional(),
  },
}, async ({ outcome, note, new_metric }) => {
  const { reviewVenture } = await import('./venture.js');
  const result = reviewVenture(db, outcome, note, new_metric);
  if (result.done) logEvent(db, now(), 'venture_review', `${outcome}: ${note.slice(0, 80)}`);
  return ok(result);
});

server.registerTool('faizos_frontier_ingest', {
  title: 'Weekly frontier fetch (deterministic; you classify after)',
  description: 'Fetch recent arXiv entries for the current and next track into the frontier table, then report drifted tracks (current_as_of older than 60 days). Fetch is deterministic; summarising what each item changes for Faiz happens in session.',
  inputSchema: {},
}, async () => {
  const { fetchFrontier, driftedTracks } = await import('./frontier.js');
  const { realFetch } = await import('./venture.js');
  const result = await fetchFrontier(db, realFetch);
  logEvent(db, now(), 'frontier_ingest', `${result.inserted} new rows`);
  const recent = db.prepare(
    "SELECT f.title, f.url, f.summary, t.code AS track FROM frontier f LEFT JOIN tracks t ON t.id = f.affects_track_id WHERE f.actioned = 0 ORDER BY f.ingested_at DESC LIMIT 15",
  ).all();
  return ok({ ...result, drifted_tracks: driftedTracks(db), unactioned: recent, note: 'Group by track. One line per item on what it changes for the current build. Skip tracks more than two positions away.' });
});


// ---- v3: guidance policy, reveal-and-contrast, the rebuild gate, mode, OSS, cost drill ----

server.registerTool('faizos_guidance', {
  title: 'Which guidance policy applies here',
  description: 'Returns write_from_empty or worked_example_first for a build, based on its track. Call this BEFORE teaching. Expertise reversal: worked examples beat blank pages for novices and reverse for experts, so production tracks show a reference first and ML tracks do not.',
  inputSchema: { build_id: z.number() },
}, async ({ build_id }) => {
  const { guidanceFor } = await import('./v3.js');
  return ok(guidanceFor(db, build_id));
});

server.registerTool('faizos_reveal_contrast', {
  title: 'Record the reveal-and-contrast step (mandatory before review)',
  description: 'After his attempt, show the reference implementation and have him write one line per difference between it and his reasoning. This consolidation phase is where cognitive load drops and the learning sticks; generation alone is not what the evidence tested.',
  inputSchema: {
    build_id: z.number(),
    notes: z.string().describe('his own words, one line per difference between his reasoning and the reference'),
  },
}, async ({ build_id, notes }) => {
  const { recordReveal } = await import('./v3.js');
  const r = recordReveal(db, build_id, notes);
  if (r.recorded) logEvent(db, now(), 'reveal', `build #${build_id}`);
  return ok(r);
});

server.registerTool('faizos_rebuilds_due', {
  title: 'Builds awaiting an unaided rebuild',
  description: 'Provisional builds whose 14 day delay has elapsed. A build that passed on the day it was written is not evidence of durable skill; only a delayed unaided reproduction is.',
  inputSchema: {},
}, async () => {
  const { rebuildsDue } = await import('./v3.js');
  const due = rebuildsDue(db);
  return ok({ due, count: due.length, note: due.length ? 'Blank the file and have him rebuild it with no reference and no hints.' : 'Nothing due.' });
});

server.registerTool('faizos_complete_rebuild', {
  title: 'Record the outcome of an unaided rebuild',
  description: 'unaided=true marks the build done, which is the only state that counts as learned. unaided=false reschedules another 14 days, honestly.',
  inputSchema: { build_id: z.number(), unaided: z.boolean() },
}, async ({ build_id, unaided }) => {
  const { completeRebuild } = await import('./v3.js');
  const r = completeRebuild(db, build_id, unaided);
  logEvent(db, now(), 'rebuild', `build #${build_id}: ${r.state}`);
  return ok(r);
});

server.registerTool('faizos_mode', {
  title: 'Get or set the operating mode',
  description: 'course (the P0-P7 spine, in order), venture (the active venture decides what gets built), or free (he brings the idea). Omit set_to to just read the current mode.',
  inputSchema: { set_to: z.enum(['course', 'venture', 'free']).optional() },
}, async ({ set_to }) => {
  const { currentMode, setMode, ventureNextBuild } = await import('./v3.js');
  if (set_to) setMode(db, set_to);
  const mode = currentMode(db);
  const suggestions = mode.mode === 'venture' ? ventureNextBuild(db, []) : [];
  return ok({ ...mode, venture_candidates: suggestions });
});

server.registerTool('faizos_oss', {
  title: 'The merged-PR track',
  description: 'action=status lists targets and the measured repo guidance; action=add records a candidate issue; action=update moves its state (candidate|claimed|pr_open|merged|abandoned). A merged PR writes a systems row for capstone rung 6.',
  inputSchema: {
    action: z.enum(['status', 'add', 'update']),
    id: z.number().optional(),
    repo: z.string().optional(),
    issue_url: z.string().optional(),
    issue_title: z.string().optional(),
    difficulty: z.enum(['first', 'second', 'substantive']).optional(),
    state: z.enum(['candidate', 'claimed', 'pr_open', 'merged', 'abandoned']).optional(),
    pr_url: z.string().optional(),
    review_cycles: z.number().optional(),
    notes: z.string().optional(),
  },
}, async (a) => {
  const { ossStatus, addOssTarget, updateOssTarget } = await import('./v3.js');
  if (a.action === 'add') {
    if (!a.repo || !a.issue_url) return ok({ ok: false, reason: 'repo and issue_url are required' });
    const id = addOssTarget(db, { repo: a.repo, issue_url: a.issue_url, issue_title: a.issue_title ?? '', difficulty: a.difficulty, notes: a.notes });
    return ok({ ok: true, id });
  }
  if (a.action === 'update') {
    if (!a.id) return ok({ ok: false, reason: 'id is required' });
    const r = updateOssTarget(db, a.id, { state: a.state, pr_url: a.pr_url, review_cycles: a.review_cycles, notes: a.notes });
    if (a.state === 'merged') logEvent(db, now(), 'oss_merged', a.pr_url ?? '');
    return ok(r);
  }
  return ok(ossStatus(db));
});

server.registerTool('faizos_cost_drill', {
  title: 'Score a cost estimate',
  description: 'The drill behind "every design answer ends with a number". Give the scenario, the expected figure and his figure; within 20% counts. Cost awareness is repeatedly named the thing that separates production thinkers from prototype thinkers.',
  inputSchema: {
    scenario: z.string(),
    expected_usd_per_day: z.number().optional(),
    expected_tokens_per_day: z.number().optional(),
    answer_usd_per_day: z.number().optional(),
    answer_tokens_per_day: z.number().optional(),
  },
}, async (a) => {
  const { scoreCostDrill, costDrillRecord } = await import('./v3.js');
  const r = scoreCostDrill(
    db,
    a.scenario,
    { usd_per_day: a.expected_usd_per_day, tokens_per_day: a.expected_tokens_per_day },
    { usd_per_day: a.answer_usd_per_day, tokens_per_day: a.answer_tokens_per_day },
  );
  return ok({ ...r, record: costDrillRecord(db) });
});


server.registerTool('faizos_record_insight', {
  title: 'Record what this session taught you about teaching him',
  description: 'Write down a teaching lesson so it loads at the start of every future lesson. This is the mechanism that stops him giving the same correction twice. Call it at the end of EVERY session that taught anything; the Stop hook refuses to close a teaching session that recorded nothing.',
  inputSchema: {
    note: z.string().describe('what you learned about how to teach him, specific enough to act on next time'),
    weight: z.number().optional().describe('3 for a hard rule he stated directly, 1 for an observation'),
  },
}, async ({ note, weight }) => {
  const { recordInsight } = await import('./v3.js');
  const r = recordInsight(db, note, weight ?? 1);
  if (r.recorded) logEvent(db, now(), 'insight', note.slice(0, 80));
  return ok(r);
});


server.registerTool('faizos_lesson_progress', {
  title: 'The real progress bar',
  description: 'Counted from rows, never estimated: lessons whose build has left awaiting_student, production vs ML skills with mastery above zero, and capstone rungs the scorer calls SOLID. Print this at the END of every lesson.',
  inputSchema: {},
}, async () => {
  const { lessonProgress } = await import('./v3.js');
  const { scoreCapstone } = await import('./generators.js');
  const solid = scoreCapstone(db).filter((r) => r.status === 'SOLID').length;
  return ok(lessonProgress(db, solid));
});

await server.connect(new StdioServerTransport());
