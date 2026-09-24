# The curriculum map: borrowed structure, borrowed order

Written 2026-09-24. This replaces invention with what experts already use. Every element below names
its source; the evidence sits in the four research files beside this one:
- `teaching-structure.md`: how the best-evidenced courses teach (the unit template and what not to do)
- `expert-curricula.md`: the order 16 expert curricula agree on
- `huggingface.md`: every Hugging Face course, unit by unit
- `scaledojo.md`: the ScaleDojo platform (course of ~100 chapters, 58-level design lab)
ScaleDojo's Instagram captions were analysed on 2026-09-01 (`../../project-reasoning.md`); a fresh scrape on
2026-09-24 was refused by Instagram (rate limit, 429) and not forced.

---

## Part 1 · How every unit is taught (the structure)

One template, never changed between units (every framework course keeps one frame, teaching-structure A6).

**Size:** 20 to 25 minutes: 3 segments of 4 to 6 minutes (Ng, the 6.9-million-session edX study, ScaleDojo's
2 to 4 minute chapters). **Ratio:** about 1 part reading to 2 parts doing (CMU: doing gave 6 times the
learning of reading). No more than 250 words before he answers something.

| Step | Time | What happens | Borrowed from |
|---|---|---|---|
| 0 Recall | 2 min | 3 questions from earlier units: his mistakes queue, spaced at 1, 3, 7, 21 days | Duolingo mistakes review, Khan mastery challenges |
| 1 Goal card | 30 s | Three lines: "You will decide X." "Done when: 4/5 on the check and the lab target." "Case: [company]." | ScaleDojo opening problem, HF unit goals |
| 2 The failure | 1 min | One real case going wrong, with numbers | ScaleDojo chapter openings |
| 3 Segments x3 | 4-6 min each | a) predict or pick first; b) under 250 words with one worked example on named data; c) one check question, every option explained | Brilliant pretest, Hello Interview "try it first", HF quiz feedback, Ng in-video quiz |
| 4 Judge practice | 5-8 min | One of the five practice types below, always with a numeric target | ScaleDojo lab, Hello Interview, Hamel homework |
| 5 Check | 3 min | 5 questions, pass 4/5. A miss is "not yet": reread the segment, 5 new questions | Ng mastery quizzes, Khan, Launch School, ScaleDojo 70% |
| 6 Close | 30 s | One-line takeaway: the decision, when to choose it, the number that decides it | ScaleDojo takeaway table, Huyen chapter summaries |

