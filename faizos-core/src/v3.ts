// v3 curriculum: the production spine (P-tracks), the per-domain guidance policy, the
// reveal-and-contrast step, the 14 day unaided rebuild, and the OSS + cost drills.
//
// The governing evidence: deployment appears in 78.3% of AI-engineering postings and
// self-hosting models in 2.5%. The P-tracks are the critical path; T0-T10 become the
// evidence-conversion layer.
import type Database from 'better-sqlite3';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DB = join(HERE, '..', 'data', 'faiz.db');

const now = (): string => new Date().toISOString();
const today = (): string => new Date().toISOString().slice(0, 10);
export const REBUILD_DAYS = 14;

// ---- P-track seeds ---------------------------------------------------------------------

export interface PTrackSeed {
  code: string;
  title: string;
  position: number;
  prereqs: string[];
  completionTest: string;
  kind: 'production' | 'ship';
  /** Novice domain: read a worked example first. Expert domain: write from empty. */
  guidance: 'worked_example_first' | 'write_from_empty';
}

export const P_TRACKS: PTrackSeed[] = [
  { code: 'P0', title: 'The engineering floor', position: 0, prereqs: [], kind: 'production', guidance: 'worked_example_first',
    completionTest: 'New project, add a dependency, write a failing test, make it pass, push with green CI, in fifteen minutes without looking anything up.' },
  { code: 'P1', title: 'Async Python and FastAPI', position: 1, prereqs: ['P0'], kind: 'production', guidance: 'worked_example_first',
    completionTest: 'Write the blocking version, load-test it, watch p99 collapse, fix it with TaskGroup and a pooled client, and show the before and after.' },
  { code: 'P2', title: 'Docker and one real deploy', position: 2, prereqs: ['P1'], kind: 'production', guidance: 'worked_example_first',
    completionTest: 'It loads on your phone.' },
  { code: 'P3', title: 'CI/CD with OIDC', position: 3, prereqs: ['P2'], kind: 'production', guidance: 'worked_example_first',
    completionTest: 'CI builds an image and deploys it in under three minutes with zero static credentials, and the IAM trust policy is scoped to one repo and ref.' },
  { code: 'P4', title: 'Postgres and the data layer', position: 4, prereqs: ['P2'], kind: 'production', guidance: 'worked_example_first',
    completionTest: 'Diagnose a slow query from EXPLAIN output alone, and state where pgvector ceilings out for a given corpus and why.' },
  { code: 'P5', title: 'Streaming and reliability', position: 5, prereqs: ['P4'], kind: 'production', guidance: 'worked_example_first',
    completionTest: 'Kill the client mid-stream and prove the usage row still wrote.' },
  { code: 'P6', title: 'Observability and evals', position: 6, prereqs: ['P5'], kind: 'production', guidance: 'write_from_empty',
    completionTest: 'A documented regression the CI gate caught, with a paired test proving the fix was real and not noise.' },
  { code: 'P7', title: 'Cost engineering', position: 7, prereqs: ['P6'], kind: 'production', guidance: 'write_from_empty',
    completionTest: 'Every design answer ends with a number, unprompted.' },
  { code: 'P8', title: 'Retrieval, properly', position: 8, prereqs: ['P6'], kind: 'production', guidance: 'write_from_empty',
    completionTest: 'A ten row ablation table on your own corpus, including the filtered-query recall collapse and the fixes that did not work.' },
  { code: 'P9', title: 'Agents, tools and MCP', position: 9, prereqs: ['P8'], kind: 'production', guidance: 'write_from_empty',
    completionTest: 'An agent with designed tools, pass^k reported beside pass@1, and a written failure taxonomy.' },
  { code: 'P10', title: 'Ship and sell', position: 10, prereqs: ['P9'], kind: 'ship', guidance: 'write_from_empty',
    completionTest: 'One product with a user who is not you, carrying a real metric.' },
];

// ---- production skills -----------------------------------------------------------------
// phase 16..26 maps to P0..P10 (v1 used 0..15).

export interface PSkillSeed { id: string; name: string; track: string; must_know: 0 | 1; hint: string }

