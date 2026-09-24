import sys
program = __import__(sys.argv[1] if len(sys.argv) > 1 else "change")   # which file to test

log = []
program.call("summarise this invoice", "haiku", log)
assert log[0]["tokens"] == 1500
assert log[0]["cost"] == 0.0027
print("PASS")