**The five practice types** (he judges, never writes code; rotated, never added to mid-course):
1. **Pick the design:** 2 or 3 options with cost, latency and quality numbers; choose and name the deciding number (Hello Interview Bad/Good/Great).
2. **Set the knobs:** fixed components, he sets 2 to 4 values to hit a target, scored by rubric (ScaleDojo lab).
3. **Find the fault:** a trace, log or 10 to 20 lines of Python or SQL with one planted error; name the line and its cost (fast.ai notebooks, erroneous-example research).
4. **Label the outputs:** 8 to 12 real model outputs, pass or fail plus failure type; his agreement is computed (Hamel error analysis).
5. **Walk the frame:** a short brief, filled in the fixed steps: requirements with numbers, components, one deep dive, one trade-off (Alex Xu's 4 steps, Hello Interview).

**Module capstone** (every 4 to 6 units): one client case carried through the module, scored on ScaleDojo's
100-point rubric (completeness 20, configuration 20, fit 20, cost 15, latency 15, safety 10); pass 70,
otherwise "not yet" and one retry a week later (Launch School).
**Final capstone:** a public artifact scored against an outside benchmark (HF's GAIA test, pass above 30%),
plus a one-page design memo in the fixed frame.
**Rhythm:** fixed days, a fixed number of units a week, a module end date he sets once (Coursera dated
sessions, about 60% more completion; Duolingo streaks). He learns alone, so the rhythm replaces a cohort.

**Why this fits his own record** (docs/learning-evidence.md): short questions in one steady rhythm is what
the bootcamp did ("exactly what I needed"); decisions with numbers is what the builds did ("I liked the
build part"); a plainly stated goal answers "what am I supposed to do here" (C41); fixed stages answer
"unstructured and pointless" (C42); one unchanging format answers "the method is inconsistent" (09-14).

**What not to do** (teaching-structure Part C): long text or video with no check; read-only units;
self-paced with no dates; open research tasks for a novice (the stopped case-01 was exactly this);
no visible end; complexity before a simple working design; build-from-scratch coding; changing the
format between units; points as the goal; trusting a platform's own marketing numbers.

---

## Part 2 · What is taught, in what order

The consensus order from expert-curricula.md, stages 1 to 16. Done: stages 3, 6, 7; partly: 5, 13.
For each module: the primary reading (short, from the source itself), the practice, and the capstone.
"SD" = ScaleDojo (course module or lab level), "HF" = Hugging Face, "Huyen" = Chip Huyen, *AI Engineering*.

| Module | Stage (consensus) | Read (primary, then backup) | Practice | Module capstone |
|---|---|---|---|---|
| **M0 Consolidate** (1 week) | 3, 5, 6, 7, 13 done | none new | Recall step only, from the L1-L7 mistakes queue | none |
| **M1 How LLMs work** | 2 | SD Phase 2 mod 2-3 (tokens, embeddings, sampling, economics); HF LLM Course ch.1; Karpathy "Deep Dive into LLMs" in 20-minute parts; Huyen ch.2 | SD lab Act 0 levels -8 to -5; Act 1 levels 1-4 | SD level 6 "The Cost Calculator" |
| **M2 Prompting and structured output** | 4 | SD mod 3-4; Huyen ch.5; Anthropic prompt tutorial | SD levels 5, 8, 9 | SD level 9 "The Model Selector" |
| **M3 Evaluation, deeper** | 5 | Huyen ch.3-4; SD mod 8 and 14; HF Cookbook `llm_judge`, `rag_evaluation` | practice types 4 and 1 on real outputs | SD level 35 "The Evaluator" |
| **M4 Advanced retrieval** | 8 | SD mod 5-8 (ingestion, chunking, vector DBs, hybrid, reranking, citations, conversational RAG); Huyen ch.6 (RAG) | SD levels 11-20; the FBR tax corpus in projects/search/lab as a find-the-fault and set-the-knobs source | SD level 20 "The RAG Evaluator", then the FBR tax assistant scored on the rubric |
| **M5 Tools and MCP** | 9 | HF Agents Units 0-1; HF MCP Units 1-2; SD mod 9 | SD levels 10, 21, 22 | HF MCP Fundamentals certificate + SD level 21 |
| **M6 Agent patterns, workflows before agents** | 10 | Anthropic "Building effective agents"; SD mod 10-12; HF Agents Unit 2.1 and 3; Ng Agentic AI (optional) | SD levels 23-30 | SD level 29 "The Agent Evaluator" |
| **M7 Context and memory** | 11 | HF Context Course Units 1-5; SD mod 10 (memory) | SD level 24 | SD level 24 "The Memory Keeper" |
| **M8 Safety and guardrails** | 12 | SD mod 4 and 15; Huyen ch.5 (defensive prompting) | SD levels 8, 36 | SD level 36 "The Guard Tower" |
| **M9 Production: observe, test, recover** | 13 | Huyen ch.10; SD mod 15-16; HF Agents Bonus Unit 2 | SD levels 37-40 | SD level 39 "The A/B Tester" |
| **M10 Inference and cost at scale** | 14 | Huyen ch.9; SD mod 13; HF Cookbook serving recipes | SD levels 31-33 | SD level 33 "The Cache Layer" |
| **M11 Fine-tuning as a decision** | 15 | Huyen ch.7-8; SD mod 14; HF LLM Course ch.11 (read only) | SD level 34 | SD level 34 "The Fine-Tuner" |
| **M12 Final capstone** | all | SD Capstone module (7 chapters, a method for any GenAI design) | SD Act 5: level 47 "Trading Agent" (finance) or 41 "Enterprise RAG" | HF Agents GAIA test above 30% + a one-page design memo |
| Optional | 16 | SD "Transformers under the hood" and "RL for LLMs"; Karpathy Zero to Hero (watch, not code) | none | none |

**Where the experts disagree, and the pick made here:**
- Evals early or late: early (Huyen, Husain, Ng). His path already did this.
- Agent frameworks early or raw patterns first: patterns first (Anthropic), one framework only (HF smolagents).
- Coding: no expert curriculum is read-only. The defensible version is Ng's: read, judge and direct a coding
  assistant; run everything. The practice types above keep him in that mode.

**Size:** 12 modules of 4 to 6 units at 20 to 25 minutes, about 60 units. At 5 units a week, about 12 weeks
plus capstones. HF estimates its Agents and MCP steps at 3 to 4 hours a week for 8 to 10 weeks.

---

## Part 3 · Who does what

- **The sources explain.** The "Read" column is the source's own short chapter (ScaleDojo chapters are 2 to
  4 minutes; HF units are short sections). Claude does not rewrite them. This is the core change: the
  explaining is done by material refined on many learners, not invented per lesson.
- **Claude runs everything around the reading:** recall (step 0), goal card (1), the three predict-and-check
  segments built on that chapter (3), judge practice (4), the check with "not yet" (5), the close (6),
  the mistakes queue and spacing, and scoring capstones on the rubric. It explains extra only when asked.
- **ScaleDojo's lab is the practice ground** for "pick the design" and "set the knobs"; HF supplies
  certificates and real agent tests; Huyen supplies depth where a module needs it.
- **FaizOS becomes the tracker**: units done, check scores, mistakes queue, capstone scores, streak. The
  teaching rulebook stops growing: the template above is fixed and only his stated preferences change it.

## Part 4 · Decisions only he can make

1. **ScaleDojo Pro** (listed at ₹4,999, or ₹3,499 billed yearly; roughly US$40 to $57 a year; 7-day refund; check the exact terms on scaledojo.dev/pricing before paying): unlocks GenAI lab levels beyond the free
   primers and the quizzes. Without it, the "Practice" column falls back to Claude-built practice of the same five types.
2. **Huyen's book** (paid; price not verified): the depth layer for M3, M9-M11. Optional; the SD and HF
   material covers every module without it.
3. **Rhythm:** which days, and how many units a week (5 is the default above).
4. **Where to start:** M0 then M1, or straight into M4 (advanced retrieval), where L7 stopped.
