reply = {"text": "Refund sent", "usage": {"input_tokens": 13, "output_tokens": 4}}
record = {"text": reply["text"], "tokens_out": reply["usage"]["output_tokens"]}
done = []
done.append(record)
print(done[0]["text"])
