id: production-01
skill: production
shape: first-contact
class: C1 one-formula cost (node P1)
level: 1
title: What one AI call costs
scored: Quick set 1, Quick set 2
sources: facts.md
runs: runs/production-01-c1a.json, runs/production-01-c1b.json, runs/production-01-c1c.json, runs/production-01-c1d.json, runs/production-01-c2a.json, runs/production-01-c2b.json, runs/production-01-c2c.json, runs/production-01-c2d.json, runs/production-01-c4a.json, runs/production-01-c4b.json, runs/production-01-c4c.json, runs/production-01-c4d.json, runs/production-01-co-all.json, runs/production-01-co-call.json, runs/production-01-co-calls.json, runs/production-01-co-cap-out.json, runs/production-01-co-cap-save.json, runs/production-01-co-cut-call.json, runs/production-01-co-cut-in.json, runs/production-01-co-cut-save.json, runs/production-01-co-day.json, runs/production-01-co-haiku.json, runs/production-01-co-in.json, runs/production-01-co-inpart.json, runs/production-01-co-instr.json, runs/production-01-co-month.json, runs/production-01-co-outpart.json, runs/production-01-co-share.json, runs/production-01-h1-call.json, runs/production-01-h1-in.json, runs/production-01-h1-inpart.json, runs/production-01-h1-outpart.json, runs/production-01-h2-calls.json, runs/production-01-h2-month.json, runs/production-01-h2-rough.json, runs/production-01-h2-share.json, runs/production-01-h3-call.json, runs/production-01-h3-in.json, runs/production-01-h3-save.json, runs/production-01-h3-shirt.json, runs/production-01-h4-b-call.json, runs/production-01-h4-b-out.json, runs/production-01-h4-b-save.json, runs/production-01-h4-share-in.json, runs/production-01-h5-call.json, runs/production-01-h5-calls.json, runs/production-01-h5-cap-out.json, runs/production-01-h5-cap-save.json, runs/production-01-h5-in.json, runs/production-01-h5-inpart.json, runs/production-01-h5-month.json, runs/production-01-h5-outpart.json, runs/production-01-h5-share.json, runs/production-01-h6-call.json, runs/production-01-h6-cut-call.json, runs/production-01-h6-cut-save.json, runs/production-01-h6-inpart.json, runs/production-01-h6-outpart.json, runs/production-01-lev-a-month.json, runs/production-01-lev-b-call.json, runs/production-01-lev-b-month.json, runs/production-01-lev-b-save.json, runs/production-01-qs1-call.json, runs/production-01-qs1-calls.json, runs/production-01-qs1-cap.json, runs/production-01-qs1-haiku.json, runs/production-01-qs1-in.json, runs/production-01-qs1-inpart.json, runs/production-01-qs1-month.json, runs/production-01-qs1-outpart.json, runs/production-01-qs1-save.json, runs/production-01-qs1-share.json, runs/production-01-qs2-2000.json, runs/production-01-qs2-call.json, runs/production-01-qs2-cap-out.json, runs/production-01-qs2-cap-save.json, runs/production-01-qs2-doc-call.json, runs/production-01-qs2-doc-save.json, runs/production-01-qs2-inpart.json, runs/production-01-qs2-outpart.json, runs/production-01-qs2-share-in.json, runs/production-01-re-all.json, runs/production-01-re-call.json, runs/production-01-re-calls.json, runs/production-01-re-cap-out.json, runs/production-01-re-cap-save.json, runs/production-01-re-cut-call.json, runs/production-01-re-cut-in.json, runs/production-01-re-cut-save.json, runs/production-01-re-day.json, runs/production-01-re-haiku.json, runs/production-01-re-in.json, runs/production-01-re-inpart.json, runs/production-01-re-instr.json, runs/production-01-re-month.json, runs/production-01-re-outpart.json, runs/production-01-re-share.json, runs/production-01-ty1-call.json, runs/production-01-ty1-in.json, runs/production-01-ty1-inpart.json, runs/production-01-ty1-outpart.json, runs/production-01-ty1-wrong-tokens.json, runs/production-01-ty1-wrong.json, runs/production-01-ty2-calls.json, runs/production-01-ty2-instr.json, runs/production-01-ty2-month.json, runs/production-01-ty2-rough.json, runs/production-01-ty2-share.json, runs/production-01-ty3-call.json, runs/production-01-ty3-in.json, runs/production-01-ty3-save.json, runs/production-01-we1-call.json, runs/production-01-we1-code.json, runs/production-01-we1-in.json, runs/production-01-we1-inpart.json, runs/production-01-we1-outpart.json, runs/production-01-we1-ratio.json, runs/production-01-we1-rough-in.json, runs/production-01-we1-rough.json, runs/production-01-we1-rough2.json, runs/production-01-we1-wrong-tokens.json, runs/production-01-we1-wrong.json, runs/production-01-we2-1000.json, runs/production-01-we2-calls.json, runs/production-01-we2-day.json, runs/production-01-we2-instr.json, runs/production-01-we2-month.json, runs/production-01-we2-q.json, runs/production-01-we2-share-ans.json, runs/production-01-we2-share-instr.json, runs/production-01-we2-share-q.json, runs/production-01-we3-a-call.json, runs/production-01-we3-a-in.json, runs/production-01-we3-a-month.json, runs/production-01-we3-a-save.json, runs/production-01-we3-b-call.json, runs/production-01-we3-b-month.json, runs/production-01-we3-b-save.json, runs/production-01-we3-ratio.json
built from: docs/research/gap-audit-production.md sections 4 and 5 (sample production-01), in unit format v3

