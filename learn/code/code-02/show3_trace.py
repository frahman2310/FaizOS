# Key check for Show 3: log and the names after each call
def fake_model(prompt):
    return {"text": "Done", "usage": {"input_tokens": 6, "output_tokens": 4}}

def ask(prompt, log):
    reply = fake_model(prompt)
    record = {"prompt": prompt, "tokens_out": reply["usage"]["output_tokens"]}
    log.append(record)
    return reply["text"]

log = []
first = ask("pay rent", log)
print("after first call: first =", first, "| records in log:", len(log))
second = ask("pay school fees", log)
print("after second call: second =", second, "| records in log:", len(log))
