skill: llm
id: llm-01
level: 1
title: Capital of Pakistan
scored: Pick and say why, New case
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-deep-dive-into-llms-like-chatgpt-transcript.md
runs: runs/llm01-capital-plain.json, runs/llm01-capital-question.json, runs/llm01-capital-friend.json, runs/llm01-multiply-model.json, runs/llm01-multiply-true.json, runs/llm01-multiply2-model.json, runs/llm01-multiply2-true.json, runs/llm01-at-risk.json, runs/llm01-cold-australia-plain.json, runs/llm01-cold-australia-question.json
wrong idea: the model searches a store of facts and returns the answer

## Step: Odd result

given: the demo model is Qwen2.5-0.5B, a tiny free model with about 0.5 billion parts (numbers it learned in training), run on this Mac. Large models like Claude are far bigger, so some odd results in these units are small-model effects that Claude rarely shows. Each unit says which ones.

The model was given the start of a sentence as plain text, with no chat around it, so it simply carries on the text. For every possible next piece of text (a token: a word or part of a word; the next unit is about these), it gives a chance. Its top five, real output:

| The model was given | Top next pieces, with the model's chance for each |
|---|---|
| "The capital of Pakistan is" | located 21.9%, Lahore 8.1%, ______ 6.0% (a blank line, as in a fill-in exercise), Karachi 5.6%, the 5.5% |
| "Q: What is the capital of Pakistan? A: The capital of Pakistan is" | Islamabad 81.9%, Karachi 10.3%, Lahore 1.6%, Dh 0.7%, capital 0.7% |

Small-model effect: Islamabad missing from row 1's top five. A large model would likely rank it higher. The wording changing the chances happens in every model.

In which row is Islamabad the likeliest next piece, and what is different about that row's wording?

**Your answer.**

### Key
Row 2. It is shaped like a question followed by the start of an answer ("Q: ... A: ..."); row 1 reads like the opening of a description. Not scored. Aim: he sees that the wording, not the fact, moved the chances.

## Step: Pick and say why

Which idea best explains the two rows? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. The model gives chances for the next piece from how text like this usually went on in its training, so the wording changes the chances.
B. The model searches a store of facts; the plain sentence is a weaker search, so it pulled up the wrong entries.
C. The model has never seen the capital of Pakistan in its training text, so it is guessing.
D. The model only treats text as a question when there is a question mark; without one it does not know it is being asked.

**Your answer.**

### Key
A. B is the wrong idea this unit targets: a search for one fact would return the same fact for both wordings. C is refuted by row 2, where Islamabad got 81.9%. D: rows 1 and 2 differ in far more than the question mark (row 2 has the whole question-and-answer shape), and the next step shows a wording with no question mark that still puts Islamabad first.
Score: 1 only if he picks A and his reason says the wording (how text like this usually continues) changed the chances; 0 for A with a search or memory reason, or any other letter. Record the confidence.
Skip rule: A, right reason, confidence 4 or 5: go straight to "New case".

## Step: Predict

Here is a third wording, not yet shown to you:

"My friend asked me where Pakistan's government sits, and I told her the capital of Pakistan is"

Predict: will Islamabad be the likeliest next piece? Give a rough chance for it, as a percentage.

**Your answer.**

### Key
He gives a direction and a number before seeing the run (runs/llm01-capital-friend.json, shown next). Not scored.

## Step: Run

The real output for "... and I told her the capital of Pakistan is":

| Next piece | Islamabad | Karachi | in | Lahore | ____ |
|---|---|---|---|---|---|
| Model's chance | 45.0% | 12.5% | 7.8% | 5.1% | 1.8% |

Islamabad is first, at 45.0%: higher than in the plain sentence (not in the top five), lower than in the question-and-answer wording (81.9%). This wording has no question mark.

Compare with your prediction: how far off were you, and in which direction?

**Your answer.**

### Key
The told-her wording sits between the other two: it reads partly like someone about to state an answer. The point is his number against 45.0% and the direction of his miss. Not scored.

## Step: Explain

In one to three lines, in your own words: why did the model put "located" first in row 1 but "Islamabad" first in row 2?

**Your answer.**

### Key
Row 2 looks like a question followed by an answer, and in text like that the next piece is usually the answer. Row 1 looks like the start of a description, and descriptions often go on "is located in...". Andrej Karpathy (Deep dive into LLMs), describing how a model makes each next piece: it "gives you the answer for the probabilities of what comes next". On facts, he says "the information is not stored explicitly in any of the parameters". Mark his answer: matches, partly (name the missing piece), or wrong. Not scored.
Simpler: Look at row 2. It starts with "Q:" and then "A:". In text shaped like that, what usually comes straight after "A: The capital of Pakistan is"? And in an ordinary description, what word often follows "is"?

## Step: Wrong idea fixed

**The wrong idea:** "The model searches a store of facts and returns the answer; when it is wrong, the search failed."

