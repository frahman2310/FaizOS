def fake_model(prompt):
    return {"text": "Booked", "usage": {"input_tokens": 8, "output_tokens": 3}}

def note(question, log):
    reply = fake_model(question)
    record = {"question": question, "tokens_in": reply["usage"]["input_tokens"]}
    log.append(record)
    return reply["text"]

log = []
print(note("book a table", log))
print(log)
