import sys
program = __import__(sys.argv[1] if len(sys.argv) > 1 else "change")   # which file to test

summary = program.report(program.LOG)
assert summary["succeeded"] == 3
assert summary["retried"] == 2
assert summary["cost per success"] == 0.0027
print("PASS")
