skill: design
id: design-01
level: 1
rung: 1
class: C1 single-call feature
title: Long chats that get cut off
decision points: what to do with a long chat history; when to start summarising
prerequisites: none (the first step states the one earlier idea it uses: the model keeps nothing between calls)
scored: Your move on TalkTherapy, Your move on short chats, Decision note
sources: private/research-base/system-design/excerpts/design-01.md, private/scaledojo/learn/genai/tokens-embeddings-and-memory/conversation-memory-and-context-windows.md
runs: runs/design01-room.json, runs/design01-reply-left.json, runs/design01-msg20-all.json, runs/design01-msg20-window.json, runs/design01-msg20-summary.json, runs/design01-start-ok.json, runs/design01-start-late.json, runs/design01-dau.json, runs/design01-bar.json, runs/design01-half.json

## Step: Goal and the problem

Design, unit 1: long chats that get cut off.

**The problem.** A company runs a chatbot. Most chats are short, but some users keep one chat going for a long time. In those long chats two things go wrong: the bot's answers stop mid-sentence, and the bill for those chats is much higher than for short ones. Today you learn the one design decision that fixes both, and what that decision costs.

**The idea everything rests on.** Each time the app sends something to the model, that is one **call** (one request to the model, and the reply that comes back). The model keeps nothing from one call to the next. So how does a chatbot seem to remember what you said? The app stores the chat itself, and with every new message it sends the whole chat so far again. Your ScaleDojo chapter calls this memory an illusion that the app builds.

**Picture:** a friend who forgets everything after each reply. So before every reply you hand them the whole notebook of your conversation. The notebook gets thicker with every message, and it takes longer to read each time.

**Today's plan:** 2 short toolbox steps (the options engineers choose from), 2 worked examples where you watch an engineer decide, 2 practice guesses on a real brief from your ScaleDojo course, then 3 scored answers on briefs you have not seen.

**Done means:** you pick how a chatbot handles long chats, give the fact in the brief that decided it, and name what your pick costs.

Check you have the idea (not scored):
1. A user sends message 20 of a chat. What does the app send to the model on that call?
A. Only message 20.   B. Messages 1 to 20: the whole chat so far.
2. In one line: why would each new message in a long chat cost more than a new message in a short chat?

**Your answer.**

### Key
Kind: show
New: the model keeps nothing between calls, the app resends the whole chat with every message
Answers: 1. B. The app resends the chat so far; the model has nothing else to go on. 2. Each call carries all the earlier messages, and a long chat has more of them, so there are more tokens to pay for on every call.
Source: the ScaleDojo chapter's opening paragraph (excerpt file section 1).
Simpler: "Your friend forgets everything after each reply. On message 20, what do you have to hand them?"

## Step: Toolbox: what shares the context window

Why do answers get cut off? The model can read only a limited amount of text in one call. That limit is its context window (the most text the model can handle in one call, counted in tokens, and its own reply counts too). Three things share it on every call:
- the **system prompt** (the fixed instructions the app puts at the top of every call, such as "you are a polite support agent"),
- the chat history,
- room held back for the model's reply.

**Worked, with the toy window from your ScaleDojo chapter.** The window is 2,000 tokens. The system prompt takes 150. The app holds back 300 for the reply. The history gets what is left: 2,000 - 150 - 300 = 1,550 tokens.

Now say the app does nothing and the history grows to 1,700 tokens. The system prompt still takes its 150, so the reply is left with 2,000 - 150 - 1,700 = 150 tokens, half the 300 it needed. The model runs out of room partway through its answer and stops. That is the answer cut off mid-sentence. And all 1,700 tokens of history are paid for again on this call.

**Picture:** a page of fixed size. The heading (the system prompt) is printed first, the old conversation fills the middle, and the reply has to fit in whatever space is left at the bottom.

Check (not scored):
1. The chat keeps growing. Which part of the window gets squeezed?
A. the system prompt   B. the room for the reply
2. So what does the user see?

**Your answer.**

