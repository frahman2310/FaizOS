import sys
program = __import__(sys.argv[1] if len(sys.argv) > 1 else "change")   # which file to test

summary = program.report(program.LOG)
assert summary["worked"] == 2
assert summary["retried"] == 1
assert summary["failed"] == 1
print("PASS")
