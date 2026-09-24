# Which teaching methods work best for Faiz: components ranked by evidence

Written 2026-09-24. Question: which method, or mix of methods, gives the most retention and transfer for one
adult learning alone with an AI tutor (Claude), ScaleDojo (Architect plan), Hugging Face courses and saved
expert material? Method: split every successful platform into its parts, rank the parts by evidence of
effect on learning (not engagement), then assemble the best set per skill.

Builds on, does not repeat: `../postmortem.md` (why the old system failed), `skill-methods.md` (method per
skill, worked-example ladder, fading rule, week), `ai-tutoring.md` (tutor moves, LLM tutor studies, hint
ladder), `teaching-structure.md` (unit shapes per course), `judgement-training.md` (commit-then-reveal
sessions), `curriculum-design.md` (order, mastery bar, placement), `../teaching-methods.md` (question design).
Where a number is already there, this file cites it and adds only the conditions and the grade.

**Tags.** [M-ind] measured on a test not written by the people who built the method (standardized or school
exam). [M-res] measured on a test the researchers wrote. [M-mix] a meta-analysis pooling both. [M-self] a
number a company reports about its own product. [S] stated, no numbers. [SR] learners' own report.
**Grades.** A = several meta-analyses or large RCTs, holds on delayed or independent tests. B = one
meta-analysis or a consistent set of experiments, mostly researcher tests. C = few studies, lab only,
engagement outcomes, or large unexplained spread. D = no usable learning evidence.

**Read this first: effects do not add up.** Researcher-made tests show about twice the effect of
independent ones (645 studies) [M-mix] https://journals.sagepub.com/doi/10.3102/0013189X16656615 ; narrow
author tests 0.84 vs 0.27 on broad tests (curriculum-design.md, von Hippel). Most component effects below
are researcher-test numbers, overlap heavily (retrieval, feedback and self-explanation are all parts of
tutoring), and apply to the same minutes. A realistic target for the whole combination is the size of good
tutoring: about 0.3 to 0.8 SD on delayed course-aligned checks, smaller on transfer (ai-tutoring.md 1a).

---

## The answer in five lines

1. **For keeping what he has learned:** spaced retrieval with explained feedback. Best-evidenced component in the whole literature (grade A).
2. **For new complex material (evaluation, design, code):** expert worked examples, self-explanation on the key step, then completion and fading (grade A for novices, reverses with expertise).
3. **For judgement:** commit to an answer, then compare step by step with an expert answer (productive failure with consolidation, contrasting cases, debriefs; grade B), only after two worked examples of that problem type.
4. **For the tutor:** step-based feedback from an expert key, in a fixed order the platform sets, answer held back until he tries (grade A for step-based tutoring; B for LLM tutors built this way; harmful when unstructured).
5. **For knowing it works:** a mastery bar with delayed rechecks, one outside transfer task per level, and his score prediction before each check. Most of the rest (gamification, peer review, long video, open cases) is excluded or kept as a small supplement.

---

## 1. Component evidence table

Ranked within each group by grade, then by size on the least-inflated test available.

### 1a. Core components (grade A or strong B)