### Key
Kind: show
New: context window, the system prompt and history and reply share it, a growing history squeezes the reply
Answers: 1. B. 2. The answer stops mid-sentence.
Source: the ScaleDojo chapter's budget paragraph and toy window (excerpt file section 1); Anthropic's definition includes the reply (section 5).
Simpler: "History took 1,700 of the 2,000. The heading took 150. How much page is left for the reply?"

## Step: Toolbox: four ways to handle a long chat

So a long chat has to be kept inside the context window (the model's limit per call, from the last step). Engineers choose one of four moves. Each is best at something, and each costs something. For the numbers, look at the call for message 20.
Suppose every message is 300 tokens.

| Move | What it does | Wins on | History sent on message 20 | What it loses |
|---|---|---|---|---|
| Send everything | resend the whole chat every call | nothing forgotten; simplest | 6,000 tokens, and growing | cut-offs once the window is full |
| Bigger window | switch to a model with a bigger window | nothing forgotten for longer | 6,000 tokens, and growing | only delays the cut-off; the bill keeps growing |
| **Sliding window** | keep only the last few messages, drop older ones | cheapest; no extra call | 1,500 tokens (last 5), stays flat | anything older is gone for good |
| **Running summary** | squeeze older messages into a short summary (one extra model call writes it); keep the last few word for word | keeps the gist of the whole chat | 1,800 tokens (last 5 plus a 300-token summary), about flat | an extra call now and then; small early details |

Why a bigger window does not fix the bill: Anthropic charges the same price per token for its 1M-token window, so the history you resend costs just as much, on every call.

**Picture for the running summary:** the minutes of a long meeting. The last few exchanges are written out word for word; everything before that is a few lines of minutes.

Check (not scored):
1. Suppose a user asks about something from 10 messages ago, and the app keeps only the last 5. Can the bot answer? Yes or no, and why, in one line.
Suppose the chat then grows to message 40.
2. For each move, does the history sent go up, or stay about the same, compared with message 20?

**Your answer.**

### Key
Kind: show
New: sliding window, running summary, a bigger window only delays the cut-off
Answers: 1. No: that message was dropped, so it is not in the text sent. 2. Send everything and bigger window: up (twice the message-20 figure, since twice as many messages are resent). Sliding window and running summary: about the same (still the last 5, plus a short summary).
Source: the ScaleDojo chapter's two strategies and the hybrid (excerpt file section 1); facts.md (1M-token window at standard price per token).
Simpler for 1: "The app sends only the last 5 messages. Is the old message in what it sends?"

## Step: Worked example 1: the support chatbot

Now watch an engineer make this decision. The case is your ScaleDojo chapter's interview question.

**The case.** A company's support chatbot has chats that often run long. Users say it forgets details they gave early in a long chat. The team also says the bill for long chats is far higher than for short ones.

**1. Read the cues.** A **cue** is a fact in the case that points to a cause.
- "Forgets early details" points to early messages being dropped or cut off.
- "Long chats cost far more" points to the whole chat being resent on every call.
- Both at once: one root cause. The app resends everything until it runs out of room, then cuts. ScaleDojo's strong answer opens: "Both symptoms point at the same root cause".

**2. The options:** the four moves from the toolbox.

**3. The dead ends.**
- Bigger window: the first idea most people have. The engineer drops it: it only moves the cut-off further out, and every call still pays for the whole chat, so the bill gets worse. ScaleDojo marks this as the weak answer.
- Send everything: that is what the app does now. It is the cause.
- Sliding window: fixes the bill, but drops early messages, so the forgetting gets worse.

**4. The pick: running summary.** Keep the last few messages word for word; squeeze everything older into a short summary. Why: it is the only move that answers both cues. The history sent stays about flat (the bill), and the gist of the early chat stays in (the forgetting).

**Replay in three lines.**
- Cue: forgets early details, and long chats cost more.
- What it means: the whole chat is resent, then cut.
- Move: running summary. Cost: an extra call now and then, and some small early details lost.

Check (not scored):
1. The engineer dropped the sliding window. Which cue does it fail?
A. forgets early details   B. long chats cost more
2. The engineer dropped the bigger window. Which cue does it fail?
A. forgets early details   B. long chats cost more

**Your answer.**

### Key
Kind: show
New: a cue (a fact that points to a cause), reading two cues as one cause
Answers: 1. A: it throws early messages away. 2. B: the whole chat is still paid for on every call.
Source: ScaleDojo interview signal 9, weak and strong answers (excerpt file section 2).
Simpler: "A sliding window keeps only the last few messages. What happens to a detail from message 1?"

## Step: Worked example 2: when to start summarising

A running summary brings a second decision: **when does the app start summarising?** Before that point it just sends everything. After it, the older messages get squeezed. ScaleDojo's lab calls this setting summarize_after, and the chapter warns it can be set too high or too low. The start point can be counted in tokens or in turns (a turn is one message and its reply); the toy counts tokens. Watch the engineer check three start points on the toy window, where history has 1,550 tokens of room.

- **Start at 1,200 tokens of history** (the chapter's toy setting). When summarising starts, 1,550 - 1,200 = 350 tokens of room are still free. The summary is made before the window fills. Works.
- **Too late: start at 1,800.** That is 1,800 - 1,550 = 250 tokens past the room history has. The window fills, and the reply is cut off, before any summary is made. The cut-off is back.
- Suppose instead it starts at 200 tokens. Then almost every chat, even a 3-message one that was never going to get long, pays for summary calls. Wasted cost, nothing gained.

**The engineer's rule:** start late enough that short chats never pay for a summary, and early enough that the window never fills first. So the two facts to look for in a brief are: how long a typical chat is, and how long the longest chats get.

Check (not scored):
1. The start point is set too late. Which problem comes back?
A. answers cut off   B. wasted summary calls
2. The start point is set too early. Which problem appears?
A. answers cut off   B. wasted summary calls

**Your answer.**

### Key
Kind: show
New: the start point for summarising, too late brings cut-offs back, too early wastes calls
Answers: 1. A. 2. B.
Source: the ScaleDojo chapter's summarize_after paragraph and toy threshold (excerpt file section 1).
Simpler: "At 1,800 the history is already past its 1,550 room. Has a summary been made yet?"

## Step: Guess the move 1: QuickChat's long chats

Your turn to guess the engineer's move, on a real brief from your ScaleDojo lab (level 1, QuickChat). This is practice: not scored, and you get feedback straight after.

The brief:
- Problem: "Their chatbot is randomly cutting off responses mid-sentence." Users are angry.
- Users: "10K DAU, avg 5 messages/session". DAU means daily active users: 10K is 10,000 people a day. A session is one chat.
- Chats: "Conversations avg 800 tokens, some power users hit 15K tokens". Power users are the few people who use it far more than everyone else.
- Rule: "Must handle multi-turn conversations". A turn is one message and its reply.
- Rule: "Response must never be cut off".
- Suppose the 15K-token chats do not fit in the model's context window (its limit per call); the brief does not give the window size.

What should QuickChat do with long chats?
A. Send everything   B. Bigger window   C. Sliding window   D. Running summary

Give: your pick, and the fact in the brief that decided it, in one line.

**Your answer.**

### Key
Kind: try
Answer: D, running summary. Expert move: the level's hint says "ConversationMemory must summarize old messages to keep total tokens under the model's limit", and its mission is summarising after 20 turns at most.
Deciding fact: answers are cut off, and power users reach 15K tokens (or: it must handle chats of many turns).
Feedback if C: "not yet": a sliding window stops the cut-off, but the brief says it must handle long multi-turn chats, and a sliding window throws the early turns away. Hint: which move keeps something of the early chat?
Feedback if A or B: "not yet": A is what cuts answers off now; B only delays it and raises the bill.
Simpler: "Which move both stops the cut-off and keeps something of the early chat?"
given: 10K DAU, 5 messages a session, 800 and 15K tokens (source: excerpt file section 3, ScaleDojo level 1 brief).

## Step: Guess the move 2: when QuickChat starts summarising

The expert's move was D, a running summary. Cue: answers are cut off, and the brief says chats must go on for many turns. Dropped: the sliding window, because QuickChat's users need the earlier chat.

Next decision, same brief: **when should QuickChat start summarising?** Use two facts from the brief. A typical chat: "avg 5 messages/session". The longest chats: "some power users hit 15K tokens".

A. From turn 2 of every chat.
B. Around turn 20.
C. Never: just send everything.

Pick one, and say in one line each what goes wrong with the other two.

**Your answer.**

### Key
Kind: try
Answer: B. Expert move: the lab's mission "Enable summarization after 20 turns to prevent context overflow".
Why the others fail: A pays for summary calls on the typical 5-message chat, which never gets long (too early). C lets power users' chats fill the window, so answers are cut off again (too late).
Feedback if A: "not yet": look at the typical chat, 5 messages. Does it ever need a summary?
Feedback if C: "not yet": what happens to a 15K-token chat that never gets squeezed?
Simpler: "Start too early: which chats pay for a summary they never needed? Start never: which chats get cut off?"

## Step: How the scored part works

The expert's move was B: start summarising at about turn 20 (the lab's answer is after 20 turns at most). Cues: a typical chat is 5 messages, so starting at turn 2 pays for summaries on chats that never get long; power users reach 15K tokens, so never summarising brings the cut-off back.

Next come 3 scored answers, each on a brief you have not seen. How they are marked:
- **Your pick:** 1 if it is the expert's move with a fact from the brief as the reason. 0.5 if the move is right but no brief fact is given, or for an acceptable other move with the right reason. 0 otherwise.
- **The decision note:** 1 if all three blanks are right, including a real cost. 0.5 if one blank is missing or weak. 0 otherwise.
- You pass the unit at the design bar: an average of 70 out of 100 or more. A right answer after a hint counts 0.5.

You have all the facts you need for each answer inside its brief.

Before you start: predict your score, from 0 to 100.

**Your answer.**

### Key
Kind: show
New: -
Record his number: `uv run engine.py predict design-01 <p>`. No feedback on the number.
Simpler: "Out of 100, what do you expect: roughly how many of the 3 will you get fully right?"

## Step: Your move on TalkTherapy

A new brief from your ScaleDojo lab (a tutorial level: TalkTherapy, a therapy chat app).
- Problem: patients share personal stories, then "2 messages later the AI asks 'So tell me about yourself.'" Patients are leaving.
- Sessions: "Conversations lasting 20-60 turns over 45-minute sessions".
- Rule: "Must remember everything said in the current session".
- Rule: "Must not lose context after 20+ messages". Context here means what was said earlier in the session.
- Suppose a 60-turn session does not fit in the model's context window (its limit per call); the brief does not give the window size.

Which move: send everything, bigger window, sliding window, or running summary?

Give:
1. your pick;
2. the fact in the brief that decided it;
3. one move you dropped, and why, in one line.

**Your answer.**

### Key
Kind: scored
Expert move: running summary with the recent turns kept word for word. The level's mission is to "Enable summarization after 30 turns (compress old messages so you don't run out of space)", on top of memory that resends the chat.
Deciding fact: it must remember everything in the session, and sessions are "Conversations lasting 20-60 turns" (or: it forgets 2 messages later, so the chat is not being sent at all).
Dropped, any one with a right reason: sliding window (throws away the early story, fails "remember everything"); bigger window (only delays the cut-off, bill grows); send everything alone (the longest sessions do not fit, as the brief says to assume).
Score: 1 for running summary + a brief fact + one dropped move with a right reason. 0.5 for running summary with the fact or the dropped reason missing. 0 for sliding window, bigger window, or send everything.
given: 2 messages, 20 to 60 turns, 45 minutes, 20+ messages, 30 turns (source: excerpt file section 4, ScaleDojo level 0.3 brief and missions).