## Step: The job

**The job**

Suppose you are building a study helper for university students in Pakistan. Each time a student asks something, your app sends one call to Claude Sonnet 5, an AI model (the program that writes the answers).

Every call is made of three parts, all counted in tokens (a token is a small piece of text, often part of a word; the company that runs the model charges for every token):

- the fixed instructions: text that tells the model how to behave, the same on every call
- the student's question
- the answer the model writes back

The first two are **input**: what your app sends. The answer is **output**: what the model writes. Input and output have different prices, and prices are quoted per 1,000,000 tokens.

Why this matters: an app that looks cheap while you test it can cost more than it earns once many students use it every day, and you only find out when the bill arrives.

You will be able to: work out what one call costs, what one student costs in a month, and which part of the bill to cut first.

You are done when: you get 9 of 10 right on a short set at the end of this unit, and 9 of 10 again on a new set 7 days later.

One check on the words before we start: which of the three parts is output, and why?

**Your answer.**

### Key
Kind: show
New: a token is a charged piece of text; input vs output (the three parts of a call); separate prices quoted per 1000000 tokens
Not scored. Right: the answer, because the model writes it; the instructions and the question are sent by the app, so they are input. If wrong: point at the line "The answer is **output**: what the model writes".

## Step: Worked example 1

**Worked example 1: the cost of one call**

A picture first. A photocopy shop charges a little for each page you hand in and 5 times more for each page it prints for you. Hand in a thick stack and get back one printed page, and the stack can still cost you more than the page. (Where the picture stops: the shop counts pages, the model counts tokens.)

Suppose the study helper's fixed instructions are 6,000 tokens, a question is 500 tokens and an answer is 400 tokens.

**Which numbers, and why.** Input is everything you send: 6,000 + 500 = 6,500 tokens. Output is what comes back: 400 tokens. Sonnet 5's prices (Anthropic's price page, checked 2026-09-24): $2 per 1,000,000 input tokens, $10 per 1,000,000 output tokens.

**The rule.** cost of one call = input part + output part, and each part = tokens x price / 1,000,000. Dividing by 1,000,000 turns a price per 1,000,000 tokens into a price per token.

**Rough size first.** Round 6,500 up to 7,000: 7,000 x $2 / 1,000,000 = $0.014. Output: 400 x $10 / 1,000,000 = $0.004. Together about $0.02 a call.

**Now exactly.**
- input part: 6,500 x $2 / 1,000,000 = $0.013
- output part: 400 x $10 / 1,000,000 = $0.004
- one call: $0.013 + $0.004 = **$0.017** (close to the rough $0.02, so no slip)

**What it means.** An output token costs 5 times more, yet the input part ($0.013) is bigger than the output part ($0.004): the instructions are 15 times longer than the answer and go out on every call.

**Wrong turn (this is wrong):** pricing all 6,900 tokens at the input rate gives $0.0138. It treats the answer as if it cost $2 per 1,000,000, so the bill comes out too low.

Question: in one line, why is the 500-token question priced at $2 per 1,000,000 and not $10?

**Your answer.**

### Key
Kind: show
New: each part = tokens x price divided by 1000000; one call = input part + output part; a rough size before the exact number
Not scored (self-explanation on the key step). Right: the question is sent in by the app, so it is input and takes the input price. If wrong: point at "Input is everything you send".

## Step: Your turn 1

**Your turn: a homework helper**

Same shape, new app.

Suppose a homework helper on Sonnet 5 ($2 input, $10 output, per 1,000,000 tokens) sends 3,000 tokens of fixed instructions and a 200-token question, and gets back a 300-token answer.

The input part is done for you: 3,000 + 200 = 3,200 tokens, and 3,200 x $2 / 1,000,000 = $0.0064.

1. What is the output part?
2. What does one call cost?
3. A classmate priced all 3,500 tokens at $2 per 1,000,000 and got $0.007. Is his number too high or too low, and why?

**Your answer.**

