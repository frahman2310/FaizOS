# How the best technical courses teach: the unit, not the topic list

Checked 2026-09-24. This file is about teaching structure only. Topic order is in expert-curricula.md,
Hugging Face units in huggingface.md, ScaleDojo's catalogue in scaledojo.md, and the cognitive-science
findings in ../teaching-methods.md. Nothing here repeats those.

Every claim has a URL. Tags:
- **[M] measured**: a number from data (learner counts, completion, a study).
- **[S] stated**: the course or author describing their own method.
- **[M-self]**: a number the company reports about itself, not independently checked.

---

## Part 1. One unit, start to finish, per course

### 1. fast.ai, Practical Deep Learning for Coders
| Part | What happens |
|---|---|
| Opens | A complete working model on a real problem in lesson 1 ("Is it a bird?"), before any theory [S] https://course.fast.ai/Lessons/lesson1.html |
| Length | 9 lessons, each about 90 minutes of video [S] https://course.fast.ai/ |
| Concept | Top-down: use the whole tool, then how the tool works, then how it is built. Based on David Perkins' "whole game"; attacks "elementitis", teaching parts before the whole [S] https://www.fast.ai/posts/2016-10-08-teaching-philosophy.html |
| Doing | Watch, run the notebook, then rebuild it in a "clean" notebook with prose and outputs removed [S] https://course.fast.ai/Lessons/lesson1.html and https://github.com/fastai/fastbook/tree/master/clean |
| Check | End-of-chapter questionnaire; chapter 1 has 35 questions, all answerable from the text, answers online [M] https://github.com/fastai/fastbook/blob/master/clean/01_intro.ipynb |
| Open work | A "Further Research" section with no published answers [S] same notebook |
| Spacing | Topics are revisited at more depth later, framed by the authors as spaced repetition [S] https://www.fast.ai/posts/2016-10-08-teaching-philosophy.html |
| Community | Per-lesson forum threads and Discord [S] https://www.fast.ai/posts/2022-07-21-dl-coders-22.html |
| Evidence | Videos viewed over 6,000,000 times [M-self] https://course.fast.ai/ ; fastbook repo 25,321 stars (GitHub API, 2026-09-24) [M]. No completion rate published. |

### 2. Andrew Ng / DeepLearning.AI
| Part | What happens |
|---|---|
| Segment | Instructor plans each 5 to 10 minute segment; cutting a normal lecture into pieces "nearly always resulted in a worse learner experience" [S] https://ai.stanford.edu/~ang/papers/mooc14-OriginsOfModernMOOC.pdf |
| Check inside | In-video quizzes, weekly quizzes, randomised quizzes, and "mastery learning": students retry until right [S] same paper |
| Module shape (ML Specialization, course 1, module 1) | 20 videos (147 min total, about 7 min each), 3 practice quizzes, 4 ungraded 60-min labs [M] https://www.coursera.org/learn/machine-learning |
| Agentic AI | 5 modules, 31 videos, 9h55m, 8 graded assignments, module quizzes, ungraded labs [M] https://www.deeplearning.ai/courses/agentic-ai/ |
| Short courses | 1 to 2 hours, video beside a runnable notebook in the same tab [S] https://tinkerllm.com/blog/deeplearning-ai-short-courses-review/ |
| Community | Stack Overflow-style voted forum, chosen because 100,000-student forums drown in repeats [S] Ng paper above |
| Evidence | 2011 ml-class: 13,000 completers [M] Ng paper; course 1 has 1,251,897 enrolled, 4.9 from 32,922 reviews [M] Coursera page above; 4.8 million learners since 2012 [M-self] https://www.coursera.org/specializations/machine-learning-introduction |

