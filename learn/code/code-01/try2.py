def fake_model(prompt):
    return {"text": "Your invoice is due Friday", "input_tokens": 9, "output_tokens": 6}

reply = fake_model("When is my invoice due?")
used = reply["output_tokens"]
print(used)
