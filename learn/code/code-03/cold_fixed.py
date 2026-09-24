TESTS = [
    {"q": "2+2", "want": "4", "got": "4"},
    {"q": "3+3", "want": "6", "got": "7"},
    {"q": "5+1", "want": "6", "got": "6"},
]
right = []
for t in TESTS:
    if t["got"] == t["want"]:
        right.append(t)
print("score:", len(right), "of", len(TESTS))
