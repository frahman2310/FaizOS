# Curriculum design: what to teach, in what order, to what level, and how to measure it

Checked 2026-09-24. This file is about the design of the curriculum as a whole: levels, prerequisites,
placement, advancement and measurement. It does not repeat the files beside it:
- `expert-curricula.md`: the topic order experts agree on (stages 1 to 16)
- `teaching-structure.md`: the unit template, the 100-point capstone rubric, what not to do
- `skill-methods.md`: the five kinds of knowledge, the worked-example ladder, the 2-in-a-row rule
- `curriculum-map.md`: modules M0 to M12 and their sources
- `../teaching-methods.md`: question design, explanations, retrieval and spacing

Tags: **[M]** measured (a study or platform number). **[M-self]** a number a company reports about
itself. **[M-own]** a count made for this file from public data, method stated. **[S]** stated, no data.

---

## The short version

1. **Start from the job, then the evidence, then the lessons** (backward design). The job data is now
   good: 6,964 AI-engineer postings from 2026. Evaluation shows up in 59.7% of AI-first roles; RAG in
   39.8%; agents in 55.4%. Fine-tuning is rare (13.8%). The curriculum-map order already fits this.
2. **Whole tasks in task classes of rising complexity** (4C/ID) has the best evidence of any whole-
   curriculum framework: d = 0.79 across studies, strongest in higher education.
3. **Mastery learning works, but the size is smaller than the folklore.** About 0.5 SD on course tests,
   close to zero on broad standardized tests. A higher bar (91 to 100% on unit tests) gave bigger gains
   than 70 to 80%. Bloom's "2 sigma" does not replicate.
4. **The spiral curriculum has no direct evidence.** Its parts (spacing, interleaving) do. So use
   planned returns at a harder level, not a vague "we'll come back to it".
5. **Experts leave out most of what they do** when they explain it: 71% of knowledge steps and 73% of
   decision steps in one surgery study. Training built from cognitive task analysis beat normal training
   (g = 0.87). So worked examples must come from traces of experts working, not their summaries.
6. **Dreyfus stages are a useful vocabulary, not a measured ladder.** Turn each stage into observable
   tasks per skill. Three levels are enough for this learner: novice, competent, proficient.
7. **Self-ratings barely track real learning** (r = .29) unless he practises rating himself and is told
   how accurate he was (r = .51). So every check asks for a confidence rating first, then shows the gap.
8. **The design below:** five tracks, each with three levels and three or four task classes; one
   prerequisite graph of 40 concepts; one shared product that every module capstone extends; placement
   by graph inference; advancement by mastery plus a delayed check plus a rubric-scored capstone.

---

## Part 1. Curriculum design frameworks and their evidence

