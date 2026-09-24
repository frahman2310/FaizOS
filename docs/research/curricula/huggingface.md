# Hugging Face learning material: full map and fit for Faiz

Checked 2026-09-24. Every claim has a URL. "Last update" means the date of the latest commit to the
course's GitHub repo (checked through the GitHub API on 2026-09-24). Many of these are small maintenance
commits, so a recent date does not mean new chapters. Unit lists come from each repo's `_toctree.yml`,
which is the file that builds the course sidebar.

Code rating key (my judgement from the unit titles and hands-on pages):
- **Read/run**: you mostly read notebooks and press run; small edits at most.
- **Mixed**: you edit templates and wire pieces together.
- **Write**: the assignments ask you to write real code.

## 1. Every course on huggingface.co/learn

The catalogue at https://huggingface.co/learn lists 12 entries: LLM, Context, Robotics, smol, Agents,
Deep RL, Computer Vision, Audio, Cookbook, ML for Games, Diffusion, ML for 3D. The MCP Course is not on
that page any more but is still live at https://huggingface.co/learn/mcp-course/unit0/introduction.

| Course | Units | Time | Certificate | Last repo commit | Code |
|---|---|---|---|---|---|
| LLM Course (was NLP Course) | 12 chapters | 6-8 h per chapter-week | None formal; quizzes only | 2026-09-23 | Read/run, some Write in ch.3, 11, 12 |
| Agents Course | Units 0-4 + 3 bonus | 3-4 h per week, ~1 week per unit | Fundamentals (Unit 1) and Completion (GAIA >30%) | 2026-09-09 | Mixed; Unit 4 is Write |
| MCP Course | Units 0-3 + 3.1 | 3-4 h per week | Fundamentals (Unit 1), Completion (Units 2+3) | 2026-09-18 | Mixed to Write |
| Context Course (new, April 2026) | Units 0-6 | 2-3 h per unit | Context Fundamentals, Context Engineering | 2026-09-18 | Mixed |
| a smol course (fine-tuning) | 4 units, Evaluation "coming soon" | 3-4 h per week | Fundamentals (Unit 1), Completion (all + project) | 2026-09-17 | Write |
| Open-Source AI Cookbook | ~80 recipes | per recipe | None | 2026-09-17 | Read/run |
| Deep RL Course | 8 units + 4 bonus | 3-4 h per week | 80% assignments, honors at 100% | 2026-09-17 | Write |
| Computer Vision (community) | Units 0-13 | not stated | None | 2026-09-23 | Read/run |
| Audio Course | Units 0-8 | not stated | 80% hands-on, honors at 100% | 2026-09-23 | Mixed |
| Diffusion Course | 4 units | 6-8 h per week | None | 2026-09-17 | Write |
| ML for 3D | Units 0-5 | not stated | not stated | 2026-09-18 | Mixed |
| ML for Games | no fixed units | not stated | None | repo not found | Write (Unity) |
| Robotics Course (LeRobot) | Units 0-2 so far | not stated | not stated | 2026-09-18 | Write |

Sources: catalogue https://huggingface.co/learn ; commit dates via https://api.github.com/repos/huggingface/<repo>/commits ;
per-course facts in the sections below.