## Step: Your move on short chats

A made-up brief (a practice case, not a real company), built on the rule from worked example 2.
- Suppose a train-ticket helper bot. Chats are short: 3 or 4 messages, about 600 tokens in all.
- Suppose the model's context window (its limit per call) holds far more than that, and no chat has ever come near it.
- The team wants to add a running summary from message 2 of every chat, "just to be safe".

Give:
1. which move you would pick for this bot (send everything, bigger window, sliding window, or running summary);
2. the fact in the brief that decided it;
3. what the team's plan would cost them.

**Your answer.**

### Key
Kind: scored
Expert move: send everything (no summary yet). The chapter: a start point set "too low wastes model calls summarizing conversations that were never going to grow long in the first place".
Deciding fact: chats are 3 or 4 messages and never come near the window.
Cost of the team's plan: an extra summary call on almost every chat, for nothing; and some detail squeezed out of chats that did not need it.
Score: 1 for send everything + the short-chat fact + the wasted-calls cost. 0.5 for send everything with the fact or the cost missing, or for sliding window with "cheap, and old messages do not matter in a 4-message chat". 0 for running summary from message 2, or bigger window.
Simpler: "Worked example 2: what happens when summarising starts far too early?"

## Step: Decision note

Engineers write each decision down in a short note, so the team later knows what was chosen and why. Fill the three blanks for your TalkTherapy decision:

