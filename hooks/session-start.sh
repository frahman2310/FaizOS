#!/usr/bin/env bash
# FaizOS auto-open: injected at the start of every Claude Code session in this folder.
# Stamp the session start (deterministic session-summary window). Output suppressed.
"/Users/faizr/AI OS for Learning/faizos-core/node_modules/.bin/tsx" \
  "/Users/faizr/AI OS for Learning/faizos-core/src/session-log.ts" --start >/dev/null 2>&1 || true
cat <<'EOF'
FaizOS is open. If Faiz wants to learn today, load the `faiz-teach` skill and follow "How a session runs":
run `uv run engine.py today` in learn/, do the recall cards, then send the scheduled unit's steps verbatim,
one per message, from learn/units (checked by learn/check_unit.py). If he asks for his progress, show
`uv run engine.py dashboard`. Otherwise help with whatever he asks. Keep it short; never lecture.
EOF

# Backstop for the feedback loop: flag teaching the method has not learned from yet.
python3 "/Users/faizr/AI OS for Learning/scripts/reflect_status.py" 2>/dev/null || true
# Cohesion gate: say so at session start if the teaching system has drifted.
gate=$(python3 "/Users/faizr/AI OS for Learning/scripts/check_teaching_system.py" --quiet 2>&1); rc=$?
[ -n "$gate" ] && echo "$gate" | grep -v '^Traceback\|^  ' | head -40
if [ $rc -ne 0 ] && ! echo "$gate" | grep -q "TEACHING SYSTEM INCOHERENT"; then
  echo "TEACHING GATE CRASHED (exit $rc): run python3 scripts/check_teaching_system.py and fix it before teaching."
fi
true