| Framework | What it says | Evidence | Grade | What we take |
|---|---|---|---|---|
| **Backward design** (Wiggins and McTighe, Understanding by Design) | Stage 1 decide the results, stage 2 decide the evidence that proves them, stage 3 only then plan lessons [S] https://files.ascd.org/staticfiles/ascd/pdf/siteASCD/publications/UbD_WhitePaper0312.pdf | Few controlled tests. One quasi-experiment: one teacher, classes of 15, 18 and 16, two UbD classes beat the third on understanding items and the gap lasted 5 months; the author says only "a few empirical studies" exist [M, tiny] https://files.eric.ed.gov/fulltext/EJ1431811.pdf . A research list exists but is compiled by McTighe himself [S] https://jaymctighe.com/wp-content/uploads/2025/11/UbD-Research-Studies.docx-11.25.25.pdf | weak (as an outcome method), strong as a planning discipline | Write each level's evidence (the check and the capstone) before its lessons. Part 6 does this |
| **4C/ID** (van Merrienboer) | Learning tasks are whole tasks, grouped in task classes from simple to complex; support fades inside each class and restarts at the next; supportive information for judgement, just-in-time procedures for routines, part-task drill only for routines [S] https://www.4cid.org/wp-content/uploads/2021/04/vanmerrienboer-4cid-overview-of-main-design-principles-2021.pdf | Meta-analysis: d = 0.79 on performance across areas and outcome types; higher education a significant moderator, suits it better [M] https://link.springer.com/article/10.1007/s10984-021-09373-y | moderate to strong | The backbone of Part 6: every track is a sequence of task classes |
| **Spiral curriculum** (Bruner) | Return to the same big ideas at rising depth | "No clear empirical evidence of the overall effects"; Bruner's 1960 book gave none; spiral is tangled with other methods so hard to test [S, review] https://files.eric.ed.gov/fulltext/EJ1286824.pdf . One cross-sectional medical study: spiral students 90% vs block 70% on one concussion item [M, weak design] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6327552/ . Its parts (spacing, interleaving) are strong, see ../teaching-methods.md section 4 | weak as a whole, strong in parts | Planned returns: each core concept is met in at least three task classes, each harder |
| **Mastery learning** (Bloom's LFM, Keller's PSI) | Do not move on until the unit is mastered; test, give feedback, correct, retest | 108 controlled studies: average +0.52 SD on exams; stronger for weaker students; takes more time [M] https://www.uky.edu/~gmswan3/575/kulik_kulik_Bangert-Drowns_1990.pdf . Unit bar 91 to 100%: 0.64; 81 to 90%: 0.44; 70 to 80%: 0.49 [M] same, table 2. In four studies with both test types, effects on standardized tests were "trivially small" (0.04 to 0.09) [M] same | moderate, on course-aligned tests | High bar per node; also test on something he did not train on (Part 5) |
| **Bloom's 2 sigma** (tutoring plus mastery) | Tutored students 2 SD above class | Not replicated: tutoring meta-analyses give about 0.33 to 0.37 SD; none of 96 rigorous studies reached 2 SD; narrow author-made tests averaged 0.84 SD vs 0.27 on standardized tests; in Bloom's source studies "feedback and retesting" gave about 1.1 of the 2 sigma [M] https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/ | strong (that the claim is inflated) | Expect gains of about a third to half an SD. The part worth keeping is feedback and retesting |
| **Knowledge graphs of prerequisites** (Math Academy, ALEKS, Khan) | Map every topic and its prerequisites; place the learner on the frontier; teach only what he is ready for | ALEKS meta-analysis, 15 studies, 24 samples: "as good as, but not better than" classroom teaching; shorter use gave bigger effects [M] https://eric.ed.gov/?id=EJ1232632 . Khan: 30+ min a week associated with effect 0.36 on MAP Growth, 350k students, correlational [M-self] https://blog.khanacademy.org/khan-academy-efficacy-results-november-2024/ ; a peer-reviewed version found 0.09 to 0.18 SD per extra 30 min a week or 60 skills a year [M] same page. Math Academy states placement in 20 to 60 questions instead of 500+ by using the graph [S] https://www.justinmath.com/files/the-math-academy-way.pdf p. 375 | moderate for the method, weak for any one platform | The graph is for placement and remediation, not a guarantee of learning. Part 4 builds it |
| **Competency-based education** | Progress by demonstrated competence, not seat time | Outcomes are "mixed" for learning and jobs; better access for adult and part-time learners [S, review] https://pnpi.org/wp-content/uploads/2023/04/CBEPrimer_Apr23.pdf . WGU median bachelor's in 24 months [M-self] https://www.wgu.edu/about/story/cbe.html . The known weak point is "reliable, defensible assessments of competence" [S] https://doi.org/10.3390/knowledge6030015 | weak to moderate | Take the rule (advance on evidence, not time) and invest in the assessment (Part 5) |
| **Cognitive task analysis** (Clark, Feldon) | Interview and observe experts at work to capture the decisions they no longer notice making | 20 studies: CTA-based training beat other ways of finding content, g = 0.87 [M] https://journals.sagepub.com/doi/abs/10.1177/1555343412474821 . Surgeons teaching omitted 71% of knowledge steps, 51% of action steps, 73% of decision steps [M] https://pubmed.ncbi.nlm.nih.gov/24667500/ (figures via the abstract). Surgery meta-analysis, 12 studies: SMD 1.36 on procedural knowledge, 2.06 on technical performance for trainees; little benefit for medical students, so some prior knowledge is needed [M] https://academic.oup.com/bjsopen/article/5/6/zrab122/6460901 . Nursing: 25 of 70 cues experts used were written nowhere [S] https://www.refsmmat.com/notebooks/cognitive-task-analysis.html | moderate to strong | Worked examples should be expert traces with decisions spoken aloud (Hamel's trace notes, Hello Interview walk-throughs), not tidy summaries. Use CTA-style material from level 2 on, when he has basics |

