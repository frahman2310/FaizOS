BACKOFF = [0.5, 1.0, 0.0]      # one wait per try, so three tries

for wait in BACKOFF:
    attempts = 0
    attempts = attempts + 1

print(attempts)