**Why it is wrong:** your two rows ask for the same fact. A search for one fact gives the same result however you word it. Here Islamabad got 81.9% in one wording and was not in the top five in the other.

**The right idea:** for each next piece of text, the model gives a chance to every possible piece, based on how text like this usually went on, and picks from those chances. The wording you give changes the chances.

**What it costs:**
given: a support assistant answers 1,000 questions a day, and 1 in 5 of them is worded so that the right answer is not the likeliest next piece (like row 1).
Work it out: how many questions a day are at risk of a wrong answer? Then name one place in a real product where that would matter most.

**Your answer.**

### Key
200 a day (1,000 / 5). It matters most where a wrong answer costs money or harm: tax rates, prices, medical or legal facts. This is why products hand the model the right source text inside the prompt (retrieval) instead of trusting what it picked up in training, and why they test many wordings of the same question. Accept any sensible place. Not scored.
Simpler: A search box gives the same result however you type the question. This model did not: the "Q: ... A: ..." wording got Islamabad at 81.9%, the plain sentence did not have it in the top five. So it is not searching; it is carrying on text, and the wording steers it. Now the number: 1,000 questions, 1 in 5 at risk. How many?

## Step: New case

A new situation. The same tiny model was asked "What is 683 x 47? Reply with the number only." It answered **32519**. The right answer is 32101. (Getting sums like this wrong is partly a small-model effect: large models get them right far more often. How the answer is written, one piece after another, is the same in every model.)

Which is the best explanation? Pick one, give a one-line reason and a confidence from 1 to 5.

A. It worked the sum out correctly inside, then slipped when typing the answer.
B. It has a calculator built in, but the calculator only handles small numbers.
C. It wrote the answer one piece at a time, each the likeliest next piece after the text so far; no step checked the product.
D. It was trained on words, not numbers, so it picked digits at random.

**Your answer.**

### Key
C. A and B both assume a working calculation that a lookup or typing error spoiled; nothing in the model runs a checked sum. D: the answer is not random; it has about the right size and the model gives the same pieces the same chances every time.
Score: 1 only if he picks C and his reason says the digits come out as likely next pieces of text, not from a calculation or a stored table; 0 otherwise.

## Step: Close

Finish this line in your own words: "Next time an AI gives a confident wrong fact, I will first ask ..."

**Your answer.**

### Key
Something like: "... how the question was worded, and whether the model was given the source, rather than assuming a lookup failed." His line goes into the recall queue. Not scored.

## Cold

A new case. The same tiny model, plain text again, no chat around it:

| The model was given | Top next pieces, with the model's chance for each |
|---|---|
| "The capital of Australia is" | ______ 20.5%, Canberra 10.4%, __ 8.6%, the 6.5%, located 5.8% |
| "Q: What is the capital of Australia? A: The capital of Australia is" | Canberra 96.9%, Melbourne 1.1%, Sydney 0.6% |

Which explanation fits best? Pick one, give a one-line reason and a confidence from 1 to 5.

A. The model has Canberra saved under the question form of the fact but not under the plain form.
B. The question-and-answer shape is text where an answer usually comes next, so the chance moves to Canberra; the plain sentence often goes on with a blank or a description.
C. The model is surer about Australia than about Pakistan because Australia is written about more.
D. The model needs the letter "Q" to know it should look the answer up.

**Your answer.**

### Key
B. A and D keep the store-of-facts idea (saved entries, a lookup switched on by "Q"). C may be true about training text, but it does not explain why the same fact moves from 10.4% to 96.9% within one country.
Score: 1 only if he picks B and his reason says the wording changes which next piece is likely; 0 otherwise.

## Cards
- Q: Does a language model look up facts in a store when it answers? | A: No. For each next piece of text it gives a chance to every possible piece, from how similar text went on in its training, and picks from those (source: Karpathy, Deep dive into LLMs).
- Q: The tiny model gave Islamabad 81.9% after "Q: What is the capital of Pakistan? A: The capital of Pakistan is", but did not have it in the top five after "The capital of Pakistan is". Why? | A: The question-and-answer shape is text where the answer usually comes next; the wording changed the chances, not the fact. || Q: "... and I told her the capital of Pakistan is" gave Islamabad 45.0%, while the plain "The capital of Pakistan is" put "located" first at 21.9%. Why? | A: The told-her wording reads like someone about to state an answer; the wording changed the chances, not the fact.
- Q: The tiny model answered 347 x 29 with 9503; the truth is 10063. How did it get a wrong number? | A: It wrote the digits as likely next pieces of text, one after another; no step checked the product. || Q: The tiny model answered 683 x 47 with 32519; the truth is 32101. How did it get a wrong number? | A: It wrote the digits as likely next pieces of text, one after another; no step checked the product.
- Q: How do products make an answer depend less on what the model picked up in training? | A: They put the right source text into the prompt (retrieval).
- Q: What does a model do with plain text sent without any chat around it? | A: It carries the text on, like finishing a document, one likely piece at a time.