### 3. Andrej Karpathy
| Part | What happens |
|---|---|
| Zero to Hero | Lectures of 56 min to 2h25m; you type the whole system from a blank file; each video builds on the last; needs "solid programming (Python)" [S] https://karpathy.ai/zero-to-hero.html |
| Deep Dive into LLMs | 3h31m general-audience walkthrough in the order models are built: data, tokens, pretraining, SFT, RL, psychology, use [S] https://x.com/karpathy/status/1887211193099825254 |
| Stated method | Education is "building ramps to knowledge", measured in "eurekas per second" [S] https://www.dwarkesh.com/p/andrej-karpathy ; learning should feel like effort, warns against short-form "learning" that is entertainment [S] https://x.com/karpathy/status/1756380066580455557 |
| Check | None built in. Discord only [S] zero-to-hero page |
| Evidence | Repos: nn-zero-to-hero 24,515 stars, nanoGPT 63,347 (GitHub API, 2026-09-24) [M]. No completion data. |

### 4. Hugging Face courses (Agents, MCP, LLM)
| Part | What happens |
|---|---|
| Opens | Unit states its learning goals, then concepts, then a build ("Alfred" agent), then share it on Spaces, then a quiz [S] https://huggingface.co/learn/agents-course/unit1/introduction |
| Check | Unit 1 quiz: 6 multiple-choice questions, each option carries its own explanation, right or wrong [M] https://huggingface.co/learn/agents-course/unit1/quiz1 |
| Pacing | 3 to 4 h per week, about a unit a week, no deadline (see huggingface.md) |
| Certificates | Fundamentals after Unit 1; Completion needs a final GAIA score above 30% on a public leaderboard (see huggingface.md) |
| Running case | One character (Alfred) carries across units (see huggingface.md) |
| Evidence | agents-course org has 71,392 followers (HF API, 2026-09-24) [M]; agents-course repo 32,829 stars [M]. No completion rate published. |

### 5. ScaleDojo (closest format to what he liked)
| Part | What happens |
|---|---|
| Unit | Chapters of 2 to 4 minutes, read in order; passed by reading or scoring 70%+ on the quiz; module completion gives one-time XP [S] https://scaledojo.dev/genai/learn/welcome/how-this-course-works |
| Opens | A concrete failure. ReAct chapter opens on a research question one LLM call cannot answer [S] https://scaledojo.dev/genai/learn/giving-llms-tools/the-react-pattern-reason-then-act ; chunking chapter opens on context split across chunks causing silent retrieval failure [S] https://scaledojo.dev/genai/learn/document-ingestion-and-chunking/chunking-strategies-that-actually-work |
| Body | 3 headed sections, 600 to 1,100 words, one step-through demo (ReAct: a 7-step scheduling trace) or a slider (chunk size 90 vs 150 chars splits or keeps a warfarin-aspirin warning), then a takeaway table, then "Interview Signal" (weak vs strong answer), quiz, and 2 lab buttons [S] same two pages |
| Lab | A client brief with budget, latency SLA and missions; drag nodes (Chunker, VectorDB, Reranker, LLM, SemanticCache, PIIRedactor...) and set knobs; live cost and latency gauges turn red when over [S] https://scaledojo.dev/blogs/genai-pipeline-lab-build-ai-architectures-from-zero-to-production |
| Grading | Mechanical: component present, wired right, configured inside limits [S] https://scaledojo.dev/genai/learn/welcome-to-genai/how-this-course-connects-to-the-genai-lab . 100 points: completeness 20, configuration 20, fit 20, cost 15, latency 15, safety 10; S/A = 3 stars, B 70-84 = 2 [S] blog above |
| Warm-up | 8 unscored tutorial levels before 50 graded ones [S] lab-connection page |
| HLD labs | Failure injection (crashes, partitions, spikes) with live metrics, then AI critique; 15 to 60 XP per level [S] https://scaledojo.dev/playground/level_1 |
| Evidence | None published on completion or outcomes. |

### 6. Hamel Husain and Shreya Shankar, AI Evals
| Part | What happens |
|---|---|
| Format | 15 live sessions for 11 lessons, 3 to 5 h a week, all recorded, 10+ h office hours, 200+ page reader, Discord [S] https://maven.com/parlance-labs/evals |
| Homework | One running app (Recipe Bot) across 5 steps: prompt iteration; synthetic queries then free-text notes on failures, deliverable a "taxonomy of failure modes"; LLM judge scored by TPR/TNR on train/dev/test splits; retrieval Recall@K and MRR; per-state pass/fail diagnostics. Each with video and solution [S] https://arize.com/blog/ai-evals-maven-course-homework-the-recipe-bot-workflow/ |
| Student view | Hour-long sessions, 4 weeks, cohort of 500+ (earlier 700); Zoom plus Discord split was "distracting" [S] https://alearningjourney.substack.com/p/what-i-learned-from-ai-evals-for |
| Evidence | Rated 4.7 from 901 reviews; "over 5,000 engineers and PMs" taught [M-self] maven page |

