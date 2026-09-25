skill: llm
id: llm-01
level: 1
title: It predicts, it does not look up
scored: New case 1, New case 2, New case 3
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-deep-dive-into-llms-like-chatgpt-transcript.md
runs: runs/llm01-capital-plain.json, runs/llm01-capital-question.json, runs/llm01-capital-friend.json, runs/llm01-currency-plain.json, runs/llm01-currency-question.json, runs/llm01-cold-australia-plain.json, runs/llm01-cold-australia-question.json, runs/llm01-language-plain.json, runs/llm01-language-question.json, runs/llm01-australia-largest.json, runs/llm01-canada-largest.json, runs/llm01-turkey-largest.json, runs/llm01-newzealand-largest.json, runs/llm01-city-plain.json, runs/llm01-city-question.json, runs/llm01-nigeria-largest.json, runs/llm01-brazil-plain.json, runs/llm01-brazil-question.json, runs/llm01-canada-plain.json, runs/llm01-canada-question.json, runs/llm03-multiply-first-digit.json, runs/llm01-multiply-model.json, runs/llm01-multiply-true.json, runs/llm01-multiply2-model.json, runs/llm01-multiply2-true.json, runs/llm01-help-multiply-model.json, runs/llm01-help-multiply-true.json, runs/llm01-retry-multiply-model.json, runs/llm01-retry-multiply-true.json, runs/llm01-cold-add-model.json, runs/llm01-cold-add-true.json, runs/llm01-film.json, runs/llm01-song.json, runs/llm01-mural.json, runs/llm01-book.json, runs/llm01-exchange.json, runs/llm01-wrong-training.json, runs/llm01-wrong-table.json, runs/llm01-wrong-removed.json, runs/llm01-table-month.json, runs/llm01-help-wrong-training.json, runs/llm01-help-wrong-table.json, runs/llm01-help-wrong-removed.json, runs/llm01-help-table-month.json, runs/llm01-retry-faisal-mosque.json, runs/llm01-cold-minar.json
wrong idea: the model looks facts up in a store and returns the answer

## Step: Goal and odd result

**Goal.** By the end you can explain where an AI's answer to a fact question comes from, and when not to trust it: a tax helper that states a wrong rate costs its users money.

**The odd result.** We gave a tiny AI model on this Mac (Qwen2.5-0.5B-Instruct; the chat models you use are far bigger) the start of a sentence. It gives every possible next piece of text a chance (a piece is a word or part of a word). Its real top three:

| Start of text | Top next pieces, with their chances |
|---|---|
| "The capital of Pakistan is" | located 21.9%, Lahore 8.1%, ______ 6.0% (a blank) |
| "Q: What is the capital of Pakistan? A: The capital of Pakistan is" | Islamabad 81.9%, Karachi 10.3%, Lahore 1.6% |

Same fact both times. In row 1, Islamabad is not even in the top five.

**Before you read on** (not marked; a first guess is fine): which fits these two rows better? (a) the model looks the fact up in a stored list of facts; (b) the model guesses which text usually comes next. Give a one-line reason.

**Your answer.**

### Key
Kind: show
New: every possible next piece of text gets a chance; a piece is a word or part of a word; the demo model is tiny
Expected: (b), because a stored list would give the same fact both times. Not scored, no hints, no confidence. Whatever he picks, send the next step: it opens with the answer and a line for each option.

## Step: How it works

**Answer: (b).** If you picked (a): a stored list gives the same fact however you ask, but here Islamabad went from missing to 81.9% when only the wording changed. If you picked (b): right. Here is how it works, from Andrej Karpathy's video *Deep Dive into LLMs like ChatGPT*:

1. **Training.** The model read a huge amount of internet text. At every spot it was shown the piece that really came next, and its internal numbers were nudged so that piece gets a slightly higher chance next time.
2. **What it keeps.** Not a list of facts, but patterns: after text shaped like this, this piece usually comes next. Karpathy compares its knowledge to "something you read a month ago".
3. **The wording counts.** Asked to go on, it takes all the text so far and "gives you the answer for the probabilities of what comes next" (probabilities means chances). Change the wording and different patterns fit, so the chances change.

