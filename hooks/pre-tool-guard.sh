#!/usr/bin/env bash
# FaizOS v3 write guard. While a build is 'awaiting_student' AND its track's guidance_policy is
# 'write_from_empty', the STUDENT writes the solution file and any assistant Write/Edit is denied.
#
# v3 change: the policy is per track. Expertise reversal says worked examples beat blank pages for
# NOVICES and reverse for experts, so on production tracks (where he is a novice) the guard stands
# down and he reads a reference first. Blocking there would produce unproductive failure.
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
      .prepare(
        "SELECT b.id AS id, b.solution_path AS solution_path, " +
        "COALESCE(t.guidance_policy, \x27write_from_empty\x27) AS policy, t.code AS track " +
        "FROM builds b LEFT JOIN lessons l ON l.id = b.lesson_id LEFT JOIN tracks t ON t.id = l.track_id " +
        "WHERE b.state = \x27awaiting_student\x27 ORDER BY b.id DESC LIMIT 1"
      )
      .get();
    db.close();
    if (!build) return;
    if (build.policy !== "write_from_empty") return; // novice domain: guard stands down
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