### 7. Chip Huyen, AI Engineering (book)
| Part | What happens |
|---|---|
| Chapter | Built around design decisions, not code; each chapter ends with a summary that restates purpose and links to the next chapter [S] https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md |
| Signposting | Warns before technical sections and says the reader may skip them [S] https://www.scribd.com/document/848711698/Preview-AI-Engineering-by-Chip-Huyen |
| Case studies | Content illustrated with case studies, many from her own work [S] https://www.goodreads.com/book/show/216848047-ai-engineering |
| Check | None. No exercises. |
| Evidence | "Most read book on O'Reilly since its release" [M-self] https://huyenchip.com/books/ ; aie-book repo 17,538 stars [M] |

### 8. Brilliant, Duolingo, Khan Academy (short, interactive, non-coding references)
| | Brilliant | Duolingo | Khan Academy |
|---|---|---|---|
| Unit | One concept per lesson, 5 to 15 min, instruction mixed with blocks of similar problems [S] https://brilliant.org/about/ | Lessons "take just a few minutes" [S] https://blog.duolingo.com/duolingo-teaching-method ; up to 17 exercises, mistakes replayed at the end [S] https://duoplanet.com/duolingo-learning-path/ | Skill levels attempted, familiar, proficient, mastered, proven through exercises, quizzes, unit tests, mastery challenges [S] https://blog.khanacademy.org/khan-academy-efficacy-results-november-2024/ |
| Order | Pretest first: learner tries before the procedure is taught [S] brilliant.org/about | Patterns met by doing before rules [S] teaching-method post | Practice to proficiency, then spaced mastery challenges [S] same blog |
| Feedback | Instant, custom per answer [S] | Next items mix familiar and harder [S] | Per-item |
| Evidence | "6x more effective" claim traces to a CMU study (below) [S] https://brilliant.org/faq/ | 225 learners who finished beginner courses read at the level of 4th-semester university students [M] https://onlinelibrary.wiley.com/doi/full/10.1111/flan.12600 ; spaced-repetition model raised activity 12% [M] https://research.duolingo.com/papers/settles.acl16.pdf ; a streak feature raised day-7 retention 14% [M] https://blog.duolingo.com/how-streaks-keep-duolingo-learners-committed-to-their-language-goals/ | 350,000 students: 30+ min a week linked to about 20% more than expected growth, but only 9% reached that dose; correlational [M] Khan blog above |

The study behind "doing beats watching": in a MOOC, one extra standard deviation of doing activities gave
more than six times the learning of extra watching or reading [M] https://dl.acm.org/doi/10.1145/2724660.2724681

### 9. System design prep (judgement without code)
| | Alex Xu / ByteByteGo | Hello Interview | Grokking (Design Gurus) |
|---|---|---|---|
| Fixed frame | Same 4 steps every problem: scope, high-level design with buy-in, deep dive, wrap-up; time split for a 1-hour interview [S] https://www.shortform.com/summary/system-design-interview-summary-alex-xu | 6 time-boxed steps: requirements 5 min, entities 2, API 5, data flow 5, high-level 10-15, deep dives 10 [S] https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery | Same method in every lesson: problem, requirements, high-level, deep dive, trade-offs [S] https://www.designgurus.io/course/grokking-the-system-design-interview |
| Trade-offs taught by | Diagrams plus back-of-envelope numbers [S] same | Numbers in the brief (Bitly: <100 ms, 99.99%, 1B URLs, 100M DAU); each deep dive shows a Bad solution then Good/Great ones with pros and cons; "Try it yourself first"; expectations for Mid, Senior, Staff [S] https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly | Short one-choice lessons (SQL vs NoSQL, strong vs eventual consistency) before full problems [S] Design Gurus page |
| Warning | | "Start simple", layering complexity early means never finishing [S] delivery page | |
| Evidence | Newsletter passed 1 million subscribers in 2024 [M-self] https://dev.to/somadevtoo/is-bytebytego-a-good-place-for-system-design-interview-prep-in-2026-9fo | none published | none published |

