"""Run one unit program and save its exact output as a run file.

    python3 code/record.py code-01 trace.py            -> runs/code-01-trace.json
    python3 code/record.py code-01 test_change.py trace -> runs/code-01-test_change-trace.json
"""
import json
import subprocess
import sys
from pathlib import Path

LEARN = Path(__file__).resolve().parent.parent
unit, program, *args = sys.argv[1:]
done = subprocess.run([sys.executable, program, *args], cwd=LEARN / "code" / unit,
                      capture_output=True, text=True)
name = "-".join([unit, Path(program).stem, *args])
out = LEARN / "runs" / (name + ".json")
out.write_text(json.dumps({"program": f"code/{unit}/{program}", "args": args,
                           "exit_code": done.returncode, "output": done.stdout + done.stderr}, indent=1) + "\n")
print(out.name, "exit", done.returncode)
print(done.stdout + done.stderr)
