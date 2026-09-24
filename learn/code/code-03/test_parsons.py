import sys
program = __import__(sys.argv[1] if len(sys.argv) > 1 else "parsons")   # which file to test

assert program.spend(program.log) == 0.0054
assert program.spend([]) == 0.0
print("PASS")
