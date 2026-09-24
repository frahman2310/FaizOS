# How an AI tutor should teach: the evidence, applied to Claude teaching Faiz

Checked 2026-09-24. In this system Claude is the tutor, so this file is about the tutor's moves inside a
session: when to tell, when to ask, how to hint, how to give feedback, and what goes wrong when the tutor
is a language model.

Does not repeat: ../teaching-methods.md (self-explanation, contrasting cases, prediction, worked
examples, fading, retrieval, spacing), skill-methods.md (method per skill, worked-example ladder,
placement rule), teaching-structure.md (unit template, practice types). His record is
../../learning-evidence.md; IDs like D1, C19, E12 point there.

Tags: **[M]** measured (a study with numbers). **[S]** stated (an author or company describing its own
design or view, or a finding given without numbers). **[M-self]** a number a company reports about its
own product.

---

## The short version

1. **Good tutoring is worth about 0.3 to 0.8 of a standard deviation, not 2.** The "2 sigma" figure came
   from two small dissertations and was never repeated. Plan for a real but ordinary gain.
2. **The gain comes from small steps with feedback on each step, not from the tutor talking.** Computer
   tutors that give feedback on every step came close to human tutors; tutors who only checked the final
   answer got about a third of the gain.
3. **LLM tutors that helped all did three things**: the expert's worked solution sat inside the tutor, a
   script or platform (not the model) fixed the order of steps, and the answer was held back until the
   student tried. The one that harmed learning was plain ChatGPT that handed out answers.
4. **The learner cannot tell which one he is getting.** Students who learned less from plain GPT-4 did
   not feel they learned less. So progress is judged by cold checks, not by how the session felt.
5. **Two opposite failures.** Over-helping (giving the answer, agreeing with a wrong answer) and
   over-questioning (Socratic questions that go on after he already has it, open tasks with no frame).
   His record shows both: answers given away (C11, C18) and the open investigation (C42, C43).
6. **A system prompt alone does not keep a model's teaching consistent.** The Harvard team and OpenAI
   both say so. Consistency has to live in fixed templates, answer keys and a checker, read every session.

---

## 1. Human tutoring: what the best tutors actually do

### 1a. How big the effect really is
| Finding | Source |
|---|---|
| Bloom 1984: tutored students scored about 2 SD above classroom students, from mastery learning plus one-to-one tutoring | [M] https://en.wikipedia.org/wiki/Bloom's_2_sigma_problem |
| Re-estimate: the 2 SD came from two doctoral dissertations with small samples and was never replicated; among 96 later tutoring RCTs none reached 2 SD | [S, review] von Hippel 2024 https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/ |
| Meta-analysis of 96 tutoring RCTs (PreK to 12): average 0.37 SD, about 14 percentile points | [M] Nickow, Oreopoulos, Quan https://edworkingpapers.com/sites/default/files/ai20-267.pdf ; published version https://journals.sagepub.com/doi/abs/10.3102/00028312231208687 |
| VanLehn 2011, review of studies 1975 to 2010: human tutoring d = 0.79 over no tutoring; step-based computer tutors d = 0.76; substep-based 0.40; answer-based about 0.31 | [M] https://www.tandfonline.com/doi/abs/10.1080/00461520.2011.611369 ; summary https://laurenmarg.com/2015/10/23/article-summary-vanlehn-2011-tutoring-systems/ |

VanLehn's reading: past a certain grain size, more interaction does not add learning (the "interaction
plateau"). What matters is that the student does each step and gets feedback on it [S] same sources.

