# The Trace Key's memory table: trace.py's call() with a print after every marked line.
import time
from trace import fake_provider, cost_of, RATES

def call(prompt, model, log):
    start = time.time()
    print("(a)", prompt, model, "start=T", log)
    answer = fake_provider(prompt)
    print("(b)", prompt, model, "start=T", answer, log)
    ms = round((time.time() - start) * 1000, -2)
    print("(c)", prompt, model, "start=T", answer, ms, log)
    print("inside cost_of, rate =", RATES[model])
    cost = cost_of(model, answer["tokens_in"], answer["tokens_out"])
    print("(d)", prompt, model, "start=T", answer, ms, cost, log)
    log.append({"model": model, "ms": ms, "cost": cost})
    print("(e)", prompt, model, "start=T", answer, ms, cost, log)
    return answer["text"]

log = []
text = call("hi", "haiku", log)
print("text =", text)
