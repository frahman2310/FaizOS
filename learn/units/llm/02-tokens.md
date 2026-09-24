skill: llm
id: llm-02
level: 1
title: Text is cut into tokens, not words or letters
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/hf-llm-course-2.04.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/openai-cookbook-count-tokens-tiktoken.md, ../private/research-base/production-and-llm-behaviour/llm-behaviour/karpathy-deep-dive-into-llms-like-chatgpt-transcript.md
runs: runs/llm02-tokens-english.json, runs/llm02-tokens-urdu.json, runs/llm02-tokens-roman-urdu.json, runs/llm02-tokens-number.json, runs/llm02-tokens-strawberry.json, runs/llm02-count-r-strawberry.json, runs/llm02-tokens-withholding.json, runs/llm02-cost-by-language.json
wrong idea: a token is a word

## Step: Odd result

Before a model reads text, a tool called a tokenizer cuts the text into pieces called tokens. These are real cuts from two tokenizers: OpenAI's (used by GPT models) and Qwen's (the small model on this Mac).

| Text | Words | OpenAI pieces | Qwen pieces |
|---|---|---|---|
| "How much tax do I owe on my salary?" | 9 | 10 | 10 |
| "1234567" | 1 | 3: `123` `456` `7` | 7: one per digit |
| "strawberry" | 1 | 3: `st` `raw` `berry` | 3: `str` `aw` `berry` |

Then the Qwen model was asked how many times the letter r appears in "strawberry", number only. It answered **2**. The word has 3.

What is the first thing that strikes you about this table?

**Your answer.**

### Key
Any honest observation. Aim: he notices that the pieces do not match words (one word can be three or seven pieces), that the two tokenizers cut the same number differently, and that the model never sees the letters of "strawberry" one by one.

## Step: Pick and say why

Which idea best explains the table? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. A token is a word; the tokenizer only splits words it does not understand.
B. A token is a single letter or digit; the tokenizer groups some of them to save space.
C. The tokenizer has a fixed list of common chunks of text; common words are one chunk, and rarer text is cut into several.
D. A token is a syllable, the way a word is said aloud.

**Your answer.**

### Key
C. A is the wrong idea this unit targets: "1234567" is one word but 3 or 7 pieces, and the model does not "understand" before cutting; cutting comes first. B fits Qwen's digits, but "berry" and " salary" are single pieces of five or more letters. D is a fair guess, but `st` `raw` `berry` and `str` `aw` `berry` are not how the word is said, and two tokenizers would not disagree about syllables. Record answer, reason, confidence. If C, right reason, confidence 4 or 5: skip to "New case".

## Step: Predict

The same question in Urdu script, 8 words:

"مجھے اپنی تنخواہ پر کتنا ٹیکس دینا ہے؟"

The English version took 10 tokens on OpenAI's tokenizer. Predict: will the Urdu take more or fewer tokens on OpenAI's tokenizer, and roughly how many?

**Your answer.**

### Key
He commits a direction and a number before the run. The run was captured before the session (runs/llm02-tokens-urdu.json) and is shown in the next step.

## Step: Run

Real counts for the same question in three forms:

| Version | Words | OpenAI tokens | Qwen tokens |
|---|---|---|---|
| English | 9 | 10 | 10 |
| Urdu script | 8 | 15 | 27 |
| Roman Urdu ("Mujhe apni tankhwah par kitna tax dena hai?") | 8 | 16 | 16 |

Fewer words, more tokens. On Qwen, the Urdu word for tax, ٹیکس, was cut into four single letters: `ٹ` `ی` `ک` `س`. In Roman Urdu, "tankhwah" became `tank` `hw` `ah`, while the English word "tax" stayed one piece.

Compare with your prediction: how far off were you, and in which direction?

**Your answer.**

### Key
Urdu took 15 on OpenAI's tokenizer and 27 on Qwen's, against 10 for English. The point is his committed number against 15, and the direction of his miss. Note that the gap depends on the tokenizer: 1.5 times on one, 2.7 times on the other.

## Step: Explain

In one to three lines, in your own words: why does the same question take more tokens in Urdu than in English?

**Your answer.**

### Key
The tokenizer's list of chunks was built from lots of text, and chunks that appear often get their own entry. English text was common, so whole English words are one chunk; Urdu script and Roman Urdu were rarer, so they are cut into small pieces, down to single letters. Hugging Face LLM Course (chapter 2, tokenizers): "rare words should be decomposed into meaningful subwords." The OpenAI cookbook adds that in some languages "tokens can be shorter than one character". Mark his answer: matches, partly (name the missing piece), or wrong.

## Step: Wrong idea fixed

**The wrong idea:** "A token is a word."

**Why it is wrong:** in your runs, the one word "1234567" was 3 tokens on one tokenizer and 7 on the other, and 8 Urdu words were 27 tokens on Qwen. The model also said "strawberry" has 2 r's: it gets `str` `aw` `berry`, not letters.

**The right idea:** a token is a chunk from the tokenizer's fixed list. Common English words are often one token; numbers, rare words and other scripts break into more.

**What it costs:** you pay per token, not per word.
given: a firm's AI bill is $1,000 a month for questions asked in English.
The same questions in Urdu would cost about $1,500 on OpenAI's cutting and about $2,700 at Qwen's rate. Separately, facts.md (2026-09-24) says newer Claude models make about 30% more tokens for the same text than older Claude models, so that $1,000 becomes about $1,300 after switching. The local tokenizers only show the mechanism; Claude's exact counts need Anthropic's counter.

Before quoting a price to a client whose users write in Urdu, what would you measure first?

**Your answer.**

### Key
Count tokens on a set of real user messages, in the language they actually use, with the tokenizer of the model you will use (for Claude, Anthropic's token-counting tool), then price from that. Never price from a word count, and never from English samples when users write Urdu.

## Step: New case

A new situation, same idea. The tax phrase "withholding tax on non-filers" is 4 words. OpenAI's tokenizer cut it into 7 tokens: `with` `holding` ` tax` ` on` ` non` `-f` `ilers`.

Which is the better explanation? Pick, give a reason and a confidence 1 to 5.

A. "tax" and "on" are common chunks; "withholding" and "non-filers" are rarer, so they were cut into more common pieces.
B. The tokenizer made a mistake with the hyphen and long words, and a better tokenizer would give 4.

**Your answer.**

### Key
A. Nothing went wrong: every tokenizer cuts rare text into common pieces, and specialist tax words are rarer than everyday ones. B keeps the wrong idea (a token should be a word). Score answer and reason separately.

## Step: Close

Finish this line in your own words: "Next time I estimate what an AI feature will cost, I will ..."

**Your answer.**

### Key
Something like: "... count tokens on real messages in the users' own language with the model's own tokenizer, instead of counting words." His line goes into the recall queue.

## Cards
- Q: Is a token the same as a word? | A: No. It is a chunk from the tokenizer's fixed list; one word can be one token or several (not "a token is a word").
- Q: Why does Urdu text take more tokens than the same meaning in English? | A: The tokenizer's list has fewer Urdu chunks, because Urdu was rarer in the text it was built from, so Urdu is cut into smaller pieces.
- Q: Why do models struggle to count the letters in a word like "strawberry"? | A: They see tokens such as `str` `aw` `berry`, not single letters.
- Q: What are AI calls priced by? | A: Tokens in and tokens out, not words or characters.
- Q: Per facts.md (2026-09-24), how many more tokens do newer Claude models make for the same text than older Claude models? | A: About 30% more.
- Q: How should you estimate the token cost of a feature? | A: Count tokens on real user messages, in their language, with the tokenizer of the model you will use.
