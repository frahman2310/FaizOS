def fake_model(prompt):
    return {"text": "Sent", "usage": {"input_tokens": 7, "output_tokens": 2}}

def remind(name, book):
    reply = fake_model(name)
    record = {"name": name, "tokens_out": reply["usage"]["output_tokens"]}
    book.append(record)
    return reply["text"]

book = []
print(remind("Ali", book))
print(book)
