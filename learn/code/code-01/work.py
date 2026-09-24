# Hand checks for the Keys: the arithmetic behind cost_of, both the right way and with the slots swapped.
print("one million:", 1_000_000)
print("right way:", 1200 * 1 + 300 * 5, "then", (1200 * 1 + 300 * 5) / 1_000_000)
print("swapped:", 300 * 1 + 1200 * 5, "then", (300 * 1 + 1200 * 5) / 1_000_000)