export const P_SKILLS: PSkillSeed[] = [
  // P0
  { id: 'uv-project-setup', name: 'uv: src layout, lockfile, sync --locked', track: 'P0', must_know: 1, hint: 'Init a project and pin it so a stranger can run it.' },
  { id: 'ruff-lint-format', name: 'ruff lint and format (extend-select, not select)', track: 'P0', must_know: 1, hint: 'Configure ruff so the ASYNC rules actually fire.' },
  { id: 'pytest-fundamentals', name: 'pytest from pyproject, fixtures, parametrize', track: 'P0', must_know: 1, hint: 'One command runs the whole suite.' },
  { id: 'type-checking-python', name: 'Type checking (pyrefly / mypy) in CI', track: 'P0', must_know: 0, hint: 'Make the type checker gate the build.' },
  { id: 'git-workflow', name: 'Branching, review-shaped commits, CI on push', track: 'P0', must_know: 1, hint: 'A PR that CI approves before you do.' },
  // P1
  { id: 'async-taskgroup', name: 'TaskGroup, timeout, Semaphore (not bare gather)', track: 'P1', must_know: 1, hint: 'Fan out ten provider calls with a concurrency cap and a deadline.' },
  { id: 'async-exceptiongroup', name: 'ExceptionGroup and except*', track: 'P1', must_know: 1, hint: 'Handle one failure out of ten without losing the other nine.' },
  { id: 'blocking-the-loop', name: 'Diagnosing a blocked event loop', track: 'P1', must_know: 1, hint: 'Write the bug, load-test it, then fix it.' },
  { id: 'httpx-pooling', name: 'httpx client lifetime, Limits, split timeouts', track: 'P1', must_know: 1, hint: 'One client for the process; prove pooling works.' },
  { id: 'fastapi-structure', name: 'FastAPI layout: routers, services, providers', track: 'P1', must_know: 1, hint: 'Routers hold zero logic.' },
  { id: 'fastapi-di-lifespan', name: 'Depends and lifespan', track: 'P1', must_know: 1, hint: 'Build the client in lifespan, inject it everywhere.' },
  { id: 'provider-abstraction', name: 'Multi-provider behind one interface', track: 'P1', must_know: 1, hint: 'Swap Anthropic for OpenAI without touching a router.' },
  // P2
  { id: 'docker-multistage', name: 'Multi-stage Dockerfile, non-root, pinned base', track: 'P2', must_know: 1, hint: 'Build an image that is not embarrassing.' },
  { id: 'docker-uv-cache', name: 'uv cache mounts and layer caching', track: 'P2', must_know: 1, hint: 'Change one line of code; rebuild in seconds.' },
  { id: 'paas-deploy', name: 'Deploy to Cloud Run or Fly', track: 'P2', must_know: 1, hint: 'A URL that works from your phone.' },
  { id: 'health-readiness', name: 'Liveness vs readiness probes', track: 'P2', must_know: 1, hint: 'Drain traffic on a degraded provider instead of crash-looping.' },
  // P3
  { id: 'github-actions', name: 'GitHub Actions: test, build, push', track: 'P3', must_know: 1, hint: 'Green check before merge.' },
  { id: 'oidc-keyless-deploy', name: 'OIDC deploy with zero static keys', track: 'P3', must_know: 1, hint: 'Delete every cloud secret from the repo.' },
  { id: 'iam-trust-scoping', name: 'Scoping the OIDC sub claim to one repo and ref', track: 'P3', must_know: 1, hint: 'Prove a fork cannot assume your role.' },
  // P4
  { id: 'sqlalchemy-async', name: 'SQLAlchemy 2.0 async + asyncpg', track: 'P4', must_know: 1, hint: 'Async session with expire_on_commit off.' },
  { id: 'async-lazy-loading', name: 'selectinload and the N+1 in disguise', track: 'P4', must_know: 1, hint: 'Make lazy loading raise, then fix it properly.' },
  { id: 'alembic-migrations', name: 'Alembic (autogenerate is a draft, not a product)', track: 'P4', must_know: 1, hint: 'Catch the rename that autogenerate turns into data loss.' },
  { id: 'sql-joins-aggregation', name: 'Joins, GROUP BY vs WHERE, fan-out row explosions', track: 'P4', must_know: 1, hint: 'Explain why your row count quadrupled.' },
  { id: 'sql-window-functions', name: 'Window functions (latest-per-group)', track: 'P4', must_know: 1, hint: 'ROW_NUMBER OVER PARTITION BY, from memory.' },
  { id: 'explain-analyze', name: 'EXPLAIN (ANALYZE, BUFFERS) reading', track: 'P4', must_know: 1, hint: 'Diagnose a slow query without running variants.' },
  { id: 'pgvector-limits', name: 'pgvector ceilings: dims, RAM cliff, HNSW bloat', track: 'P4', must_know: 1, hint: 'State where it breaks before you hit it.' },
  { id: 'redis-caching', name: 'Redis/Valkey caching and atomic rate limits', track: 'P4', must_know: 0, hint: 'Token bucket as a Lua script, because GET/INCR/SET is racy.' },
  // P5
  { id: 'sse-streaming', name: 'Native FastAPI SSE, and why not WebSockets', track: 'P5', must_know: 1, hint: 'Stream tokens through a real proxy, not just localhost.' },
  { id: 'client-disconnect', name: 'Disconnect handling and shield() on the billing write', track: 'P5', must_know: 1, hint: 'Kill the client mid-stream; the usage row must survive.' },
  { id: 'proxy-buffering', name: 'Diagnosing proxy buffering killing a stream', track: 'P5', must_know: 0, hint: 'Put nginx in front with defaults and watch it break.' },
  { id: 'retries-backoff', name: 'Retries: stamina, full jitter, retry-after', track: 'P5', must_know: 1, hint: 'Know which 429 you must never retry.' },
  { id: 'circuit-breakers', name: 'Circuit breaker per provider and model', track: 'P5', must_know: 1, hint: 'Trip on 5xx and 529, never on 429.' },
  { id: 'llm-timeouts', name: 'TTFT and inter-token timeouts, not total duration', track: 'P5', must_know: 1, hint: 'A total timeout is meaningless for a 128k generation.' },
  // P6
  { id: 'error-analysis', name: 'Error analysis: open coding on 100+ real traces', track: 'P6', must_know: 1, hint: 'Hand-label before you automate anything.' },
  { id: 'failure-taxonomy', name: 'Axial coding into a failure taxonomy with counts', track: 'P6', must_know: 1, hint: 'Cluster the notes, count the frequencies, publish it.' },
  { id: 'eval-set-construction', name: 'Golden sets: traces, replays, edge cases, synthetic', track: 'P6', must_know: 1, hint: 'Every shipped bug becomes a permanent test case.' },
  { id: 'deterministic-assertions', name: 'Code assertions before LLM judges', track: 'P6', must_know: 1, hint: 'If a regex can check it, a judge should not.' },
  { id: 'llm-judge-design', name: 'LLM-as-judge: binary with critique, not Likert', track: 'P6', must_know: 1, hint: 'Decompose gradation into binary checks.' },
  { id: 'judge-validation', name: 'Judge validation: TPR, TNR, Cohen kappa, bias correction', track: 'P6', must_know: 1, hint: 'Raw accuracy is meaningless under class imbalance.' },
  { id: 'statistical-gating', name: 'Binomial SE, clustered SE, paired bootstrap, power', track: 'P6', must_know: 1, hint: 'State what your eval set can and cannot resolve.' },
  { id: 'otel-tracing', name: 'OTel spans for LLM calls; normalize, do not trust gen_ai.*', track: 'P6', must_know: 1, hint: 'Trace a request end to end into Langfuse.' },
  { id: 'ci-eval-gate', name: 'Eval gate in CI blocking on regression', track: 'P6', must_know: 1, hint: 'Make a plausible improvement fail the build.' },
  // P7
  { id: 'prompt-caching', name: 'Prompt caching arithmetic and break-even', track: 'P7', must_know: 1, hint: 'Below the minimum prefix, caching silently does nothing.' },
  { id: 'batch-api', name: 'Batch APIs: the only guaranteed 50%', track: 'P7', must_know: 1, hint: 'Move the eval runs to batch.' },
  { id: 'model-routing', name: 'Cheap-first with escalation on a real signal', track: 'P7', must_know: 0, hint: 'The escalation signal is the whole engineering problem.' },
  { id: 'cost-modeling', name: 'Cost per request and per 1k, tracked over versions', track: 'P7', must_know: 1, hint: 'Put the number on the dashboard.' },
  { id: 'token-budgeting', name: 'Token budgeting and context trimming', track: 'P7', must_know: 1, hint: 'Crossing a context tier boundary is a step function.' },
  // P8
  { id: 'retrieval-decision', name: 'When NOT to retrieve (the corpus-size framework)', track: 'P8', must_know: 1, hint: 'Long context, grep, hybrid, or agentic: pick and defend.' },
  { id: 'chunking-strategies', name: 'Structural chunking and metadata injection', track: 'P8', must_know: 1, hint: 'Parsing is 80% of the work.' },
  { id: 'contextual-retrieval', name: 'Contextual chunk prefixes / late chunking', track: 'P8', must_know: 1, hint: 'Best cost-benefit in the pipeline, still underused.' },
  { id: 'hybrid-retrieval', name: 'Hybrid BM25 + dense with RRF', track: 'P8', must_know: 1, hint: 'Dense alone loses rule numbers and SKUs.' },
  { id: 'reranking', name: 'Cross-encoder reranking', track: 'P8', must_know: 1, hint: 'The highest value five lines you will add.' },
  { id: 'retrieval-metrics', name: 'recall@k, NDCG, MRR, and the recall@50 vs @5 diagnostic', track: 'P8', must_know: 1, hint: 'The gap tells you whether a reranker can help at all.' },
  { id: 'metadata-filtering', name: 'Filtered search and silent recall collapse', track: 'P8', must_know: 1, hint: 'Ask for 10, get 3, and nothing errors.' },
  { id: 'abstention', name: 'Abstention correctness and citation precision', track: 'P8', must_know: 1, hint: 'Almost never measured, always broken.' },
  // P9
  { id: 'agent-bare-loop', name: 'The bare agent loop in ~150 lines', track: 'P9', must_know: 1, hint: 'No framework. Everything else is a variation on this.' },
  { id: 'tool-design', name: 'Tool design: consolidation, enums, no opaque IDs', track: 'P9', must_know: 1, hint: 'Expose schedule_event, not three primitives.' },
  { id: 'tool-errors', name: 'Errors as prompts, and idempotency keys', track: 'P9', must_know: 1, hint: 'A stack trace gets a loop; a sentence gets a retry.' },
  { id: 'pass-k-reliability', name: 'pass^k vs pass@k', track: 'P9', must_know: 1, hint: '70% pass@1 can be 25% pass^5.' },
  { id: 'context-engineering', name: 'Compaction, subagent isolation, progressive disclosure', track: 'P9', must_know: 1, hint: 'Measure the context rot curve on your own task.' },
  { id: 'durable-vs-checkpoint', name: 'Checkpointing vs durable execution', track: 'P9', must_know: 0, hint: 'A checkpointer means you still own retry and dedup.' },
  { id: 'mcp-server-2026', name: 'MCP on the 2026-07-28 spec', track: 'P9', must_know: 1, hint: 'server/discover, MRTR, ttlMs. Then attack it.' },
  { id: 'agent-frameworks', name: 'Pydantic AI and LangGraph, evaluated late', track: 'P9', must_know: 0, hint: 'Learn what each replaces after you hand-rolled it.' },
  // P10
  { id: 'icp-jtbd', name: 'ICP and job to be done, in one sentence', track: 'P10', must_know: 1, hint: 'Who, doing what, dissatisfied how.' },
  { id: 'distribution-channel', name: 'Pick one channel and test it', track: 'P10', must_know: 1, hint: 'One channel, measured, not five assumed.' },
  { id: 'pricing-unit-economics', name: 'Pricing defended by the cost model', track: 'P10', must_know: 1, hint: 'One number, defended with P7 arithmetic.' },
  { id: 'user-feedback-loop', name: 'One real user, and the loop from their feedback', track: 'P10', must_know: 1, hint: 'Ten users on a real workflow beats zero.' },
];