| # | Component | Best effect size (test type) | Holds when | Weakens or reverses when | Grade |
|---|---|---|---|---|---|
| 1 | **Retrieval practice** | vs restudy g = 0.51, vs nothing 0.93; 272 effects, 188 experiments [M-res] https://journals.sagepub.com/doi/abs/10.3102/0034654316689306 . In real classes g = 0.50, 222 studies, 48,478 students [M-mix] https://pubmed.ncbi.nlm.nih.gov/33683913/ ; 80% vs 36% a week later [M-res] (skill-methods.md A2) | Answers are checked right after; the test asks for the same kind of thinking as the final task | Transfer to content never tested is small (Pan and Rickard 2018 https://pdf.retrievalpractice.org/transfer/Pan_Rickard_2018.pdf ); no feedback on low-accuracy items | A |
| 1b | Format: multiple choice vs short answer | MC practice g = 0.70, short answer 0.48 in Adesope (same URL). Counter-intuitive; explained by feedback and success rate | MC with an explanation for every option (HF quizzes, ScaleDojo) | MC without feedback can plant the wrong option. Free recall is best when the item is well learned. Rule: short answer or free recall first, then the options as a check | B |
| 2 | **Spacing** | Spaced vs massed retrieval g = 0.74, 29 studies [M-res] https://link.springer.com/article/10.1007/s10648-020-09572-8 ; best gap grows with the retention interval (Cepeda 2006, local copy `private/research-base/learning-methods/cepeda-2006-distributed-practice-meta.md`) | Gap about 10 to 20% of how long it must be kept | Gaps so long that recall fails and no feedback follows | A |
| 3 | **Worked examples, then fading** | g = 0.48 in maths, meta-analysis [M-res] https://link.springer.com/article/10.1007/s10648-023-09745-1 ; ITS meta-analysis: worked examples a top moderator (ai-tutoring.md 2a) | Novice, many interacting parts (d = 0.65 for examples on high-interactivity material; Chen, Kalyuga, Sweller 2015, skill-methods.md) | **Reverses with expertise**: generation beats examples on simple material (d = 0.96 the other way) and once the learner knows the procedure (Kalyuga 2007, local copy) | A |
| 4 | **Completion problems** | Completion group beat generation group on building programs, lower drop-out (high school, 10 lessons) [M-res] https://journals.sagepub.com/doi/10.2190/4NK5-17L7-TWQV-1EHL ; Parsons problems as good as writing on a one-week test, less time (skill-methods.md C5) | Between studying and solving; programming and procedures | Can train template copying without understanding (same study); pair with "why this step" | B |
| 5 | **Elaborated feedback** | Overall d = 0.48, 435 studies, N > 61,000; high-information feedback d = 0.99, corrective 0.46, praise or punishment 0.24 [M-mix] https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full ; computer-based: elaborated g = 0.49, right/wrong only 0.05 (Van der Kleij 2015, ai-tutoring.md 4f) | Says what was wrong, why, and how to do it next; about the task | About the person (over a third of feedback interventions made performance worse, Kluger and DeNisi, ai-tutoring.md); wrong feedback | A |
| 6 | **Step-based tutoring** | Step-based computer tutors d = 0.76, human 0.79, answer-only 0.31 (VanLehn 2011) [M-res] https://www.tandfonline.com/doi/abs/10.1080/00461520.2011.611369 ; field ITS 0.18 to 0.27 on state tests [M-ind] (ai-tutoring.md 2a) | He shows each step; feedback hits the first wrong step | Finer than step grain adds nothing (interaction plateau); field gains are a third of lab gains | A (lab), B (field) |
| 7 | **Mastery learning with a bar** | +0.52 SD, 108 studies; bar 91 to 100% gives 0.64 vs 0.44 to 0.49 for lower bars; on standardized tests 0.04 to 0.09 [M-res and M-ind] https://www.uky.edu/~gmswan3/575/kulik_kulik_Bangert-Drowns_1990.pdf | High bar, corrective loop, retest with new items | Gains mostly on course-aligned tests; costs time | B |
| 8 | **Self-explanation prompts** | g = 0.55, 64 reports (Bisra 2018) [M-res] https://link.springer.com/article/10.1007/s10648-018-9434-x | Focused prompt on the key step, while studying an example or after a bottom-out hint | Open "explain this" gives vague answers; costs time | B |
| 9 | **Interleaving** | g = 0.42 overall [M-res] (Brunmair and Richter 2019, ../teaching-methods.md 4); maths classroom RCT, 54 classes: 61% vs 38%, d = 0.83 [M-res, unannounced test] (skill-methods.md A2) | Confusable problem types where choosing the method is the skill | Simple word material; before each type has been learned once | B |

### 1b. Components for judgement and transfer (grade B, conditional)

