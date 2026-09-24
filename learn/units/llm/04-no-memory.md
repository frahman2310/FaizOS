skill: llm
id: llm-04
level: 1
title: A name it was never told
scored: Pick and say why, New case
sources: ../private/research-base/production-and-llm-behaviour/llm-behaviour/anthropic-context-windows.md
runs: runs/llm04-fresh-call.json, runs/llm04-buried-fact.json, runs/llm04-last-call.json, runs/llm04-last-call-cost.json, runs/llm04-chat-total.json, runs/llm04-chat-cost.json, runs/llm04-day-cost.json, runs/llm04-card-last-call.json, runs/llm04-card-last-call-cost.json
wrong idea: the model remembers me between chats

## Step: Odd result

given: the demo model is Qwen2.5-0.5B, a tiny free model with about 0.5 billion parts (numbers it learned in training), run on this Mac. Large models like Claude are far bigger, so some odd results are small-model effects that Claude rarely shows. This unit says which.

The tiny model got one message as a brand new call (one request sent to the model, and its reply):

"Earlier in this chat I told you my name and the city I live in. What are they?"

Its real answer:

"In this chat, your name is "Qwen" and the city you live in is Hangzhou, Zhejiang Province, China."

This is the full text that was sent. The chat software added the lines around your message by itself; you never typed them:

```output
<|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>
<|im_start|>user
Earlier in this chat I told you my name and the city I live in. What are they?<|im_end|>
<|im_start|>assistant
```

(Small-model effect: making up an answer instead of saying "you have not told me". Large models more often say they do not know.)

Of the two things it gave, the name and the city, which one can you find in the text sent, and which not?

**Your answer.**

### Key
The name: "Qwen" is in the hidden first line. The city is not in the text at all; Hangzhou is where Alibaba is based, a link the model picked up in training. Not scored. Aim: he sees that the answer came from the only text it had.

## Step: Pick and say why

Why did the model not give your real name and city? Pick one, give a one-line reason, and your confidence from 1 (guessing) to 5 (sure).

A. It had forgotten your earlier chat, the way a person forgets after some time.
B. It mixed you up with another user whose chat it still had.
C. It knew your details but held them back to protect your privacy.
D. Each call starts fresh: it sees only the text sent in that call, and nothing in it gave your name or city, so it used the only name there.

**Your answer.**

### Key
D. A is the wrong idea this unit targets: there was never an earlier chat inside the model to forget. B: no other user's text was sent either; the model has only this call's text. C: holding back would give a refusal, not a confident wrong name.
Score: 1 only if he picks D and his reason says the model sees only the text sent in this call; 0 otherwise. Record the confidence.
Skip rule: D, right reason, confidence 4 or 5: go straight to "New case".

## Step: Predict

Another fresh call. This time your details are inside the message, among notes about other people:

"Notes for the tax office visit.
My name is Faiz and I live in Lahore.
Ali lives in Karachi and files in March.
Sara lives in Quetta and asked about zakat.
Bilal lives in Multan and owes a late fee.
Hina lives in Peshawar and has two salaries.
Usman lives in Sialkot and runs a shop.
Ayesha lives in Hyderabad and rents a flat.
Kamran lives in Faisalabad and sells cloth.
Zara lives in Islamabad and works from home.
Omar lives in Gujranwala and has a car loan.
Nadia lives in Rawalpindi and teaches.
Question: what is my name, and which city do I live in?"

Predict: will the tiny model answer Faiz and Lahore, with all those other names and cities around? Give your chance as a percentage.

**Your answer.**

### Key
He gives a chance before seeing the run (runs/llm04-buried-fact.json, shown next). Not scored.

## Step: Run

The real answer:

"Your name is Faiz, and you live in Lahore."

Same tiny model, same settings as the call that said "Qwen". The only difference is that your details were inside the text sent.

Compare with your prediction: how sure were you, and were you right?

**Your answer.**

### Key
It answered correctly, even with the other names and cities around. The point is his chance against the result, and noticing that what changed was the text sent, not the model. Not scored.

## Step: Explain

In one to three lines, in your own words: how does a chat app make the model seem to remember what you said five messages ago?

**Your answer.**

### Key
On every new message the app sends the whole conversation so far, plus the new message, as one prompt. The model reads it all fresh each time. Anthropic (Context windows) calls the context window a "working memory" for the model, and says each turn's input "Contains all previous conversation history plus the current user message". Mark his answer: matches, partly (name the missing piece), or wrong. Not scored.
Simpler: The model only reads what is sent in one call. So if it answers about message 1 while you are on message 6, message 1 must have been sent again. Who sends it again: you, the app, or the model?

## Step: Wrong idea fixed

