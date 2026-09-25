def fake_model(prompt):
    return {"text": "Pay by card", "input_tokens": 7, "output_tokens": 4}

answer = fake_model("How do I pay?")
n = answer["input_tokens"]
print(n)
