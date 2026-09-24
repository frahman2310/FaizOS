# Prints what spend holds after each pass of the third loop in trace.py (for the Key's table).
from trace import LOG
spend = 0.0
for row in LOG:
    spend = spend + row["cost"]
    print(spend)
