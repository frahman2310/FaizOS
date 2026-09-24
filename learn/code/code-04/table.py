# The Trace Key's memory table: trace.py's report() with a print after every marked line that runs.
from trace import LOG

def report(log):
    oks = []
    print("after (a): row -  oks", oks)
    for row in log:
        if row["ok"]:
            oks.append(row)
            print("after (b): row", row, " oks", oks)
    retried = 0
    print("after (c): row", row, " oks", oks, " retried", retried)
    for row in oks:
        if row["tries"] > 1:
            retried = retried + 1
            print("after (d): row", row, " oks", oks, " retried", retried)
    return {"worked": len(oks), "retried": retried}

print(report(LOG))