| # | Component | Best effect size (test type) | Holds when | Weakens or reverses when | Grade |
|---|---|---|---|---|---|
| 10 | **Productive failure with consolidation** | d = 0.36 on conceptual and transfer, up to 0.58 with high fidelity, 166 comparisons, no loss on procedure (Sinha and Kapur 2021) [M-mix] https://journals.sagepub.com/doi/10.3102/00346543211019105 | He has the tools to attempt; teaching builds on his attempt and compares it with the canonical one | Without comparison: "no or negative effects" (Loibl, Roll, Rummel 2017, local copy); cold on a new task class | B |
| 11 | **Contrasting cases** | d = 0.50 comparing vs studying single cases (Alfieri et al. 2013) [M-res] (../teaching-methods.md 1c); side-by-side methods raised procedural flexibility, not conceptual (Rittle-Johnson and Star 2007) | Cases differ in one feature; explanation follows the comparison | Many differences at once; no telling afterwards | B |
| 12 | **Erroneous examples** | Delayed test d = 0.33, no difference immediately [M-res] https://link.springer.com/article/10.1007/s40593-015-0064-x | After correct examples; he must explain and fix, not only spot | Complete novices (Große and Renkl 2007, skill-methods.md) | B |
| 13 | **Expert critique, debrief, design review** | Debriefs d = 0.67, 46 samples, N = 2,136 [M-mix] https://pubmed.ncbi.nlm.nih.gov/23516804/ ; ShadowBox 18 to 28% closer to experts [M, developer-run] (judgement-training.md) | Structured, per decision, after he commits | Unstructured "any thoughts?" review | B |
| 14 | **Cognitive task analysis as the content source** | g = 0.87, 20 studies [M-res] https://journals.sagepub.com/doi/abs/10.1177/1555343412474821 ; experts omit about 70% of decision steps when teaching (curriculum-design.md) | Worked examples show the expert's decisions and cues, not just the result | Few studies, mostly medicine and military | B |
| 15 | **Prediction before demonstration** | Students who predicted a physics demo understood it better than those who only watched; watching alone was no better than not seeing it [M-res] https://mazur.harvard.edu/publications/classroom-demonstrations-learning-tools-or-entertainment ; review (Brod 2021) https://link.springer.com/content/pdf/10.3758/s13423-021-01904-1.pdf ; pre-questions g = 0.66 for asked content, 0.01 for other content (../teaching-methods.md 3) | Prediction with a one-line reason, answer shown at once | Coin-flip guesses; answer delayed | B |
| 16 | **Simulations and virtual labs** | g = 0.85, 145 studies, higher education, complex skills [M-mix, mostly researcher tests] https://journals.sagepub.com/doi/10.3102/0034654320933544 | **Low prior knowledge: supported by examples. High prior knowledge: reflection phases help more** (same study) | Unscaffolded exploration by novices | B |

### 1c. Components with weak, mixed or conditional evidence (grade C or D)

