# Lesson 6 · judge · teaching script
Goal: find what is really failing, then an AI judge you can trust. Skills: error-analysis,
failure-taxonomy, sql-joins-aggregation, sql-window-functions, llm-judge-design, judge-validation,
statistical-gating. Number: failure counts by kind, and the judge's agreement with his own labels.

Carry-over from L5: three adjustments, from docs/learning-evidence.md
- Word every question as a concrete scenario with a one-word or one-number answer. Two L5 questions used abstract nouns ("does the list notice", "how many different setups") and both had to be reworded.
- Ask the Someone broke it question for the label alone unless the value matters; R2-B Q5 asked for both and came back blank.
- Keep every build option a real trade-off (C35) and name in the Key what the winner gives up; L5 D1 and D2 were called out as obvious.
Also: his weakest L5 answers were the baseline moving after a change lands, and least access. Both belong in L6 as one-line reminders inside a part, not as new teaching.

## R1-A · Naming what actually fails
New: a failure kind, a short name you give to one repeated way the AI gets it wrong
Status: done 2026-09-18

# Lesson 6 · Round 1 · Part A · Naming what actually fails

**The problem.** The gate now stops changes that make things worse, but the accounting firm still rings up, so something is wrong with the summaries the gate happily allows. Your app made 4,000 calls last week and you know from the pass rate that about 8% of them are bad, which is roughly 320 ruined summaries, but you have no idea what is wrong with them. So you guess: you reword the instructions to be stricter about totals, the pass rate moves a point, and you cannot tell whether you fixed the real problem or a rare one. Guessing costs a week per attempt, and the firm is counting the weeks.

**The fix:** read a sample of the real failures, give each one a short name for what went wrong, and count how many of each name you see.

```
missing_total       41
wrong_currency      18
truncated_page_2     9
credit_note_positive 6
```

**Picture:** a hospital triage board. You treat what is actually coming through the door in the numbers it arrives in, not the case you personally find interesting.

- **A failure matches a name you already have:** add one to that count.
- **A failure matches no name:** give it a new name.
- **Two people give the same failure different names:** the name is too vague, so split it into ones that can be applied the same way by anyone.

**Your turn.**

1. You read 100 real failures and 41 of them are missing_total. What share of failures is that?
2. About 320 summaries fail each week. If missing_total is 41% of failures, how many of those 320 does fixing it remove?
3. Two names are proposed: "bad output" and "missing_total". Which one can two different people apply the same way?
4. A failure shows a credit note reported as a positive amount, and no existing name fits it. Do you force it into missing_total, or give it a new name?
5. **Someone broke it.** The counts were taken from your own 100 test cases instead of from real failures the firm hit. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 41%
2. about 131
3. missing_total
4. a new name
5. quietly wrong
Relies on: a share is part / whole x 100; 82 of your 100 test cases are invented (L5 decision 2)

## R1-B · Asking a table one question
New: a SQL count, a question that counts the rows of a table matching one condition
Status: done 2026-09-18 (Q1, Q2 were read-backs; led to C36)

# Lesson 6 · Round 1 · Part B · Asking a table one question

**The problem.** Every call your app makes is now written down as one row in a table: which invoice, which day, and the failure name you gave it (or none if it worked). After a month that table has 16,000 rows, and every Monday the firm asks how many summaries lost their total last week. Scrolling a spreadsheet takes an hour and you miscount, and next Monday you do it again from scratch. You want to ask the table the question once, in words it understands, and get the number back in a second every week.

**The fix:** write the question in SQL (a language nearly every database understands for asking questions of tables) and let the database count.

```sql
SELECT COUNT(*) FROM calls
WHERE failure = 'missing_total';
```

Read it as: count the rows (`SELECT COUNT(*)`) in the table called calls (`FROM calls`), keeping only the rows whose failure column holds exactly that text (`WHERE ...`). In SQL a single `=` asks "is equal", unlike Python where it moves a sticker, and text goes in single quotes.

**Picture:** a spreadsheet filter. Filter one column down to one value and read the row count at the bottom of the screen.

- **A row's failure is exactly 'missing_total':** it is counted.
- **Any other row:** it is skipped.
- **The WHERE line is removed:** every row in the table is counted.

**Your turn.**

1. The table has 4,000 rows and 131 of them have failure 'missing_total'. What number does the query return?
2. Same table, WHERE line deleted. What number comes back?
3. 131 out of 4,000 calls: what percentage is that?
4. Someone writes `WHERE failure = missing_total` with no quotes. Does SQL read missing_total as text, or go looking for a column with that name?
5. **Someone broke it.** The query says `WHERE failure = 'Missing_Total'`, but the table stores the name in lowercase, and the query returns 0. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 131
2. 4,000
3. about 3.3%
4. a column
5. quietly wrong
Relies on: quotes mean the text itself (bootcamp round 3); capitals count; a share is part / whole x 100

## R1-C · Every count in one question
New: GROUP BY, sorting rows into piles by one column with a count per pile
Status: pending

# Lesson 6 · Round 1 · Part C · Every count in one question

**The problem.** The firm's Monday question grew: they now want the count for every failure name, not just missing_total. You write one query per name, twelve in all, and run them one by one. On Thursday a new kind of failure appears, dates read in the wrong order, and you name it date_wrong, but none of your twelve queries ask about it, so it never shows up in Monday's report while it quietly spreads. A report built from a fixed list of names can only ever find the failures you already knew about.

**The fix:** ask for all the counts at once, letting the database sort the rows into piles by failure name and count each pile, which is what GROUP BY does.

```sql
SELECT failure, COUNT(*) FROM failures
GROUP BY failure;
```

It returns one line per name that exists in the table right now, with its count beside it.

**Picture:** a heap of shop receipts. You sort them into piles by shop name, then count each pile. A receipt from a shop you have never heard of simply starts a new pile.

- **Rows share a failure name:** they land in one pile and get one count.
- **A name appears for the first time:** it gets its own line without anyone writing a new query.
- **The GROUP BY line is removed:** all rows form one pile, so you get one number for the whole table.

**Your turn.**

1. On Thursday date_wrong appears 7 times. Does it show up in your old twelve queries? Does it show up in the GROUP BY query?
2. The failures table holds five rows: missing_total, wrong_currency, missing_total, missing_total, wrong_currency. Write down exactly what the GROUP BY query returns.
3. About 320 summaries fail a week, and the counts say missing_total is the biggest pile at 131. You can afford one fix this month. After fixing missing_total, roughly how many failures a week remain?
4. You delete the GROUP BY line but keep `SELECT failure, COUNT(*)`. How many lines of output come back?
5. **Someone broke it.** The query was changed to `GROUP BY invoice`, and almost every line shows a count of 1. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. no; yes
2. missing_total 3, wrong_currency 2
3. about 189
4. one
5. quietly wrong
Relies on: GROUP BY makes one pile per distinct value; a count without GROUP BY is one pile; remaining = before minus the fixed pile