**How the frameworks fit together:** backward design decides what counts as done; job-task analysis and
CTA decide the content; 4C/ID decides the shape (task classes); the prerequisite graph decides the order
inside and across tracks; mastery rules decide when he moves; spaced returns keep it.

---

## Part 2. Skill progression: from novice to expert, as observable tasks

### 2a. What the progression models say

| Model | Claim | Evidence | Use |
|---|---|---|---|
| Dreyfus five stages: novice, advanced beginner, competent, proficient, expert | Rules without context, then situational cues, then chosen plans with felt responsibility, then seeing the situation whole, then intuition | Built from studies of chess players, pilots and tank drivers [S] https://en.wikipedia.org/wiki/Dreyfus_model_of_skill_acquisition . Benner applied it to nursing from interviews and narratives over 21 years [S] https://journals.sagepub.com/doi/10.1177/0270467604265061 . Critiques: too linear to explain everyday learning, and no objective criteria for who counts as expert [S] https://en.wikipedia.org/wiki/Patricia_Benner ; a medical-education critique of the model as a basis for clinical problem-solving [S] https://pubmed.ncbi.nlm.nih.gov/20563279/ | Vocabulary for levels; the levels must be defined by tasks, not feelings |
| Chi, Feltovich and Glaser 1981 | Novices sort problems by surface (pulleys vs inclined planes), experts by the principle that solves them | Classic lab study [M] https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog0502_2 | A clean test of level: can he group AI problems by the principle (a biased measure, a missing retrieval, a cost driver) rather than by the tool? |
| Deliberate practice (Ericsson) | Expertise comes from structured practice | 88 studies: practice explains 26% of variance in games, 21% music, 18% sports, 4% education, under 1% professions [M] https://journals.sagepub.com/doi/abs/10.1177/0956797614535810 | Hours alone will not produce a professional expert; feedback on real work matters more |
| SFIA (skills framework used by employers) | Levels of responsibility: 1 follow, 2 assist, 3 apply, 4 enable, 5 ensure and advise, 6 initiate, 7 set strategy. Machine learning skill: level 3 "applies established techniques... deploys models while monitoring", level 4 "assesses suitability, designs solutions, troubleshoots production" [S] https://sfia-online.org/en/sfia-9/skills/machine-learning | Industry standard, no outcome data | Maps our levels to job levels |

### 2b. Levels used here

Dreyfus's expert stage takes years of real work, so it is out of scope. The tracks use three levels:

| Level | Dreyfus stage | Job equivalent | Observable test |
|---|---|---|---|
| **L1 Novice** | novice to advanced beginner | none yet | Follows the fixed frame with steps shown; spots the principle in a worked example |
| **L2 Competent** | competent | junior: Dropbox IC1-IC2, SFIA 3 | Does a standard task of the class alone, in the frame, and justifies each choice with a number |
| **L3 Proficient** | proficient (narrow) | junior-to-mid: Dropbox IC2-IC3, SFIA 3-4 | Handles a new variation; says which input would flip the decision before computing; groups problems by principle |

### 2c. Milestones per track (what he can do, observed, at each level)