| # | Component | Best effect size (test type) | Holds when | Weakens or reverses when | Grade |
|---|---|---|---|---|---|
| 17 | **LLM tutors** | Harvard physics RCT (Kestin 2025), N = 194: 0.73 to 1.3 SD, 0.63 by regression [M-res] (ai-tutoring.md 3a). Ghana, Rori on WhatsApp, about 1,000 pupils, 8 months: 0.37 SD [M-res, growth test] https://arxiv.org/abs/2402.09809 . Turkey (Bastani 2025), about 1,000: plain GPT-4 17% worse on the exam without AI, guarded tutor about equal to control [M-ind, school exam] (ai-tutoring.md). **Khanmigo, 18 schools, 2 years, cluster RCT: 0.06 to 0.08 SD a year, same as Khan practice without AI; pupils messaged it in only 17% of sessions with a mistake** [M-ind] https://edworkingpapers.com/sites/default/files/ai26-1551.pdf . Undergraduates with AI while writing: +0.27 SD kept a week later; gains only for those who used it to explain, not to write [M-res] https://arxiv.org/abs/2607.08849 | Expert solution inside the tutor, fixed step order, answer withheld, learner actually uses it for explanations | Free chat, answers on request, learner not engaging | B for structured, harmful unstructured |
| 18 | **GenAI in general (meta-analyses)** | ChatGPT on learning g = 0.67 (35 studies) https://www.nature.com/articles/s41599-026-07019-z ; GenAI g = 0.68, **with teacher support 1.43, without 0.08** https://doi.org/10.1177/07356331251349620 [M-mix, many short, small, researcher tests] | A human or a fixed structure steers use | Unsupported use; novelty; researcher tests | C |
| 19 | **Automated feedback on open work** | Writing: g = 0.55, 20 studies, N = 2,828 [M-mix] https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2023.1162454/full ; AI feedback on self-regulation g = 0.51, 85 articles https://link.springer.com/article/10.1007/s10648-026-10166-z | Combined with other support; feedback checked against a rubric | Accuracy: plain GPT-4 made logic errors in 42% of maths solutions; ChatGPT gave wrong feedback 59% of the time in MathDial (ai-tutoring.md 5) | C |
| 20 | **Peer assessment** | g = 0.31, 54 studies [M-mix] https://link.springer.com/article/10.1007/s10648-019-09510-3 ; calibrated peer review: 65.5% of grades within 10% of staff after calibration (judgement-training.md) | Grading trains the grader, calibrated against expert grades | No peers in his setting | C (not usable as is) |
| 21 | **Gamification** | Cognitive g = 0.49, only k = 19, N = 1,686; motivational 0.36; behavioural 0.25 [M-mix] https://eric.ed.gov/?id=EJ1245270 . No element (fiction, competition, collaboration) moderated the cognitive effect; competition plus collaboration beat competition alone only on behaviour (full text https://d-nb.info/1202307655/34 ). Streaks: +14% day-7 return, not learning [M-self] (teaching-structure.md) | As a rhythm aid | Points as the goal; nothing shows which element carries learning | C |
| 22 | **Video and segment length** | Adding video to teaching g = 0.80; replacing teaching with video 0.28; 105 studies [M-mix] https://journals.sagepub.com/doi/10.3102/0034654321990713 . Engagement drops after 6 minutes (6.9 million sessions) [engagement only] (teaching-structure.md A1); learner-paced segments g about 0.32 to 0.36 (Rey 2019, ../teaching-methods.md 2d) | Short, planned, as a supplement with a check after | Long passive video as the main activity | B (supplement), C (as the method) |
| 23 | **ICAP (interactive > constructive > active > passive)** | Framework review; the direct classroom test (Menekse et al. 2013, engineering) found I > C > A > P on researcher tests; review of 71 ICAP studies: mostly lab, two-condition comparisons https://files.eric.ed.gov/fulltext/EJ1422395.pdf ; Chi and Wylie 2014 https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chiwylie2014icap_2.pdf ; doing 6x watching in a MOOC [M-res] (teaching-structure.md) | Constructive (generate something not in the text) beats active and passive: well supported | **Interactive over constructive is the weakest link**; Thurn et al. 2023 question the assumptions (cited in the ERIC review). For him "interactive" means dialogue with Claude, which has no independent test | B for C > A > P, C for I > C |
| 24 | **Dual coding, diagrams, multimedia design** | 29 reviews, 1,189 studies: 11 principles with positive meta-analytic effects; largest for signalling and placing words next to the picture they describe [M-mix] https://journals.sagepub.com/doi/abs/10.3102/00346543211052329 | A diagram replaces text, labels sit on the picture, one thing highlighted | Decorative pictures, seductive details (../teaching-methods.md 2b); "learning styles" matching has no support | B (design rules), D (styles) |
| 25 | **Goal setting and visible progress** | Monitoring goal progress d = 0.40, 138 RCTs, N = 19,951; larger when progress is recorded and reported [M-mix, mostly health goals] https://pubmed.ncbi.nlm.nih.gov/26479070/ ; a large field test of reflective goal setting in higher education found no effect https://www.tandfonline.com/doi/full/10.1080/19345747.2023.2231440 | Progress is physically recorded, specific | Vague goals; progress shown as points not skills | C for learning |
| 26 | **Metacognitive calibration (predict your score)** | Interventions raise monitoring accuracy g = 0.25, 35 studies [M-res] https://www.researchgate.net/publication/383307111_Meta-analysis_of_Interventions_for_Monitoring_Accuracy_in_Problem_Solving ; self-ratings correlate .29 with real learning, .51 when practised with accuracy feedback (curriculum-design.md) | Prediction compared with the real score every time | Changing when the judgement is made hurt accuracy (same meta) | C for learning, B as a **measure** |
| 27 | **Case-based learning** | Liked by students; effect on learning "inconclusive", 104 papers (BEME) https://pubmed.ncbi.nlm.nih.gov/22578051/ | The gains come from moves inside cases (commit, reflect, debrief) | Open discussion of a case as the method | C |
| 28 | **Immediate vs delayed feedback** | Classroom studies favour immediate; lab list-learning favours delayed (Kulik and Kulik 1988, 53 studies) https://journals.sagepub.com/doi/abs/10.3102/00346543058001079 ; delayed lowered effects in computer-based learning (Van der Kleij 2015) | Immediate for procedures and steps | Delayed helps retention mainly in lab tasks; spacing gives the same delay benefit without withholding help | B (immediate for his skills) |

---

## 2. Platform decomposition

Component numbers refer to section 1. "Outcome data" is for the platform as a whole.

