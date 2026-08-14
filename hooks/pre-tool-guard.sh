#!/usr/bin/env bash
# FaizOS v2 write guard. While a build is in state 'awaiting_student', the STUDENT writes the
# solution file. Any Write/Edit against that path from the assistant is denied here, with a
# pointer at /faiz-hint and /faiz-unlock. This is what makes "he writes it" mechanical.
#
# Input: Claude Code PreToolUse JSON on stdin ({tool_name, tool_input:{file_path}}).
# Output: a deny decision when the guard fires; nothing (exit 0) otherwise.
# Fail-open: any internal error allows the call. The guard protects learning integrity; it must
# never brick ordinary file edits.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GUARD_DB="${FAIZOS_GUARD_DB:-$ROOT/faizos-core/data/faiz.db}"
export GUARD_DB ROOT
cd "$ROOT/faizos-core" 2>/dev/null || exit 0
node --input-type=commonjs -e '
let raw = "";
process.stdin.on("data", (d) => (raw += d));
process.stdin.on("end", () => {
  try {
    const input = JSON.parse(raw || "{}");
    const tool = input.tool_name || "";
    if (tool !== "Write" && tool !== "Edit") return; // only file writes are guarded
    const filePath = (input.tool_input && input.tool_input.file_path) || "";
    if (!filePath) return;
    const Database = require("better-sqlite3");
    const db = new Database(process.env.GUARD_DB, { readonly: true, fileMustExist: true });
    const build = db
      .prepare("SELECT id, solution_path FROM builds WHERE state = \x27awaiting_student\x27 ORDER BY id DESC LIMIT 1")
      .get();
    db.close();
    if (!build) return;
    const path = require("path");
    const abs = path.resolve(process.env.ROOT, build.solution_path);
    const target = path.resolve(filePath);
    if (target === abs || target.endsWith(path.sep + build.solution_path)) {
      const reason =
        "FaizOS guard: build #" + build.id + " is awaiting the student. " +
        build.solution_path + " is HIS file to write from empty. " +
        "If he is stuck, serve one hint rung with /faiz-hint. " +
        "If he explicitly hands it over, /faiz-unlock records that honestly. Until then, do not write it.";
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: reason,
        },
      }));
    }
  } catch (e) {
    // fail open
  }
});
' 2>/dev/null
exit 0
