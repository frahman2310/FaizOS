# FaizOS v2 changelog

What changed between v1 and v2, by section. Started at Phase 5, finished at Phase 7.

## Schema (Phase 1)

Additive only, via a new minimal migration runner (`migrations/`, `schema_migrations`,
`src/migrate.ts`). New columns: lessons gained mode, depth, track_id, hint_max_rung,
student_wrote; skills gained track_id, source; insights gained mode. New tables: tracks,
systems, experiments, errors, code_reviews, ventures, evidence, frontier, builds. The
partial unique index on ventures(wip_lock) WHERE stage = 'active' makes the database itself
refuse a second active venture. Two flagged additive extensions beyond spec 9.1:
builds.test_path and evidence.jtbd. No pre-existing table, column or row was touched;
verified against docs/v1-rowcounts.json.

## Backfill (Phase 2)

Eleven tracks seeded from spec section 5. All 66 skills and 43 of 44 lessons mapped to
tracks (one protocol-update lesson has no skills and stays NULL). The 44 v1 builds live in
systems as kind study with no metric, which is truthful. The error taxonomy seeded with 8
categories parsed from the v1 friction record, including the user-approved ordering-pairing
category.

## Tools and hooks (Phase 3)

faizos_lesson_start now leads with the active build, the failing-test path, the top open
error categories, the current track with frontier notes, due reviews and the active venture.
faizos_record_lesson classifies errors, records the deepest hint rung, student_wrote, mode
and depth. faizos_ship writes systems rows with kind and real metrics. New tools:
faizos_track_status, faizos_spec_build, faizos_hint (a four rung ladder that never skips),
faizos_review_code (three passes recorded), faizos_log_experiment (seed spread at n >= 3),
faizos_error_report, faizos_unlock_build. The PreToolUse guard denies Write/Edit against an
awaiting_student solution path, tested by violation. The Stop hook refuses to close over an
open build. The server migrates its database on startup.

## Commands (Phase 4)

New: /faiz-learn, /faiz-spec, /faiz-hint, /faiz-review (three-pass code review), /faiz-run,
/faiz-errors, /faiz-drill (the old /faiz-review FSRS flow lives here), /faiz-venture,
/faiz-frontier, /faiz-unlock. Rewritten: /faiz (build-heavy dashboard) and /faiz-build
(Build Mode with milestone spine and the explain/flow/ship depth toggle). All old command
names keep working.

## Artefacts (Phase 5)

New deterministic generators: EXPERIMENTS.md (runs, cost, spread, noise verdicts), ERRORS.md
(taxonomy with trend), VENTURES.md (gitignored by default; venture evidence stays local until
a deliberate publish decision), FRONTIER.md (by track, with 60 day drift flags). CAPSTONE.md
is now generated and auto scored from systems and experiments; every rung prints the rule it
was scored by, and the first honest render came out 1 solid, 7 missing, which is stricter
than the v1 hand audit and correctly so.

## Venture arm (Phase 6)

Five stages in src/venture.ts, split so everything deterministic lives in code and everything
semantic happens in session. Stage 1 ingest fetches the prompt's 8 free-tier sources
(HN Algolia, GitHub, SEC EDGAR with a proper User-Agent, Companies House and Product Hunt
behind env keys that skip gracefully, YC RFS, MCP registry, arXiv) sequentially with a polite
delay, dedupes on url+excerpt, and never scrapes G2, Capterra, Upwork, Fiverr or app stores.
Stage 2 classification runs in session: faizos_venture_pending surfaces unclassified rows,
faizos_venture_classify_save writes JTBD, importance and dissatisfaction back and groups rows
into candidate ventures. Stage 3 corroboration is deterministic: two or more independent
source families advance a venture; multiple hits within one family do not count. Stage 4
scores the six axes with fixed weights (2,3,3,3,1,2) normalised to 0..5, and refuses
uncorroborated ventures. Stage 5 activates with a 14 day deadline and a five milestone spine;
the partial unique index makes the database refuse a second active venture, and a kill
requires a post mortem that lands in insights. The four spec 8.7 opportunities are seeded as
candidates with their evidence. scripts/install-crons.sh contains the daily ingest line and
is never run automatically. All ten venture tests mock the fetcher; zero network in tests.

