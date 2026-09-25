reply = {
    "content": [{"type": "text", "text": "Islamabad"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 14, "output_tokens": 4},
}
print(reply["usage"])
print(reply["usage"]["output_tokens"])
print(reply["content"][0]["text"])
