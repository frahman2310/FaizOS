def fake_model(prompt):
    return {"text": "Hello, Faiz", "input_tokens": 5, "output_tokens": 3}

reply = fake_model("Say hello")
print(reply["text"])