### 1b. What expert tutors do (Lepper, Chi, Graesser)
| Finding | Source |
|---|---|
| Lepper and Woolverton studied highly effective maths tutors: INSPIRE = Intelligent (deep subject knowledge), Nurturant, Socratic, Progressive (ordered tasks), Indirect (errors handled by questions and hints, rarely "that's wrong, here's why"), Reflective (student explains their reasoning), Encouraging. Half of it is about motivation, not content | [S] https://www.eoas.ubc.ca/research/cwsei/resources/INSPIRE-Guidelines.pdf ; https://www.sciencedirect.com/science/article/abs/pii/B9780120644551500105 ; summary https://pmc.ncbi.nlm.nih.gov/articles/PMC3292071/ |
| Chi et al. 2001: when tutors were stopped from explaining and giving feedback and only prompted, students learned just as much; learning tracked what the student built (deeper scaffolding episodes, more reading), not how much the tutor explained | [M] https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog2504_1 ; summary https://edgeoflearning.com/learning-from-human-tutoring/ |
| Graesser, Person, Magliano 1995, ordinary tutors: tutors ask most of the questions; the Socratic method was absent; tutors find it very hard to identify a student's actual bug; deep reasoning questions correlated with learning, student "do you understand?" checks did not (students say yes when they do not) | [M] https://onlinelibrary.wiley.com/doi/abs/10.1002/acp.2350090604 ; summary http://www.jimdavies.org/summaries/graesser1995.html |
| VanLehn et al. 2007, 7 experiments: tutorial dialogue beat reading a text only when the material was above the student's level (novices on intermediate material, large effects). At the right level, reading did as well | [M] https://pubmed.ncbi.nlm.nih.gov/21635287/ ; PDF https://itgs.ict.usc.edu/papers/06CS_KVL_AG.pdf |
| Lisp Tutor: adding explanations to hints and feedback made learning faster but did not raise post-test scores; once shown the right step, students could build the reason themselves | [M] Anderson, Conrad, Corbett 1989, reported in https://www.cs.cmu.edu/~aleven/Papers/2016/Aleven_etal_IJAIED2016-Helpseeking.pdf |

### 1c. Step-based vs answer-based feedback
Answer-based: the tutor sees only the final answer ("wrong, try again"). Step-based: the tutor sees each
step and responds to the first wrong one. Step-based roughly doubles the effect (0.76 vs about 0.31) [M]
VanLehn above. For a chat tutor this means: ask for the working, not just the answer, and respond to the
first step that went wrong.

### 1d. When a tutor should tell and when to ask
Putting 1b together:
- **Tell** facts, names and rules he cannot work out alone. Asking about them only produces guesses
  (Chi's prompting worked because students had the text; dialogue beats reading only at the right
  level). His record: every question built on a rule never stated failed (E7, B6); cold why-questions
  0 / 4 (A6).
- **Ask** about use, cause and consequence once he has the pieces: what happens next, which line, which
  direction, why this option. This is where his reasoning is.
- **Tell after asking**: once he has tried, give the expert version and compare. Explanation after an
  attempt costs nothing in learning and saves time (Lisp Tutor result).

---

## 2. Intelligent tutoring systems

### 2a. Results at scale
| System | Result | Source |
|---|---|---|
| Cognitive Tutor Algebra I, middle and high schools in 7 states, randomised | No effect in year 1; about 0.20 SD in year 2 in high schools (the authors suggest schools needed a year to learn to use it) | [M] https://www.rand.org/pubs/external_publications/EP50410.html ; https://www.rand.org/pubs/working_papers/WR1050.html |
| ASSISTments homework, 43 Maine schools, 2,850 students | g = 0.18 on the state test; larger for lower performers | [M] https://files.eric.ed.gov/fulltext/EJ1194398.pdf |
| ITS meta-analysis, US K-12, 18 studies | g = 0.27; the provision of worked examples was one of the top moderators | [M] https://arxiv.org/abs/2511.04997 |
| ALEKS | No independent large RCT found in this search; the meta-analysis above is the best available summary | gap |

Takeaway: in real use ITS gains are 0.2 to 0.3 SD, lower than lab results, and the design details
(worked examples, feedback per step) decide which end you get.