| Platform | Components used | Outcome data for the platform | Grade of that data |
|---|---|---|---|
| **ScaleDojo** (Architect) | 2 to 4 min chapters, one idea (22); worked-example chapters: HLD 7, GenAI 7, LLD 9, API 4, Forge 3 (3, 14); 1,085 quiz items with answer and explanation (1, 5); 358 weak vs strong "interview signal" pairs (11); drag-and-drop labs with gauges and failure injection (16); AI critique of designs (19); XP (21); 70% pass per chapter (7, low bar) | None published (teaching-structure.md Part 1.5) | D |
| **Math Academy** | Knowledge graph, placement test, worked example then 2 to 5 practice items per step with subgoal labels (3, 4), fail twice then prerequisite review (7), spaced review down the graph (1, 2), mixed reviews (9), XP (21) | "4x more efficient" is a time estimate for AP Calculus BC; lessons passed 93% first time, 98% second [M-self] `private/research-base/learning-methods/mathacademy-faq.md` . No independent trial found | D (self only) |
| **Khan Academy** | Video worked examples (3, 22), step hints ending in a full solution (6), mastery levels and challenges (7), spaced mastery challenges (2), Khanmigo tutor (17) | RCT 11,000 pupils, mastery programme: 0.12 to 0.22 SD; India RCT with a supervisor ensuring about 1 h a week: 0.44 to 0.47 SD; Khanmigo 2-year RCT: 0.06 to 0.08 SD a year [M-ind] (`khan-multiple-studies-learning-gains.md` local; Khanmigo URL in row 17). Usage-linked 0.36 in a quasi-experiment [M-self] | B (independent RCTs exist; effect depends on dose) |
| **Brilliant** | Problem before explanation (10, 15), short lessons (22), custom feedback per answer (5), streaks (21) | "6x more effective" is Koedinger's doing-vs-watching MOOC result, not a Brilliant study (teaching-structure.md Part C) | D |
| **Duolingo** | Short lessons, mistakes replayed (1), half-life spaced repetition (2), streaks and leagues (21, 25) | Finishers of beginner courses read at 4th-semester university level, N = 225, no control group [M-res] https://onlinelibrary.wiley.com/doi/full/10.1111/flan.12600 ; spacing model +12% activity, streaks +14% return (engagement) [M-self] | C |
| **CS50 / CS50.ai** | Problem sets with a pseudocode scaffold (4), check50 tests (5, 6), AI duck that withholds answers (17) | Duck answered forum questions 88% and 77% correctly; 211,000 users; students felt it was "a personal tutor" [SR] https://cs.harvard.edu/malan/publications/fp0627-liu.pdf . No learning comparison | C (accuracy), D (learning) |
| **CS1-LLM (UCSD)** | Read, explain, test and decompose before writing; LLM from week 1; open projects | Exams roughly the same as earlier CS1 years on tracing and reading, slightly lower on writing from scratch [M-res, historical comparison] https://arxiv.org/abs/2406.15379 | C |
| **Hamel and Shreya, AI Evals** | One running app across 5 homeworks with solutions (3, 4), open coding then taxonomy then counts (14), judge measured against human labels (26 in another form), live sessions (22) | 4.7 from 901 reviews, "5,000+ taught"; NurtureBoss 33% to 95% after fixes is a client result, not a learning result [M-self] (teaching-structure.md) | D |
| **Hello Interview / ByteByteGo** | Fixed frame every problem (3), "try it yourself first" (10), Bad/Good/Great deep dives (11), back-of-envelope numbers, level expectations (13) | None published; ByteByteGo 1 million newsletter subscribers [M-self] | D |
| **Hugging Face courses** | Goals, concepts, hands-on build, quiz with explanation per option (1b, 5), certificate with a leaderboard bar (GAIA over 30%) as an outside test (7) | Followers and repo stars only | D |
| **fast.ai** | Whole game first, notebooks, 35-question questionnaire per chapter with answers in text (1), spiral revisit (2), 90-min videos (22) | 6 million views [M-self]; no completion or learning data | D |
| **DeepLearning.AI** | 5 to 10 min planned segments with in-video quizzes (22, 1), mastery retries (7), ungraded labs | 13,000 completers of the 2011 class; enrolment and ratings [M-self] | D |

