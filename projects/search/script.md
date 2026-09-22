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
Status: done 2026-09-22

# Lesson 7 · Round 1 · Part C · Measuring whether search finds the right passage

**The problem.** The firm switched to the weighted search, and the engineer says it "feels better". Reading answers cannot check that: when an answer quotes a wrong rate, you cannot tell if search missed the right passage or the AI misread one it was given. The two need different fixes, so the firm needs a number for search alone. A tax partner spends two days writing 200 real client questions and marking, for each, the one passage that holds the answer.

**The fix:** run every test question through search and count how often the marked passage lands in the top 5; that count over the number of questions is called Recall@5.

```python
hits = 0
for q in test_questions:
    top5 = search(q["question"], 5)
    if q["right_passage"] in top5:
        hits = hits + 1
recall_at_5 = hits / len(test_questions)
```

Counted case: the old word-counting search hit on 124 of the 200 questions, so its Recall@5 is 124 / 200 = 62%.

**Picture:** a net that holds 5 fish. Recall@5 is how often the fish you wanted is in it. Where it breaks: some questions need two passages (a rate and its exemption), and only one is marked.

- **Marked passage in the top 5:** a hit, the AI has what it needs.
- **It is 6th:** a miss, same as 500th.
- **Two passages needed, one marked:** a hit, while the AI still lacks half the answer.

**Worked chain** (another case): the engineer writes test questions in the Ordinance's own wording → each shares rare words with its passage → Recall@5 reads high → the firm stops improving search → clients asking in their own words get misses.

**Your turn.**

1. The weighted search puts the marked passage in the top 5 for 158 of the 200 questions. What is its Recall@5?
2. Search X: marked passage in the top 5 for 150 questions, exactly 6th for the other 50. Search Y: top 5 for 150, beyond 100th for the other 50. Give both Recall@5 figures; which is closer to good, and what one cheap change shows it?
3. The partner found each "right passage" by typing the question into the current search and picking from what it returned. Which way does Recall@5 read, which way does the decision to let clients use it bend, and what reaches them?
4. Recall@5 is 79%. Does that show 79% of client answers are correct, or only something weaker? Name two other things a correct answer needs.
5. **Someone broke it.** The scoring loop calls `search(q["question"], 50)`, while the app still sends the AI 5 passages. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 79% [warmup]
2. both 75%; X is closer, sending 6 passages instead of 5 lifts X to 100% and does nothing for Y [pair]
3. reads high (every marked passage is one the search already finds) → bends toward putting it in front of clients → questions the search cannot find fail in front of clients [chain]
4. only that the right passage reached the AI; the AI must read it correctly, and the passage must be current law [prove]
5. quietly wrong (it measures recall at 50 and reports it as recall at 5, so it reads high) [broke]
Relies on: a hit means the marked passage is in the top 5; 6th counts as a miss; a test built with the tool it tests reads high

## R1-D · Rewarding the right passage for ranking high
New: MRR, the average of 1 over the place where the right passage lands
Status: done 2026-09-22 (How it works skipped 4th place; he had to ask)

# Lesson 7 · Round 1 · Part D · Rewarding the right passage for ranking high

**The problem.** Recall@5 counts a hit the same whether the right passage came 1st or 5th. That matters for two reasons at the firm. First, when two passages disagree, the AI tends to lean on the one placed first, so a right passage at 5th loses to an old circular at 1st. Second, finance wants to send 2 passages instead of 5 to cut cost and wait time, and a right passage sitting at 4th or 5th would then be dropped. Two searches can both score 79% Recall@5 while one puts the right passage 1st and the other puts it 5th, and the firm cannot tell them apart.

**The fix:** score each question by 1 divided by the place where the right passage landed (0 if it is not in the top 5), and average over all questions. This is called MRR (mean reciprocal rank: mean is average, reciprocal is 1 over).

```python
total = 0
for q in test_questions:
    rank = place_of(q["right_passage"], search(q["question"], 5))
    if rank > 0:
        total = total + 1 / rank
mrr = total / len(test_questions)
```

**How it works:**
1. `place_of` gives 1 for first place, 2 for second, up to 5, and 0 when the passage is missing.
2. `1 / rank` turns a place into points: 1st is 1, 2nd is 0.5, 3rd 0.33, 5th 0.2. Missing adds nothing.
3. `total / len(...)` averages. Counted case: four questions landing 1st, 2nd, 5th and missing give 1 + 0.5 + 0.2 + 0 = 1.7, over 4 is 0.425.

