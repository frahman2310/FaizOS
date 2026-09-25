skill: llm
id: llm-02
level: 1
title: Tokens, not words
scored: New case
sources: ../private/scaledojo/learn/genai/tokens-embeddings-and-memory/how-llms-see-text-tokenization.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/hf-llm-course-2.04.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-deep-dive-into-llms-like-chatgpt-transcript.md
runs: runs/llm02-tokens-english.json, runs/llm02-tokens-urdu.json, runs/llm02-tokens-roman-urdu.json, runs/llm02-tokens-strawberry.json, runs/llm02-count-r-strawberry.json, runs/llm02-tokens-withholding-word.json, runs/llm02-retry-backwards.json, runs/llm02-urdu-bill.json, runs/llm02-urdu-bill-qwen.json, runs/llm02-roman-ratio.json, runs/llm02-help-roman-bill.json, runs/llm02-help-english-bill.json, runs/llm02-help-roman-bill-cost.json, runs/llm02-cold-jazzcash.json, runs/llm02-instr-english.json, runs/llm02-instr-urdu.json, runs/llm02-instr-ratio-openai.json, runs/llm02-instr-ratio-qwen.json, runs/llm02-help-english.json, runs/llm02-help-urdu.json, runs/llm02-help-ratio-openai.json, runs/llm02-help-ratio-qwen.json, runs/llm02-cold-google.json, runs/llm02-cold-easypaisa.json, runs/llm02-cold-islamabad-a.json, runs/llm02-tokens-islamabad.json
wrong idea: a token is a word, so a bill can be counted in words

## Step: Goal and odd result

**Goal.** By the end of this unit you can explain why the same question can cost more in Urdu than in English and why a model slips on letters, and you can price a feature from the right count. Why it matters: AI providers charge per token, not per word.

**Two new words.** A model does not read words. First a tokenizer (a tool that cuts text into pieces from a fixed list) cuts the text; each piece is called a token. The "pieces of text" in unit 1 were tokens. Providers bill by the number of tokens.

**The odd result.** The same tax question, cut by OpenAI's public tokenizer (a real one, free to run):

| Text | Words | Tokens |
|---|---|---|
| English: "How much tax do I owe on my salary?" | 9 | 10 |
| Urdu: "مجھے اپنی تنخواہ پر کتنا ٹیکس دینا ہے؟" | 8 | 15 |

Fewer words, more tokens, so a bigger bill for the same question.

**Before you read on** (not marked): from these two rows, is a token the same as a word? Yes or no, and a one-line reason from the numbers.

**Your answer.**

### Key
Kind: show
New: a tokenizer cuts text into tokens from a fixed list, providers bill per token
Expected: no; 9 words made 10 tokens and 8 words made 15. Not scored, no hints. Whatever he says, send the next step: it opens with the answer.

## Step: How it works

**Answer: no.** 9 English words made 10 tokens; 8 Urdu words made 15. The counts match the words in neither row.

**How the list is built** (ScaleDojo, *How LLMs See Text: Tokenization*). Before any model is trained, the list is built from a huge pile of text. It starts from single letters, then "repeatedly finds the most frequent adjacent pair of pieces across the whole training corpus and merges it into a single new piece" (adjacent: side by side; corpus: the pile of text). ScaleDojo's worked run on five words, low, lower, lowest, newer, wider:

| Round | Pair joined | Why this pair |
|---|---|---|
| 1 | l + o = lo | side by side in 3 of the 5 words |
| 2 | lo + w = low | in the same 3 words |
| 3 | e + r = er | in lower, newer and wider |

After a few merges "lower" is 2 pieces, low + er. A real list repeats this many thousands of times, then is fixed. Hugging Face (LLM Course, chapter 2): "frequently used words should not be split into smaller subwords, but rare words should be decomposed into meaningful subwords."

**On your rows.** English was very common in the text OpenAI's list was built from, so " tax" and " salary" are one token each. Urdu was rarer, so تنخواہ (salary) became 3 tokens, ` تن` `خوا` `ہ`, and ٹیکس (tax) became 2.

**The model gets only these pieces.** Karpathy: "the models don't see characters they see tokens".

**A picture.** A shop till has one-press keys for its best sellers; anything else is typed in bits. Where it breaks: the keys were chosen once, from what sold in the past (the text the list was built from), and they never change for your shop.

**Your turn** (one line): why is ٹیکس 2 tokens while " tax" is 1?

**Your answer.**