### 10. Mastery and cohort programs (only what transfers)
- **Launch School**: two-part assessment, a written test of concepts (open book, timed) and a live 1-on-1
  interview; a miss is "Not Yet" with a one-week wait before retry [S] https://medium.com/launch-school/on-launchschool-interview-assessments-926797cbaa81 ;
  "you cannot force mastery into a time-box"; admits indefinite duration is "the biggest source of anxiety" [S] https://public.launchschool.com/mastery ;
  outcomes: 2023 US Capstone graduates' average salary $116,763 [M-self] https://public.launchschool.com/salaries (selective: only top students enter Capstone).
- **Recurse Center**: self-directed; "work at the edge of your abilities" [S] https://www.recurse.com/self-directives . Suits experienced programmers, not novices.
- **Audited bootcamps (CIRR)**: only 3 schools still publish audited outcomes; Codesmith 2023-24: 70.1% in-field within 360 days, median $110,000 [M] https://www.cirr.org/schooldata and https://tripleten.com/blog/posts/coding-bootcamp-with-best-job-placement
- **Cohort vs self-paced**: Coursera found session-based (dated) courses about 60% more likely to be completed than self-paced [M-self] https://blog.coursera.org/coming-soon-to-all-courses-flexible-session-based ; Maven reports 96% week-1 to week-2 retention vs 16% for MOOCs [M-self] https://maven.com/resources/a16z-cohorts-are-king ; no independent study confirms the Maven figure https://aienablement.academy/insights/cohort-completion-rates-honest

---

## Part A. Patterns shared by the best-evidenced courses

Evidence strength: **strong** = independent study; **medium** = large platform data; **weak** = self-described only.

| # | Pattern | Used by | Evidence | Strength |
|---|---|---|---|---|
| A1 | **Short, planned segments with a check after each.** 2 to 10 minutes, then a question. | Ng (5-10 min + in-video quiz), ScaleDojo (2-4 min + quiz), Duolingo, Brilliant (5-15 min) | Engagement drops sharply past 6 minutes, 6.9 million sessions [M] https://dl.acm.org/doi/10.1145/2556325.2566239 ; Ng found planned segments beat chopped lectures [S] | strong |
| A2 | **The learner does more than they read.** Every unit ends in an activity, not a summary. | Brilliant (no videos), Duolingo, ScaleDojo labs, HF hands-on, fast.ai notebooks, Hamel homework | Doing gave 6x the learning of watching or reading [M] Koedinger 2015 above | strong |
| A3 | **Try first, then explain, with instant specific feedback.** | Brilliant (pretest), Hello Interview ("Try it yourself first"), HF quizzes (explanation per option), Duolingo | Brilliant stated [S]; productive failure and feedback effects in ../teaching-methods.md | medium |
| A4 | **Mastery gate with retries ("not yet").** A fixed pass mark; fail means review and retry with new items. | Ng (randomised quizzes, retries), Khan (proficient/mastered), Launch School (Not Yet), ScaleDojo (70%), HF certificates | Khan: each skill to proficiency linked to +0.5 pts learning, 221,000 students [M]; Launch School outcomes [M-self] | medium |
| A5 | **Whole working thing first, parts later, spiral back.** | fast.ai (whole game), HF (first agent in Unit 1), Hello Interview (simple working design first), Karpathy Deep Dive (in build order) | fast.ai 6M views [M-self]; no controlled comparison found | weak to medium |
| A6 | **One fixed frame reused on every problem.** Same steps, same order, time-boxed. | Alex Xu (4 steps), Hello Interview (6 steps), Grokking (5 steps), Hamel (analyse, measure, improve), ScaleDojo (same 6-part rubric) | ByteByteGo 1M subscribers [M-self]; consistent with worked-example and schema research in ../teaching-methods.md | medium |
| A7 | **Judgement taught by graded contrasts.** Bad vs good vs great, weak vs strong answer, with numbers. | Hello Interview (Bad/Good/Great), ScaleDojo (Interview Signal; 90 vs 150 char slider), Karpathy (base vs chat model shown side by side) | Contrasting-cases research in ../teaching-methods.md | medium |
| A8 | **Numeric targets and a mechanical rubric.** Brief gives budget, latency, quality; score is points, not opinion. | ScaleDojo (100-pt rubric, red gauges), HF (GAIA > 30%), Hamel (TPR/TNR, Recall@K), Hello Interview (<100 ms, 99.99%) | [S] across all four; no outcome study | weak (but fits him) |
| A9 | **One running case across units, ending in a public capstone.** | Hamel (Recipe Bot, 5 homeworks), HF (Alfred, then GAIA leaderboard), Karpathy (each video extends the last repo), ScaleDojo (capstone checklist) | [S]; HF org 71k followers [M] | weak to medium |
| A10 | **Spaced return and a fixed rhythm.** Old items come back; a small daily or weekly commitment. | Duolingo (HLR, streaks), Khan (mastery challenges), fast.ai (revisit topics), Coursera sessions | Duolingo +12% activity, +14% day-7 retention [M]; Coursera dated sessions +60% completion [M-self] | strong for spacing, medium for rhythm |