const PHASE_BASE = 16; // P0 -> 16 ... P10 -> 26

export function seedPTracks(db: Database.Database): number {
  const insert = db.prepare(
    `INSERT INTO tracks (code, title, position, status, prereq_codes, completion_test, current_as_of, kind, guidance_policy)
     SELECT ?, ?, ?, 'pending', ?, ?, ?, ?, ?
     WHERE NOT EXISTS (SELECT 1 FROM tracks WHERE code = ?)`,
  );
  let added = 0;
  for (const t of P_TRACKS) {
    added += insert.run(t.code, t.title, t.position, JSON.stringify(t.prereqs), t.completionTest, today(), t.kind, t.guidance, t.code).changes;
  }
  return added;
}

/** T-tracks keep their default kind 'ml' and write_from_empty policy; set explicitly for clarity. */
export function markMlTracks(db: Database.Database): number {
  return db.prepare("UPDATE tracks SET kind = 'ml' WHERE code LIKE 'T%' AND (kind IS NULL OR kind = '')").run().changes;
}

export function seedPSkills(db: Database.Database): number {
  const trackId = db.prepare('SELECT id FROM tracks WHERE code = ?');
  const insert = db.prepare(
    `INSERT INTO skills (id, name, phase, must_know, build_hint, mastery, confidence, on_curriculum, track_id, source)
     SELECT ?, ?, ?, ?, ?, 0, 0, 1, ?, 'v3-production'
     WHERE NOT EXISTS (SELECT 1 FROM skills WHERE id = ?)`,
  );
  let added = 0;
  for (const s of P_SKILLS) {
    const t = trackId.get(s.track) as { id: number } | undefined;
    const phase = PHASE_BASE + Number(s.track.slice(1));
    added += insert.run(s.id, s.name, phase, s.must_know, s.hint, t?.id ?? null, s.id).changes;
  }
  return added;
}