### Key
Kind: show
New: the list is built by joining the most frequent side-by-side pairs then fixed, common text stays one token and rare text is cut into several, the model gets tokens not letters
Expected: " tax" was common in the text the list was built from, so it got its own piece; the Urdu word was rarer, so it is cut. Not marked.

## Step: Predict

Now the same question in Roman Urdu (Urdu written in English letters), 8 words:

"Mujhe apni tankhwah par kitna tax dena hai?"

What you know: on OpenAI's tokenizer (the tool that cut the text), English took 10 tokens and Urdu script took 15.

Predict:
1. More or fewer tokens than English's 10?
2. A rough number.
3. One-line reason: which words will stay whole, which will be cut, and why?

**Your answer.**

### Key
Kind: try
Real run (runs/llm02-tokens-roman-urdu.json, shown next): 16 tokens. A good reason: " tax" is common English and stays whole; Roman Urdu words like "tankhwah" and "Mujhe" were rare in the list's text, so they are cut. Accept any number above 10 with a reason about common and rare text. Not scored; feedback at once.

## Help: Predict

A worked prediction on a shorter pair.

English: "What is my electricity bill?" (5 words). Roman Urdu: "Mera bijli ka bill kitna hai?" (6 words).

1. Which words are common English? In the English row, all of them. In the Roman Urdu row, only " bill".
2. So the English should be about one token per word, and the Roman Urdu words other than " bill" may be cut.
3. Prediction: Roman Urdu has more tokens than English.

The real counts on OpenAI's tokenizer: English 6 (What, is, my, electricity, bill, ?). Roman Urdu 10: `M` `era` ` bij` `li` ` ka` ` bill` ` kit` `na` ` hai` `?`. " bill" stayed whole; "Mera", "bijli" and "kitna" were cut.

Now make your three predictions for "Mujhe apni tankhwah par kitna tax dena hai?" the same way.

**Your answer.**

### Key
Kind: show
New: -
He should predict more than 10 with a common-or-rare reason. Real: 16.

## Step: Run and compare

Real counts on OpenAI's tokenizer:

| Version | Words | Tokens |
|---|---|---|
| English | 9 | 10 |
| Urdu script | 8 | 15 |
| Roman Urdu | 8 | 16 |

The Roman Urdu cut: `M` `uj` `he` ` ap` `ni` ` tank` `hw` `ah` ` par` ` kit` `na` ` tax` ` den` `a` ` hai` `?`. " tax" stayed whole (common English); "tankhwah" became ` tank` `hw` `ah` (rare, so cut into common bits).

**Letters.** The demo model in these units is Qwen2.5-0.5B, a tiny model (0.5B learned numbers, B = billions) running on this Mac. It has its own tokenizer, which cuts "strawberry" into `str` `aw` `berry`. Asked how many times r appears in "strawberry", the model answered **2**; there are 3. It gets 3 tokens, never the 10 letters one by one. (Partly a small-model effect: Karpathy says big models "now get it correct". The cutting into tokens happens in every model.)

**Compare** (one or two lines): how far off was your prediction, in which direction, and which rule from the last message explains the gap?

**Your answer.**

### Key
Kind: show
New: each model has its own tokenizer, letter tasks slip because the model gets tokens
Expected: his gap against 16, and the rule: common text stays whole, rare text is cut. Not marked.

## Step: Wrong idea fixed

**The wrong idea:** "A token is a word, so a bill can be counted in words."

**This is wrong.** In your runs, 9 English words were 10 tokens, 8 Urdu words were 15, and the one word "strawberry" was 3.

**The right idea:** a token is a piece from the fixed list of the tokenizer (the tool that cuts the text). Text that was common in the text the list was built from stays whole; rarer text is cut into more pieces. Each model has its own list: Qwen's tokenizer cut the same Urdu question into 27 tokens, not 15.

**A decision, priced.**
Suppose a firm pays $1,000 a month for an English tax helper, and its users switch to Urdu script. The price per token stays the same.

Work out:
1. The new monthly bill at OpenAI's ratio from your run (15 tokens where English had 10), and at Qwen's (27 where English had 10).
2. A client asks you to quote a monthly price today for an Urdu-script helper. Which bill would you quote, and what would you measure first? One line each.

**Your answer.**

