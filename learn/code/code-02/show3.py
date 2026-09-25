def fake_model(prompt):
    return {"text": "Done", "usage": {"input_tokens": 6, "output_tokens": 4}}

def ask(prompt, log):
    reply = fake_model(prompt)
    record = {"prompt": prompt, "tokens_out": reply["usage"]["output_tokens"]}
    log.append(record)
    return reply["text"]

log = []
first = ask("pay rent", log)
second = ask("pay school fees", log)
print(second)
print(log)
