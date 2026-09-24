import time

RATES = {"haiku": {"in": 1.00, "out": 5.00}}   # dollars per million tokens

def fake_provider(prompt):
    time.sleep(0.3)                             # pretend the AI takes 0.3 seconds
    return {"text": "reply to: " + prompt, "tokens_in": 1200, "tokens_out": 300}

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

def call(prompt, model, log):
    start = time.time()
    answer = fake_provider(prompt)
    ms = round((time.time() - start) * 1000, -2)
    cost = cost_of(model, answer["tokens_out"], answer["tokens_in"])
    log.append({"model": model, "ms": ms, "cost": cost})
    return answer["text"]

log = []
text = call("summarise this invoice", "haiku", log)
print(text)
print(log)