**On your two rows.** Row 2 is shaped like a question followed by its answer. On the internet, after "A: The capital of Pakistan is", the next piece is usually the answer, so Islamabad gets 81.9%. Row 1 reads like the start of a description or a school worksheet, where "is" is often followed by "located" or a blank. (Islamabad missing from row 1 is partly a small-model effect; wording moves the chances in every model.)

**A picture.** Your phone keyboard suggests the next word from what people usually type. Karpathy calls the model at this first stage, before its chat training, "a glorified autocomplete". Where the picture breaks: your phone shows a few suggestions; this model gives a chance to every possible piece, and it learned from far more text.

**Your turn** (one line): in row 2, which words in the text make "Islamabad" the likely next piece?

**Your answer.**

### Key
Kind: show
New: training nudges the chance of the real next piece; the model keeps patterns rather than a list of facts; the wording changes the chances
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
Two options: (a) it is not a question, so Islamabad stays as low as in row 1; (b) "I told her ... is" reads like someone about to state the answer, so Islamabad rises well above row 1, but a story is not a question and answer, so it stays below row 2.
Worked answer: 1. Which row does it look like? It has no "Q: ... A:", so it is not row 2. 2. But "I told her the capital of Pakistan is" is text where the next words are usually the answer, so it is not row 1 either. 3. So: yes, Islamabad first; a chance between the two rows; the reason is "about to state the answer, but a story". He says it back in one line.

## Step: Run and compare

The real output for "... and I told her the capital of Pakistan is":

| Next piece | Islamabad | Karachi | in | Lahore | ____ |
|---|---|---|---|---|---|
| Model's chance | 45.0% | 12.5% | 7.8% | 5.1% | 1.8% |

Islamabad is first at 45.0%: far above row 1, below row 2's 81.9%. "I told her ... is" is text where someone is about to state an answer, which pushes the answer's chance up. But it is a story, not a question and answer, and stories go on in many ways ("in", a blank), so it stays below row 2.

**Wrong, but likely.** Karachi got 12.5% here and 10.3% in row 2. Karachi is written next to "Pakistan" very often, so after text about Pakistan it is a likely piece, even when the answer is another city. A pattern can pull up a wrong answer that is common.

The question's shape can do this too. Same tiny model:

| Start of text | Top next pieces |
|---|---|
| "Q: What is the largest city in Australia? A: The largest city in Australia is" | Sydney 35.0%, Melbourne 22.6%, Canberra 22.4% |

Sydney is right. Canberra is Australia's capital, not its largest city, yet it gets 22.4%: text shaped "Q: What is the ... of Australia? A:" is very often a question about the capital, so the shape pulls the capital up. (How close a wrong answer gets is partly a small-model effect; patterns pulling on the chances happen in every model.)

**Compare** (one or two lines): how far off was your prediction, in which direction, and which part of the wording explains the gap?

**Your answer.**

### Key
Kind: show
New: a word often written near the topic gets chance even when it is wrong; a common question shape pulls up the usual answer to that shape
Expected: his own gap against 45.0%, and a line on the wording (about to state an answer, but a story). Not marked.

## Step: One piece at a time

**How a whole answer is written.** In Karpathy's account, the model picks one piece, adds it to the text, and is asked again. A long answer is built this way, one piece at a time. No step looks a fact up or checks the result.

A worked case. The same tiny model, asked as a question: "What is 347 x 29? Reply with the number only."

1. The first piece: the model gave "9" a 94.5% chance. After a multiplication question, a number of about the right size is likely text.
2. It added "9", was asked again, and so on, piece after piece. It wrote **9503**. The true answer is 10063.
3. What did the sum? Nothing. The digits are likely text, not a calculation, and nothing checked them.

**Nothing comes back "not found".** Asked "Who directed the 2018 film The Lanterns of Hunza?" (we made the film up), it answered: "The Lanterns of Hunza was directed by Jia Zhangke", a real director who did not make it. After "Who directed the film ...?", a director's name is the likely next text, and there is no list of films to search. (Bigger models get more sums right and more often say they do not know, because they are trained to. The answer is still written one piece at a time.)

**What products do about it.** When a fact must be right, products paste the source text (for example the official rate table) into the prompt, the text sent to the model. Karpathy: "it always works better if you just give it to them". Then the answer comes from text in front of the model, not from something it "read a month ago".