**What the decomposition shows.** The only platforms with independent learning evidence (Khan, ITS such as
Cognitive Tutor and ASSISTments) share four parts: worked or hinted solutions, step-level feedback, a mastery
gate, and spaced return. Their field effects are 0.1 to 0.45 SD and depend on how much the learner actually
does (Khan: 9% reach the working dose; Khanmigo: 17% use when stuck). Everything that makes platforms feel
modern (AI chat, labs, XP, video) has no independent outcome data of its own. So: take the four proven parts
as the backbone, and use ScaleDojo's labs and AI critique as practice ground, not as proof.

---

## 3. Interactions and conflicts, and the rule that settles each

| Conflict | What the evidence says | Resolving rule for Faiz |
|---|---|---|
| Worked examples vs productive failure | Examples win for novices on high-interactivity material; attempt-first wins on conceptual understanding and transfer once tools exist and consolidation follows (rows 3, 10) | **First two problems of a new type: worked example. From the third: he attempts first, then compares with the expert.** A new task class restarts at a worked example. Simple facts (LLM behaviour): predict first, no worked example |
| Worked examples vs expertise | Help reverses as knowledge grows (row 3) | 90-second first-step test at the start of each unit; right twice → skip the example (skill-methods.md D2) |
| Retrieval vs re-teaching ("no repetition") | Re-testing is retrieval; re-reading is not (row 1; postmortem cause 6) | Old material returns only as a question with feedback, never as a re-explanation, unless he misses it twice |
| Retrieval format | MC with explanations showed larger effects, but can plant errors; recall is harder and closer to real use (row 1b) | Short answer first (one line), then the options with per-option explanations |
| Immediate feedback vs delayed benefit | Immediate wins in real classes; the delay benefit comes back through spacing (row 28) | Feedback right after each step; the delayed test is the spaced recheck |
| Self-explanation vs his dislike of long work | Prompts cost time; focused prompts beat open ones (row 8) | One "why" on the key step only, one line. Never a chain (ai-tutoring.md 4e: 44.3% of expert edits cut over-questioning) |
| Interleaving vs learning each type once | Interleaving hurts before the types are known (row 9) | Block the first learning of a type inside a unit; interleave in the daily recall and the weekly mixed review |
| AI feedback vs accuracy | AI feedback helps on average but plain models are often wrong and sycophantic (rows 17, 19) | Claude marks only against a key written before the session (expert solution or run code). ScaleDojo's AI critique is a second opinion: when it disagrees with the expert source, the source wins |
| AI help vs his own thinking | Using AI to explain helps; using it to produce the answer hurts later unaided work (row 17: Bastani, Lehmann, arXiv 2607.08849) | He predicts, specifies or attempts before any AI output; the bottom-out hint ends with his one-line explain-back |
| Gamification vs learning | Points raise activity, not learning; the cognitive effect has no identified element (row 21) | XP and streaks count units done and rechecks passed, never time or points. No leaderboards |
| Simulation vs novice overload | Novices need examples in simulations; reflection helps later (row 16) | Before a lab level: one worked design of the same pattern (ScaleDojo worked-example chapter). After: a four-line after-action review |
| Structure vs his reasoning | Too little structure failed (case-01); too much suppressed his thinking (postmortem causes 3) | Fixed frame per skill; his attempt fills the frame; the expert answer always exists |
| Mastery bar vs time | Higher bars give more learning but cost time (row 7) | 90% on the unit check, but only 2 correct in a row to climb a rung inside the unit. Delayed rechecks catch false mastery |

---

## 4. The recommended combination

### 4a. One unit (25 minutes), same order for every skill

| Min | Step | Components | Source (nothing invented) | Evidence |
|---|---|---|---|---|
| 0 to 3 | **Recall**: 3 spaced items (1, 3, 7, 21 days), short answer first, then options with explanations | 1, 1b, 2, 5, 9 | ScaleDojo quiz bank (1,085 items with explanations); HF quiz items; his own missed items | A |
| 3 to 5 | **First-step test and prediction**: one new problem, he writes only his first step and predicts his unit-check score | 3 (placement), 15, 26 | Problem from the expert source for this unit | B |
| 5 to 13 | **Study or attempt**: worked example with one focused "why" on the key step (new type); or his attempt in the fixed frame (third problem onward) | 3, 8, 10, 14 | ScaleDojo worked-example chapters, Hello Interview free breakdowns, Hamel field guide and Recipe Bot solutions, CS50P and Exercism, SRE book numbers | A / B |
| 13 to 20 | **Completion or faded problem**, step-based feedback from the key; hint ladder one rung at a time | 4, 5, 6 | Claude cuts the rungs from the named expert example; key written and run before the session | A |
| 20 to 23 | **Compare**: his answer next to the expert's, decision by decision; one contrast pair where available | 10, 11, 13 | ScaleDojo weak vs strong signals; Hello Interview Bad/Good/Great; expert labels | B |
| 23 to 25 | **Check**: 3 to 5 new items; his predicted score logged next to the real one | 1, 7, 26 | ScaleDojo quiz items not seen before; Claude-cut variations of the expert example | B |

