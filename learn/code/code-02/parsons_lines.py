# The Change step's shuffled lines, exactly as shown to him (data, not a program to run as-is).
LINES = """
        tries = tries + 1                        # A
    return None, tries                           # B
        try:                                     # C
    tries = 0                                    # D
            time.sleep(pause)                    # E
        tries = 0                                # F
            return fake_provider(prompt), tries  # G
    for pause in PAUSES:                         # H
        except RuntimeError:                     # I
"""
print(LINES)
