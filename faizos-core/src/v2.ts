// v2 helpers: the deterministic logic behind the new MCP tools. Pure functions over the
// database so they can be tested directly, without spinning up the MCP server.
import type { Database } from 'better-sqlite3';

const now = (): string => new Date().toISOString();
const today = (): string => now().slice(0, 10);

// ---- builds and the write guard ------------------------------------------------------------

export interface BuildRow {
  id: number;
  lesson_id: number | null;
  solution_path: string;
  test_path: string;
  state: string;
  created_at: string;
  unlocked_at: string | null;
}

export function activeBuild(db: Database): BuildRow | null {
  const row = db
    .prepare("SELECT * FROM builds WHERE state IN ('awaiting_student', 'in_review') ORDER BY id DESC LIMIT 1")
    .get() as BuildRow | undefined;
  return row ?? null;
}

export function studentWroteRatio(db: Database): { written: number; unlocked: number; ratio: number } {
  const written = (db.prepare("SELECT COUNT(*) AS c FROM builds WHERE state = 'done'").get() as { c: number }).c;
  const unlocked = (db.prepare("SELECT COUNT(*) AS c FROM builds WHERE state = 'unlocked'").get() as { c: number }).c;
  const total = written + unlocked;
  return { written, unlocked, ratio: total === 0 ? 1 : written / total };
}

export interface SpecBuildArgs {
  topic: string;
  slug?: string;
  mode?: 'course' | 'build';
  depth?: 'explain' | 'flow' | 'ship';
  track_code?: string;
}

export interface SpecBuildResult {
  lesson_id: number;
  build_id: number;
  solution_path: string;
  test_path: string;
  open_error_categories: Array<{ category: string; rule_broken: string; occurrences: number }>;
  track: { code: string; title: string } | null;
}

const slugify = (s: string): string =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 50) || 'build';

export function specBuild(db: Database, args: SpecBuildArgs): SpecBuildResult {
  const mode = args.mode ?? 'course';
  const depth = args.depth ?? 'explain';
  const slug = slugify(args.slug ?? args.topic);
  const solutionPath = `projects/${slug}/${slug.replace(/-/g, '_')}.py`;
  const testPath = `projects/${slug}/test_${slug.replace(/-/g, '_')}.py`;

  let trackId: number | null = null;
  let track: { code: string; title: string } | null = null;
  if (args.track_code !== undefined) {
    const t = db.prepare('SELECT id, code, title FROM tracks WHERE code = ?').get(args.track_code) as
      | { id: number; code: string; title: string }
      | undefined;
    if (t) {
      trackId = t.id;
      track = { code: t.code, title: t.title };
    }
  }

  const ts = now();
  const lessonInfo = db
    .prepare(
      `INSERT INTO lessons (ts, topic, skills, struggles, worked, mode, depth, track_id)
       VALUES (?, ?, '[]', '[]', '[]', ?, ?, ?)`,
    )
    .run(ts, args.topic, mode, depth, trackId);
  const lessonId = Number(lessonInfo.lastInsertRowid);
  const buildInfo = db
    .prepare(
      `INSERT INTO builds (lesson_id, solution_path, test_path, state, created_at)
       VALUES (?, ?, ?, 'awaiting_student', ?)`,
    )
    .run(lessonId, solutionPath, testPath, ts);

  return {
    lesson_id: lessonId,
    build_id: Number(buildInfo.lastInsertRowid),
    solution_path: solutionPath,
    test_path: testPath,
    open_error_categories: topOpenErrors(db, 3),
    track,
  };
}

// ---- hint ladder ---------------------------------------------------------------------------

export const HINT_FRAMES: Record<number, string> = {
  1: 'Which assertion failed, and what that assertion is actually checking, in English. Nothing about his code.',
  2: 'Which REGION of his file the bug is in. Not the line, the region.',
  3: 'The concept or Python rule he has broken, stated as a rule, without reference to his code.',
  4: 'The line, with the reasoning.',
};

export interface HintResult {
  granted: boolean;
  rung: number;
  frame: string;
  reason: string;
  previous_max: number;
}