// ---- the per-domain guidance policy -----------------------------------------------------

export interface GuidancePolicy {
  policy: 'write_from_empty' | 'worked_example_first';
  track_code: string | null;
  guard_active: boolean;
  reason: string;
}

/**
 * Expertise reversal: worked examples beat blank pages for novices and reverse for experts.
 * The guard only fires where he is already expert; on production tracks he reads a reference
 * first, modifies it, and only then writes from empty.
 */
export function guidanceFor(db: Database.Database, buildId: number): GuidancePolicy {
  const row = db
    .prepare(
      `SELECT t.code AS code, t.guidance_policy AS policy
         FROM builds b
         LEFT JOIN lessons l ON l.id = b.lesson_id
         LEFT JOIN tracks  t ON t.id = l.track_id
        WHERE b.id = ?`,
    )
    .get(buildId) as { code: string | null; policy: string | null } | undefined;
  const policy = (row?.policy === 'worked_example_first' ? 'worked_example_first' : 'write_from_empty') as GuidancePolicy['policy'];
  return {
    policy,
    track_code: row?.code ?? null,
    guard_active: policy === 'write_from_empty',
    reason:
      policy === 'write_from_empty'
        ? 'He is past novice here. Blank page; the guard is on.'
        : 'He is a novice here. Show a worked reference first, have him modify it, then write from empty. The guard is off.',
  };
}

// ---- reveal and contrast ----------------------------------------------------------------

/**
 * Productive Failure is generate THEN instruct. The consolidation step is where load drops and
 * the learning sticks, so it is mandatory before review.
 */
