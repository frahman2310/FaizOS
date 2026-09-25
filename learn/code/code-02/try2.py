reply = {"text": "Due Friday", "usage": {"input_tokens": 15, "output_tokens": 3}}
record = {"text": reply["text"], "tokens_in": reply["usage"]["input_tokens"]}
log = []
log.append(record)
print(log[0]["tokens_in"])