### Key
Kind: try
1 = $0.003 (300 x $10 / 1,000,000). 2 = $0.0094 ($0.0064 + $0.003). 3 = too low: the 300 answer tokens cost $10 per 1,000,000, not $2. Not scored; aim: most of it right first try; count his first-try results for the tries line after Lever. Wrong twice: stuck order, then Help: Your turn 1.
Two options: 1: the 300 answer tokens take the input price ($2) or the output price ($10)? 2: add the two parts, or multiply them? 3: were his 300 answer tokens priced at their own price or at the cheaper input price?
Worked answer: 1: the answer is output, so 300 x $10 / 1,000,000 = $0.003. 2: one call = input part + output part = $0.0064 + $0.003 = $0.0094. 3: too low: he priced all 3,500 tokens at $2, so 3,500 x $2 / 1,000,000 = $0.007 treats the 300 answer tokens as input; they cost $10 per 1,000,000, so his number misses money.

## Step: Worked example 2

**Worked example 2: from one call to one student a month**

Back to the study helper at $0.017 a call.

Suppose a student asks 20 questions a day, every day for 30 days.

**Which numbers, and why.** A month's bill is the number of calls times the cost of one call. Calls in a month = calls a day x days: 20 x 30 = 600 calls.

- one student a month: 600 x $0.017 = **$10.20**
- 1,000 students a month: 1,000 x $10.20 = **$10,200**
- 1,000 students for one day: 1,000 x 20 x $0.017 = **$340** (leave out the days)

**Where the money goes in one call.** A share is one part divided by the whole call, written as a percent.

| Part | Cost | Share of the call |
|---|---|---|
| fixed instructions: 6,000 x $2 / 1,000,000 | $0.012 | $0.012 / $0.017 = 70.6% |
| answer: 400 x $10 / 1,000,000 | $0.004 | $0.004 / $0.017 = 23.5% |
| question: 500 x $2 / 1,000,000 | $0.001 | $0.001 / $0.017 = 5.9% |

The three shares add up to 100%.

**What it means.** Each extra student adds $10.20 a month, and 70.6% of it pays for the same instructions sent again and again.

The rule, last: monthly cost = cost of one call x calls a day x days x number of students.

Question: in one line, why does the monthly bill grow with the number of students while the shares in the table stay the same?

**Your answer.**

### Key
Kind: show
New: calls in a month = calls a day x days; the bill = cost of a call x number of calls; a share = one part divided by the whole call
Not scored. Right: every call has the same three parts in the same sizes, so more calls multiply every part by the same number. If wrong: point at the table, which is about one call.

## Step: Your turn 2

**Your turn: the homework helper, a month**

The homework helper costs $0.0094 a call (your answer in the last step).

Suppose a student uses it 10 times a day for 30 days.

1. Rough size first, as in the worked example: round $0.0094 to $0.01. Roughly what does one student cost a month?
2. Now exactly: what does one student cost a month?
3. The fixed instructions cost $0.006 of each call (3,000 x $2 / 1,000,000). What share of the call is that?

**Your answer.**

### Key
Kind: try
1 = about $3 (300 calls x $0.01). 2 = $2.82 (300 x $0.0094). 3 = 63.8% ($0.006 / $0.0094). Not scored; aim: most of it right first try; count his first-try results. Wrong twice: stuck order, then Help: Your turn 2.
Two options: 1: 300 calls x $0.01, or 10 calls x $0.01? 2: 300 x $0.0094, or 30 x $0.0094? 3: $0.006 / $0.0094, or $0.0094 / $0.006?
Worked answer: 1: calls in a month = 10 x 30 = 300; 300 x $0.01 = about $3. 2: 300 x $0.0094 = $2.82, close to the rough $3, so no slip. 3: a share is the part divided by the whole call: $0.006 / $0.0094 = 63.8%.

## Step: Worked example 3

**Worked example 3: what a number means**

Two ideas to cut the study helper's $0.017 call:
(a) cut the fixed instructions in half, to 3,000 tokens
(b) cap every answer at 200 tokens (tell the model to stop by 200)

**A saving is before minus after.** Work out the new cost of a call, then subtract it from the old one.

| Idea | Call after | Saving per call (before minus after) | Per student a month (x 600 calls) |
|---|---|---|---|
| (a) | $0.011 | $0.017 - $0.011 = **$0.006** | $3.60 |
| (b) | $0.015 | $0.017 - $0.015 = **$0.002** | $1.20 |

(a): input is 3,000 + 500 = 3,500 tokens; 3,500 x $2 / 1,000,000 = $0.007, plus the $0.004 output = $0.011.
(b): input stays $0.013; output becomes 200 x $10 / 1,000,000 = $0.002; total $0.015.

**Wrong turn (this is wrong):** "cut (a) saves $0.011". That is the cost of a call after the cut, only one side. A saving needs both sides.

**What it means.** Cut (a) saves 3 times as much as (b), because it shrinks the biggest share of the call (70.6%). Look at the biggest share first.