### Key
Kind: try
1. $1,000 x 15 / 10 = $1,500; $1,000 x 27 / 10 = $2,700.
2. Neither yet: both ratios come from one sentence and two tokenizers. Measure tokens on a set of real user messages, in Urdu script, with the tokenizer of the model you will actually use (for Claude, Anthropic's token counter, since its tokenizer is not public: facts.md), then price. Accept "quote the higher one as a ceiling" only if he also says to measure first.
Not scored; feedback at once. If stuck, the Help block.

## Help: Wrong idea fixed

A worked version with other numbers.

Suppose a firm pays $2,000 a month for an English helper, and its users switch to Roman Urdu. Your run gave Roman Urdu 16 tokens where English had 10. The price per token stays the same.

1. The bill follows the tokens, not the words: $2,000 x 16 / 10 = $3,200 a month. The ratio 16 / 10 is 1.6 times.
2. What to quote: one sentence is a thin base. Measure tokens on real user messages in Roman Urdu, with the tokenizer (the text-cutting tool) of the model you will use, then multiply by its price per token.

Now do your numbers the same way: $1,000 a month, 15 and 27 tokens where English had 10.

**Your answer.**

### Key
Kind: show
New: -
His answers should be $1,500 and $2,700, then "measure real messages with the model's own tokenizer".

## Step: Checks

Three quick checks. One line each.

1. Your helper's users switch from English to Roman Urdu. From your run, does the bill go up or down, and by roughly how many times?
2. The same Urdu question was 15 tokens on OpenAI's tokenizer (its text-cutting tool) and 27 on Qwen's. Why can two tokenizers cut the same text so differently?
3. Asked to write "withholding" backwards, letter by letter, the tiny model wrote "hewtning" (the right answer is "gnidlohhtiw"). Both tokenizers cut the word into `with` `holding`. Why is this hard for the model?

**Your answer.**

### Key
Kind: try
1. Up, about 1.6 times (16 tokens where English had 10), at the same price per token.
2. Each list was built from its own pile of text; Urdu was common enough in OpenAI's pile to get more Urdu pieces, and rarer in Qwen's, so Qwen cuts it into smaller pieces, some single letters.
3. It gets 2 tokens, not 11 letters, so it has to know which letters sit inside each piece before it can reverse them. (Partly a small-model effect.)
Not scored; feedback at once. If he misses one twice, the Help block.

## Help: Checks

A worked check on a new word.

"JazzCash" (a Pakistani payment app) on two tokenizers. OpenAI's: `Jazz` `Cash`, 2 tokens. Qwen's: `J` `azz` `Cash`, 3 tokens.

Why do they differ? Each list was built from its own pile of text. "Cash" was common in both piles, so it is one piece on both. "Jazz" was common enough in OpenAI's pile to be one piece; in Qwen's it was not, so it is cut.

Why would a model slip when spelling "JazzCash" backwards? It gets `Jazz` `Cash`, not 8 letters, so it has to know which letters are packed inside each piece.

And the cost: text cut into more tokens costs more, at the same price per token.

Now go back to the check you were on and answer it the same way.

**Your answer.**

### Key
Kind: show
New: -
He answers the check he was stuck on; answers as in the Checks Key.

## Step: New case

A product case. Your helper sends the same instruction with every question. The team translated it into Urdu script, and the input bill went up. Real counts:

| Instruction | Words | OpenAI tokens | Qwen tokens |
|---|---|---|---|
| "Answer only from the FBR rate table below." | 8 | 10 | 10 |
| "صرف نیچے دی گئی ایف بی آر ریٹ ٹیبل سے جواب دیں۔" | 12 | 16 | 33 |

A teammate says: "The provider charges more per token for Urdu."

In one line: what actually made the bill go up? Add a reason from this unit, then your confidence from 1 (guessing) to 5 (sure).

**Your answer.**

### Key
Kind: scored
Right: the price per token did not change (providers list one price per token, whatever the language: facts.md). The Urdu instruction is cut into more tokens, 16 instead of 10 on OpenAI's tokenizer (1.6 times) and 33 on Qwen's (3.3 times), because Urdu was rarer in the text each list was built from, so it has fewer Urdu pieces.
Score: 1 if his line says the Urdu is cut into more tokens (same price per token) and the reason is the list built from common text (Urdu rarer); 0.5 if right only after a hint (stuck order: his own answer to "How it works", then two options: (a) the price per token went up; (b) the same price, but more tokens; then the Help block); 0 if he agrees the price per token is higher or counts words. Record his confidence (calibration only).

## Help: New case

A worked example of the same kind.

The instruction "Please reply in short, simple sentences." is 6 words. Its Urdu version, "براہ کرم مختصر اور آسان جملوں میں جواب دیں۔", is 9 words.

1. Count tokens, not words. OpenAI's tokenizer: English 8, Urdu 15. Qwen's: English 8, Urdu 24.
2. Price: the same per token in both languages. So the Urdu instruction costs 15 / 8, about 1.9 times as much on OpenAI's count, and 24 / 8 = 3.0 times on Qwen's.
3. Why more tokens? Every English word here is common, so each is one token. Urdu was rarer in the text the lists were built from, so a word like مختصر (short) is cut: ` مخت` `صر`.

Now answer the teammate about the FBR instruction the same way, in one line, with your confidence.

**Your answer.**

### Key
Kind: show
New: -
Mark his answer against the New case Score line (0.5 because help was used).

## Step: Close

Finish this line in your own words: "Next time I estimate what an AI feature will cost, I will ..."

**Your answer.**

### Key
Kind: close
Something like: "... count tokens on real messages, in the users' own language, with the model's own tokenizer, instead of counting words." His line goes into the recall queue. Not scored.

## Retry

A new case. Your helper for a Pakistani payments firm writes the brand name in almost every reply. On OpenAI's tokenizer (the tool that cuts text into tokens), "Google" is 1 token, while "Easypaisa" is 4: `E` `as` `yp` `aisa`.

A teammate says: "The tokenizer cuts every name longer than 6 letters."

In one line: what is the real reason "Easypaisa" is cut, and one piece of evidence from this unit against the teammate? Then your confidence from 1 to 5.

**Your answer.**

### Key
Kind: scored
Right: "Google" was very common in the text the list was built from, so it has its own piece; "Easypaisa" was rare, so it is cut into common bits. Evidence against the length rule: "holding" (7 letters) stayed 1 token in the Checks, while "Easypaisa" is cut into bits as short as 2 letters; length is not the rule, frequency is.
Score: 1 if he gives the common-or-rare reason and any fair evidence against length; 0.5 after a hint or with the reason but no evidence; 0 if he accepts the length rule or says the tokenizer "does not understand" the name.

## Cold

A new case. The tiny model was asked: "How many times does the letter a appear in the word Islamabad? Reply with the number only." It answered **2**. The word has 3. Both tokenizers cut "Islamabad" into `Islam` `abad`.

In one line: why is counting its a's hard for the model? Add a reason from this unit, then your confidence from 1 to 5.

**Your answer.**

### Key
Kind: scored
Right: the model gets 2 tokens, `Islam` and `abad`, not the 9 letters, so it cannot see the a's one by one; it has to know which letters are packed inside each piece (Karpathy: "the models don't see characters they see tokens"). Partly a small-model effect.
Score: 1 if his line says the model gets tokens, not letters; 0.5 after a hint; 0 if he says it cannot count or was careless, with no mention of tokens.

## Cards
- Q: Is a token the same as a word? | A: No. A token is a piece from the tokenizer's fixed list; one word can be one token or several.
- Q: "How much tax do I owe on my salary?" was 10 tokens in English and 15 in Urdu script on OpenAI's tokenizer. Why more in Urdu? | A: Urdu was rarer in the text the list was built from, so it is cut into more pieces. || Q: On Qwen's tokenizer the same question was 10 tokens in English and 27 in Urdu script. Why? | A: Urdu was rarer in the text Qwen's list was built from, so it is cut into more, smaller pieces.
- Q: How is a tokenizer's list built? | A: It starts from single letters and repeatedly joins the most frequent side-by-side pair into one new piece, then the list is fixed (ScaleDojo).
- Q: The tiny model said "strawberry" has 2 r's. Why do letter tasks trip models? | A: The model gets tokens such as `str` `aw` `berry`, not the letters one by one. || Q: Asked to write "withholding" backwards, the tiny model wrote "hewtning". Why? | A: It gets 2 tokens, `with` `holding`, not the letters one by one.
- Q: English questions cost $1,000 a month; users switch to Urdu script at 15 tokens where English had 10, same price per token. New bill? | A: $1,500: the bill follows the tokens, not the words. || Q: An English helper costs $2,000 a month; users switch to Roman Urdu at 16 tokens where English had 10, same price per token. New bill? | A: $3,200 a month.
- Q: Before quoting the monthly price of an AI feature, what do you measure? | A: Tokens on a set of real user messages, in their language, with the tokenizer of the model you will actually use; then apply its price per token.