We decided to ______ for TalkTherapy, because ______ (a fact from the brief). It costs us ______.

**Your answer.**

### Key
Kind: scored
Model note: We decided to keep the recent turns word for word and summarise the older ones for TalkTherapy, because it must remember everything said in a session and sessions are "Conversations lasting 20-60 turns". It costs us an extra model call now and then, and some small details from early in the session, which matters here because patients share personal details.
Score: 1 if all three blanks are right, with a real cost (extra calls, lost small details). 0.5 if one blank is missing or the cost is "nothing". 0 otherwise.
given: 20 to 60 turns (source: excerpt file section 4).

## Step: Close

Your rule for next time, in one line: "Next time I see ______, I do ______."

**Your answer.**

### Key
Kind: close
Expert rule: "Next time a chat forgets early details or costs more the longer it runs, I keep the recent messages word for word, summarise the older ones, and start summarising after a typical chat would have ended but before the longest ones fill the window."
Mark his line against it: right if it has the cue (long chats cut off, forget, or cost more) and the move (running summary). Store the corrected line, in his words where right: `uv run engine.py close design-01 "<line>"`.

## Help: Guess the move 1: QuickChat's long chats

A second worked example, on a new surface.
- Suppose a cooking-helper bot. Users plan a whole week of meals in one chat, often 40 messages or more.
- They complain that near the end it forgets which dishes they picked at the start.