**Which way does an unsure number bend the bill?** The 400-token answers were measured in a test week when students asked short questions. If real answers run longer, the true bill is **higher** than $10.20 a month; if they run shorter, it is **lower**. More tokens than you counted can only add cost; fewer can only remove it.

Question: in one line, why is cut (a)'s saving $0.006 and not $0.011?

**Your answer.**

### Key
Kind: show
New: saving = before minus after, the biggest share is where to cut first, which way an unsure token count bends the bill
Not scored. Right: $0.011 is what a call costs after the cut; the saving is the gap from $0.017. If wrong: point at the table's "before minus after" column.

## Step: Your turn 3

**Your turn: what the numbers mean**

The homework helper costs $0.0094 a call and $2.82 per student a month.

1. Suppose its fixed instructions drop from 3,000 to 1,500 tokens. A call then costs $0.0064. What is the saving per call?
2. A teammate says that cut "saves $0.0064 a call". Right or wrong, and what did they work out?
3. The 300-token answers were measured on easy homework. Harder homework gets longer answers. Is the true monthly bill higher or lower than $2.82?

**Your answer.**

### Key
Kind: try
1 = $0.003 ($0.0094 - $0.0064, before minus after). 2 = wrong: $0.0064 is the cost of a call after the cut; the saving is $0.003. 3 = higher. Not scored; count his first-try results. Wrong twice: stuck order, then Help: Your turn 3.
Two options: 1: $0.0094 - $0.0064, or $0.0064 on its own? 2: is $0.0064 what a call costs after the cut, or the gap between before and after? 3: longer answers are more output tokens: do more tokens add cost or remove it?
Worked answer: 1: a saving is before minus after: $0.0094 - $0.0064 = $0.003. 2: wrong: $0.0064 is what a call costs after the cut, only one side; the saving is $0.003. 3: higher: longer answers are more output tokens at $10 per 1,000,000, and more tokens than you counted can only add cost.

## Step: Lever

**Lever: pick one cut**

A lever is the one change that moves the bill the most. You can make one of these two cuts to the homework helper this week; each takes a day of work.

| Cut | Call after | Saving per call | Saving per student a month (x 300 calls) | What it risks |
|---|---|---|---|---|
| A. instructions from 3,000 to 1,500 tokens | $0.0064 | $0.003 | $0.90 | the model may follow your rules less closely |
| B. answers capped at 150 tokens | $0.0079 | $0.0015 | $0.45 | long explanations get cut off |

The last column matters too. A cost number compares cuts that keep the answers equally good; it cannot tell you the answers are still good.

Which cut do you make first, A or B? Give the one number that decides it, and the share you worked out earlier that explains why.

**Your answer.**

### Key
Kind: try
A. Deciding number: the saving per call, $0.003 against $0.0015 (twice as much). Why: the fixed instructions are the biggest share of the call, 63.8%. Not scored. Wrong twice: stuck order, then Help: Lever.
Two options: is the deciding number the saving per call, or the cost of a call after the cut? Is the biggest share of the call the fixed instructions or the answer?
Worked answer: Cut A. It saves $0.003 a call against $0.0015 for B, twice as much ($0.90 against $0.45 per student a month). It wins because the fixed instructions are the biggest share of the call, 63.8%, so cutting them moves the most money.
After this step, record the try steps (Your turn 1 to 3 and Lever, 10 answers): engine.py tries production-01 <right first try> 10. Under 7 right: slow down and use the Help blocks before the Quick set.

## Step: Quick set 1

**Short set, part 1 of 2.** Work these alone. Give each answer as a number with its unit ($ or %). Keep a call's cost exact; round a share to 1 decimal place and a month's bill to the cent. If you are stuck on one, say so: a right answer after a hint counts half.

Prices per 1,000,000 tokens: Sonnet 5 $2 input, $10 output. Haiku 4.5 (a smaller, cheaper Claude model) $1 input, $5 output.

Suppose a tutor bot on Sonnet 5 sends 4,000 tokens of fixed instructions and a 100-token question, and gets back a 500-token answer. Each student uses it 15 times a day for 30 days.

1. What does one call cost?
2. What does one student cost a month?
3. What share of each call is the answer?
4. If answers are capped at 250 tokens, what is the saving per call?
5. What would one call cost if the same bot ran on Haiku 4.5?

**Your answer.**

