skill: llm
id: llm-03
level: 1
title: Same answer five times
scored: Pick and say why, New case
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/huyen-sampling-for-text-generation.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/anthropic-glossary.md
runs: runs/llm03-multiply-temp0.json, runs/llm03-multiply-first-digit.json, runs/llm01-multiply-true.json, runs/llm03-multiply2-temp0.json, runs/llm03-multiply2-true.json, runs/llm03-fruit-chances.json, runs/llm03-apple-total.json, runs/llm03-fruit-temperatures.json, runs/llm03-city-temperatures.json, runs/llm03-wrong-a-day.json, runs/llm03-cold-colour-chances.json, runs/llm03-cold-colour-temperatures.json
wrong idea: temperature 0 means the model is sure, so the answer is right and always the same

## Step: Odd result

given: the demo model is Qwen2.5-0.5B, a tiny free model with about 0.5 billion parts (numbers it learned in training), run on this Mac. Large models like Claude are far bigger, so some odd results are small-model effects that Claude rarely shows. This unit says which.

The tiny model was asked "What is 347 x 29? Reply with the number only." five times, with temperature (a setting that controls how the model picks from its chances) at 0. All five answers were **9503**. The true answer is 10063. (Getting the sum wrong is a small-model effect; the repeating is not.)

Before writing anything, the model gives a chance to every possible first piece of text:

| First piece | "9" | "8" | "3" | "1" |
|---|---|---|---|---|
| Model's chance | 94.5% | 5.1% | 0.2% | 0.1% |

Which first piece would have started the true answer, and what chance did the model give it?

**Your answer.**

### Key
"1", at 0.1%. The model gave its wrong first digit 94.5%, then wrote the same wrong answer every time. Not scored. Aim: he sees that repeating and a high chance did not make it right.

## Step: Pick and say why

Here is a second sum, also at temperature (the picking setting) 0: "What is 256 x 34?" came back as 8160 all five times. The true answer is 8704.

Why did the model give the same answer five times? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. At temperature 0 the model becomes certain, so it checks its work and settles on one answer.
B. At temperature 0 the model always takes its likeliest next piece; the same text gives the same chances, so the same pick, right or wrong.
C. The model remembers its first answer and repeats it to stay consistent.
D. 8160 is the number the model has stored for this sum, and temperature cannot change a stored fact.

**Your answer.**

### Key
B. A is the wrong idea this unit targets: nothing is checked, and the answer is wrong. C: each of the five was made fresh, with nothing carried over; they match because the same rule on the same chances gives the same pick. D brings back the lookup idea from the first unit: there is no stored answer, only chances for the next piece.
Score: 1 only if he picks B and his reason says temperature 0 means taking the likeliest piece each time (so it repeats, right or wrong); 0 otherwise. Record the confidence.
Skip rule: B, right reason, confidence 4 or 5: go straight to "New case".

## Step: Predict

New question: "Name one fruit. Answer with one word." The model's chances for the first piece: Apple 49.9%, App 23.4% (most likely the start of Apple too; together 73.3%), Orange 11.8%, Ban 4.4%. At temperature (the picking setting) 0, all 10 answers were Apple.

Now 10 answers at each of two higher temperatures, 0.7 and 1.5. Predict: how many different answers out of 10 at 0.7, and at 1.5? Will the answers at 1.5 all be real fruit?

**Your answer.**

### Key
He gives two numbers and a yes or no before seeing the run (runs/llm03-fruit-temperatures.json, shown next). Not scored.

## Step: Run

Real answers, 10 at each temperature (the picking setting):

| Temperature | Different answers | What came out |
|---|---|---|
| 0 | 1 | Apple, 10 times |
| 0.7 | 4 different strings, 2 different fruits | "Apple" 5 times, "Apple." 3 times, "Orange", "Apples." |
| 1.5 | 10 | "Apple", "apple", "Banana", "Grapes.", "anise.", "Itinerary", "roselogan.smile", "PearidueATIC_ES Compilation", "(apple) Hello there", "Grapes. Quint" |

