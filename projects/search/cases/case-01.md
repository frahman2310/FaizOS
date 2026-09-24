# Case 01 · The search that cannot hear clients

**Evidence:** `../lab/out/documents.txt` `../lab/out/baseline_word_250_dev.txt` `../lab/out/baseline_meaning_250_dev.txt` `../lab/questions_README.md`

**Your job.** You are the engineer called in to fix a broken search system. Find out why it fails, change it until it passes two bars set by the firm's managing partner, and then explain in a one-page memo what was wrong and what you did. You do not write code and there is no quiz: you decide what to look at, what to change and what to conclude, and I carry out each instruction and show you exactly what came back.

**The situation.** A Karachi tax firm wants an AI assistant to answer clients' withholding-tax questions from the real FBR documents, instead of from whatever the AI remembers, which may be years out of date. The assistant works in two steps. First, a search step reads the client's question and picks the 5 passages from the FBR documents most likely to contain the answer. Second, the AI writes its reply using only those 5 passages. So if search hands over the wrong passages, the AI answers wrongly however good it is: search is the part that has to work first, and it is the only part in this case.

**The problem.** Search was measured for the first time today on 100 test questions. When a question uses the law's own words ("rate under section 149 for salary"), the right passage is in the top 5 for 79% of questions. When a question is asked the way a client would ask it (these are different questions from the law-worded ones, on a different mix of items: "I earn about 18 lakh from my job, how much tax is cut?"), the right passage is in the top 5 for only 19%. Real clients almost never use the law's words. On top of that, for 7 of the 100 questions search put a passage from the outdated 2023 rate card first, which would hand the AI a rate that is no longer the law.

**The bar.** The partner will let clients use the assistant only when both hold:
1. given: at least 80% of client-worded questions have the right passage in the top 5 (today: 19%).
2. given: no question has a passage from the 2023 rate card in first place (today: 7 of 100 do), because a client acting on a 2023 rate pays the wrong tax.

**What you have.**
- **The documents**, real and unedited, as FBR published them:
  - the Income Tax Ordinance 2001, amended to 31.07.2025 (804 pages): the law itself
  - the Withholding Tax Rate Card updated to 30 June 2025 (14 pages): FBR's summary table of current rates
  - FBR Circular 01 of 2025-26 (12 pages): FBR's explanation of what the Finance Act 2025 changed; it is a scan, so it has typing errors
  - the old 2023 rate card (20 pages): outdated, left in because real archives always hold old versions
- **150 test questions**, each with the passage that answers it marked by two or three exact phrases that passage must contain, so the lab can tell automatically whether search found it. 90 are worded like a client and 60 like the law; 36 have answers that changed since 2023.
  - 100 are for development: use them as often as you like while you investigate.
  - 50 are held back for one final exam at the end. Using them early would let you tune the system to the exam, and its score would then read high, the same trap as L6's best-of-five.
- **Two search methods** you already know:
  - word search: the Part B rarity weights, refined so a word repeated in a passage counts a little more and long passages are marked down
  - meaning search: the Part A map, using a free model that turns each text into 384 numbers
- **Today's full measurement** on the 100 development questions, with the documents cut into passages of 250 words (1,314 passages in all):

```
                    word search            meaning search
                    Recall@5  MRR  2023#1   Recall@5  MRR  2023#1
all questions       45%       0.28   7      34%       0.19   5
worded like law     79%       0.53   5      56%       0.34   3
worded like client  19%       0.08   2      18%       0.09   2
changed since 2023  35%       0.24   0      26%       0.15   2
```

Recall@5: share of questions whose right passage is in the top 5. MRR: the Part D score for how high it ranks. 2023#1: questions whose first passage came from the 2023 card.

**How you work.** Each message you send is one move: something you want to see, check or change, in plain words. For example: "show me 5 client questions it missed and what it found instead", "ask the search this question and show me the top 5", "how many passages come from each document?", "run it with 100-word passages", "remove the 2023 card and measure again". Those show how to steer the lab; they are not hints. I run your move and paste what came back. You read it, decide what it tells you, and choose the next move. When a move tests an idea of yours, say the number you expect before I run it, so you can see how often your reasoning holds.

**What the lab can do.**
- **Ask:** run any question and show the top 5 passages, with document, page and score.
- **Measure:** score any setup on the 100 development questions: either method, any passage size, any overlap between passages.
- **Query:** answer anything about past runs in SQL, with the L6 tools (WHERE, GROUP BY, JOIN). The main table, `results`, has one row per question per run: where the right passage landed (0 for missed) and the document and year of the top passage. The others are `questions`, `passages` and `runs`.
- **Read:** show any passage, page or test question in full.
- **Change:** build anything you describe in words: drop or add a document, cut passages differently, label them, combine the methods, fix a test question. I tell you in two lines what changed, then measure it. Ask to see the code and you get the lines that matter, with notes.
- **Explain:** anything you ask about, at the depth you ask. I will not explain unasked or suggest what to try. The one exception is that I will stop you before an irreversible step, such as using the 50 held-back questions before you declare you are done.

**How it ends.**
1. You declare a setup ready.
2. It runs once on the 50 held-back questions, and must clear both bars there.
3. You write a one-page memo to the partner in your own words: what was wrong, what you changed, the numbers, and what could still go wrong.
4. An adversarial reviewer attacks the memo, and you answer its attacks before the partner sees it.

**Your move.**

## Log

| # | His move | His expectation | What came back | Verdict |
|---|---|---|---|---|
| 1a | Use word search; remove the 2023 card | 2023 card first: 0 | 2023 card first: 0 of 100. Client Recall@5 19% → 21%, law 79% → 81% (run 3) | confirmed |
| 1b | Plus: a layer rewrites client questions into law wording (small AI, saw only the question) | client Recall@5 about 79% | client Recall@5 33%, MRR 0.25; law unchanged at 81% (run 4) | refuted |
| 2 | Challenged the result: rewording should have moved the number | (none) | Lab checked: rewrite applied; client questions 9 miss→hit, 2 hit→miss, 10 hit both, 36 miss both. My brief called the law and client sets "the same kind of question": they are different questions, so 79% was never a guaranteed target | look (caught a misleading line in my brief) |
| 3 | Show the client questions that miss (current setup, run 4) | (none) | 38 of 57 listed: the document holding the answer vs the top passage search returned | look |
| 4 | Show all rate card passages | (none) | 23 passages of 250 words (I had said 19: wrong count, corrected) | look |
| 5 | Said the exercise felt unstructured and pointless | (none) | Case restructured into 6 fixed stages (C42); Stage 1 evidence laid out: 5 misses side by side (out/stage1_evidence.json) | look |
