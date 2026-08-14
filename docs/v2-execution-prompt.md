# FaizOS v2: Claude Code execution prompt

**How to use this.** Put `FaizOS-v2-Research-and-Spec.md` in the root of the FaizOS repository, open Claude Code in that repository, and paste the block below. It is written to be run phase by phase across several sessions, not in one shot. The prompt tells Claude Code to stop at the end of each phase.

If you want to run only one phase later, paste the same block and add `Run Phase N only.` at the end.

---

## The prompt

```
You are implementing FaizOS v2, a restructure of my personal AI learning system.

Read `FaizOS-v2-Research-and-Spec.md` in this repository first, in full, before writing any
code. It is the specification. This prompt is the execution contract. Where they disagree,
the spec wins on WHAT and this prompt wins on HOW.

Also read, for context on what exists today: README.md, COURSE.md, CAPSTONE.md, the
faizos-core/ source tree, .claude/ commands, and hooks/.

## Who I am and how to work with me

I am a finance undergraduate learning to build AI systems. I can read code and reason about
architecture. I am not yet fluent at writing code from an empty file, and fixing that is the
entire point of this restructure. So: when you write code in this task, you are writing the
SYSTEM, not my learning exercises. Write it properly and completely.

Be blunt. If part of the spec is wrong, badly designed, or will not work in this codebase,
say so before implementing it rather than building it and mentioning the problem afterwards.
I would rather lose ten minutes to an argument than a week to a bad schema.

## Absolute constraints

1. NEVER delete, drop, rename or truncate any existing table, column or row. All schema
   changes are additive. If you believe a destructive change is necessary, stop and tell me
   why instead of doing it.
2. NEVER modify or delete existing rows in: skills, mastery, missions, streak, lessons,
   insights, revisions. Backfill means adding values to NEW columns on existing rows and
   inserting into NEW tables. Nothing else.
3. Back up faizos-core/data/faiz.db to a timestamped file OUTSIDE the repository before the
   first migration, and verify the backup opens and row counts match.
4. Work on a branch. One commit per phase. Every commit must leave `npm test` and
   `npx tsx src/smoke.ts` passing.
5. Stop at the end of each phase. Print a summary of what changed, what the tests say, and
   what the next phase will do. Wait for me before continuing.
6. If a phase turns out to need a decision I have not made, stop and ask. Do not guess on
   anything that touches the database.

## Phases

### Phase 0. Safety and audit
- Create branch `faizos-v2`.
- Back up the database as described above. Verify it.
- Run `npm test` and `npx tsx src/smoke.ts`. If either fails on the current code, STOP and
  report. Do not start migrating a broken system.
- Produce a written audit at `docs/v1-audit.md`: the current schema with every table and
  column, the current MCP tool surface, the current hook wiring, the current slash commands,
  and the current artefact generators with what each reads from. I need this to check your
  understanding before you touch anything.
- Record row counts per table in that audit.
- Commit. Stop.

### Phase 1. Schema
Implement section 9.1 of the spec exactly.
- Use a numbered migration file with explicit up and down functions. If the project has no
  migration mechanism, build a minimal one first (a `migrations/` directory, a
  `schema_migrations` table, and a runner) and say so.
- Additive only: ALTER TABLE ADD COLUMN, CREATE TABLE, CREATE INDEX.
- Include the partial unique index on ventures(wip_lock) WHERE stage = 'active'. This is
  load bearing: the database must physically refuse a second active venture.
- Run the migration against the BACKUP copy first. Verify every pre-existing table has the
  same row count as recorded in the Phase 0 audit. Only then run against live.
- Add tests that assert the new tables exist, the WIP constraint actually rejects a second
  active venture, and no pre-existing row count changed.
- Commit. Stop.

### Phase 2. Backfill
- Map the 20 existing modules onto the 11 tracks in spec section 5. Seed the `tracks` table.
  Set track_id on existing lessons and skills. Where a module maps to more than one track,
  ask me rather than guessing.
- Insert the 44 existing builds into `systems` with kind = 'study', no metric, and status
  reflecting reality. Do not invent metrics. A study build has no benchmark number and the
  record should say so.
- Parse the recurring frictions recorded in REVISIONS.md and COURSE.md into seed rows in
  `errors`, mapped onto the taxonomy in spec section 3.2. Set occurrences from how often
  each appears. Show me the parsed list before inserting it.
- Verify: every existing lesson and skill row still exists, now with a track_id.
- Commit. Stop.

### Phase 3. MCP tools and hooks
Implement spec sections 9.2 and 9.4.
- Extend faizos_lesson_start to load, before every lesson: the top 3 open error categories
  from `errors` ranked by occurrences, the current track and its frontier notes, due spaced
  repetition items, and the active venture if any.
- Extend faizos_record_lesson to classify errors into the taxonomy, record the deepest hint
  rung reached, and set student_wrote.
- Add the new tools listed in 9.2.
- Add the PreToolUse hook that blocks Write and Edit against the active build's solution
  path while the build state is `awaiting_student`. This is the most important single piece
  of this phase. Test it by actually attempting a blocked write and asserting the failure.
  The block message must point at /faiz-hint and /faiz-unlock.
- Add the SessionEnd hook that refuses to close with an unrecorded lesson or uncommitted
  build.
- Commit. Stop.

### Phase 4. Commands
Implement spec section 9.3.
- Add the new slash commands. Keep every existing command working as an alias.
- /faiz-spec must produce three things and nothing else: a plain English design brief with
  no code, a Python rules card of 3 to 6 entries in the form
  `construct -> meaning -> the one rule that trips people`, weighted toward my currently
  open error categories, and a FAILING test file at the build path.
- /faiz-hint must serve exactly one rung and refuse to skip. Rung 4 is never given
  unprompted.
- /faiz-review must run all three passes in order: my code line by line in plain English,
  then a diff against reference classified into correctness / clarity / taste, then error
  classification written to `errors`.
- Commit. Stop.

### Phase 5. Artefacts
Implement spec section 9.5.
- Add generators for EXPERIMENTS.md, ERRORS.md, VENTURES.md, FRONTIER.md.
- Rewrite the CAPSTONE.md generator so the 8 rungs are AUTO SCORED from `systems` and
  `experiments`. A rung is satisfied only if backed by a system row with a real metric. Do
  not let it flatter me.
- All generators stay deterministic with no model in the loop.
- Commit. Stop.

### Phase 6. Venture arm
Implement spec section 8.3 in stage order. Do not build stage 4 or 5 before stages 1 to 3
produce real evidence rows.
- Stage 1 ingest: free tier sources only, exactly the table in spec 8.3. Hacker News via
  Algolia, GitHub, SEC EDGAR, Companies House, YC RFS, MCP registry, Product Hunt, arXiv.
  No scraping of G2, Capterra, Upwork, Fiverr or the app stores. Respect rate limits and set
  a proper User-Agent on SEC EDGAR.
- Stage 2 extract: classifier producing job-to-be-done, importance, dissatisfaction. Every
  record stores its source URL and a raw excerpt. Never store a summary without evidence.
- Stage 3 corroborate: an opportunity advances only if it appears in at least 2 INDEPENDENT
  source families. Multiple hits within one family do not count.
- Stage 4 score: the 6 weighted axes in spec 8.3.
- Stage 5 gate: WIP limit of 1, enforced by the database index from Phase 1, plus the 14 day
  kill review with exactly three outcomes (continue, park, kill) and a mandatory post mortem
  written back to `insights` on kill.
- Seed the pipeline with the opportunities in spec 8.7, with their sources attached.
- Add the daily ingest cron for stages 1 and 2 only.
- Commit. Stop.

### Phase 7. Frontier ingest
- Seed the `frontier` table from spec section 6, one row per subsection, with URLs and an
  `affects_track_id`.
- Wire the weekly cron: pull arXiv, lab blogs and release notes for the tracks I am on or
  about to reach, write to `frontier`, and flag tracks whose current_as_of has drifted by
  more than 60 days.
- /faiz-frontier surfaces the week's ingest grouped by affected track.
- Commit. Stop.

## Code quality

- TypeScript strict. No `any` in new code.
- Every new MCP tool gets a test.
- Every new table gets a test that inserts and reads back.
- No network calls in the test suite. Mock the ingest sources.
- Keep the deterministic core deterministic. Anything with a model in the loop belongs in a
  command or a hook, never in an artefact generator.

## Writing style for anything you generate that I will read

This applies to slash command output, generated markdown, design briefs and review text.

- No em dashes. Use commas, full stops, colons or brackets.
- No "it's not X, it's Y" constructions.
- No throat clearing. Lead with the answer.
- Plain sentences. Define a new term in one sentence plus an analogy, never more.
- One idea per message when teaching. Wait for my answer before revealing the reasoning.

## Definition of done for the whole task

- `npm test` and `npx tsx src/smoke.ts` pass.
- No pre-existing row was modified or deleted, provable against the Phase 0 audit counts.
- The PreToolUse guard demonstrably blocks a write to an awaiting_student solution path.
- The database rejects a second active venture.
- CAPSTONE.md regenerates with rungs scored from real system and experiment rows.
- /faiz-learn and /faiz-build both run end to end and both write to skills, insights,
  revisions and errors.
- docs/v1-audit.md and a docs/v2-changelog.md exist, and the changelog states what changed
  between v1 and v2 per section.

Start with Phase 0. Do not proceed past it without me.
```

