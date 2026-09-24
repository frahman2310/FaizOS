skill: llm
id: llm-01
level: 1
title: It predicts the next word; it does not look things up
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-state-of-gpt-transcript.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-deep-dive-into-llms-like-chatgpt-transcript.md
runs: runs/llm01-capital-plain.json, runs/llm01-capital-question.json, runs/llm01-capital-after-told.json, runs/llm01-capital-friend.json, runs/llm01-multiply-model.json, runs/llm01-multiply-true.json
wrong idea: the model searches a store of facts and returns the answer

## Step: Odd result

A small AI model (Qwen, run on this Mac) was given the start of a sentence and asked for the word that comes next. It gives a chance for every possible next word. These are its top five, real output:

| The model was given | Top next words, with the model's chance for each |
|---|---|
| "The capital of Pakistan is" | located 21.9%, Lahore 8.1%, ______ 6.0%, Karachi 5.6%, the 5.5% |
| "Q: What is the capital of Pakistan? A: The capital of Pakistan is" | Islamabad 81.9%, Karachi 10.3%, Lahore 1.6% |
| "Islamabad is the capital of Pakistan. The capital of Pakistan is" | located 32.4%, the 10.8%, a 7.0% |

Same fact, three wordings, three very different answers. In the third, it had just been told the answer.

What is the first thing that strikes you about this table?

**Your answer.**

### Key
Any honest observation. Aim: he notices that the wording, not the fact, drives the answer, and that "Islamabad" is missing from rows 1 and 3.

## Step: Pick and say why

Which idea best explains the table? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. The model looks the fact up in a store of facts, but the lookup sometimes fails.
B. The model continues text the way similar text usually continued in what it was trained on.
C. The model does not know the capital of Pakistan.
D. The model understands the question only when it has a question mark.

**Your answer.**

### Key
B. A is the wrong idea this unit targets (a lookup would not change with wording, and would not miss a fact it was just given). C is refuted by row 2 (81.9%). D is a surface guess: row 3 has no question mark and fails, but so does the lack of an answer-shaped context. Record answer, reason, confidence. If B, right reason, confidence 4 or 5: skip to "New case".

## Step: Predict

Here is a fourth wording, not yet run:

"My friend asked me where Pakistan's government sits, and I told her the capital of Pakistan is"

Predict: will "Islamabad" be the model's top next word? Give a rough chance for it, as a percentage.

**Your answer.**

### Key
He commits a direction and a number before the run. The run was captured before the session (runs/llm01-capital-friend.json) and is shown in the next step.

## Step: Run

The real output for "... and I told her the capital of Pakistan is":

| Next word | Islamabad | Karachi | in | Lahore | ____ |
|---|---|---|---|---|---|
| Model's chance | 45.0% | 12.5% | 7.8% | 5.1% | 1.8% |

Islamabad is now first, at 45.0%: higher than the plain sentence (not in the top five), lower than the question-and-answer wording (81.9%). Compare with your prediction: how far off were you, and in which direction?

**Your answer.**

### Key
The told-her wording sits between the other two: it reads partly like someone about to state an answer. The point is his committed number against 45.0%, and the direction of his miss.

## Step: Explain

In one to three lines, in your own words: why did the model put "located" first in row 1 but "Islamabad" first in row 2?

**Your answer.**

### Key
Row 2 looks like a question followed by an answer, and in text like that the next word is usually the answer. Row 1 looks like the start of a descriptive sentence, and sentences like that often continue "is located in...". Andrej Karpathy (State of GPT): a base model is a "document completer"; to it, text "is just a sequence of tokens", and it continues it. Mark his answer: matches, partly (name the missing piece), or wrong.

## Step: Wrong idea fixed

**The wrong idea:** "The model searches a store of facts and returns the answer; when it is wrong, the search failed."

**Why it is wrong:** the same fact came back at 81.9% in one wording and not in the top five in another, and it was missed straight after being stated. A search would not behave like that.

**The right idea:** the model gives a chance to every possible next word, based on how text like this usually continued. The answer you get depends on the wording you give.

**What it costs:** a support assistant that answers 1,000 customer questions a day works out what to say from the wording of each question. Two customers asking the same thing in different words can get different answers. Where in a real product would that matter most?

**Your answer.**

### Key
Anywhere a wrong answer has a cost: tax rates, prices, medical or legal facts. This is why the tax assistant hands the model the right passage (retrieval) instead of trusting what it remembers, and why evaluation tests many wordings of the same question.

## Step: New case

A new situation, same idea. The same small model was asked "What is 347 x 29? Reply with the number only." It answered **9503**. The right answer is 10063.

Which is the better explanation? Pick, give a reason and a confidence 1 to 5.

A. It looked up the multiplication table and misread one digit.
B. It produced digits one at a time, each being the likeliest next piece of text, and one was wrong.

**Your answer.**

### Key
B. There is no table being read; digits are produced as next pieces of text, one after another. Score answer and reason separately.

## Step: Close

Finish this line in your own words: "Next time an AI gives a confident wrong fact, I will first ask ..."

**Your answer.**

### Key
Something like: "... whether the wording pushed it there, and whether it was given the source, rather than assuming its lookup failed." His line goes into the recall queue.

## Cards
- Q: Does a language model look up facts in a store when it answers? | A: No. It gives a chance to every possible next word, based on how similar text continued in its training, and picks from those.
- Q: Why can the same question in different wording get a different answer? | A: The wording changes which continuations are likely, so it changes the chances of each next word.
- Q: The model missed a fact it had just been told in the same text. What does that show? | A: It continues patterns of text; having the fact in the text does not guarantee it is used.
- Q: How do products make answers depend less on the model's memory? | A: They hand it the right source text in the prompt (retrieval) and test many wordings of the same question.
