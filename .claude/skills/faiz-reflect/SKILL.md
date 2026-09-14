---
name: faiz-reflect
description: Learn from Faiz's answers. Reads a session's teaching exchanges, logs the evidence, and updates the faiz-teach skill in place so the method improves without contradictions. Run at every lesson close, immediately when he corrects the teaching, and whenever SessionStart reports UNREFLECTED TEACHING.
---

# Reflect: turn his answers into a better method

Two files, two jobs, never mixed:
- `docs/learning-evidence.md` holds EVIDENCE only (counts, quotes, the session ledger).
- `.claude/skills/faiz-teach/SKILL.md` holds INSTRUCTIONS only. It is the single source.

## Steps

1. **Extract.** Run, with the transcript path (the current session's, or the one SessionStart named):
   `python3 scripts/extract_teaching.py <transcript.jsonl>`
   It prints every question message and his reply since the last reflect.

2. **Score each exchange.** For each question: its type (compute, classify, trace, predict broken
   code, write, explain), right first try or not, and what recovered him if he was stuck. Note
   every sentence where he judges the teaching ("I don't understand", "this was better", "never",
   "stop") word for word. Note which features the message had: new terms introduced, a tiny
   example before real code, a picture, paths spelled out, code shown in chat vs in a file.

3. **Log it.** Append one row per part to `## Session ledger` in `docs/learning-evidence.md`
   (date | lesson/part | questions | right first try | stuck points | his feedback), update any
   measured table whose totals changed, and update the "taught" list under the ledger. Evidence only.

4. **Change the method only when justified:**
   - he stated a rule or a preference: change it now, his latest words win;
   - or the ledger shows the same pattern in 2 or more parts (for example, first-try accuracy
     drops whenever a part lacks a picture).
   Edit faiz-teach IN PLACE: rewrite the affected rule. Never append a second version of a rule.
   Then read the whole skill top to bottom and remove or rewrite anything the change contradicts.
   Cite the evidence briefly in parentheses next to the rule.

5. **Keep enforcement in step.** If a template marker changed, update the `Template markers:` line
   in faiz-teach. Validate every lesson script: `python3 scripts/check_lesson_script.py projects/<lesson>/script.md`.

6. **Mark it done:** `python3 scripts/extract_teaching.py <transcript.jsonl> --mark`, then log one
   line with `faizos_record_insight` ("REFLECT LOG: <session>, ledger row added"). A log, never a rule.

7. **Commit** the skill, the evidence file and `docs/reflect-state.json` together, with a message
   naming the evidence behind each rule change.

Never store rules anywhere else: not in memory notes, not in the insights table, not in commands.
