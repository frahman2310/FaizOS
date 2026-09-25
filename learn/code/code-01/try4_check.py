# Key check for Try with me 4: what each option does
reply = {
    "content": [{"type": "text", "text": "Karachi"}],
    "stop_reason": "max_tokens",
    "usage": {"input_tokens": 20, "output_tokens": 50},
}
options = {
    "A": lambda: reply["text"],
    "B": lambda: reply["content"][0],
    "C": lambda: reply["content"][0]["text"],
    "D": lambda: reply["content"],
}
for name, get in options.items():
    try:
        print(name, "prints", get())
    except KeyError as err:
        print(name, "crashes: KeyError:", err)