### Key
Kind: scored
Score: (items right) / 5, his first reply only; a right number with a wrong or missing unit counts wrong; a share to 1 decimal place or to the nearest whole percent counts right; a month's or a day's bill rounded to the cent counts right; a right answer after the Two options hint counts half; after the Worked answer, 0.
1 = $0.0132. 2 = $5.94 (450 calls). 3 = 37.9%. 4 = $0.0025 (the answer part falls from $0.005 to $0.0025). 5 = $0.0066.
Meaning items: 3, 4.
Two options: (only the item he says he is stuck on) 1: is the 100-token question input or output? 2: 450 calls x the cost of one call, or 15 calls x it? 3: the answer part divided by the whole call, or the whole call divided by the answer part? 4: the answer part before minus after the cap, or the new answer part on its own? 5: halve both prices, or halve only the output price?
Worked answer: 1: input 4,100 x $2 / 1,000,000 = $0.0082; output 500 x $10 / 1,000,000 = $0.005; one call $0.0132. 2: 15 x 30 = 450 calls; 450 x $0.0132 = $5.94. 3: $0.005 / $0.0132 = 37.9%. 4: the answer part falls from $0.005 to $0.0025; before minus after = $0.0025. 5: 4,100 x $1 / 1,000,000 + 500 x $5 / 1,000,000 = $0.0066.

## Step: Quick set 2

**Solutions, part 1**
1. Input 4,000 + 100 = 4,100 tokens: 4,100 x $2 / 1,000,000 = $0.0082. Output 500 x $10 / 1,000,000 = $0.005. One call **$0.0132**.
2. 15 x 30 = 450 calls; 450 x $0.0132 = **$5.94**.
3. $0.005 / $0.0132 = **37.9%**.
4. The answer part falls from $0.005 to $0.0025 (250 x $10 / 1,000,000). Before minus after: **$0.0025**.
5. 4,100 x $1 / 1,000,000 + 500 x $5 / 1,000,000 = **$0.0066**: half the Sonnet 5 cost, because both Haiku prices are half.

**Short set, part 2 of 2.**

Suppose a summariser (an app that shortens a document) on Haiku 4.5 reads a 20,000-token document and writes a 300-token summary.

6. What does one call cost?
7. Which saves more per call: sending only the 10,000 tokens of the document that matter, or capping the summary at 150 tokens? Give both savings.
8. A teammate says sending 10,000 tokens "saves $0.0115 a call". Right or wrong, and what did they work out?

Back to the tutor bot from part 1 ($5.94 per student a month):

9. Its 500-token answers were measured while testers asked for long, detailed answers. Real students want short ones. Is the true bill higher or lower than $5.94?
10. With 2,000 students, what is the monthly bill?

**Your answer.**

### Key
Kind: scored
Score: (items right) / 5, his first reply only; a right number with a wrong or missing unit counts wrong; a month's bill rounded to the cent counts right; a right answer after the Two options hint counts half; after the Worked answer, 0.
6 = $0.0215. 7 = the document: saves $0.01; the summary cap saves $0.00075 (both savings needed). 8 = wrong: $0.0115 is the cost after the cut; the saving is $0.01. 9 = lower. 10 = $11,880.
Meaning items: 7, 8, 9. Across both halves, 5 of 10 items are about what a number means.
Two options: (only the item he says he is stuck on) 6: the document at $1 and the summary at $5, or both at $1? 7: each saving as before minus after, or each new call cost? 8: is $0.0115 the cost of a call after the cut, or the gap between before and after? 9: shorter answers are fewer tokens: do fewer tokens add cost or remove it? 10: 2,000 x $5.94, or 2,000 x $0.0132?
Worked answer: 6: 20,000 x $1 / 1,000,000 + 300 x $5 / 1,000,000 = $0.02 + $0.0015 = $0.0215. 7: document $0.0215 - $0.0115 = $0.01; summary cap: the output part falls from $0.0015 to $0.00075, saving $0.00075; the document cut saves more. 8: wrong: $0.0115 is the cost after the cut; before minus after is $0.0215 - $0.0115 = $0.01. 9: lower: fewer tokens than you counted can only remove cost. 10: 2,000 x $5.94 = $11,880.

## Step: Close

**Solutions, part 2**
6. 20,000 x $1 / 1,000,000 + 300 x $5 / 1,000,000 = $0.02 + $0.0015 = **$0.0215**.
7. Document: $0.0215 - $0.0115 = **$0.01**. Summary cap: the output part falls from $0.0015 to $0.00075, a saving of **$0.00075**. The input is 93% of this call, so it is the lever.
8. **Wrong.** $0.0115 is the cost after the cut. Before minus after: $0.0215 - $0.0115 = $0.01.
9. **Lower.** Fewer tokens than you counted can only remove cost.
10. 2,000 x $5.94 = **$11,880**.

**Close**

Finish this line in your own words: "Next time I see an AI bill, I first ..."

**Your answer.**

### Key
Kind: close
Not scored. Any line naming a real move: price input and output separately; find the biggest share; a saving is before minus after. Record with engine.py close production-01 "<his line>".

## Help: Your turn 1

**One call, another app**

Suppose a translation app on Haiku 4.5 ($1 input, $5 output, per 1,000,000 tokens) sends 1,000 tokens of fixed instructions plus a 1,000-token text, and writes a 1,200-token translation.

- Input is everything sent: 1,000 + 1,000 = 2,000 tokens. 2,000 x $1 / 1,000,000 = $0.002.
- Output is what the model writes: 1,200 x $5 / 1,000,000 = $0.006.
- One call: $0.002 + $0.006 = **$0.008**.