**Picture:** prize money for a race: $1 for 1st, 50 cents for 2nd, 20 cents for 5th, nothing outside the top 5. MRR is the average prize. Where it breaks: the prize halves from 1st to 2nd, but an AI that reads all 5 passages carefully does almost as well with the answer 2nd.

- **Right passage 1st:** full point, the passage the AI leans on is the right one.
- **Right passage 5th:** a hit for Recall@5 but only 0.2 here, and it is cut if only 2 are sent.
- **Missing:** 0 for both measures.

**Worked chain** (another case): the test set holds only questions with a single matching circular → nothing competes for 1st place → MRR reads high → finance cuts to 2 passages → questions where an old and a new circular both match lose the new one.

**Your turn.**

1. Five questions land 1st, 1st, 3rd, 4th and missing. What is MRR?
2. Search P puts the right passage 5th for all 200 questions. Search Q puts it 1st for 120 and misses the other 80. Give Recall@5 and MRR for each. If the firm sends only the top 1 passage, which search gets more questions right, and how many?
3. For cutting from 5 passages to 2 to lose no hits at all, what would have to be true about where right passages land?
4. The app shuffles each top 5 into random order before the AI sees it, but MRR is measured before the shuffle. Nothing crashes. Is the MRR too high or too low for what the AI actually gets, and who notices first, and how?
5. **Someone broke it.** The points line was typed as `total = total + rank`. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. about 0.52 ((1 + 1 + 0.33 + 0.25 + 0) / 5 = 2.58 / 5) [warmup]
2. P: Recall@5 100%, MRR 0.2; Q: Recall@5 60%, MRR 0.6. With 1 passage, Q gets 120 right and P gets 0 [pair]
3. every right passage lands 1st or 2nd; none at 3rd to 5th [must-be-true]
4. too high (the right passage is no longer reliably first when the AI reads); the tax partner, seeing answers lean on the wrong passage while MRR looks fine [which-way]
5. quietly wrong (worse places add more points, so a worse search scores higher) [broke]
Relies on: 1 over the place; missing adds 0; average is total over count; the AI leans on the first passage

## R1-E · How big each passage should be
New: passage size, how many words each cut-out passage holds
Status: done 2026-09-22

# Lesson 7 · Round 1 · Part E · How big each passage should be

**The problem.** Before search runs, the 6,000 pages are cut into passages, and the size of the cut decides what search can find. A tax answer often spans neighbouring sentences: one says who the rule covers, the next gives the rate. Cut too small and they land in different passages, so the 5 sent can carry one half without the other. Cut too big and each passage holds dozens of topics, so wrong passages share the question's words by accident and push the right one out. On the 200 test questions, 25-word passages scored 58% Recall@5 (116 of 200), 250 words 81% (162), 1,000 words 66% (132).

**The fix:** cut passages big enough to keep a rule and its rate together, and no bigger, and pick the size by measuring Recall@5 at each one.

```
Section 153(1)(b), services. A person not on the Active Taxpayer
List pays withholding at twice the normal rate. The normal rate is 4%.
```

At 1 sentence that is three passages, and the answer (8%) needs two. At 250 words it is one passage. At 1,000 words it shares a passage with 30 other rates.

**Picture:** a newspaper scrapbook. Cut single lines and a headline loses its story; paste whole pages and the story is lost in the crowd. Where it breaks: a reader sees neighbouring clippings; search sees each passage alone.

- **Rule and rate together:** it matches the rare words and carries the answer.
- **Split across two passages:** each matches part of the question; one half can miss the top 5.
- **Buried in a huge passage:** it matches, but so do many wrong ones, and it gets crowded out.

**Worked chain** (another case): test questions all ask about long rate schedules → big passages score best → the firm picks big passages → short everyday questions get crowded out, at a higher bill.

**Your turn.**