### 4b. Per skill: what changes inside that unit

| Skill | Entry point and ladder | Practice ground | Checked against | Expected effect, grade |
|---|---|---|---|---|
| **Evaluation and error analysis** | Full ladder, slow: 2 worked examples (Hamel's steps, laid out as in skill-methods.md C1), then he labels traces before seeing expert labels; erroneous example (a judge never compared with human labels) only after 2 correct ones | Hamel/Shreya homework repos (Recipe Bot), HF Cookbook `llm_judge` and `rag_evaluation`, ScaleDojo GenAI mod 8 and 14, lab level 35 | His agreement with expert labels (true positive and true negative rates) as a number | Worked examples 0.48 [A] plus contrast and consolidation 0.36 to 0.50 [B]; no study on evals itself (carried over) |
| **LLM behaviour** | No worked examples. Predict with a reason, Claude runs it, he explains the surprise in one line; the fact goes into spaced recall | HF LLM Course ch. 1 to 2, ScaleDojo GenAI mod 2 to 3 and lab Act 0 to 1, tokenizer and sampling runs | The measured run | Prediction [B], retrieval and spacing [A]: this skill gets the most reliable gain |
| **System design** | 2 worked examples per task class, then design first in the fixed frame; reveal per decision; same brief with one number changed; after-action review | ScaleDojo HLD and GenAI worked-example chapters, then the matching lab level with failure injection; Hello Interview, ByteByteGo | Expert design section by section, the lab's 100-point rubric, the brief's numbers; ScaleDojo AI critique as second opinion | Productive failure 0.36 [B], debrief 0.67 [B], simulation with examples 0.85 [B, researcher tests]; transfer is the least certain of the five |
| **Production maths** | Fastest fading (his strength): one CFA-style worked numeric solution per formula, then "what flips it" variations; interleave cost, latency and error budget | SRE book and workbook numbers, ScaleDojo economics chapters and lab gauges (cost, latency) | Exact number, then the expert's lever | Interleaving 0.42 to 0.83 [B], retrieval [A]; small worked-example need (expertise reversal) |
| **Code** | Read and trace before write: predict output, Parsons or fill 1 to 3 lines, find the bug with hypothesis-test-narrow, small edit, prompt problem (spec that makes an AI produce code passing given tests), review an AI diff against tests | ScaleDojo Forge (84 chapters, 256 quiz items), CS50P problem sets, Exercism with community solutions, his own evaluation scripts | Tests passing, then the expert or community solution | Completion [B], worked examples [A], step feedback from tests [A]; CS1-LLM shows reading and tracing hold up with LLM use [C] |

### 4c. The week (keeps skill-methods.md D1, adds the checks)

| Day | Unit | Added here |
|---|---|---|
| Daily | 3 to 5 min recall (component 1, 2) | Missed items return next day in a different surface |
| Mon | Evaluation | |
| Tue | Code | |
| Wed | System design, with its ScaleDojo lab level | After-action review, four lines |
| Thu | Code plus one LLM-behaviour predict-and-run | |
| Fri | Production, mixed set | |
| Sat | Mixed review: one cold item per skill (9) and the weekly measures in section 5 | Delayed rechecks at 7 and 21 days |
| Every 4 to 6 weeks | Module capstone and one outside transfer task | ScaleDojo lab level not practised, HF certificate, or a fresh trace set |

### 4d. Who supplies what

| Role | Supplier | Not allowed |
|---|---|---|
| Curriculum order | curriculum-design.md and curriculum-map.md (expert curricula, job data) | Claude reordering mid-module |
| Worked examples and expert answers | ScaleDojo worked-example chapters and signals, Hello Interview, ByteByteGo, Hamel and Shreya, HF, CS50P, Exercism, SRE, CFA-style | Claude-written examples with no named source |
| Retrieval items | ScaleDojo quiz bank, HF quizzes, his missed items | New items that test untaught rules |
| Practice under failure | ScaleDojo labs (gauges, Murphy's Lab failure injection) | Labs before one worked design of that pattern |
| Tutor moves (hints, step feedback, fading, comparison) | Claude, against a pre-written key | Free chat; answers before an attempt; Socratic chains |
| Measurement | Tracker: rung per skill, recall results, calibration gap, transfer scores | Satisfaction or messages sent as the measure |

### 4e. Deliberately excluded or kept small

| Excluded | Why |
|---|---|
| Unstructured AI chat as a teacher | Bastani plain GPT-4: 17% worse without AI [M-ind]; Khanmigo field effect near zero when learners do not engage [M-ind] |
| Peer assessment | No peers. Its active part (grading against expert grades) is kept as calibration: he grades, then sees the expert grade |
| Points, leaderboards, game fiction | Cognitive effect not tied to any element; k = 19 [C]. Only a visible count of units and rechecks stays, for rhythm |
| Long video as the method | Replacing teaching with video 0.28; supplement only, 20-minute parts at most, with a check after (Karpathy, DeepLearning.AI) |
| Open case discussion, open research tasks | Case-based learning "inconclusive"; minimal guidance fails novices; case-01 failed in six moves |
| Delayed feedback on steps | Classroom evidence favours immediate; spacing supplies the delay benefit |
| Learning-style matching, highlighting, re-reading | No support (Pashler 2008); low utility (Dunlosky 2013) |
| Goal-setting exercises | No effect in a large higher-education field test; replaced by a recorded progress table (monitoring d = 0.40 [C]) |

---

## 5. How to know it is working

Five measures. Each has a threshold and a fixed response, so the method changes only when a measure says
so (the postmortem's cause 1 was changing the method after complaints).

| Measure | How | Threshold | If it fails |
|---|---|---|---|
| **Delayed retention** | Items from units 7 and 21 days old, cold, short answer, in the Saturday review | 80% or more at 7 days; 70% or more at 21 days | Below for two weeks in a row: shorten the gaps, add a second recall slot; below 60%: the unit's "not yet" loop reopens |
| **Transfer** | One task per level he did not train on: an unpractised ScaleDojo lab level, a fresh trace set from a different product, a new CS50P or Exercism problem, a new cost case | Lab score 70 or more (2 stars); expert-label agreement 80% or more; tests pass on first full attempt | Course checks high but transfer low (gap over 20 points): cut completion rungs, add a novel-variation rung and more contrast pairs before the next level |
| **Calibration gap** | Predicted vs actual score on every unit check | Mean absolute gap 10 points or less after 4 weeks; alarm above 20 | Above 20 for three checks: after each check he sees item-by-item which predictions were wrong; grade one expert-graded sample before the next check |
| **First-step accuracy** | 90-second first-step test at the start of each unit | Rising across a task class; 2 right in a row skips the worked example | Flat across 4 units: the task class is too hard; go back one class |
| **Dose** | Units done and rechecks taken per week | 5 units and 1 Saturday review | Two weeks below 3 units: fix the rhythm first; no method change until dose is met (Khan: gains track dose) |

**The early warning that matters most.** High same-day scores with low 7-day recall or low transfer is the
pattern of the old system (87% first try, later found shallow). If the unit check is above 90% and the 7-day
recheck is below 70%, the unit taught recognition, not learning: the check items were too close to the
examples. Replace them with new-surface items.

---

## Gaps and caveats

- No study tests these components on adult self-learners of AI engineering; every effect is carried over
  from maths, physics, programming, medicine and language learning.
- Most meta-analytic effects are on researcher-made tests; independent-test effects are about half. The
  platform with the best independent data (Khan) shows 0.1 to 0.45 SD, dose-dependent.
- Sailer and Homner, Chernikova and the ICAP review were read from abstracts and full-text extracts; the
  Adesope MC vs short-answer result is from the abstract. The AI-vs-human feedback meta-analysis
  (https://www.tandfonline.com/doi/full/10.1080/01443410.2025.2553639 , 41 studies) refused automated fetch;
  its effect sizes were not checked.
- ScaleDojo, Math Academy, Hello Interview, Hamel's course, fast.ai and Hugging Face have no independent
  outcome data. Their value here is as material and practice ground, judged by his own transfer scores.
- The thresholds in section 5 follow Kulik (90% bar), curriculum-design.md and skill-methods.md; they are
  starting values to tune after four weeks of his data, not tested optima.