Each part uses its own price: sent tokens at the input price, written tokens at the output price. Here the output part is the bigger one, because the translation is long.

Now your homework helper: its answer is 300 tokens at $10 per 1,000,000. What is the output part?

**Your answer.**

### Key
Kind: show
New: -
$0.003 (300 x $10 / 1,000,000). Then send Your turn 1 again, whole and verbatim, so he answers all three questions.

## Help: Your turn 2

**From a call to a month, another app**

The translation app costs $0.008 a call.

Suppose a user translates 5 times a day for 30 days.

- Calls in a month = calls a day x days: 5 x 30 = 150.
- Rough size first: $0.008 is close to $0.01, so about 150 x $0.01 = $1.50.
- Exactly: 150 x $0.008 = **$1.20** a month.
- Share of the output part: $0.006 / $0.008 = **75%** of each call.

Now your homework helper, used 10 times a day for 30 days: how many calls is that in a month, and what do you multiply that number by to get the monthly cost?

**Your answer.**

### Key
Kind: show
New: -
300 calls, multiplied by the cost of one call ($0.0094). Then send Your turn 2 again, whole and verbatim.

## Help: Your turn 3

**A saving, and which way a number bends**

A picture: a shirt marked Rs 1,500 is on sale for Rs 1,200. You saved Rs 300: before minus after. Rs 1,200 is what you pay, not what you saved.

Same with a call. Suppose the translation app ($0.008 a call) cuts its instructions from 1,000 to 500 tokens. Input becomes 500 + 1,000 = 1,500 tokens, so a call costs 1,500 x $1 / 1,000,000 + $0.006 = $0.0075. Saving: $0.008 - $0.0075 = **$0.0005**. Saying "it saves $0.0075" is the one-side slip.

Which way does an unsure number bend the bill? The 1,200-token translations were measured on short news items. If users send long contracts, translations run longer: more tokens, so the true bill is **higher**. Shorter texts would make it **lower**.

Now your homework helper: before the cut a call costs $0.0094, after it $0.0064. Which one is the saving: $0.0064, or $0.0094 - $0.0064?

**Your answer.**

### Key
Kind: show
New: -
$0.0094 - $0.0064 = $0.003. Then send Your turn 3 again, whole and verbatim.

## Help: Lever

**The lever is the biggest share of that app**

The translation app costs $0.008 a call: the input part is $0.002 (25%) and the output part $0.006 (75%). Two cuts:

| Cut | Call after | Saving per call |
|---|---|---|
| A. instructions from 1,000 to 500 tokens | $0.0075 | $0.0005 |
| B. translations without extra notes, 1,200 to 900 tokens | $0.0065 | $0.0015 |

B saves 3 times as much, because output is the biggest share here. So the lever is not always the instructions: it is whichever part is the biggest share of that app's call.

Now your homework helper: which part is the biggest share of its call, and so which cut saves more?

**Your answer.**

### Key
Kind: show
New: -
The fixed instructions (63.8%), so cut A. Then send Lever again, whole and verbatim.

## Help: Quick set 1

**The whole chain on another app**

Suppose a CV checker on Sonnet 5 sends 2,500 tokens of fixed instructions and a 1,500-token CV, and writes a 200-token answer. A user runs it 5 times a day for 30 days.

1. Input 2,500 + 1,500 = 4,000 tokens: 4,000 x $2 / 1,000,000 = $0.008. Output 200 x $10 / 1,000,000 = $0.002. One call: **$0.01**.
2. 5 x 30 = 150 calls; 150 x $0.01 = **$1.50** a month.
3. Share of the answer: $0.002 / $0.01 = **20%**.
4. Cap answers at 100 tokens: the output part falls from $0.002 to $0.001 (100 x $10 / 1,000,000). Before minus after: **$0.001** saved.
5. On Haiku 4.5 both prices are half: $0.004 + $0.001 = **$0.005**.

Now take an item you missed in part 1 and work it the same way, one line per step.

**Your answer.**

### Key
Kind: show
New: -
He reworks the missed item line by line; compare with Solutions, part 1. Sent at the retry (SKILL step 5), before the Retry item.

## Help: Quick set 2

**Savings and direction, another app**

Suppose an email sorter on Haiku 4.5 reads an 8,000-token email thread and writes a 100-token label.

- One call: 8,000 x $1 / 1,000,000 + 100 x $5 / 1,000,000 = $0.008 + $0.0005 = **$0.0085**.
- Send only the last 4,000 tokens: $0.004 + $0.0005 = $0.0045. Saving, before minus after: $0.0085 - $0.0045 = **$0.004**. "It saves $0.0045" would be the new cost: the one-side slip.
- The input is most of this call, so cutting input is the lever; trimming the 100-token label would save almost nothing.
- Which way: the 100-token labels were measured while testers asked for a reason with each label. Real users want the label only: fewer tokens, so the true bill is **lower**.

