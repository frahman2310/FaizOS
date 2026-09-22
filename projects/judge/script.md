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
Status: done 2026-09-18

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

## R1-D · Joining two tables
New: JOIN, lining up rows of two tables by a column they share
Status: done 2026-09-18

# Lesson 6 · Round 1 · Part D · Joining two tables

**The problem.** Your failures table says which invoices failed, but not who sent them or how much money was on them. That information lives in a separate invoices table the firm already keeps. The firm's finance director does not care that 131 summaries lost their total; she cares how much money her staff approved without seeing it, and which supplier keeps causing it. Copying supplier and amount across by hand for 131 rows takes an afternoon and invites mistakes, and it has to be redone every week.

**The fix:** ask the database to line up rows from both tables wherever their invoice number matches, which is what JOIN does, and then read the columns you need from either side.

```sql
SELECT invoices.supplier, invoices.amount
FROM failures
JOIN invoices ON failures.invoice = invoices.invoice
WHERE failures.failure = 'missing_total';
```

`invoices.amount` means the amount column of the invoices table; the name before the dot says which table.

**Picture:** a bank statement laid against a pile of receipts. You pair each line with the receipt carrying the same reference number, and only then can you see what each payment was for.

- **The invoice number is in both tables:** the two rows are joined into one line.
- **It is in failures but missing from invoices:** that failure drops out of the result.
- **The invoices table holds the same number twice:** the failure is joined to both copies and appears twice.

**Your turn.**

1. failures holds INV-7 and INV-9. invoices holds INV-7 (Acme, $500) and INV-8 (Zed, $90). How many lines does the join return, and whose?
2. INV-9 failed but the firm never entered it in invoices. Does it appear anywhere in the result?
3. The joined result says missing_total put $52,000 of payments at risk this week, 60% of it from Acme. The firm can ask one supplier to send typed invoices. Which supplier, and how many dollars of that risk does it cover?
4. The director asks for the money at risk. Can the failures table answer that alone, or do you need the join?
5. **Someone broke it.** Last month's import loaded every invoice into the invoices table twice. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. one line: Acme
2. no
3. Acme, $31,200
4. you need the join (the amount lives in invoices)
5. quietly wrong (every failure is joined twice, so the money at risk doubles)
Relies on: rows join where the shared column matches; unmatched rows drop out; a duplicate matches twice; 60% of 52,000

## R1-E · The latest problem per supplier
New: numbering rows inside each pile without merging them (ROW_NUMBER over a PARTITION)
Status: done

# Lesson 6 · Round 1 · Part E · The latest problem per supplier

**The problem.** Every Friday the finance director rings each supplier whose invoices keep failing, and she wants to quote their most recent bad invoice so the call is specific. GROUP BY supplier gives her a count per supplier, but it squashes each pile into one line, so the actual latest invoice is gone. Sorting all 320 failures by date and hunting down each supplier's newest by eye takes an hour and she has twice quoted the wrong invoice to an angry supplier. She needs each supplier's rows kept whole, numbered newest first, so she can take number 1 from each.

**The fix:** number the rows inside each supplier's pile, newest first, without merging the pile, and keep only the rows numbered 1.

```sql
SELECT supplier, invoice, day,
  ROW_NUMBER() OVER (PARTITION BY supplier ORDER BY day DESC) AS place
FROM failed_invoices;
```

`PARTITION BY supplier` makes one pile per supplier but keeps every row. `ORDER BY day DESC` puts the newest day first. `ROW_NUMBER()` writes 1, 2, 3 down each pile, and `AS place` names that new column.

**Picture:** a race run in separate heats. Every heat has its own winner, and nobody merges the heats to find them.

- **Within a supplier's pile:** the newest failure gets place 1, the next newest place 2.
- **Every row stays:** unlike GROUP BY, nothing is squashed into one line.
- **Keep only place 1:** you get exactly one row per supplier, their latest failure.

**Your turn.**

1. Acme failed on days 3, 9 and 5; Zed failed on days 2 and 8. Which Acme day gets place 1, and which Zed day?
2. Someone removes `DESC`, so each pile is ordered oldest first. Which Acme day gets place 1 now?
3. The director wants each supplier's latest bad invoice. Does GROUP BY supplier give her that, or the numbering query keeping place 1?
4. This week 40 different suppliers had failures, and each call takes the director 6 minutes. How long do her Friday calls take?
5. **Someone broke it.** `PARTITION BY supplier` was deleted, so the whole table is numbered as one pile, and the director keeps place 1. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. Acme day 9, Zed day 8
2. day 3
3. the numbering query keeping place 1
4. 240 minutes, 4 hours (one row per supplier, 40 x 6)
5. quietly wrong (one row comes back, the newest failure overall, so she rings one supplier)
Relies on: GROUP BY squashes a pile into one line; DESC means largest first; place 1 per pile gives one row per pile