---

## Part B. Unit template for Faiz

Built only from A1 to A10. Source of each element in brackets. The template never changes between
units: same parts, same order, same labels (A6).

**Unit size:** 20 to 25 minutes, made of 3 segments of 4 to 6 minutes each (A1: Ng, Guo, ScaleDojo).
**Ratio:** about 1 part reading to 2 parts doing, by time (A2: Koedinger, Brilliant). No segment has more
than 250 words of explanation before he must answer something.

| Step | Time | What he sees | Source |
|---|---|---|---|
| 0. Recall | 2 min | 3 questions from earlier units, chosen by spacing (1, 3, 7, 21 days) and from his mistakes queue | Duolingo mistakes review, Khan mastery challenges (A10) |
| 1. Goal card | 30 s | Three plain lines: "You will decide X." "You are done when you score 4/5 on the check and hit the lab target." "Real case: [company or system]." | ScaleDojo opening problem; HF unit goals; his own need for a stated task |
| 2. The failure | 1 min | One concrete case that goes wrong, with numbers (e.g. cost 5x budget, a warning split across chunks) | ScaleDojo chapter openings (A5, A7) |
| 3. Segment x3 | 4-6 min each | (a) Predict or pick first, one question, before any teaching. (b) Explanation under 250 words with one worked example using named data and numbers. (c) One check question; every option has its own explanation | Brilliant pretest, Hello Interview "try it first", HF quiz feedback, Ng in-video quiz (A1, A3) |
| 4. Judge practice | 5-8 min | One of five fixed practice types (below), always with a numeric target | A2, A7, A8 |
| 5. Check | 3 min | 5 questions, pass at 4/5. Miss = "not yet": he rereads the linked segment and gets 5 new questions | Ng mastery learning, Launch School, HF 80% cert, ScaleDojo 70% (A4) |
| 6. Close | 30 s | One-line takeaway table: decision, when to choose it, the number that decides it | ScaleDojo takeaway table, Huyen chapter summary |

**The five practice types (he judges, never writes code).** Rotate them, never invent new ones mid-course:
1. **Pick the design.** Two or three options with cost, latency and quality numbers; choose and give the deciding number. (Hello Interview Bad/Good/Great; ScaleDojo Interview Signal)
2. **Set the knobs.** A mini lab: fixed components, he sets 2 to 4 values (chunk size, cache TTL, model, max steps) to hit a target; score by the rubric. (ScaleDojo lab and 100-point rubric)
3. **Find the fault.** A short trace, log or 10 to 20 lines of Python/SQL with one planted error; he names the line and the consequence in money or users. (fast.ai clean notebook; erroneous examples in ../teaching-methods.md)
4. **Label the outputs.** 8 to 12 real model outputs; he marks pass/fail and names the failure type, then the system computes his agreement. (Hamel error analysis, TPR/TNR homework)
5. **Walk the frame.** A short brief; he fills the fixed steps (requirements with numbers, components, one deep dive, one trade-off) in one line each. (Alex Xu 4 steps, Hello Interview time boxes)

