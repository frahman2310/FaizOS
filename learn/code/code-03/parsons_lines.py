# The Change step's shuffled lines, exactly as shown to him (data, not a program to run as-is).
LINES = """
        total = total + row              # A
    return total                         # B
    for row in log:                      # C
        total = total + row["cost"]      # D
    total = 0.0                          # E
def spend(log):                          # F
"""
print(LINES)