export function grantHint(db: Database, buildId: number, requestedRung: number): HintResult {
  const build = db.prepare('SELECT id, lesson_id FROM builds WHERE id = ?').get(buildId) as
    | { id: number; lesson_id: number | null }
    | undefined;
  if (!build || build.lesson_id === null) {
    return { granted: false, rung: 0, frame: '', reason: `no build #${buildId} with a lesson`, previous_max: 0 };
  }
  const lesson = db.prepare('SELECT hint_max_rung FROM lessons WHERE id = ?').get(build.lesson_id) as {
    hint_max_rung: number;
  };
  const max = lesson.hint_max_rung ?? 0;
  if (requestedRung < 1 || requestedRung > 4) {
    return { granted: false, rung: 0, frame: '', reason: 'rungs are 1 to 4', previous_max: max };
  }
  if (requestedRung <= max) {
    // Re-serving an already earned rung is allowed; skipping ahead is never allowed.
    const frame = HINT_FRAMES[requestedRung];
    return { granted: true, rung: requestedRung, frame: frame ?? '', reason: 're-serving an earned rung', previous_max: max };
  }
  if (requestedRung !== max + 1) {
    return {
      granted: false,
      rung: 0,
      frame: '',
      reason: `rung ${requestedRung} refused: the next rung is ${max + 1}. Rungs are served strictly in order.`,
      previous_max: max,
    };
  }
  db.prepare('UPDATE lessons SET hint_max_rung = ? WHERE id = ?').run(requestedRung, build.lesson_id);
  const frame = HINT_FRAMES[requestedRung];
  return { granted: true, rung: requestedRung, frame: frame ?? '', reason: 'granted', previous_max: max };
}

// ---- error taxonomy ------------------------------------------------------------------------

export interface ErrorEntry {
  category: string;
  description: string;
  code_excerpt?: string;
  rule_broken?: string;
}

// One aggregate row per category (lesson_id NULL). Repeats increment occurrences.
export function recordErrors(db: Database, errors: ErrorEntry[]): number {
  const existing = db.prepare('SELECT id FROM errors WHERE category = ? AND lesson_id IS NULL');
  const bump = db.prepare(
    'UPDATE errors SET occurrences = occurrences + 1, last_seen = ?, description = ?, code_excerpt = ?, resolved = 0 WHERE id = ?',
  );
  const insert = db.prepare(
    `INSERT INTO errors (lesson_id, category, description, code_excerpt, rule_broken, resolved, occurrences, last_seen)
     VALUES (NULL, ?, ?, ?, ?, 0, 1, ?)`,
  );
  let recorded = 0;
  for (const e of errors) {
    const row = existing.get(e.category) as { id: number } | undefined;
    if (row) bump.run(today(), e.description, e.code_excerpt ?? '', row.id);
    else insert.run(e.category, e.description, e.code_excerpt ?? '', e.rule_broken ?? '', today());
    recorded += 1;
  }
  return recorded;
}

export function topOpenErrors(db: Database, limit: number): Array<{ category: string; rule_broken: string; occurrences: number }> {
  return db
    .prepare(
      'SELECT category, rule_broken, occurrences FROM errors WHERE resolved = 0 ORDER BY occurrences DESC, category LIMIT ?',
    )
    .all(limit) as Array<{ category: string; rule_broken: string; occurrences: number }>;
}

// ---- code review ---------------------------------------------------------------------------

export interface ReviewArgs {
  build_id: number;
  student_code: string;
  reference_code?: string;
  diff_summary?: string;
  correctness_diffs?: string[];
  taste_diffs?: string[];
  errors?: ErrorEntry[];
}

