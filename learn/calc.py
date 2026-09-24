#!/usr/bin/env python3
"""Compute a number for a unit and save it as a run with the command that made it (no number from memory).

    python3 calc.py llm02-cost "1000 * 15 / 10" --note "English bill scaled by Urdu/English token ratio"
"""
import argparse
import datetime
import json
import shlex
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("name"); ap.add_argument("expression"); ap.add_argument("--note", default="")
a = ap.parse_args()
value = eval(a.expression, {"__builtins__": {}}, {"round": round, "min": min, "max": max, "sum": sum})
out = {"kind": "calc", "command": "python3 calc.py " + shlex.join(sys.argv[1:]), "expression": a.expression,
       "value": value, "note": a.note, "made": datetime.datetime.now().isoformat(timespec="seconds")}
path = Path(__file__).parent / "runs" / f"{a.name}.json"
path.write_text(json.dumps(out, indent=1))
print(value, f"(saved {path.name})")
