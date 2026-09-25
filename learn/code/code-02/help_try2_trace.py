# Key check for Help: Try with me 2
reply = {"text": "Refund sent", "usage": {"input_tokens": 13, "output_tokens": 4}}
record = {"text": reply["text"], "tokens_out": reply["usage"]["output_tokens"]}
print("after line 2, record:", record)
done = []
done.append(record)
print("after line 4, done:", done)
print(done[0]["text"])
