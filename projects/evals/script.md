# Lesson 5 · evals · teaching script
Goal: an eval set of real cases and a gate that blocks a bad change. Skills: eval-set-construction,
deterministic-assertions, ci-eval-gate, github-actions, oidc-keyless-deploy, iam-trust-scoping.
Number: pass rate on 100 cases, and one change the gate blocks.

Carry-over from L4: three adjustments, from docs/learning-evidence.md
- Every saving or difference question comes after one worked "before minus after" on other numbers (E11: 0/2 first try in L4).
- Every Someone broke it question defines the labels inline (B11b: both L4 label misses were the word "wrong").
- The build goes one decision per message, each option with its effect on the target number worked through, then a debrief with the road not taken (B14: decision 5 "no deadline" predicted 736 ms, measured 1,753 ms; C31, C32).
Also: evals are where his weak spot lives (E1, quietly wrong); lean every part on catching quiet failures with numbers.

## R1-Av1 · A fixed test for every change
New: an eval set, a fixed list of real cases with what a right answer must contain
Status: withdrawn 2026-09-15 (undefined jargon: prompt, ship, summariser, eval set; C33)

# Lesson 5 · evals · Round 1 · Part A · A fixed test for every change

**The problem.** You change your summariser's prompt, try it on 3 invoices, they look fine, and you ship. By Monday 40 of every 100 summaries leave out the total, and nothing warned you.

**The fix:** keep an eval set, a fixed list of real cases each saying what a right answer must contain, and run every case after every change.

```python
cases = [
    {"invoice": "INV-001", "must_contain": "$120"},
    {"invoice": "INV-002", "must_contain": "$45"},
]
```

The pass rate is cases passed divided by all cases. To compare two runs, take before minus after: 90% then 85% is a drop of 90 - 85 = 5 points. Separate chances multiply: two coin flips both heads is 0.5 x 0.5 = 0.25.

**Picture:** a driving test on a fixed route. Every driver takes the same turns, so scores can be compared. A quick drive round the block tells you almost nothing.

- **The summary contains the `must_contain` text:** that case passes.
- **It does not:** that case fails.
- **Every change:** all cases run again, so two pass rates can be compared.

**Your turn.**

