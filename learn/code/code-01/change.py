import time

RATES = {"haiku": {"in": 1.00, "out": 5.00}}   # dollars per million tokens

def fake_provider(prompt):
    time.sleep(0.3)                             # pretend the AI takes 0.3 seconds
    return {"text": "reply to: " + prompt, "tokens_in": 1200, "tokens_out": 300}

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

def call(prompt, model, log):
    start = time.time()                                                # (a)
    answer = fake_provider(prompt)                                     # (b)
    ms = round((time.time() - start) * 1000, -2)                       # (c)
    cost = cost_of(model, answer["tokens_in"], answer["tokens_out"])   # (d)
    tokens = answer["tokens_in"] + answer["tokens_out"]
    log.append({"model": model, "ms": ms, "cost": cost, "tokens": tokens})
    return answer["text"]                                              # (f)

log = []
text = call("summarise this invoice", "haiku", log)
print(text)
print(log)