export function recordReveal(db: Database.Database, buildId: number, notes: string): { recorded: boolean; reason: string } {
  const build = db.prepare('SELECT id, state FROM builds WHERE id = ?').get(buildId) as { id: number; state: string } | undefined;
  if (!build) return { recorded: false, reason: `no build #${buildId}` };
  if (!notes.trim()) return { recorded: false, reason: 'the contrast notes are the point; an empty reveal records nothing' };
  db.prepare('UPDATE builds SET reveal_notes = ?, revealed_at = ? WHERE id = ?').run(notes, now(), buildId);
  return { recorded: true, reason: 'reveal recorded. Review may proceed.' };
}

export function hasRevealed(db: Database.Database, buildId: number): boolean {
  const r = db.prepare('SELECT revealed_at FROM builds WHERE id = ?').get(buildId) as { revealed_at: string | null } | undefined;
  return Boolean(r?.revealed_at);
}

// ---- the delayed unaided rebuild --------------------------------------------------------

/**
 * A build that passed on the day it was written is not evidence of durable skill. In the
 * controlled study, 3 of 9 students who succeeded on the day failed the same task two weeks
 * later. So review lands a build in 'provisional', and only an unaided rebuild makes it 'done'.
 */
export function markProvisional(db: Database.Database, buildId: number): { state: string; rebuild_due: string } {
  const due = new Date(Date.now() + REBUILD_DAYS * 86400000).toISOString().slice(0, 10);
  db.prepare("UPDATE builds SET state = 'provisional', rebuild_due = ? WHERE id = ?").run(due, buildId);
  return { state: 'provisional', rebuild_due: due };
}

export function rebuildsDue(db: Database.Database): Array<{ id: number; solution_path: string; rebuild_due: string; topic: string | null }> {
  return db
    .prepare(
      `SELECT b.id, b.solution_path, b.rebuild_due, l.topic
         FROM builds b LEFT JOIN lessons l ON l.id = b.lesson_id
        WHERE b.state = 'provisional' AND b.rebuild_due IS NOT NULL AND b.rebuild_due <= ?
        ORDER BY b.rebuild_due`,
    )
    .all(today()) as Array<{ id: number; solution_path: string; rebuild_due: string; topic: string | null }>;
}

export function completeRebuild(db: Database.Database, buildId: number, unaided: boolean): { state: string; reason: string } {
  const b = db.prepare('SELECT id, state FROM builds WHERE id = ?').get(buildId) as { id: number; state: string } | undefined;
  if (!b) return { state: 'unknown', reason: `no build #${buildId}` };
  if (b.state !== 'provisional') return { state: b.state, reason: `build #${buildId} is '${b.state}', not awaiting a rebuild` };
  if (!unaided) {
    const due = new Date(Date.now() + REBUILD_DAYS * 86400000).toISOString().slice(0, 10);
    db.prepare('UPDATE builds SET rebuild_due = ? WHERE id = ?').run(due, buildId);
    return { state: 'provisional', reason: `needed help, so it is not durable yet. Rescheduled to ${due}.` };
  }
  db.prepare("UPDATE builds SET state = 'done' WHERE id = ?").run(buildId);
  return { state: 'done', reason: 'rebuilt unaided after the delay. That is the only evidence that counts.' };
}

// ---- mode ------------------------------------------------------------------------------

export type Mode = 'course' | 'venture' | 'free';

export function currentMode(db: Database.Database): { mode: Mode; reason: string; next_track: string | null } {
  const meta = db.prepare("SELECT value FROM meta WHERE key = 'mode'").get() as { value: string } | undefined;
  const forced = meta?.value as Mode | undefined;

  const spineLeft = db
    .prepare("SELECT code FROM tracks WHERE kind = 'production' AND status != 'complete' AND position <= 7 ORDER BY position LIMIT 1")
    .get() as { code: string } | undefined;
  const venture = db.prepare("SELECT id, title FROM ventures WHERE stage = 'active'").get() as { id: number; title: string } | undefined;

  if (forced === 'free') return { mode: 'free', reason: 'free build mode, set explicitly', next_track: spineLeft?.code ?? null };
  if (spineLeft) {
    return { mode: 'course', reason: `the spine is not finished: ${spineLeft.code} is next, and everything later assumes a deployed service.`, next_track: spineLeft.code };
  }
  if (venture) {
    return { mode: 'venture', reason: `spine complete. "${venture.title}" now decides what gets built.`, next_track: null };
  }
  return { mode: 'course', reason: 'spine complete and no active venture. Activate one, or use free build.', next_track: null };
}

export function setMode(db: Database.Database, mode: Mode): void {
  db.prepare("INSERT INTO meta (key, value) VALUES ('mode', ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value").run(mode);
}

/**
 * Venture Mode picks at the intersection of what the venture needs and where he is weakest.
 * Skills the venture names come first, ordered by his mastery ascending.
 */
export function ventureNextBuild(db: Database.Database, neededSkillIds: string[]): Array<{ id: string; name: string; mastery: number; build_hint: string }> {
  if (neededSkillIds.length === 0) {
    return db
      .prepare("SELECT id, name, mastery, build_hint FROM skills WHERE on_curriculum = 1 AND must_know = 1 ORDER BY mastery ASC LIMIT 3")
      .all() as Array<{ id: string; name: string; mastery: number; build_hint: string }>;
  }
  const marks = neededSkillIds.map(() => '?').join(',');
  return db
    .prepare(`SELECT id, name, mastery, build_hint FROM skills WHERE id IN (${marks}) ORDER BY mastery ASC LIMIT 3`)
    .all(...neededSkillIds) as Array<{ id: string; name: string; mastery: number; build_hint: string }>;
}