**The wrong idea:** "The model remembers me between chats."

**Why it is wrong:** in your runs, a fresh call answered "Qwen" and Hangzhou: the name came from the only name in the text sent. The same model got Faiz and Lahore right as soon as they were in the text sent.

**The right idea:** the model keeps nothing between calls. The app sends the conversation again each time, up to the context window (the most text one call can hold).

**What it costs:** sent-again text is paid for again on every call.
given: in a chat, each of your messages is 300 tokens, and a chat has 20 of them. With each new message, the app sends every earlier message again plus the new one (replies are left out here to keep it simple). Claude Sonnet 5 input costs $2.00 per 1M tokens (facts.md, checked 2026-09-24).
Work it out: how many input tokens does the call for message 20 send, and what does that one call cost?

**Your answer.**

### Key
6,000 tokens (20 x 300), costing $0.012 (6,000 x 2.00 / 1,000,000). Over the whole chat: 300 x (1 + 2 + ... + 20) = 63,000 tokens, $0.126; at 1,000 chats a day, $126 a day. Sending only the new message would be far cheaper, but the model would lose the chat. To cut the cost, accept any "send less" answer: drop or summarise old messages, keep only what the next answer needs. (If he names caching: cache reads cost 0.1x the normal input price on most Claude models, facts.md.) Each cut risks the model missing something it was told earlier. Not scored.
Simpler: The model keeps nothing after a call, so the app sends the whole chat again each time. Message 1 is sent 20 times by the end. For the call on message 20, the app sends 20 messages of 300 tokens. How many tokens is that?

## Step: New case

A new situation. A friend says: "Claude in the app remembered my project from last week, so the model learns about me."

Which is the best explanation? Pick one, give a one-line reason and a confidence from 1 to 5.

A. The app saved notes about the project and added them to the text sent with the new chat.
B. The company retrained the model on his chats overnight, so the project is now part of the model.
C. Last week's chat is still inside the context window (the most text one call can hold), which keeps filling up across chats.
D. The model searched the web for his name and found the project.

**Your answer.**

### Key
A. Chat apps with a memory feature store notes outside the model and put them into the text sent. B: models are not retrained per user after each chat; the model file stays the same. C: the context window is only the text of one call; it does not carry over between calls. D: nothing about his project would be on the web, and a web search, if the app had one, would still arrive as text sent.
Score: 1 only if he picks A and his reason says the memory is text the app stores and sends, not a change in the model; 0 otherwise.

## Step: Close

Finish this line in your own words: "Next time an AI seems to remember me, I will ..."

**Your answer.**

### Key
Something like: "... ask what text the app sent with my message, since the model only knows what is in that call." His line goes into the recall queue. Not scored.

## Cold

A new case. A developer builds a support bot on Claude. To save money, each call sends only the customer's newest message.

A customer's first message gives her order number. Her second message says "When will my order arrive?" The bot replies "Could you tell me your order number?"

Why did the bot ask again? Pick one, give a one-line reason and a confidence from 1 to 5.

A. The model's memory for this customer filled up after one message.
B. The second call's text did not include the first message, so the model had nothing to read the number from.
C. The model saved the number but will not repeat personal data.
D. Claude forgets fast in long chats; a bigger model would have kept it.

**Your answer.**

### Key
B. Each call starts fresh, and this app sends only the newest message, so the number was never in the text the model saw. A and D treat the model as holding a memory that fills or fades. C invents storage inside the model; nothing is saved between calls. The fix is for the app to send the earlier messages (or a note of the number) again.
Score: 1 only if he picks B and his reason says the number was not in the text sent in that call; 0 otherwise.

## Cards
- Q: Does a model remember anything between calls? | A: No. Each call starts fresh; it only knows the text sent in that call (source: Anthropic, Context windows).
- Q: How does a chat app make the model seem to remember earlier messages? | A: It sends the whole conversation again with every new message.
- Q: What is the context window? | A: The most text one call can hold, including the conversation sent again and the reply.
- Q: A chat app sends every earlier 300-token message again with each new one. How many input tokens does the call for message 20 send, and what does it cost at $2.00 per 1M tokens? | A: 6,000 tokens (20 x 300), $0.012. || Q: A chat app sends every earlier 500-token message again with each new one. How many input tokens does the call for message 10 send, and what does it cost at $2.00 per 1M tokens? | A: 5,000 tokens (10 x 500), $0.01.
- Q: In a fresh call, the tiny Qwen model said your name was "Qwen". Where did that name come from? | A: From a hidden line the chat software adds to every call ("You are Qwen, created by Alibaba Cloud"), the only name in the text sent.
- Q: How does an app "remember" you across chats? | A: It stores notes outside the model and adds them to the text sent in the new chat.