Small-model effect: the amount of junk at 1.5. This tiny model was run with no cut-off (every piece, however rare, could be picked). Services usually cut off the rarest pieces, and large models spread their chances less, so there you would see more odd or off-topic answers, rarely this much nonsense. That variety grows with temperature is true of every model.

Compare with your prediction: how far off were you, and in which direction?

**Your answer.**

### Key
0: one answer. 0.7: still mostly Apple, 4 strings but only 2 fruits. 1.5: 10 different, and several are not fruit, or not even words. The point is his numbers against 4 and 10, and whether he expected the non-fruit. Not scored.

## Step: Explain

In one to three lines, in your own words: why does raising the temperature (the picking setting) give more different answers, including some that are not fruit?

**Your answer.**

### Key
Two sets of chances: the model's chances (fixed by the model and the text) and the picking chances (what temperature makes of them before one piece is picked). Low temperature makes the likeliest piece's picking chance even bigger (at 0 it is simply taken every time); high temperature evens them out, so rare pieces, including nonsense, get a real picking chance. The model's chances do not change. Chip Huyen (Sampling for text generation): temperature is used to "redistribute the probabilities of the possible values"; higher temperature makes output "more creative but potentially less coherent". Mark his answer: matches, partly (name the missing piece), or wrong. Not scored.
Simpler: The model gave Apple 49.9% and Orange 11.8%. At 0 it always takes the top one. At a high setting the picks are spread out more evenly, so small ones like "Itinerary" get picked sometimes. Why would that give more different answers?

## Step: Wrong idea fixed

**The wrong idea:** "At temperature (the picking setting) 0 the model is sure, so its answer is right, and it is always the same."

**Why it is wrong:** at 0, the tiny model gave 9503 five times for 347 x 29, with 94.5% on its wrong first digit. Same and confident, still wrong. And "always the same" holds only on this Mac, where 0 strictly means "take the top piece". On a provider's servers, Anthropic says: "Even with temperature set to 0, the results will not be fully deterministic".

**The right idea:** temperature changes the picking chances, not the model's chances, and not whether they are right. At 0 the model takes its likeliest piece; that usually repeats, but on a provider it is not guaranteed.

**What it costs:**
given: a tax assistant runs at temperature 0 and answers 1,000 questions a day. For 5% of askers, their wording makes a wrong rate the likeliest answer.
Work it out: how many wrong answers a day? Would testing that wording once, and seeing the same answer twice, catch the problem?

**Your answer.**

### Key
50 a day (1,000 x 5 / 100). Only if the answer is checked against the true rate: getting the same answer twice shows it repeats, not that it is right. Low temperature is still sensible for facts and numbers (fewer odd answers), but correctness comes from giving the model the right source and checking answers against known truth. And a test that compares exact text can fail at random on a provider even at 0, so check meaning, not exact wording. Not scored.
Simpler: Temperature 0 means "always take the top pick". If the top pick is wrong, you get the same wrong answer every time. So a repeated answer is not a checked answer. Now: 1,000 questions a day, 5% hit a wrong top pick. How many?

## Step: New case

A new situation. A travel app asked the tiny model "Name one city in Pakistan. Answer with one word." 10 times at temperature (the picking setting) 1.5. Answers included "Islamabad", "Lahore", "Quetta" run into junk, "Patiala." (a city in India), and "Jakarta Mexico" followed by Arabic words.

A colleague says: "Use 1.5, it makes the app more creative." Which is the best view? Pick one, give a one-line reason and a confidence from 1 to 5.

A. Good idea: a higher setting makes the model think harder, so its answers get better.
B. It makes no difference to what is said; the setting only changes the tone of the wording.
C. Fine for facts: the model's chances still point to Pakistani cities, so it will name only real Pakistani cities, just different ones.
D. Poor idea for facts: it raises the picking chances of rare pieces, so wrong or off-topic answers turn up more often.

**Your answer.**