## R2-A · A second AI that marks the work
New: an AI that marks each output pass or fail against one written rule (a judge)
Status: done

# Lesson 6 · Round 2 · Part A · A second AI that marks the work

**The problem.** The firm's summariser (the machine that turns a supplier email into a one-line invoice note) sent out 320 notes last week. Round 1 counted failures in SQL, but those counts only exist because a person had already read each note and marked it right or wrong. Reading one note against its email takes about 40 seconds, so marking all 320 is most of an afternoon every week, and nobody has that afternoon. So the team marks 20 and assumes the rest are like them, which means a fault sitting in 5% of notes is usually invisible in the sample. The wrong notes still reach suppliers, and the team believes a pass rate it never measured.

**The fix:** have a second AI read each output against one written rule and answer with a single label, PASS or FAIL. That marker is called a judge.

```python
def judge(email, note):
    ask = ("Does the note state the invoice total from the email? "
           f"Email: {email}\nNote: {note}\n"
           "Answer with one word, PASS or FAIL.")
    return call_ai(ask).strip()
```

The rule is one checkable question, and the reply is one of two words, so the answers can be counted like the hand labels in Round 1.

**Picture:** a marker with a one-line mark scheme going through 320 papers. The scheme decides everything: a vague one gives a different mark each time.

- **Note states the total:** the judge hands back PASS, and the row counts as a pass.
- **Note misses the total:** FAIL, and the row joins the failure counts from Round 1.
- **Judge replies "it depends":** neither label, so the row matches no count and quietly vanishes from the rate.

**Your turn.**

1. Marking all 320 notes by hand takes 40 seconds each. How many minutes of someone's week is that?
2. A fault hits 5% of the notes, and the team hand-marks 20 of the 320. How many bad notes are in the week, and how many does that sample expect to catch?
3. The rule is changed to "Is this note good?". The same note is judged twice and gets two different labels. Which part of the ask caused that?
4. The judge marks 300 notes PASS. Does that prove the summariser is right 94% of the time, or only something weaker? Say what it proves.
5. **Someone broke it.** The judge starts replying `PASS - the total is stated`, and the counting code keeps only replies exactly equal to `PASS`. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. about 213 minutes, three and a half hours
2. 16 bad notes, the sample of 20 expects 1
3. "good" is not checkable, so the AI decides it differently each run
4. only that the judge says so; nothing yet shows the judge agrees with a person
5. quietly wrong (every reply fails the exact match, so the pass rate reads 0%)
Relies on: percent of a number; a judge marks against one written rule; a vague rule gives different answers each run; exact text matching

## R2-B · Checking the judge against a person
New: measuring where a judge disagrees with a person
Status: done

# Lesson 6 · Round 2 · Part B · Checking the judge against a person

**The problem.** The judge from Part A now marks all 320 notes and reports a 94% pass rate, and the team starts making decisions on that number: which supplier to chase, whether last week's change to the summariser helped. But the judge is the same kind of AI that wrote the notes, and nobody has checked whether it marks the way a person would. A soft judge waves bad notes through, so the pass rate reads high while suppliers still get wrong totals. A harsh judge fails good notes, so Fridays go on chasing failures that are not real. Either way the number looks solid and steers the firm wrong.

**The fix:** take a set of notes a person has already marked by hand, run the judge on the same notes, and measure how often the judge agrees, separately for the bad ones and the good ones.

```python
bad   = [h for h in human if h == "FAIL"]
caught = [1 for h, j in zip(human, judge) if h == "FAIL" and j == "FAIL"]
catch_rate = len(caught) / len(bad)
```

The catch rate (also called TPR, the true positive rate) is: of the notes the person marked FAIL, the share the judge also marked FAIL. The clear rate (TNR, the true negative rate) is the mirror: of the notes the person marked PASS, the share the judge also marked PASS.

**Picture:** a smoke alarm. The catch rate is how often it sounds in a real fire; the clear rate is how often it stays quiet while you cook. One number alone tells you nothing about the other.

- **Judge and person both say FAIL:** caught, it counts toward the catch rate.
- **Person says FAIL, judge says PASS:** a miss, a real bad note the judge waves through.
- **Person says PASS, judge says FAIL:** a false alarm, a good note the team wastes Friday on.

