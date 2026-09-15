# Lesson 4 · live · teaching script
Goal: his first live URL. Skills: fastapi-structure, provider-abstraction, docker-multistage,
docker-uv-cache, paas-deploy, health-readiness. Round 1: reaching a machine by URL, registering a
machine at an address, the health check, the provider slot. Round 2: the sealed box (image),
box size, cold start, p95 over the internet. Then the build.

## R1-A · A machine anyone can reach
New: a URL, a web address that runs your machine on a computer that is always on
Status: done 2026-09-14

# Lesson 4 · live · Round 1 · Part A · A machine anyone can reach

**The problem.** Your meter only runs on your laptop. A client who wants your invoice summaries cannot use it, and the moment you close the lid, nothing answers at all.

**The fix:** put the machine on a computer that is always on, and give it a web address (a URL) that anyone can call.

```
someone types:   https://meter.example.com/price
their screen:    {"haiku": 0.0027}
```

A URL is just an address. Visiting it runs one of your machines on that always-on computer, and whatever the machine returns is sent back.

**Picture:** a vending machine. In your bedroom, only you can use it. On a busy street, anyone walking past can put a coin in and get a drink, at 3 a.m. too.

- **The always-on computer is running:** the call reaches your machine, it runs, and its return comes back to the caller.
- **Nothing is running at that address:** the call never reaches a machine, and the caller sees an error.

**Your turn.**

1. A client sends 10,000 calls a day to your URL. Each costs you $0.0027 and you charge $0.01. What is your profit per day?
2. Your meter runs only on your laptop and the lid is closed. The client calls the URL. Does your machine run?
3. The URL runs a machine that returns `{"haiku": 0.0027}`. What does the caller's screen show?
4. Is a URL a machine, or the address that reaches one?
5. **Someone broke it.** The URL still works, but someone changed the machine to return last year's price, `{"haiku": 0.0135}`. The client is billed from it. Crash, quietly wrong, or fine?

### Key
1. $73 a day ((0.01 - 0.0027) x 10,000)
2. no
3. {"haiku": 0.0027}
4. the address that reaches one
5. quietly wrong

## R1-B · Putting a machine at an address
New: the `@app.get("/address")` tag above a machine
Status: done 2026-09-14

# Round 1 · Part B · Putting a machine at an address

**The problem.** The always-on computer holds lots of machines. When a call arrives for `/price`, something has to decide which machine runs.

**The fix:** put a tag directly above a machine that names its address.

```python
@app.get("/price")
def price():
    return {"haiku": 0.0027}
```

`app` is your web app, made once at the top of the file with a toolbox called FastAPI. The tag line `@app.get("/price")` means: "when someone visits `/price`, run the machine right below me."

**Picture:** a post room with labelled pigeonholes. A letter addressed to `/price` goes into the `/price` pigeonhole, and only that one.

- **Someone visits `/price`:** the machine under that tag runs, and its return goes back to them.
- **Someone visits an address no tag names:** no machine runs, and they get a "not found" error.
- **A machine with no tag:** it exists in the file, but no URL can reach it.

**Your turn.**

1. The file has two tags: `/price` returns `{"haiku": 0.0027}` and `/health` returns `{"ok": True}`. Someone visits `/health`. What comes back?
2. Someone visits `/prices`, with an extra s. What happens?
3. A machine in the file has no tag above it. Can any URL run it?
4. `/price` is visited 10,000 times in a day. How many times does the price machine run?
5. **Someone broke it.** The two tags got swapped, so `@app.get("/price")` now sits above the health machine. The billing system visits `/price`. What comes back? Crash, quietly wrong, or fine?

### Key
1. {"ok": True}
2. a "not found" error; no machine runs
3. no
4. 10,000
5. {"ok": True}; quietly wrong

## R1-C · Are you alive?
New: a health check, an address the hosting company visits to ask "are you working?"
Status: done 2026-09-14

# Round 1 · Part C · Are you alive?

**The problem.** The company running your always-on computer has no idea whether your app froze an hour ago. It keeps sending users to a machine that cannot answer.

**The fix:** give your app a health check, an address the hosting company visits every few seconds to ask "are you working?"

```python
@app.get("/health")
def health():
    return {"ok": True}
```

If the reply is good, users keep coming. If there is no reply, or an error, the hosting company stops sending users there and restarts your app.

