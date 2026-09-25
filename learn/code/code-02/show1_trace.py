# Key check for Show 1: what log holds after each line
log = []
print("after line 1:", log, len(log))
log.append({"amount": 500})
print("after line 2:", log, len(log))
log.append({"amount": 120})
print("after line 3:", log, len(log))
print(len(log))
print(log[1])
