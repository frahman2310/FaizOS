# Real-world project reasoning

How to frame every build so it reads like production work rather than coursework. Synthesised
from all 146 ScaleDojo posts (scraped 2026-09-01, 238,855 characters of captions) and the
Hugging Face / Grigorev / Husain / Huyen research.

---

## Part 1 · What ScaleDojo actually does

An Instagram account, 146 posts, 8,776 followers, running one format relentlessly since Feb 2026:
a real onsite interview question from a named company and level, answered in numbered steps.

**Their format, exactly:**

```
Day 72 - Microsoft L6 Azure

"A hospital wants to deploy GPT-4 internally but their data cannot leave
 their servers under any circumstances. Design the fully air-gapped GenAI
 deployment architecture."

Asked at: Microsoft (L6 Onsite)

<one plain sentence defining the core idea>

Step 1: Understand what air-gapped requires.
  No API calls to any external endpoint, ever. Not encrypted, not logged
  externally, not even telemetry. This rules out cloud-hosted inference.

Step 2: Deploy model weights on-premises, not via API.
  GPT-4 itself is API-only and cannot be air-gapped, so use a self-hosted
  open-weight model on the hospital's own GPU hardware.

Step 3: Isolate the network at the physical layer.
  ...
```

The word **"step" appears 735 times across 146 posts** — five times per post. That is the whole
method, and it is worth copying.

### The four properties that make it work

1. **A hard constraint with a number in it.** 10M documents. 100ms. 1B daily calls. 300M users.
   Zero hallucinations. 111 of 146 posts (76%) carry an explicit scale figure. The number is what
   turns "design a chatbot" into an engineering problem, because it eliminates most designs.
2. **Every step is a decision, not a topic.** The heading is "Deploy model weights on-premises,
   not via API", never "Deployment". You can disagree with a decision; you cannot disagree with
   a topic.
3. **Each step names what it rules out.** Air-gapped rules out cloud inference. That is the
   actual reasoning: a constraint eliminating options, not a list of components.
4. **Plain language before jargon.** "RAG stands for Retrieval Augmented Generation. Instead of
   letting the model guess from memory, you give it actual documents to read before it answers."
   Then the steps.

### What their 146 posts are about

| Topic | Posts | Avg views | Read |
|---|---|---|---|
| Scale / hard numbers | 111 | 11,986 | Present in 76% of everything |
| **RAG & retrieval** | 61 | 15,842 | The most-covered subject by far |
| Data pipelines | 52 | 11,626 | |
| **Cost & caching** | 51 | 12,632 | |
| **Serving & latency** | 46 | **25,548** | Second-highest engagement |
| **Training / fine-tuning** | 29 | **37,725** | **Highest engagement of any topic** |
| Evals & hallucination | 28 | 18,785 | |
| Safety / jailbreak / PII | 22 | **4,830** | **Lowest engagement by 2.5×** |
| Context & memory | 15 | 14,933 | |
| Agents | 13 | 15,072 | Least covered |

**Two findings worth acting on.** Training and serving draw the most attention despite being the
smallest share of actual job postings (fine-tuning 24.8%, self-hosting 2.5%) — that is an
audience-interest signal, not a hiring signal, and the two should not be confused. And safety
gets the least engagement while being the thing every employer now asks about, which makes a
documented injection result *more* differentiating, not less.

---

## Part 2 · The synthesis: how a FaizOS lesson should be framed

ScaleDojo has the framing and no artifact. Hugging Face has artifacts and weak framing. The
combination is what a real project looks like.

| Source | Gives us | Fails at |
|---|---|---|
| **ScaleDojo** | Constraint-driven questions, step-as-decision reasoning, real company/level provenance | Nothing is built. It is an answer, not a repo. |
| **Hugging Face** | Real artifacts: a GAIA-scored Space, an MCP server with webhooks and tunnels, a leaderboard-ranked model | Certificates are unproctored marketing; thresholds are low; framing is absent |
| **Grigorev / Husain / Huyen** | What is actually measured and hired for: evals first, a private labelled set, cost arithmetic | No narrative that makes a beginner care |

### The lesson frame, adopted

Every lesson from L3 onward gets four parts:

1. **The question**, in ScaleDojo's exact shape — a named company and level, a real constraint,
   a number. Drawn from the 146-question bank below or written in that shape.
2. **The steps**, each a decision with what it rules out. This is the design brief, and it is
   what he should be able to say out loud in an interview before writing any code.
3. **The build** — the single self-contained file, unchanged from the format that works.
4. **The number** he produces, compared against the constraint from step 1. Did it meet the bar?

The fourth part is the join that neither source has on its own: ScaleDojo never measures, HF
never sets a bar.

### The question bank

Real onsite questions, ranked by reach, mapped onto the 20 lessons:

| Lesson | Question to frame it with | Asked at |
|---|---|---|
| L4 contract | *"Your LLM is 99.9% accurate. At Google's scale that is 10 million wrong answers a day. Design the system that catches the 0.1% before users do."* | Google |
| L5–L8 evals | *"Design a RAG pipeline for 10M documents with zero hallucinations."* | Google L5 |
| L7 triage | *"A user watches 10 minutes of a show and quits. Design the system that figures out exactly why."* | Netflix |
| L9–L11 retrieval | *"Design an AI recommendation engine for 300M users. Latency under 100ms."* | GenAI series |
| L12 grounded | *"A user jailbreaks your LLM in production. What are your real-time detection and mitigation strategies?"* | Anthropic Applied AI |
| L13–L14 agents | *"Design a multi-agent system where 3 AI agents collaborate to write, review and deploy code autonomously."* | — |
| L15 MCP | *"Design an AI Gateway that routes between GPT, Claude and Gemini with auto-fallback."* | — |
| L16 service | *"Redesign Alexa using an LLM backend. How do you keep responses conversational, fast and accurate mid-sentence?"* | — |
| L17 store | *"Gmail reads 1.8 billion emails a day and decides in milliseconds if it is spam, without reading private content."* | Google |
| L18 ship-it | *"Design a prompt caching system for 1B daily LLM API calls. Optimise for cost and latency."* | Google L5 |
| L19 prove | *"A hospital wants GPT-4 internally but data cannot leave their servers. Design the air-gapped deployment."* | Microsoft L6 |
| L20 capstone | *"A competitor steals your client's fine-tuned model just by sending it the right prompts. Design the architecture that makes this impossible."* | — |

Others worth keeping: a GenAI code reviewer that catches bugs, security holes and cost
inefficiencies pre-commit; an explainability layer that satisfies a government audit at 4B
queries a day; a recommendation system that learns from two users who disagree about the same
episode without learning the wrong lesson.

---

## Part 3 · The rule this produces

**A project is real when a constraint eliminated a design.**

That is the single test. "I built a RAG chatbot" is coursework. "The corpus was 10M documents so
a full-context approach cost $3 per query against $0.015 for retrieval, which is why I retrieved;
then recall@50 was 0.81 while recall@5 was 0.34, which is why I added a reranker" is engineering.
Same system, and only one of them survives a follow-up question.

Every FaizOS lesson now has to produce that second sentence.