The engineer's thinking:
- Cue: forgets early picks, in long chats. What it means: early messages are dropped once the window is full.
- Dropped: the sliding window, because the early picks are exactly what gets thrown away. Dropped: the bigger window, because it only delays the problem and every call pays for the whole chat.
- Move: running summary. The picks from early on survive as a line in the summary ("chose rice on Monday, soup on Tuesday").

Back to QuickChat: which fact in its brief is like "users plan a whole week in one chat"?

**Your answer.**

### Key
Kind: show
New: -
Answer: "Must handle multi-turn conversations" (and power users reaching 15K tokens): long chats whose early part still matters, so the move is the running summary.

## Help: Guess the move 2: when QuickChat starts summarising

A second worked example, on a new surface.
- Suppose a homework-help bot. A typical chat is 4 messages. The longest chats fill the window at about message 50.

The engineer checks three start points:
- Start at message 2: every 4-message chat pays for a summary it never needed. Too early.
- Never start: the 50-message chats fill the window and get cut off. Too late.
- Start somewhere in between, well after 4 and well before 50. Short chats never pay; long chats are squeezed in time.

Back to QuickChat: a typical chat is 5 messages, and power users reach 15K tokens. Which of A, B or C sits in between?

**Your answer.**

### Key
Kind: show
New: -
Answer: B, around turn 20: after a typical 5-message chat is over, before the power users' chats fill the window.

## Help: Your move on TalkTherapy

A second worked example, on a new surface.
- Suppose a study-coach bot for exam revision. One session runs 30 to 50 messages.
- The student explains their weak topics at the start; the bot must keep those in mind all session.
- Suppose a 50-message session does not fit in the model's window.

The engineer's thinking:
- Cue: what was said at the start must stay in use for the whole session.
- Sliding window: dropped, it throws the start away. Bigger window: dropped, it only delays the cut-off, and the bill grows. Send everything: dropped, a 50-message session does not fit.
- Move: running summary, with the recent messages kept word for word. Cost: an extra call now and then, and some small details.

