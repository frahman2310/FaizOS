# The Trace Key's memory table: trace.py's fetch() with a print after every marked line.
import time
import trace
from trace import PAUSES

def show(where, **v):
    print(where, v)

def fetch(prompt, records):
    trace.outcomes[:] = ["timeout", "ok", "ok"]
    tries = 0
    reason = ""
    text = "-"
    for pause in PAUSES:
        tries = tries + 1
        show("after (a)", pause=pause, tries=tries, outcomes=trace.outcomes, reason=reason, text=text, records=records)
        try:
            text = trace.fake_provider(prompt)
            show("after (b)", pause=pause, tries=tries, outcomes=trace.outcomes, reason=reason, text=text, records=records)
            records.append({"done": True, "tries": tries})
            show("after (c)", pause=pause, tries=tries, outcomes=trace.outcomes, reason=reason, text=text, records=records)
            return text
        except RuntimeError as err:
            reason = str(err)
            show("after (d)", pause=pause, tries=tries, outcomes=trace.outcomes, reason=reason, text=text, records=records)
            print("err is", repr(err), "and its kind is", type(err).__name__)
            time.sleep(pause)

fetch("USD to PKR", [])