**Picture:** a lifeguard calling out to a swimmer every 10 seconds: "you OK?" A wave back means carry on. Silence means they dive in.

- **The health machine replies `{"ok": True}`:** users keep being sent to your app.
- **No reply or an error:** users stop being sent there, and your app is restarted.

**Your turn.**

1. The hosting company checks every 10 seconds. How many checks is that in one day (86,400 seconds)?
2. Someone makes each check do a real AI call costing $0.0027. What do the checks alone cost per day?
3. Your app is frozen and cannot reply at all. Does it keep getting users, or get restarted?
4. The password your app uses to call the AI company has expired. Which check notices: A, which replies OK whenever the app is running, or B, which also confirms the password still works?
5. **Someone broke it.** The health machine always returns `{"ok": True}`. The password has expired, so every summary call fails, and users keep being sent to the app. Crash, quietly wrong, or fine?

### Key
1. 8,640
2. about $23 a day (8,640 x 0.0027 = 23.33)
3. restarted
4. B
5. quietly wrong

## R1-D · One socket for every AI company
New: one machine that hides which AI company answers, so switching changes one line
Status: done 2026-09-14

# Round 1 · Part D · One socket for every AI company

**The problem.** Your app asks the AI for replies in 40 different places, each calling Anthropic directly. The day a cheaper AI company appears, switching means finding and changing all 40, and missing one.

**The fix:** every place calls one machine of your own, and only that machine knows which company answers.

```python
def complete(prompt):
    return ask_anthropic(prompt)
```

The whole app calls `complete(prompt)`. To switch companies, you change the one line inside `complete`.

**Picture:** a wall socket. Your lamp plugs into the socket, not into the power station. Change electricity supplier and nothing in the house gets rewired.

- **The app calls `complete`:** whichever company is named inside answers.
- **You switch company:** one line inside `complete` changes, and the 40 places that call it stay the same.
- **A place that calls a company directly:** it ignores `complete`, so a switch never reaches it.

**Your turn.**

1. Without `complete`, how many lines must change to switch company across the 40 places?
2. With `complete`, how many?
3. Anthropic costs $0.0027 a call and another company $0.0020. At 100,000 calls a day, how much does switching save per day?
4. The app calls `complete("hi")` and the line inside is `return ask_other_company(prompt)`. Which company answers?
5. **Someone broke it.** The switch was made inside `complete`, but 3 of the 40 places called `ask_anthropic` directly. After the switch, those 3 still use and bill the old company. Crash, quietly wrong, or fine?

### Key
1. 40
2. 1
3. $70 a day (0.0007 x 100,000)
4. the other company
5. quietly wrong

## R2-A · The sealed box
New: an image (a Docker image), a sealed box with your app plus all it needs
Status: done 2026-09-14

# Round 2 · Part A · The sealed box

**The problem.** Your app works on your laptop. On the always-on computer it refuses to start, because that computer has a different Python and none of your toolboxes.

**The fix:** pack the app and everything it needs into one sealed box, called an image (a Docker image), and have the always-on computer just run the box.

```
the box holds:
  Python 3.12
  the FastAPI toolbox
  your app's files
  the command that starts the app
```

**Picture:** a packed lunchbox. Everything you need to eat is inside, so it does not matter which canteen you sit down in.

- **Everything is in the box:** the app starts the same way on your laptop and on the always-on computer.
- **The computer has its own different Python:** the app ignores it and uses the Python inside the box.
- **Something was left out of the box:** the app fails to start on every computer, so you see it on the first run.

**Your turn.**

1. The box holds Python 3.12. The always-on computer has Python 3.9 of its own. Which Python runs your app?
2. The FastAPI toolbox was left out of the box. Does the app start?
3. The box is 1,000 MB and the computer downloads it at 50 MB per second before starting the app. How many seconds is that?
4. Does your user's web browser go inside your box?
5. **Someone broke it.** The box was packed from an old copy of your files where `/price` returns `{"haiku": 0.0135}`. Your laptop has the new file with 0.0027. The box goes live. What does `/price` return? Crash, quietly wrong, or fine?

### Key
1. 3.12, the one in the box
2. no
3. 20 seconds
4. no
5. {"haiku": 0.0135}; quietly wrong

## R2-B · A smaller box
New: a two-stage box, where only the finished app is copied into a small clean box
Status: done 2026-09-14