**Your turn** (one line): in making 9503, which step did the multiplication?

**Your answer.**

### Key
Kind: show
New: an answer is built one piece at a time; nothing looks a fact up or checks it; paste the source text into the prompt when a fact must be right
Expected: none; each digit was a likely next piece. Not marked.

## Step: Wrong idea fixed

**The wrong idea:** "The model looks facts up in a store; when it is wrong, the lookup failed."

**This is wrong.** Your three wordings ask for one fact. A lookup gives the same answer however you ask. The model gave Islamabad: not in the top five, then 45.0%, then 81.9%. And a made-up film still got a director.

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
Not scored; feedback at once.
Two options: for the number removed, (a) 240, the wrong answers from training alone; (b) 220, wrong before minus wrong after, because the table still leaves 20 a day wrong.
Worked answer: 240 a day wrong from training alone; 20 with the table; 240 - 20 = 220 removed. 2,000 x $0.003 = $6 a day, x 30 = $180 a month. $180 a month against 220 wrong tax answers a day: pay it, since a wrong rate costs a user money. Shop names: no single right fact to paste, and a weak name costs little, so probably not. He says it back in one line.

## Step: Checks

Three quick checks on the same idea. One line each.

1. Same tiny model, two wordings: "The capital of Australia is" and "Q: What is the capital of Australia? A: The capital of Australia is". Which gives Canberra the higher chance: the first or the second?
2. "Q: What is the national language of Pakistan? A: The national language of Pakistan is" gave Urdu 38.8% and "Pun" 23.6% ("Pun" is the start of "Punjabi"). A teammate says: "So its fact store has a wrong entry for the language." What is the better explanation?
3. Your helper must quote this year's FBR rate. Which makes the answer depend less on what the model picked up in training: (a) ask the question more politely, or (b) paste the official rate table into the prompt?

**Your answer.**

### Key
Kind: try
1. The second: Canberra 96.9% there, 10.4% in the first (which put a blank first, 20.5%). Text shaped as a question and its answer is usually followed by the answer.
2. There is no store of entries. Punjabi is written about next to "Pakistan" and "language" very often, so after this text "Pun..." is a likely next piece and gets some chance.
3. (b). Karpathy: "it always works better if you just give it to them".
Not scored; feedback at once, one line per check.
Two options: for check 2, (a) the store holds a wrong entry for Pakistan's language; (b) Punjabi is often written next to "Pakistan" and "language", so it is a likely next piece, and nothing checks it.
Worked answer: 1. The second wording is shaped like a question and its answer, so the answer is the likely next piece: Canberra 96.9% against 10.4%. 2. No store exists; "Pun" gets 23.6% because it often follows text like this (the same way Karachi got chance in the capital rows). 3. (b): with the table in the prompt, the answer comes from text in front of the model. He says each back in one line.

## Step: New case 1

Three new cases now, each on its own. They are marked: an answer and a one-line reason each.

**Case 1.** The same tiny model was asked: "What is 683 x 47? Reply with the number only." It answered **32519**. The right answer is 32101.

A teammate says: "It has a calculator inside, and the calculator has a bug."

1. What actually produced 32519? One line.
2. Your reason: which idea from this unit shows it? One line.

**Your answer.**

### Key
Kind: scored
Right: 1. It wrote the digits as likely next pieces of text, one after another; no calculator did the sum. 2. From "One piece at a time": an answer is built one piece at a time and nothing checks it (as with 9503 for 347 x 29).
Score: 0.5 for the answer (likely digits written piece by piece, not a calculation or a lookup) + 0.5 for the reason (one piece at a time, nothing checks). A part right only after a hint gets half its marks. 0 for a part that keeps the calculator or a stored table.
Two options: (a) it calculated, then slipped when typing the answer; (b) it wrote likely-looking digits one piece at a time, and nothing did the sum.
Worked answer: the model received text: a question and "Reply with the number only". It gives a chance to every next piece, picks one, adds it, and is asked again. After a multiplication question, digits of about the right size are likely text, so 32519 came out piece by piece. No step multiplied 683 by 47, and nothing checked it. He says it back in one line.

## Step: New case 2

**Case 2.** Same tiny model, next piece only:

| Start of text | Top next pieces |
|---|---|
| "Q: What is the largest city in Turkey? A: The largest city in Turkey is" | Istanbul 55.7%, Ankara 42.2%, İzmir 0.4% |

Istanbul is right. Ankara is Turkey's capital.

1. Why does Ankara get 42.2%? One line.
2. Your reason: which idea from this unit explains it? One line.

**Your answer.**

### Key
Kind: scored
Right: 1. Text shaped "Q: What is the ... of Turkey? A:" is very often a question about the capital, so the shape pulls Ankara up. 2. From "Run and compare": a common question shape pulls up the usual answer to that shape (Canberra 22.4% for Australia's largest city); the model follows patterns, it does not look up "largest city = Istanbul".
Score: 0.5 for the answer (the question shape usually asks for the capital, so it pulls the capital up) + 0.5 for the reason (patterns, not a lookup; the Canberra case counts). A part right only after a hint gets half its marks. 0 for a part that says the stored fact is wrong or the model mixed up two entries.
Two options: (a) its store has Ankara filed as the largest city by mistake; (b) questions shaped like this are very often about the capital, so the pattern pulls the capital up.
Worked answer: "Q: What is the ... of Turkey? A: The ... of Turkey is" is a shape seen very often with the capital as the answer. The model gives chances from patterns like that, so Ankara gains chance even though the question asks for the largest city. There is no stored "largest city" entry to check. Same as Canberra in the Australia row. He says it back in one line.

## Step: New case 3

**Case 3.** The same tiny model was asked: "Who composed the 2016 song Barish Mein Hisaab? Reply with the name only." We made the song up. It answered: **Sufjan Stevens** (a real American singer who did not write it).

1. Why did it give a name instead of saying the song does not exist? One line.
2. Your reason: which idea from this unit explains it? One line.

**Your answer.**

### Key
Kind: scored
Right: 1. After "Who composed the song ...?", a musician's name is the likely next text, so it wrote one. 2. From "One piece at a time": there is no list of songs to search, so nothing comes back "not found", and nothing checks the name (as with the made-up film).
Score: 0.5 for the answer (a name is the likely text after such a question) + 0.5 for the reason (no list is searched and nothing checks, so nothing comes back "not found"). A part right only after a hint gets half its marks. 0 for a part that says its store of songs is out of date or the lookup failed.
Two options: (a) it searched its store of songs, and the store is out of date; (b) after a "Who composed ...?" question, a name is the likely next text, and there is no list to search, so nothing says "not found".
Worked answer: the model received a question shaped "Who composed the song ...?". In text like this, the next words are usually a musician's name, so a name gets high chance and is written piece by piece. No step searched for the song, so nothing could come back "not found", and nothing checked the name. Same as the made-up film. He says it back in one line.

## Step: Close

Finish this line in your own words: "Next time an AI gives me a confident wrong fact, I will first ..."

**Your answer.**

### Key
Kind: close
Something like: "... remember it predicts likely text and does not look facts up, so I check the wording and give it the source." His line goes into the recall queue. Not scored.

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

## Help: Checks

A worked check on a new case, same tiny model.

The wording "Q: What is the largest city in Canada? A: The largest city in Canada is" gave: Toronto 66.3%, Ottawa 22.5%, Vancouver 3.6%. Toronto is right; Ottawa is Canada's capital.

The question: why does Ottawa get 22.5% when the answer is Toronto?

The worked answer: text shaped "Q: What is the ... of Canada? A:" is very often a question about the capital, so the shape pulls Ottawa up. The model gives chances from patterns like this. It has no entry saying "largest city = Toronto" to check against, and nothing checks the result.

Now go back to the check you were on and answer it the same way: which pattern in the text explains the chance?

**Your answer.**

### Key
Kind: show
New: -
He answers the check he was stuck on, naming the pattern in the text. Answers as in the Checks Key.

## Help: New case 1

A worked example of the same kind.

The tiny model was asked "What is 58 x 76? Reply with the number only." It answered **4368**. The truth is 4408.

1. What did the model receive? Text: a question, then "Reply with the number only".
2. What does it do with text? It gives a chance to every possible next piece, from patterns in its training text, picks one, adds it, and is asked again.
3. So the digits of 4368 came out one piece after another, each a likely piece after the text so far. After a multiplication question, a number of about the right size is likely text.
4. What checked the result? Nothing. No step multiplied 58 by 76. That is why it can be wrong, and still sound sure.

Now answer the teammate's calculator claim about 683 x 47 the same way: the answer, then the reason.

**Your answer.**

### Key
Kind: show
New: -
Mark his answer against the New case 1 Score line (each part right after this help gets half its marks).

## Help: New case 2

A worked example of the same kind.

"Q: What is the largest city in New Zealand? A: The largest city in New Zealand is" gave Auckland 82.3%, Wellington 14.4%. Auckland is right; Wellington is the capital.

1. What shape is the text? "Q: What is the ... of New Zealand? A:", a shape very often used to ask for a capital.
2. So the pattern pulls the capital, Wellington, up, even though the question asks for the largest city.
3. Is anything looked up or checked? No. The chances come from patterns in training text.

Now answer the Turkey case the same way: why Ankara gets 42.2%, then your reason.

**Your answer.**

### Key
Kind: show
New: -
Mark his answer against the New case 2 Score line (each part right after this help gets half its marks).

## Help: New case 3

A worked example of the same kind.

Asked "Who painted the 1998 mural The Tea Sellers of Quetta? Reply with the name only." (we made the mural up), the tiny model answered **Rahul Thapa**.

1. What did it receive? A question shaped "Who painted the mural ...?".
2. What text usually comes next after a question like that? A person's name.
3. Did anything search for the mural? No: there is no list of murals, only patterns. So nothing could come back "not found", and nothing checked the name.

Now answer the song case the same way: why a name, then your reason.

**Your answer.**

### Key
Kind: show
New: -
Mark his answer against the New case 3 Score line (each part right after this help gets half its marks).

## Retry

New cases, same tiny model. One or two lines each.

1. Asked "What is 612 x 38? Reply with the number only.", it answered **22056**; the right answer is 23256. What produced 22056, and which idea from this unit shows it?
2. "Q: What is the largest city in Pakistan? A: The largest city in Pakistan is" gave Islamabad 38.6%, Karachi 37.8%, Lahore 16.0%. Karachi is the largest city. Why does Islamabad come first, and which idea explains it?
3. Asked "Who wrote the 2019 novel The Ledger of Lyari? Reply with the author's name only." (we made the novel up), it answered: "The Ledger of Lyari was written by Jhumpa Lahiri." Why a name instead of "no such book", and which idea explains it?
4. Two wordings: "The capital of Brazil is" and "Q: What is the capital of Brazil? A: The capital of Brazil is". Which gives the start of "Brasília" the higher chance?
5. A helper must state the right fee for a bank's cards. Which makes its answer rest on the real fees: (a) tell it to be careful, or (b) paste the bank's fee table into the prompt?
6. "Q: In which city is the Faisal Mosque? A: The Faisal Mosque is in" gave Riyadh 23.1%, Medina 10.1%, Islamabad 9.2%. The mosque is in Islamabad; it is named after King Faisal of Saudi Arabia. Why does Riyadh come first, and which idea explains it?

**Your answer.**

### Key
Kind: scored
Right: 1. Likely digits written one piece at a time; nothing did the sum or checked it (answer 1 mark, reason 1 mark). 2. Text shaped "Q: What is the ... of Pakistan? A:" is very often a question about the capital, so the shape pulls Islamabad up; a pattern, not a lookup (answer 1, reason 1). 3. After "Who wrote the novel ...?", a real author's name is the likely next text; there is no list of books to search, so nothing comes back "not found" (answer 1, reason 1). 4. The second, the question-and-answer shape: "Bras" 96.6% there, 10.5% in the plain sentence (1 mark). 5. (b) (1 mark). 6. "Faisal" is written next to Saudi Arabia and Riyadh very often, so after text about the Faisal Mosque, Riyadh is a likely piece even though it is wrong (answer 1); a word often written near the topic gets chance, a pattern and not a lookup, as with Karachi (reason 1).
Score: 10 marks: 2 each for items 1 to 3 and 6 (answer, reason), 1 each for items 4 and 5. A mark earned only after a hint counts half. Record Retry = marks / 10. 0 for a part that keeps a calculator, a store or a failed lookup.

## Cold

New cases, same tiny model. One or two lines each.

1. Asked "What is 1234 + 5678 + 91? Reply with the number only.", it answered **2710**; the right answer is 7003. What produced 2710, and which idea from this unit shows it?
2. "Q: What is the largest city in Nigeria? A: The largest city in Nigeria is" gave Lagos 46.3%, "Abu" 45.8% (the start of Abuja, Nigeria's capital). Lagos is right. Why does Abuja come so close, and which idea explains it?
3. Asked "In which year did the Gwadar Silk Stock Exchange open? Reply with the year only." (we made the exchange up), it answered **2018**. Why a year instead of "no such exchange", and which idea explains it?
4. Two wordings: "The capital of Canada is" and "Q: What is the capital of Canada? A: The capital of Canada is". Which gives Ottawa the higher chance?
5. A helper must quote the right electricity tariff. Which makes its answer depend less on what the model picked up in training: (a) ask the question in simpler words, or (b) paste the official tariff table into the prompt?
6. "Q: In which city is Minar-e-Pakistan? A: Minar-e-Pakistan is in" gave Lahore 30.3%, Islamabad 14.3%, "Pakistan" 11.6%. Lahore is right. Why does Islamabad get 14.3%, and which idea explains it?

**Your answer.**

### Key
Kind: scored
Right: 1. Likely digits written one piece at a time; nothing added the numbers or checked them (answer 1, reason 1). 2. Text shaped "Q: What is the ... of Nigeria? A:" is very often a question about the capital, so the shape pulls Abuja up; a pattern, not a lookup (answer 1, reason 1). 3. After "In which year did ... open?", a year is the likely next text; there is no list of exchanges to search, so nothing comes back "not found" (answer 1, reason 1). 4. The second: Ottawa 96.6% there; not in the top five of the plain sentence (1 mark). 5. (b) (1 mark). 6. Islamabad is written next to "Pakistan" very often, so after text about Minar-e-Pakistan it is a likely piece even though the answer is Lahore (answer 1); a word often written near the topic gets chance, a pattern and not a lookup, as with Karachi (reason 1).
Score: 10 marks: 2 each for items 1 to 3 and 6 (answer, reason), 1 each for items 4 and 5. A mark earned only after a hint counts half. Record Cold = marks / 10. 0 for a part that keeps a calculator, a store or a failed lookup.

## Cards
- Q: Does a language model look up facts in a store when it answers? | A: No. It gives a chance to every possible next piece, from patterns in its training text, and builds the answer one piece at a time. Nothing checks the result.
- Q: The tiny model gave Islamabad 81.9% after "Q: What is the capital of Pakistan? A: The capital of Pakistan is", but it was not in the top five after "The capital of Pakistan is". Why? | A: Row 2 is shaped like a question followed by its answer, so the answer is the likely next piece. Same fact, different wording, different chances. || Q: "... and I told her the capital of Pakistan is" gave Islamabad 45.0%, between the plain sentence and the question-and-answer wording. Why in between? | A: It is text where someone is about to state an answer, but it is a story, not a question and answer, so other pieces keep some chance.
- Q: Asked for Australia's largest city, the tiny model gave the capital, Canberra, 22.4%. Why does a wrong answer get so much chance? | A: Text shaped "Q: What is the ... of Australia? A:" is very often a question about the capital, so the shape pulls the capital up. || Q: After "A: The capital of Pakistan is", Karachi still got 10.3%. Why? | A: Karachi is written next to "Pakistan" very often, so it is a likely next piece even when it is wrong.
- Q: How do products make a fact answer depend less on what the model picked up in training? | A: Paste the source text (for example the official rate table) into the prompt. Karpathy: "it always works better if you just give it to them".
- Q: The tiny model answered 347 x 29 with 9503 (truth 10063). What produced the wrong number? | A: It wrote likely digits one piece at a time; nothing did the sum or checked it. || Q: Asked who directed a film we made up, the tiny model named a real director. Why not "not found"? | A: There is no list to search; a name is the likely text after such a question, and nothing checks it.
- Q: Karpathy calls this kind of model "a glorified autocomplete". Where does the phone-keyboard picture break? | A: Your phone shows a few suggestions; this model gives a chance to every possible piece, and it learned from far more text.