Now take an item you missed in part 2 and work it the same way.

**Your answer.**

### Key
Kind: show
New: -
He reworks the missed item; compare with Solutions, part 2. Sent at the retry, before the Retry item.

## Retry

**Another short set, part 1 of 2** (5 items now, 5 in the next message). Give each answer as a number with its unit, or the word asked for. Keep a call's cost exact; round a share to 1 decimal place and a bill to the cent.

Prices per 1,000,000 tokens: Sonnet 5 $2 input, $10 output; Haiku 4.5 $1 input, $5 output.

Suppose an FAQ bot (it answers common questions about a university's admissions) on Sonnet 5 sends 2,000 tokens of fixed instructions and a 200-token question, and writes a 250-token answer. Each user asks 12 times a day for 30 days. You have 300 users.

1. Cost of one call?
2. Cost of one user a month?
3. All 300 users for a month?
4. What share of a call is the fixed instructions?
5. Cutting the instructions to 1,000 tokens saves how much per call?

**Your answer.**

### Key
Kind: scored
Score: (items right) out of 10 across Retry and Retry 2, his first reply only; a right number with a wrong or missing unit counts wrong; a share to 1 decimal place or to the nearest whole percent counts right; a bill rounded to the cent counts right. Pass 9 of 10. Mark after Retry 2, then record once: engine.py done production-01 --step "Retry=<right divided by 10>" --retry.
1 = $0.0069. 2 = $2.484 (360 calls; $2.48 accepted). 3 = $745.20. 4 = 58.0% (58% accepted). 5 = $0.002 (a call becomes $0.0049).
Meaning items: 4, 5.
Worked answer (after marking, for each missed item): 1: input 2,000 + 200 = 2,200 tokens, 2,200 x $2 / 1,000,000 = $0.0044; output 250 x $10 / 1,000,000 = $0.0025; one call $0.0069. 2: 12 x 30 = 360 calls; 360 x $0.0069 = $2.484. 3: 300 x 360 x $0.0069 = $745.20. 4: 2,000 x $2 / 1,000,000 = $0.004; $0.004 / $0.0069 = 58.0%. 5: input 1,000 + 200 = 1,200 tokens; 1,200 x $2 / 1,000,000 + $0.0025 = $0.0049; before minus after $0.0069 - $0.0049 = $0.002.

## Retry 2

**Another short set, part 2 of 2.** Same FAQ bot as part 1: Sonnet 5, 2,000 tokens of fixed instructions, a 200-token question, a 250-token answer; 12 calls a day for 30 days; 300 users.

6. A teammate says cutting the instructions to 1,000 tokens "saves $0.0049 a call". Right or wrong, and what did they work out?
7. Cost of one call on Haiku 4.5?
8. Which saves more per call: answers capped at 125 tokens, or instructions cut to 1,000? Give both savings.
9. The 2,000 instruction tokens were counted before you added three new rules to them. Is the true bill higher or lower than your answer to 3?
10. What do all 300 users cost in one day?

**Your answer.**

### Key
Kind: scored
Score: (items right) out of 10 across Retry and Retry 2, as in the Retry Key; record once, now: engine.py done production-01 --step "Retry=<right divided by 10>" --retry.
6 = wrong: $0.0049 is the cost after the cut; the saving is $0.002. 7 = $0.00345. 8 = the instructions cut: $0.002 against $0.00125 for the cap. 9 = higher. 10 = $24.84.
Meaning items: 6, 8, 9. Across both parts, 5 of 10 items are about what a number means.
Worked answer (after marking, for each missed item): 6: wrong: $0.0049 is what a call costs after the cut, only one side; before minus after is $0.0069 - $0.0049 = $0.002. 7: 2,200 x $1 / 1,000,000 + 250 x $5 / 1,000,000 = $0.00345. 8: the cap takes the output part from $0.0025 to $0.00125, saving $0.00125; the instructions cut saves $0.002, so it wins. 9: higher: more tokens than you counted can only add cost. 10: 300 x 12 x $0.0069 = $24.84.

## Cold

**Cold check, part 1 of 2** (5 items now, 5 in the next message). Give each answer as a number with its unit, or the word asked for. Keep a call's cost exact; round a share to 1 decimal place and a bill to the cent.

Prices per 1,000,000 tokens: Sonnet 5 $2 input, $10 output; Haiku 4.5 $1 input, $5 output.

Suppose your FBR tax assistant (it answers questions about Pakistan's income tax) runs on Sonnet 5. It sends 5,000 tokens of fixed instructions and a 300-token question, and writes a 600-token answer. Each user asks 8 times a day for 30 days. You have 500 users.

1. Cost of one call?
2. Cost of one user a month?
3. All 500 users for a month?
4. What share of a call is the fixed instructions?
5. Cutting the instructions to 2,500 tokens saves how much per call?

**Your answer.**

### Key
Kind: scored
Score: (items right) out of 10 across Cold and Cold 2, his first reply only; a right number with a wrong or missing unit counts wrong; a share to 1 decimal place or to the nearest whole percent counts right; a bill rounded to the cent counts right. Pass 9 of 10. Predict before this part (engine.py predict production-01 P --cold); mark after Cold 2, then record once: engine.py done production-01 --step "Cold=<right divided by 10>" --cold.
1 = $0.0166. 2 = $3.984 (240 calls; $3.98 accepted). 3 = $1,992. 4 = 60.2%. 5 = $0.005 (a call becomes $0.0116).
Meaning items: 4, 5.
Worked answer (after marking, for each missed item): 1: input 5,000 + 300 = 5,300 tokens, 5,300 x $2 / 1,000,000 = $0.0106; output 600 x $10 / 1,000,000 = $0.006; one call $0.0166. 2: 8 x 30 = 240 calls; 240 x $0.0166 = $3.984. 3: 500 x 240 x $0.0166 = $1,992. 4: 5,000 x $2 / 1,000,000 = $0.01; $0.01 / $0.0166 = 60.2%. 5: input 2,500 + 300 = 2,800 tokens; 2,800 x $2 / 1,000,000 + $0.006 = $0.0116; before minus after $0.0166 - $0.0116 = $0.005.

## Cold 2

**Cold check, part 2 of 2.** Same FBR tax assistant as part 1: Sonnet 5, 5,000 tokens of fixed instructions, a 300-token question, a 600-token answer; 8 calls a day for 30 days; 500 users.

6. A teammate says cutting the instructions to 2,500 tokens "saves $0.0116 a call". Right or wrong, and what did they work out?
7. Cost of one call on Haiku 4.5?
8. The 600-token answers were measured on simple salary questions. Real users also ask about businesses and property, which get longer answers. Is the true bill higher or lower than your answer to 3?
9. Which saves more per call: answers capped at 300 tokens, or instructions cut to 2,500? Give both savings.
10. What do all 500 users cost in one day?

**Your answer.**

### Key
Kind: scored
Score: (items right) out of 10 across Cold and Cold 2, as in the Cold Key; record once, now: engine.py done production-01 --step "Cold=<right divided by 10>" --cold.
6 = wrong: $0.0116 is the cost after the cut; the saving is $0.005. 7 = $0.0083. 8 = higher. 9 = the instructions cut: $0.005 against $0.003 for the cap. 10 = $66.40.
Meaning items: 6, 8, 9. Across both parts, 5 of 10 items are about what a number means.
Worked answer (after marking, for each missed item): 6: wrong: $0.0116 is what a call costs after the cut, only one side; before minus after is $0.0166 - $0.0116 = $0.005. 7: 5,300 x $1 / 1,000,000 + 600 x $5 / 1,000,000 = $0.0083. 8: higher: longer answers are more output tokens, and more tokens than you counted can only add cost. 9: the cap takes the output part from $0.006 to $0.003, saving $0.003; the instructions cut saves $0.005, so it wins. 10: 500 x 8 x $0.0166 = $66.40.

## Cards

- Q: Sonnet 5 ($2 in, $10 out per 1,000,000 tokens), 5,000 tokens in, 200 out: cost of a call? | A: $0.012 || Q: Haiku 4.5 ($1 in, $5 out per 1,000,000 tokens), 8,000 in, 400 out: cost of a call? | A: $0.01 || Q: Sonnet 5, 1,000 in, 1,000 out: cost of a call? | A: $0.012 || Q: Haiku 4.5, 2,000 in, 100 out: cost of a call? | A: $0.0025
- Q: A cut takes a call from $0.02 to $0.014. Saving per call? | A: $0.006 (before minus after) || Q: A cut takes a call from $0.05 to $0.035. Saving per call? | A: $0.015 || Q: A cut takes a call from $0.009 to $0.006. Saving per call? | A: $0.003 || Q: A cut takes a call from $0.12 to $0.09. Saving per call? | A: $0.03
- Q: A call costs $0.02; its instructions cost $0.015. Their share? | A: 75% || Q: A call costs $0.01; its answer costs $0.004. The answer's share? | A: 40% || Q: A call costs $0.012; its question costs $0.003. The question's share? | A: 25% || Q: A call costs $0.018; its instructions cost $0.009. Their share? | A: 50%
- Q: Answer length was measured on easy questions; real ones are harder. Is the true bill higher or lower? | A: higher (more tokens only add cost) || Q: The instructions were counted before you added two rules. Higher or lower? | A: higher || Q: Answers were measured while testers asked for detail; real users want short replies. Higher or lower? | A: lower || Q: You priced every token at the input rate. Is your number too high or too low? | A: too low (output costs more per token)
