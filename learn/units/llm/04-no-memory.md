skill: llm
id: llm-04
level: 1
title: Each call starts fresh; the model only knows what is sent
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/anthropic-context-windows.md
runs: runs/llm04-fresh-call.json, runs/llm04-history-sent.json, runs/llm04-resend-cost.json
wrong idea: the model remembers me between chats

## Step: Odd result

The small Qwen model on this Mac was sent one message, as a brand new call:

"Earlier in this chat I told you my name and the city I live in. What are they?"

Its real answer:

"In this chat, your name is "Qwen" and the city you live in is Hangzhou, Zhejiang Province, China."

Nothing had been said earlier. The model did not say "I don't know"; it gave a name and a city with full confidence.

What is the first thing that strikes you about this answer?

**Your answer.**

### Key
Any honest observation. Aim: he notices that the model had no earlier chat to look at, and filled the gap with its own name and a city it is linked with, instead of admitting it had nothing.

## Step: Pick and say why

Why did the model not give a real name and city? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. It had forgotten, the way a person forgets after some time.
B. It knew the answer but held it back to protect privacy.
C. Each call starts fresh: the model only sees the text sent in that call, and none was sent about a name or city.
D. It stores what each user says, but this small model has too little room to keep it.

**Your answer.**

### Key
C. A treats the model like a person whose memory fades; there was never anything to forget. B: holding back would give a refusal, not a confident made-up name. D is the wrong idea this unit targets: the model file does not change between calls, whatever its size. Record answer, reason, confidence. If C, right reason, confidence 4 or 5: skip to "New case".

## Step: Predict

A second fresh call. This time the earlier line is pasted into the same message:

"Earlier in this chat I said: my name is Faiz and I live in Lahore. What is my name, and which city did I say I live in?"

Predict: will it answer Faiz and Lahore? Give your chance as a percentage.

**Your answer.**

### Key
He commits a direction and a number before the run. The run was captured before the session (runs/llm04-history-sent.json) and is shown in the next step.

## Step: Run

The real answer to the call with the earlier line included:

"Your name is Faiz, and you live in Lahore. The city you mentioned earlier was Lahore."

Same small model, same settings. The only difference from the failed call is that the earlier line was inside the text sent.

Compare with your prediction: how sure were you, and were you right?

**Your answer.**

### Key
It answered correctly. The point is his committed chance against the result, and noticing that what changed was the text sent, not the model.

## Step: Explain

In one to three lines, in your own words: how does a chat app make the model seem to remember what you said five messages ago?

**Your answer.**

### Key
On every new message the app sends the whole conversation so far, plus the new message, as one prompt (all the text sent in one call). The model reads it all fresh each time. Anthropic (Context windows) calls the context window a "working memory", and says each turn's input "contains all previous conversation history plus the current user message". Mark his answer: matches, partly (name the missing piece), or wrong.

## Step: Wrong idea fixed

**The wrong idea:** "The model remembers me between chats."

**Why it is wrong:** in your run, a fresh call made up the name "Qwen" and the city Hangzhou. The same model got Faiz and Lahore right only when that line was in the text sent.

**The right idea:** the model keeps nothing between calls. The app re-sends the conversation each time, up to the context window, the most text one call can hold.

**What it costs:** re-sent history is paid for again on every call.
given: a chat has 20 exchanges of about 300 tokens each, and the app handles 1,000 chats a day.
Re-sending everything adds up to 63,000 input tokens per chat, against 6,000 if only each new message were sent: 10.5 times more. At Claude Sonnet 5's input price of $2.00 per million tokens (facts.md, 2026-09-24), that is $0.126 per chat instead of $0.012, or $126 a day instead of $12.

What could the app do to cut that cost?

**Your answer.**

### Key
Shorten what is re-sent: drop or summarise old turns, keep only what the next answer needs, and use prompt caching (facts.md: cache reads cost 0.1x the normal input price on most Claude models). Each of these trades cost against the risk of the model missing something it was told earlier.

## Step: New case

A new situation, same idea. A friend says: "Claude in the app remembered my project from last week, so the model learns about me."

Which is the better explanation? Pick, give a reason and a confidence 1 to 5.

A. The model learned about the project and stored it inside itself.
B. The app saved notes about the project and put them into the text sent with the new chat.

**Your answer.**

### Key
B. Chat apps with a memory feature store notes outside the model and add them to the prompt; the model itself is a fixed file that does not change after a chat. A is the wrong idea in a new surface. Score answer and reason separately.

## Step: Close

Finish this line in your own words: "Next time an AI seems to remember me, I will ..."

**Your answer.**

### Key
Something like: "... ask what text the app sent with my message, since the model only knows what is in that call." His line goes into the recall queue.

## Cards
- Q: Does a model remember anything between calls? | A: No. Each call starts fresh; it only knows the text sent in that call (not "it remembers me").
- Q: How does a chat app make the model seem to remember earlier messages? | A: It re-sends the whole conversation with every new message.
- Q: What is the context window? | A: The most text one call can hold, including the conversation re-sent and the reply.
- Q: Why does a long chat cost more per message than a short one? | A: Every earlier message is re-sent and paid for again as input on each call.
- Q: What did the fresh Qwen call do when asked for a name it was never told? | A: It made one up with confidence ("Qwen", Hangzhou) instead of saying it did not know.
- Q: How does an app "remember" you across chats? | A: It stores notes outside the model and adds them to the text sent in the new chat.
