# Lesson 7 · search · teaching script
Goal: retrieval from scratch, then vectors. Skills: retrieval-metrics, retrieval-decision,
chunking-strategies, contextual-retrieval, pgvector-limits. Number: Recall@5, MRR, recall vs chunk size.

Carry-over from L6: four adjustments, from docs/learning-evidence.md
- Before any question asking which way a wrong number bends a decision (or what a number proves), show one worked chain of the same kind on other numbers in the part. L6 Round 2 went 0/3 first try on exactly these (E12).
- Build: write and run the model first and take every given from its output. L6 Decision 4 stated a scan share that clashed with Decision 3 and needed a correction.
- Build: no prediction step; after the last pick, build and run at once ("Idw predict, just build", C37). Show him the combined effect when two picks each add cost; in L6 two individually fine picks broke the budget together.
- First lesson under C38/C39: every part follows the new template (counts for rates, How it works for formulas, Worked chain before direction questions, 3+ bank questions tagged in the Key); every decision has 2+ realistic difficulties and a prediction with all its data.
Also: his weakest L6 answers were complement counts (how many did NOT agree) and GROUP BY one pile vs many. Cohen's kappa was not taught in L6; teach it where agreement between two labellers comes up.

## R1-A · Finding the right pages before the AI answers
New: handing the AI only the few passages most likely to hold the answer (retrieval)
Status: pending

# Lesson 7 · Round 1 · Part A · Finding the right pages before the AI answers

**The problem.** A Karachi tax firm answers about 150 client questions a week, like "what withholding rate applies to a non-filer's services invoice?". The answers sit in about 6,000 pages of FBR circulars and the Income Tax Ordinance. Today the AI answers from what it learned two years ago, and the 2025 Finance Act changed several rates since, so about 30 of 150 weekly answers (1 in 5) quote an old rate. It cannot be sent all 6,000 pages: one call takes at most about 300, and each page costs $0.003 to send. A wrong rate means the client deducts too little tax, and the firm pays the penalty to keep them.

**The fix:** before the AI answers, search the pages for the 5 passages most likely to hold the answer and send only those, with the rule "answer only from these". This is called retrieval.

```python
def answer(question):
    passages = search(question, 5)
    ask = f"Answer only from these passages:\n{passages}\nQuestion: {question}"
    return call_ai(ask)
```

**Picture:** a clerk who pulls 5 pages from the archive for the partner, not the whole archive. Where it breaks: a clerk understands the question; this search only matches words (Part B).

- **The right passage is among the 5:** the AI quotes the current rule.
- **It is not:** the AI works from wrong passages and a confident wrong rate goes out.
- **An old and a new circular both match:** both go, and the AI can quote the old one.

**Worked chain** (another case): search is tested only on questions answered by one short circular → those are easy to find, so the hit rate reads high → the firm lets the AI answer clients → answers spread across the long Ordinance fail in front of clients.

**Your turn.**

1. Five passages of half a page each go with every question. What does sending them cost per week, at 150 questions?
2. 140 of 150 answers now quote a rate found in the passages sent. Does that show 140 are right, or only something weaker? What one check would show right?
3. A spot check uses 50 questions, all on rules unchanged since 2023. Which way does its accuracy read against real questions, which way does the decision to let the AI answer clients bend, and what reaches clients?
4. Setup costs $400 once, plus question 1's weekly cost. Each old-rate answer costs the firm $90. How many must it prevent a week to pay back in 4 weeks?
5. **Someone broke it.** The loader that files pages for search skipped the 2025 Finance Act folder. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. $1.13 (150 x 2.5 pages x $0.003) [warmup]
2. only that the answers came from the passages; a person checking a sample of rates against the current law [prove]
3. reads high → bends toward letting it answer → old rates on the changed rules reach clients [chain]
4. at least 1.2 a week, so 2 (400 + 4 x 1.13 = 404.52; 404.52 / 4 / 90 = 1.12) [flip]
5. quietly wrong (search still returns 5 passages, all from before the 2025 changes) [broke]
Relies on: cost = pages x price; the AI answers from what it is sent; a test on easy cases reads high