1. A page is 500 words and costs $0.003 to send. At 1,000-word passages, what do 5 passages per question cost a week, at 150 questions?
2. 25 words and 1,000 words both lose to 250. Give the reason each loses; they differ.
3. A colleague reasons: 1) bigger passages hold more text; 2) so the right sentence is more likely among the 5 sent; 3) so answers improve. Which step is wrong, and what does the test show?
4. The test questions were all answered by a single sentence. Which way does the 25-word Recall@5 read against real questions, which way does the size decision bend, and what reaches clients?
5. **Someone broke it.** A typo set the passage size to 25,000 words instead of 250. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. $4.50 (150 x 5 x 2 pages x $0.003) [warmup]
2. 25 words: the rule and its rate split into different passages; 1,000 words: wrong passages match by accident and crowd the right one out [pair]
3. step 2: more text means wrong passages match too, so Recall@5 fell from 81% to 66% [wrong-step]
4. reads high (single-sentence answers never split) → bends toward small passages → questions needing a rule and its rate together miss [chain]
5. quietly wrong (it still runs: each passage is 50 pages, recall falls and the bill jumps) [broke]
Relies on: pages x price; a passage matches only the words inside it; more words per passage means more accidental matches

## R2-A · Searching by meaning instead of words
New: an embedding, a list of numbers that places a text on a map of meanings
Status: pending

# Lesson 7 · Round 2 · Part A · Searching by meaning instead of words

**The problem.** The 250-word search still missed 38 of the 200 test questions, and 22 of those 38 were clients using different words from the law. A client writes "I'm not registered with FBR, what gets deducted from my consultancy invoices?", while the law says "a person not on the Active Taxpayer List" and "services". They share no rare word, so every weight from Part B is zero and the right passage never makes the top 5. Real clients rarely use the Ordinance's wording, so the gap grows with every ordinary client.

**The fix:** turn every passage and question into a list of numbers where similar meanings get similar numbers, and rank passages by closeness to the question. That list is called an embedding.

```python
q = embed("not registered with FBR, consultancy invoices")
p = embed("person not on the Active Taxpayer List, services")
print(closeness(q, p))    # 0.91; near 1 means near in meaning
```

**How it works**, with 2 numbers instead of the real 1,024:
1. `embed` places each text on a map: "not registered" lands at [0.9, 0.1], "not on the Active Taxpayer List" at [0.85, 0.2], "sales tax on goods" at [0.1, 0.95].
2. `closeness` multiplies the matching numbers and adds them: 0.9 x 0.85 + 0.1 x 0.2 = 0.785, against 0.9 x 0.1 + 0.1 x 0.95 = 0.185 for sales tax.
3. Highest closeness ranks first, so a passage sharing no words with the question still wins.

**Picture:** a city where shops of one kind cluster on one street; you find tailors by walking to that street, whatever each sign says. Where it breaks: the map is drawn from ordinary text, where "filer" and "non-filer" share sentences, so it parks them together although their rates differ.

- **Other words, same meaning:** close, found.
- **Same topic, opposite rule:** "filer" and "non-filer" sit close, so the wrong rate can rank first.
- **An exact code like 153(1)(b):** the map blurs numbers, so word search finds it better.

**Worked chain** (another case): meaning search is tested only on rate questions → it reads higher than on real questions → the firm leans toward dropping word search → questions citing a section number start missing.

**Your turn.**

1. On the 2-number map a question sits at [0.8, 0.3]; passage A at [0.7, 0.4]; passage B at [0.2, 0.9]. Give both closeness scores. Which ranks first?
2. A client asks "what is the rate under section 153(1)(b)?". Word or meaning search: which likelier puts the right passage first, and why?
3. The meaning search is tested only on questions written in the Ordinance's own words. Does its lead over word search read bigger or smaller than on real client questions, does that push the firm toward adopting it or skipping it, and what reaches clients?
4. For a non-filer's question, meaning search ranks a passage stating the filer rate first, at closeness 0.93. Does 0.93 show that passage answers the question, or only something weaker? Say what.
5. **Someone broke it.** `embed` was upgraded: questions get numbers from the new version, the 12,000 passages still hold the old version's. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. A 0.68, B 0.43; A first [warmup]
2. word search: the section number is an exact rare token, and the meaning map blurs numbers [pair]
3. smaller (on the law's own wording word search already scores well) → toward skipping it → client paraphrases keep missing [chain]
4. only that it is near in topic; filer and non-filer sit close on the map although their rates differ [prove]
5. quietly wrong (the two versions draw different maps, so closeness compares points from two maps) [broke]
Relies on: multiply matching numbers and add; nearest ranks first; word search scores rare exact words; a map drawn from ordinary text