### 2b. Knowledge tracing
Bayesian knowledge tracing keeps a running probability that the learner has mastered each skill,
updated after every attempt; the tutor moves on once the probability passes a threshold [S] Corbett and
Anderson 1995 https://link.springer.com/article/10.1007/BF01099821 . Khan Academy found that giving its
LLM tutor the student's recent problem history and missing prerequisites raised next-item correctness by
6.1% across more than a million threads [M-self] https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/ .
For Claude: read the learner record (the "taught, do not re-teach" list and the mistakes queue) before
teaching, every session. A tutor with no memory re-teaches known ideas (C22, C27) and misses the weak ones.

### 2c. Hint design
| Finding | Source |
|---|---|
| Cognitive Tutor hints come in levels: a general principle first, then how it applies to this step, then the **bottom-out hint**, which does everything except type the answer | [S] https://www.cs.cmu.edu/~aleven/Papers/2016/Aleven_etal_IJAIED2016-Helpseeking.pdf |
| Students raced through: 68% of hint levels before the last were viewed for under 1 second. And they avoided help: after 3 errors on a step, the next action was a hint request only 34% of the time | [M] same |
| Help-seeking feedback made students use hints more carefully, even after it stopped, but did not raise learning | [M] same |
| Help helped most at a middle level of skill; for novices on a skill, abstract hint levels help little | [M] Roll et al. 2014, reported in same |
| Breaking a problem into smaller steps worked better than one long hint | [M] Razzaq and Heffernan 2006, reported in same |
| Gaming the system (racing to the answer, trial and error) was the off-task behaviour most strongly linked to lower learning, as strong as prior knowledge | [M] Baker et al. 2004 https://dl.acm.org/doi/10.1145/985692.985741 |
| But bottom-out hints can work as worked examples: time spent on the bottom-out hint predicted learning, consistent with self-explaining it | [M] Shih, Koedinger, Scheines 2008 http://pact.cs.cmu.edu/koedinger/pubs/Shih,%20Koedinger,%20Scheines-08.pdf |
| Recommendation: keep principle-based hints and bottom-out hints; prompt self-explanation after errors and after the bottom-out hint | [S] Aleven et al. 2016, same PDF |

### 2d. The assistance dilemma
Koedinger and Aleven: every tutor must decide how much to give and how much to hold back. Too little help
and the student flounders and learns nothing; too much and they do not do the thinking. No fixed setting
is right: the best level depends on the learner's current skill [S] https://link.springer.com/article/10.1007/s10648-007-9049-0 .
The expertise reversal effect is the same idea from the other side (see ../teaching-methods.md 2a).
In his record: the open investigation was the "too little" end (C42, C43); answers in the chat bar were
the "too much" end (C11, C18).

---

## 3. LLM tutors, 2023 to 2026

