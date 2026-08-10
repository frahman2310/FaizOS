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
git -C "$ROOT" add notebook/SESSIONS.md notebook/SUMMARY.md notebook/REVISION.md >/dev/null 2>&1 || true
if ! git -C "$ROOT" diff --cached --quiet -- notebook/SESSIONS.md notebook/SUMMARY.md notebook/REVISION.md 2>/dev/null; then
  git -C "$ROOT" commit -q -m "auto: session log + build summary + revision guide" >/dev/null 2>&1 || true
  git -C "$ROOT" push -q >/dev/null 2>&1 || true
fi

# --- job 2: nudge the model to analyze an un-closed ship (one nudge only; guarded vs loops) ---
if echo "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
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
