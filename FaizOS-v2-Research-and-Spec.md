# FaizOS v2

## A restructure of the learning system: depth, two modes, frontier content, and a venture research arm

**Version 2.0 specification and research record**
**Written 14 August 2026**
**Supersedes: COURSE.md v1 (20 modules, 44 builds, 66 skills, 52 revision notes)**

---

## Contents

1. [Verdict](#1-verdict)
2. [Diagnosis: what actually went wrong](#2-diagnosis-what-actually-went-wrong)
3. [The replacement pedagogy](#3-the-replacement-pedagogy)
4. [The two modes](#4-the-two-modes)
5. [Curriculum v2: the depth ladder](#5-curriculum-v2-the-depth-ladder)
6. [The frontier update: what changed while you were learning](#6-the-frontier-update-what-changed-while-you-were-learning)
7. [The compute plan](#7-the-compute-plan)
8. [The venture research arm](#8-the-venture-research-arm)
9. [System architecture changes](#9-system-architecture-changes)
10. [Migration plan](#10-migration-plan)
11. [Week one](#11-week-one)
12. [Confidence, conflicts and open questions](#12-confidence-conflicts-and-open-questions)
13. [Sources](#13-sources)

---

## 1. Verdict

The course worked. The method is sound and you should keep it. The three things you identified are real, but you have misdiagnosed one of them, and you have missed the largest one entirely.

**What you got right.** The Brick Method, the four-concept cap, the walk-the-code addition, the insight loop that carries teaching lessons forward between sessions, and the deterministic artefact generation are all good design. None of that changes in v2. The proof that the cap is real is the strongest piece of evidence in your whole record: nine concepts produced one correct blank out of five, three concepts an hour later produced three out of three. That is a measured limit, not a guess, and it survives into v2 intact.

**What you got right about the failure.** Depth. Forty four builds of forty to eighty lines each, in pure Python, is a vocabulary course. You now know what every term means and you cannot build any of them at production scale. That is a real ceiling and v2 breaks it.

**Where your diagnosis is wrong.** You think the coding did not land because the explanation was insufficient, and you are proposing to fix it by explaining every line before you write. That will not work, and it will feel like it is working, which is worse. If someone explains the reference solution line by line and then asks you to reproduce it, you are transcribing from short term memory. You are not composing. The reason the code never landed is simpler and more brutal: across 44 builds you wrote somewhere around 100 lines of code, every one of them a single expression dropped into scaffolding somebody else wrote. You have never once started from an empty file. That is the entire problem. The fix is not more explanation before the attempt, it is a real attempt against a failing test suite, with explanation arriving as a review of your code afterwards.

**What you missed.** Your own CAPSTONE.md already told you: the bottleneck is compute, and one rented GPU hour unlocks four rungs. Twenty modules and forty four builds have produced zero trained models, zero benchmark numbers on a real eval, and zero deployed artefacts. The record you have built is a record of lessons, not of systems. Fifty dollars of spot H100 time changes that this month. No amount of curriculum redesign does. If you implement one thing from this document, make it section 7.

**On the venture arm.** Idea supply is not your constraint. Execution capacity is. A pipeline that produces twenty scored opportunities a week will produce twenty abandoned repositories. I have specified it as an evidence engine with a hard work-in-progress limit of one, not as an idea generator, and I explain why in section 8. There are also two structural constraints in your specific situation, a UK student visa restriction and a Pakistani payment rail problem, that gate every downstream choice about monetisation. Resolve those before you build anything commercial. They are free to resolve and expensive to get wrong.

---

## 2. Diagnosis: what actually went wrong

### 2.1 The coding problem is a mechanism problem, not an explanation problem

Count the lines. Forty four builds, one to four blanks each, call it 2.5 blanks on average, and most blanks are a single expression. That is roughly 110 lines of code written across an entire course. Every one of them sat inside a file whose imports, control flow, data structures, function signatures, and test harness were written for you. You were never asked to decide what a function should take, what it should return, how to structure a loop, where state lives, or what to name anything.

The blank teaches the concept. It does not teach programming. Those are different skills and the course only ever trained one of them.

Look at the friction list in your own record. Every recurring friction you logged is a *conceptual* inversion (duration versus rate, exp versus ln) or a *syntactic* slip (assignments written where expressions belong, bare function names without brackets). What is entirely absent from that list is any friction about program structure, because you were never in a position to have one. You cannot record an error you were never given the opportunity to make.

The measured evidence that walk-the-code helped is also weaker than it looks. Blank errors dropped from "English phrase pasted as code" to zero across three builds. That is a real improvement in one narrow failure mode: knowing that the thing between the brackets has to be a Python expression. It is not evidence that you can write code.

### 2.2 Pure Python was correct, and is now the ceiling

No NumPy, no PyTorch, no frameworks, everything from scratch. For 44 builds that was the right call and it is why you can actually explain attention rather than recite it. Keep the artefacts, keep the pride, and retire the constraint.

You cannot build a comprehensive AI system in pure Python loops. You cannot train anything. You cannot profile anything meaningful, because the profile of a Python loop tells you about Python, not about the algorithm. You cannot touch a GPU. Every single topic in modules 11 through 14, the kernel, compile, distributed and inference material, was taught as arithmetic about systems you have never run. You computed that a 1 GB all-reduce moves 1.5 GB and takes 15 ms on NVLink. You have never run an all-reduce.

In v2 the default medium is PyTorch, and from-scratch appears exactly once per new concept as a twenty line numerical check that the library does what you think it does. That check is where the pure Python instinct earns its keep: it is the fastest way to confirm you actually understand a mechanism, and it costs twenty minutes instead of a build.

### 2.3 The record tracks lessons, not artefacts

You have 52 revision notes, 66 skills and a mastery graph. You have no experiment log, no benchmark numbers, no checkpoints, no deployed services. `SUMMARY.md` indexes builds. `CAPSTONE.md` audits eight rungs and finds two solid, three partial, three missing.

The structural fix is to change the unit of progress. In v1 a build is a file with blanks that runs and prints a number. In v2 a **system** is a thing that runs on real hardware, produces a metric that can be compared to a published baseline, and is either deployed or reproducible from a single command. Systems have experiment logs attached. That is what a portfolio is made of, and it is what a recruiter, a hedge fund quant team, or a co-founder can actually evaluate.

### 2.4 Compute is the bottleneck and it is cheap now

This is the part that should annoy you, because the numbers are absurd.

Karpathy's `nanochat` d24 model, roughly 1.38B parameters trained on about 8.8B FineWeb-edu tokens, matched GPT-2's CORE score in 3.04 hours on one 8×H100 node for about **73 dollars**, achieved 29 January 2026. The original GPT-2 run cost OpenAI on the order of 43,000 dollars. The speedrun tier of the same repo is now roughly 1.65 hours on 8×H100, about 48 dollars at on-demand rates and about 15 dollars on spot.

`modded-nanogpt` record 86 reaches 3.28 validation loss on FineWeb in **1.266 minutes on 8×H100**, dated 27 May 2026. That is about 0.17 GPU-hours. Under one dollar per run. You could run four hundred architecture ablations for the price of a textbook, and each one would teach you more about optimisers and attention variants than any explanation I can write.

Spot H100 capacity floors around 0.45 to 1.00 dollars per GPU-hour on marketplaces, and A100 80GB spot floors near 0.13 to 0.27. Kaggle gives roughly 30 free GPU-hours per week on a P100. Modal gives 30 dollars of free credit a month with per-second billing.

Three hundred dollars buys roughly 170 to 300 spot H100-hours. That is about four full nanochat pretraining runs at on-demand rates or twenty at spot rates, plus hundreds of modded-nanogpt ablations, plus dozens of LoRA fine-tunes. It is not enough for frontier scale anything. Roughly 10^20 FLOPs, which is 2019 territory. It is more than enough to convert three missing capstone rungs into evidence.

The correct read of your capstone audit is that you were right about the diagnosis and wrong about the size of the obstacle. It is fifty dollars, not a research lab.

### 2.5 Where else your framing is off

**"The course just touched the basics" understates it in one direction and overstates it in another.** The conceptual coverage is genuinely broad and genuinely current for a 2025 syllabus. Someone who can explain MLA, FlashAttention tiling, ZeRO sharding, GRPO's uniform-group failure and superposition in SAEs has real conceptual range. What is thin is not the concepts, it is that every one of them is held at the level of a worked arithmetic example rather than a running system. You do not need to relearn the concepts. You need to attach each one to hardware.

**"I need it tailored to building comprehensive and complex AI systems" needs a definition or it becomes a wish.** In v2 "complex system" means one of exactly four things, and each has a concrete completion test:

1. A model you trained end to end, with a validation metric, a seed spread over at least three seeds, and a compute-matched baseline.
2. A serving stack you deployed, with measured TTFT, inter-token latency, and goodput under load.
3. A kernel you wrote that beats a reference implementation on real hardware, with a roofline analysis explaining why.
4. A product that a person who is not you has used, ideally paid for.

Anything that does not land in one of those four is a study exercise, which is fine, but it does not count as a system and does not go in the portfolio.

**"Latest in AI work, models, frontier work" is a maintenance problem, not a content problem.** Any syllabus that hardcodes the frontier is stale in three months. vLLM shipped eleven minor versions between November 2025 and August 2026. PyTorch moved to a two month release cadence and is on 2.13. FlashAttention 4 landed in March 2026 and is still a PyPI pre-release in August. So v2 does not hardcode a frontier module. It hardcodes a **weekly frontier ingest** into the same database that already runs your insight loop, and a rule that every track has a live "current as of" section regenerated from that ingest. Section 6 gives you the August 2026 snapshot to start from.

---

## 3. The replacement pedagogy

You asked for: no blanks, explain each line simply as a beginner would need, mention the important Python rules, and then I write the code myself.

I am giving you that with one change to the ordering, and the change matters more than anything else in this document.

### 3.1 The loop

**Old loop:** walk the pre-written file, define every token, point at the blank, he fills the blank.

**New loop:**

```
1. CONCEPT      one to four concepts, each with its own worked number      (unchanged from v1)
2. DESIGN       the interface, the shapes, the invariants, the failure modes
3. RULES        the specific Python constructs this build needs, with their gotchas
4. TESTS        a failing test suite, handed to you, that defines "done"
5. WRITE        you write the whole file, from empty, alone
6. HINTS        a four rung ladder, only when you ask, never skipping rungs
7. REVIEW       line by line walk of YOUR code, then diff against reference
8. RECORD       insights, error classification, mastery, revision note
```

Steps 1, 3 and 7 are the "explain every line simply" you asked for. The difference is *where* step 7 sits. Explanation of a reference solution before you write is input you will nod along to. Explanation of your own code after you have fought a failing test for twenty minutes is the only kind that sticks, because you already have a stake in every line.

Step 4 is the load-bearing addition. A failing test suite does three things a blank cannot. It defines done without ambiguity. It gives you a feedback loop that does not require me. And it teaches you the actual professional workflow, which is read the spec, write the thing, watch it fail, fix it.

### 3.2 What each step contains

**Step 2, the design brief.** Written in plain English, no code. For example, for a rotary embedding build:

> You are writing one function. It takes a query vector and a position index. It returns a vector of the same length, rotated by an angle proportional to the position. The rotation happens in pairs: element 0 and element 1 form a 2D point that gets rotated, then elements 2 and 3, and so on. The angle for pair k at position i is i times theta to the power of negative 2k over d. The invariant that matters: if you rotate the query by its position and the key by its position, the dot product between them depends only on the difference between the two positions. The test checks exactly that invariant, at four different position pairs. The most common way this goes wrong is rotating both vectors by the same position, which makes every score identical.

That last sentence is drawn from your own error log. You made exactly that mistake in build 10.

**Step 3, the Python rules card.** Between three and six entries, each in the form `construct → what it means → the one rule that trips people`. Only constructs this build actually needs, and weighted toward whatever is currently open in your error taxonomy. Example:

```
zip(a, b)          pairs up two sequences, stops at the shorter one
                   RULE: it returns an iterator, not a list. list(zip(a,b)) if you need to reuse it.

range(0, n, 2)     0, 2, 4, ... up to but NOT including n
                   RULE: the stop value is always excluded. range(0,4,2) is [0,2], not [0,2,4].

a[i:i+2]           a slice: a new list with two elements starting at i
                   RULE: slicing copies, indexing does not. a[0] is an element, a[0:1] is a list.

f(x) vs f           f runs the function. f on its own IS the function object.
                   RULE: this is your #2 recorded error. Check every call site for brackets.
```

**Step 6, the hint ladder.** This is the part that protects the whole design. When you are stuck, you get rungs in order and you have to ask for each one:

```
Rung 1   Which assertion failed, and what that assertion is actually checking, in English.
Rung 2   Which region of your file the bug is in. Not the line. The region.
Rung 3   The concept or Python rule you have broken, stated as a rule, without reference to your code.
Rung 4   The line, with the reasoning.
```

The rule is that rung 4 is never given unprompted and never given first. If you burn through to rung 4 on more than a third of builds in a track, the concept density for that track was too high and the system should log that as an insight and reduce it. That is the same self-correcting mechanism that found the four-concept cap.

**Step 7, the review.** Three passes.

1. *Your code, line by line, in plain English.* What each line does, what the variable holds at that point, what type it is. This is the walk-the-code format you liked, applied to your own file.
2. *Diff against reference.* Not "yours is wrong", but for each difference: is this a correctness difference, a clarity difference, or a taste difference. Most differences will be taste, and saying so is important, because otherwise you will learn to write my code instead of learning to write.
3. *Error classification.* Every genuine mistake gets a category and goes into the error table. Categories are things like `expression-vs-statement`, `off-by-one`, `type-confusion`, `mutation-vs-copy`, `shape-mismatch`, `inverse-relationship`, `missing-call-brackets`, `state-in-wrong-scope`, `broadcasting`. This is the direct replacement for the prose "recurring frictions" list in v1 and it is the single mechanism that fixes your stated complaint, because the top open categories get injected into step 3 of every subsequent build.

### 3.3 What I write and what you write

This has to be enforced mechanically, not by good intentions, because in a live session the path of least resistance is always for me to just write it.

**I write:** test suites, data loading, plotting and reporting, argument parsing, logging, config files, CI, Dockerfiles, anything that touches an external API, and any code in a language that is not the point of the lesson.

**You write:** every function that is the concept. In v1 that was one line. In v2 it is the module.

**Enforcement:** a `PreToolUse` hook that blocks Write and Edit against the current build's solution path while the build state is `awaiting_student`. If I try to write your file, the tool call fails. You unlock it with `/faiz-unlock` and that unlock is recorded in the database and shows on your dashboard as a skipped build. Not a punishment, just an honest number, because a portfolio of builds you did not write is worth nothing and you should be able to see the ratio.

### 3.4 What carries over unchanged

- The four-concept cap. Proven twice in one session, do not touch it.
- One idea per message, wait for the answer, reveal the reasoning not just the answer.
- Define every new term in one sentence plus an analogy. Never more.
- Anchor every new topic to something you already shipped.
- On a wrong answer, say what was right first, correct gently, give the one line reason, re-check with a variation.
- Every new concept carries its own worked number.
- The insight loop: load accumulated teaching insights before a lesson, distil one or two new ones after.

---

## 4. The two modes

Both modes write to the same database. That is the point. Free building has to populate the same skills, mastery, insights, revisions and error tables as structured learning, otherwise you end up with two disconnected systems and the whole feedback architecture you already built stops working.

### 4.1 Course Mode

**Invoked by:** `/faiz-learn [track]` or `/faiz-learn next`

Structured, syllabus driven, one track at a time. The full eight step loop from section 3.1. Concepts come from the curriculum in section 5. A track is not complete until its system exists and its metric is logged.

Course Mode owns the *breadth* guarantee. Left to your own devices you will build agents and skip kernels, because agents are fun and kernels are painful. The syllabus exists to stop that.

### 4.2 Build Mode

**Invoked by:** `/faiz-build "<what you want to build>"` or `/faiz-build venture:<id>`

You bring the thing. The system:

1. **Scopes** it into a milestone spine, between three and seven milestones, each independently runnable and independently testable. It states explicitly what is out of scope for v0. Scoping is where most solo projects die, so this step is not optional and not skippable.
2. **Extracts concepts just in time.** Whatever the milestone requires that you have not met before becomes a concept card, gets a skill row, gets a revision note, and enters spaced repetition. Building a RAG pipeline and hitting reranking for the first time creates the reranking skill exactly as if the syllabus had delivered it.
3. **Runs the same eight step loop per milestone,** with the interruption level under your control.
4. **Flags syllabus collisions.** If a build needs something the syllabus covers in a track you have not reached, the system says so and offers either a just-in-time mini-lesson or a jump. Your choice, recorded either way.

**The depth toggle you asked for.** Two settings, switchable mid build:

- `explain` (default). Full loop. Design brief and Python rules card before you write. This is the more interactive mode you described.
- `flow`. You write first. No pre-teaching. Explanation arrives only at review. For when you know roughly what you are doing and stopping to be taught breaks concentration.

There is a third state that you should be able to reach and that most learning systems refuse to offer:

- `ship`. I write it, you review it, nothing is recorded as a skill. For genuine boilerplate and for when a deadline matters more than learning. Honest, logged, and does not pollute the mastery graph with things you did not do.

### 4.3 What is shared

| Table | Course Mode | Build Mode |
|---|---|---|
| `skills`, `mastery` | writes | writes |
| `insights` | writes | writes |
| `revisions` | writes | writes |
| `errors` | writes | writes |
| `experiments` | writes | writes |
| `systems` | writes | writes |
| `streak` | writes | writes |
| `tracks` | drives | reads, flags gaps |
| `ventures` | reads | consumes |

The insight loop is mode aware. An insight recorded during a Build Mode session is tagged with mode and with the build, so the system can learn things like "he skips the design brief when in flow mode and then makes shape errors", which is exactly the kind of second order pattern the v1 loop was designed to catch and never had enough surface area to find.
---

## 5. Curriculum v2: the depth ladder

Eleven tracks. Roughly nine to twelve months at ten to fifteen hours a week. Every track ends in a **system** as defined in section 2.5, not a build. Every track has a completion test that involves a number.

The ordering is not negotiable in the first four tracks. T0 through T3 are prerequisites for everything else and skipping them is how you end up back where you are now, able to explain things you cannot build.

### T0. Python and engineering for machine learning

**Why first:** this is the missing prerequisite. It is the entire content of your complaint. Nothing else in this curriculum works until you can start from an empty file and end with a tested, typed, profiled, version controlled module.

**Concepts:** modules and imports and why circular imports happen. Virtual environments with `uv` and why pinned Python matters. `pytest`, fixtures, parametrised tests, and what a good assertion looks like. Type hints and what `mypy` actually catches. `ruff` and what a linter is for. Dataclasses. Context managers. Generators and why they matter for data loading. Exceptions and when to raise versus return. `cProfile` and reading a cumulative time table. `git` beyond commit and push: branches, rebase, bisect. Reading a stack trace properly. The debugger, `pdb` or the IDE one, because print debugging is where a lot of your time is going and you probably do not know it.

**Systems:** a small library, written by you from empty files, with a real test suite, CI on GitHub Actions, type checking, and a published package. The library itself is trivial on purpose. The point is the scaffolding.

**Completion test:** you can create a new project, add a dependency, write a failing test, make it pass, profile the hot path, and push with green CI, in under fifteen minutes without looking anything up.

**Note:** you will want to skip this track. Do not. It is four to six weeks and it is the difference between v2 working and v2 being v1 with different words.

### T1. PyTorch fluency

**Why:** the medium changes here. Everything from T2 onwards is PyTorch.

**Concepts:** tensors, shapes, strides, views versus copies, and why `.contiguous()` exists. Broadcasting rules and the three ways they silently do the wrong thing. `autograd`, `requires_grad`, the graph, `backward()`, and `detach()`. `nn.Module`, parameters, buffers, state dicts. Optimisers and what `zero_grad()` actually clears. `DataLoader`, workers, collation, pinned memory. Devices and the cost of a `.cpu()` call in a loop. Mixed precision, `autocast`, `GradScaler`. `torch.compile` and what a graph break is. `nn.LinearCrossEntropyLoss` in PyTorch 2.13, which fuses the final projection with cross entropy and cuts peak memory by up to 4x on large vocabularies, which matters the moment you start pretraining.

**The from-scratch bridge:** re-derive your own micrograd against `torch.autograd` on the same function, and show the gradients match to floating point tolerance. That is the twenty minute check that makes the library stop being magic.

**Systems:** re-implement builds 3 through 7 (micrograd, tiny net, neuron, layer, XOR MLP) as a single PyTorch module with tests, then train the XOR net and plot the loss curve. Same content you already know, new medium, so the only thing you are learning is the tool.

**Completion test:** given a shape mismatch error you have never seen, you diagnose it from the traceback without running anything.

### T2. Train a real model, and learn how to know whether it worked

**Why:** this is where the capstone rungs get filled and where module 20 stops being theory.

**Concepts:** the full pretraining loop. Data: tokenisation at scale, sharding, streaming, and why FineWeb-edu is the standard student dataset. Learning rate schedules, warmup, weight decay, gradient clipping. Checkpointing and resumption. Mixed precision and FP8 in practice. Muon as an optimiser, which is now confirmed in frontier production and not just a research curiosity, and why it converges faster than AdamW on this workload. Weights and Biases or equivalent for run tracking. Then the research method from your module 20, applied for real: seeds and spread over at least three runs, compute matched baselines, and single component ablations.

**Systems:**
1. Reproduce `modded-nanogpt` at the current record. Then run twenty ablations of your own, one component at a time, each under a dollar. This is the single best learning-per-pound harness that exists.
2. Run `nanochat` speedrun tier to a real CORE score. Roughly 15 to 48 dollars.
3. Run `nanochat` d24 to GPT-2 parity. Roughly 73 dollars.

**Completion test:** you produce a results table with mean and spread over three seeds, a compute matched baseline, and an ablation, and you can point at a result of your own and say honestly whether anything was measured. Capstone rungs 3, 5 and 7 close here.

### T3. Modern architecture, as of 2026

**Why:** your module 7 to 10 content describes the 2024 consensus. That consensus broke. Section 6.1 has the detail.

**Concepts:** fine grained MoE at high expert counts and low active fractions, top-k routing, shared experts, load balancing, and why active parameter fraction fell to roughly 3 to 4 percent. LatentMoE, routing and computing experts in a reduced dimension to cut memory bandwidth and all-to-all traffic. Linear attention and the delta rule: Gated DeltaNet, and Kimi Delta Attention as a finer gated extension. Hybrid stacking patterns and their ratios. Sparse attention: blockwise top-k selection and token level sparsity. Residual stream engineering: hyper-connections and the manifold constraint that restores the identity mapping. Sliding window plus global hybrids. Mamba-2 with attention anchors at production scale.

**Systems:** build a small hybrid attention MoE from PyTorch primitives, roughly 100M to 300M parameters, with a 3:1 linear to full attention ratio and 16 experts top-2, and train it on FineWeb with modded-nanogpt as the harness. Then ablate: pure attention versus hybrid, dense versus MoE, with and without a shared expert. Each ablation is a few dollars.

**Completion test:** a results table showing what each architectural component was actually worth on your budget, with seed spread, and an honest statement of which differences were inside the noise.

### T4. Kernels and the hardware

**Why:** you did modules 11 and 12 as arithmetic. Now you run them.

**The ladder, and only descend when the level above measurably fails you:** `torch.compile` → Helion → Triton and Gluon → CuTe DSL.

**Concepts:** roofline and arithmetic intensity, now measured rather than computed by hand. Occupancy and why it is not the metric people think. Memory hierarchy on Blackwell, including Tensor Memory as a new explicitly managed 256 KB per SM tier. `tcgen05` replacing warp synchronous `wgmma` with per thread MMA issue. CTA pair execution as a first class tiling dimension. The FlashAttention 4 thesis, which is the most important single idea in this track: **tensor core throughput doubled while everything else scaled slowly or not at all**, so the bottleneck has moved from matmul to softmax, exponentials, rescaling and epilogues. That is why FA4 emulates the exponential in software with a polynomial and makes softmax rescaling conditional. Autotuning as a first class activity.

**Systems:** write a fused softmax in Triton and beat the unfused PyTorch version. Write a tiled attention forward pass in Helion and get within a stated factor of FlashAttention. Produce a roofline plot for each, with a written explanation of why the measured point sits where it does. Rent B200 or H100 time for one concentrated week rather than dribbling hours.

**Completion test:** a kernel you wrote that beats a reference on real hardware, with a roofline analysis that predicted the result before you measured it.

**Note on your MacBook Air:** you can write and debug Triton and Helion syntax locally and you cannot run CUDA kernels. PyTorch 2.13 did ship FlexAttention on Metal with hand written kernels, roughly 12x over SDPA on sliding window shapes, so Apple Silicon is now a real target for attention experimentation. But if the Air is not an M5, you have no GPU matrix units and the memory bandwidth ceiling of 100 to 153 GB/s is the binding constraint on anything generative. Treat the Air as a development machine and rent the compute.

### T5. Inference and serving

**Why:** modules 14 and 15 taught paged KV, continuous batching and speculative decoding as arithmetic. Now you serve something and measure it.

**Concepts:** pin a vLLM version, because the API surface moves weekly and any blog post older than two months is wrong. The V1 engine and Model Runner V2. Prefix caching as a storage hierarchy problem across HBM, RAM, SSD and remote, not as a hash table. Disaggregated prefill and decode: why prefill is FLOP bound and decode is bandwidth bound, why they want different tensor parallel degrees, and the hard requirement for RDMA interconnect between nodes. Decode context parallelism, which shards KV by sequence position rather than by head, and exists because MLA forces full replication of the compressed latent once tensor parallelism exceeds the KV head count. Speculative decoding in its current form: EAGLE-3 as the commodity baseline, then parallel drafting (P-EAGLE, DFlash, DSpark) which decouples draft cost from block length, and multi token prediction now shipping as trained weights so you get speculation with no separate drafter. Structured decoding with XGrammar. FP8 KV cache and its break even at roughly 7k tokens, below which it is a net loss.

**Systems:** serve a 7B to 30B model on a rented GPU under vLLM. Measure TTFT, inter token latency and goodput across batch sizes and produce the curve. Turn on FP8 KV cache and measure the break even yourself. Add a speculative drafter and measure acceptance length and the throughput decay as concurrency rises, which is the honest framing of all speculative decoding.

**Completion test:** a serving benchmark report with your own numbers, and a written prediction of what each configuration change would do that you made before running it.

### T6. Post-training and RL

**Why:** your modules 15 and 16 taught REINFORCE, PPO clipping, GRPO, DPO and reward modelling. The field moved.

**Concepts:** SFT properly, including packing and loss masking. Preference optimisation and why DPO won on cost, one stage and two models instead of two stages and three. The GRPO family as it actually exists in 2026: clip-higher and dynamic sampling from DAPO, sequence level ratios from GSPO, importance weight clipping rather than update clipping from CISPO, and the reshaping kernels that followed. The failure modes with names now: uniform group degeneracy, which you already know, and the formal length bias result showing that no weighting scheme can be both gradient unbiased and length invariant, which means Dr. GRPO did not fix GRPO, it traded one problem for another. Entropy collapse in RLVR and the finding that it is not uniformly harmful and is driven mainly by positive advantage tokens. RLVR versus rubric graded rewards for non verifiable domains, and reward hacking as something now measured in controlled environments rather than argued about. The single most useful result for planning: the ScaleRL finding that recipe choices split into those that move the asymptote and those that only move compute efficiency, and that most of what people tune only moves efficiency.

**Systems:** GRPO on a small model against a verifiable task, using `verifiers` for the environment and `prime-rl` or TRL AsyncGRPO for the loop, or Unsloth if you are on a single GPU. Then reproduce the uniform group failure deliberately and fix it. Then run a rubric graded reward on a non verifiable task and try to hack your own reward function, which is the fastest way to internalise Goodhart.

**Completion test:** a reward curve, an entropy curve, and a written account of a failure mode you caused on purpose and then fixed.

### T7. Agents, harnesses and evaluation

**Why:** this is where your FaizOS system itself lives, and where the venture arm will be built.

**Concepts:** harness design, which matters as much as model choice. The Anthropic long running agent pattern: an initializer agent that writes a structured feature list, a git repository, progress files and a setup script, then a coding agent doing one feature per session with end to end testing before the session ends. Context engineering, compaction, tool clearing. Evolving playbooks and the context collapse failure mode that comes from monolithic rewriting. The two hard empirical findings from 2026 agent evaluation: sequential scaling plateaus once accumulated context passes roughly 96k to 112k tokens, well below the nominal limit, and there is a **verification gap**, where correct solutions appear more often as you sample more but agents cannot select them, so self-choice lags pass@k. The practical consequence is that marginal test time compute is better spent on a better verifier than on more samples. pass@1 as reliability versus pass@k as capability, and the fact that the same low pass@1 implies opposite fixes depending on the gap. Agentic RL and long horizon credit assignment. Environment synthesis, which is the real 2026 data problem.

**Systems:** rebuild FaizOS itself as the exercise. It is already an MCP server with hooks and a database, and v2 needs a substantial rewrite, so you build your own learning system as your agent track project. That is the highest leverage build available to you because you use it every day and every defect is felt. Then run an agent against a real benchmark harness and get a number.

**Completion test:** FaizOS v2 running, plus a scored run on a public agent benchmark.

### T8. Multimodal and retrieval

**Concepts:** ViT and patchification, and why context cost is quadratic in resolution. CLIP style contrastive alignment. VLM fusion and the token budget consequence, where five images can outweigh a thousand word question. Diffusion as supervised noise prediction, and rectified flow straightening the path from roughly fifty steps to four. Production retrieval: hybrid dense and sparse, wide cheap recall then reranking for precision, and the specific failure where a chunk at rank 37 is retrieved and still never reaches a top-5 context.

**Systems:** a retrieval system over your own corpus with a measured recall@50 and precision@5, before and after reranking. A small VLM fine tune.

### T9. Safety, interpretability and evaluation as a discipline

**Concepts:** SAEs and superposition, now trained rather than described. Prompt injection as an architectural problem, since instructions and fetched content are the same tokens and there is no instruction channel, so the defence is tool gating rather than prompting. Scalable oversight, debate, weak to strong generalisation and why it exceeds its teacher where distillation cannot. Evaluation as a discipline: contamination, seed variance, compute matched baselines, and the fact that most published gains sit inside the noise.

**Systems:** train an SAE on a small model's activations and find an interpretable feature. Build a gated tool harness and demonstrate a blocked injection.

### T10. Ship

**Concepts:** MCP servers under the current spec, which went stateless in the July 2026 revision, eliminating session management so servers run behind plain load balancers. That is a meaningful cost reduction for a solo builder. Distribution surfaces and their real constraints, covered in section 8.5. Packaging, licensing, pricing, and outcome based pricing as the emerging norm for agent products.

**Systems:** one published MCP server or desktop extension, and one product with a user who is not you.

### Track summary

| Track | Weeks | Systems | Cost | Closes capstone rung |
|---|---|---|---|---|
| T0 Python and engineering | 4 to 6 | 1 | 0 | tooling |
| T1 PyTorch fluency | 3 | 1 | 0 | |
| T2 Train a real model | 4 | 3 | ~120 | 3, 5, 7 |
| T3 Modern architecture | 5 | 2 | ~60 | 1, 2 |
| T4 Kernels | 5 | 3 | ~80 | 4 |
| T5 Inference and serving | 4 | 2 | ~40 | 6 |
| T6 Post-training and RL | 5 | 3 | ~60 | 8 |
| T7 Agents and harnesses | 6 | 2 | ~20 | |
| T8 Multimodal and retrieval | 4 | 2 | ~20 | |
| T9 Safety and interpretability | 3 | 2 | ~20 | |
| T10 Ship | ongoing | 2 | ~30 | |

Costs are indicative GPU spend at spot rates as of 13 August 2026 and will drift. Total is roughly 450 dollars spread across nine to twelve months, and the first 120 dollars buys the majority of the portfolio value.

---

## 6. The frontier update: what changed while you were learning

This section is the August 2026 snapshot. It is not the permanent content of the syllabus. Section 9 specifies the weekly ingest that keeps it current.

### 6.1 The attention consensus collapsed

This is the single biggest change relative to your module 7 to 10 content, and it is the thing to internalise. In 2024 and early 2025 the answer to "what attention do I use" was GQA, or MLA if you cared about KV cache. That monoculture is gone. Every major lab now runs something different:

| Model | Attention |
|---|---|
| Qwen3.5 and 3.6 | Gated DeltaNet linear attention plus Gated Attention, 3 to 1 |
| Kimi K3 | Kimi Delta Attention plus Gated MLA, roughly 69 to 24 across 93 layers |
| GLM-5 | MLA with DeepSeek Sparse Attention layered on top |
| DeepSeek V4 | Compressed Sparse Attention plus Heavily Compressed Attention |
| MiniMax M3 | MiniMax Sparse Attention, blockwise top-k |
| MiniMax M2.5 | full multi head attention, deliberately, for reliability |
| Gemma 4 | sliding window at 512 or 1024 plus global |
| NVIDIA Nemotron 3 | Mamba-2 with periodic attention anchors |

Two things follow. First, sparse attention is now the price of admission for a million token context, and the clearest sign it has become an industry primitive is that GLM-5 shipped DeepSeek's DSA rather than inventing its own. Second, hybrid Mamba plus transformer reached genuine production scale with Nemotron 3 Super at 120B total and 1M context, where previously this was 7B class territory.

The teaching consequence for you: your RoPE, GQA and MLA builds are still correct and still the right foundation. They are now the *baseline* against which the current mechanisms are variations, which is exactly the anchoring structure the Brick Method already uses.

### 6.2 MoE went extremely sparse

Active parameter fractions across current open models: DeepSeek V4-Pro roughly 3.1 percent, Kimi K3 3.7 percent, Qwen3.5 4.3 percent, GLM-5 5.4 percent, Nemotron 3 Super 10.5 percent. Expert counts hit 896 in Kimi K3 with top-16 and 2 shared, and 512 in both Qwen3.5 and Nemotron 3.

**LatentMoE** appeared independently at Moonshot and NVIDIA in the same quarter: route and compute experts in a reduced latent dimension to cut memory bandwidth and all-to-all communication. Convergent invention across two labs is usually a sign that an idea is structurally forced rather than clever.

The consumer consequence matters for you specifically: a 35B-A3B MoE at 4 bit beats a 27B dense at 4 bit on both memory and speed, because only about 3B parameters are active. MoE changed the consumer calculus more than quantisation did.

### 6.3 Precision fell to four bits in production

FP8 is now the floor. Qwen3.5 runs a native FP8 pipeline for activations, MoE routing and GEMM with BF16 preserved in sensitive layers. Mistral Large 3 ships FP8. GLM-5 ships an FP8 variant.

FP4 arrived in shipped models, which is the genuinely new thing. DeepSeek V4 runs FP4 experts with FP8 elsewhere. Kimi K3 uses MXFP4 weights and MXFP8 activations via quantisation aware training. Nemotron 3 trained in NVFP4 with selective BF16 in the final 15 percent of the network. The research base is a 12B parameter NVFP4 run over 10T tokens matching FP8 loss and downstream accuracy, using random Hadamard transforms for outliers, 2D quantisation, stochastic rounding for gradients and selective high precision layers.

Practical decision rule: on Blackwell, NVFP4 for weights on models at or above 30B, MXFP4 where the checkpoint already ships that way, FP8 as the safe default everywhere else. NVFP4 accuracy recovery improves with scale, roughly 99 percent at 70B and above but 95 to 98 percent at 7B to 14B, which is the opposite of the intuition most people have.

### 6.4 Optimisers: Muon is confirmed at frontier scale

DeepSeek V4 states Muon for faster convergence and greater training stability. That is the first explicit frontier scale production disclosure. Theory caught up in parallel with scaling law work. I found no evidence of Shampoo, SOAP or true second order methods in production frontier runs.

For you this is directly actionable, because `modded-nanogpt` already uses Muon and its records are built on it. You will meet it in T2 as a working component rather than as a paper.

### 6.5 Residual stream engineering became a thing

DeepSeek's manifold constrained hyper-connections restore the identity mapping property that plain hyper-connections break, via a manifold constrained projection, and shipped in production in V4. Kimi K3's Attention Residuals is a parallel thread. Follow on work already exists for GNNs and SSMs. This is a direct descendant of the residual lesson you already built, where 30 blocks deep gave RMS 27.7 with residuals versus 0.07 without.

### 6.6 Post-training moved past plain GRPO

Covered in T6. The short version: the 2026 default is not GRPO, it is a GRPO family recipe with clip-higher, dynamic sampling and either a sequence level or reshaped importance ratio, run off policy. DAPO, GSPO, CISPO and VESPO are all shipped loss types in mainstream libraries now, not papers. Rollout staleness and train versus inference numerical mismatch are treated as first class bugs, with dedicated tooling.

The two findings worth memorising:

- **ScaleRL:** compute to performance curves for RL are sigmoidal, not power law, and recipe choices split into those that move the asymptote and those that only move compute efficiency. Loss aggregation, normalisation, curriculum and off policy algorithm choice mostly move efficiency. This is the RL analogue of your module 26 Amdahl lesson and it should be taught the same way.
- **The length bias impossibility result:** no length based weighting scheme can be simultaneously gradient unbiased and length invariant for group relative outcome reward policy optimisation. GRPO is approximately length invariant but biased. Dr. GRPO is unbiased but not length invariant. It is a structural tradeoff, not a bug someone will fix.

### 6.7 Inference: the interesting layer moved above the engine

Prefix caching is default on and near zero overhead, so the work moved to tiered storage across HBM, RAM, SSD and remote. Disaggregated prefill and decode is the production shape, with the hard caveat that without RDMA it falls back to TCP and should only be used for testing. Decode context parallelism showed a genuinely large win on MLA models, sustaining 6,091 tokens per second per GPU at 512 concurrency versus a baseline that peaked at roughly 1,863 at 64 concurrency before running out of memory.

Speculative decoding changed the most. Parallel drafting displaced autoregressive drafting because EAGLE-3 needs K sequential forward passes for K draft tokens, so draft latency scales with speculation depth. P-EAGLE, DFlash and DSpark decouple draft cost from block length, with P-EAGLE showing roughly 30 percent higher acceptance length at K=7 on code benchmarks. And multi token prediction now ships in weights, so for models with MTP heads you get speculation with no drafter to train or host.

### 6.8 Kernels: the bottleneck moved off matmul, and Python became competitive

FlashAttention 4 is the reference text for the current era. Its framing thesis is that Blackwell exhibits asymmetric hardware scaling, tensor core throughput doubles while other functional units scale slowly or not at all. Everything else in the paper follows: software emulated exponentials via polynomial approximation because the special function unit did not keep up, conditional softmax rescaling to cut non matmul work, tensor memory and 2-CTA MMA mode to cut shared memory traffic. Results of roughly 1.3x over cuDNN on B200 and 2.7x over Triton.

The structural change for kernel authors is that it is written in CuTe DSL embedded in Python rather than C++ templates, with 20 to 30x faster compile times. Combined with PyTorch 2.13 adding a CuTe DSL backend to Inductor, and Helion arriving as a PyTorch Foundation hosted tile level DSL with reported B200 geomean of 3.27x over eager versus 2.7x for torch.compile and 1.76x for hand written Triton, the conclusion is that **C++ template metaprogramming is no longer the entry fee for writing state of the art kernels**. That is the single fact that makes T4 feasible for you at all.

### 6.9 Agents: two hard results

The verification gap and the context ceiling, both covered in T7. Together they say that in 2026 marginal test time compute is better spent on a better verifier or selector than on more samples or longer traces. Separately, OSWorld 2.0 with 108 long horizon computer use tasks, median task around 1.6 hours of human operation, has the best model at 20.6 percent binary success. ARC-AGI-3 has frontier models at 0.5 percent or below where humans solve 100 percent with no prior training. Computer use and interactive novel environments are dramatically unsolved, which is where the research opportunity actually is.

### 6.10 The structural point about who publishes

The open weight frontier is now almost entirely Chinese, DeepSeek, Qwen, Moonshot, Z.ai and MiniMax, plus Mistral, NVIDIA and Google. Meta has shipped nothing on its open weights organisation since November 2025 and pivoted to a closed family. Anthropic, OpenAI, Google for Gemini, and xAI disclose zero architecture: no parameter counts, no MoE configs, no attention variants, no context scaling method. Any specific architectural claim about those models circulating publicly is not primary sourced.

For your syllabus this means the models you can actually study are the Chinese open weight releases plus Gemma, and Gemma 4's model card is unusually detailed. Study those. Do not build a mental model of the frontier from speculation about closed models.
---

## 7. The compute plan

This is the highest leverage section in the document and it is the shortest.

### 7.1 Indicative rates, captured 13 August 2026

| GPU | On demand floor | Spot floor | Where |
|---|---|---|---|
| H100 SXM | ~1.89 to 3.29 | ~0.45 to 1.00 | UpCloud, RunPod, Prime Intellect, Vast |
| H200 | ~1.60 to 2.14 | ~0.40 | Vast, Prime Intellect |
| A100 80GB | ~0.27 to 1.59 | ~0.13 | Vast, RunPod |
| B200 | ~3.75 to 6.79 | ~3.06 | Vast, Verda, Prime Intellect |
| RTX 4090 | ~0.74 | | RunPod |

All figures indicative, per GPU hour, USD, and drifting. Verify before committing.

**Free tiers.** Kaggle Notebooks give roughly 30 GPU-hours per week on a P100 with no credit card, which is the better free tier for anything sustained. Colab free gives a T4 with a 12 hour session cap and no availability guarantee. Modal gives 30 dollars of credit a month with per second billing, which suits intermittent solo work better than a rented box because you pay nothing while idle.

### 7.2 The rule

Develop and debug on free tiers. Rent only when the script is known good. Use spot with checkpointing for the actual run. **Prefer 8 GPUs for one hour over one GPU for eight hours.** Same cost, eight times faster iteration, and every reference repository you will use is tuned for an 8 GPU node.

### 7.3 The budget

| Spend | Buys | Unlocks |
|---|---|---|
| 0 | Kaggle plus Modal credits | T0, T1, all development |
| 15 to 50 | one nanochat speedrun, plus 20 modded-nanogpt ablations | capstone rungs 3, 5, 7 |
| 120 | above plus nanochat d24 to GPT-2 parity, plus T3 architecture ablations | rungs 1, 2 |
| 300 | above plus a concentrated kernel week on B200 and a serving benchmark | rungs 4, 6 |
| 450 | the full curriculum | all eight |

Three hundred dollars is roughly 10^20 FLOPs. That is GPT-2 2019 territory, not GPT-3. It is not enough for frontier scale anything, meaningful RLHF at scale, or multi node experiments. It is enough to convert your entire capstone from understanding to evidence.

### 7.4 The MacBook Air

**Do:** write and debug PyTorch and MLX; run 4 bit models up to roughly 8B on 16 GB or 14 to 27B on 32 GB; LoRA fine tune small models overnight; run `mlx_lm.server` as a local OpenAI compatible endpoint for agent development; learn Helion and Triton syntax locally.

**Do not:** benchmark anything you intend to publish, because the Air is fanless and thermally throttles in ways that MacBook Pro numbers will not show; attempt CUDA kernel development locally; expect Blackwell FP4 behaviour to replicate on Metal.

Two useful facts. MLX now has a real CUDA backend, so you can prototype on the Air and run the same code on a rented NVIDIA box. And if the Air is an M5, its GPU neural accelerators make prompt processing roughly 4x faster but token generation only 1.2x faster, because decode is bandwidth bound and bandwidth only went from 120 to 153 GB/s. Good for long prompt agentic work, marginal for long generation.

---

## 8. The venture research arm

### 8.1 The blunt framing first

You asked for a research pipeline that produces buildable business ideas and feeds them into Build Mode. Before the design, three things you need to accept or the whole thing becomes a distraction generator.

**Idea supply is not your constraint.** You can generate ten plausible AI product ideas in an afternoon. You have shipped zero products. Adding an automated idea firehose to a system whose bottleneck is execution makes the bottleneck worse, not better. This is why the design below has a hard work in progress limit of one and a kill gate, and why those are enforced in the database rather than by intention.

**An LLM driven idea generator is weak at exactly the thing you want it for.** a16z's own 2026 note makes the point that models are still not very good at deciding what to build next. So the pipeline's value is not ideation. It is **evidence gathering**: systematically finding places where real people are complaining about a real problem, corroborating that signal across independent sources, and presenting it to you with the evidence attached. You make the decision. The machine does the grinding.

**Most of what you will read about this online is fabricated.** Roughly 70 percent of search results for questions like "vertical AI gross margins 2026" are programmatically generated marketing pages with invented statistics. My researcher found Crunchbase's own H1 2026 report stating that early stage funding totalled 589 billion dollars in Q2, in the same article that put the entire quarterly total at 205 billion. Early stage cannot be 2.9x the total. It is a typo in a primary source, almost certainly 58.9 billion. The corroboration gate in section 8.3 exists because of exactly this.

### 8.2 The market context, briefly

The capital market is irrelevant to you and that is good news. Global venture funding hit 510 billion dollars in H1 2026, but OpenAI and Anthropic alone took 217 billion of it, 43 percent of all global venture funding. In Q1, three megadeals took 67 percent of all AI capital and the remaining 1,543 deals split what was left. Global seed funding was about 12 billion in Q2 with only around 5 billion in rounds at or under 10 million dollars.

So you are not competing for capital. You are competing for **distribution** and for **problems the labs will not touch**. The pipeline should score on reachability without capital, not on total addressable market.

What the traction data actually teaches: Harvey went from 100 million ARR in August 2025 to 350 million by July 2026, at roughly 1,200 dollars per lawyer per month with 20 seat minimums, which is a 288,000 dollar minimum annual contract value sold through enterprise procurement. Sierra hit 100 million ARR in seven quarters on outcome based pricing. Both prove the category works. Neither is a motion you can execute. The transferable lessons are that the winning price point for vertical AI is over 1,000 dollars per seat per month or per outcome rather than 29 dollars a month, and that **an opportunity is stronger when the outcome is countable**: invoices reconciled, claims processed, filings submitted.

The durable defensibility, based on the Harvey case where frontier reasoning models jumping from roughly 60 to 90 percent accuracy compressed the differentiation window, is not model quality. It is owning a system of record, a regulated filing integration, a proprietary data loop, or a distribution surface the labs do not control. Model capability commoditises. Integration and liability do not.

### 8.3 Pipeline architecture

Five stages, and the corroboration gate is the one that matters.

**Stage 1, ingest.** Free tier only, daily cron, no spend. Sources with verified free programmatic access:

| Source | Access | Cost |
|---|---|---|
| Hacker News | Firebase API and Algolia search API | free, no key |
| GitHub issues and discussions | REST and GraphQL | free, 5,000 requests per hour authenticated |
| SEC EDGAR | full REST API at data.sec.gov | free, no key, User-Agent required |
| UK Companies House | developer API suite | free, key required |
| YC Requests for Startups | scrape | free |
| MCP official registry | REST API | free |
| Product Hunt | GraphQL | free tier, token |
| arXiv | API | free |
| Reddit | official Data API | free tier, commercial around 0.24 dollars per 1,000 calls |

Deliberately excluded at ingest: G2, Capterra, Upwork, Fiverr and the app stores. They have no public API, scraping them breaches terms of service, and the paid scraper route should only ever be used to validate an already shortlisted candidate, never for breadth.

**Stage 2, extract.** An LLM classifier over ingested text producing structured records: the job to be done, an importance score, and a dissatisfaction score. This is Ulwick's Outcome Driven Innovation instrument, and it fits complaint mining precisely, because "high importance, low satisfaction" is literally what a bug report or forum complaint encodes. Everything gets a source URL and a raw excerpt. Nothing is stored as a summary without its evidence.

**Stage 3, corroborate.** An opportunity advances only if it appears in **at least two independent source families**. A GitHub issue cluster plus a job posting spike counts. Three posts in the same Reddit thread does not. This single rule kills the large majority of false positives and it is cheaper than a better model.

**Stage 4, score.** Six axes, scored 1 to 5, weighted for your constraints rather than an investor's:

| Axis | Weight | What it asks |
|---|---|---|
| Opportunity gap | 2 | importance minus satisfaction, from stage 2 |
| Distribution reachability without capital | 3 | can you reach a hundred of these users with zero marketing budget |
| Lab absorption risk (inverted) | 3 | does this survive the next frontier release, or is it a prompt and a text box |
| Buildable to v0 in fourteen days | 3 | by you, part time, at your current skill level |
| Teaches you something on the curriculum | 1 | does building it advance a track |
| Regulatory and entity feasibility | 2 | see section 8.6, this is a gate not a score |

An idea scoring 5 on opportunity gap and 1 on reachability is worth nothing to you. That is the standard failure of RICE and ICE applied to a solo builder, and it is why the two custom axes carry the most weight.

**Stage 5, gate and hand off.** Maximum **one** active venture, enforced by a unique constraint in the database. A venture entering `active` state generates a scoped fourteen day v0 with a single falsifiable success metric, and hands it to Build Mode as a milestone spine. At day fourteen there is a mandatory kill review with three outcomes: continue with a new fourteen day metric, park with a written reason, or kill with a post mortem that writes back into the insights table. No fourth option, and no silent drift.

### 8.4 What the pipeline outputs

A weekly briefing, generated deterministically, containing: new corroborated opportunities with their evidence and scores, the status of the active venture against its fourteen day metric, and anything that failed the corroboration gate with the reason, because the failures are as instructive as the passes.

### 8.5 Distribution surfaces, and their real constraints

This is the part most opportunity research gets wrong, so here it is with the friction stated.

| Surface | Discovery | Payment rail | Solo accessible |
|---|---|---|---|
| Claude connectors directory, remote MCP | yes | no | **gated, submission needs a Team or Enterprise org** |
| Claude desktop extensions, MCPB | yes | no | **yes, separate form, no org gate** |
| OpenAI Apps SDK | yes | partial, external checkout works today and OpenAI takes no cut | yes |
| Chrome Web Store | yes, strong organic reach | **no, payments deprecated since February 2021** | yes, but bring your own billing and licence tracking |
| Shopify App Store | yes | yes, native and mature | yes, verify current revenue share |
| Salesforce AppExchange | yes | yes | high compliance burden |
| Slack, Notion | moderate | historically bring your own | yes |
| Official MCP registry | emerging | no | yes |

Two practical conclusions. Neither lab app store gives you a turnkey payment rail in 2026, though OpenAI is closer because external checkout works now and you keep 100 percent. And **the Claude MCPB desktop extension route is the only lab distribution surface with no organisation plan gate**, which combined with the July 2026 stateless MCP spec cutting hosting complexity makes it the lowest friction door available to you right now.

### 8.6 The two hard constraints in your specific situation

These gate everything downstream. Resolve them before you build anything commercial. Both are free to resolve and expensive to get wrong.

**UK student visa.** The gov.uk Student visa work page lists, verbatim, among the things you cannot do: **"be self-employed"**. What that page does not address, and therefore what I cannot state as fact, is company directorship, unpaid founder activity, holding equity, and the precise term time hour cap. Secondary sources discuss a director versus self employment distinction, but this is exactly where secondary sources are unreliable and the consequence of error is severe. This is factual regulatory context, not legal advice. Confirm with Durham's international student office or a qualified immigration adviser before anything else.

**Pakistan payment rails.** Stripe does not support Pakistan registered entities. Getting paid internationally as a Pakistani resident entity has historically required Payoneer or Wise or an SBP permitted export account. This pushes you toward one of three structures: a foreign holding entity, selling to customers who already earn in USD, or local rails with a hard revenue ceiling. My researcher could not verify current Stripe Atlas eligibility or SBP foreign currency retention rules from primary sources, so treat this as an open item to check rather than a settled fact.

These two interact. The self employment prohibition and the payment rail constraint jointly determine what entity structure is even available, and that determines which monetisation surface you can use. Sequence them first.

### 8.7 Seeded opportunities, with evidence

Not recommendations. Starting points with sources attached, for the pipeline to work on.

**Pakistani e-invoicing compliance.** Pakistan has mandatory e-invoicing phasing in under FBR Rule 150Q, with integration deadlines extended during 2026 and draft 2026 rules contemplating CCTV at point of sale. This is the strongest structurally evidenced opportunity in the set for your situation specifically: a compliance deadline creates non discretionary SME spend, it is a system of record integration and therefore defensible per section 8.2, it is invisible to frontier labs, you have local context a Bay Area founder does not, and it maps directly onto YC's stated Request for Startups entry on AI native compliance infrastructure. Two caveats. Deadlines have already slipped at least once, so regulatory timing is the main risk. And there are already incumbents in the niche. Verify current deadline status at fbr.gov.pk before committing anything.

**The USD earning Pakistani cohort.** Pakistani freelancer export earnings hit a record 1.76 billion dollars in FY2025-26, against total remittances of 41.6 billion. This is the highest value Pakistani customer segment for a solo software founder for one structural reason: they already earn in dollars. Selling PKR denominated software to Pakistani SMEs runs into a realistic willingness to pay of roughly 7 to 55 dollars a month and hard payment friction. Selling USD denominated tooling to Pakistani exporters does not. Note there is an unresolved discrepancy between the 1.76 billion export earnings figure and PSEB's 1.1 billion award framing, different measurement bases.

**Self maintaining APIs.** From YC's current Requests for Startups: agents that automatically update customer codebases when an API provider ships a breaking change. Narrow, technical, testable, no regulatory surface, and you can dogfood it on your own repositories. This is the highest fit with your curriculum because building it is T7 work.

**MCPB desktop extensions.** Per section 8.5, the only ungated lab distribution surface. Worth treating as a channel to test rather than a product idea.

**Also in YC's current list and plausibly solo buildable:** AI native compliance infrastructure, multiplayer AI, a cloud for small software, and adaptive early literacy tutoring. Explicitly not solo buildable on your budget, and the pipeline should auto reject them: defence, compute at sea, physical world operating systems, aging population hardware, human verification infrastructure, crypto.

### 8.8 What I could not verify

Stated plainly so you do not build a scoring model on sand. There is no citable primary source for AI native vertical company gross margins or churn in 2026. Bessemer's 2026 State of the Cloud URL returned 404 and I cannot confirm the edition exists. Every "2026 SaaS benchmark" page found was generated content with unverifiable numbers. **Do not parameterise anything on assumed margin benchmarks.** Similarly unverified: current Shopify, Slack, Notion and Salesforce revenue share terms; which specific startup categories 2026 lab releases actually killed; Pakistan's 0.25 percent IT export withholding regime beyond tax year 2026, where industry was still lobbying for extension as of May 2026; and Pakistan e-commerce market sizing.

---

## 9. System architecture changes

You already have the right architecture. A TypeScript and SQLite MCP server as a deterministic core, slash commands, session hooks, and deterministically regenerated artefacts. v2 extends it. It does not replace it.

### 9.1 Database changes

**Preserve unchanged:** `skills`, `mastery`, `missions`, `streak`, `lessons`, `insights`, `revisions`. Every row keeps its ID. Nothing is deleted.

**Alter:**

```sql
ALTER TABLE lessons  ADD COLUMN mode TEXT DEFAULT 'course';        -- course | build
ALTER TABLE lessons  ADD COLUMN depth TEXT DEFAULT 'explain';      -- explain | flow | ship
ALTER TABLE lessons  ADD COLUMN track_id INTEGER;
ALTER TABLE lessons  ADD COLUMN hint_max_rung INTEGER DEFAULT 0;   -- deepest hint reached
ALTER TABLE lessons  ADD COLUMN student_wrote INTEGER DEFAULT 1;   -- 0 if unlocked
ALTER TABLE skills   ADD COLUMN track_id INTEGER;
ALTER TABLE skills   ADD COLUMN source TEXT DEFAULT 'syllabus';    -- syllabus | build | venture
ALTER TABLE insights ADD COLUMN mode TEXT;
```

**New tables:**

```sql
-- The curriculum spine. Seeded from section 5.
tracks(id, code, title, position, status, prereq_codes, completion_test, current_as_of)

-- Replaces "projects" as the unit of progress. A system runs on real hardware.
systems(id, track_id, title, repo_url, kind, status, metric_name, metric_value,
        baseline_value, deployed_url, created_at, shipped_at)
        -- kind: trained_model | serving_stack | kernel | product

-- Every run. This is what v1 had no equivalent of.
experiments(id, system_id, config_json, seed, metric_name, metric_value,
            gpu_type, gpu_hours, cost_usd, notes, created_at)

-- THE table that fixes the coding complaint.
errors(id, lesson_id, category, description, code_excerpt, rule_broken,
       resolved, occurrences, last_seen)
       -- category: expression-vs-statement | off-by-one | type-confusion
       --         | mutation-vs-copy | shape-mismatch | inverse-relationship
       --         | missing-call-brackets | state-in-wrong-scope | broadcasting
       --         | api-misuse | silent-truncation

-- Code review records, so the diff walk is queryable later.
code_reviews(id, lesson_id, student_code, reference_code, diff_summary,
             correctness_diffs, taste_diffs, created_at)

-- The venture arm.
ventures(id, title, thesis, stage, score_json, weighted_score, wip_lock,
         v0_metric, v0_deadline, outcome, postmortem, created_at)
         -- stage: candidate | corroborated | scored | active | parked | killed
evidence(id, venture_id, source_family, source_url, excerpt,
         importance, dissatisfaction, captured_at)

-- Weekly frontier ingest, so the syllabus stays current without being rewritten.
frontier(id, area, title, url, summary, affects_track_id, ingested_at, actioned)
```

Constraint that matters: a partial unique index on `ventures(wip_lock)` where `stage = 'active'`, so the database physically refuses a second active venture.

### 9.2 MCP tools

**Keep:** `faizos_lesson_start`, `faizos_record_lesson`, and whatever exists for mastery, missions and streak.

**Extend `faizos_lesson_start`** to also load, before every lesson: the top three open error categories from `errors` ordered by occurrences, the current track and its `current_as_of` frontier notes, due spaced repetition items, and the active venture if any. This is the mechanism that makes the error taxonomy actually change the teaching rather than just recording it.

**Extend `faizos_record_lesson`** to classify errors into the taxonomy, record the deepest hint rung reached, and set `student_wrote`.

**New tools:**

```
faizos_track_status(track_code)          -> position, systems, completion test state
faizos_spec_build(topic, mode, depth)    -> design brief, python rules card, test suite path
faizos_hint(lesson_id, rung)             -> one rung, refuses to skip
faizos_review_code(lesson_id, path)      -> three pass review, writes code_reviews and errors
faizos_log_experiment(system_id, ...)    -> writes experiments, returns seed spread if n>=3
faizos_error_report()                    -> open categories ranked, with trend
faizos_venture_ingest()                  -> runs stage 1 and 2, writes evidence
faizos_venture_score()                   -> runs stage 3 and 4, writes ventures
faizos_venture_activate(id)              -> stage 5, enforces WIP lock, emits milestone spine
faizos_venture_review()                  -> the 14 day kill gate
faizos_frontier_ingest()                 -> weekly, writes frontier, flags affected tracks
```

### 9.3 Commands

| Command | Purpose |
|---|---|
| `/faiz` | dashboard: streak, track, active system, open errors, active venture |
| `/faiz-learn [track\|next]` | Course Mode |
| `/faiz-build "<thing>"` | Build Mode |
| `/faiz-spec` | generate design brief, rules card and failing tests for the current build |
| `/faiz-hint` | next rung only |
| `/faiz-review` | three pass review of your code |
| `/faiz-run` | log an experiment, compute seed spread, warn on missing baseline |
| `/faiz-errors` | your open error taxonomy and trend |
| `/faiz-drill` | spaced repetition, now including code drills not just concept recall |
| `/faiz-venture [ingest\|score\|activate\|review]` | the venture arm |
| `/faiz-frontier` | this week's ingest and which tracks it affects |
| `/faiz-ship` | publish, update systems, regenerate artefacts |
| `/faiz-unlock` | explicitly hand a build to the assistant, recorded |
| `/faiz-notes` | revision materials |

### 9.4 Hooks

**Keep:** the `lesson_start` and `record_lesson` session hooks. That loop is the best thing in v1.

**Add:**

1. **`PreToolUse` guard on Write and Edit.** If the target path matches the active build's solution path and the build state is `awaiting_student`, block the call with a message pointing at `/faiz-hint` and `/faiz-unlock`. This is what makes section 3.3 real rather than aspirational.
2. **`SessionEnd` artefact commit.** Refuses to close a session with an unrecorded lesson or an uncommitted build. Writes the revision note.
3. **Weekly `frontier_ingest` cron.** Pulls arXiv, lab blogs and release notes for the tracks you are on or about to reach, writes to `frontier`, and flags tracks whose `current_as_of` has drifted.
4. **Daily `venture_ingest` cron.** Stage 1 and 2 only. Cheap, free tier, no decisions.

### 9.5 Artefacts

Keep all five deterministic generators and add three:

| File | Contents | New |
|---|---|---|
| `REVISIONS.md` | per lesson notes, chronological | |
| `REVISION.md` | study guide by track | |
| `SUMMARY.md` | coverage, skills, system index | |
| `SESSIONS.md` | session log | |
| `CAPSTONE.md` | eight rung portfolio audit, now auto scored from `systems` and `experiments` | changed |
| `EXPERIMENTS.md` | every run, with cost, seed spread, and baseline comparison | **new** |
| `ERRORS.md` | your error taxonomy, open and closed, with trend | **new** |
| `VENTURES.md` | pipeline state, evidence, kill decisions and post mortems | **new** |
| `FRONTIER.md` | rolling ingest, by track, with `current_as_of` stamps | **new** |

`CAPSTONE.md` becoming auto scored from real tables rather than hand written is the change that keeps you honest. A rung is either backed by a system row with a metric or it is not.

---

## 10. Migration plan

Non destructive, phased, and each phase leaves the system usable. Do not attempt this in one session.

**Phase 0. Safety.** Branch. Back up `faizos-core/data/faiz.db` to a timestamped copy outside the repository. Snapshot every generated artefact. Confirm `npm test` and `npx tsx src/smoke.ts` pass on the current code before touching anything.

**Phase 1. Schema.** Additive migrations only, in a numbered migration file with an up and a down. No drops, no renames, no data deletion. Run the migration against the backup copy first, verify row counts are unchanged on every existing table, then run against live.

**Phase 2. Backfill.** Map the 20 existing modules onto the 11 new tracks, preserving every lesson and skill row and setting `track_id`. Map the 44 builds into `systems` with `kind = 'study'` and no metric, which is truthful. Parse the recorded recurring frictions from your revision notes into seed rows in `errors`. This backfill is what makes the new error injection useful from day one rather than after a month of accumulation.

**Phase 3. Tools and hooks.** Add the new MCP tools. Extend `lesson_start` and `record_lesson`. Add the `PreToolUse` guard. Test the guard specifically by trying to violate it.

**Phase 4. Commands.** Add the new slash commands. Keep the old ones as aliases so nothing you have muscle memory for breaks.

**Phase 5. Artefacts.** Add the four new generators. Rewrite the `CAPSTONE.md` generator to auto score.

**Phase 6. Venture arm.** Build ingest for the free tier sources only, then the classifier, then the corroboration gate, then scoring. Do not build stages 4 and 5 before stages 1 to 3 are producing real evidence rows, because scoring an empty pipeline teaches nothing.

**Phase 7. Frontier ingest.** Seed `frontier` from section 6 of this document, then wire the weekly cron.

**Rollback:** every phase is a separate commit with a working test suite. Restore the database from the Phase 0 backup and check out the previous commit.

---

## 11. Week one

In order. Do not reorder.

1. **Spend fifty dollars.** Rent 8 spot H100s. Run `modded-nanogpt` once. You will have trained a language model to a target loss before you have finished restructuring anything. This is the fastest possible correction to the biggest gap in your record, and everything else in this document is easier to motivate once it is done.
2. **Resolve the visa question.** One email to Durham's international student office. Free, fast, and it gates every commercial decision downstream.
3. **Phase 0 and Phase 1 of the migration.** Branch, back up, additive schema. One session.
4. **Start T0.** Not T3, not T7, not the venture arm. T0. Create an empty repository and write a tested, typed, linted library from empty files with green CI. It will feel like a step backwards and it is the thing that makes the rest work.
5. **Seed `errors` from your existing friction list.** Twenty minutes, and it makes the very first v2 lesson better than the last v1 one.

What not to do in week one: build the venture arm, redesign the curriculum further, or read more about the frontier. All three are more comfortable than items 1 and 4, which is exactly why they are the trap.

---

## 12. Confidence, conflicts and open questions

Stated so you can weight the rest appropriately.

**High confidence.** The pedagogy change in section 3, because it follows from a line count you can verify yourself. The compute numbers in section 7, all from vendor pricing pages and public repositories on 13 August 2026. The architecture trends in section 6.1 to 6.5, all from arXiv papers and Hugging Face model cards. The distribution surface constraints in section 8.5, all from primary vendor documentation.

**Conflicts I could not resolve.**

- DeepSeek V4 parameter counts: the arXiv paper says V4-Pro at 1.6T total and 49B active, the Hugging Face organisation listing shows a V4-Pro-0813 at 1.7T. Likely a post paper revision, unreconciled.
- GLM-5 parameters: model card says 744B total and 40B active, the organisation listing says 754B.
- The MiniMax sparse attention paper describes a 109B model while pointing at the 427B M3 as the production artefact.
- Pakistani freelancer earnings: 1.76 billion export earnings versus PSEB's 1.1 billion award framing for the same fiscal year, different measurement bases.
- The Crunchbase early stage figure discussed in section 8.1.

**Not verified from primary sources.** AI native gross margin and churn benchmarks, in any form. Shopify, Slack, Notion and Salesforce current revenue share terms. Which startup categories 2026 lab releases killed, which is my synthesis and explicitly opinion. Pakistan Stripe or Stripe Atlas eligibility and current SBP foreign currency rules. UK student visa treatment of directorship, equity holding and unpaid founder work, which is the highest stakes unresolved item in the entire document. Whether multi agent orchestration actually beats a single well harnessed agent on general tasks, where Anthropic explicitly leaves the question open and I found no rigorous 2026 study.

**Deliberate omissions.** I have not specified the exact content of every lesson in every track, because that is what `/faiz-spec` generates at the time, informed by your error table and the current frontier ingest. Hardcoding lesson content in a document is how a syllabus goes stale.

**The assumption most likely to be wrong.** That you will do T0. Everything downstream depends on it and it is the least interesting four weeks in the plan. If you skip it, the coding problem you described will persist through v2 exactly as it persisted through v1, and no amount of line by line explanation will substitute for it.

---

## 13. Sources

**Architecture and models.** Kimi K3 technical report, arXiv 2607.24653. DeepSeek V4, arXiv 2606.19348 and the Hugging Face model card. DeepSeek V3.2 and sparse attention, arXiv 2512.02556. Manifold constrained hyper-connections, arXiv 2512.24880. Qwen3.5-397B-A17B model card, Hugging Face. Kimi Linear and KDA, arXiv 2510.26692. GLM-5, arXiv 2602.15763. MiniMax sparse attention, arXiv 2606.13392. Gemma 4 model card, ai.google.dev. NVIDIA Nemotron 3 Super technical report. Mistral Large 3, Hugging Face. NVFP4 pretraining, arXiv 2509.25149. Muon scalability, arXiv 2502.16982.

**Post-training and RL.** GSPO, arXiv 2507.18071. DAPO, arXiv 2503.14476. CISPO in MiniMax-M1, arXiv 2506.13585. VESPO, arXiv 2602.10693. Length bias impossibility, arXiv 2607.23364. Gradient starvation in binary reward GRPO, arXiv 2605.07689. Entropy in RL for reasoning, arXiv 2511.05993. ScaleRL, arXiv 2510.13786. Rubrics as Rewards, arXiv 2507.17746. Rubric reward hacking and CHERRL, arXiv 2606.04923. OpenAI beneficial RL, alignment.openai.com/beneficial-rl. Kimi K2.5, arXiv 2602.02276. verl, TRL, prime-rl, verifiers, SkyRL, OpenRLHF and Unsloth repositories and documentation.

**Inference, kernels and systems.** FlashAttention-4, arXiv 2603.05451. PyTorch 2.10 to 2.13 release blogs. Triton and CUTLASS release notes. Helion, pytorch.org/blog/helion. Blackwell microbenchmarks, arXiv 2512.02189. vLLM release notes and blog: Model Runner V2, decode context parallelism, P-EAGLE, parallel drafting speculators, FP8 KV cache. SGLang releases. TensorRT-LLM release notes. llm-compressor releases. NVFP4 quantisation, developers.redhat.com. MLX releases and Apple ML Research on M5. Unsloth dynamic quantisation documentation.

**Agents and evaluation.** General AgentBench, arXiv 2602.18998. Anthropic on effective harnesses for long running agents and on context engineering. Agentic context engineering, arXiv 2510.04618. OSWorld 2.0, arXiv 2606.29537. ARC-AGI-3 technical report, arcprize.org. Terminal-Bench 2.0 leaderboard and Harbor.

**Compute.** Lambda, RunPod, Modal, Together and Prime Intellect pricing pages, 13 August 2026. getdeploying.com and gpufinder.dev marketplace floors. modded-nanogpt and nanochat repositories and discussions.

**Venture and market.** YC Requests for Startups. Crunchbase H1 2026 and PitchBook Q1 2026 AI funding. Forbes AI 50 2026. a16z, Notes on AI Apps in 2026. Sequoia, 2026: This is AGI. Sacra on Harvey. Sierra on 100M ARR. Anthropic connectors submission documentation. MCP specification 2026-07-28. OpenAI Apps SDK monetisation documentation. Chrome Web Store payments deprecation notice. State Bank of Pakistan Quarterly Payment Systems Review Q3 FY26. PwC Worldwide Tax Summaries, Pakistan. FBR Rule 150Q e-invoicing material. gov.uk Student visa work page. SEC EDGAR and UK Companies House developer APIs.

---

*FaizOS v2 specification. Written 14 August 2026. Supersedes COURSE.md v1. Every figure carries a date because every figure will drift.*