---

## Two follow up prompts

**After the migration is done, to run your first v2 lesson:**

```
/faiz-learn T0

Course Mode, depth = explain. Follow the v2 loop exactly:
concept, design brief, Python rules card, failing tests, then I write the whole file from
an empty buffer. Do not write any part of my solution file. Do not show me reference code
before I attempt it. If I ask for help, give me one hint rung at a time and make me ask for
each one. Review my code line by line only after the tests pass or after I explicitly give up.
```

**To kick off the venture arm once it exists:**

```
/faiz-venture ingest

Then show me only the opportunities that passed the corroboration gate, with their evidence
and source URLs attached, scored on all six axes. Tell me explicitly which ones failed the
gate and why. Do not recommend one. I will pick, and I am picking exactly one.
```

---

## Note before you run any of this

Two items in the spec gate the commercial half of the system and neither is a coding problem:

1. The UK Student visa page states you cannot be self employed. Its treatment of company
   directorship, equity and unpaid founder work is not addressed on the primary page, and
   secondary sources are unreliable on it. Confirm with Durham's international student office
   before the venture arm produces anything you intend to monetise.
2. Stripe does not support Pakistan registered entities. Your payment structure determines
   which distribution surface is even usable, so resolve it before building toward one.

Neither blocks Phases 0 through 5 or Phase 7. Both block acting on Phase 6 output.
