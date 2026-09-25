skill: llm
id: llm-01
level: 1
title: It predicts, it does not look up
scored: New case
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-deep-dive-into-llms-like-chatgpt-transcript.md
runs: runs/llm01-capital-plain.json, runs/llm01-capital-question.json, runs/llm01-capital-friend.json, runs/llm01-currency-plain.json, runs/llm01-currency-question.json, runs/llm01-cold-australia-plain.json, runs/llm01-cold-australia-question.json, runs/llm01-language-plain.json, runs/llm01-language-question.json, runs/llm01-multiply-model.json, runs/llm01-multiply-true.json, runs/llm01-multiply2-model.json, runs/llm01-multiply2-true.json, runs/llm01-wrong-training.json, runs/llm01-wrong-table.json, runs/llm01-wrong-removed.json, runs/llm01-table-month.json, runs/llm01-help-wrong-training.json, runs/llm01-help-wrong-table.json, runs/llm01-help-wrong-removed.json, runs/llm01-help-table-month.json, runs/llm01-book.json, runs/llm01-city-plain.json, runs/llm01-city-question.json
wrong idea: the model looks facts up in a store and returns the answer

## Step: Goal and odd result

**Goal.** By the end of this unit you can explain where an AI's answer to a fact question comes from, and say when not to trust it on its own. Why it matters: a tax helper that states a wrong rate costs its users money, and you can only fix what you understand.

**The demo model.** Every run in these units uses Qwen2.5-0.5B, a tiny free model running on this Mac (0.5B is its size: 0.5B learned numbers, B = billions). The chat models you use are many times bigger. When a result comes from its small size, the unit says so.

**The odd result.** We gave the model the start of a sentence and asked only for its next piece of text (a piece is a word or part of a word; unit 2 shows how text is cut). The model gives every possible next piece a chance. Its real top five:

| Start of text given to the model | Top next pieces, with the model's chance for each |
|---|---|
| "The capital of Pakistan is" | located 21.9%, Lahore 8.1%, ______ 6.0% (a blank, as in a fill-in worksheet), Karachi 5.6%, the 5.5% |
| "Q: What is the capital of Pakistan? A: The capital of Pakistan is" | Islamabad 81.9%, Karachi 10.3%, Lahore 1.6%, Dh 0.7% (the start of a longer word), capital 0.7% |

Same fact both times. In row 1, Islamabad is not even in the top five.

**Before you read on** (not marked; a first guess is fine): which fits these two rows better? (a) the model looks the fact up in a stored list of facts; (b) the model guesses which text usually comes next. Give a one-line reason.

**Your answer.**

### Key
Kind: show
New: every possible next piece of text gets a chance, a piece is a word or part of a word, the demo model is tiny (0.5B)
Expected: (b), because a stored list would give the same fact both times. Not scored, no hints, no confidence. Whatever he picks, send the next step: it opens with the answer and a line for each option.

## Step: How it works

**Answer: (b).** If you picked (a): a stored list gives the same fact however you ask, but here Islamabad went from missing to 81.9% when only the wording changed. If you picked (b): right. Here is how it works, from Andrej Karpathy's video *Deep Dive into LLMs like ChatGPT*:

1. **Training.** The model read a huge amount of internet text. At every spot it was shown the piece that really came next, and its learned numbers were nudged so that piece gets a slightly higher chance next time.
2. **What it keeps.** Not a list of facts, but patterns: after text shaped like this, this piece usually comes next. Karpathy compares its knowledge to "something you read a month ago".
3. **Answering.** It takes all the text so far and "gives you the answer for the probabilities of what comes next" (probabilities means chances). One piece is picked (unit 3 shows how), added to the text, and it is asked again. A long answer is built this way, one piece at a time. Nothing in this looks a fact up or checks the result.

