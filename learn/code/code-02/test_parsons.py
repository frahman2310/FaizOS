import sys
program = __import__(sys.argv[1] if len(sys.argv) > 1 else "parsons")   # which file to test

program.outcomes[:] = ["timeout", "ok", "ok"]       # reset the fake provider
assert program.fetch("hi") == ("rate: hi", 2)
print("PASS")
