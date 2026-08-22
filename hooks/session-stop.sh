#!/usr/bin/env bash
# FaizOS session close. Two jobs, in order:
#   1. ALWAYS (deterministic, no model needed): write this session's summary to notebook/SESSIONS.md
#      from DB facts, and commit+push it if it changed. This is the non-negotiable session log.
#   2. If a shipped build hasn't been analyzed yet, nudge the model to run the rich close-loop once.
INPUT=$(cat)
ROOT="/Users/faizr/AI OS for Learning"
TSX="$ROOT/faizos-core/node_modules/.bin/tsx"

# --- job 1: deterministic summaries (run every stop, model-independent) ---
#   SESSIONS.md = per-session log ; SUMMARY.md = full content+build summary (per lesson/module).
"$TSX" "$ROOT/faizos-core/src/session-log.ts"      >/dev/null 2>&1 || true
"$TSX" "$ROOT/faizos-core/src/build-summary.ts"    >/dev/null 2>&1 || true
"$TSX" "$ROOT/faizos-core/src/revision-compile.ts" >/dev/null 2>&1 || true
"$TSX" "$ROOT/faizos-core/src/generators.ts" all   >/dev/null 2>&1 || true
git -C "$ROOT" add notebook/SESSIONS.md notebook/SUMMARY.md notebook/REVISION.md notebook/EXPERIMENTS.md notebook/ERRORS.md notebook/FRONTIER.md CAPSTONE.md >/dev/null 2>&1 || true
if ! git -C "$ROOT" diff --cached --quiet 2>/dev/null; then
  git -C "$ROOT" commit -q -m "auto: session log + summaries + v2 artefacts" >/dev/null 2>&1 || true
  git -C "$ROOT" push -q >/dev/null 2>&1 || true
fi

# --- job 2: refuse to close with unfinished v2 work (one nudge only; guarded vs loops) ---
if echo "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

# v3: block only on 'in_review'. That state means work was done and never recorded, which is
# the case worth protecting. 'awaiting_student' is the DESIGNED handoff state: the build has
# just been specced and he is going away to write it, possibly over hours. Blocking there
# prevented the intended workflow and bought nothing, since the build persists in the database
# and /faiz leads with it next session. Found by hitting it in real use on P0 build #1.
OPEN_BUILD=$(cd "$ROOT/faizos-core" && node --input-type=commonjs -e '
try {
  const Database = require("better-sqlite3");
  const db = new Database("data/faiz.db", { readonly: true, fileMustExist: true });
  const b = db.prepare("SELECT id, solution_path, state FROM builds WHERE state = \x27in_review\x27 ORDER BY id DESC LIMIT 1").get();
  db.close();
  if (b) process.stdout.write(b.id + " " + b.state + " " + b.solution_path);
} catch (e) {}
' 2>/dev/null)
if [ -n "$OPEN_BUILD" ]; then
  cat <<EOF
{"decision":"block","reason":"FaizOS: build $OPEN_BUILD has work that was never recorded. Before finishing: if the tests pass or he gives up, run the three-pass review (/faiz-review, which records it via faizos_review_code); if he is handing it over, /faiz-unlock records that honestly. A session never closes over an unreviewed, unrecorded build."}
EOF
  exit 0
fi

STATE=$("$TSX" "$ROOT/faizos-core/src/faiz.ts" faizos_state 2>/dev/null)
PENDING=$(printf '%s' "$STATE" | python3 -c "import json,sys
try: print(json.load(sys.stdin).get('pending_close') or '')
except Exception: print('')" 2>/dev/null)
if [ -n "$PENDING" ]; then
  cat <<EOF
{"decision":"block","reason":"FaizOS auto-close: a shipped build (mission $PENDING) hasn't been analyzed yet. Before finishing, run the close-loop now: (1) analyze it — read the repo, bank the skills with faizos_analyze, teach the one gap; (2) POST THE FULL REVISION NOTE IN CHAT (do not just save it silently — the user must SEE it), then save it with faizos_save_revision, and show the course progress bar (faizos_progress) under it; (3) call faizos_record_lesson with 1-2 new_insights (this clears the flag). If a module just hit 100%, also POST + save a Module Completion Summary. Then SHARE the compiled study guide with SendUserFile notebook/REVISION.md, and commit + push. The deterministic session log / summary / revision guide are written automatically; you still owe the user the visible note."}
EOF
fi
exit 0