Back to TalkTherapy: which line of its brief plays the part of "must keep the weak topics in mind all session"?

**Your answer.**

### Key
Kind: show
New: -
Answer: "Must remember everything said in the current session" (with "Conversations lasting 20-60 turns"). So the move is the running summary.

## Help: Your move on short chats

A second worked example, on a new surface.
- Suppose a bot that answers "what's the weather in Lahore?" Each chat is 1 or 2 messages.

The engineer's thinking:
- Cue: chats are tiny and never come near the window.
- Running summary: dropped. It would add an extra call to chats that never grow long. That is the "too early" mistake from worked example 2.
- Sliding window: harmless but pointless; there is nothing old to drop.
- Move: send everything. Nothing is lost, there is no extra call, and it is the simplest.

Back to the train-ticket bot: what do its 3 or 4 message chats have in common with the weather bot?

**Your answer.**

### Key
Kind: show
New: -
Answer: both are short and never near the window, so sending everything is enough, and a summary from message 2 only adds wasted calls.

## Help: Decision note

A filled note for the support chatbot from worked example 1:

We decided to keep the last few messages word for word and summarise the older ones for the support bot, because users say it forgets early details and long chats cost far more. It costs us an extra model call now and then, and some small early details.

Look at the three blanks: the move, a fact from the case, and a real cost (never "nothing"). Now fill yours for TalkTherapy.

**Your answer.**

### Key
Kind: show
New: -
Answer: his TalkTherapy note, marked with the Decision note's Score line.

## Retry

A new brief (made up for practice).
- Suppose a language-tutor bot. Learners practise English conversation in one chat for 30 to 50 messages.
- They complain that late in the chat the bot forgets the topic they chose at the start.
- The team also says long chats cost far more than short ones.
- Suppose a 50-message chat does not fit in the model's context window (its limit per call).

Which move: send everything, bigger window, sliding window, or running summary? Give your pick, the fact that decided it, and one move you dropped with why.

**Your answer.**

### Key
Kind: scored
Expert move: running summary with recent messages kept word for word (the same two cues as ScaleDojo's support-bot case: forgets early details, and long chats cost more).
Score: 1 for running summary + a brief fact + one dropped move with a right reason. 0.5 for running summary with the fact or the dropped reason missing. 0 otherwise.

## Cold

A new brief (made up for practice).
- Suppose a university admissions helper. Most chats are 3 or 4 messages. A few applicants stay for 60 messages or more, going through their whole application.
- In those long chats, it forgets the grades they gave at the start, and those chats cost far more than the rest.
- Suppose a 60-message chat does not fit in the model's context window (its limit per call).

Which move: send everything, bigger window, sliding window, or running summary? Give your pick, the fact that decided it, and what your pick costs.

**Your answer.**

### Key
Kind: scored
Expert move: running summary with the recent messages kept word for word (cues: forgets early details, and long chats cost more; the same two cues as ScaleDojo's support-bot case). Cost: an extra model call now and then, and some small early details.
Score: 1 for running summary + a brief fact + a real cost. 0.5 for running summary with the fact or the cost missing. 0 otherwise. Note for feedback: a summary can squeeze out exact grades; an engineer would keep such key facts in the summary, but that is not marked here.

## Cards

- Q: A chatbot's long chats cost far more than its short ones. What does that cue tell you? | A: The whole chat is being resent on every call, so each new message pays for all the earlier ones again. || Q: Users say a bot forgets what they told it early in a long chat. What does that cue tell you? | A: Early messages are being dropped or cut off so the chat fits the model's limit per call.
- Q: Why is "use a model with a bigger window" a weak fix for long chats? | A: It only moves the cut-off further out, and every call still pays for the whole chat again, so the bill keeps growing. || Q: A teammate says a model with a 1M-token window solves long chats. What stays wrong? | A: The resent history is still paid for on every call at the same price per token, so the bill keeps growing, and the cut-off is only delayed.
- Q: Summarising starts too late. What goes wrong? | A: The window fills before any summary is made, so answers are cut off again. || Q: Summarising starts at message 2 of every chat. What goes wrong? | A: Short chats that were never going to grow long pay for summary calls: wasted cost for nothing.