### 3a. Controlled studies
| Study | Design | Result | Source |
|---|---|---|---|
| Harvard physics, Kestin, Miller et al. 2025 | RCT, crossover, N = 194; AI tutor at home vs the same lesson as in-class active learning | Median gains more than double; effect 0.73 to 1.3 SD (0.63 by linear regression); median time 49 min vs 60 min in class; more engaged (4.1 vs 3.6 of 5) | [M] https://www.nature.com/articles/s41598-025-97652-6.pdf |
| World Bank Nigeria, De Simone et al. 2025 | RCT, 6-week after-school English programme, GPT-4 (Copilot) with teacher support | 0.31 SD overall, 0.23 SD on English; each extra day attended added learning; girls gained more | [M] https://ideas.repec.org/p/wbk/wbrwps/11125.html ; https://blogs.worldbank.org/en/education/From-chalkboards-to-chatbots-Transforming-learning-in-Nigeria |
| Bastani et al. 2025, Turkey | RCT, about 1,000 high-school maths students, four 90-min sessions: GPT Base (plain ChatGPT-4), GPT Tutor (teacher solutions + hint-only prompt), control | Practice: +48% Base, +127% Tutor. Exam without AI: Base 17% worse than control; Tutor about equal to control. Base students mostly asked for the answer; plain GPT-4 was right only 51% of the time (logic errors 42%); Base students did not think they had learned less | [M] https://pmc.ncbi.nlm.nih.gov/articles/PMC12232635/ ; https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education/ |
| Lehmann, Cornelius, Sting 2024, coding classes | Observational data plus experiments | Using an LLM for explanations helped; using it to get solutions hurt; copy-paste encouraged solution-seeking; self-rated benefit exceeded actual benefit; complete beginners gained most | [M] https://arxiv.org/abs/2409.09047 |
| LearnLM with Eedi, UK 2025 | RCT, N = 165, five schools; LearnLM drafted each message, an expert tutor approved or edited it | 76.4% of drafts sent with zero or one-to-two character edits; transfer to a new topic 66.2% vs 60.7% with human-only tutors (+5.5 points); 5 factual errors in 3,617 drafts (0.1%). Edits: 44.3% to fix pacing (Socratic questioning that went on after the student had it), 33.6% clarity, 19.5% tone | [M] https://arxiv.org/abs/2512.23633 |
| Tutor CoPilot, Wang et al. 2024 | RCT, 900 human tutors, 1,800 students; an LLM suggested moves to the human tutor | +4 points topic mastery, +9 for the weakest tutors; tutors asked more guiding questions and gave away fewer answers | [M] https://arxiv.org/abs/2410.03017 |
| ChatGPT hints vs human hints, Pardos and Bhandari 2023 | N = 77, algebra | 70% of ChatGPT hints passed quality checks; human-written hints gave significant gains, ChatGPT hints did not | [M] https://arxiv.org/abs/2302.06871 |

### 3b. Product tutors
| Product | What it does | Evidence | Source |
|---|---|---|---|
| Khanmigo | Socratic tutor inside Khan Academy | No independent learning RCT found; a J-PAL trial is registered; a 69-student physics study found no difference vs Google search; Khan's own A/B tests: learner history +6.1% next-item correctness, shorter replies cut 3 s latency with no accuracy loss, adding worked problem-type examples had no effect | [S] https://www.povertyactionlab.org/initiative-project/ai-powered-tutoring-unleashing-full-potential-personalized-learning-khanmigo ; [M] https://jtl.uwindsor.ca/index.php/jtl/article/view/10052 ; [M-self] https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/ |
| Google LearnLM | Trained (not just prompted) on "pedagogical instruction following". Principles: active learning, manage cognitive load, adapt to the learner, stimulate curiosity, deepen metacognition, do not reveal the answer | Experts preferred it by +31% over GPT-4o, +11% over Claude 3.5 Sonnet, +13% over Gemini 1.5 Pro [M-self]; replies 298 vs 423 tokens; rated better at finding mistakes but worse at noticing successes, which the authors link to training against sycophancy [M-self] | https://arxiv.org/abs/2412.16429 ; https://arxiv.org/abs/2407.12687 |
| Claude learning mode (Anthropic, April 2025) | Socratic questions ("How would you approach this problem?"), focus on principles, templates for study work | No outcome data published [S]. Anthropic's own data: about 47% of student conversations were "direct", asking for answers with little engagement [M-self] | https://www.anthropic.com/news/introducing-claude-for-education ; https://www.anthropic.com/news/anthropic-education-report-how-university-students-use-claude |
| ChatGPT study mode (OpenAI, July 2025) | Socratic questions, scaffolded replies, knowledge checks; built from system instructions, not training | OpenAI: the approach "results in some inconsistent behavior and mistakes across conversations" [S]; no outcome data | https://openai.com/index/chatgpt-study-mode/ ; https://www.infoq.com/news/2025/08/study-mode-chatgpt |

