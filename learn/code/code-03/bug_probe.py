# The check most likely to be asked for: both sides of the check, for the first case.
from bug import CASES, summarise

case = CASES[0]
note = summarise(case)
print("note =", repr(note))
print("case =", case)
print("labels of case =", list(case))
print('case["must_include"] in note ->', case["must_include"] in note)
print('case["must_include"] in case ->', case["must_include"] in case)
