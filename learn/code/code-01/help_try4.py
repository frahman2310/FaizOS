reply = {
    "content": [{"type": "text", "text": "Mardan"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 7, "output_tokens": 2},
}
print(reply["content"][0])
print(reply["content"][0]["text"])