| Track | L1 Novice | L2 Competent | L3 Proficient |
|---|---|---|---|
| **Evaluation and error analysis** | Reads 20 traces and writes a note per failure; computes precision, recall, TPR/TNR from a given table | Builds a failure taxonomy from 50 to 100 traces with counts and cost; writes a pass/fail check; validates an LLM judge against his labels and states whether it can be trusted | Designs the eval plan for a new system (retrieval, answer, agent trajectory) before building; spots when a metric bends a decision and in which direction; sizes the eval set for the decision at stake |
| **How LLMs behave** | Predicts the direction of a change (temperature, context length, prompt order) with a one-line reason, right 3 out of 4 | Explains a real failure from the mechanism (tokenisation, sampling, missing context, post-training habit) and names the fix type | Chooses between prompt, RAG, tool, or fine-tune for a new case with the mechanism as the reason; predicts where a model will fail before testing |
| **System design** | Fills the design frame for a known brief with a worked example open | Designs a known problem type alone (single call, RAG, workflow) to the brief's numbers; scores 70+ on the rubric | Designs a new type; defends one trade-off with numbers; says what changes when one number in the brief changes 10x |
| **Production** | Computes cost per request, latency percentiles, cache savings from a given exhibit | Builds the cost and latency budget for a design; sets retries, timeouts and alert thresholds with a reason | Finds the input that dominates cost or failure; plans an A/B test with a sample size; reads a dashboard and says what to change |
| **Code** | Traces a 30-line function by hand and predicts output; orders given lines (Parsons) | Debugs with a fixed process (reproduce, hypothesis, check, fix); makes a 5 to 20 line edit that passes tests; reads a SQL query and says what it returns | Writes the spec and tests that make an AI assistant produce a correct change; reviews an AI diff and finds the planted bug; navigates an unfamiliar repo to the line that matters |

Sources for the milestone wording: Dropbox IC1 "navigates unfamiliar codebases", "escalates when stuck";
IC2 "independently... solve defined problems", "debug and read and navigate through a large code base";
IC3 "independently design software components in well scoped scenarios", owns operational issues [S]
https://dropbox.github.io/dbx-career-framework/ic1_software_engineer.html ,
https://dropbox.github.io/dbx-career-framework/ic2_software_engineer.html ,
https://dropbox.github.io/dbx-career-framework/ic3_software_engineer.html ; SFIA levels above; skill-type
content from skill-methods.md.

---

## Part 3. Deriving content from the job

### 3a. What AI engineer postings ask for (2026)

Source: Alexey Grigorev's field guide, 6,964 postings on builtin.com with "AI Engineer" in LA, New York,
London, Amsterdam, Berlin and India, eight monthly scrapes Feb to Aug 2026, skills extracted by an LLM and
normalised; he says treat shares as a floor [M] https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/02-skills.md

| Finding | Number | Track it feeds |
|---|---|---|
| Roles working directly on AI (RAG, agents) | 70.0% | all |
| AI-first roles asking for evaluation skills | 59.7% (LLM evaluation 30.9%, observability 24.5%, guardrails 17.9%) | Evaluation |
| Any agent skill | 55.4%; MCP rose from 9.9% to 17.6% in 8 months | System design, LLM behaviour |
| RAG | 39.8%; vector databases 1,647 jobs | System design, Evaluation |
| Python / SQL | 70.8% / 14.4% | Code |
| CI/CD, Docker, Kubernetes, observability | 2,560 / 1,700 / 1,666 / 1,547 jobs | Production |
| Largest hirers | Capital One, Citi, Optum, Wells Fargo, JPMorgan, BlackRock among the top 20 | finance domain is an asset, not a detour |

Responsibilities, share of 4,894 postings [M] https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/03-responsibilities.md :
building AI systems 98.1%; deploy to production 78.3%; infrastructure 69.2%; evaluation and quality 68.5%;
collaboration and communication 68.2%; monitoring 64.3%; API integration 62.4%; performance optimisation
57.2%; agents 48.4%; RAG 42.0%; security 40.1%; fine-tuning 13.8%. Between Feb and Jun, agents rose from
41.8% to 54.8% of postings and security from 35.5% to 44.9%.

### 3b. Junior vs senior tasks (own count)

Method [M-own]: 8,051 structured postings from the same repo (`job-market/data_structured`, scrapes to
2026-09-23), deduplicated by job id, AI-first only, split by title (junior, entry, graduate, associate,
"I" / senior, lead, staff, principal, manager, architect / neither), then keyword regex over each
posting's responsibility list. Junior n = 208 is small; treat differences under 5 points as noise.