// ---- OSS track -------------------------------------------------------------------------
// Measured 2026-08-22 via the GitHub API: vLLM 23 open good-first-issues and 62% of merges
// external; transformers 0 GFI but 39 unclaimed "Good Second Issue"; TRL 5% external (trap);
// litellm 95 of 100 closed PRs unmerged (trap).

export const OSS_REPOS: Array<{ repo: string; verdict: string; label: string }> = [
  { repo: 'vllm-project/vllm', verdict: 'Best target. 62% of merges are external and your FlashAttention/KV-cache work is load-bearing. Note: >500 LOC needs an RFC first, and p75 time-to-merge is ~11 days.', label: 'good first issue' },
  { repo: 'huggingface/transformers', verdict: 'Best hidden value. 0 open good-first-issues but 39 unclaimed Good Second Issues, which is exactly the gap someone who hand-wrote attention can fill.', label: 'Good Second Issue' },
  { repo: 'modelcontextprotocol/python-sdk', verdict: 'Low barrier, low prestige. Fine for breaking the seal on a first merge.', label: 'good first issue' },
  { repo: 'huggingface/trl', verdict: 'TRAP. 60 of 66 recent merges were maintainers; ~5% external.', label: '' },
  { repo: 'BerriAI/litellm', verdict: 'TRAP. 95 of the last 100 closed PRs were closed unmerged.', label: '' },
];

export function addOssTarget(
  db: Database.Database,
  args: { repo: string; issue_url: string; issue_title: string; difficulty?: string; notes?: string },
): number {
  const info = db
    .prepare(
      `INSERT INTO oss_targets (repo, issue_url, issue_title, difficulty, state, notes, created_at)
       VALUES (?, ?, ?, ?, 'candidate', ?, ?)`,
    )
    .run(args.repo, args.issue_url, args.issue_title, args.difficulty ?? 'first', args.notes ?? '', now());
  return Number(info.lastInsertRowid);
}

export function updateOssTarget(
  db: Database.Database,
  id: number,
  args: { state?: string; pr_url?: string; review_cycles?: number; notes?: string },
): { ok: boolean; reason: string } {
  const t = db.prepare('SELECT id, repo FROM oss_targets WHERE id = ?').get(id) as { id: number; repo: string } | undefined;
  if (!t) return { ok: false, reason: `no oss target #${id}` };
  const merged = args.state === 'merged' ? now() : null;
  db.prepare(
    `UPDATE oss_targets
        SET state = COALESCE(?, state), pr_url = COALESCE(?, pr_url),
            review_cycles = COALESCE(?, review_cycles), notes = COALESCE(?, notes),
            merged_at = COALESCE(?, merged_at)
      WHERE id = ?`,
  ).run(args.state ?? null, args.pr_url ?? null, args.review_cycles ?? null, args.notes ?? null, merged, id);
  if (args.state === 'merged') {
    db.prepare(
      `INSERT INTO systems (title, repo_url, kind, status, created_at, shipped_at)
       SELECT ?, ?, 'product', 'shipped', ?, ?
       WHERE NOT EXISTS (SELECT 1 FROM systems WHERE title = ?)`,
    ).run(`PR: ${t.repo}`, args.pr_url ?? '', now(), now(), `PR: ${t.repo}`);
    return { ok: true, reason: 'merged, and recorded as capstone rung 6 evidence.' };
  }
  return { ok: true, reason: `updated to ${args.state ?? 'unchanged'}` };
}

export function ossStatus(db: Database.Database): { targets: Array<Record<string, unknown>>; merged: number; repos: typeof OSS_REPOS } {
  const targets = db.prepare("SELECT * FROM oss_targets WHERE state != 'abandoned' ORDER BY id DESC").all() as Array<Record<string, unknown>>;
  const merged = (db.prepare("SELECT COUNT(*) c FROM oss_targets WHERE state = 'merged'").get() as { c: number }).c;
  return { targets, merged, repos: OSS_REPOS };
}

// ---- the cost drill --------------------------------------------------------------------

export interface CostAnswer { tokens_per_day?: number; usd_per_day?: number }