1. 100 cases, 88 pass. What is the pass rate?
2. The old prompt passed 88 cases and the new one passes 60. How many points did the pass rate drop?
3. The case says `must_contain: "$45"` and the summary reads "Total due: $54". Pass or fail?
4. 40 in 100 summaries are broken, so each checked invoice has a 0.6 chance of looking fine. What is the chance all 3 invoices you checked by eye look fine?
5. **Someone broke it.** The `must_contain` values were copied from the new prompt's own summaries, so the new prompt passes 100%. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 88%
2. 28 points (88 - 60)
3. fail
4. 0.216, about 22%
5. quietly wrong (the test just repeats the new prompt's answers)
Relies on: pass rate = passed / all; before minus after; separate chances multiply; a case passes only if the text is contained exactly

## R1-Av2 · Checking every change the same way
New: a test case, one real invoice paired with the text a correct summary must include
Status: withdrawn 2026-09-17 (problem had no context; C34)

# Lesson 5 · Round 1 · Part A · Checking every change the same way

**The problem.** Your app sends each invoice to the AI with the same written instructions, and the AI writes back a short summary. You reword the instructions, read 3 summaries, they look fine, and put the change live. A week later you find that 40 of every 100 summaries leave out the total amount.

**The fix:** before any change goes live, run it on the same list of real invoices, each paired with the one piece of text a correct summary must include. Each of those pairs is called a test case.

```python
test_cases = [
    {"invoice": "INV-001", "must_include": "$120"},
    {"invoice": "INV-002", "must_include": "$45"},
]
```

**Picture:** a teacher's answer key. For each exam question it lists the one thing a correct answer must have, so every student is marked exactly the same way.

- **The summary includes the required text exactly:** that test case passes.
- **It does not:** that test case fails.
- **After every change:** the whole list runs again and you count how many passed.

**Your turn.**

1. INV-002 must include `$45`. The summary says "Total due: $54". Pass or fail?
2. INV-001 must include `$120`. The summary says "Invoice total $120, due Friday". Pass or fail?
3. The list has 100 test cases and 88 pass. What percentage passed?
4. 40 in every 100 summaries leave out the total. Which is more likely to catch that: reading 3 summaries by eye, or checking all 100 test cases?
5. **Someone broke it.** The required text for every test case was copied from the new instructions' own summaries, so every test case passes. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. fail
2. pass
3. 88%
4. checking all 100 test cases
5. quietly wrong (the answer key was copied from the answers being marked)
Relies on: a test case passes only when the exact text appears; percentage = passed / all x 100

## R1-A · Checking every change the same way
New: a test case, one real invoice paired with the text a correct summary must include
Status: done 2026-09-18

# Lesson 5 · Round 1 · Part A · Checking every change the same way

**The problem.** Your client is an accounting firm that receives 1,000 supplier invoices a week. Your app sends each invoice to the AI with the same written instructions, the AI writes back a three-line summary, and the firm's staff approve payments from that summary without opening the invoice. The AI does not follow fixed rules the way a calculator does: it follows your wording, so rewording the instructions changes how it handles every invoice, including the ones you never look at. You reword the instructions, read 3 summaries, they look fine, and put the change live. For a week nobody reads the other 997, and 40 in every 100 summaries now leave out the total, so staff approve payments without seeing the amount.

**The fix:** before any change goes live, run it on the same list of real invoices, each paired with the one piece of text a correct summary must include. Each of those pairs is called a test case.

```python
test_cases = [
    {"invoice": "INV-001", "must_include": "$120"},
    {"invoice": "INV-002", "must_include": "$45"},
]
```

**Picture:** a teacher's answer key. For each exam question it lists the one thing a correct answer must have, so every student is marked exactly the same way.

- **The summary includes the required text exactly:** that test case passes.
- **It does not:** that test case fails.
- **After every change:** the whole list runs again and you count how many passed.

**Your turn.**

1. INV-002 must include `$45`. The summary says "Total due: $54". Pass or fail?
2. INV-001 must include `$120`. The summary says "Invoice total $120, due Friday". Pass or fail?
3. The list has 100 test cases and 88 pass. What percentage passed?
4. 40 in every 100 summaries leave out the total. Which is more likely to catch that: reading 3 summaries by eye, or checking all 100 test cases?
5. **Someone broke it.** The required text for every test case was copied from the new instructions' own summaries, so every test case passes. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. fail
2. pass
3. 88%
4. checking all 100 test cases
5. quietly wrong (the answer key was copied from the answers being marked)
Relies on: a test case passes only when the exact text appears; percentage = passed / all x 100

## R1-B · A check that stops the program
New: assert, a line that stops the program when a check is false
Status: done 2026-09-18

# Lesson 5 · Round 1 · Part B · A check that stops the program

**The problem.** Your test cases now run automatically every time you change the instructions, and they print how many passed. The person putting the change live at 6pm sees a hundred lines of output scroll past and does not read them, because nothing about a printed line demands attention. So a run that printed "88 of 100 passed" goes live anyway, and the accounting firm gets a week of summaries with no totals. A printed message is a suggestion. What you want is something that makes the machine refuse to carry on when a check fails, so the bad change physically cannot reach the firm.

**The fix:** use `assert`, a line that asks a yes-or-no question and stops the whole program the moment the answer is no.

```python
passed = 88
total = 100
assert passed == total
```

**Picture:** a smoke alarm. Silent while everything is fine, and impossible to ignore when it is not.

- **The answer is yes (88 == 88):** nothing happens at all and the next line runs.
- **The answer is no (88 == 100):** the program stops on that line with an error called AssertionError, and nothing after it runs.
- **A printed message instead:** it scrolls past and the program carries on regardless.

**Your turn.**

1. `passed` is 100 and `total` is 100. What does the assert line do?
2. `passed` is 88 and `total` is 100. What does it do, and does the line after it run?
3. Which is harder to ignore at 6pm: one printed line among a hundred, or the program stopping with an error?
4. The firm gets 1,000 invoices a week and 40 in every 100 summaries lose the total. How many bad summaries is that in a week?
5. **Someone broke it.** The line was changed to `assert passed >= 0`, and `passed` is 88. What does the assert line do? Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. nothing; the next line runs
2. stops with AssertionError; the next line does not run
3. the program stopping
4. 400
5. nothing (88 is at least 0), so every change passes the check; quietly wrong
Relies on: == asks whether two things are the same; >= asks at least; a stopped program shows the line it stopped on

## R1-C · Where the cases come from
New: cases come from real failures, not from invoices you imagine
Status: done 2026-09-18

# Lesson 5 · Round 1 · Part C · Where the cases come from

**The problem.** You sit at your desk and write 100 test cases by inventing invoices: one page, clean English, a total at the bottom. The accounting firm's real post bag is nothing like that. It holds handwritten scans, two-page invoices with the total on page two, amounts in rupees and dollars, and credit notes whose total is negative. Your list passes 100% every time while the firm keeps ringing up to complain, because a list you invented can only test the failures you already thought of, and those were never the ones hurting you. The failures that cost money are the ones nobody imagined.

**The fix:** build the list out of invoices that really failed, so every complaint the firm makes becomes a new test case.

```python
test_cases = [
    {"invoice": "scan-0412-handwritten", "must_include": "PKR 84,000"},
    {"invoice": "credit-note-77", "must_include": "-$310"},
]
```

**Picture:** a driving instructor. Practising in an empty car park forever is comfortable and teaches nothing. The roundabout that fails people is the one worth driving again and again.

- **A complaint arrives:** that invoice becomes a case with the text its summary should have contained, and the list gets closer to the real post bag.
- **A later change breaks a case that used to pass:** the list catches it. The same failure coming back is called a regression.
- **A case you invented at your desk:** it passes forever and tells you nothing new.

**Your turn.**

1. The firm complains 6 times a month and each complaint becomes a case. How many real cases after 3 months?
2. Which list is more likely to catch tomorrow's failure: 100 invoices you invented, or 18 invoices that really failed?
3. A complaint about a handwritten scan was fixed and became a case. Months later a change breaks it again. Does the list notice?
4. The AI misread a credit note and reported the total as positive. Should that invoice become a test case?
5. **Someone broke it.** The pass rate, meaning the share of cases that pass, had to read 100% before a meeting, so someone deleted the 12 cases that were failing. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 18
2. the 18 real ones
3. yes, that case fails
4. yes
5. quietly wrong (100% now measures only the cases that already passed)
Relies on: a case passes only when the exact text appears; the list only tests what is in it

## R1-D · How many cases you need
New: the size of the list decides the smallest change it can show
Status: done 2026-09-18

# Lesson 5 · Round 1 · Part D · How many cases you need

**The problem.** You keep 20 test cases because each one costs an AI call to run. You reword the instructions, the pass rate goes from 90% to 85%, and you spend an afternoon arguing with yourself about whether the change is worse or whether that is just noise. With 20 cases, one single case swinging from pass to fail moves the number by 5 points all on its own, so a 5 point drop tells you nothing at all. Meanwhile the firm is waiting, and you either ship a worse change or throw away a good one on a coin flip.

**The fix:** hold enough cases that one case is worth far less than the change you need to notice.

```
 20 cases  -> one case is worth 100 / 20  = 5 points
100 cases  -> one case is worth 100 / 100 = 1 point
500 cases  -> one case is worth 0.2 points
```

**Picture:** bathroom scales that only show whole stones. Step on them after a month of dieting and they read the same number, not because nothing changed but because the marks are too far apart.

- **20 cases, a 5 point drop:** that is one case, so you cannot tell a real fall from luck.
- **100 cases, a 5 point drop:** that is 5 cases changing together, which luck explains far less easily.
- **Every extra case:** one more AI call on every run, so the list costs money and time.

**Your turn.**

1. Your list has 25 cases. How many points is one case worth?
2. You need to notice a 2 point drop. Which list can even show a difference that small: 25 cases or 100 cases?
3. Each case costs $0.0027 to run. You run the 100 case list 20 times a day. What does that cost per day?
4. A 500 case list at the same price: what does one run cost?
5. **Someone broke it.** To save money the list was cut from 100 cases to 10, and a change is still blocked only when the pass rate falls. A change arrives that really makes 5 in every 100 summaries worse. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 4 points
2. 100 cases
3. $5.40 a day (100 x 0.0027 x 20)
4. $1.35
5. quietly wrong (with 10 cases one case is 10 points, so a 5 point fall cannot show and the change goes through)
Relies on: one case is worth 100 / number of cases; a run costs one AI call per case

## R2-A · A check nobody can skip
New: a gate, an automatic check that every proposed change must pass before it is allowed in
Status: done 2026-09-18

# Lesson 5 · Round 2 · Part A · A check nobody can skip

**The problem.** You now have 100 real cases and a check that stops on a failure, but both only run when you remember to run them. On Friday evening you make a one word change to the instructions, decide it is too small to be worth a run, and push it out. The change quietly breaks handwritten scans, and the accounting firm approves a week of payments from summaries with no totals before anyone notices. Nothing in this story is a technical failure: the machinery worked and was simply not switched on, which is how most of these weeks happen.

**The fix:** put the check in the path the change must travel, so it runs on every proposed change by itself and refuses the ones that fail. A check placed there is called a gate.

```
change proposed -> run all 100 cases -> all pass? -> yes: allowed in
                                                 -> no:  blocked
```

**Picture:** airport security. Every passenger goes through the same scanner, and nobody gets to decide that their own bag is too small to bother with.

- **Every case passes:** the change is allowed in.
- **Any case fails:** the change is blocked and the failing case is named.
- **You forget to run anything:** it makes no difference, because the gate runs on the proposal, not on your good intentions.

**Your turn.**

1. 100 cases run, 99 pass and 1 fails. Is the change allowed in or blocked?
2. You never run the cases on your own laptop. Does the change still get checked?
3. With a gate in place, how many bad summaries does the Friday change deliver to the firm?
4. One run of the 100 cases costs $0.27. Your team proposes 20 changes a day, 5 days a week. What do the runs cost for the week?
5. **Someone broke it.** The gate was set to report failures but allow the change in anyway, so the Friday change goes through with 1 case failing. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. blocked
2. yes
3. 0
4. $27 (0.27 x 20 x 5)
5. quietly wrong (the report is right and the change still reaches the firm)
Relies on: a case passes only when the exact text appears; the gate runs on the proposed change, not on the laptop

## R2-B · What the gate compares against
New: the baseline, the score of the version the firm is using today
Status: done 2026-09-18

# Lesson 5 · Round 2 · Part B · What the gate compares against

**The problem.** Your gate blocks anything scoring under 95%, which sounded strict and sensible when you set it. The trouble is that your list is full of the firm's genuinely hard invoices, so the version they are happily using today scores 92%. Every change you propose is now blocked, including the ones that fix handwritten scans, so within a week your team quietly drops the bar to 85% to get any work through. Now a change that takes the firm from 92% down to 86% sails past, because an absolute number tells you nothing about whether this change makes the firm's life better or worse.

**The fix:** run both versions on the same cases and block the change only when it scores lower than the version the firm is using today, whose score is called the baseline.

```
baseline, live today: 92 of 100 pass
proposed change:      89 of 100 pass  -> worse, blocked
proposed change:      94 of 100 pass  -> better, allowed
```

**Picture:** a runner's personal best. Nobody bans an athlete for missing the world record. You compare them with their own last time, on the same track.

- **The change scores above the baseline:** allowed in, and its score becomes the new baseline.
- **The change scores the same:** allowed in, because the firm is no worse off.
- **The change scores below:** blocked, and the cases that changed are named.

**Your turn.**

1. The baseline is 92 and the change scores 90. Blocked or allowed?
2. The baseline is 92 and the change scores 92. Blocked or allowed?
3. With the old rule of "must beat 95%" and today's live version at 92%, how many of your changes get through?
4. The baseline is 92, a change scoring 94 is allowed in, and the next change scores 93. Blocked or allowed?
5. **Someone broke it.** The baseline is measured by running the proposed change itself and comparing that score with itself. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. blocked
2. allowed
3. none
4. blocked (the baseline is 94 now)
5. quietly wrong (the two scores always match, so everything is allowed)
Relies on: the baseline is the live version's score on the same cases; a passing change becomes the new baseline

## R2-C · The computer that runs the gate
New: a recipe file that starts a fresh computer to run the gate (GitHub Actions)
Status: done 2026-09-18

# Lesson 5 · Round 2 · Part C · The computer that runs the gate

**The problem.** The gate has to run on some computer, and the obvious one is your laptop. Your laptop is asleep at 2am when a teammate in another city proposes a change, so nothing checks it. Worse, your laptop has Python 3.12 and theirs has 3.9, so the same cases can pass on one machine and fail on the other, and the team ends up arguing about whose computer is right instead of whether the change is good. A check that depends on which machine ran it is not a gate, it is a coin flip with extra steps.

**The fix:** keep a recipe file in the project that says what to run, and let a service start a fresh identical computer for every proposed change and run it there. The service that does this is called GitHub Actions.

```
when:   a change is proposed
start:  a fresh computer, same setup every time
run:    build the box, run the 100 cases
report: pass or fail, back onto the proposal
```

**Picture:** a rented test kitchen. Every baker uses the same oven, so a burnt cake says something about the recipe rather than about somebody's oven at home.

- **A change is proposed at 2am:** a fresh computer starts, runs the cases and reports, with nobody awake.
- **A case fails:** the report says fail, and the change is blocked.
- **Your laptop has a different Python:** it makes no difference, because the fresh computer is set up identically every run.

**Your turn.**

1. Your laptop is off when a teammate proposes a change. Does the gate still run?
2. Three teammates have three different laptops. How many different setups actually run the cases?
3. The service charges $0.008 a minute, a run takes 3 minutes, and there are 20 runs a day. What does that cost per day?
4. Should the recipe file live inside the project, so it travels with the code, or in one person's private notes?
5. **Someone broke it.** The recipe was changed so the cases run only when a person clicks a button. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. yes
2. one
3. $0.48 (0.008 x 3 x 20)
4. inside the project
5. quietly wrong (the gate looks present but only runs when somebody remembers to click)
Relies on: the gate blocks a change when a case fails; the fresh computer is identical every run

## R2-D · The password the robot needs
New: a short-lived pass the robot asks for at run time instead of a stored password
Status: done 2026-09-18

# Lesson 5 · Round 2 · Part D · The password the robot needs

**The problem.** The fresh computer has to call the AI to run your 100 cases, so it needs the password your app uses with the AI company. The easy route is to paste that password into the service's settings, where it sits forever, readable by every run and by anyone who can edit the recipe file. Your AI account has a $500 a day spending limit and access to the firm's invoices, so that one string of text is the whole lock. Leaked passwords are usually found and used within minutes, and then you are changing the password everywhere it appears while the bill runs.

**The fix:** store no lasting password, and have the robot prove which project it is at run time and receive a pass that expires within minutes. Proving identity that way is called OIDC.

```
stored password:  valid forever, readable by every run
short-lived pass: asked for when the run starts, expires in 15 minutes
```

**Picture:** a building. Posting a permanent master key through the letterbox, or issuing a visitor badge that stops working at 5pm.

- **A stored password leaks:** it works until somebody notices and changes it everywhere.
- **A short-lived pass leaks:** it is worthless a few minutes later.
- **The robot needs access:** it asks at the start of the run and is given only what the run needs.

**Your turn.**

1. A stored password leaks at 9am and you notice at 5pm. For how many hours can a stranger use it?
2. A 15 minute pass leaks at 9am and you notice at 5pm. For how long can it be used?
3. The AI account allows $500 a day. What is the most a leaked password can cost you per day until it is changed?
4. Should the run's pass also be allowed to change the live service, or only to run the cases?
5. **Someone broke it.** To stop runs ever being refused access, the short-lived pass was given the right to do everything in the account. The 100 cases run and report correctly. Crash (it stops), quietly wrong (runs, wrong result), or fine (runs, right result)?

### Key
1. 8 hours
2. 15 minutes
3. $500 a day
4. only to run the cases
5. fine (the result is right; the risk if that pass leaks is now the whole account)
Relies on: a leaked password works until it is changed; a short-lived pass expires by itself

## BUILD-D1 · How many cases
New: none
Status: done 2026-09-18 (picked B)

# Lesson 5 · The build · Decision 1 of 5

**The build.** A working gate on this Mac: it runs your cases against two versions of the instructions and blocks the worse one. Target: it must block a change that makes 5 in every 100 summaries worse, must not block a change that is equal or better, and one run must cost under $1 and finish in under 2 minutes.

**Decision 1: how many cases.** Givens: the firm has sent 18 real complaints, you can invent as many cases as you like, each case costs $0.0027 in AI calls and about 0.4 seconds. The change you must catch makes 5 in every 100 summaries worse.

**Option A, 20 cases.**
- **What happens:** one quick run over a small list.
- **Effect on the target:** one case is worth 100 / 20 = 5 points, so a 5 point fall is a single case and cannot be told apart from luck. The gate misses the change you must catch.
- **Cost:** $0.05 and 8 seconds a run.
- **Rules out:** noticing anything smaller than a 5 point change.

**Option B, 100 cases.**
- **What happens:** every run scores both versions over 100 cases.
- **Effect on the target:** one case is worth 1 point, so the 5 point fall shows up as 5 cases turning red, which luck rarely produces.
- **Cost:** $0.27 and 40 seconds a run.
- **Rules out:** the cheapest possible run, and any hope of seeing a 1 point change.

**Option C, 500 cases.**
- **What happens:** the same run over a much longer list.
- **Effect on the target:** one case is worth 0.2 points, so even a 1 point fall is visible.
- **Cost:** $1.35 and about 3 minutes a run, which breaks both limits.
- **Rules out:** staying under $1 a run and under 2 minutes.

**Your pick.**

### Key
B. A is blind to the 5 point fall; C is sharper but breaks the cost and time limits. B gives up the resolution C would have had.

## BUILD-D2 · Where the 100 cases come from
New: none
Status: done 2026-09-18 (picked C)

# Lesson 5 · The build · Decision 2 of 5

**Decision 2: where the 100 cases come from.** Givens: 18 invoices really failed and the firm complained about each one. The rest of the list has to come from somewhere. The change you must catch breaks handwritten scans, and 12 of the 18 complaints are handwritten scans. An invented case is one you write at your desk from a clean typed invoice.

**Option A, 100 invented cases.**
- **What happens:** you write 100 tidy invoices and the text each summary should contain.
- **Effect on the target:** none of them are handwritten, so the broken change passes all 100 and the gate lets it through. The target is missed outright.
- **Cost:** an afternoon of writing, no waiting on the firm.
- **Rules out:** catching any failure you did not already imagine.

**Option B, the 18 real complaints only.**
- **What happens:** the list is exactly what the firm has complained about.
- **Effect on the target:** 12 of 18 are handwritten, so the change turns them red and the gate blocks it. But one case is worth 100 / 18 = 5.6 points, so smaller changes stay invisible.
- **Cost:** $0.05 a run, and you wait for complaints to grow the list.
- **Rules out:** seeing changes smaller than about 6 points.

**Option C, the 18 real plus 82 invented.**
- **What happens:** every real complaint stays in, and invented cases pad the list to 100.
- **Effect on the target:** the 12 handwritten cases still turn red, and with 100 cases one case is 1 point, so the 5 point fall is clear. Both halves of the target hold.
- **Cost:** $0.27 a run plus the afternoon of writing.
- **Rules out:** pretending the pass rate describes the firm's real post bag, since 82 cases are your own inventions.

**Your pick.**

### Key
C. A cannot see the failure at all; B sees it but is too coarse for smaller ones. C gives up an honest pass rate, since 82 of its cases are invented and inflate the score.

## BUILD-D3 · The rule the gate uses
New: none
Status: done 2026-09-18 (picked B)

# Lesson 5 · The build · Decision 3 of 5

**Decision 3: the rule that blocks a change.** Given: the AI does not answer identically every time, so running the same version twice scores up to 2 cases apart on your 100 cases. The change you must catch costs 5 points. Your team proposes 20 changes a day, and a blocked change costs someone an hour of rechecking.

**Option A, block on any fall below the baseline.**
- **What happens:** score once, block if even one case fewer passes.
- **Effect on the target:** catches the 5 point fall every time. It also blocks unchanged work whenever the AI wobbles 1 or 2 cases down, which is most days, so perhaps 5 of 20 changes a day get stopped for nothing.
- **Cost:** $0.27 a run, plus about 5 wasted hours a day across the team.
- **Rules out:** trusting a block, which is how teams end up switching the gate off.

**Option B, block only on a fall of more than 2 points.**
- **What happens:** score once, allow anything within the wobble.
- **Effect on the target:** the 5 point fall is still blocked. A real 2 point fall now passes silently, and three of those in a row take the firm down 6 points with no warning.
- **Cost:** $0.27 a run, no wasted hours.
- **Rules out:** catching small real falls, and noticing slow decay.

**Option C, run each version twice and compare the averages.**
- **What happens:** four runs per change instead of two, then compare.
- **Effect on the target:** averaging halves the wobble to about 1 case, so a 2 point fall is catchable and the 5 point fall is certain.
- **Cost:** $0.54 and 80 seconds a run, and double the AI calls on every proposal.
- **Rules out:** the cheapest run, and it still leaves some wobble.

**Your pick.**

### Key
B for a team shipping 20 changes a day; C once small falls matter more than the extra spend. B gives up small real falls; C gives up half the run budget; A gives up the team's trust.

## BUILD-D4 · When the gate runs
New: none
Status: done 2026-09-18 (picked C)

# Lesson 5 · The build · Decision 4 of 5

**Decision 4: when the gate runs.** Givens: your team proposes 20 changes a day, a run costs $0.27 and takes 40 seconds, and the firm processes about 140 invoices a day. A bad change that reaches the firm ruins every summary it touches until someone pulls it back.

**Option A, on every proposed change.**
- **What happens:** all 20 proposals a day are scored before anyone can let them in.
- **Effect on the target:** a bad change never reaches the firm, so bad summaries from it are 0.
- **Cost:** $5.40 a day, and 40 seconds added to each proposal.
- **Rules out:** a free gate, and instant proposals: every change now waits on a run.

**Option B, once a night.**
- **What happens:** one run at 2am scores whatever went in that day.
- **Effect on the target:** a bad change let in at 9am is live all day, so about 140 invoices get bad summaries before the night run finds it.
- **Cost:** $0.27 a day, and nothing added to any proposal.
- **Rules out:** blocking anything, since the change is already in when the run happens.

**Option C, on every proposed change that touches the instructions, nightly for everything else.**
- **What happens:** changes to the AI instructions are gated; changes elsewhere wait for the night run.
- **Effect on the target:** the 5 point change you must catch is an instructions change, so it is blocked. A bad change in other code still reaches the firm for up to a day.
- **Cost:** about $1.35 a day if 5 of the 20 proposals touch instructions.
- **Rules out:** catching failures that come from the rest of the code before they land.

**Your pick.**

### Key
A when the firm is live and 140 invoices a day are at stake; C when the run budget matters more than code-side failures. A gives up $5.40 a day and 40 seconds per proposal; C gives up protection against non-instruction changes; B gives up the ability to block at all.

## BUILD-D5 · What the run uses for a password
New: none
Status: done 2026-09-18 (picked B)

# Lesson 5 · The build · Decision 5 of 5

**Decision 5: what the run uses for a password.** Givens: the run must call the AI 200 times per proposal, your AI account allows $500 a day, setting up a short-lived pass takes about two hours of fiddling with settings, and you are one person with no security team. The cases must reflect what the real AI does today.

**Option A, a stored password.**
- **What happens:** the password sits in the service's settings and every run reads it.
- **Effect on the target:** the gate works exactly as designed and the numbers are real.
- **Cost:** nothing to set up. If it ever leaks, someone can spend $500 a day and read the firm's invoices until you notice and change it everywhere.
- **Rules out:** limiting the damage of a leak, and knowing which run used the password.

**Option B, a short-lived pass.**
- **What happens:** each run proves which project it is and gets a pass that dies in 15 minutes.
- **Effect on the target:** identical numbers, since the AI calls are the same.
- **Cost:** about two hours of setup now, and a fiddly settings page you will forget the details of.
- **Rules out:** a five minute setup, and running the gate anywhere that cannot do this handshake.

**Option C, recorded AI answers, no password.**
- **What happens:** the run replays answers recorded earlier instead of calling the AI.
- **Effect on the target:** it cannot catch the change you must catch. Reworded instructions produce the same recorded answers, so the 5 point fall is invisible.
- **Cost:** free, instant, and no password anywhere.
- **Rules out:** testing anything about the AI itself, which is the whole point of the gate.

**Your pick.**

### Key
B for anything the firm depends on; A only while nothing real is behind the account. B gives up two hours and portability; A gives up any limit on a leak; C gives up the ability to catch instruction changes at all.

## BUILD-CALL · Predict the numbers
New: none
Status: pending

# Lesson 5 · The build · Your predictions

Your five picks, which I will build exactly:

```
1  100 cases
2  the 18 real complaints plus 82 invented
3  block only on a fall of more than 2 points
4  gate every change that touches the instructions, nightly for the rest
5  a short-lived pass, no stored password
```

Two versions will run against your list. The version live today passes 92 of 100. The proposed change reworks the wording and breaks handwritten scans, turning 5 cases that used to pass into failures. A second, better change fixes 3 invoices that were failing and breaks nothing.

**Your call.** Predict five numbers:

1. The broken version's pass rate.
2. Under your rule from decision 3, is the broken change blocked or allowed?
3. The better change's pass rate.
4. Under your rule, is the better change blocked or allowed?
5. One run scores both versions over your list, at $0.0027 an AI call. What does one run cost?

### Key
1. 87%  2. blocked (a 5 point fall is more than 2)  3. 95%  4. allowed  5. $0.54 (200 calls)
What this gives up: with rule B a 2 point fall would pass unseen, and 82 invented cases inflate the 92.
