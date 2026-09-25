# Learning structure: System design of AI/LLM products

> **Amended 2026-09-24:** the independent review (`review.md`) kept this structure with changes. Where this file disagrees with `INTEGRATED.md` (plain step names, shared recall queue, one mastery rule, start order, the week), `INTEGRATED.md` wins.


Written 2026-09-24. The skill: choose and connect components (retrieval, tools, agents, memory, guardrails,
serving) for a brief with a budget, a latency target and a quality bar, and defend each choice against the
alternatives. His words: "logic build-up + cognitive development". His own reasoning must grow, so every
class moves him from studying expert decisions to committing his own first (section 2, corrected 2026-09-25).

Builds on, does not repeat: `../recommended-method.md` (10-step unit), `../postmortem.md`,
`../curricula/judgement-training.md` (ShadowBox, crit, AAR, the 35-minute design session in 8c),
`../curricula/skill-methods.md` C3 (worked-example anatomy), `../curricula/scaledojo-method-analysis.md`,
`../curricula/method-effectiveness.md`, `../curricula/teaching-craft.md`, `../curricula/curriculum-design.md`
(task classes 6b). Materials: `private/research-base/system-design/` ("saved") and `private/scaledojo/` ("SD").

Tags: **[M]** measured in a study, **[M-dev]** measured by the method's own makers, **[S]** stated by an
expert or institution, no numbers. Grades in section 8: strong, moderate, weak.

---

## 1. What kind of learning this is, and what the new experts add