| Share of postings mentioning | Junior (208) | Unmarked, mostly mid (2,548) | Senior and up (2,896) |
|---|---|---|---|
| test or debug | **48%** | 39% | 39% |
| RAG, retrieval, vectors, embeddings | **51%** | 42% | 47% |
| deploy or production | 68% | 73% | 74% |
| evaluate, benchmark, judge | 41% | 46% | **52%** |
| monitoring or observability | 42% | 40% | **52%** |
| design or architect | 59% | 60% | **74%** |
| lead, mentor, own, strategy | 57% | 55% | **78%** |
| agents | 60% | 64% | 67% |

Reading: junior roles lean to building and debugging retrieval features; evaluation, monitoring and
architecture ownership grow with level. His plan puts evaluation and design first because they are his
strengths and the senior differentiators, which is fine, but a junior hire is tested on code reading,
debugging and RAG. The code track cannot be optional.

### 3c. From the job to the curriculum (job-task analysis, done lightly)

1. Take the responsibility areas above with 40%+ frequency: build, deploy, evaluate, integrate, monitor,
   optimise, agents, RAG, security. These are the whole tasks.
2. For each, the tasks at junior level (Dropbox IC1-IC2, SFIA 3): these set L2.
3. For the decisions inside each task, use CTA-style sources where experts talk through real work:
   Hamel's trace notes and FAQ (evaluation), Hello Interview and ScaleDojo walk-throughs (design), Google
   SRE worked numbers (production). This is the fix for the 71% omission problem.
4. Check against interview reality: the field guide collects 2026 take-home assignments
   https://github.com/alexeygrigorev/ai-engineering-field-guide . One take-home per level is the external
   test in Part 5.

---

## Part 4. Prerequisite graph for the five tracks

Built from the orders in expert-curricula.md: Huyen (foundations, then evaluation, then prompting, then
RAG and agents, then fine-tuning, then inference, then architecture); Husain and Shankar (read traces and
build a failure taxonomy before writing evaluators); Anthropic (workflows before agents); Ng (evals and
error analysis before agent autonomy); roadmap.sh (embeddings, then vector databases, then RAG). Where an
edge rests on logic only it is marked (logic).

### 4a. Nodes (40)

| Track | Nodes (id: concept) |
|---|---|
| LLM behaviour (B) | B1 tokens and the context window · B2 sampling, temperature, non-determinism · B3 pretraining and post-training, why models hallucinate · B4 embeddings and similarity · B5 prompting and structured output · B6 tool calling mechanics · B7 context engineering, long-context decay, memory · B8 prompt vs RAG vs fine-tune |
| Evaluation (E) | E1 read traces, open coding · E2 failure taxonomy, counts x cost · E3 confusion matrix, precision, recall, sampling error · E4 code-based checks · E5 LLM judge and its TPR/TNR · E6 retrieval metrics (Recall@k, MRR) · E7 eval set design and CI gate · E8 agent and trajectory evaluation · E9 online evaluation and A/B tests |
| Production (P) | P1 cost per request · P2 latency and percentiles · P3 retries, timeouts, fallbacks · P4 caching economics · P5 throughput and rate limits · P6 monitoring, alerts, drift · P7 routing and cost at scale |
| System design (D) | D1 the design frame (brief, numbers, pipeline) · D2 single-call feature · D3 RAG design · D4 workflows (chain, route, parallel, evaluator-optimizer) · D5 tools and MCP integration · D6 agents with memory · D7 guardrails and prompt-injection defence · D8 production architecture · D9 fine-tune decision |
| Code (C) | C1 read and trace Python · C2 lists, dicts, JSON · C3 read SQL, aggregation · C4 API calls, HTTP, errors · C5 read tests · C6 debug process · C7 read async and concurrency · C8 steer an AI assistant with spec and tests · C9 read a service repo (FastAPI, Docker) |

### 4b. Edges (A -> B means A before B)