**Your turn.**

1. The person marked 20 notes FAIL, and the judge marked 14 of those FAIL. What is the catch rate?
2. The person marked 40 notes PASS, and the judge marked 36 of them PASS. What is the clear rate, and how many good notes get chased for nothing?
3. A lazy judge replies FAIL to everything. What is its catch rate, and what is its clear rate?
4. A judge has a catch rate of 70% and a clear rate of 99%, and the firm uses its fail count to decide whether a change to the summariser is safe to release. Which way does that judge bend the decision, and what reaches the supplier because of it?
5. **Someone broke it.** The human labels are in the order the notes were written, and the judge labels come back sorted by supplier name. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 70%
2. 90%, 4 good notes chased
3. catch rate 100%, clear rate 0%
4. it misses 3 in 10 real failures, so the fail count reads low and a worse summariser looks safe to release; wrong totals keep reaching suppliers
5. quietly wrong (each judge label is compared against another note's human label, so both rates are meaningless)
Relies on: a share is the part over the whole; the two rates are measured on different piles; pairing two lists depends on their order

## R2-C · Telling a real gain from luck
New: how far a measured rate wobbles by luck on a set of that size
Status: done

# Lesson 6 · Round 2 · Part C · Telling a real gain from luck

**The problem.** The team now has a judge it has checked, and it runs on the 60 cases from Lesson 5 before and after every change to the summariser. Last Tuesday the rate read 88%, someone reworded the instructions, and the new run read 92%. That four point rise is written in the release note as proof the change worked, and the reworded version ships. But those 60 cases are a sample, and which cases happen to land on the edge of passing changes run to run, so the rate moves even when nothing at all was changed. On a set of 60 that natural movement is bigger than four points, so the firm keeps shipping changes on the strength of noise and eventually ships one that makes the notes worse.

**The fix:** work out how far the rate moves by luck alone on a set that size, and only believe a change that is bigger than that movement.

```python
from math import sqrt
n, p = 100, 0.50
wobble = 2 * sqrt(p * (1 - p) / n)
print(wobble)   # 0.10, about 10 points
```

The wobble shrinks with the square root of the number of cases, so getting it half as wide takes four times as many cases, not twice as many.

**Picture:** weighing yourself on a bathroom scale that reads a pound either side. A two pound drop tells you nothing; only a swing bigger than the scale's own wobble is real.

- **Rise smaller than the wobble:** you have learned nothing, and the honest release note says undecided.
- **Rise bigger than the wobble:** the change probably did something, and it is worth shipping.
- **Same cases run before and after:** you can instead count only the cases that flipped, which cancels out how hard each case is.

**Your turn.**

1. A set of 100 cases scores 50%. What is the wobble in points, using the line above?
2. On 60 cases the rate goes 88% to 92% after a change. The wobble on that set is about 8 points. What should the release note say?
3. The team wants to detect a 2 point gain, and the wobble on their 60 cases is 8 points. Roughly how many cases do they need to get the wobble under 2 points?
4. A release needs a rise to be reported, so the engineer runs the same 60 cases five times and writes down the best of the five runs. What does that do to the reported rate, and what ships because of it?
5. **Someone broke it.** The before rate is measured on the old 60 cases and the after rate on a new set of 300 different cases. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 10 points
2. undecided, the rise is inside the wobble
3. about 16 times as many, roughly 960 cases
4. best of five picks up the luckiest run, so the reported rate reads high and changes that did nothing keep shipping
5. quietly wrong (the difference mixes the change with how hard the new cases are, so it measures both at once)
Relies on: the wobble shrinks with the square root of the number of cases; a rise inside the wobble proves nothing; a comparison only holds when one thing differs

## BUILD-D1 · Which notes you label by hand
New: none
Status: done 2026-09-22 (picked C)

# Lesson 6 · The build · Decision 1 of 4

**The build.** A judge on this Mac that marks the firm's summaries, checked against your own hand labels. Target: a catch rate of at least 85% and a clear rate of at least 95%, each measured with a wobble under 10 points; one-off hand labelling under 5 hours; judging under $5 a week.

**Decision 1: which notes you label by hand.** Givens: the summariser writes 4,000 notes a week and about 8% are bad. A person labels one note in 40 seconds, so 5 hours is 450 notes. The complaints table from Round 1 holds 320 notes already known to be bad. Unknown: whether some kind of failure never gets complained about.

**Option A, 100 random notes.**
- **What happens:** you label 100 notes picked by chance from last week.
- **Effect on the target:** only about 8 are bad, so the catch rate rests on 8 notes and wobbles about 25 points. You cannot tell an 85% judge from a 60% one.
- **Cost:** 67 minutes of labelling.
- **Rules out:** meeting the 10-point wobble on the catch rate.

**Option B, 400 random notes.**
- **What happens:** the same, four times bigger.
- **Effect on the target:** about 32 bad notes, so the catch rate wobbles about 13 points: close, still over 10. The clear rate rests on 368 good notes and wobbles about 2.
- **Cost:** 4.4 hours.
- **Rules out:** the 10-point catch rate target, unless you label far more.

**Option C, 200 random notes plus 200 from the complaints table.**
- **What happens:** half chosen by chance, half taken from known failures.
- **Effect on the target:** about 216 bad notes, so the catch rate wobbles about 5 points; 184 good notes, so the clear rate wobbles about 3.
- **Cost:** 4.4 hours.
- **Rules out:** reading the true pass rate off your labels (half were chosen because they failed), and a fair share of any failure kind nobody complains about.

**Your pick.**

### Key
C. Only C gets the catch rate under a 10-point wobble inside 5 hours. It gives up a fair mix of failure kinds: failures nobody complains about are thin in the bad pile, and only the 200 random notes stand guard for them. If complaints were known to miss a kind, B would be the safer pick.

## BUILD-D2 · The rule the judge marks against
New: none
Status: done 2026-09-22 (picked C)

# Lesson 6 · The build · Decision 2 of 4

**Decision 2: the rule the judge marks against.** Givens: your Round 1 counts were missing_total 41, wrong_currency 18, truncated_page_2 9, credit_note_positive 6. All 74 are mistakes about the total. A vague rule makes the judge change its mind on the same note from run to run. Unknown: whether other kinds of failure exist, like a wrong due date, that nobody has counted yet.

**Option A, one broad rule: "Is this note correct?"**
- **What happens:** one call per note, and the judge decides for itself what correct means.
- **Effect on the target:** it can notice any kind of failure, even uncounted ones, but it flips on about 1 note in 8. About 12% of good notes get FAIL on a given run, so the clear rate sits near 88%, under the 95% target.
- **Cost:** one call per note.
- **Rules out:** a steady clear rate, and two runs that agree.

**Option B, one narrow rule: "Does the note state the total exactly as in the email, same currency and same sign?"**
- **What happens:** one call per note, one checkable question.
- **Effect on the target:** all four counted kinds are total mistakes, so all 74 are in its reach. It flips on about 1 note in 100, so the clear rate sits near 98%.
- **Cost:** one call per note.
- **Rules out:** seeing any failure that is not about the total. It stays blind to those until someone adds a rule.

**Option C, the total rule plus a second call checking the due date.**
- **What happens:** two calls per note, each with its own narrow rule.
- **Effect on the target:** it catches the counted kinds plus wrong due dates if they exist. Each rule has its own false alarms, so a good note gets two chances to be failed: the clear rate is near 96%.
- **Cost:** two calls per note, which doubles the judging bill whichever AI you pick in Decision 3.
- **Rules out:** half of the $5 a week, for a failure kind nobody has seen yet.

**Your pick.**

### Key
B. It covers all 74 counted failures and keeps the clear rate highest. It gives up blindness to non-total failures. The 200 random notes from Decision 1 are the check: if they show a due-date kind, C becomes right.

## BUILD-D3 · Which AI judges, and how many notes
New: none
Status: done 2026-09-22 (picked C modified: strong AI on 800 random, cheap AI on the other 3,200)

# Lesson 6 · The build · Decision 3 of 4

**Decision 3: which AI judges, and how many notes.** Givens: 4,000 notes a week, and your Decision 2 makes two calls per note. The cheap AI costs $0.0004 a call; a stronger AI costs $0.003. The cheap AI is the same one that writes the notes, so it misreads faded and handwritten scans the same way; those are about a third of the bad notes. The firm uses the judge to gate changes and count failure kinds; nobody re-sends a single note.

**Option A, the cheap AI on all 4,000 notes.**
- **What happens:** 8,000 cheap calls a week, every note marked.
- **Effect on the target:** it catches about 93% of bad typed notes but only half of the bad scans, because it cannot read them either. Two thirds at 93% plus one third at 50% puts the catch rate near 79%, under 85%.
- **Cost:** $3.20 a week.
- **Rules out:** the 85% catch rate, since its blind spot is the summariser's blind spot.

**Option B, the stronger AI on all 4,000 notes.**
- **What happens:** 8,000 strong calls a week, every note marked.
- **Effect on the target:** catch rate near 93% on every kind, scans included.
- **Cost:** $24 a week, almost five times the limit.
- **Rules out:** the $5 a week target.

**Option C, the stronger AI on 800 notes picked by chance.**
- **What happens:** 1,600 strong calls a week; the other 3,200 notes are never marked.
- **Effect on the target:** catch rate near 93%. The weekly pass rate rests on 800 notes, so it wobbles about 2 points, enough to see a 5-point fall.
- **Cost:** $4.80 a week.
- **Rules out:** flagging every bad note. Four in five are never looked at.

**Your pick.**

### Key
C. Strong enough to read scans, cheap enough to fit $5, and the firm only needs the rate. It gives up marking every note: if the firm had to catch each bad note before it reached a supplier, C would fail and the budget would have to rise to B.

## BUILD-D4 · How a change is judged better or worse
New: none
Status: done 2026-09-22 (picked B). Correction sent in BUILD-CALL: scans go from 1 in 7 notes to 1 in 3, a 2.4 point drop, not a third to half and 3 points.

# Lesson 6 · The build · Decision 4 of 4

**Decision 4: how the gate from Lesson 5 decides a change to the summariser is worse.** Givens: the instructions change about once a month. The strong AI's weekly pass rate rests on 800 notes and wobbles about 2 points. At month end, scans rise from a third of notes to half, and scans fail about three times as often as typed notes, so the pass rate drops about 3 points with nothing changed. Your 400 hand-labelled emails from Decision 1 are fixed and can be summarised again at any time.

**Option A, block on any fall in this week's rate against last week's.**
- **What happens:** the gate compares two weekly numbers.
- **Effect on the target:** a change that did nothing falls by luck about half the time, so about half of harmless changes get blocked.
- **Cost:** nothing extra.
- **Rules out:** trusting a block, since half are noise.

**Option B, block only on a fall bigger than the 2-point wobble.**
- **What happens:** the same comparison with a margin.
- **Effect on the target:** luck no longer blocks, but the notes differ each week. A harmless change at month end reads as a 3-point fall and is blocked; a real 3-point fall made at month start can be hidden by an easier week.
- **Cost:** nothing extra.
- **Rules out:** telling a change apart from a change in the invoice mix.

**Option C, run the old and new versions on the same 400 labelled emails and count notes that flip from pass to fail.**
- **What happens:** both versions summarise identical emails and the strong AI judges both.
- **Effect on the target:** the invoice mix is identical, so only the change shows.
- **Cost:** 1,600 strong calls, $4.80 per change, about $1.20 a week spread over a month, on top of weekly judging.
- **Rules out:** seeing new invoice types, since the 400 emails stay fixed until you label more.

**Your pick.**

### Key
C. It is the only option where one thing differs. It gives up freshness and $1.20 a week; if the budget has no room, B with the month-end swing noted is the fallback.

## BUILD-CALL · Predict the numbers
New: none
Status: done 2026-09-22 (he skipped predicting: "just build")

# Lesson 6 · The build · Your predictions

One correction first. In Decision 4 I wrote that scans go from a third of notes to half at month end. That clashes with Decision 3, where scans are a third of the bad notes. The consistent figure is 1 in 7 notes normally and 1 in 3 at month end, so the pass rate drops about 2.4 points with nothing changed, not 3. That is still over the 2-point wobble, so the reasoning in Decision 4 is unchanged.

Your four picks, which I will build exactly:

```
1  label 200 random notes + 200 from the complaints table
2  two rules, two calls per note: the total, and the due date
3  strong AI on 800 random notes, cheap AI on the other 3,200
4  block a change only on a fall bigger than the 2-point wobble
```

**Your call.** Predict four numbers:

1. What does one week of judging cost under your Decisions 2 and 3?
2. The cheap AI's 3,200 notes hold about 256 bad ones, and it catches 79% of them. How many bad notes does it miss each week?
3. Each of your two rules fails a good note 2% of the time. What is the strong judge's clear rate, and does it clear the 95% target?
4. Ten harmless changes are made at month end. How many does your gate block?

### Key
1. $7.36 ($4.80 strong + $2.56 cheap), over the $5 target
2. about 54
3. about 96% (98% x 98%), just over 95%
4. about 5 of 10 (the 2.4 point drop sits just past the 2 point line, so luck decides about half)
What this gives up: the cheap half breaks the budget, and rule B cannot tell a change from the month-end mix.
