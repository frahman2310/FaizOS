skill: llm
id: llm-02
level: 1
title: Strawberry and Urdu
scored: Pick and say why, New case
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/hf-llm-course-2.04.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/openai-cookbook-count-tokens-tiktoken.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-deep-dive-into-llms-like-chatgpt-transcript.md
runs: runs/llm02-tokens-english.json, runs/llm02-tokens-urdu.json, runs/llm02-tokens-roman-urdu.json, runs/llm02-tokens-number.json, runs/llm02-tokens-digits.json, runs/llm02-tokens-strawberry.json, runs/llm02-count-r-strawberry.json, runs/llm02-tokens-withholding.json, runs/llm02-urdu-bill.json, runs/llm02-urdu-bill-qwen.json, runs/llm02-claude-switch.json, runs/llm02-cold-invoice.json, runs/llm02-ratio-openai.json, runs/llm02-ratio-qwen.json, runs/llm02-claude-tokens-only.json
wrong idea: a token is a word

## Step: Odd result

given: the demo model is Qwen2.5-0.5B, a tiny free model with about 0.5 billion parts (numbers it learned in training), run on this Mac. Large models like Claude are far bigger, so some odd results are small-model effects that Claude rarely shows. This unit says which.

Before a model reads text, a tokenizer (a tool that cuts text into pieces of text, called tokens) cuts it up. These are real cuts from two tokenizers: OpenAI's public o200k tokenizer (from the GPT-4o era) and Qwen's.

| Text | Words | OpenAI pieces | Qwen pieces |
|---|---|---|---|
| "How much tax do I owe on my salary?" | 9 | 10 | 10 |
| "1234567" | 1 | 3: `123` `456` `7` | 7: one per digit |
| "strawberry" | 1 | 3: `st` `raw` `berry` | 3: `str` `aw` `berry` |

Then the Qwen model was asked how many times the letter r appears in "strawberry", number only. It answered **2**. The word has 3. (Small-model effect, in part: Karpathy says large models "now get it correct". The cutting into pieces is the same for every model.)

Which text do the two tokenizers cut differently, and in which form does "strawberry" reach the model?

**Your answer.**

### Key
"1234567" (3 pieces vs 7). "strawberry" reaches the model as 3 pieces, never as 10 single letters. Not scored. Aim: he sees that pieces are not words and not letters.

## Step: Pick and say why

Which idea best explains the table? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. A token is a word; the tokenizer (the tool that cuts the text) only splits a word it does not understand.
B. A token is a single letter or digit; the tokenizer groups some of them to save space.
C. A token is a syllable, cut the way the word is said aloud.
D. The tokenizer has a fixed list of chunks built from lots of text; common text is one chunk, other text is cut into several.

**Your answer.**

### Key
D. A is the wrong idea this unit targets: "1234567" is one word but 3 or 7 pieces, and the cutting happens before the model reads anything, so nothing is "understood" first. B fits Qwen's digits, but " salary" and "berry" are single pieces of five or more letters. C: `st` `raw` `berry` and `str` `aw` `berry` are not how the word is said, and two tokenizers would not disagree about syllables.
Score: 1 only if he picks D and his reason points to a fixed list of chunks (common text stays whole, other text is cut); 0 otherwise. Record the confidence.
Skip rule: D, right reason, confidence 4 or 5: go straight to "New case".

## Step: Predict

The same question in Urdu script, 8 words:

"مجھے اپنی تنخواہ پر کتنا ٹیکس دینا ہے؟"

The English took 10 tokens on OpenAI's tokenizer (the tool that cut the text). Predict: will the Urdu take more or fewer tokens on it, and roughly how many?

**Your answer.**

### Key
He gives a direction and a number before seeing the run (runs/llm02-tokens-urdu.json, shown next). Not scored.

## Step: Run

Real counts for the same question in three forms:

| Version | Words | OpenAI tokens | Qwen tokens |
|---|---|---|---|
| English | 9 | 10 | 10 |
| Urdu script | 8 | 15 | 27 |
| Roman Urdu ("Mujhe apni tankhwah par kitna tax dena hai?") | 8 | 16 | 16 |

