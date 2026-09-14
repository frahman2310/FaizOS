#!/usr/bin/env python3
"""SessionStart backstop: report teaching exchanges that faiz-reflect has not learned from yet."""
import glob
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_teaching import exchanges, load_state

DIR = "/Users/faizr/.claude/projects/-Users-faizr-AI-OS-for-Learning"
state = load_state()
pending = []
for path in glob.glob(os.path.join(DIR, "*.jsonl")):
    if time.time() - os.path.getmtime(path) > 30 * 86400:
        continue
    n = len(exchanges(path))
    done = state.get(os.path.basename(path), 0)
    if n > done:
        pending.append((path, n - done))
for path, n in pending:
    print(f"UNREFLECTED TEACHING: {n} question/answer exchanges in {path}. Before teaching, run the "
          f"faiz-reflect skill on that transcript so the method learns from them.")
