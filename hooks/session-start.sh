#!/usr/bin/env bash
# FaizOS auto-open: injected at the start of every Claude Code session in this folder.
# Stamp the session start (deterministic session-summary window). Output suppressed.
"/Users/faizr/AI OS for Learning/faizos-core/node_modules/.bin/tsx" \
  "/Users/faizr/AI OS for Learning/faizos-core/src/session-log.ts" --start >/dev/null 2>&1 || true
cat <<'EOF'
FaizOS is open — this is Faiz's build-and-ship home screen. Before anything else this session,
call the `faizos_state` tool and render the dashboard: a warm one-line greeting with his 🔥 streak
and last ship, his 2–3 weakest must-know skills as tiny bars, and ONE clear next step (continue a
build / start one / review). Show the menu: build · ship · analyze · review · notes · radar. If he
chooses to build, call `faizos_lesson_start` FIRST to load what FaizOS learned about teaching him,
then teach with the Brick Method. Keep it ~5 seconds to read. Never lecture.
EOF