## Frontier ingest (Phase 7)

The frontier table is seeded with the ten spec section 6 subsections, each mapped to the
track it affects (6.10 is general and maps to none). src/frontier.ts fetches weekly: recent
arXiv entries for the current track and the next one only, because frontier for tracks far
ahead is noise. Fetch is deterministic and dedupes on url+title; summarising what an item
changes for the current build happens in session through faizos_frontier_ingest, which also
reports every track whose current_as_of has drifted past 60 days. /faiz-frontier renders the
week grouped by track. The weekly cron line lives in scripts/install-crons.sh next to the
daily venture line; the script is provided, never run automatically. Three frontier tests,
all mocked.

## Definition of done

Checked at the end of Phase 7: full test suite and smoke green; every pre-existing row intact
against docs/v1-rowcounts.json; the guard denies a write to an awaiting_student solution path
through the real hook script; the database refuses a second active venture; CAPSTONE.md
regenerates auto scored; the learn and build loops write to skills, insights, revisions and
errors end to end; docs/v1-audit.md and this changelog exist.

---

# FaizOS v3 — the curriculum

Built 2026-08-22 to `FaizOS-v3-Curriculum-Spec.md`, which is grounded in 4,894 job descriptions
plus five research streams. The governing number: deployment appears in 78.3% of AI-engineering
postings and self-hosting models in 2.5%, so the production spine becomes the critical path and
T0-T10 become the evidence-conversion layer.

## Schema (migration 002)

Additive only, verified against docs/v1-rowcounts.json. `tracks` gained kind and
guidance_policy; `builds` gained rebuild_due, reveal_notes and revealed_at; `systems` gained
p95_ms and cost_per_1k. New tables: oss_targets, cost_drills. down() reverts cleanly and the
up-down-up round trip was rehearsed on a copy before touching the live database.

## The pedagogy corrections

**Guidance is now per domain.** Expertise reversal says worked examples beat blank pages for
novices and the advantage reverses as expertise grows. The PreToolUse guard reads
tracks.guidance_policy instead of firing unconditionally: it stays on for the ML tracks, where
he is past novice, and stands down on the production tracks, where forcing a blank page would
produce failure he cannot learn from. Tested in both directions.

**Reveal and contrast is mandatory.** faizos_review_code refuses until faizos_reveal_contrast
has recorded his diff against the reference. Productive failure is generate THEN instruct; the
consolidation phase is where load drops and generation alone is not what the evidence tested.

**Review no longer completes a build.** It lands in `provisional` with a 14 day rebuild date.
In the controlled study, 3 of 9 students who succeeded on the day failed the same task two
weeks later. Only an unaided rebuild moves a build to `done`; needing help reschedules it
honestly. studentWroteRatio counts provisional as written, because the gate measures durability
and not authorship.

## The production spine

Eleven P-tracks (P0 engineering floor through P10 ship) and 67 production skills, none of which
v1 covered. currentTrack now orders production before ship before ml, so the spine outranks the
ML tracks until P7 is complete.

## Modes

faizos_mode returns course, venture or free. Course holds while any P0-P7 track is unfinished,
because everything later assumes a deployed service. Venture Mode picks at the intersection of
what the active venture needs and where he is weakest.

## Tools and commands

New tools: faizos_guidance, faizos_reveal_contrast, faizos_rebuilds_due,
faizos_complete_rebuild, faizos_mode, faizos_oss, faizos_cost_drill. faizos_state now leads with
a due rebuild when there is one, and carries mode, guidance and the cost drill record. New
commands: /faiz-cost (every design answer ends with a number) and /faiz-oss (the merged-PR
track, with the measured repo guidance: vLLM is the best target at 62% external merges, TRL and
litellm are traps). /faiz-spec, /faiz-review, /faiz-learn and /faiz were updated for v3.

## Capstone

The eval metric family widened to the production vocabulary (kappa, pass^k, NDCG, MRR,
faithfulness). Rung 2 now notes whether the deployed system carries p95 and cost. The closing
guidance no longer assumes rented hardware: every remaining rung runs on the M4, with Soup on
the MLX backend for rungs 3 and 5 and mx.fast.metal_kernel for rung 4.

**83 tests green, smoke green, every protected v1 row intact.**