/** Within 20% counts. The habit is ending every design answer with a number, not precision. */
export function scoreCostDrill(
  db: Database.Database,
  scenario: string,
  expected: CostAnswer,
  answer: CostAnswer,
): { correct: boolean; off_by_ratio: number | null; reason: string } {
  const e = expected.usd_per_day ?? expected.tokens_per_day;
  const a = answer.usd_per_day ?? answer.tokens_per_day;
  let ratio: number | null = null;
  let correct = false;
  if (typeof e === 'number' && typeof a === 'number' && e > 0) {
    ratio = Number((a / e).toFixed(3));
    correct = ratio >= 0.8 && ratio <= 1.2;
  }
  db.prepare(
    `INSERT INTO cost_drills (scenario, expected_json, answer_json, correct, off_by_ratio, created_at)
     VALUES (?, ?, ?, ?, ?, ?)`,
  ).run(scenario, JSON.stringify(expected), JSON.stringify(answer), correct ? 1 : 0, ratio, now());
  return {
    correct,
    off_by_ratio: ratio,
    reason: correct
      ? 'within 20%. The habit is the point.'
      : ratio === null
        ? 'no comparable number given. A design answer without a number is the failure mode.'
        : `off by ${ratio}x. Redo the arithmetic out loud.`,
  };
}

export function costDrillRecord(db: Database.Database): { attempts: number; correct: number; last: Record<string, unknown> | null } {
  const attempts = (db.prepare('SELECT COUNT(*) c FROM cost_drills').get() as { c: number }).c;
  const correct = (db.prepare('SELECT COUNT(*) c FROM cost_drills WHERE correct = 1').get() as { c: number }).c;
  const last = (db.prepare('SELECT * FROM cost_drills ORDER BY id DESC LIMIT 1').get() ?? null) as Record<string, unknown> | null;
  return { attempts, correct, last };
}

// ---- the teaching feedback loop -------------------------------------------------------

/**
 * Record what this session taught ME about teaching him. These surface at every
 * faizos_lesson_start, which is the mechanism that stops him having to give the same
 * correction twice. Deduped on the note text; a repeat raises the weight.
 */
export function recordInsight(db: Database.Database, note: string, weight = 1, mode = 'course'): { recorded: boolean; reason: string } {
  const trimmed = note.trim();
  if (trimmed.length < 20) return { recorded: false, reason: 'an insight that short teaches nothing next session' };
  db.prepare(
    `INSERT INTO insights (ts, note, weight, mode) VALUES (?, ?, ?, ?)
     ON CONFLICT(note) DO UPDATE SET weight = weight + 1, active = 1, ts = excluded.ts`,
  ).run(now(), trimmed, weight, mode);
  return { recorded: true, reason: 'recorded. It loads at the start of every future lesson.' };
}

/**
 * Did today's teaching get captured? A session that ran a lesson and recorded nothing has
 * dropped whatever it learned. The Stop hook uses this to refuse to close.
 */
export function insightGap(db: Database.Database): { last_lesson: string | null; last_insight: string | null; gap: boolean } {
  // Session independent, and it must stay identical to the copy inlined in hooks/session-stop.sh.
  // Calendar days are wrong here because one lesson often spans several of them.
  const lastLesson = (db.prepare('SELECT MAX(ts) t FROM lessons').get() as { t: string | null }).t;
  const lastInsight = (db.prepare('SELECT MAX(ts) t FROM insights').get() as { t: string | null }).t;
  return {
    last_lesson: lastLesson,
    last_insight: lastInsight,
    gap: Boolean(lastLesson) && (!lastInsight || lastLesson! > lastInsight),
  };
}

// ---- the 20 lesson plan, and a progress bar computed from real rows ----------------------

export const LESSONS: Array<{ n: number; slug: string; name: string; track: string }> = [
  { n: 1,  slug: 'tokencost', name: 'what an AI feature costs',            track: 'P7' },
  { n: 2,  slug: 'ratecard',  name: 'rate cards: dicts, lists and loops',  track: 'P7' },
  { n: 3,  slug: 'meter',     name: 'an instrumented LLM client',          track: 'P0' },
  { n: 4,  slug: 'contract',  name: 'structured output that never breaks', track: 'P5' },
  { n: 5,  slug: 'synth',     name: 'build the eval set',                  track: 'P6' },
  { n: 6,  slug: 'harness',   name: 'the assertion runner and CI gate',    track: 'P6' },
  { n: 7,  slug: 'triage',    name: 'error analysis on 100+ traces',       track: 'P6' },
  { n: 8,  slug: 'judge',     name: 'an LLM judge you can trust',          track: 'P6' },
  { n: 9,  slug: 'bm25',      name: 'lexical retrieval from scratch',      track: 'P8' },
  { n: 10, slug: 'embed',     name: 'vector index and chunking sweep',     track: 'P8' },
  { n: 11, slug: 'hybrid',    name: 'RRF fusion and reranking',            track: 'P8' },
  { n: 12, slug: 'grounded',  name: 'citations, abstention, injection',    track: 'P8' },
  { n: 13, slug: 'loop',      name: 'an agent in 150 lines, no framework', track: 'P9' },
  { n: 14, slug: 'control',   name: 'budgets, resume, human approval',     track: 'P9' },
  { n: 15, slug: 'mcp',       name: 'a server on the 2026-07-28 spec',     track: 'P9' },
  { n: 16, slug: 'service',   name: 'async FastAPI that does not block',   track: 'P1' },
  { n: 17, slug: 'store',     name: 'Postgres, pgvector, real SQL',        track: 'P4' },
  { n: 18, slug: 'ship-it',   name: 'Docker, deploy, CI with OIDC',        track: 'P2' },
  { n: 19, slug: 'prove',     name: 'the ML evidence sprint',              track: 'T6' },
  { n: 20, slug: 'capstone',  name: 'shipped, with a results table',       track: 'P10' },
];