# Round 2 · Part B · A smaller box

**The problem.** To build your app you need extra tools. Pack them all into the box and it weighs 1,000 MB, so every start waits for a huge download of tools the live app never uses.

**The fix:** use two stages. Build in a big workshop box, then copy only the finished app into a small clean box, and only the small box goes live.

```
stage 1, the workshop:   Python, building tools, your files   1,000 MB
stage 2, the lunchbox:   small Python, the finished app          200 MB
only stage 2 goes live
```

**Picture:** a furniture factory. The saws and workbenches stay in the factory. Only the finished chair is put on the lorry.

- **Two stages:** only the 200 MB box is downloaded and started.
- **One stage:** the building tools ship too, so every start downloads 1,000 MB.
- **Something the live app needs is left in the workshop:** the small box is missing it, so the app fails to start.

**Your turn.**

1. At 50 MB per second, how many seconds to download the 1,000 MB box? And the 200 MB box?
2. You put out a new version 30 times a month. How many seconds of downloading does the small box save per month?
3. Do the building tools go live in the two-stage setup?
4. A file of test data is only used while building. Workshop or lunchbox?
5. **Someone broke it.** The FastAPI toolbox was left in the workshop and never copied into the lunchbox. The box goes live. Crash, quietly wrong, or fine?

### Key
1. 20 seconds; 4 seconds
2. 480 seconds ((20 - 4) x 30)
3. no
4. workshop
5. crash (the app fails to start and shows the error)

## R2-C · Reusing steps that did not change
New: reused steps, where a rebuild skips any step whose inputs did not change
Status: done 2026-09-15

# Round 2 · Part C · Reusing steps that did not change

**The problem.** You change one price in your app and rebuild the box. Installing the toolboxes takes 90 seconds, and it happens all over again for a one-number change.

**The fix:** build the box in steps, slow ones that rarely change first, and let a rebuild reuse every step whose inputs did not change.

```
step 1: start from a small Python      reused
step 2: install the toolboxes, 90 s    reused while the toolbox list is unchanged
step 3: copy your app's files, 2 s     redone whenever a file changes
```

**Picture:** a pizza shop that makes the dough once in the morning and only adds the topping per order. Remaking the dough for every pizza would turn a 2 minute order into an hour.

- **You change one price:** steps 1 and 2 are reused, and only step 3 is redone.
- **You add a toolbox to the list:** step 2 is redone.
- **A step is redone:** every step after it is redone too, even if its own inputs did not change.

**Your turn.**

1. You change one price. How many seconds does the rebuild take?
2. You add a toolbox to the list. How many seconds now?
3. You change a price 20 times in a day. How many seconds does reusing step 2 save that day?
4. Your app's files change often. Should they be copied before or after the toolboxes are installed?
5. **Someone broke it.** The order got swapped: your files are copied in step 2, and the toolboxes installed in step 3. You change one price. How many seconds does the rebuild take? The box that comes out works normally. Crash, quietly wrong, or fine?

### Key
1. 2 seconds
2. 92 seconds
3. 1,800 seconds (90 x 20)
4. after
5. 92 seconds; fine (the box is correct, only slow to build)

## R2-D · The shop that locks up when it is quiet
New: a cold start, the wait while a switched-off app starts again
Status: done 2026-09-15

# Round 2 · Part D · The shop that locks up when it is quiet

**The problem.** Some hosting companies switch your app off when nobody has used it for a while, to save money. The next user waits for it to start again, a cold start, before any reply begins.

**The fix:** know which kind of host you are on, and pick the one whose waits your users can accept.

```
sleeps when idle:   switched off after 15 min with no calls
                    first call after that: 3 s to start + 0.2 s reply
always on:          never switched off, every call 0.2 s
                    about $7 a month (an estimate)
```

**Picture:** a shop that locks up when the street is empty. The next customer waits outside while the owner walks back and unlocks. A 24-hour shop never makes anyone wait, but pays staff all night.

- **The app was used in the last 15 minutes:** both hosts reply in 0.2 s.
- **The app sat idle for over 15 minutes on the sleeping host:** the first call waits 3 s to start, then 0.2 s.
- **Always on:** no start wait ever, and you pay for every hour.

**Your turn.**