| Edge | Why | Source |
|---|---|---|
| B1 -> P1 -> P7 | cost is tokens x price; routing is choosing price | Huyen ch.2 then ch.9 |
| B2 -> E5, B2 -> P4 | a judge and a cache both depend on how repeatable output is | logic |
| B3 -> B8 -> D9 | the fine-tune decision needs to know what post-training changes | Huyen ch.2, ch.7 |
| B4 -> E6 -> D3 | measure retrieval before designing it | roadmap.sh; Huyen ch.3-4 before ch.6 |
| B5 -> D2 -> D4 | workflows are chained single calls | Anthropic "Building effective agents" |
| B6 -> D5 -> D6 | tools before agents | Ng Agentic AI modules 3 then 5 |
| B7 -> D6 | memory is a context decision | Microsoft agents lessons 12-13 |
| C2, C3 -> E1 -> E2 | traces are JSON; counting failures is SQL | Husain and Shankar (read traces first) |
| E3 -> E5, E3 -> E6, E3 -> E9 | every metric here is a confusion-matrix or sampling idea | logic |
| E2 -> E4 -> E5 -> E7 | failure types, then cheap checks, then a judge, then a gated set | Hamel FAQ order |
| E7 -> D4, E5 + B6 -> E8 -> D6 | no workflow without an eval set; no agent without trajectory evals | Ng The Batch Oct 2025; Huyen evals before agents |
| P1 + P2 -> D1 | the design frame needs cost and latency numbers | ScaleDojo and Hello Interview frames |
| C4 -> P3 -> D8, P4 + P6 -> D8 | production architecture needs failure handling and monitoring | Huyen ch.10 |
| E3 + P6 -> E9 | an A/B test needs sampling error and live metrics | logic |
| B6 + D5 -> D7 | injection attacks come in through tools and retrieved text | roadmap.sh agents security block |
| C1 -> C5 -> C8, C1 -> C6 | spec-with-tests needs reading tests; debugging needs tracing | skill-methods.md C5 |
| C4 + C7 -> C9 | a service repo is API code plus async | logic |

### 4c. The graph in short

```
Code:        C1 -> C2 -> C3 ----------------> (feeds E1)
             C1 -> C5 -> C8      C1 -> C6      C4 + C7 -> C9
LLM:         B1 -> B2 -> B5 -> B6 -> B7        B3 -> B8        B4
Evaluation:  E1 -> E2 -> E4 -> E5 -> E7 -> E8 -> E9      (E3 feeds E5, E6, E9; B4 -> E6)
Production:  B1 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7
Design:      D1 -> D2 -> D3 -> D4 -> D5 -> D6 -> D7 -> D8 -> D9
Cross-links: E6 -> D3   E7 -> D4   E8 -> D6   P3,P4,P6 -> D8   B8 -> D9   B6 -> D5, E8
```

Where he stands (from curriculum-map.md and expert-curricula.md, to be confirmed by placement):
likely mastered B1, P1, P2, P3, E1 to E7 basics, B4, E6, C1 to C3; partly C4, C5, C9 (FastAPI in Docker).

---

## Part 5. Measuring progress

