#!/usr/bin/env bash
# FaizOS auto-analyze: if a build was shipped but not yet analyzed/summarized, force the
# close-loop before the session can end. One nudge only (guarded against infinite loops).
INPUT=$(cat)
# If we already blocked once this stop-cycle, let it through (avoid loops).
if echo "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi
STATE=$("/Users/faizr/AI OS for Learning/faizos-core/node_modules/.bin/tsx" "/Users/faizr/AI OS for Learning/faizos-core/src/faiz.ts" faizos_state 2>/dev/null)
PENDING=$(printf '%s' "$STATE" | python3 -c "import json,sys
try: print(json.load(sys.stdin).get('pending_close') or '')
except Exception: print('')" 2>/dev/null)
if [ -n "$PENDING" ]; then
  cat <<EOF
{"decision":"block","reason":"FaizOS auto-close: a shipped build (mission $PENDING) hasn't been analyzed yet. Before finishing, run the close-loop now: (1) analyze it — read the repo, bank the skills with faizos_analyze, teach the one gap; (2) post the Revision Note, save it with faizos_save_revision, and show the course progress bar (faizos_progress) under it; (3) call faizos_record_lesson with 1-2 new_insights (this clears the flag). Then commit + push the journey. Then you're done."}
EOF
fi
exit 0
