reply = {
    "content": [{"type": "text", "text": "Karachi"}],
    "stop_reason": "max_tokens",
    "usage": {"input_tokens": 20, "output_tokens": 50},
}
print(reply["stop_reason"])