Fewer words, more tokens. On Qwen, the Urdu word for tax, ٹیکس, was cut into four single letters: `ٹ` `ی` `ک` `س`. In Roman Urdu, "tankhwah" became `tank` `hw` `ah`, while "tax" stayed one piece.

Compare with your prediction: how far off were you, and in which direction?

**Your answer.**

### Key
Urdu took 15 on OpenAI's tokenizer and 27 on Qwen's, against 10 for English: 1.5 times on one, 2.7 times on the other, so the gap depends on the tokenizer. The point is his number against 15 and the direction of his miss. Not scored.

## Step: Explain

In one to three lines, in your own words: why does the same question take more tokens in Urdu than in English?

**Your answer.**

### Key
The tokenizer's list of chunks was built from lots of text, and text that appears often gets its own chunk. English was common in that text, so whole English words are one chunk; Urdu script and Roman Urdu were rarer, so they are cut into small pieces, down to single letters. Hugging Face LLM Course (chapter 2, tokenizers): "rare words should be decomposed into meaningful subwords." The OpenAI cookbook adds that in some languages "tokens can be shorter than one character". Mark his answer: matches, partly (name the missing piece), or wrong. Not scored.
Simpler: The tokenizer has a list of chunks. Chunks for text it saw a lot are big (a whole English word). Chunks for text it saw little are small (single Urdu letters). Which was it shown more of: English or Urdu?

## Step: Wrong idea fixed

**The wrong idea:** "A token is a word."

**Why it is wrong:** in your runs, the one word "1234567" was 3 tokens on one tokenizer (the tool that cuts text) and 7 on the other, and 8 Urdu words were 27 tokens on Qwen.

**The right idea:** a token is a chunk from the tokenizer's fixed list. Common English words are often one token; rare words and other scripts break into more. Numbers follow a fixed rule instead: OpenAI's cuts digits into groups of up to 3 ("1000000" became `100` `000` `0`), Qwen's cuts every digit alone.

**What it costs:** you pay per token, not per word.
given: a firm pays $1,000 a month for questions in English. Its users switch to Urdu script, and their messages show the same ratio as your run on OpenAI's tokenizer (15 tokens where English had 10). The price per token stays the same.
Work it out: what is the new monthly bill? Then: before quoting a price to a client whose users write Urdu, what would you measure first?

**Your answer.**

### Key
$1,500 (1,000 x 15 / 10). With Qwen's ratio it would be $2,700. Both ratios come from one sentence, so they hold only if real messages show the same ratio: measure tokens on a set of real user messages, in the language they use, with the tokenizer of the model you will use (for Claude, Anthropic's token counter), then price from that.
Count and price together: facts.md (checked 2026-09-24) says Claude 4.7 and later make about 30% more tokens for the same text than Sonnet 4.6 and earlier, but Sonnet 5 input costs $2.00 per 1M tokens against $3.00 for Sonnet 4.6. So a $1,000 input bill on Sonnet 4.6 becomes about $867 on Sonnet 5, not $1,300. Not scored.
Simpler: A word can be one token or several. You pay per token. If Urdu takes 15 tokens where English took 10, each question costs 15 / 10 as much. So a $1,000 bill becomes what?

## Step: New case

A new situation. The tax phrase "withholding tax on non-filers" is 4 words. OpenAI's tokenizer (the tool that cuts text) made 7 tokens: `with` `holding` ` tax` ` on` ` non` `-f` `ilers`.

Which is the best explanation? Pick one, give a one-line reason and a confidence from 1 to 5.

A. The tokenizer made a mistake at the hyphen; a better tokenizer would give 4.
B. " tax" and " on" are common chunks; "withholding" and "non-filers" are rarer as whole words, so they were cut into more common pieces.
C. The tokenizer cuts every word longer than 6 letters into parts.
D. Tax words are cut up on purpose so the model pays more attention to them.

**Your answer.**

