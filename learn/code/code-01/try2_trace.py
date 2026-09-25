# Key check for Try with me 2
def fake_model(prompt):
    return {"text": "Your invoice is due Friday", "input_tokens": 9, "output_tokens": 6}

reply = fake_model("When is my invoice due?")
print("after reply = ..., reply holds:", reply)
used = reply["output_tokens"]
print("after used = ..., used holds:", used)
print(used)