**On your two rows.** Row 2 is shaped like a question followed by its answer. On the internet, after "A: The capital of Pakistan is", the next piece is usually the answer, so Islamabad gets 81.9%. Row 1 reads like the start of a description or a school worksheet, where "is" is often followed by "located" or a blank. Same fact, different wording, different chances. (Islamabad missing from row 1's top five is partly a small-model effect: bigger models learned from more text. The wording moving the chances happens in every model.)

**A picture.** Your phone keyboard suggests the next word from what people usually type. Karpathy calls this kind of model "a glorified autocomplete". Where the picture breaks: your phone only suggests one word; this model writes the whole answer by repeating the step, and it learned from far more text.

**Your turn** (one line): in row 2, which words in the text make "Islamabad" the likely next piece?

**Your answer.**

### Key
Kind: show
New: training nudges chances toward the real next piece so the model keeps patterns not a list of facts, the wording changes the chances, an answer is built one piece at a time and nothing checks it
Expected: the "Q: ... A: The capital of Pakistan is" shape; after "A:" in text like this, the answer usually comes next. Accept any line that points at the question-and-answer shape. Not marked.

## Step: Predict

A third wording of the same fact, same tiny model:

"My friend asked me where Pakistan's government sits, and I told her the capital of Pakistan is"

What you already know: the plain sentence (row 1) did not have Islamabad in its top five; the question-and-answer shape (row 2) gave it 81.9%.

Predict three things:
1. Will Islamabad be the likeliest next piece here: yes or no?
2. A rough chance for it: below row 1, between the two rows, or near row 2's 81.9%?
3. One-line reason: which part of this wording pushes the chance up or down?

**Your answer.**

### Key
Kind: try
Real run (runs/llm01-capital-friend.json, shown in the next step): Islamabad is first, at 45.0%, between the two rows. A good reason: "I told her the capital of Pakistan is" reads like someone about to state the answer (pushes it up), but it is a story, not a question and answer (keeps it below row 2). Accept any prediction with a reason that points at the wording. Not scored; feedback at once, then the next step shows the run.

## Help: Predict

A worked prediction on another fact, same tiny model.

The two wordings: row A "The currency of Pakistan is the"; row B "Q: What is the currency of Pakistan? A: The currency of Pakistan is the".

1. Which one reads like a question followed by its answer? Row B.
2. So in row B the answer should gain chance. The answer is "Pakistani rupee", so the piece to watch is "Pakistani".
3. Prediction: "Pakistani" higher in B than in A.

The real run: row A gave Pakistani 24.4%, ru 20.7%, Ru 17.9% ("ru" and "Ru" are the start of "rupee"). Row B gave Pakistani 63.5%. The prediction held, and the reason was the shape of the wording.

Now do the same for the friend wording: does "and I told her the capital of Pakistan is" read more like row A, more like row B, or in between? Then give your three answers.

**Your answer.**

### Key
Kind: show
New: -
He should land on "in between" with a reason about the wording. Real answer: 45.0% (runs/llm01-capital-friend.json).

## Step: Run and compare

The real output for "... and I told her the capital of Pakistan is":

| Next piece | Islamabad | Karachi | in | Lahore | ____ |
|---|---|---|---|---|---|
| Model's chance | 45.0% | 12.5% | 7.8% | 5.1% | 1.8% |

Islamabad is first at 45.0%: far above row 1, below row 2's 81.9%. "I told her ... is" is text where someone is about to state an answer, which pushes the answer's chance up. But it is a story, not a question and answer, and stories go on in many ways ("in", a blank), so it stays below row 2. (Karachi at 12.5% is partly a small-model effect; the wording moving the chances happens in every model.)

**What products do about it.** Because a model's facts are patterns from training, products that must be right paste the source text (for example the official rate table) into the prompt, the text sent to the model. Karpathy: "it always works better if you just give it to them". Then the answer comes from text in front of the model, not from something it "read a month ago".

**Compare** (one or two lines): how far off was your prediction, in which direction, and which part of the wording explains the gap?

**Your answer.**

### Key
Kind: show
New: paste the source text into the prompt when a fact must be right
Expected: his own gap against 45.0%, and a line on the wording (about to state an answer, but a story). Not marked.

## Step: Wrong idea fixed

**The wrong idea:** "The model looks facts up in a store; when it is wrong, the lookup failed."

**This is wrong.** Your three wordings ask for one fact. A lookup gives the same answer however you ask. The model gave Islamabad: not in the top five, then 45.0%, then 81.9%.

**The right idea:** it gives a chance to every possible next piece, from patterns in its training text, and builds the answer one piece at a time. The wording changes the chances. Nothing checks the result.

**A decision, priced.**
Suppose an FBR tax helper answers 2,000 questions a day. Your team tested 100 real user questions: from training alone 12 answers were wrong; with the official rate table pasted into every prompt, 1 was wrong. Pasting the table adds $0.003 to each question.

Work out:
1. Wrong answers a day each way, and how many a day the table removes.
2. The extra cost of the table for a 30-day month.
3. Would you pay it for the tax helper? Would you for a helper that suggests names for a new shop? One line of reason each.

**Your answer.**

### Key
Kind: try
1. Training alone: 2,000 x 12 / 100 = 240 wrong a day. With the table: 2,000 x 1 / 100 = 20. Removed: before minus after, 240 - 20 = 220 a day (E11: both sides, not one).
2. 2,000 x $0.003 x 30 = $180 a month.
3. Tax helper: yes; $180 a month to stop 220 wrong tax answers a day, each of which can cost a user money. Shop names: probably not; there is no single right fact to paste, and a name he does not like costs little. Accept either on the shop with a reason about what a wrong answer costs or whether a source exists.
Not scored; feedback at once. If stuck, the Help block.

## Help: Wrong idea fixed

A worked version with other numbers.

Suppose a bank's helper answers 5,000 questions a day; in a 100-question test, 8 were wrong from training alone and 2 were wrong with the bank's fee table pasted in; the table adds $0.004 to each question.

1. Wrong a day from training alone: 5,000 x 8 / 100 = 400. With the table: 5,000 x 2 / 100 = 100. Removed: before minus after, 400 - 100 = 300 a day.
2. Extra cost: 5,000 x $0.004 x 30 = $600 a month.
3. Decision: $600 a month to stop 300 wrong fee answers a day. A wrong fee angers a customer and can cost the bank, so pay it. The reason comes from this unit: the model's facts are patterns, so a fact that must be right is handed to it.

Now do your numbers the same way: 2,000 questions a day, 12 and 1 wrong per 100, $0.003 per question.

**Your answer.**

### Key
Kind: show
New: -
His answers should come out as 240, 20, 220 removed, $180 a month.

## Step: Checks

Three quick checks on the same idea. One line each.

1. Same tiny model, two wordings: "The capital of Australia is" and "Q: What is the capital of Australia? A: The capital of Australia is". Which gives Canberra the higher chance: the first or the second?
2. In the question-and-answer row at the start, Karachi still got 10.3%. A teammate says: "So its fact store has a wrong entry for Pakistan." What is the better explanation?
3. Your helper must quote this year's FBR rate. Which makes the answer depend less on what the model picked up in training: (a) ask the question more politely, or (b) paste the official rate table into the prompt?

**Your answer.**

### Key
Kind: try
1. The second: Canberra 96.9% there, 10.4% in the first (which put a blank first, 20.5%). Text shaped as a question and its answer is usually followed by the answer.
2. There is no store of entries. Karachi is a common word in text about Pakistan, so after this text it is a likely next piece and gets some chance.
3. (b). Karpathy: "it always works better if you just give it to them".
Not scored; feedback at once, one line per check. If he misses one twice, the Help block.

## Help: Checks

A worked check on a new fact, same tiny model.

The wording "Q: What is the national language of Pakistan? A: The national language of Pakistan is" gave: Urdu 38.8%, Pun 23.6% ("Pun" is the start of "Punjabi"), English 7.6%.

The question: why does "Pun" get 23.6% when the answer is Urdu?

The worked answer: Punjabi is often written about next to "Pakistan" and "language", so text like this often goes on with "Pun...". The model gives chances from those patterns. It has no entry saying "national language = Urdu" to check against. And the plain sentence "The national language of Pakistan is" put a blank first, at 16.7%: it reads like a worksheet.

Now go back to the check you were on and answer it the same way: which pattern in the text explains the chance?

**Your answer.**

### Key
Kind: show
New: -
He answers the check he was stuck on, naming the pattern in the text. Answers as in the Checks Key.

## Step: New case

A new kind of case. The same tiny model was asked in a chat: "What is 683 x 47? Reply with the number only." It answered **32519**. The right answer is 32101. (Getting sums like this wrong is largely a small-model effect; big models get far more of them right. How the answer is produced is the same in every model.)

A teammate says: "It has a calculator inside, and the calculator has a bug."

In one line: what actually produced 32519? Add a reason from this unit, then your confidence from 1 (guessing) to 5 (sure).

**Your answer.**

### Key
Kind: scored
Right: it wrote the digits as likely next pieces of text, one after another, from patterns in training text; no calculator and no step did the sum or checked it. The reason comes from "How it works" point 3 (an answer is built one piece at a time; nothing checks the result).
Score: 1 if his line says the digits came out as likely next pieces (predicted text, not a calculation or a lookup) and nothing checked them; 0.5 if right only after a hint (stuck order: his own answer to "How it works", then two options: (a) it calculated, then slipped when typing; (b) it wrote likely-looking digits one piece at a time and nothing did the sum; then the Help block); 0 if he keeps the calculator or a stored table. Record his confidence (calibration only).

## Help: New case

A worked example of the same kind.

The tiny model was asked "What is 347 x 29? Reply with the number only." It answered **9503**. The truth is 10063.

1. What did the model receive? Text: a question, then "Reply with the number only".
2. What does it do with text? It gives a chance to every possible next piece, from patterns in its training text, picks one, adds it, and is asked again.
3. So the digits of 9503 came out one piece after another, each a likely piece after the text so far. After a multiplication question, a number of about the right size is likely text.
4. What checked the result? Nothing. No step multiplied 347 by 29. That is why it can be wrong, and still sound sure.

Now answer the teammate's calculator claim about 683 x 47 the same way, in one line, with your confidence.

**Your answer.**

### Key
Kind: show
New: -
Mark his answer against the New case Score line (0.5 because help was used).

## Step: Close

Finish this line in your own words: "Next time an AI gives me a confident wrong fact, I will first ..."

**Your answer.**

### Key
Kind: close
Something like: "... remember it predicts likely text and does not look facts up, so I check the wording and give it the source." His line goes into the recall queue. Not scored.

## Retry

A new case. The same tiny model was asked in a chat: "Who wrote the 2019 novel The Ledger of Lyari? Reply with the author's name only." There is no such novel; we made the title up. It answered: "The Ledger of Lyari was written by Jhumpa Lahiri." (Jhumpa Lahiri is a real author who did not write it. Bigger models more often say they do not know, because they are trained to; the way the text is produced is the same.)

In one line: why did it name an author instead of saying the book does not exist? Add a reason from this unit, then your confidence from 1 to 5.

**Your answer.**

### Key
Kind: scored
Right: after a question like "Who wrote the novel ...?", a real author's name is the likely next text. The model builds the answer from patterns, one piece at a time; it has no list of books to search, so nothing comes back "not found" and nothing checks the name.
Score: 1 if his line says it produced likely-looking text (an author's name is what usually follows such a question) and nothing looked the book up or checked; 0.5 after a hint; 0 if he says its store of books is out of date or the lookup failed.

## Cold

A new case, same tiny model, next piece only:

| Start of text given to the model | Top next pieces, with the model's chance for each |
|---|---|
| "The largest city in Pakistan is" | Karachi 21.2%, Lahore 8.8%, __ 8.6%, ____ 5.7%, located 5.4% |
| "Q: What is the largest city in Pakistan? A: The largest city in Pakistan is" | Islamabad 38.6%, Karachi 37.8%, Lahore 16.0%, P 1.3%, Dh 1.2% |

The largest city is Karachi. The question-and-answer wording, which helped for the capital, now puts the wrong city first.

In one line: why? Add a reason from this unit, then your confidence from 1 to 5.

**Your answer.**

### Key
Kind: scored
Right: text shaped "Q: What is the ... of Pakistan? A: The ... of Pakistan is" is very often followed by "Islamabad" (questions about the capital are common), so that pattern pulls Islamabad up. The model is not consulting a stored "largest city = Karachi"; it follows patterns in the wording. (Being this close to wrong is partly a small-model effect.)
Score: 1 if his line says the wording is shaped like text that usually goes on with "Islamabad" (a pattern, not a lookup); 0.5 after a hint; 0 if he says the stored fact is wrong or the model confused two entries.

## Cards
- Q: Does a language model look up facts in a store when it answers? | A: No. It gives a chance to every possible next piece, from patterns in its training text, and builds the answer one piece at a time. Nothing checks the result.
- Q: The tiny model gave Islamabad 81.9% after "Q: What is the capital of Pakistan? A: The capital of Pakistan is", but it was not in the top five after "The capital of Pakistan is". Why? | A: Row 2 is shaped like a question followed by its answer, so the answer is the likely next piece. Same fact, different wording, different chances. || Q: "... and I told her the capital of Pakistan is" gave Islamabad 45.0%, between the plain sentence and the question-and-answer wording. Why in between? | A: It is text where someone is about to state an answer, but it is a story, not a question and answer, so other pieces keep some chance.
- Q: How do products make a fact answer depend less on what the model picked up in training? | A: Paste the source text (for example the official rate table) into the prompt. Karpathy: "it always works better if you just give it to them".
- Q: The tiny model answered 683 x 47 with 32519 (truth 32101). What produced the wrong number? | A: It wrote likely digits one piece at a time; nothing did the sum or checked it. || Q: The tiny model answered 347 x 29 with 9503 (truth 10063). What produced the wrong number? | A: The digits came out one piece after another, each a likely piece after the text so far; nothing checked the result.
- Q: Karpathy calls this kind of model "a glorified autocomplete". Where does the phone-keyboard picture break? | A: Your phone only suggests one word; this model writes the whole answer by repeating the step, and it learned from far more text.