**Feedback:** immediate after every answer; for choices, the reason each option is right or wrong; for labs,
the points per rubric line and which number was out of range (HF quizzes, ScaleDojo grading).

**Review and spacing:** every missed item joins a mistakes queue; the recall step pulls from it on days 1,
3, 7 and 21 (Duolingo, Khan). One module in five later reopens an old topic at more depth (fast.ai spiral).

**Module capstone (every 4 to 6 units):** one running client case carried through the whole module (Hamel
Recipe Bot, HF Alfred). The capstone is a single brief with budget, latency and quality targets; he designs
it with practice types 1, 2 and 5, and it is scored on a fixed 100-point rubric: completeness 20,
configuration 20, fit 20, cost 15, latency 15, safety 10 (ScaleDojo). Pass mark 70; below that, "not yet"
and one retry after a week (Launch School).

**Final capstone:** a public artifact scored against an outside benchmark or leaderboard (HF GAIA > 30%),
plus a 1-page design memo that follows the fixed frame (Alex Xu, Huyen).

**Rhythm:** fixed days and a fixed unit count per week, a visible streak, a module deadline he sets once
(Coursera session-based, Duolingo streaks). He works alone, so the rhythm replaces the cohort.

---

## Part C. What not to do (evidence of failure or drop-off)

| Do not | Evidence |
|---|---|
| Long videos or long text blocks without a check | Engagement falls sharply after 6 min [M] https://dl.acm.org/doi/10.1145/2556325.2566239 ; chopped lectures worse than planned segments [S] Ng paper |
| Watch-or-read-only units | Doing gives 6x watching [M] Koedinger; open MOOCs: 3.13% of participants completed in 2017-18, and 52% of registrants never started [M] https://www.insidehighered.com/digital-learning/article/2019/01/16/study-offers-data-show-moocs-didnt-achieve-their-goals |
| Self-paced with no dates | Dated sessions about 60% more completion [M-self] Coursera; Khan: only 9% reach the dose that works [M] |
| Open-ended "go research this" tasks for a novice | fast.ai's own "Further Research" has no answers by design [S]; minimal-guidance teaching underperforms for novices [M, review] https://www.tandfonline.com/doi/abs/10.1207/s15326985ep4102_1 ; Recurse-style self-direction assumes experience [S] |
| No end in sight | Launch School calls indefinite duration its biggest source of anxiety [S] https://public.launchschool.com/mastery . Give every module a size and an end |
| Adding complexity before a simple working design | Hello Interview: candidates who layer complexity early never finish [S] |
| Build-from-scratch coding as the main activity | Karpathy's series requires solid Python [S]; wrong mode for a learner who judges rather than writes |
| Splitting one course across many channels | Zoom plus Discord split was "distracting" [S] Hamel student review |
| Changing the unit format between units | Every framework course above keeps one frame for every problem (A6) [S]; also his own record of disliking AI-invented formats |
| Points and streaks as the goal | Streaks raise return visits [M] Duolingo, not learning; Khan's gains track skills mastered, not time logged [M] |
| Trusting marketing numbers | Brilliant's "6x" is the Koedinger doing-vs-watching result, not a Brilliant study; Maven's 96% is self-reported [S] |

---

## Gaps

- No published completion rate for fast.ai, Karpathy, Hugging Face, ScaleDojo, Hello Interview or ByteByteGo.
- YouTube view counts could not be pulled (YouTube returned 429 to yt-dlp on 2026-09-24).
- ScaleDojo quiz length and retry rules are behind the Pro paywall; lab level URLs load by JavaScript, so
  the lab description comes from ScaleDojo's own blog and course pages, not a live level.
- The PNAS Khan Academy causal study (https://www.pnas.org/doi/10.1073/pnas.2507708123) returned 403; its effect size was not checked.