### 1a. The kind
Design is an ill-structured problem with many valid answers (Galster and Angelov 2016: students struggle
most when a problem "can be solved in many ways" [S] https://dl.acm.org/doi/10.1145/2889160.2889187 ).
Three things sit inside it, and each is trained differently:

| Part | Kind | How experts train it |
|---|---|---|
| Recognise the problem type and its usual shape ("tiered support", "tenant-filtered RAG") | case library, recognition | many worked cases per type; guess the expert's move |
| Put numbers on a design (tokens, requests a second, cost a day, latency per stage) | procedure, his strength | NALSD bill of materials, back-of-envelope |
| Choose between options and defend it (the trade-off) | judgement | kata, design review, ADR, crit on his own draft |

Unlike code (the machine is the judge) or evaluation (agreement with expert labels is a number), design has
no single key: two different designs can both meet the brief. So the check is **the brief's numbers plus a
rubric of reasoning, with partial credit where experts differ**, never "matches the reference".

### 1b. What the new experts add

| Expert or practice | What it adds | Tag and source | What it changes here |
|---|---|---|---|
| **Ted Neward, Architectural Katas** | Problem: architects "only get the chance to architect fewer than a half-dozen times in their career", so practise on invented briefs. Teams of 3 to 5, a moderator plays "customer, boss, project manager", teams design in a fixed time, present, answer questions, peers vote thumbs up / meh / down on whether they asked the right customer questions and chose "credible and feasible" technology | [S] https://nealford.com/katas/ ; rules https://www.architecturalkatas.com/rules.html | Claude plays the customer from a hidden fact sheet; unknowns must be written down as **assumptions**, which the kata judges |
| **Richards and Ford** | First law: "everything in software architecture is a trade-off"; second law: "why is more important than how". No best design, only the "least worst" set of trade-offs. Stakeholders pick the **top 3** architecture characteristics, not a ranking of all. Book katas: 45 minutes, then present and vote | [S] https://bagerbach.com/books/fundamentals-of-software-architecture/ ; https://danlebrero.com/2021/11/17/fundamentals-of-software-architecture-summary/ | Every brief starts with his top 3 characteristics; every decision records its cost ("least worst") |
| **O'Reilly Katas 2026 (AI-assisted architecture)** | Teams submit ADRs and diagrams; judges scored six criteria: innovative AI use, fit to constraints, right level of detail, handling uncertainty, alignment, and **proving the AI's results can be trusted** | [S] https://github.com/Humanberto/architectural-katas-2026 ; format https://www.oreilly.com/live-events/architectural-katas/0636920458487/ | Rubric dimension R6 (evaluation and trust) comes from this |
| **Google SRE, NALSD** | Design is iterated through fixed questions: basic design ("is it possible? can we do better?"), then scaled design ("is it feasible? is it resilient? can we do better?"). Numbers are a "bill of materials"; rough numbers are fine because the value is "combining many imperfect-but-reasonable results" | [S] https://sre.google/workbook/non-abstract-design/ | The session's middle steps are these questions, in this order |
| **NALSD classroom** | Groups of 4 to 6 with one experienced SRE facilitator; three breakouts (single datacenter 40 min, multi-datacenter 30 min, provision the system 35 min) with 5-minute breaks; groups do "their own solution first", then the leader presents a sample solution with the reasons; can be done "with a buddy or on your own" | [S] slides https://sre.google/static/pdf/nalsd-pubsub-slides.pdf ; https://cloud.google.com/blog/products/devops-sre/join-sre-classroom-nalsd-workshops | Design sessions are 40 minutes, longer than other skills; a mid-session break point is allowed |
| **Kleppmann (DDIA)** | Teaches tools by comparing them "so that you can see the strengths and weaknesses of each", goes "under the hood", and ties ideas back to reality: looking good "on a whiteboard" is not working | [S] https://dataintensive.net/ | Background reading is organised as trade-off tables per component, read before the class (the toolbox steps) and kept open during it |
| **Hohpe (Architect Elevator)** | Architects "see more dimensions": they turn an either/or into a third option; architecture is buying and selling **options** whose value grows with uncertainty; "what's the question?" before any diagram | [S] https://www.infoq.com/articles/thinking-like-architect/ | Changed-fact questions ask "which option did your design keep open?" |
| **Will Larson (Staff Engineer)** | A good design doc "describes a specific problem, surveys possible solutions, and explains the selected approach"; start from the problem; keep templates minimal; to improve, **reread your designs after building and study where the build deviated from the plan** | [S] https://lethain.com/static/blog/staffeng/staffeng-2020-12-16.pdf (pp. 41 to 43) | A design-vs-build deviation check on his FBR assistant (section 7) |
| **Google design docs** | Sections: context and scope, goals and non-goals, design, **alternatives considered**, cross-cutting concerns; the doc is "the place to write down the trade-offs"; 1 to 3 page "mini design docs" for small work | [S] https://www.industrialempathy.com/posts/design-docs-at-google/ | His written artefact is a 1-page mini design doc |
| **Amazon narratives** | Six-page memos read in silence at the meeting's start; Bezos: the narrative "forces better thought and better understanding of what's more important than what"; PR/FAQ starts from the customer | [S] https://www.cnbc.com/2018/04/23/what-jeff-bezos-learned-from-requiring-6-page-memos-at-amazon.html ; https://workingbackwards.com/concepts/working-backwards-pr-faq-process/ | Borrow only the internal FAQ: 3 hard questions a reviewer would ask, answered in writing (L3) |
| **AWS Well-Architected review** | A review is "a conversation and not an audit", "hours not days", blame-free, done early "to avoid one-way doors"; output: high- and medium-risk issues and an improvement plan. The Generative AI Lens has 29 questions over 6 pillars, e.g. GENSEC05 "How do you avoid excessive agency for models?", GENCOST05 "optimize agent workflows for cost", GENOPS01 "achieve and verify consistent model output quality" | [S] https://docs.aws.amazon.com/wellarchitected/latest/framework/the-review-process.html ; questions from https://github.com/aws-samples/sample-well-architected-custom-lens/blob/main/generative-ai-lens/generative-ai-lens.json | The flawed-design review uses these questions as the checklist; one-way vs two-way doors decide how much a decision deserves |
| **Nygard ADRs** | One short record per "architecturally significant" decision: title, status, context, decision, consequences (good and bad) | [S] https://adr.github.io/ | The session ends with one ADR for the hinge decision |
| **Cross; Lawson; Lloyd and Scott; Atman** | Experts move fast to an early **solution conjecture** and use it to explore the problem ("problem and solution co-evolve"); that ability comes from "specific experience of the problem type". Freshmen who spent a large share of time defining the problem did **not** produce better designs; seniors did benefit from problem scoping. Experts spent 69% more time scoping (Atman 2007) | [S, review of protocol studies] https://www.panda.sys.t.u-tokyo.ac.jp/kushiro/ReferencePaper/Nigel%20Cross/Expertise-overview.pdf ; [M] Atman 2007 https://onlinelibrary.wiley.com/doi/10.1002/j.2168-9830.2007.tb00945.x | **Challenge to the interview frames:** a novice does not get a long requirements phase. Scoping is boxed at 5 minutes; a conjecture comes early; scoping time grows with level |
| **Fricke (in Cross)** | Generating one or very few alternatives led to fixation; generating many led to time spent managing them. Good designers ran a "balanced search" | [M, protocol study, as reported by Cross] same PDF | 2 to 3 options per decision point, never 1, never 6 |
| **Ahmed (in Cross)** | Novice engineers used trial and error; experienced ones evaluated a tentative decision before building it | [M, as reported] same PDF | Numbers come before the lab canvas, not after |
| **Debiasing workshop (2025)** | 36 participants; a 60-minute workshop teaching (1) list several options, (2) list each option's drawbacks, (3) discuss risks. Biased statements fell from 49.9% to 23.1% (p = 0.0008); anchoring and optimism fell significantly | [M] https://arxiv.org/html/2502.04011 | Each decision row must carry options, a drawback and a risk |
| **Design reasoning cards (Schriek et al. 2016)** | 12 master's teams, 6 given cards (constraint, assumption, risk, trade-off): card teams did on average 75% more reasoning | [M, small] http://www.architecturemining.org/publications/SchriekWTB16.pdf | The four cards become the four prompts he sees when stuck |
| **Studies of graduates' design** | Graduating students given a design task: 38% had at least a first step towards a design, 2% a complete one (Eckerdal et al. 2006, as reported in the follow-up) | [M, as reported] https://www.researchgate.net/publication/228427888_Can_graduating_students_design_revisited | A degree does not produce design skill; explicit, repeated practice with feedback is needed |
| **Software architecture education research** | 50 studies over 28 years, mostly single-course experience reports judged by student feedback; very few controlled experiments (Oliveira et al. 2022). A 2026 map of 45 studies calls active methods "promising yet underexplored". A kata workshop in a university course was judged by student surveys only | [S, mapping] https://sol.sbc.org.br/index.php/cibse/article/download/20964/20790 ; https://doi.org/10.1145/3786580.3786954 ; https://dl.acm.org/doi/10.1145/3593663.3593694 | The formats are borrowed for structure; the effect sizes come from nearby measured methods (section 8) |

**What the new experts change in the earlier plan.**
1. The 25-minute unit in `recommended-method.md` is too short for a whole design: every expert format runs a
   design in 40 to 45 minutes (katas, NALSD breakouts, interview frames). Design gets its own anatomy.
2. The ScaleDojo 100-point rubric (completeness, configuration, fit, cost, latency, safety) scores the
   diagram, not the reasoning: it gives no points for alternatives, trade-offs or evaluation. The rubric in
   section 5 adds them.
3. Requirements-first frames suit experts; for a novice, long scoping does not help (Atman). Conjecture early,
   then check it with numbers (NALSD), then open the alternatives.
4. His written output is not a filled frame but two professional artefacts: a mini design doc with
   "alternatives considered", and one ADR. These are what the trade uses to reason in writing.

---

## 2. The structure: a ladder of rungs per task class (corrected 2026-09-25)

**Corrected 2026-09-25** after `../gap-audit-system-design.md` (findings S1 to S6, S9, K1) and
`../audit-pedagogy.md`. The earlier version opened every class with "guess the architect's move" and gave a
full "Design Crit" (his own design before any expert reasoning) from design 4 on, with component knowledge
read only after an attempt. For a novice that is commit-first on first contact, which the research base does
not support (`skill-methods.md` C3 and E; `method-effectiveness.md` line 34; `judgement-training.md` line 217;
Kapur and Roll's boundary conditions). The corrected shape follows the expert order: **show, try together,
then alone** (INTEGRATED 2.3), inside a ladder that restarts at rung 1 for every new task class.

Every unit is one rung of one class, written in unit format v3 (`learn/check_unit.py`: Kind show / try /
scored / close, Help blocks, Retry and Cold items). One decision per message, at most five short questions
per message, every term explained where it first appears, each try aimed at about 80% right.

**Rungs 1 and 2: study, then guess the move on a parallel case** (two units per class, each on a different
expert case).

| Order | Step (Kind) | What he gets | Source of material |
|---|---|---|---|
| 1 | **Goal and the problem** (show) | the failure with its stake, the one earlier idea it rests on, what "done" means; one self-explanation check | the class's ScaleDojo chapter |
| 2 | **Toolbox**, one step per decision point (show) | that decision's options, taught before any use: the problem first, the chapter's own toy example, one picture, and a table where every option has "wins on", "effect on the target number" and "what it loses" (C32, C35, B14); one or two short checks. The table stays available for the rest of the class | the matching ScaleDojo module (C1: modules 2 and 3; C2: 5 to 8; C3: 9 and 12; C4: 10 and 11) |
| 3 | **Worked example**, one step per decision (show) | an expert case modelled aloud: the cues and what each means, the options, the dead end and why it was dropped, the pick and why, then a 3-line replay (cue, what it means, move); one self-explanation question | ScaleDojo chapter text and its interview-signal weak/strong pair; Anthropic and other full-text sources; private excerpt per unit |
| 4 | **Guess the move**, one step per decision (try) | a parallel case (a real ScaleDojo lab brief where one exists), one decision per step, only decisions he has just seen worked; each step opens with the reveal of the previous one (expert cue and dropped option); feedback at once; a Help block (second worked example, new surface) for each | ScaleDojo lab level briefs and missions, never their simulation numbers (audit R2) |
| 5 | **How the scored part works** (show) | the scoring lines in plain words, then his score prediction (K2, C39) | |
| 6 | **Your move** on new briefs (scored) | the same decisions on briefs he has not seen, including at least one where the cue points to a different option (C35: decisions must not be obvious); pick, the brief fact that decided it, and a dropped option or a cost | ScaleDojo briefs; made-up briefs marked "Suppose", with the key taken from the expert rule |
| 7 | **Decision note** (scored) | a fill-in frame: "We decided to ___, because ___ (a brief fact). It costs us ___." | |
| 8 | **Close** (close) | "Next time I see X, I do Y", marked against the Key's expert rule before it enters recall (S12) | |
| after | **Help**, **Retry**, **Cold** | a prepared second worked example per try and scored step; a Retry brief after a miss; a Cold brief at 7 days, same decision, new surface | |

**Later rungs** (from `../gap-audit-system-design.md` section 5; move up only after 2 passes in a row, back one
rung after two misses at a rung, `skill-methods.md` D2):

| Rung | Steps, in order |
|---|---|
| 3 completion | First-step check (write only the first decision and its reason); Read the brief; Worked pipeline and numbers (given, one self-explanation question); Choices 1..n (his); Compare with the expert 1..n; What if; Decision note; Close |
| 4 faded | First-step check; Read the brief; Numbers (his, checked by a run); Choices 1..n; Compare 1..n; What if; Decision note; Close |
| 5 full design | First-step check; Read the brief; First design; Numbers; Choices 1..n; Compare 1..n; What if; Decision note; Close |
| 6 variation | as rung 5, on an old brief with one fact changed (the changed number tagged as a variation of its source) |

Rules that hold on every rung: every brief lists all its facts with their source, and unknowns as
"assume X" (no hidden fact sheet, C31, audit S8); "First design" (his own design before expert reasoning)
appears only from rung 5, after he has passed the completion rung and the first-step check, and the
productive-failure opening is used on the class's hinge decision, not on every step (audit S4); reveals are per
decision, never the whole design first; feedback narrates at most 3 changes (S15); the stuck order is the
shared one, with the two options in its step 2 taken from the toolbox table. The session length stays about 40
minutes for rungs 5 and 6; rungs 1 to 4 are sized by their steps, not a clock.

**Why this is not the other four skills' structure.**

| | Evaluation | Code | Production | LLM behaviour | **System design** |
|---|---|---|---|---|---|
| Unit of work | a batch of traces | a pattern or bug | a formula and a lever | one mechanism | **a whole brief** |
| Judge | agreement with expert labels | tests passing | the exact number | the measured run | **brief's numbers + reasoning rubric, partial credit** |
| Reveal | disagreements only | run result | worked solution | run result | **modelled first (rungs 1 and 2); per decision point after he commits (rung 3 on)** |
| Output artefact | taxonomy, judge | a passing change | a number and a lever | a one-line explanation | **mini design doc + ADR** |
| Session | 8 to 25 min | 30 min | short, mixed | 20 min | **rungs 1 to 4 sized by their steps; about 40 min for full designs** |
| Fading speed | slow | medium | fastest | barely uses examples | **slowest; restarts each class** |

---

## 3. Progression

### 3a. Task classes (4C/ID; each restarts at rung 1)

| Class | Example brief | Worked cases for rungs 1 and 2 (2 each) | SD lab levels to design from the brief |
|---|---|---|---|
| **C1 Single-call feature** (prompt, model choice, token budget, streaming, basic guardrail) | SD level 1 QuickChat: $5 per 1,000 requests, 2,000 ms, 10K DAU x 5 messages, 800-token conversations, some at 15K, "never cut off" | SD level 1 and 6 briefs worked by the tutor from `genai-sd-sdhandbook-genai-interview.md` (code assistant: 2B tokens a day) and the tiered moderation example in `genai-sd-myengineeringpath-worked.md` | 1, 4, 5, 6, 8, 9 |
| **C2 RAG** | internal Q&A over 10k PDFs, p95 under 3 s | MyEngineeringPath RAG support chatbot (500 articles, p95 < 3 s, faithfulness > 0.90); TopGenAIJobs production RAG | 11 to 17, 19, 20 |
| **C3 Tool-using workflow** | support desk with order lookup and refunds | SD "Enterprise RAG and Support Copilots" (support part: 50,000 tickets a day, 60% simple, 3 tiers); MyEngineeringPath code-review agent ($0.25 to $0.50 a review) | 21, 27, 28, 42 |
| **C4 Agent with memory** | research or ops agent that plans and remembers | SD "Autonomous and Multi-Modal Agents"; Anthropic multi-agent research system (saved note) | 22 to 25, 29 |
| **C5 Multi-tenant platform** (stretch, L3) | 50 departments, zero cross-tenant leakage | SD "Enterprise RAG" (2M documents, 10,000 concurrent users); SD "AI Operating Systems"; Huyen GenAI platform | 30, 41, 49 |
Serving, gateway, cache, cost, observability and recovery (SD levels 31 to 40) are not a class of their own:
they enter every class from C2 as the "twist" and as rubric lines, interleaved with `production.md`.
Classes run in step with evaluation (C2 design needs retrieval metrics from evaluation class 2).

### 3b. Fading rules inside a class
1. **Rungs 1 and 2:** study units (toolbox, worked example, guess the move on a parallel case), section 2.
2. **Rung 3:** completion (pipeline and numbers given; he writes the choices, the what-if and the note).
3. **Rung 4:** faded (pipeline given; he writes the numbers and the choices).
4. **Rungs 5 and 6:** full design, then a changed-fact variation.
5. **Support fades across levels, not only within a class:** L1 the tutor names the decision points; L2 he
   must find them (scored: did he find the expert's hinge decision?); L3 he also writes the customer
   questions and the internal FAQ (3 hard reviewer questions).
6. **Climb:** 2 passes in a row at a rung moves him up one rung; at rung 5, 2 designs in a row at 70+ on the
   rubric with all brief numbers met moves him to the next class. **Fall back:** two misses at a rung send him
   back one rung (Math Academy fail-twice rule, `skill-methods.md` D2).
7. **Skip:** from rung 2, each unit opens with a 90-second first-step check (write only the first decision
   and its reason). Right twice in a row with a right reason: skip the next study rung (Kalyuga).

### 3c. Levels with observable milestones

| Level | Milestone (observed, cold, a week after the last session on that class) |
|---|---|
| **L1 Novice** (C1 done) | In guess-the-move, matches the expert or an acceptable alternative at 60% or more of decision points; bill of materials within 20% of the expert's; names the top 3 characteristics the expert named, 2 of 3 |
| **L2 Competent** (C2 and C3 done) | Designs a C2 or C3 brief alone to 70+, all brief numbers met; finds the hinge decision without being told; every decision has 2 to 3 options with a drawback; answers the twist correctly on 4 of 5 components |
| **L3 Proficient** (C4 done, C5 started) | New domain cold at 80+; finds the planted flaw in 4 of 5 flawed designs; sorts 12 mixed briefs by governing principle (cost-driven routing, isolation, freshness, agency risk) with 10 right (Chi, Feltovich, Glaser: experts sort by principle); a ScaleDojo lab designed on paper passes on first build |

---

## 4. Practice formats (each with one concrete example from the saved materials)

| Format | How it runs | Concrete example |
|---|---|---|
| **1 Kata (the Design Crit)** | Section 2. The main weekly session | SD GenAI level 1, QuickChat: responses cut off mid-sentence; $5 per 1,000 requests, 2,000 ms, 10K DAU x 5 messages, 800-token average, power users at 15K tokens, "never cut off". Hinge decision: what to do with long histories (truncate, sliding window, summarise, bigger context model). Twist: power users grow to 30% of traffic |
| **2 Guess the architect's move** | Section 2, rungs 1 and 2 (on a parallel case, after the modelled one) | SD "Worked Example: Enterprise RAG and Support Copilots" (`learn/genai/capstone-designing-full-genai-systems/`): decision 1 "where does tenant isolation happen?" (expert: filter by tenant_id inside the vector search, before similarity search, not after); decision 2 "one pipeline or tiers for support?" (expert: 3 tiers, 0 automated, 1 agent with tools, 2 human) |
| **3 Mini design doc with alternatives considered** | 1 page: context, goals and non-goals, the design, alternatives considered (at least 2, each with why rejected), cross-cutting concerns (Google template). Written at the end of each class as the capstone of that class | SD level 42, AI Customer Support: 50,000 tickets a day, 60% simple. Alternatives he must weigh: one agent for everything; humans for everything plus retrieval suggestions; three tiers. Non-goal he must state (for example, no refunds above a set amount without a human) |
| **4 ADR** | End of every session, 5 to 8 lines, Nygard fields; one record's consequences become the next record's context | "Tenant isolation at query time. Context: 50 departments, zero leakage. Decision: tenant_id filter inside the vector query. Consequences: + a wrong-department chunk is unreachable; − per-tenant index tuning is harder; − every new data source must carry tenant_id" (from the SD worked example) |
| **5 Review a flawed design** | He gets someone else's design with one or two planted flaws; he runs the Well-Architected GenAI questions over it and lists high- and medium-risk issues and one fix each. Then the expert review. Only after 2 correct designs of that class (Große and Renkl) | SD interview signal (multi-agent chapter): a team wants to rebuild a single-agent support bot as five agents "for better answers". Checklist hits: GENCOST05 (agent workflow cost; Anthropic reports multi-agent systems use about 15x the tokens of chat, https://www.anthropic.com/engineering/multi-agent-research-system ), GENREL02 (communication between components), GENSEC05 (excessive agency) |
| **6 Changed-fact variation** | An old brief, redone cold with one number changed; he first says what moves, then redesigns only that part | SD level 6, The Cost Calculator: the assistant costs $52K a month, the CEO wants $15K "without users noticing", 70% of queries are simple lookups. Twist: simple lookups are only 40% of traffic. Does routing still reach $15K, or is caching now the main lever? |
| **7 Write first, then weak vs strong** (10-minute drill) | Prompt only; he writes 2 to 4 sentences; names the weak answer's type; marks which of the 4 moves (mechanism, consequence, alternative with cost, check) he had | SD pair on the Enterprise RAG chapter: a teammate wants to filter other departments' documents after retrieval "since it is simpler". Weak: "fine, they get filtered either way". Strong: post-retrieval filtering leaves the chunk reachable, one filter bug is a leak, query-time filtering makes it structurally unreachable |
| **8 ScaleDojo lab from the brief** | Sandbox on. He writes the design and numbers on paper from the case brief **before** opening the canvas; builds it; only then reads the missions as an after-check. Any design meeting the numbers passes by his rubric even if a mission is unticked. ScaleDojo's AI review is a second opinion; where it conflicts with the expert source, the source wins | SD level 41, Enterprise RAG Platform (KnowledgeBase Corp: 2M documents, 50 departments, answers only from their own documents). Paper first, canvas second, missions third |
| **9 Real case replay** (monthly) | He designs from a real team's constraints, then reads what they actually built and why (SRE "Wheel of Misfortune" idea applied to design) | Anthropic multi-agent research system (saved note): constraints and goal first; then their architecture, token cost and failure lessons |

---

## 5. Assessment

### 5a. Rubric (100 points), anchored in the expert frames
Scored per design by the tutor against a key prepared before the session. Where a panel of expert sources
disagrees (ScaleDojo vs Hello Interview vs MyEngineeringPath), any listed expert option gets full credit on
that decision (script concordance idea, `judgement-training.md` 2).

| Dimension | Points | 0 | Half | Full | Expert anchor |
|---|---|---|---|---|---|
| **R1 Framing** | 15 | jumps to boxes; no characteristics | top 3 listed but the driving number missing; assumptions unstated | top 3 match the brief; driving number named; assumptions and non-goals written | Richards and Ford; kata assumptions; Google goals and non-goals |
| **R2 Simplest workable design** | 15 | agent or multi-agent where a fixed workflow meets the brief; or a missing core stage | works but has one component without a reason | every component has one reason; nothing added before the simple version meets the brief | Anthropic "start simple"; NALSD "is it possible?" |
| **R3 Numbers** | 20 | no estimate, or off by 10x | estimate present, one brief number missed or unchecked | peak load, tokens, cost a day and per 1,000 requests, latency per stage; every brief number checked and met | NALSD bill of materials; BBG estimation |
| **R4 Options and trade-offs** | 20 | one option per decision | options listed, drawbacks missing, or choice not tied to a cue | 2 to 3 options per decision, the pick's drawback and risk, the deciding cue; one-way doors flagged | first law; "alternatives considered"; debiasing workshop; Fricke |
| **R5 Failure and safety** | 15 | no failure mode | failure modes named, no response | per-stage failure and fallback; guardrails; isolation; no excessive agency ("is it resilient?") | NALSD; WA GENREL03, GENSEC02, GENSEC05 |
| **R6 Evaluation and trust** | 10 | none | a metric named | how quality is measured before launch and watched after, with a threshold | Katas 2026 "prove the results can be trusted"; WA GENOPS01, GENPERF02 |
| **R7 The record** | 5 | no ADR | ADR without consequences | ADR with context and good and bad consequences | Nygard |
Each decision's written reason is also tagged with the 4 moves from ScaleDojo's strong answers (mechanism,
consequence, alternative with cost, check); the share of reasons with 3 or more moves is tracked (section 7).

### 5b. Mastery criteria
- **Per class:** 2 designs in a row at 70+ with every brief number met, then a **cold** design of a new brief
  in that class 7 days later at 70+ (mastery bar with delayed recheck, `recommended-method.md`).
- **Per level:** the milestones in 3c, plus one outside transfer task: a ScaleDojo lab of that class,
  designed on paper from the brief and passing on first build, scored 70+ on this rubric.
- **Not mastery:** a high in-session crit score. Structured reflection costs accuracy on the day and pays a
  week later (Mamede 2012, `judgement-training.md` 2), so only the cold score counts.

### 5c. Retention plan
| When | What | Why |
|---|---|---|
| Daily, 2 min (inside the shared recall slot) | 2 "cue → move" cards from his own AARs, at 1, 3, 7, 21 days | recognition of typical cases is most of expert judgement (Klein) |
| Weekly | the 10-minute drill (format 7) draws one pair from an old class | interleaving (d = 0.79 to 0.83) |
| Every 2 weeks | one old brief cold with a changed fact (format 6) | spacing plus transfer |
| Monthly | real case replay (format 9) and the sorting-by-principle test (12 briefs) | far transfer and principle-based sorting |
| After each build of the FBR assistant | reread the design doc; list decisions that held and those the build changed, and why | Larson's design-vs-build deviation study |

---

## 6. Weekly dose and session length

| Slot | Length | What |
|---|---|---|
| Main (Wed, fixed) | 40 min (Design Crit) or 30 min (Study variant); may split at the break point | section 2 |
| Drill (Sat, fixed) | 15 min | format 7 once (10 min) + one twist on an old brief (5 min) |
| Daily recall | about 2 min | cue cards, inside the shared slot |
| Every 4th week | 60 min, replaces the main session | format 8 (lab from the brief) or format 3 (class capstone doc) |
| **Total** | **about 65 to 70 min a week** | comparable to LLM behaviour, below code, above evaluation's 45 to 50 |

Why this length: every expert format runs one design in 40 to 45 minutes (Neward and Richards and Ford katas,
NALSD breakouts of 30 to 40, interview frames 45), because a design only shows its trade-offs whole. Why not
more: his record punishes long single blocks (postmortem table), so the session has one break point and the
drill is short. Why at least weekly: judgement grows with the number of cases met and compared (Klein; the
chess "serious study" finding), so volume comes from many small cases (drills, cards) around one whole design.
Pace: a class takes about 4 to 6 weeks (2 Study + 3 to 4 Crit + cold recheck), so C1 to C4 fit in about 5 months.

---

## 7. Measures that show it is working

| Measure | How | Healthy | Alarm |
|---|---|---|---|
| Cold rubric score | new brief of the current class, 7 days after the last session | 70+ (L2), 80+ (L3) | in-session crit 80+ but cold under 60: recognition, not learning |
| Guess-the-move match | share of decision points matching an expert option | rising within a class; 60%+ by design 2 | flat across 2 classes |
| Hinge found unaided (L2+) | did he name the expert's hinge decision? | 3 of 4 designs | under half |
| Options discipline | decisions with 2 to 3 options, a drawback and a risk | 80%+ | picks the first-listed option 80%+ of the time (anchoring) |
| Four-move coverage | reasons with 3+ of: mechanism, consequence, alternative with cost, check | 70%+ after 6 weeks | under 40% |
| Numbers | brief numbers checked and met; estimate within 20% of the expert's run | all met | same unit error twice |
| Twist accuracy | components that should move, named correctly | 4 of 5 | under 3 of 5 |
| Flawed-design detection (L3) | planted flaws found with a fix | 4 of 5 | under 3 |
| Calibration | predicted vs actual cold score | gap 10 points or less after 4 weeks | gap above 20 twice |
| Transfer | ScaleDojo lab of the class, paper first, passes on first build | yes, per class | fails and the design met the missions only by copying |
| Build deviation | FBR decisions that survived building | rising; reasons for changes named | changes he cannot explain |

---

## 8. Evidence grade for each choice, and what is excluded

| Choice | Evidence | Grade |
|---|---|---|
| Commit before any expert reasoning, then compare per decision | productive failure with consolidation d = 0.36 (only with comparison); ShadowBox 18 to 28% [M-dev]; debrief d = 0.67 | moderate |
| Worked cases first per class (rungs 1 and 2) | worked examples g = 0.48 for novices; conjecture needs "specific experience of the problem type" (Lloyd and Scott) | strong (examples), moderate (the design link) |
| 2 to 3 options, drawback, risk per decision | debiasing workshop, biased statements 49.9% to 23.1%, n = 36 [M]; cards +75% reasoning, 12 teams [M]; Fricke [M, protocol] | moderate (small samples, direct to software design) |
| Numbers step (NALSD bill of materials) | Google's stated practice [S]; plays to his measured strength (about 88% first-try on numbers) | weak to moderate |
| Scoping boxed at 5 min for novices | Atman: freshmen's long problem definition did not help, seniors' did [M] | moderate |
| Crit on his own draft | Schön's account [S]; code review research on knowledge transfer [M, surveys] | weak |
| Changed-fact twist | law hypotheticals, tactical decision games [S]; Think Like a Commander [M] | weak to moderate |
| ADR and mini design doc as outputs | Nygard, Google, Larson [S]; writing forces thought (Bezos) [S] | weak (as learning), strong as job practice |
| Reasoning rubric with partial credit | kata judging and SCT [S / M]; no validity study for this rubric | weak |
| 7-day cold recheck, spaced cue cards, interleaved drills | retrieval g = 0.51, spacing g = 0.74, interleaving d = 0.79 to 0.83 | strong |
| 40-minute session | expert formats [S]; no dose study for design | weak |
| Whole package | no controlled study of system-design teaching exists (mapping studies above); effects are carried over | weak for the package |

**Excluded, and why.**
| Excluded | Why |
|---|---|
| Group katas and peer voting | no peers; replaced by a panel of expert sources and partial credit. Calibrated peer grading needs peers (`judgement-training.md` 4) |
| Full six-page memos and PR/FAQ | built for funding decisions, hours of writing; only the internal FAQ is kept, at L3 |
| ATAM and formal architecture evaluation methods | heavy multi-day methods; the mapping study notes applying ATAM does not mean one can evaluate |
| Interview time pressure (45 min, talk aloud) before L3 | interview performance is a different skill; frames are kept, the clock is not |
| Reading DDIA or the saved essays front to back | passive (ICAP); read per component, as trade-off tables in the toolbox steps before the class |
| ScaleDojo missions as the design, and its reference-match pass rule | missions state the answer; valid alternatives fail; used only as an after-check |
| ScaleDojo quiz items as evidence of learning | 70% is reachable without reading the question (`scaledojo-method-analysis.md`) |
| Open "design anything" tasks with no expert key | open investigation failed (postmortem cause 3); minimal guidance underperforms for novices |
| Side-by-side comparison of several expert designs before L2 | novices learn less from comparison before one method is known; L1 compares with one expert, per decision |
| XP, leaderboards, certificates | reward completion, not skill |

## Gaps
- No controlled study of teaching system design, software architecture or LLM system design was found;
  the architecture-education literature is mostly experience reports judged by surveys.
- The kata-in-course report (ECSEE 2023) and the 2026 mapping study were read from abstracts only (full text
  refused connection); Eckerdal's 38% and 2% are as reported by the follow-up paper.
- Kleppmann's and Hohpe's teaching views come from their book pages and an article, not the full books.
- The Cross review reports Fricke, Ahmed and Lloyd and Scott second-hand.
- ScaleDojo levels 2 to 58 are locked in the saved copy except level 1 and the tutorials; briefs beyond the
  summary line must be read in the app (Sandbox on).
