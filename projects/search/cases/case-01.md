# Case 01 · The search that cannot hear clients

**Evidence:** `../lab/out/documents.txt` `../lab/out/baseline_word_250_dev.txt` `../lab/out/baseline_meaning_250_dev.txt` `../lab/questions_README.md`

**The situation.** A Karachi tax firm wants its AI assistant to answer withholding-tax questions from clients, using the real FBR documents instead of what the AI remembers. Before the AI writes anything, a search step must pick the 5 passages most likely to hold the answer, because the AI can only answer from what it is handed. The managing partner will switch the assistant on for clients only when search can prove itself: given: at least 80% of client-worded questions must have the right passage in the top 5, and given: no question may get the outdated 2023 rate card as its top passage, because a client acting on a 2023 rate pays the wrong tax. The system was built this week and measured for the first time today. It is nowhere near that bar, and nobody yet knows why.

**What you have.**
- **The documents**, real and unedited, as FBR published them: the Income Tax Ordinance 2001 amended to 31.07.2025 (804 pages), the Withholding Tax Rate Card updated to 30 June 2025 (14 pages), FBR Circular 01 of 2025-26 explaining the Finance Act 2025 (12 pages, scanned, so it has typing errors), and the old 2023 rate card (20 pages), left in because real archives always hold old versions.
- **150 test questions**, each with the passage that answers it marked by two or three exact phrases that passage must contain. 90 are worded like a client ("I earn about 18 lakh from my job"), 60 like the law ("rate under section 149 for salary"). 36 have answers that changed since 2023. They are split: 100 for development, which you can use as often as you like, and 50 held back for one final exam. Touching the 50 early would let you tune the system to the exam, and its score would then read high, the same trap as L6's best-of-five.
- **Two search methods**: word search (the Part B rarity weights, refined: a word repeated in a passage counts a little more, and long passages are marked down) and meaning search (the Part A map, using a free model with 384 numbers per text).
- **Today's measurement** on the 100 development questions, passages cut at 250 words (1,314 passages in all):

```
                    word search            meaning search
                    Recall@5  MRR  2023#1   Recall@5  MRR  2023#1
all questions       45%       0.28   7      34%       0.19   5
worded like law     79%       0.53   5      56%       0.34   3
worded like client  19%       0.08   2      18%       0.09   2
changed since 2023  35%       0.24   0      26%       0.15   2
```

"2023#1" counts questions whose top passage came from the old 2023 card.

**What the lab can do.** You direct it; I operate it and report exactly what came back.
- **Ask** any question and see the top 5 passages, with document, page and score.
- **Measure** any setup on the development questions: word or meaning search, any passage size, any overlap between passages.
- **Query** every run in SQL: tables `results` (one row per question per run: the place the right passage landed, 0 for missed, and the top passage's document and year), `questions`, `passages`, `runs`. Everything from L6 works here: WHERE, GROUP BY, JOIN.
- **Read** any passage, page or test question in full.
- **Change** anything you describe in words: drop or add a document, cut passages differently, label them, combine methods, fix a test question. I build it, tell you in two lines what changed, and measure it. Ask to see the code and you get the lines that matter, with notes.
- **Explain** anything, when you ask and at the depth you ask. I will not explain unasked, and I will not suggest what to try. The one exception is that I will stop you before an irreversible step, such as using the 50 held-back questions before you are done.

**Done means.** A setup that clears both of the partner's bars on the 50 held-back questions, measured once. Then a one-page memo to the partner in your words: what was wrong, what you changed, what the numbers were, and what could still go wrong. An adversarial reviewer will attack the memo before the partner sees it.

**How it runs.** Each move is one message from you: what you want to look at or change, and, when you are testing an idea, what number you expect. I run it and paste what came back. Your expectations and what actually happened go into the log below, which is the only score this case keeps.

**Your move.**

## Log

| # | His move | His expectation | What came back | Verdict |
|---|---|---|---|---|
