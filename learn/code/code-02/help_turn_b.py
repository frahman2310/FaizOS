def fake_model(prompt):
    return {"text": "Checked", "usage": {"input_tokens": 5, "output_tokens": 1}}

def check(invoice, book):
    reply = fake_model(invoice)
    record = {"invoice": invoice, "tokens_out": reply["usage"]["output_tokens"]}
    book.append(record)
    return reply  # aim: hand back the text of the reply

book = []
one = check("INV-1", book)
print(book)
two = check("INV-2", book)
print(two)
print(len(book))
print(book[0]["invoice"])
