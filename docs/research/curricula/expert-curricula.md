# How expert educators order an AI-engineering curriculum

Research date: 2026-09-24. Every claim has a URL. "Checked" means fetched on 2026-09-24.
Where a page did not show something (for example a full lesson list), this file says so instead of guessing.

The learner: finance undergraduate, programming since Aug 2026, reads and judges Python and SQL well,
does not want to write code. Goal: design, read, judge and direct production AI systems.
Already covered: token cost, model choice, retries and timeouts, FastAPI in Docker, eval sets and CI gates,
error analysis in SQL, LLM-as-judge validation (TPR/TNR), basic retrieval (BM25, embeddings, Recall@k, MRR, chunk size).

---

## Part 1. Source by source

### 1. Chip Huyen, "AI Engineering" (O'Reilly, 2025)

- Who and why credible: author of "Designing Machine Learning Systems"; taught ML systems at Stanford; the book's repo lists the audience as AI engineers, ML engineers, data scientists, engineering managers and technical PMs. https://github.com/chiphuyen/aie-book (repo last pushed 2026-07-03)
- Core thesis: AI engineering is "less about modeling and training, and more about model adaptation"; evaluation is the hardest part. https://newsletter.pragmaticengineer.com/p/the-ai-engineering-stack and https://learning.acm.org/techtalks/mlengineering
- Audience and prerequisites: technical roles; "self-contained and modular"; ML familiarity helps but is not required. https://github.com/chiphuyen/aie-book
- Full table of contents, in order (https://raw.githubusercontent.com/chiphuyen/aie-book/main/ToC.md):
  1. Introduction to Building AI Applications with Foundation Models (use cases, planning, the AI engineering stack)
  2. Understanding Foundation Models (training data, modeling, post-training, sampling)
  3. Evaluation Methodology (language modeling metrics, exact evaluation, AI as a judge, comparative evaluation)
  4. Evaluate AI Systems (criteria, model selection, designing the eval pipeline)
  5. Prompt Engineering (best practices, defensive prompt engineering)
  6. RAG and Agents (RAG, agents, memory)
  7. Finetuning (when to finetune, memory bottlenecks, techniques)
  8. Dataset Engineering (curation, augmentation and synthesis, processing)
  9. Inference Optimization
  10. AI Engineering Architecture and User Feedback
- Projects: none built in; it is a design and judgment book. The repo adds resources and case studies.
- Format and length: book, 10 chapters (roughly 500 pages per retailer listings, not verified here).
- Cost: paid book (O'Reilly page returned 403 to the fetcher, so price not verified).
- Currency: 2025 edition. Agents chapter predates MCP and the 2025-2026 agent wave.
- Coding demanded: almost none. Reading and reasoning.
- Fit: HIGH. It is written for exactly "design, judge, direct", and puts evaluation before prompting.

### 2. Hamel Husain and Shreya Shankar, AI Evals for Engineers and PMs (Maven) plus public material

- Who and why credible: Hamel, ML engineer with 25+ years (Airbnb, GitHub, DataRobot); Shreya, ML systems researcher, UC Berkeley PhD. Say they have trained 2,000+ PMs and engineers including teams at OpenAI and Anthropic. https://maven.com/parlance-labs/evals (checked)
- Audience and prerequisites: engineers and PMs already building something; basic LLM familiarity helpful but not required. https://maven.com/parlance-labs/evals
- Syllabus: 11 lessons over 4 weeks. The public page shows only L1 "Building Agents, Foundations" and L2 "Building Agents, Designing for Evaluability"; the rest cover error analysis, evaluator design, CI/CD, red-teaming and optimization per the page summary. https://maven.com/parlance-labs/evals
- Course reader chapter order (from public descriptions): Introduction and the "Three Gulfs"; LLMs, prompts and evaluation basics; Error Analysis (starting dataset, open coding, axial coding); then automated evaluators, code-based vs LLM-as-judge. https://x.com/HamelHusain/status/1932657675294421061 and https://thingsithinkithink.blog/posts/2025/06-21-llm-evals-lesson-2-error-analysis/ (lifecycle: Analyze, Measure, Improve)
- Public free material: the Evals FAQ says error analysis is "the most important activity in evals"; order is read traces and write notes, build a failure taxonomy, build evaluators for the important failures, then repeatable eval sets; suggests building a custom annotation viewer with a coding assistant. https://hamel.dev/blog/posts/evals-faq/ (page shows modified 2026-09-21)
- Projects: 4 homework assignments with solutions (a "Recipe Bot" workflow). https://arize.com/blog/ai-evals-maven-course-homework-the-recipe-bot-workflow/
- Format and length: live cohort, 3-5 hours a week for 4 weeks, 200+ page reader, office hours, Discord.
- Cost: US$4,200. Next cohort Oct 10 to Nov 21, 2026. https://maven.com/parlance-labs/evals
- Currency: 2025-2026, actively updated.
- Coding demanded: "coding skills optional"; explicitly valuable for non-technical roles. https://maven.com/parlance-labs/evals
- Fit: HIGH for the free material (it matches his read-and-judge style and extends what he has done); LOW value for money on the paid course from Pakistan, since he already has TPR/TNR and error analysis.

### 3. Full Stack Deep Learning, LLM Bootcamp

- Who: Charles Frye, Sergey Karayev, Josh Tobin; FSDL ran the well-known deep learning production course before this. https://fullstackdeeplearning.com/llm-bootcamp/ (checked)
- Syllabus in order (Spring 2023): 1 Launch an LLM App in One Hour; 2 LLM Foundations; 3 Learn to Spell: Prompt Engineering; 4 Augmented Language Models; 5 Project Walkthrough: askFSDL; 6 UX for Language User Interfaces; 7 LLMOps; 8 What's Next?; plus guest talks (training your own LLM, agents by Harrison Chase, fireside with Peter Welinder).
- Projects: askFSDL, a retrieval Q&A bot, walked through.
- Format: recorded lectures, about one weekend of content. Cost: free.
- Currency: April 2023. The page itself warns that tools and model capabilities "have evolved since".
- Coding: moderate, but lectures are mostly conceptual.
- Fit: LOW-MEDIUM. The "ship in one hour first" order and the UX lecture are still good ideas; the tool content is stale.

### 4. Maxime Labonne, llm-course (GitHub)

- Who: Head of Post-Training at Liquid AI (GitHub profile, checked via API). Repo has ~83k stars; last pushed 2026-02-05. https://github.com/mlabonne/llm-course
- Three tracks, in order:
  - LLM Fundamentals (optional): Mathematics for ML; Python for ML; Neural Networks; NLP.
  - The LLM Scientist: LLM Architecture; Pre-Training; Post-Training Datasets; Supervised Fine-Tuning; Preference Alignment; Evaluation; Quantization; New Trends.
  - The LLM Engineer: Running LLMs; Building a Vector Storage; RAG; Advanced RAG; Agents; Inference Optimization; Deploying LLMs; Securing LLMs.
- Projects: linked Colab notebooks (fine-tuning, quantization, merging); the roadmap itself is a curated link list.
- Format: free roadmap with links. Length: open-ended.
- Currency: early 2026.
- Coding: Scientist track is heavy; Engineer track is moderate.
- Fit: MEDIUM. The Engineer track is a clean checklist in a sensible order; the Scientist track is for model builders, not for him. Note that evals sit inside the Scientist track, not the Engineer track, which is the opposite of Huyen and Husain.

### 5. Andrej Karpathy, Neural Networks: Zero to Hero, and his LLM talks

- Who: founding member of OpenAI, former Tesla AI lead, founder of Eureka Labs. https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again
- Zero to Hero, in order (https://karpathy.ai/zero-to-hero.html, checked): 1 micrograd (backprop), 2 makemore bigram, 3 MLP, 4 activations and BatchNorm, 5 manual backprop, 6 WaveNet, 7 Let's build GPT, 8 GPT tokenizer. His channel adds "Let's reproduce GPT-2 (124M)", 4h01m (channel listing via yt-dlp).
- Prerequisites: "solid programming (Python), intro-level math". Total about 17 hours of video, free.
- General-audience LLM talks (no coding): "Intro to Large Language Models" (1h, Nov 2023); "Deep Dive into LLMs like ChatGPT" (3h31m, Feb 5 2025) covering pretraining, SFT, RL, hallucination and tool use https://x.com/karpathy/status/1887211193099825254 ; "How I use LLMs" (2h11m, 2025); "Software Is Changing (Again)" keynote (June 17 2025, Software 3.0) https://www.youtube.com/watch?v=LCEmiRjPEtQ
- Newer: nanochat (Oct 2025), a full ChatGPT-style training pipeline, about 8,000 lines, intended capstone for LLM101n. https://github.com/karpathy/nanochat . The LLM101n repo is archived (last push Aug 2024). https://github.com/karpathy/LLM101n
- Coding: Zero to Hero is 100 percent "type along and implement".
- Fit: LOW for Zero to Hero (it is theory-by-implementation, the opposite of his mode). HIGH for the Deep Dive and Software 3.0 talks as the "ML foundations understood" layer.

### 6. DeepLearning.AI (Andrew Ng) short courses

- Who: Andrew Ng, Coursera and Google Brain co-founder; DeepLearning.AI hosts 50+ courses. https://www.deeplearning.ai/courses
- Most relevant:
  - Agentic AI (Ng himself). Modules in order: 1 Introduction to Agentic Workflows; 2 Reflection Design Pattern; 3 Tool Use; 4 Practical Tips for Building Agentic AI (evals and error analysis); 5 Patterns for Highly Autonomous Agents. 9h55m, 31 videos, 8 graded assignments, intermediate Python expected. Free audit; Pro US$25-30/month. https://www.deeplearning.ai/courses/agentic-ai/ (checked; announced Oct 2025 https://www.linkedin.com/posts/andrewyng_announcing-my-new-course-agentic-ai-building-activity-7381380126317404160-wW75)
  - Retrieval Augmented Generation (RAG), 26h, intermediate: BM25 vs semantic search vs Reciprocal Rank Fusion, evals driving reliability. https://www.deeplearning.ai/courses/retrieval-augmented-generation (announced July 2025 https://x.com/AndrewYNg/status/1945502636012445937)
  - Evaluating AI Agents (with Arize): traces, evaluator types, structured experiments. https://x.com/AndrewYNg/status/1892258190546653392 (Feb 2025)
  - MCP: Build Rich-Context AI Apps with Anthropic (May 2025). https://www.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic
  - Long-Term Agentic Memory with LangGraph; Safe and Reliable AI via Guardrails. https://www.deeplearning.ai/short-courses/
- Ng's recommended order: no official AI-engineer path was found. Staff guidance points non-coders to "AI Python for Beginners" first. https://careery.pro/blog/ai-careers/deeplearning-ai-courses-guide . Community threads asking for an order get no official answer. https://community.deeplearning.ai/t/does-deeplearning-ai-have-a-learning-path/787126
- Ng's stated priority: the biggest predictor of team progress on agents is a disciplined process for evals and error analysis; prototype first, then look at outputs, then build metrics (The Batch, Oct 15 2025). https://www.deeplearning.ai/the-batch/improve-agentic-performance-with-evals-and-error-analysis-part-1 and https://x.com/AndrewYNg/status/1978867684537438628
- Coding: notebook labs; you can run and read them.
- Fit: MEDIUM-HIGH. Ng's Agentic AI course is the best-taught agent-design course found, and cheap.

### 7. roadmap.sh AI Engineer and AI Agents roadmaps

- Who: community roadmap project, very widely used; content maintained on GitHub. https://github.com/kamranahmedse/developer-roadmap
- AI Engineer roadmap sections top to bottom (from https://roadmap.sh/ai-engineer.json, updated 2026-09-11): Introduction; How LLMs Work; Prompt Engineering; Context Engineering; Type of Models; Hugging Face; Choosing the Right Model; local and routed models (Ollama, LM Studio, OpenRouter); What are Embeddings; Embedding Models; Vector Databases; What are RAGs; AI Agents; Model Context Protocol (MCP); AI Safety and Ethics; LLM Observability; LLM Evaluations; Regression Testing; Multimodal AI; Development Tools.
- AI Agents roadmap (https://roadmap.sh/ai-agents.json, updated 2026-03-09): prerequisites (backend basics, git, REST, streaming) ; LLM fundamentals (transformers, embeddings, RAG basics, open vs closed, pricing) ; Agent Loop; prompt engineering; Tool Definition; MCP and creating MCP servers; Agent Memory (short, long, episodic vs semantic); architectures (RAG agent, ReAct, Planner-Executor, DAG agents, manual from scratch); function calling; then evaluation and observability tools; then security (prompt injection, sandboxing, PII, guardrails, red teaming).
- Projects: a separate projects page. Format: free interactive map. Coding: implied, not taught.
- Currency: Sept 2026, the most current source here.
- Fit: MEDIUM. Good coverage checklist, no pedagogy. Puts evals near the end, which the evals experts disagree with.

### 8. Microsoft, "Generative AI for Beginners" and "AI Agents for Beginners"

- Who: Microsoft Cloud Advocates. 120k and 75k GitHub stars, both pushed Sept 2026. https://github.com/microsoft/generative-ai-for-beginners and https://github.com/microsoft/ai-agents-for-beginners
- Generative AI for Beginners, 21 lessons in order, each tagged Learn or Build: 00 Setup; 01 Intro to GenAI and LLMs; 02 Exploring and comparing LLMs; 03 Using GenAI responsibly; 04 Prompt engineering fundamentals; 05 Advanced prompts; 06 Text generation apps; 07 Chat apps; 08 Search apps with vector databases; 09 Image generation apps; 10 Low-code apps; 11 Function calling; 12 UX for AI apps; 13 Securing GenAI apps; 14 GenAI application lifecycle (LLMOps); 15 RAG and vector databases; 16 Open source models and Hugging Face; 17 AI agents; 18 Fine-tuning; 19 SLMs; 20 Mistral models; 21 Meta models.
- AI Agents for Beginners, in order: Intro and use cases; Agentic frameworks; Agentic design patterns; Tool use; Agentic RAG; Trustworthy agents; Planning; Multi-agent; Metacognition; Agents in production; Agentic protocols (MCP, A2A, NLWeb); Context engineering; Agentic memory; Microsoft Agent Framework; Computer use agents; Deploying scalable agents; Local agents; Securing agents.
- Format: text, code and short videos per lesson. Cost: free (API or GitHub Models costs). Coding: Python notebooks; readable.
- Fit: MEDIUM. The agents course order is solid and current; parts are Azure-flavoured.

### 9. Alexey Grigorev / DataTalksClub: LLM Zoomcamp and AI Engineering Buildcamp

- Who: founder of DataTalks.Club and the Zoomcamp series, principal data scientist, Kaggle Master, author of "Machine Learning Bookcamp". https://github.com/DataTalksClub/llm-zoomcamp and https://maven.com/alexey-grigorev/from-rag-to-agents
- LLM Zoomcamp 2026, in order: Module 1 Agentic RAG (keyword search RAG, then function calling); Module 2 Vector Search; Module 3 Orchestration (Kestra); Workshop: Data ingestion of LLM traces (dlt, DuckDB); Module 4 Evaluation (retrieval and answer quality, offline and online); Module 5 Monitoring (user feedback, dashboards); Module 6 Best Practices (hybrid search, reranking); Module 7 End-to-end example; Capstone project with peer review of 3 projects.
- Prerequisites: "Python: You can write code confidently", command line, basic Docker; ML not required. About 10 weeks. Free; about US$1-5 of API credits. Repo pushed 2026-09-15.
- AI Engineering Buildcamp (Maven): 9 weeks, RAG to agents, testing, evaluation, monitoring, a documentation-agent running project and a capstone; "code-first"; US$1,799; cohort 4 runs Sep 21 to Nov 22 2026. https://maven.com/alexey-grigorev/from-rag-to-agents
- Fit: MEDIUM for Zoomcamp (the best free production-shaped project spine, but it expects him to write code); LOW for Buildcamp (price and code-first).

### 10. Reference layers (brief)

| Source | What it is | Date | Use for him |
|---|---|---|---|
| Made With ML, Goku Mohandas https://madewithml.com/ | Classic MLOps course: Design, Data, Model, Develop, Utilities, Testing, Reproducibility, Production. Needs Python, NumPy, PyTorch | repo pushed 2026-03 | Low. Read Design and Testing/Production pages only |
| Eugene Yan, "Patterns for Building LLM-based Systems" https://eugeneyan.com/writing/llm-patterns/ | 7 patterns in order: Evals, RAG, Fine-tuning, Caching, Guardrails, Defensive UX, Collect User Feedback. Says evals "should be the starting point" | 2023 | High as a design map |
| Anthropic, "Building effective agents" https://www.anthropic.com/engineering/building-effective-agents | Prompt chaining, Routing, Parallelization, Orchestrator-workers, Evaluator-optimizer, Agents. "Find the simplest solution possible" | Dec 19 2024 | High, core design vocabulary |
| Anthropic Academy https://anthropic.skilljar.com/ | 23 free courses incl. Building with the Claude API, Intro to MCP, MCP Advanced, Intro to agent skills, Intro to subagents, AI Fluency | 2025-2026 | Medium, tool-specific |
| Anthropic courses repo https://github.com/anthropics/courses | API fundamentals, Prompt engineering tutorial, Real world prompting, Prompt evaluations, Tool use | pushed 2026-08 | Medium |
| OpenAI Cookbook https://developers.openai.com/cookbook | Agents, Evals, RAG and memory, voice, multimodal recipes | live, 2026 | Reference only |

### 11. Other widely endorsed material

- swyx, "The Rise of the AI Engineer" (June 30 2023): AI engineers work on the API side of the line; the effective ones he names have not done the Ng Coursera courses nor know PyTorch; do not start with "Attention is All You Need". https://www.latent.space/p/ai-engineer
- Latent Space, "The 2025 AI Engineering Reading List" (Dec 27 2024): about 50 papers, one a week, in 10 sections: Frontier LLMs; Benchmarks and Evals; Prompting, ICL and CoT; RAG; Agents; Code Generation; Vision; Voice; Image/Video Diffusion; Finetuning. https://www.latent.space/p/2025-papers . Fit: MEDIUM, for year two.
- Stanford CS336, Language Modeling from Scratch (Spring 2026): 5 assignments, Basics, Systems, Scaling, Data, Alignment and reasoning RL; states the code volume is "at least an order of magnitude greater" than other classes. https://cs336.stanford.edu/ . Fit: LOW, a model-builder course.
- Alexey Grigorev's AI engineering field guide (2026 research into AI-engineer interview take-homes): https://github.com/alexeygrigorev/ai-engineering-field-guide . Useful later to see what hiring tests.

---

## Part 2. Summary table

| # | Source | Cost | Current? | Coding demanded | Fit |
|---|---|---|---|---|---|
| 1 | Huyen, AI Engineering | book | 2025 | none | HIGH |
| 2 | Husain and Shankar evals | free FAQ / US$4,200 | 2026 | optional | HIGH (free) / LOW (paid) |
| 3 | FSDL LLM Bootcamp | free | 2023 | moderate | LOW-MED |
| 4 | Labonne llm-course | free | 2026 | moderate to heavy | MEDIUM |
| 5 | Karpathy Zero to Hero / talks | free | 2023-25 | heavy / none | LOW / HIGH |
| 6 | DeepLearning.AI (Agentic AI, RAG, MCP) | audit free, US$25-30/mo | 2025 | notebooks | MED-HIGH |
| 7 | roadmap.sh | free | Sept 2026 | implied | MEDIUM |
| 8 | Microsoft beginners courses | free | 2026 | notebooks | MEDIUM |
| 9 | LLM Zoomcamp / Buildcamp | free / US$1,799 | 2026 | confident Python | MEDIUM / LOW |
| 10 | Yan, Anthropic, cookbooks | free | 2023-26 | little | HIGH as reference |
| 11 | Latent Space list / CS336 | free | 2025-26 | none / very heavy | MEDIUM / LOW |

---

## Part 3. Synthesis

### A. The consensus order

Each stage: what it is, who teaches it best, where experts disagree. "[done]" marks what he has already covered.

1. **What AI engineering is and the stack.** Application-centric, adapt models rather than train them.
   Best: Huyen ch1; swyx essay; roadmap.sh Introduction. No real disagreement.

2. **How LLMs work, conceptually.** Tokens, pretraining, post-training (SFT, RLHF), sampling, hallucination.
   Best: Karpathy "Deep Dive into LLMs"; Huyen ch2; roadmap "How LLMs Work".
   Disagreement: Karpathy, Labonne's Scientist track and CS336 teach this by implementing a model; swyx and Huyen say understand it, do not build it.

3. **Model choice, APIs, cost and latency basics.** [done]
   Best: Huyen ch4 (model selection); Microsoft lesson 02; roadmap "Choosing the Right Model".

4. **Prompting and structured output**, including defensive prompting.
   Best: Huyen ch5; Anthropic prompt tutorial; Microsoft 04-05.
   Disagreement: roadmap.sh now splits "context engineering" out as its own stage right after prompting.

5. **Evaluation methodology.** Exact metrics, AI as judge, comparative evaluation, eval pipeline. [partly done]
   Best: Huyen ch3-4; Husain and Shankar; Yan.
   Disagreement, the biggest one: Huyen, Yan, Husain and Ng put evals early (Huyen before prompting; Yan "the starting point"). Microsoft (lesson 14), roadmap.sh (near the end), Zoomcamp (module 4) and Labonne (inside the Scientist track) put it after building. Ng's compromise: build a quick prototype, then evals immediately.

6. **Error analysis and judge validation.** Read traces, open and axial coding, failure taxonomy, validate the judge. [done]
   Best: Husain and Shankar FAQ and reader; Ng's Batch letters.

7. **Retrieval and RAG basics.** [done]
   Best: DeepLearning.AI RAG course; Zoomcamp modules 1-2; Huyen ch6.

8. **Advanced retrieval and RAG evaluation.** Hybrid search, reranking, query rewriting, retrieval vs answer quality.
   Best: Zoomcamp modules 4 and 6; Labonne "Advanced RAG"; DeepLearning.AI RAG (RRF).
   Disagreement: Zoomcamp opens with "agentic RAG" in module 1, before plain vector search.

9. **Tool use, function calling and MCP.**
   Best: Ng Agentic AI module 3; Microsoft agents lessons 04 and 11; Anthropic Academy MCP; DeepLearning.AI MCP course.

10. **Agent design patterns: workflows before agents.** Chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, reflection, planning, multi-agent.
    Best: Anthropic "Building effective agents"; Ng Agentic AI modules 1, 2, 5; Microsoft agents 03, 07, 08.
    Disagreement: Anthropic says use raw APIs first; Microsoft and roadmap.sh introduce frameworks early.

11. **Context engineering and memory.** What goes in the window, compaction, short and long-term memory.
    Best: Microsoft agents 12-13; roadmap.sh Context Engineering; Huyen ch6 (memory). Newest stage; 2023-2024 sources lack it.

12. **Safety, security and guardrails.** Prompt injection, sandboxing tools, PII, red teaming.
    Best: Labonne "Securing LLMs"; Microsoft 13 and agents 18; roadmap.sh agents security block; Huyen defensive prompting.
    Disagreement: Microsoft puts "responsible AI" at lesson 03; most others put security late.

13. **Production: deploy, observe, monitor, collect feedback.** Tracing, dashboards, online evals, user feedback loops, regression tests. [deploy and CI done]
    Best: Huyen ch10; Zoomcamp modules 5 and trace workshop; FSDL LLMOps and UX lectures; Yan (feedback, defensive UX).

14. **Inference optimization, caching and cost at scale.** Batching, quantization, prompt caching, model routing.
    Best: Huyen ch9; Labonne "Inference Optimization"; Yan "Caching".

15. **Finetuning and dataset engineering, as a decision.** When to finetune vs prompt vs RAG; data curation and synthesis.
    Best: Huyen ch7-8; Labonne Scientist track; Microsoft 18.
    Disagreement: Yan places finetuning right after RAG; Huyen, Microsoft and Labonne's Engineer track keep it late. Almost all say try prompting and RAG first.

16. **Optional deep foundations.** Build a GPT, backprop, tokenizer.
    Best: Karpathy Zero to Hero and nanochat; CS336. Only model-builder curricula make this mandatory.

Where he is now: stages 3, 6, 7 done; 5 and 13 partly done. The consensus says the next gaps are 2 (conceptual depth), 8, 9-11 (agents as a system), 12, then 14-15.

### B. What experts say about pedagogy for this learner

**Project-first or theory-first?** The applied experts lean project-first with theory on demand.
- FSDL's first lecture is "Launch an LLM App in One Hour". https://fullstackdeeplearning.com/llm-bootcamp/
- Zoomcamp is "for people who learn by doing" and ends with a peer-reviewed capstone. https://github.com/DataTalksClub/llm-zoomcamp
- Microsoft alternates "Learn" and "Build" lessons. https://github.com/microsoft/generative-ai-for-beginners
- Ng: prototype first, then examine outputs, then build evals. https://www.deeplearning.ai/the-batch/improve-agentic-performance-with-evals-and-error-analysis-part-1
- swyx: you do not learn to drive by reading the engine schematics. https://www.latent.space/p/ai-engineer
- Counterweight: Huyen's book is framework-first and argues fundamentals outlast tools https://github.com/chiphuyen/aie-book ; Karpathy teaches theory by building from scratch https://karpathy.ai/zero-to-hero.html
- Practical reading: the consensus is "build something small, then use theory to explain what you saw". Error analysis on a real system is the shared core method (Husain, Ng, Yan).

**How much coding does a designer and judge of AI systems need?**
- Low end: Husain and Shankar say coding is optional and the course serves non-technical roles. https://maven.com/parlance-labs/evals . Huyen's audience explicitly includes managers and technical PMs. https://github.com/chiphuyen/aie-book
- Middle: Ng says learn "enough coding to use AI-assisted coding tools effectively", and names steering coding agents as a key AI-engineering skill; he also calls AI-assisted coding "a deeply intellectual exercise", not vibes. https://x.com/AndrewYNg/status/1900219116822102116 and https://www.deeplearning.ai/the-batch/tag/letters
- Anthropic: patterns are "a few lines of code" on raw APIs, so reading code is enough to follow them. https://www.anthropic.com/engineering/building-effective-agents
- High end: Zoomcamp wants confident Python; Buildcamp is "code-first"; Karpathy wants solid Python; CS336 is "an order of magnitude" more code. Karpathy hand-wrote nanochat because coding agents did not help enough on novel code. https://developers.slashdot.org/story/25/10/19/0022237/openai-cofounder-builds-new-open-source-llm-nanochat---and-doesnt-use-vibe-coding
- Honest finding: no expert curriculum found is designed as "read-only". Every one with projects assumes the learner writes or runs code. The defensible version of his path is "reads, judges and directs a coding agent, runs everything, writes little", which matches Ng's framing. Pure no-code is not something any of these experts endorse for an AI engineer role; it does fit the PM-facing tracks (Husain and Shankar, Huyen).

### C. Three best-fitting primary spines

**Spine 1: Huyen's "AI Engineering" as the backbone, Husain and Shankar free material for evals, Karpathy's Deep Dive for foundations.**
- Why: closest match to "design, read, judge"; order puts evals early, matching his progress; one coherent author voice; ch6-10 cover exactly his gaps.
- Trade-offs: no projects, so he must attach his own build to each chapter; dense; 2025 edition is thin on MCP, context engineering and current agent practice (patch with Anthropic's agents essay and Microsoft agents lessons 11-13); book costs money.

**Spine 2: DeepLearning.AI, Ng's Agentic AI then the RAG course, with Anthropic's "Building effective agents".**
- Why: best-taught agent design course found; Ng's evals-and-error-analysis emphasis matches his existing strength; graded assignments give checkpoints; free to audit or about US$25-30 a month.
- Trade-offs: notebook labs assume intermediate Python (he can read them, but assignments expect edits); little on deployment, monitoring, cost at scale; partner short courses vary in quality and some are vendor demos.

**Spine 3: LLM Zoomcamp 2026, done in "direct and judge" mode, with roadmap.sh as the coverage checklist.**
- Why: free, current (Sept 2026), production-shaped order (RAG, search, orchestration, evaluation, monitoring, best practices), a real capstone with peer review, and a trace-ingestion workshop that suits his SQL strength.
- Trade-offs: states it wants confident Python writers; tool choices (Kestra, dlt) churn; less conceptual depth on why LLMs behave as they do; he would need a coding agent to produce the code he then reviews, which is a deviation from how the course is meant to be taken.

Recommendation among the three: Spine 1 as the order and the "why", Spine 3's capstone shape as the project, and Ng's Agentic AI module 4 or Anthropic's essay when he reaches agents. This is a judgement call, not something any single source prescribes.

---

## Sources not fully verified

- Chip Huyen price and page count (O'Reilly returned 403).
- Husain and Shankar lessons 3-11 titles (not shown publicly; only the topic summary).
- DeepLearning.AI release dates are taken from announcement posts, not course pages.
- Hamel's FAQ "modified 2026-09-21" is what the page reported.