### 3c. What separated the tutors that helped from those that harmed
| Design choice | Helped | Harmed or no effect |
|---|---|---|
| Where the right answer comes from | Expert step-by-step solutions written into the prompt (Harvard, Bastani GPT Tutor); expert approves each message (Eedi) | The model solves it itself: 42% logic errors (Bastani Base); ChatGPT hints ungraded (Pardos) |
| Who controls the order of steps | The platform walks the student through parts in a fixed order. Harvard: "a system prompt could not reliably provide enough structure to scaffold problems with multiple parts" | Free chat |
| When the answer appears | Held back; hints first (GPT Tutor, Harvard "DO NOT give away the full solution") | On request at once (GPT Base; students asked for answers most of the time) |
| Reply length | Brief (Harvard "Keep responses BRIEF"; LearnLM 298 vs 423 tokens; Khan shorter replies) | Long replies (learners in LearnLM workshops called them overload) |
| What the student does | Explains, attempts, asks for explanation (Lehmann) | Copies a solution (Lehmann, Bastani) |
| Pacing | Move on once the student has it (Eedi tutors' top edit) | Questioning that continues after success (44.3% of Eedi edits) |
| Memory of the learner | History and prerequisites given to the tutor (Khan +6.1%) | Each session starts blank (Eedi tutors noted LearnLM could not recall past sessions) |
| Human in the loop | Teacher support (Nigeria), expert approval (Eedi), tutor copilot | Unsupervised general chatbot |

Sources: rows above, plus Kestin quotes from the PDF at https://www.nature.com/articles/s41598-025-97652-6.pdf

---

## 4. Principles for Claude tutoring Faiz one-to-one

Each rule names the evidence and the line in his record it fits. Where faiz-teach already has the
rule, this section gives it its research backing rather than a new rule.

### 4a. Worked examples
1. **Written before the session, not improvised.** Every worked example and every answer key is
   prepared and checked (numbers computed by running code) before the part is sent. Harvard and Bastani
   GPT Tutor put the expert solution in the tutor; plain GPT-4 was wrong half the time [M].
2. **The example must share the exact shape of what he will be asked.** His record: same-shape example
   9 / 9, mismatched example copied wrongly (B13, E8). Surface can differ; steps must match.
3. **Tiny and generic first, then the real case** (B1: 78 to 80% with it, 27% without).
4. **One line of "why" per step**, so the reason is there to compare against (Aleven: principle plus how it
   applies to this step [S]).

### 4b. When to withhold the answer
1. **Withhold by default on questions he can reach with what was taught.** Answers on demand made
   students worse off without AI (Bastani Base −17% [M]); solution-seeking hurt, explanation-seeking
   helped (Lehmann [M]). Matches C11 and C18.
2. **Give it on request, or after the second failed hint** (C19, C23, C28). This is the bottom-out hint
   and it is legitimate: ITS research says tutors need it to end floundering, and time spent on it
   predicts learning when the student processes it [M] Shih 2008; [S] Aleven 2016.
3. **After a given answer, one line from him in his own words** ("why is it 480 and not 120?"), then the
   same idea returns reworded in a later part. Given answers were retained only 1 / 3 (D7); self-explaining
   the bottom-out hint is what separates learning from copying (Shih [M]).
4. **Never withhold a fact or rule.** Withholding is for applications of taught rules. A question built
   on an untaught rule is not productive struggle; it is a guess (E7; Chi and VanLehn 2007 in 1b).

### 4c. Prompting self-explanation
1. **Ask for the reason on the key step only, and aim it at a target**: "which line lets this happen, and
   why", not "explain this" (see ../teaching-methods.md 1a).
2. **Ask for his working, not just the answer**, so feedback can hit the first wrong step (step-based
   0.76 vs answer-based about 0.31 [M] VanLehn).
3. **Do not ask "does that make sense?"** Students say yes when they do not (Graesser [M]). A one-line
   check question does the job.

### 4d. When he says "I don't understand"
In order. Evidence from his record first, research second.
| Step | Move | His record | Research |
|---|---|---|---|
| 0 | If he says it about the whole part: stop, rebuild the part from the template with fewer new things; do not answer its questions first | D8 2 / 2 | Dialogue helps only when material is above level; bring it to level (VanLehn 2007 [M]) |
| 1 | Point at his own earlier answer or numbers | D1 15 / 17 | Tutors fail at diagnosing bugs; his own prior step is a diagnosis for free (Graesser [M]) |
| 2 | Shrink to two options (higher or lower, toward or away) | D4 5 / 7; E12 3 / 3 once reworded | Smaller steps beat one long hint (Razzaq and Heffernan [M]) |
| 3 | One new everyday picture, with where it breaks | D2 8 / 10 | Analogies with the mapping made explicit (../teaching-methods.md 2e) |
| 4 | Bottom-out: the answer with the reason per line, then his one-line explain-back | D7 ends the stall 6 / 6 | Shih 2008 [M] |
| Never | More prose, re-reading the rule, "scroll up" | D6 0 / 5 | Long hints lose to steps [M] |

### 4e. Keeping his reasoning central without leaving him lost
1. **His attempt comes before the expert version, inside a fixed frame.** Try first, then compare
   section by section (skill-methods.md C3). The frame and the expert answer are what stop an attempt
   from turning into the lost feeling of case-01 (C42, C43; Koedinger and Aleven's "too little" end [S]).
2. **Ask about decisions and consequences, tell the facts** (1d). Chi 2001: students learn as much when
   the tutor mostly prompts, provided they have the material [M].
3. **Stop when he has it.** The most common expert fix to LearnLM was cutting Socratic questioning short
   once the student was right (44.3% of edits) [M]. Matches "ik this dont repeat" (C22) and "give me the
   answer for 4 and move on" (C28). One follow-up "why" is enough; not a chain.
4. **Say "wrong" plainly and give one reframe** (C12). Lepper's expert tutors were indirect about errors,
   but they were working with children and motivation; he has asked for plain wording, and his own rule
   wins. Indirect here means a hint that points, not a hint that hides.

### 4f. Feedback timing and form
1. **Right after each part's answers**, per question. Delayed feedback lowered effects in computer-based
   learning [M] Van der Kleij 2015 https://journals.sagepub.com/doi/abs/10.3102/0034654314564881 ;
   immediate feedback is more efficient for procedural skills, delayed may help transfer in concept
   learning [S] Shute 2008 https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf .
   The delay he gets for transfer comes from spacing (the recall queue), not from holding feedback back.
2. **Explain, do not just mark.** Elaborated feedback g = 0.49, right/wrong only 0.05, correct answer only
   0.32 [M] Van der Kleij 2015.
3. **About the task, not about him.** Feedback helped on average (d = 0.41) but over a third of feedback
   interventions made performance worse [M] Kluger and DeNisi 1996 https://www.mrbartonmaths.com/resourcesnew/8.%20Research/Marking%20and%20Feedback/The%20effects%20of%20feedback%20interventions.pdf .
   No "great job", no "you should know this".
4. **Check the answer against the key before replying**, step by step. LLM tutors that first locate the
   error in the student's steps give correct feedback more often with fewer hallucinations [M] Daheim et
   al. 2024 https://arxiv.org/abs/2407.09136 .

### 4g. Consistency: stopping the tutor inventing formats
The evidence that prompts alone fail:
- Harvard: the system prompt could not reliably keep multi-part problems in order, so the platform
  enforced the sequence [S] Kestin PDF above.
- OpenAI: system-instruction tutoring gives "inconsistent behavior and mistakes across conversations" [S].
- LearnLM authors: models tend to change their solution to the same problem several times in one
  conversation [S] https://arxiv.org/abs/2407.12687 .
- His record: 80% with the template and 27% without it, same day, same lesson (A12, A13); "The method is
  inconsistent, you keep deviating" (C28); 114 old `insights` rows still active and contradicting the
  skill (section C, item 7).

Guards:
1. **One source of teaching rules**: the faiz-teach skill. Nothing else (memory, database insights, old
   docs) may carry teaching instructions; retire contradicting rows.
2. **Fixed templates per skill, from skill-methods.md**, read at session start. A new format only by a
   logged decision, never mid-lesson.
3. **A checker script, not the model's judgment**, verifies each part against the template before it is
   sent (the Harvard lesson: structure in the platform, not the prompt).
4. **Answer keys and worked examples written and verified before the session**, so the tutor cannot drift
   to a different solution halfway.
5. **Read the learner record first** (taught list, mistakes queue, last session's stuck points): Khan's
   +6.1% from history [M-self]; Eedi tutors' complaint that the model had no memory of past sessions [S].

---

## 5. Failure modes of AI tutors and the guard for each

| Failure | Evidence | Guard in this system |
|---|---|---|
| **Over-helping**: answer given too soon | Plain ChatGPT as tutor revealed the solution 66% of the time and gave wrong feedback 59% of the time (MathDial) [M] https://arxiv.org/abs/2412.09416 ; GPT-4 still revealed it about 47% of the time in MRBench [M] same; Bastani Base −17% [M] | Answer only on request or after 2 failed hints; no hints that imply the answer (C11, C18); explain-back after any given answer |
| **Hallucinated content**: wrong facts, wrong numbers | Plain GPT-4: 42% logic errors, 8% arithmetic on high-school maths [M] Bastani; even supervised LearnLM: 0.1% [M] Eedi | Expert keys prepared before the session; every number produced by running code; claims about tools and APIs checked against docs, not memory |
| **Sycophancy**: agreeing with a wrong answer or caving when pushed | Five assistants tailored answers to the user's stated view and wrongly admitted mistakes when challenged; preference training rewards it [M] Sharma et al. https://arxiv.org/abs/2310.13548 ; sycophantic behaviour in 58% of tested cases across GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro [M] SycEval https://ojs.aaai.org/index.php/AIES/article/view/36598 | Mark against the written key, not against how confident he sounds; if he pushes back, recheck the key by running it, then hold or correct with the reason; never confirm half an answer (B12) |
| **Over-questioning**: Socratic chains after he has it | 44.3% of Eedi expert edits fixed pacing [M]; his C22, C28 | One follow-up "why" at most; move on when right |
| **Too little structure**: open tasks, no expert answer | Productive failure fails without comparison to the canonical answer [S] Loibl and Rummel (skill-methods.md); his case-01 (C41 to C43) | Fixed frame, expert answer always exists, compared after his attempt |
| **Inconsistent pedagogy** | Harvard, OpenAI, LearnLM statements above [S]; A12 vs A13 in his record [M] | Section 4g |
| **Illusion of learning** | Bastani Base students did not think they learned less [M]; Lehmann: perceived benefit exceeded real benefit [M] | Progress judged by cold first-try scores and delayed recall, logged in the session ledger, not by how a session felt |
| **Jargon and long replies** | LearnLM learners called long replies overload; Harvard "Keep responses BRIEF" [S]; his C1, C21, C33 | Glossary check on undefined terms; one part per message; code in chat, not files |
| **No memory of the learner** | Khan +6.1% with history [M-self] | Read the evidence file and taught list before teaching |
| **Help abuse on his side** | Racing to the bottom-out hint predicted lower learning [M] Baker 2004; Aleven 68% of hint levels read under 1 s [M] | Rungs served one at a time; the bottom-out rung always ends with his explain-back |

---

## Gaps
- Nature, PNAS, Wiley and Springer full texts refused automated fetch in places; Chi 2001, Graesser 1995
  and Lepper findings come from abstracts and faithful summaries, not the full papers.
- The INSPIRE PDF host did not resolve on 2026-09-24; the INSPIRE list is confirmed by the CBE Life
  Sciences summary and the search result text, not read directly.
- Kestin's effect size range (0.73 to 1.3) depends on how the ceiling effect is handled; the regression
  estimate is 0.63.
- No independent RCT of Khanmigo, Claude learning mode or ChatGPT study mode on learning outcomes was
  found. Their design claims are stated, not measured.
- No LLM tutoring study found for adult self-learners in AI engineering; all RCTs are school or
  undergraduate maths, physics, English or coding. The principles in section 4 are carried over.
- ALEKS: no independent large RCT found in this search.
