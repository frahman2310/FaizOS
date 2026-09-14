# Lesson 3 · meter · teaching script
Taught so far: see the Session ledger in docs/learning-evidence.md. Round 2 Part A is done.

## R2-B · Changing what's under a label
New: putting a dict label on the left of `=`
Status: rebuilt 2026-09-14 (old version used a table for broken code)

# Round 2 · Part B · Changing what's under a label

**The problem.** The trip switch has to remember two things between calls: how many failures in a row, and the closed-until time. Both keep changing.

**The fix:** keep both in one dict, and change a value by putting its label on the left of `=`.

```python
score = {"home": 0, "away": 0}
score["home"] = score["home"] + 1
```

**Picture:** a scoreboard with two labelled boxes. You rub out the number under "home" and write the new one. "Away" is untouched.

- **Right side first:** `score["home"]` is 0, so 0 + 1 = 1.
- **Then the label on the left** gets it: "home" is now 1.
- **Every other label** stays as it was.

The real scoreboard, and the lines that change it:

```
breaker = {"dead_in_a_row": 0, "open_until": 0.0}         the switch's scoreboard
def breaker_record(ok, now):              told after each call; ok is True if it worked
    if ok:
        breaker["dead_in_a_row"] = 0                       worked: streak back to 0
    else:
        breaker["dead_in_a_row"] = breaker["dead_in_a_row"] + 1    failed: add 1
```

**Your turn.**

1. Starting from `{"home": 0, "away": 0}`, the `score["home"]` line runs twice. What is `score`?
2. `breaker` starts as shown. One call fails. What is `breaker["dead_in_a_row"]`?
3. Another call fails. Now what is it?
4. The next call works. Now what is it?
5. **Someone broke it.** The adding line became `breaker["dead_in_a_row"] = 1`. Three calls fail in a row. What is it after the third? Crash, quietly wrong, or fine?

### Key
1. {"home": 2, "away": 0}
2. 1
3. 2
4. 0
5. 1; quietly wrong (it can never reach 3, so the switch never trips)

## R2-C · The switch trips
New: `>=` (at least)
Status: pending

# Round 2 · Part C · The switch trips

**The problem.** Counting failures does nothing on its own. When the streak reaches 3, something has to actually close the shop.

**The fix:** when the streak is at least 3, write the closed-until time and start counting again from 0.

```python
if streak >= 3:
    open_until = now + 5.0
    streak = 0
```

`>=` means "at least": `3 >= 3` is True, `4 >= 3` is True, `2 >= 3` is False.

**Picture:** a fuse box. Three sparks in a row and the fuse trips. Once it is reset, the spark count starts again from zero.

- **Streak reaches 1 or 2:** nothing else happens.
- **Streak reaches 3:** closed for 5 seconds, and the streak goes back to 0.

The real lines, which run straight after a failure is added:

```
TRIP_AT = 3                        failures in a row before it trips
COOL_OFF = 5.0                     seconds it stays closed
if breaker["dead_in_a_row"] >= TRIP_AT:
    breaker["open_until"] = now + COOL_OFF      write the closed-until time
    breaker["dead_in_a_row"] = 0                start counting again
```

**Your turn.**

1. Is `2 >= 3` True or False? And `3 >= 3`?
2. The third failure in a row happens when the clock reads 200.0. What is `open_until`?
3. Straight after that, what is `dead_in_a_row`?
4. On a normal day, 1 call in 12 fails by bad luck. Which setting closes the shop after a single unlucky failure: `TRIP_AT = 3` or `TRIP_AT = 1`?
5. **Someone broke it.** They deleted the line that starts counting again from 0. The shop reopens and one more call fails. What is `dead_in_a_row`, and does it trip again straight away? Crash, quietly wrong, or fine?

### Key
1. False; True
2. 205.0
3. 0
4. TRIP_AT = 1
5. 4, and 4 >= 3 so it trips again after one failure; quietly wrong

## R2-D · Reading the report
New: none (the idea: a number built only from calls that worked)
Status: pending

# Round 2 · Part D · Which calls a number counts

**The problem.** On a bad day, failed calls drop out of the timing numbers. So latency can look better on the worst day, while users are getting errors.

**The fix:** always ask which calls a number was built from, and read it next to the success rate.

```python
times = []
for row in log:
    if row["ok"]:
        times.append(row["ms"])
```

**Picture:** a restaurant that only asks diners who finished their meal how long they waited. People who walked out after an hour are never counted, so the wait looks great.

- **A call worked:** its time goes into `times`, and so into p50 and p95.
- **A call failed:** it is skipped, and its time never reaches p50 or p95.

Two example days:

```
                 normal day    bad day
succeeded        100%          60%
p95 latency      676 ms        410 ms
```

**Your turn.**

1. 100 calls, 40 fail. How many times end up in `times`?
2. Which day looks faster on p95?
3. On which day were users better off?
4. A call fails all three tries after 1,500 ms. Is its 1,500 in the p95? How many records does it add to the log?
5. **Someone broke it.** They removed the `if row["ok"]:` line. On a day when the closed sign turned away 17 of 20 calls, each recorded at 0 ms, what does p50 show? Crash, quietly wrong, or fine?

### Key
1. 60
2. the bad day
3. the normal day
4. no; one record
5. 0 ms (17 of the 20 times are 0); quietly wrong

## R2-E · Find the planted bug
New: none (reading a real report to find a one-word change)
Status: pending

# Round 2 · Part E · Find the planted bug

**The problem.** Someone changed one word in the report. Nothing crashes and the normal day still looks right. Only the outage day gives it away.

**The fix:** check each number against what must be true, then find the line that could make them disagree.

```python
retried = 0
for row in oks:
    if row["attempts"] > 1:
        retried = retried + 1
```

**Picture:** counting "customers who paid after one declined swipe". You count from the paid receipts. Count from every receipt and the walk-outs get counted too.

- **Counting from `oks`:** only calls that worked, so each counted call really succeeded on a retry.
- **Counting from every record:** a failed call also has `"attempts": 3`, so it gets counted.

The outage day, from the broken copy I ran:

```
calls              20
succeeded          0  (0%)
succeeded on retry 3
skipped by breaker 17
```

**Your turn.**

1. How many calls succeeded?
2. So how many calls can possibly have succeeded on a retry?
3. The report says 3. Is it telling the truth?
4. A failed call has `"attempts": 3`. Is `3 > 1` True or False?
5. **Someone broke it.** Which word in the counting loop was changed, and to what? Crash, quietly wrong, or fine?

### Key
1. 0
2. 0
3. no
4. True
5. `oks` changed to `log`; quietly wrong