1. On the sleeping host, how long does the first call after a quiet hour take?
2. The always-on host costs $7 a month. Roughly what is that per day, over 30 days?
3. Your app gets a call every minute all day. Does the sleeping host ever switch it off?
4. Product wants 95 of every 100 calls under 1 second, and calls arrive a few times per hour with 20 minute gaps. Which host keeps that promise?
5. **Someone broke it.** The team tested the sleeping host by calling it every minute and saw every call at 0.2 s. Real users arrive every 20 minutes. The dashboard still shows the test numbers. Crash, quietly wrong, or fine?

### Key
1. 3.2 seconds
2. about $0.23 a day
3. no
4. always on
5. quietly wrong (real users each wait 3.2 s)

## R2-E · The trip there and back
New: travel time, the round trip from the user to the always-on computer
Status: done 2026-09-15

# Round 2 · Part E · The trip there and back

**The problem.** Your meter measured a p95 of 676 ms on your laptop. A user in Karachi calling an always-on computer in America also waits for the call to travel there and back, and your laptop never saw that.

**The fix:** measure p95 from where your users are, and put the always-on computer near them.

```
what the user waits = travel there and back + your app's own time
Karachi to America:   about 250 ms travel (estimate) + 676 ms
Karachi to Mumbai:    about  60 ms travel (estimate) + 676 ms
```

**Picture:** food delivery. The kitchen cooks in 10 minutes either way, but a kitchen across the city makes you wait longer for the ride.

- **Measured on the same computer as the app:** travel is 0, so you see only the app's own time.
- **Called from Karachi to America:** about 250 ms of travel is added to every call.
- **Computer moved near the users:** less travel, and the app's own time stays the same.

**Your turn.**

1. App time 676 ms, travel 250 ms. How long does the Karachi user wait?
2. Product promises under 1,000 ms. Does the America computer keep it, and by how many ms?
3. With the Mumbai computer, how long is the wait, and how many ms are left under 1,000?
4. Does moving the computer closer change your app's own 676 ms?
5. **Someone broke it.** The team reports p95 from a test run on the same computer the app lives on, so the dashboard shows 676 ms. Karachi users call the America computer. Crash, quietly wrong, or fine?

### Key
1. 926 ms
2. yes, by 74 ms
3. 736 ms; 264 ms left
4. no
5. quietly wrong (users wait about 926 ms)

## BUILD-L4 · Your meter as a web service
New: none (every decision uses Round 1 and Round 2)
Status: done 2026-09-15

# Lesson 4 · The build · Your meter as a web service

**The build.** Your L3 meter becomes a real web service inside a box, running on this Mac and measured with 100 real calls. Target: a Karachi user's p95 under 1,000 ms, for under $15 a month.

**Decision 1: the box.** One stage, about 1,000 MB, 20 s download per start: costs nothing extra to set up, rules out fast starts. Two stages, about 200 MB, 4 s: rules out shipping building tools, costs care (a toolbox left in the workshop crashes the start).

**Decision 2: the health check,** asked every 10 seconds. A) replies OK while the app runs: $0, rules out noticing an expired password. B) also confirms the password works, without a paid AI call: about $0, rules out users being sent to an app that cannot answer. C) makes a real AI call each time: $23 a day, rules out a cheap health check.

**Decision 3: the host.** Calls arrive every 20 minutes. Sleeps when idle: $0 while quiet, 3 s cold start after 15 idle minutes, rules out the 1,000 ms promise here. Always on: about $7 a month (estimate), rules out saving money when nobody calls.

**Decision 4: where the computer lives.** America: about 250 ms travel from Karachi (estimate), rules out most of your spare time. Mumbai: about 60 ms (estimate), rules out being quick for American users.

**Decision 5: the AI call's deadline.** In this simulator 4% of AI calls hang for 2 s. 1 second, with the L3 retries: rules out waiting on a hung call, costs one retry. No deadline: rules out cutting any hang short, costs a 2 s wait each time.

**Your call.** Pick one option for each of the 5 decisions. Then predict two numbers: the Karachi user's p95 in ms, and the monthly cost.

### Key
Target: Karachi p95 < 1,000 ms and < $15 a month. A sound set: two stages, B, always on, Mumbai, 1 second.
Predicted with that set: about 740 ms (L3 app p95 ~676 + 60 travel), about $7 a month. Measured values replace this after the run.