### Key
D. A treats temperature as effort; nothing thinks harder. B: the run changed what was said, not just tone. C: the model's chances stay the same, but the picking chances of rare pieces rise, which is how India and Jakarta got in. The junk itself is extreme here (tiny model, no cut-off); with a large model expect more wrong or off-topic answers, not nonsense.
Score: 1 only if he picks D and his reason says a high setting gives rare pieces a bigger picking chance; 0 otherwise.

## Step: Close

Finish this line in your own words: "Next time I choose a temperature (the picking setting) for a feature, I will ..."

**Your answer.**

### Key
Something like: "... use a low one for facts and numbers, remember that low means the likeliest pick (usually repeated, not guaranteed, and not proof it is right), and check answers against the truth." His line goes into the recall queue. Not scored.

## Cold

A new case. Asked "Name one colour. Answer with one word.", the tiny model gave these chances for the first piece: Red 88.8%, Blue 8.4%, Yellow 1.2%. On this Mac at temperature (the picking setting) 0, all 10 answers were Red.

A developer builds the same feature on a provider's service, at 0, and writes a test that passes only if the exact text "Red" comes back on every call. Over many calls, what should she expect? Pick one, give a one-line reason and a confidence from 1 to 5.

A. Almost always "Red", but not guaranteed: at 0 the likeliest piece is taken, and on a provider's servers the same input can still give a different output, so an exact-text test can fail by chance.
B. Always "Red": at 0 the model is certain, so the output cannot change.
C. "Red" on the first call, then the same text every time, because the provider stores the first answer and sends it back.
D. A mix, with Red about 88.8% of the time, because 0 still picks by the model's chances.

**Your answer.**

### Key
A. B is the certainty idea; Anthropic: "Even with temperature set to 0, the results will not be fully deterministic". C invents a stored answer; each call is worked out fresh. D mixes up the two chances: 88.8% is the model's chance, but at 0 the picking chance of the top piece is all of it, so on this Mac Red came 10 of 10.
Score: 1 only if he picks A and his reason says 0 takes the likeliest piece but a provider does not guarantee identical output; 0 otherwise.

## Cards
- Q: What does temperature change? | A: The picking chances: how the model picks from its own chances for the next piece. Not the model's chances, and not whether they are right (source: Huyen, Sampling for text generation).
- Q: The tiny model answered 347 x 29 with 9503 five times at temperature 0; the truth is 10063. Is a repeated answer at temperature 0 proof it is right? | A: No. At 0 it takes the likeliest piece every time, so it repeats whatever is likeliest, right or wrong. || Q: The tiny model answered 256 x 34 with 8160 five times at temperature 0; the truth is 8704. Is a repeated answer at temperature 0 proof it is right? | A: No. At 0 it takes the likeliest piece every time, so it repeats whatever is likeliest, right or wrong.
- Q: Name one reason output at temperature 0 can still change between calls to a provider. | A: The provider does not guarantee identical output: Anthropic says results "will not be fully deterministic" even at 0 (small number differences on the servers can flip a close pick). || Q: Why can a test that checks for exact text fail at random, even at temperature 0, on a provider's service? | A: Identical inputs can give different outputs across calls (Anthropic glossary), so check meaning, not exact wording.
- Q: Asked to name a fruit 10 times at temperature 1.5, how many different answers did the tiny model give, and why? | A: 10, several not fruit: a high setting evens out the picking chances, so rare pieces get picked. || Q: Asked to name a city in Pakistan 10 times at temperature 1.5, the tiny model gave 9 different answers, including a city in India. Why? | A: A high setting evens out the picking chances, so rare, wrong pieces get picked.
- Q: The tiny model's chance for "Apple" as the first piece was 49.9%, yet at temperature 0 it answered Apple 10 times of 10. Which chances did temperature 0 change? | A: The picking chances (the top piece is always taken); the model's chances stayed the same. || Q: The tiny model gave its first digit "9" a 94.5% chance for 347 x 29, and at temperature 0 it answered 9503 every time. Did temperature 0 change the model's 94.5%? | A: No. It changed only the picking chances: the top piece is always taken.
