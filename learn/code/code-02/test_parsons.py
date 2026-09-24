import sys
program = __import__(sys.argv[1] if len(sys.argv) > 1 else "parsons")   # which file to test

program.script[:] = ["529 overloaded", "529 overloaded", "ok"]    # reset the fake provider
assert program.call("hi") == ("reply to: hi", 3)
print("PASS")