function bar(done: number, total: number, width = 20): string {
  const filled = total === 0 ? 0 : Math.round((done / total) * width);
  return '#'.repeat(filled) + '.'.repeat(width - filled);
}

export interface LessonProgress {
  lessons: { done: number; total: number; pct: number; bar: string };
  skills: { touched: number; total: number; pct: number; bar: string };
  ml: { touched: number; total: number; pct: number; bar: string };
  capstone: { solid: number; total: number; pct: number; bar: string };
  next: { n: number; slug: string; name: string; track: string } | null;
  rendered: string;
}

/**
 * Everything here is counted from real rows. A lesson counts once its build leaves
 * 'awaiting_student'; a skill counts once its mastery is above zero; a rung counts only when
 * the capstone scorer says SOLID. Nothing is estimated and nothing flatters.
 */
export function lessonProgress(db: Database.Database, capstoneSolid?: number): LessonProgress {
  const doneBuilds = (db.prepare(
    "SELECT COUNT(*) c FROM builds WHERE state IN ('done','provisional','unlocked')",
  ).get() as { c: number }).c;
  const lessonsDone = Math.min(doneBuilds, LESSONS.length);

  // Split by kind. Lumping them together reads as 50% done when every production skill is at
  // zero, which overstates readiness. Production is the critical path; ML is already banked.
  const q = (where: string): number =>
    (db.prepare(`SELECT COUNT(*) c FROM skills s LEFT JOIN tracks t ON t.id = s.track_id WHERE ${where}`).get() as { c: number }).c;
  const prodTouched = q("t.kind IN ('production','ship') AND s.mastery > 0");
  const prodTotal = q("t.kind IN ('production','ship')");
  const mlTouched = q("(t.kind = 'ml' OR t.kind IS NULL) AND s.mastery > 0");
  const mlTotal = q("(t.kind = 'ml' OR t.kind IS NULL)");
  const touched = prodTouched;
  const totalSkills = prodTotal;

  const solid = capstoneSolid ?? 0;
  const next = LESSONS[lessonsDone] ?? null;

  const pct = (a: number, b: number): number => (b === 0 ? 0 : Math.round((a / b) * 100));
  const L = { done: lessonsDone, total: LESSONS.length, pct: pct(lessonsDone, LESSONS.length), bar: bar(lessonsDone, LESSONS.length) };
  const S = { touched, total: totalSkills, pct: pct(touched, totalSkills), bar: bar(touched, totalSkills) };
  const C = { solid, total: 8, pct: pct(solid, 8), bar: bar(solid, 8) };

  const pad = (s: string, n: number): string => s + ' '.repeat(Math.max(0, n - s.length));
  const M = { touched: mlTouched, total: mlTotal, pct: pct(mlTouched, mlTotal), bar: bar(mlTouched, mlTotal) };
  const rendered = [
    `Lessons     ${L.bar}  ${pad(`${L.done}/${L.total}`, 8)}${L.pct}%`,
    `Production  ${S.bar}  ${pad(`${S.touched}/${S.total}`, 8)}${S.pct}%   <- the critical path`,
    `ML (banked) ${M.bar}  ${pad(`${M.touched}/${M.total}`, 8)}${M.pct}%   understood, not yet evidenced`,
    `Capstone    ${C.bar}  ${pad(`${C.solid}/${C.total}`, 8)}${C.pct}%   rungs with a real metric row`,
    next ? `\nNext        L${next.n} ${next.slug} - ${next.name}  (${next.track})` : '\nAll 20 lessons complete.',
  ].join('\n');

  return { lessons: L, skills: S, ml: M, capstone: C, next, rendered };
}

// ---- CLI: tsx src/v3.ts seed [--db <path>] ----------------------------------------------

const invokedDirectly = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (invokedDirectly) {
  const flag = process.argv.indexOf('--db');
  const dbPath = flag !== -1 && process.argv[flag + 1] ? (process.argv[flag + 1] as string) : DEFAULT_DB;
  const { default: DB } = await import('better-sqlite3');
  const db = new DB(dbPath, { fileMustExist: true });
  db.pragma('journal_mode = WAL');
  const cmd = process.argv[2] ?? 'seed';
  if (cmd === 'progress') {
    const { scoreCapstone } = await import('./generators.js');
    const solid = scoreCapstone(db).filter((r) => r.status === 'SOLID').length;
    console.log('\n' + lessonProgress(db, solid).rendered + '\n');
  } else if (cmd === 'seed') {
    console.log(`P-tracks seeded:   ${seedPTracks(db)}`);
    console.log(`T-tracks marked:   ${markMlTracks(db)}`);
    console.log(`P-skills seeded:   ${seedPSkills(db)}`);
  } else {
    console.error('unknown command (use seed)');
    db.close();
    process.exit(1);
  }
  db.close();
}