### 1.1 LLM Course (formerly NLP Course)
- URL: https://huggingface.co/learn/llm-course/chapter1/1 . Sidebar source: https://github.com/huggingface/course/blob/main/chapters/en/_toctree.yml
- Purpose: LLMs and NLP with the HF libraries, from classic NLP to current LLM techniques (chapter1/1 page).
- Prerequisites: "strong" Python, an intro deep learning course recommended, PyTorch helpful (chapter1/1).
- Time: each chapter is about one week at 6-8 hours (chapter1/1).
- Certificate: the intro says there is no certification yet (chapter1/1). Chapters 1 and 11 end with a sign-in quiz
  ("Certification exam", "Exam Time!"), but the quiz page names no pass mark or certificate
  (https://huggingface.co/learn/llm-course/chapter1/11 , https://huggingface.co/learn/llm-course/chapter11/7).
- Hands-on: Colab or SageMaker notebooks from https://github.com/huggingface/notebooks (chapter1/1).

| Ch | Title | Sections (from toctree) | Hands-on |
|---|---|---|---|
| 0 | Setup | Introduction | environment |
| 1 | Transformer models | NLP and LLMs; what Transformers can do; how they work; architectures; Inference with LLMs; Bias and limitations; quiz | pipeline() notebooks, quiz |
| 2 | Using Transformers | Behind the pipeline; Models; Tokenizers; Multiple sequences; Optimized Inference Deployment; quiz | notebooks |
| 3 | Fine-tuning a pretrained model | Processing data; Trainer API; full training loop; Understanding Learning Curves; quiz | fine-tune notebook |
| 4 | Sharing models and tokenizers | The Hub; using pretrained models; sharing; Building a model card; quiz | push to Hub |
| 5 | The Datasets library | local data; slice and dice; big data; create a dataset; Semantic search with FAISS; quiz | notebooks |
| 6 | The Tokenizers library | train a tokenizer; fast tokenizers; BPE, WordPiece, Unigram; build one block by block; quiz | notebooks |
| 7 | Classical NLP tasks | token classification; masked LM; translation; summarization; causal LM from scratch; QA; Mastering LLMs; quiz | notebooks |
| 8 | How to ask for help | errors; forums; debugging the training pipeline; good issues; quiz | none |
| 9 | Building and sharing demos | Gradio intro; first demo; Interface; sharing; Hub integration; Blocks; quiz | Gradio Space |
| 10 | Curate high-quality datasets | Argilla setup; load; annotate; use annotated data; quiz | Argilla Space |
| 11 | Fine-tune Large Language Models | Chat Templates; SFTTrainer; LoRA; Evaluation; Exam | SFT + LoRA notebook |
| 12 | Build Reasoning Models | RL on LLMs; DeepSeek R1 "aha moment"; GRPO in DeepSeekMath; GRPO in TRL; GRPO exercise; Unsloth exercise; "Coming soon" | GRPO notebooks |

### 1.2 AI Agents Course
- URL: https://huggingface.co/learn/agents-course/unit0/introduction . Toctree: https://github.com/huggingface/agents-course/blob/main/units/en/_toctree.yml
- Prerequisites: basic Python, basic LLM knowledge (taught in Unit 1). Time: 3-4 h per week, about a week per unit, no deadline (unit0 page).
- Certificates, free: Fundamentals = Unit 0 + Unit 1; Completion = Unit 1 + one use-case assignment + final challenge (unit0 page).
- Final challenge: 20 GAIA level-1 validation questions, exact-match grading, run from a duplicated Space
  https://huggingface.co/spaces/agents-course/Final_Assignment_Template , scores on
  https://huggingface.co/spaces/agents-course/Students_leaderboard (https://huggingface.co/learn/agents-course/unit4/hands-on).
  Certificate needs a score "above 30%" (https://huggingface.co/learn/agents-course/unit4/get-your-certificate).

| Unit | Title | Sections | Hands-on |
|---|---|---|---|
| 0 | Welcome | Onboarding, Discord | account setup |
| 1 | Introduction to Agents | What is an Agent; What are LLMs; Messages and Special Tokens; What are Tools; Thought-Action-Observation; ReAct; Actions; Observe; Dummy Agent Library; first agent with smolagents; final quiz | duplicate a Space, first agent |
| 2.1 | smolagents | why smolagents; code agents; code vs JSON actions; Tools; Retrieval Agents; Multi-Agent Systems; Vision and Browser agents; quizzes | notebooks |
| 2.2 | LlamaIndex | LlamaHub; components; tools; agents; agentic workflows; quizzes | notebooks |
| 2.3 | LangGraph | building blocks; first graph; Document Analysis Graph; quiz | notebooks |
| 3 | Use Case for Agentic RAG | Agentic RAG; RAG tool for guest stories; building tools; Gala agent | build an agent |
| 4 | Final Project | What is GAIA; final hands-on; certificate; what next | GAIA agent, leaderboard |
| B1 | Fine-tuning an LLM for Function-calling | what is function calling; fine-tune | notebook |
| B2 | Agent Observability and Evaluation | what is observability; monitoring and evaluating agents (Langfuse, OpenTelemetry, cost, latency, online vs offline eval); quiz | notebook |
| B3 | Agents in Games with Pokemon | LLMs in games; build and launch a battle agent | Space |

Bonus 2 tools: https://github.com/huggingface/agents-course/blob/main/units/en/bonus-unit2/monitoring-and-evaluating-agents-notebook.mdx

### 1.3 MCP Course
- URL: https://huggingface.co/learn/mcp-course/unit0/introduction . Toctree: https://github.com/huggingface/mcp-course/blob/main/units/en/_toctree.yml
- Prerequisites: basic AI/LLM knowledge, APIs, Python or TypeScript. Time: 3-4 h per week. Certificates: Fundamentals = Unit 1; Completion = Units 2 and 3 (unit0 page).

| Unit | Title | Sections | Hands-on |
|---|---|---|---|
| 0 | Welcome | | |
| 1 | Introduction to MCP | Key Concepts; Architectural Components; Communication Protocol; Capabilities; MCP SDK; MCP Clients; Hugging Face MCP Server; Gradio MCP Integration; 2 quizzes; certificate | quizzes |
| 2 | End-to-End MCP Application | Gradio MCP server; MCP clients; MCP in your AI coding assistant; Gradio MCP client; Tiny Agents with the Hub; local Tiny Agents on AMD | build and deploy a Space |
| 3 | Custom Workflow Servers (for Claude Code) | Module 1 MCP server; Module 2 GitHub Actions; Module 3 Slack notification; PR agent walkthrough; certificate | build a PR workflow server |
| 3.1 | Pull Request Agent on the Hub | setup; MCP server; MCP client; Webhook Listener; 2 quizzes | webhook agent |

The unit0 page mentions a Unit 4 of bonus units with partner libraries; the toctree has no Unit 4 pages.

### 1.4 Context Course (new in 2026)
- URL: https://huggingface.co/learn/context-course/unit0/introduction . Toctree: https://github.com/huggingface/context-course/blob/main/units/en/_toctree.yml
- Released 2026-04-20 (https://ai-tldr.dev/releases/huggingface-context-course-2026/).
- Purpose: context engineering for code agents (Claude Code, Codex, OpenCode). Prerequisites: Python basics, command line,
  HF account, one installed code agent. Time: 2-3 h per unit. Certificates: Context Fundamentals = Unit 1-2 quizzes at 70%+;
  Context Engineering = Unit 1-5 quizzes at 70%+ plus capstone (https://huggingface.co/learn/context-course).

| Unit | Title | Sections | Hands-on |
|---|---|---|---|
| 1 | Skills | What are Agent Skills; SKILL.md format; using skills; building your first skill; 2 quizzes | write a skill |
| 2 | MCP | concepts and architecture; MCP servers in Python; agents as MCP clients; Gradio MCP; build and deploy an MCP server; 2 quizzes | deploy MCP server |
| 3 | Plugins | plugin anatomy; build; use; 2 quizzes | build a plugin |
| 4 | Subagents | patterns; using subagents; multi-agent workflow; 2 quizzes | workflow |
| 5 | Hooks | hook events and lifecycle; agent activity dashboard with Gradio; 2 quizzes | dashboard |
| 6 | Bonus: Nano Harness | agentic loop deep dive; tools and sandboxing; extending Nano Harness; quiz | extend a harness |

### 1.5 a smol course (fine-tuning)
- URL: https://huggingface.co/learn/smol-course . Toctree: https://github.com/huggingface/smol-course/blob/main/units/en/_toctree.yml
- Prerequisites: LLM basics, Python, ML fundamentals, PyTorch, transformer basics. Time: 3-4 h per week. Certificates:
  Fundamentals = Unit 1; Completion = all units + final project (https://huggingface.co/learn/smol-course).
- Units per toctree: 1 Instruction Tuning (chat templates, SFT, LoRA/PEFT, exercises, Training with HF Jobs, submit project);
  2 Preference Alignment (DPO, advanced DPO, hands-on); 3 Vision Language Models (use, fine-tune, hands-on); 4 Model Evaluation ("Coming soon!").
- The landing page lists a different plan (Evaluation as unit 2; RL, Synthetic Data, Award Ceremony scheduled Oct-Dec) and the
  preference page is titled "Unit 3" (https://huggingface.co/learn/smol-course/unit2/1). Treat evaluation as not yet published.
- Hands-on: train SmolLM3 with DPO, compare with baseline, submit to a course leaderboard (unit2/1 page).

### 1.6 Open-Source AI Cookbook
- URL: https://huggingface.co/learn/cookbook . Toctree: https://github.com/huggingface/cookbook/blob/main/notebooks/en/_toctree.yml
- Sections: MLOps, LLM, Computer Vision, Diffusion, Multimodal, Search, Agents, Enterprise Hub. No certificate, no order; every recipe is one notebook.
- Recipes that matter for Faiz are listed in section 2.

### 1.7 Other courses (short, all low fit)
- **Deep RL**: Units 1 intro, 2 Q-Learning, 3 Deep Q-Learning (Atari), 4 Policy Gradient, 5 Unity ML-Agents, 6 Actor-Critic, 7 Multi-agent, 8 PPO (two parts);
  bonus: Huggy, Optuna, advanced topics, Godot imitation learning. Colab + push agents to Hub; leaderboard currently not working. 80%/100% certificates.
  (https://huggingface.co/learn/deep-rl-course/unit0/introduction , https://github.com/huggingface/deep-rl-class/blob/main/units/en/_toctree.yml)
- **Computer Vision**: Units 1 fundamentals, 2 CNNs, 3 ViT, 4 multimodal, 5 generative, 6 basic tasks, 7 video, 8 3D, 9 model optimization,
  10 synthetic data, 11 zero-shot, 12 ethics, 13 outlook. Colab notebooks, no certificate.
  (https://huggingface.co/learn/computer-vision-course/unit0/welcome/welcome , https://github.com/huggingface/computer-vision-course/blob/main/chapters/en/_toctree.yml)
- **Audio**: Units 1 audio data, 2 audio apps, 3 architectures, 4 music genre classifier, 5 ASR, 6 TTS, 7 putting it together, 8 finish line.
  Needs deep learning background. 80%/100% certificates. (https://huggingface.co/learn/audio-course/chapter0/introduction)
- **Diffusion**: Units 1 intro + from scratch, 2 fine-tuning and guidance, 3 Stable Diffusion, 4 advanced. Two notebooks per unit,
  6-8 h per week, no certificate, content dated late 2022. (https://huggingface.co/learn/diffusion-course/unit0/1 ,
  https://github.com/huggingface/diffusion-models-class)
- **ML for 3D**: Units 1 what is 3D, 2 multi-view diffusion, 3 Gaussian splatting, 4 meshes, 5 capstone.
  (https://github.com/huggingface/ml-for-3d-course/blob/main/units/en/_toctree.yml)
- **ML for Games**: needs Unity, no new units planned, no certificate, deliverable is a game demo
  (https://huggingface.co/learn/ml-games-course/unit0/introduction).
- **Robotics (LeRobot)**: only Units 0-2 (welcome, intro, classical robotics) so far
  (https://github.com/huggingface/robotics-course/blob/main/units/en/_toctree.yml).

## 2. Practice surfaces for a learner who judges rather than writes

| Surface | What you do there | URL |
|---|---|---|
| Inference Providers | Call 200+ models through one OpenAI-compatible router (`router.huggingface.co/v1`); compare providers on the same model | https://huggingface.co/docs/inference-providers/index |
| Free tier | Free users get $0.10 per month in credits ("subject to change"); PRO gets $2.00 and can spend it on Spaces, Endpoints, Jobs; after credits you must buy more; HF passes provider prices through with no markup | https://huggingface.co/docs/inference-providers/pricing |
| hf-inference (old "serverless Inference API") | Now mostly CPU models: embeddings, rerankers, classifiers, small LLMs; billed by compute time past free credits | https://huggingface.co/docs/inference-providers/pricing |
| Playground | Chat with hosted models in the browser, no code | https://huggingface.co/playground |
| Usage page | See spend by model and provider (good cost drill) | https://huggingface.co/settings/inference-providers/overview |
| Spaces + ZeroGPU | Run anyone's demo; read its `app.py` in the Files tab. Daily GPU quota: 2 min anonymous, 5 min free, 40 min PRO; free accounts can host 2 ZeroGPU Spaces | https://huggingface.co/docs/hub/spaces-zerogpu |
| Model cards | Judge a model: intended use, limits, training data, eval claims | https://huggingface.co/docs/hub/model-cards |
| Dataset cards | Judge a dataset: sources, licence, bias notes | https://huggingface.co/docs/hub/datasets-cards |
| HF Jobs | Run a training or eval script on HF hardware from the CLI (used by smol course) | https://huggingface.co/docs/hub/jobs-overview |
| smolagents docs | Small agent library; read agent traces step by step | https://huggingface.co/docs/smolagents/index |
| lighteval | HF's evaluation toolkit for benchmark runs | https://huggingface.co/docs/lighteval/index |

Leaderboards:
- Open LLM Leaderboard is retired and archived; HF said it could push people to "hill climb irrelevant directions"
  (https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard/discussions/1135 ,
  https://huggingface.co/posts/burtenshaw/596060753193040). Read it only as history of benchmark saturation.
- Live and useful: MTEB for choosing embedding models (https://huggingface.co/spaces/mteb/leaderboard),
  LMArena mirror (https://huggingface.co/spaces/lmarena-ai/lmarena-leaderboard), GAIA for agents
  (https://huggingface.co/spaces/gaia-benchmark/leaderboard), Open ASR (https://huggingface.co/spaces/hf-audio/open_asr_leaderboard),
  and a search over all leaderboards (https://huggingface.co/spaces/OpenEvals/find-a-leaderboard).

Cookbook recipes for his track (all at https://huggingface.co/learn/cookbook/<slug>):

| Topic | Recipe | Slug |
|---|---|---|
| RAG | Advanced RAG on HF docs (LangChain) | `advanced_rag` |
| RAG | RAG backed by SQL and Jina Reranker | `rag_with_sql_reranker` |
| RAG | Semantic cache to improve a RAG system | `semantic_cache_chroma_vector_database` |
| Evals | RAG Evaluation (synthetic eval set, judge agent) | `rag_evaluation` |
| Evals | LLM-as-a-judge (build and check a judge against humans) | `llm_judge` |
| Evals | Evaluating AI search engines with `judges` | `llm_judge_evaluating_ai_search_engines_with_judges_library` |
| Agents | Agent with tool-calling using smolagents | `agents` |
| Agents | Agentic RAG with query reformulation | `agent_rag` |
| Agents | Text-to-SQL agent with error correction | `agent_text_to_sql` |
| Agents | Multi-agent web assistant | `multiagent_web_assistant` |
| Serving | Benchmarking TGI (latency and throughput) | `benchmarking_tgi` |
| Serving | Migrating from OpenAI to open LLMs via TGI Messages API | `tgi_messages_api_demo` |
| Observability | Phoenix dashboard on HF Spaces | `phoenix_observability_on_hf_spaces` |
| Inference | Serverless Inference API walkthrough | `enterprise_hub_serverless_inference_api` |

## 3. Fit rating for Faiz

Faiz: finance undergrad, coding since Aug 2026, reads and judges Python/SQL, does not want to write code; goal is production
AI engineering. Already has: token cost, model choice, retries/timeouts, FastAPI + Docker, eval sets and CI gates, SQL error
analysis, judge validation, BM25/embeddings/Recall@k/MRR/chunk size. Ratings are my judgement from section 1.

| Course | Fit | Why |
|---|---|---|
| Agents Course | **High** | Agents, tools, agentic RAG, observability with cost and latency; smolagents code is short and readable; certificate path mostly runs templates |
| MCP Course | **High** (Units 1-2), Medium (3) | Direct hit on MCP; Unit 3 is real server code, judge it rather than write it |
| Context Course | **High** | He already works through Claude Code skills, hooks, subagents; this names and structures what he uses daily |
| LLM Course ch.1-2, 4, 9, 11 (reading) | **Medium-High** | Foundations he should understand not implement: tokenizers, inference, model cards, Gradio demos, what fine-tuning and LoRA are |
| LLM Course ch.3, 5-8, 10, 12 | Low-Medium | Training loops, tokenizer internals, classic NLP tasks, GRPO; implementation depth he does not need now |
| Cookbook (selected recipes) | **High** | Read-and-run notebooks on exactly RAG, evals, judges, agents, serving |
| smol course | Low now | Write-heavy fine-tuning; evaluation unit unpublished; revisit only if a venture needs a custom model |
| Deep RL, CV, Audio, Diffusion, 3D, Games, Robotics | **Skip** | Outside LLM app engineering; mostly write-heavy; need PyTorch or Unity |

## 4. Recommended order

Principle: concepts he lacks first, then agents and MCP where HF is strongest, then use the Cookbook as a judged-evidence
library that maps onto what he already covered. Skip anything that repeats his existing work.

| Step | Material | Mode | Why here |
|---|---|---|---|
| 1 | LLM Course ch.1 (all) | read + quiz | What transformers are; "Inference with LLMs" and "Bias and limitations" |
| 2 | LLM Course ch.2: Behind the pipeline, Tokenizers, Optimized Inference Deployment | read | Links tokens to his cost work; the deployment section covers serving engines |
| 3 | LLM Course ch.4: The Hub, Building a model card | read | Teaches how to judge models on the Hub; pair with model and dataset card docs |
| 4 | Practice: Playground + Inference Providers usage page | run | Same prompt across 3 models and providers; record cost and latency; free tier is only $0.10 per month, so keep runs small |
| 5 | Agents Unit 0-1 | read + quiz | Thought-Action-Observation, tools, messages; earns Fundamentals certificate |
| 6 | Agents Unit 2.1 smolagents only | read/run | One framework is enough; skip 2.2 LlamaIndex and 2.3 LangGraph for now (same ideas, different API) |
| 7 | Cookbook `agents`, `agent_rag`, `agent_text_to_sql` | read/run | Text-to-SQL ties to his SQL error analysis; agent_rag extends his retrieval metrics |
| 8 | Agents Unit 3 Agentic RAG | run | Use-case assignment for the Completion certificate |
| 9 | Agents Bonus Unit 2 Observability and Evaluation | read/run | Langfuse traces, cost, latency, online vs offline eval; closest to production |
| 10 | MCP Course Unit 1 | read + quiz | Protocol, capabilities, clients, HF MCP server; Fundamentals certificate |
| 11 | MCP Course Unit 2 | run | Gradio MCP server on a Space, connect a client and a coding assistant |
| 12 | Context Course Units 1-5 | read + quizzes + small projects | Skills, MCP, plugins, subagents, hooks; Unit 2 overlaps MCP Unit 1-2, so skim it |
| 13 | Agents Unit 4 GAIA | run + judge | 20 questions, exact match, >30% for certificate; good exercise in reading failure traces |
| 14 | Cookbook evals: `rag_evaluation`, `llm_judge`, `llm_judge_evaluating_ai_search_engines_with_judges_library` | read | Compare with his own judge validation; look for what HF checks that he did not |
| 15 | Cookbook serving: `benchmarking_tgi`, `semantic_cache_chroma_vector_database`, `tgi_messages_api_demo` | read | Latency, throughput, caching; extends his cost and deploy work |
| 16 | LLM Course ch.11 (Chat Templates, SFT, LoRA, Evaluation) | read only | Understand fine-tuning as an option in model choice; do not do the code exam |
| 17 | MCP Unit 3 and Context Unit 6 Nano Harness | read and judge | Optional depth: real server and agent-loop code to review, not write |

What to skip and why:
- LLM Course ch.3, 5, 6, 7, 8, 10, 12: training loops, tokenizer training, classic NLP tasks, GRPO. Implementation depth; ch.12 is research-level.
- LLM Course ch.9 Gradio: only if he needs to ship a demo Space; he already deploys with FastAPI.
- Agents Units 2.2 and 2.3: second and third frameworks teach the same loop.
- Agents Bonus 1 (function-calling fine-tune) and Bonus 3 (Pokemon): fine-tuning and games, off track.
- smol course: write-heavy, and its evaluation unit is not out yet.
- Cookbook RAG basics (`advanced_rag` and the many vendor RAG recipes): he already covered BM25, embeddings, Recall@k, MRR, chunk size;
  read one only as a comparison.
- Open LLM Leaderboard: archived; use MTEB for embedding choice and GAIA for agents instead.
- All non-LLM courses (Deep RL, CV, Audio, Diffusion, 3D, Games, Robotics).

Rough time: steps 1-13 are about 8-10 weeks at the stated 3-4 h per week pace of the Agents and MCP courses
(https://huggingface.co/learn/agents-course/unit0/introduction , https://huggingface.co/learn/mcp-course/unit0/introduction).
Certificates reachable without writing much code: Agents Fundamentals and Completion, MCP Fundamentals, Context Fundamentals.