| Measure | What the evidence says | Rule here |
|---|---|---|
| **Mastery bar** | Unit bars of 91 to 100% gave the biggest gains (0.64 vs 0.44 to 0.49) [M] Kulik 1990 above | A node is mastered at 2 correct in a row cold with a correct reason (skill-methods.md D2) **and** at least 9 of 10 on the node's mixed check |
| **Placement** | ALEKS places in about 25 to 30 adaptive questions by picking items that split the possible knowledge states in half [S] https://www.aleks.com/about_aleks/knowledge_space_theory ; Math Academy in 20 to 60, giving credit up the graph for a pass and down the graph for a fail, and marking low-confidence areas as "conditional" until later work confirms them [S] https://www.justinmath.com/files/the-math-academy-way.pdf pp. 375-376 | Placement check per track: start at the middle of the track's chain; pass = credit all ancestors, fail = test the parent. About 8 to 12 items per track. Inferred credit is conditional until he passes one task that uses it |
| **Retention** | Spacing and retrieval are strong (../teaching-methods.md section 4). Mastery-programme gains shrink on tests the learner did not train for [M] Kulik 1990 | Each mastered node gets delayed checks at 7 and 21+ days inside new work. A node that fails a delayed check goes back to "not yet" |
| **Transfer** | Narrow author-made tests inflate effects about 3x vs broad tests (0.84 vs 0.27) [M] von Hippel above | Each level ends with one external task he did not train on: a ScaleDojo lab level, a Hugging Face certificate, or a 2026 take-home from the field guide |
| **Rubrics** | 75 studies: rubrics raise scoring reliability, most when analytic, topic-specific, with exemplars and rater training; they do not make the judgement valid by themselves [M] https://www.sciencedirect.com/science/article/abs/pii/S1747938X07000188 | Analytic rubric with rows per track, anchored by one scored exemplar at 50, 70 and 90. The 100-point rubric in teaching-structure.md stays; each capstone adds track rows. Holistic score only as a sanity check |
| **Portfolio and capstone** | Consistent with CBE's rule of advancing on evidence; outcomes evidence is mixed [S] PNPI above | Every level produces one artefact kept in the repo: eval report, design doc, cost model, reviewed PR, LLM-behaviour write-up |
| **Self-assessment** | Self-ratings correlate .29 with real learning when made once, .30 when repeated without feedback, .51 when practised with feedback on accuracy; closer when the self-rating matches the test's form (.47 vs .24); a third of studies wrongly used self-ratings as proof of learning [M] https://gwern.net/doc/psychology/cognitive-bias/illusion-of-depth/2010-sitzmann.pdf | Before each check he states expected score and confidence per item; after, he sees the gap. Track the calibration gap as a number. Self-rating never counts as evidence of mastery |
| **Progress rate** | Khan uses "skills to proficient" per week as its outcome metric, about 2 a week in its guideline [M-self] https://blog.khanacademy.org/khan-academy-efficacy-results-november-2024/ | Headline metric: nodes mastered per week plus delayed-check pass rate. Time spent is not a progress measure |

---

## Part 6. The curriculum architecture for this learner

### 6a. Evidence first (backward design): what each level must produce

| Track | L2 evidence | L3 evidence |
|---|---|---|
| Evaluation | Failure taxonomy of 100 traces from his own system, with a validated judge (TPR and TNR reported) | Eval plan written before a new build, then a report showing the plan caught a real regression |
| LLM behaviour | 20 predict-then-run items, 80%+ correct direction with reasons | A written choice of prompt vs RAG vs tool vs fine-tune for two new cases, confirmed by a run |
| System design | Two designs of known types scoring 70+ on the rubric | One design of a new type scoring 70+, plus a "brief changed 10x" revision |
| Production | Cost and latency budget for a design within 20% of measured | A/B plan with sample size, and a monitoring plan with thresholds, applied to his product |
| Code | 5 debugging tasks solved with the fixed process; 3 edits passing tests | 3 AI-assistant changes steered by his spec and tests; 2 AI diffs reviewed with the planted bug found |

### 6b. Task classes per track (4C/ID): each class restarts at a worked example

| Track | Class 1 | Class 2 | Class 3 | Class 4 |
|---|---|---|---|---|
| Evaluation | single-call outputs, binary pass/fail | retrieval plus answer, two-stage metrics | multi-step workflow, per-step and end-to-end | agent trajectories and online A/B |
| LLM behaviour | one knob, one call (temperature, length) | prompt and context effects | tools and retrieved text in context | model choice and adaptation (fine-tune, routing) |
| System design | single-call feature | RAG system | workflow with tools | agent with memory in production |
| Production | per-request cost and latency | retries, caching, rate limits | monitoring and alerts | cost at scale and experiments |
| Code | read and trace one function | debug a script, read SQL | small edits with tests | steer an AI assistant on a service repo |

Classes run in step across tracks: class 2 in design (RAG) needs class 2 in evaluation (retrieval metrics).
Levels map to classes: L1 = class 1 done, L2 = class 2 done, L3 = class 3 done. Class 4 is stretch work
for the final capstone.

### 6c. How the tracks interlock: one product that grows

One product carried through every module capstone, so each capstone is a whole task touching all five
tracks. Suggested: the FBR tax assistant already started in `projects/search/lab`, grown from a single
call to a production agent. Finance postings being among the top hirers (Part 3a) makes this a portfolio
piece, not only practice.

