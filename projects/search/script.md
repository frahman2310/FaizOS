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
Status: done 2026-09-22

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

## R1-B · Scoring a passage by the words it shares
New: scoring passages by shared words, rare words counting more
Status: done 2026-09-22

# Lesson 7 · Round 1 · Part B · Scoring a passage by the words it shares

**The problem.** The firm's 6,000 pages are cut into 12,000 passages of about half a page, and search must pick 5 of them for each client question. The first search counted how many of the question's words each passage contained. For "withholding rate for non-filer services", the winner was a sales tax passage that said "rate" and "services" (2 words), level with the right income tax passage that said "rate" and "non-filer" (2 words), and the sales tax one came first. "Rate" sits in 6,000 of the 12,000 passages, so matching it tells you almost nothing, while "non-filer" sits in only 120, so matching it nearly pins the answer down. Counting every word as 1 treats the useless clue and the decisive one the same, and about 1 in 4 questions got the wrong top passage.

**The fix:** give each shared word a weight that grows with how rare the word is across all passages, and rank passages by the total.

```python
from math import log10
N = 12000
def score(question_words, passage_words, found_in):
    total = 0
    for w in question_words:
        if w in passage_words:
            total = total + log10(N / found_in[w])
    return total
```

**How it works**, for one word:
1. `found_in[w]` is how many of the 12,000 passages contain the word: "rate" 6,000, "services" 1,200, "non-filer" 120.
2. `N / found_in[w]` is how rare it is: 2 for "rate", 10 for "services", 100 for "non-filer".
3. `log10` counts the zeros: log10 of 10 is 1, of 100 is 2, of 2 is about 0.3. So a word 50 times rarer counts about 7 times more, not 50 times, and one rare word cannot drown out the rest.
4. `if w in passage_words` checks the word is there at all; saying "rate" 40 times still earns 0.3 once.

**Picture:** clues in a detective case. "Wore shoes" fits everyone in Karachi; "left-handed, Peshawari accent" fits a handful, so it carries the case. Where it breaks: the detective knows "non-filer" and "not on the active taxpayer list" mean the same person; this score does not.

- **The passage holds the rare words:** its total is high and it makes the top 5.
- **It holds only common words, many times:** each counts once, at a small weight, so it sinks.
- **It says the same thing in other words:** that word scores 0, and the right passage can miss the top 5.

**Your turn.**

1. A passage contains "rate" and "non-filer"; another contains "rate" and "services". Score both.
2. Search A counts every shared word as 1; search B uses the weights above. For the two passages in question 1, which comes first in A, which in B, and which one holds the answer?
3. "Withholding" appears in some number of the 12,000 passages. Above how many passages does it count for less than "services" does?
4. The firm loads 12,000 more passages of 2019 circulars, every one mentioning "non-filer". Nothing crashes. Does the weight of "non-filer" go up or down, and who is first to notice the damage, and how?
5. **Someone broke it.** The weight line was typed as `log10(found_in[w] / N)`. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 2.3 and 1.3 [warmup]
2. A: a tie, order decided by chance; B: the non-filer passage first, and it holds the answer [pair]
3. more than 1,200 passages (log10(12,000 / 1,200) = 1) [flip]
4. down, from 2 to about 0.3 (24,000 / 12,120 is about 2); the tax partner, when non-filer answers start quoting 2019 circulars [which-way]
5. quietly wrong (every weight turns negative, so the rarest words push a passage down hardest) [broke]
Relies on: log10 of 10 is 1, of 100 is 2, of 2 is about 0.3; a word counts once; rarer means fewer passages contain it

## R1-C · Measuring whether search finds the right passage
New: Recall@5, the share of test questions whose right passage lands in the top 5
Status: pending

# Lesson 7 · Round 1 · Part C · Measuring whether search finds the right passage

**The problem.** The firm switched to the weighted search from Part B, and the engineer says it "feels better". Nobody can check that by reading answers: when an answer quotes a wrong rate, you cannot tell whether search failed to fetch the right passage or the AI misread a passage it was given. The two failures need different fixes, one in search and one in the instructions, so the firm needs a number for search alone. A tax partner spends two days writing 200 real client questions and, for each, marks the one passage that holds the answer. Search is then scored on how often that marked passage makes the 5 sent to the AI.

**The fix:** run every test question through search and count how many times the marked passage lands in the top 5; that count over the number of questions is called Recall@5.

```python
hits = 0
for q in test_questions:
    top5 = search(q["question"], 5)
    if q["right_passage"] in top5:
        hits = hits + 1
recall_at_5 = hits / len(test_questions)
```

Counted case: the old word-counting search put the marked passage in the top 5 for 124 of the 200 questions, so its Recall@5 is 124 / 200 = 62%.

**Picture:** a fishing net that can hold 5 fish. Recall@5 is how often the one fish you wanted is in the net. Where it breaks: some questions need two passages (a rate and its exemption), and the partner marked only one.

- **The marked passage is in the top 5:** a hit, the AI has what it needs.
- **It is 6th:** a miss, counted exactly the same as if it were 500th.
- **The question needs two passages and one is marked:** it can count as a hit while the AI still lacks half the answer.

**Worked chain** (another case): the engineer writes the test questions using the Ordinance's own wording → every question shares rare words with its passage → Recall@5 reads high → the firm stops improving search → clients who ask in their own words ("filer status") get misses.

**Your turn.**

1. The weighted search puts the marked passage in the top 5 for 158 of the 200 questions. What is its Recall@5?
2. Search X: the marked passage is in the top 5 for 150 questions and exactly 6th for the other 50. Search Y: top 5 for 150, and beyond 100th for the other 50. Give both Recall@5 figures, and say which one is closer to good, and what one cheap change shows it.
3. The partner found each "right passage" by typing the question into the current search and picking from its results. Which way does Recall@5 read, which way does the decision to ship bend, and what reaches clients?
4. Recall@5 is 79%. Does that show 79% of client answers are correct, or only something weaker? Name the two other things that must hold for an answer to be correct.
5. **Someone broke it.** The scoring loop calls `search(q["question"], 50)`, while the app still sends the AI 5 passages. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 79% [warmup]
2. both 75%; X is closer, sending 6 passages instead of 5 lifts X to 100% and does nothing for Y [pair]
3. reads high (every marked passage is one the search already finds) → bends toward putting it in front of clients → questions the search cannot find fail in front of clients [chain]
4. only that the right passage reached the AI; the AI must read it correctly, and the passage must be current law [prove]
5. quietly wrong (it measures recall at 50 and reports it as recall at 5, so it reads high) [broke]
Relies on: a hit means the marked passage is in the top 5; 6th counts as a miss; a test built with the tool it tests reads high
