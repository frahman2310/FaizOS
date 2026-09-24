# The curriculum map: borrowed structure, borrowed order (v2)

Written 2026-09-24. This replaces invention with what experts already use. Every element below names
its source; the evidence sits in the four research files beside this one:
- `teaching-structure.md`: how the best-evidenced courses teach (the unit template and what not to do)
- `expert-curricula.md`: the order 16 expert curricula agree on
- `huggingface.md`: every Hugging Face course, unit by unit
- `scaledojo.md`: the ScaleDojo platform (course of ~100 chapters, 58-level design lab)
ScaleDojo's Instagram captions were analysed on 2026-09-01 (`../../project-reasoning.md`); a fresh scrape on
2026-09-24 was refused by Instagram (rate limit, 429) and not forced.

---

## Part 1 · How it is taught: five skills, five methods (revised 2026-09-24)

The first version of this map used one unit template for everything. Faiz's own analysis (C44, handwritten
notes) showed that is the mistake the whole project kept making: the five skills are different kinds of
knowledge and each needs its own method. The evidence for each method is in `skill-methods.md`.

**The shared backbone for the three applied skills** (code, evaluation, system design), which is what he
asked for (C45: worked examples and detailed workings as the reference point):
**1 study a worked example → 2 completion problem (he writes the last steps) → 3 faded example (he writes
most steps) → 4 independent problem → 5 novel variation.** At every blank he writes his step and one line
of why before the expert step is shown. Worked examples come first because he is a novice in these
(van Gog 2011); his own attempt comes first once he has two worked examples of that problem type, and it is
always followed by a side-by-side comparison with an expert answer (Kapur 2014; Loibl and Rummel 2014).
That comparison is what the failed open investigation lacked, and the attempt-first step is what the old
explain-then-quiz lessons lacked.

| Skill (his label) | Kind of knowledge | Method | One worked example looks like | His own reasoning comes in | Checked against |
|---|---|---|---|---|---|
| **Evaluation** (core: logic + understanding + methods) | method + judgement | full ladder, slow | goal, givens, read and note 6 traces, group into failure types, count × cost, turn one into a pass/fail check, measure the checker, did the fix move the number, common wrong turns (Hamel's field guide in CFA layout) | labels traces before seeing the expert's labels; every blank step | expert labels (agreement computed), then the measured failure rate |
| **LLM behaviour** (understanding, "all learning") | facts + concepts | predict, run, explain; spaced recall. Few worked examples (for simple facts, answering first beats examples) | claim, predict, real run with numbers, why, cost or risk, where it breaks, recall question | the prediction before every run | the measured run |
| **System design** (core: logic build-up + cognitive development) | judgement | 2 worked examples per problem type, then he designs first and compares section by section; then the same brief with one number changed | brief with numbers, requirements, capabilities, pipeline, estimate, deep dive as Bad/Good/Great, cross-cutting layer, check against the brief, wrong turns, what a senior answer adds (Hello Interview + ScaleDojo) | every design from the third on, written before any reveal; one line per section "mine vs expert, which is better for this brief" | the expert design, the 100-point rubric, the brief's numbers |
| **Production** (small maths + quality control, applied) | procedure + applied maths | CFA-style worked numeric solution per new formula, faded fast (his strength); the real skill is "which input flips the decision" | exhibit, question, formula, substitution with units, answer and meaning, sensitivity, wrong turns (CFA + Google SRE) | the sensitivity and lever questions | the exact number, then the expert's lever |
| **Code** (core: understand, steer, write; "code needs to be learnt") | procedure, built by repetition | read and trace before explain, explain before write: predict output, Parsons problem (put given lines in order), fill 1 to 3 lines, find the bug with a fixed process, small edit, prompt problem (a spec that makes an AI assistant produce code passing given tests), review an AI diff | goal with one input and output, code with labelled blocks, trace table, why each block, the test, wrong turns, the spec he would give an AI | prediction before each run, hypothesis before each debug step, spec before each AI request | tests passing, then the expert solution |

**Moving from worked examples to independent work** (skill-methods.md D2, Math Academy's stated rules):
- Each unit opens with a 90-second first-step test on a new problem. Right step and right reason twice → skip the worked example.
- Climb one rung after 2 correct in a row with a correct reason; 2 misses in a row → back one rung and a prerequisite review.
- A harder problem type restarts at a worked example. A worked example is retired once he passes a new variation cold.
- Production fades fastest, system design slowest; LLM behaviour barely uses worked examples.

**The week** (5 units of 20 to 25 minutes plus 3 minutes a day; the core three take about 70%):
| Daily | Mon | Tue | Wed | Thu | Fri | Sat (optional) |
|---|---|---|---|---|---|---|
| 3-minute recall (LLM-behaviour cards, missed items at 1, 3, 7, 21 days) | Evaluation | Code | System design | Code + one predict-and-run | Production, mixed set | one cold item from each track |

**What stays from the first version:** short segments with a check after each; more doing than reading;
"not yet" with new questions instead of a fail; a scored module capstone every 4 to 6 weeks (ScaleDojo's
100-point rubric, pass 70); a final public capstone; a fixed rhythm; one unchanging format *per skill*.

**What not to do** (teaching-structure Part C and skill-methods Part E): one format for every skill;
open research tasks without a frame and an expert answer; the expert design shown before his attempt
(after the first two); AI-written code before he has specified it; generic metrics before reading traces;
long text with no check; self-paced with no dates; changing a skill's format mid-course.

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

## Part 3 · Who does what, and where the material comes from

- **Worked examples come from experts, not from Claude**, wherever one exists:
  - system design: ScaleDojo's worked-example chapters (HLD: URL shortener, chat, news feed, video, ad clicks; GenAI capstone: enterprise RAG, developer tools, search and tutoring, agents, AI OS; LLD: parking lot to chess), Hello Interview and ByteByteGo write-ups;
  - evaluation: Hamel Husain's field guide and the HF Cookbook eval recipes;
  - production: Google SRE worked numbers, CFA-format problems;
  - code: CS50, Exercism and ScaleDojo's Forge chapters (Python from variables to decorators, 84 chapters);
  - checks: ScaleDojo's quiz bank (every chapter has a quiz with the correct answer and an explanation) and its weak-vs-strong "interview signal" answers, which are ready-made contrast pairs.
  All ScaleDojo material is saved for his personal study in `private/scaledojo/` (git-ignored, never published).
- **Claude builds only the rungs the sources lack**: completion and faded versions of an expert example, variations with one number changed, first-step tests, and the scoring. Each generated item names the expert example it was cut from.
- **ScaleDojo's labs are the practice ground for design** (drag, connect, stress-test, AI critique); GenAI lab levels unlock in order as he completes them.
- **FaizOS tracks** rung per skill, first-step results, the mistakes queue and capstone scores. The teaching rulebook is replaced by this map; only his stated preferences change it.

## Part 4 · Decisions only he can make

1. ~~ScaleDojo plan~~: done, he bought Architect (2026-09-24).
2. **Huyen's book** (paid; price not verified): the depth layer for M3, M9-M11. Optional; the SD and HF
   material covers every module without it.
3. **Rhythm:** which days, and how many units a week (5 is the default above).
4. **Where to start:** M0 then M1, or straight into M4 (advanced retrieval), where L7 stopped.