### Key
B. A keeps the wrong idea (a token should be a word). C: " salary" (6 letters) and "holding" (7 letters) each stayed one piece, so length is not the rule. D: the cut happens before the model, from a fixed list; nothing chooses where attention goes.
Score: 1 only if he picks B and his reason says common text stays whole and rarer text is cut into pieces from the list; 0 otherwise.

## Step: Close

Finish this line in your own words: "Next time I estimate what an AI feature will cost, I will ..."

**Your answer.**

### Key
Something like: "... count tokens on real messages, in the users' own language, with the model's own tokenizer, and use that model's price, instead of counting words." His line goes into the recall queue. Not scored.

## Cold

A new case. The text "Invoice 88317702" was cut by OpenAI's tokenizer (the tool that cuts text into tokens) and by Qwen's:

| | OpenAI pieces | Qwen pieces |
|---|---|---|
| "Invoice 88317702" | 5: `Invoice` ` ` `883` `177` `02` | 10: `Invoice` ` ` and then one piece per digit |

Why do they cut the number so differently, while "Invoice" stays one piece on both? Pick one, give a one-line reason and a confidence from 1 to 5.

A. The number is rare, so each tokenizer cut it wherever its digit pairs were rarest.
B. OpenAI's tokenizer understands it as an amount and splits it like thousands.
C. Each tokenizer cuts digits by its own fixed rule (groups of up to 3 on OpenAI's, one digit each on Qwen's); "Invoice" is a common chunk on both lists.
D. A tokenizer splits a number wherever a digit repeats.

**Your answer.**

### Key
C. A applies the rarity idea, which is right for words but not for numbers: numbers follow a fixed rule. B: the cut comes before any understanding, and `883` `177` `02` is not a thousands split (that would start with a group of two digits). D: `883` keeps the repeated 8s together.
Score: 1 only if he picks C and his reason names a fixed rule for digits that differs between the tokenizers; 0 otherwise.

## Cards
- Q: Is a token the same as a word? | A: No. It is a chunk from the tokenizer's fixed list; one word can be one token or several (source: Hugging Face LLM Course, tokenizers chapter).
- Q: "How much tax do I owe on my salary?" was 10 tokens on OpenAI's tokenizer in English and 15 in Urdu script. Why more in Urdu? | A: Urdu was rarer in the text the tokenizer's list was built from, so it has fewer Urdu chunks and cuts Urdu into smaller pieces. || Q: On Qwen's tokenizer, the same tax question was 10 tokens in English and 27 in Urdu script. Why more in Urdu? | A: Urdu was rarer in the text the tokenizer's list was built from, so it cuts Urdu into smaller pieces, some single letters.
- Q: The tiny Qwen model said "strawberry" has 2 r's. Name one reason models find letter counting hard. | A: They see tokens such as `str` `aw` `berry`, not letters (Karpathy; large models now usually get this one right). || Q: OpenAI's tokenizer turns "strawberry" into `st` `raw` `berry`. Why does that make counting its r's hard for a model? | A: The model gets 3 chunks, not 10 letters, so the letters are never shown one by one.
- Q: How does OpenAI's o200k tokenizer cut "1234567", and how does Qwen's? | A: OpenAI's: `123` `456` `7` (groups of up to 3); Qwen's: 7 pieces, one per digit. || Q: How does OpenAI's o200k tokenizer cut "1000000", and how does Qwen's? | A: OpenAI's: `100` `000` `0` (groups of up to 3); Qwen's: one piece per digit.
- Q: A firm on Claude Sonnet 4.6 ($3.00 per 1M input tokens) moves to Sonnet 5 ($2.00), which makes about 30% more tokens for the same text (facts.md, 2026-09-24). What happens to a $1,000 input bill? | A: About $867: more tokens, but a lower price; count and price together. || Q: A firm's English questions cost $1,000 a month. Its users switch to Urdu script, at 15 OpenAI tokens where English had 10, same price per token. New bill? | A: $1,500 (1,000 x 15 / 10), if real messages show that ratio.
- Q: How should you estimate the token cost of a feature? | A: Count tokens on real user messages, in their language, with the tokenizer of the model you will use, then apply that model's price.