export function recordReview(db: Database, args: ReviewArgs): { review_id: number; errors_recorded: number } {
  const build = db.prepare('SELECT id, lesson_id FROM builds WHERE id = ?').get(args.build_id) as
    | { id: number; lesson_id: number | null }
    | undefined;
  if (!build) throw new Error(`no build #${args.build_id}`);
  const info = db
    .prepare(
      `INSERT INTO code_reviews (lesson_id, student_code, reference_code, diff_summary, correctness_diffs, taste_diffs, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
    )
    .run(
      build.lesson_id,
      args.student_code,
      args.reference_code ?? '',
      args.diff_summary ?? '',
      JSON.stringify(args.correctness_diffs ?? []),
      JSON.stringify(args.taste_diffs ?? []),
      now(),
    );
  const errorsRecorded = recordErrors(db, args.errors ?? []);
  db.prepare("UPDATE builds SET state = 'done' WHERE id = ? AND state IN ('awaiting_student', 'in_review')").run(
    args.build_id,
  );
  return { review_id: Number(info.lastInsertRowid), errors_recorded: errorsRecorded };
}

// ---- unlock --------------------------------------------------------------------------------

export function unlockBuild(db: Database, buildId: number): { unlocked: boolean; reason: string } {
  const build = db.prepare('SELECT id, lesson_id, state FROM builds WHERE id = ?').get(buildId) as
    | { id: number; lesson_id: number | null; state: string }
    | undefined;
  if (!build) return { unlocked: false, reason: `no build #${buildId}` };
  if (build.state !== 'awaiting_student' && build.state !== 'in_review') {
    return { unlocked: false, reason: `build #${buildId} is '${build.state}', nothing to unlock` };
  }
  db.prepare("UPDATE builds SET state = 'unlocked', unlocked_at = ? WHERE id = ?").run(now(), buildId);
  if (build.lesson_id !== null) {
    db.prepare('UPDATE lessons SET student_wrote = 0 WHERE id = ?').run(build.lesson_id);
  }
  return { unlocked: true, reason: 'recorded honestly: this build was not written by the student' };
}

// ---- experiments ---------------------------------------------------------------------------

export interface ExperimentArgs {
  system_id: number;
  config_json?: string;
  seed?: number;
  metric_name: string;
  metric_value: number;
  gpu_type?: string;
  gpu_hours?: number;
  cost_usd?: number;
  notes?: string;
}

export interface SeedSpread {
  n: number;
  mean: number;
  min: number;
  max: number;
  spread: number;
}

export function logExperiment(db: Database, args: ExperimentArgs): { experiment_id: number; seed_spread: SeedSpread | null } {
  const info = db
    .prepare(
      `INSERT INTO experiments (system_id, config_json, seed, metric_name, metric_value, gpu_type, gpu_hours, cost_usd, notes, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    )
    .run(
      args.system_id,
      args.config_json ?? '{}',
      args.seed ?? null,
      args.metric_name,
      args.metric_value,
      args.gpu_type ?? null,
      args.gpu_hours ?? null,
      args.cost_usd ?? null,
      args.notes ?? '',
      now(),
    );
  const values = (
    db
      .prepare('SELECT metric_value FROM experiments WHERE system_id = ? AND metric_name = ? AND metric_value IS NOT NULL')
      .all(args.system_id, args.metric_name) as Array<{ metric_value: number }>
  ).map((r) => r.metric_value);
  let spread: SeedSpread | null = null;
  if (values.length >= 3) {
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const lo = Math.min(...values);
    const hi = Math.max(...values);
    spread = { n: values.length, mean, min: lo, max: hi, spread: hi - lo };
  }
  return { experiment_id: Number(info.lastInsertRowid), seed_spread: spread };
}

// ---- tracks --------------------------------------------------------------------------------

export interface TrackRow {
  id: number;
  code: string;
  title: string;
  position: number;
  status: string;
  prereq_codes: string;
  completion_test: string;
  current_as_of: string | null;
}

export function currentTrack(db: Database): TrackRow | null {
  const active = db.prepare("SELECT * FROM tracks WHERE status = 'active' ORDER BY position LIMIT 1").get() as
    | TrackRow
    | undefined;
  if (active) return active;
  const next = db.prepare("SELECT * FROM tracks WHERE status = 'pending' ORDER BY position LIMIT 1").get() as
    | TrackRow
    | undefined;
  return next ?? null;
}

export interface TrackStatus {
  track: TrackRow;
  systems: Array<{ id: number; title: string; kind: string; status: string; metric_name: string | null; metric_value: number | null }>;
  skills: { total: number; touched: number; avg_mastery: number };
  frontier_notes: Array<{ title: string; url: string; summary: string; ingested_at: string }>;
}

export function trackStatus(db: Database, code: string): TrackStatus | null {
  const track = db.prepare('SELECT * FROM tracks WHERE code = ?').get(code) as TrackRow | undefined;
  if (!track) return null;
  const systems = db
    .prepare('SELECT id, title, kind, status, metric_name, metric_value FROM systems WHERE track_id = ? ORDER BY id')
    .all(track.id) as TrackStatus['systems'];
  const skillAgg = db
    .prepare(
      'SELECT COUNT(*) AS total, SUM(CASE WHEN last_seen IS NOT NULL THEN 1 ELSE 0 END) AS touched, AVG(mastery) AS avg FROM skills WHERE track_id = ?',
    )
    .get(track.id) as { total: number; touched: number | null; avg: number | null };
  const frontierNotes = db
    .prepare(
      'SELECT title, url, summary, ingested_at FROM frontier WHERE affects_track_id = ? ORDER BY ingested_at DESC LIMIT 5',
    )
    .all(track.id) as TrackStatus['frontier_notes'];
  return {
    track,
    systems,
    skills: {
      total: skillAgg.total,
      touched: skillAgg.touched ?? 0,
      avg_mastery: Number((skillAgg.avg ?? 0).toFixed(3)),
    },
    frontier_notes: frontierNotes,
  };
}

// ---- ventures (read side used by lesson_start and the dashboard) ---------------------------

export interface VentureRow {
  id: number;
  title: string;
  thesis: string;
  stage: string;
  weighted_score: number | null;
  v0_metric: string | null;
  v0_deadline: string | null;
}

export function activeVenture(db: Database): VentureRow | null {
  const row = db
    .prepare(
      "SELECT id, title, thesis, stage, weighted_score, v0_metric, v0_deadline FROM ventures WHERE stage = 'active' LIMIT 1",
    )
    .get() as VentureRow | undefined;
  return row ?? null;
}
