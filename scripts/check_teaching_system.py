#!/usr/bin/env python3
"""Check that the teaching system is one coherent pipeline. Exit 0 when all checks pass.

Usage: python3 scripts/check_teaching_system.py [--quiet]   (--quiet prints failures only)
"""
import glob
import json
import os
import re
import subprocess
import sys

ROOT = "/Users/faizr/AI OS for Learning"
MEMORY = "/Users/faizr/.claude/projects/-Users-faizr-AI-OS-for-Learning/memory"
SKILL = os.path.join(ROOT, ".claude/skills/faiz-teach/SKILL.md")

# Phrases from superseded methods. None may appear in anything that instructs Claude.
STALE = [r"Brick Method", r"one tiny concept per (message|step)", r"ONE self-contained", r"YOUR TURN zone with",
         r"insights_to_apply", r"load(s)? at the (next faizos_lesson_start|start of every future lesson)",
         r"writes? (whole files )?from empty", r"never reveal the correct answer"]
SURFACES = (glob.glob(os.path.join(ROOT, ".claude/commands/*.md"))
            + [p for p in glob.glob(os.path.join(ROOT, ".claude/skills/*/SKILL.md")) if "faiz-teach" not in p]
            + [os.path.join(ROOT, f) for f in ("hooks/session-start.sh", "hooks/session-stop.sh", "hooks/teaching-rules.sh",
                                               "faizos-core/src/server.ts", "faizos-core/src/v3.ts", "CLAUDE.md")]
            + glob.glob(os.path.join(MEMORY, "*.md")))

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


for path in SURFACES:
    if not os.path.exists(path):
        continue
    text = open(path, errors="replace").read()
    hits = [p for p in STALE if re.search(p, text, flags=re.I) and "SUPERSEDED" not in text[:400]]
    check(f"no superseded method in {os.path.relpath(path, ROOT) if path.startswith(ROOT) else os.path.basename(path)}",
          not hits, ", ".join(hits))

skill = open(SKILL).read() if os.path.exists(SKILL) else ""
check("faiz-teach skill exists", bool(skill))
for label in ("## How a session runs", "## How this file changes", "INTEGRATED.md", "check_unit.py", "engine.py"):
    check(f"skill has '{label}'", label in skill)

teaching_notes = [p for p in glob.glob(os.path.join(MEMORY, "*.md"))
                  if re.search(r"teach", os.path.basename(p)) or re.search(r"(?i)how to teach", open(p).read()[:300])]
check("memory holds one teaching pointer, not rules", len(teaching_notes) <= 1, ", ".join(map(os.path.basename, teaching_notes)))

settings = json.load(open(os.path.join(ROOT, ".claude/settings.json")))["hooks"]
wired = json.dumps(settings)
for event, needle in (("UserPromptSubmit", "teaching-rules.sh"), ("Stop", "teaching-guard.py"),
                      ("SessionStart", "session-start.sh"), ("Stop", "session-stop.sh")):
    check(f"{event} hook runs {needle}", needle in json.dumps(settings.get(event, [])))

server = open(os.path.join(ROOT, "faizos-core/src/server.ts")).read()
check("lesson_start loads no insight rules", not re.search(r"SELECT note, weight FROM insights", server))

evidence = os.path.join(ROOT, "docs/learning-evidence.md")
check("evidence file has a Session ledger", os.path.exists(evidence) and "## Session ledger" in open(evidence).read())
check("reflect state exists", os.path.exists(os.path.join(ROOT, "docs/reflect-state.json")))

for script in glob.glob(os.path.join(ROOT, "projects/*/script.md")):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts/check_lesson_script.py"), script],
                       capture_output=True, text=True)
    check(f"{os.path.relpath(script, ROOT)} passes the checker", r.returncode == 0, r.stdout.strip().replace("\n", " | "))

for case in glob.glob(os.path.join(ROOT, "projects/*/cases/case-*.md")):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts/check_case.py"), case], capture_output=True, text=True)
    check(f"{os.path.relpath(case, ROOT)} passes the case checker", r.returncode == 0, r.stdout.strip().replace("\n", " | "))
units = glob.glob(os.path.join(ROOT, "learn/units/*/*.md"))
check("at least one unit prepared", bool(units))
for unit in units:
    r = subprocess.run([sys.executable, os.path.join(ROOT, "learn/check_unit.py"), unit], capture_output=True, text=True)
    check(f"{os.path.relpath(unit, ROOT)} passes check_unit", r.returncode == 0, r.stdout.strip().replace("\n", " | "))
check("fact sheet exists", os.path.exists(os.path.join(ROOT, "learn/facts.md")))
r = subprocess.run([sys.executable, os.path.join(ROOT, "learn/selftest.py")], capture_output=True, text=True)
check("checker, guard and engine catch every planted attack (learn/selftest.py)", r.returncode == 0,
      " | ".join(l for l in r.stdout.splitlines() if l.startswith(("FAIL", "SKIP"))) or r.stderr[-300:])
for name in ("faiz-drill", "faiz-hint", "faiz-learn", "faiz-build"):     # only faiz-teach defines teaching
    f = os.path.join(ROOT, f".claude/commands/{name}.md")
    check(f"/{name} is retired, defines no recall or hints", not os.path.exists(f) or "Retired" in open(f).read())
check("devils-advocate agent exists", os.path.exists(os.path.join(ROOT, ".claude/agents/devils-advocate.md")))

quiet = "--quiet" in sys.argv
failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    if ok and quiet:
        continue
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
if quiet and failed:
    print("TEACHING SYSTEM INCOHERENT: fix the FAIL lines above before teaching "
          "(python3 scripts/check_teaching_system.py).")
if not quiet:
    print(f"\n{len(results) - len(failed)} of {len(results)} checks pass.")
sys.exit(1 if failed else 0)