| Capstone (curriculum-map module) | Product step | Evaluation | LLM behaviour | Design | Production | Code |
|---|---|---|---|---|---|---|
| M1-M2 | single-call answerer with structured output | pass/fail checks on 50 questions | prompt and temperature predictions | class 1 design | cost per answer | trace the call code |
| M3-M4 | RAG over the tax corpus | retrieval vs answer metrics, judge validated | why retrieved text changes answers | class 2 design | cache and latency budget | debug a retrieval bug |
| M5-M7 | workflow with tools and memory | per-step and end-to-end evals | tool-call failure modes | class 3 design | retries and rate limits | edit a tool with tests |
| M8-M9 | guarded, monitored service | online checks, A/B plan | injection behaviour | guardrails, D8 | alerts and dashboard | review an AI diff |
| M10-M12 | cost-optimised, routed, final memo | regression gate in CI | routing and fine-tune decision | class 4 design | cost at scale | steer an assistant on the repo |

Each capstone uses the analytic rubric with one row block per track (Part 5); a track's level only rises
when its row block scores 70%+ and the node checks are mastered.

### 6d. Spiral returns (planned, not vague)

- **Inside tracks:** every core concept appears in at least three task classes. Example: "a biased
  measure bends the decision" meets a judge (class 1), a retriever (class 2), an agent step (class 3).
- **Across time:** daily 3-minute recall at 1, 3, 7, 21 days (curriculum-map.md); delayed node checks at
  7 and 21+ days (Part 5); every module capstone revisits all five tracks at the next class.
- **Frequency:** a full-track return every 4 to 6 weeks (each capstone); a concept return every 1 to 3
  weeks inside new tasks. No review-only lessons: returns sit inside new work (../teaching-methods.md).

### 6e. Placement and advancement rules

1. **Placement (once, then after any 3-week break):** 8 to 12 items per track, walking the graph from
   the middle (Part 5). Result: each node marked mastered, conditional, or not yet. Start each track at
   its lowest not-yet node whose prerequisites are mastered.
2. **Conditional nodes** become mastered the first time he uses them correctly in a task; one miss sends
   them to not yet.
3. **Node mastery:** 2 correct in a row cold with a reason, plus 9/10 on the node's mixed check, plus a
   pass on the 7-day delayed check.
4. **Falling back:** 2 misses in a row on a node, or a failed delayed check, sends him to review the
   node's parents in the graph (Math Academy rule, skill-methods.md D2).
5. **Task-class advancement:** all nodes of the class mastered, the class's L-evidence (6a) produced,
   and the capstone's rows for that track at 70%+.
6. **Level-up:** class advancement plus one external transfer task passed (Part 5) plus the 21-day
   delayed checks for that class at 80%+.
7. **Calibration:** before every check he predicts his score; the gap is logged. A gap above 20 points
   two checks running triggers one lesson where he rates first and is shown the answer key item by item.
8. **Pace guide, not a deadline:** about 2 nodes a week per active track (Khan's rate), so the 40-node
   graph plus capstones fits the curriculum-map's 12-week estimate with room for fallbacks. Each module
   keeps a size and an end date (teaching-structure.md Part C).

### 6f. What FaizOS must store for this to work

Per node: status (not yet, conditional, mastered), last check date, delayed-check results, misses in a
row. Per track: current class and level, calibration gap. Per capstone: rubric rows by track. The
existing mistakes queue and rung-per-skill records already cover part of this.

---

## Gaps and cautions

- Most frameworks above were tested on school or college content, not on AI engineering; the 4C/ID and
  CTA results are the closest (complex professional skills).
- Kulik's mastery gains mostly come from course-aligned tests; this is why Part 5 adds external tasks.
- Backward design, spiral and CBE have weak outcome evidence; they are used here as planning rules.
- The junior-vs-senior split (3b) is my keyword count on LLM-extracted responsibilities, with a small
  junior sample. It shows direction, not precise shares.
- The Sullivan 2014 omission figures were read from the abstract via a search summary; PubMed's page did
  not render for the fetcher. Peña's 2010 Dreyfus critique was not readable (403); only its topic is cited.
- No public, company-issued career ladder specific to "AI engineer" was found; Dropbox (software) and
  SFIA (machine learning) are the nearest public frameworks. Blog "AI engineer ladders" were skipped as
  unsourced.
