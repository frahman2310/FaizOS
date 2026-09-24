skill: llm
id: llm-03
level: 1
title: Temperature reshapes the chances; it does not make the model sure
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/huyen-sampling-for-text-generation.md
runs: runs/llm03-fruit-chances.json, runs/llm03-fruit-temperatures.json, runs/llm03-city-temperatures.json, runs/llm03-multiply-temp0.json, runs/llm01-multiply-true.json
wrong idea: temperature 0 means the model is certain, so the answer is right

## Step: Odd result

The small Qwen model on this Mac was asked: "Name one fruit. Answer with one word." Before it writes anything, it gives a chance to every possible first piece. Its top four, real output:

| First piece | Apple | Orange | App | Ban |
|---|---|---|---|---|
| Model's chance | 23.3% | 12.6% | 8.8% | 5.0% |

Then it was asked the same thing 10 times with temperature set to 0. Temperature is a dial that controls how the model picks from those chances. All 10 answers were **Apple**.

A 23.3% favourite won 10 times out of 10. What is the first thing that strikes you?

**Your answer.**

### Key
Any honest observation. Aim: he notices that "Apple" was far from certain (under a quarter), yet temperature 0 gave it every time, so "always the same" did not mean "sure".

## Step: Pick and say why

Why did temperature 0 give "Apple" every time when its chance was only 23.3%? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. At temperature 0 the model becomes certain that Apple is the right answer.
B. At temperature 0 the model reuses its first answer for the next nine.
C. Apple is the most correct fruit, so a careful setting finds it every time.
D. At temperature 0 the model always takes the single likeliest piece, however small its lead.

**Your answer.**

### Key
D. A is the wrong idea this unit targets: the chances did not change, Apple stayed at 23.3%; only the picking rule changed. B is a fair guess, but each of the 10 answers was made fresh; they match because the same rule on the same chances gives the same pick. C: there is no "most correct" fruit; Orange was a fine answer at 12.6%. Record answer, reason, confidence. If D, right reason, confidence 4 or 5: skip to "New case".

## Step: Predict

The same question, 10 answers at each of two higher temperatures: 0.7 and 1.5.

Predict: how many different answers out of 10 at 0.7, and how many at 1.5? And will the answers at 1.5 all be real fruit?

**Your answer.**

### Key
He commits two numbers and a yes or no before the run. The run was captured before the session (runs/llm03-fruit-temperatures.json) and is shown in the next step.

## Step: Run

Real answers, 10 at each temperature:

| Temperature | Different answers | What came out |
|---|---|---|
| 0 | 1 | Apple, 10 times |
| 0.7 | 4 | "Apple" 5 times, "Apple." 3 times, "Orange", "Apples." |
| 1.5 | 10 | "Apple", "apple", "Banana", "Grapes.", "anise.", "Itinerary", "roselogan.smile", "PearidueATIC_ES Compilation", "(apple) Hello there", "Grapes. Quint" |

At 1.5 every answer was different, and several are not fruit at all, or not even words.

Compare with your prediction: how far off were you, and in which direction?

**Your answer.**

### Key
Temperature 0: one answer. 0.7: still mostly Apple, 4 different. 1.5: 10 different, and about half are broken. The point is his committed numbers against 4 and 10, and whether he expected the junk.

## Step: Explain

In one to three lines, in your own words: why does raising the temperature give more different answers, including junk?

**Your answer.**

### Key
Temperature reshapes the chances before one is picked. Low temperature makes the likeliest piece even likelier (at 0 it is simply taken every time); high temperature flattens the chances, so rare pieces, including nonsense ones, get a real chance of being picked. Chip Huyen (Sampling for text generation): higher temperature makes outputs "more creative but potentially less coherent"; at 0, "the model just picks the token" with the highest score. Mark his answer: matches, partly (name the missing piece), or wrong.

## Step: Wrong idea fixed

**The wrong idea:** "Temperature 0 means the model is certain, so its answer is right."

**Why it is wrong:** in your run, Apple won 10 out of 10 at temperature 0 with only a 23.3% chance. And asked "What is 347 x 29?" five times at temperature 0, the model answered 9503 every time. The right answer is 10063.

**The right idea:** temperature changes how the model picks from its chances, not how right the chances are. Temperature 0 gives the same answer each time, and the same wrong answer if the likeliest piece is wrong.

**What it costs:** given: a tax assistant runs at temperature 0 and answers 1,000 questions a day.
If its likeliest answer to one common wording is a wrong rate, every user who asks that way gets the same wrong rate, and it looks consistent, so nobody notices. Would testing that question once catch the problem?

**Your answer.**

### Key
Only if the one answer is checked against the true rate. Getting the same answer twice proves consistency, not correctness. Low temperature is still sensible for facts and numbers (fewer junk answers), but correctness comes from giving the model the right source and testing answers against known truth.

## Step: New case

A new situation, same idea. A travel app asked the model "Name one city in Pakistan. Answer with one word." 10 times at temperature 1.5. Real answers included "Islamabad", "Lahore", "Quetta" run into junk, "Patiala." (a city in India), and "Jakarta Mexico" followed by Arabic words.

A colleague says: "Use temperature 1.5, it makes the app more creative." Which is the better view? Pick, give a reason and a confidence 1 to 5.

A. Higher temperature gives more variety, but the extra variety includes wrong and broken answers, because rare pieces get a real chance.
B. Higher temperature makes the model more imaginative, so it will name more real cities.

**Your answer.**

### Key
A. "Creative" here means less likely picks, and less likely picks include wrong countries and junk. B assumes the extra variety is good variety. Score answer and reason separately.

## Step: Close

Finish this line in your own words: "Next time I choose a temperature for a feature, I will ..."

**Your answer.**

### Key
Something like: "... use a low one for facts and numbers, remember that low means repeatable, not right, and check answers against the truth." His line goes into the recall queue.

## Cards
- Q: What does temperature change? | A: How the model picks from its chances for the next piece, not how right those chances are.
- Q: What does the model do at temperature 0? | A: Always takes the single likeliest next piece, so the same question gives the same answer.
- Q: Does temperature 0 mean the model is certain or right? | A: No. The Qwen run picked Apple at a 23.3% chance every time, and gave 9503 for 347 x 29 every time (not "temperature 0 means right").
- Q: What happens to the chances at high temperature? | A: They flatten, so rare pieces, including wrong and broken ones, get picked more often.
- Q: Why is a repeated answer at temperature 0 not proof it is correct? | A: The same picking rule on the same chances repeats whatever is likeliest, wrong or right.
