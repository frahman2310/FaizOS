# Teaching craft: how the best teachers actually explain and set practice

Checked 2026-09-24. This file is about craft: the concrete moves inside one explanation, one worked example
or one practice item. It copies techniques, not platforms.

Does not repeat: ../teaching-methods.md (self-explanation, contrasting cases, prediction, analogies,
signalling, refutation text), skill-methods.md (method per skill, worked-example ladder, fading),
teaching-structure.md (unit shapes and templates), ai-tutoring.md (tutor moves, hints, withholding).
Where a finding is already there, this file points to it and adds only the craft.

Tags: **[M]** measured (a study with numbers). **[S]** stated (the teacher or company describing their own
method, or a finding given without numbers). **[M-self]** a number a company reports about itself.
Skill codes: **E** evaluation and error analysis, **L** how LLMs behave, **D** system design,
**P** production maths, **C** code.

---

## Part 1. The resources, one craft at a time

### 1. Khan Academy (Sal Khan's videos, hints, Khanmigo)
| Technique | Real example | Why it works | Transfer to Faiz |
|---|---|---|---|
| **Talk like a person working it out beside you.** Unscripted voice, hand-drawn steps appear as he says them, no face, no slides. Khan's own tips: be conversational, draw by hand, "not too fancy", prepare then speak freely, 10 minutes maximum [S] https://www.fastcompany.com/3007137/4-tips-creating-sal-khan-style-instruction-videofrom-sal-khan | His cousins preferred the recorded Sal: they could pause and replay him without feeling they were wasting his time or being asked "do you understand this?" [S] https://www.khanacademy.org/talks-and-interviews/conversations-with-sal/v/salman-khan-talk-at-ted-2011-from-ted-com | 6.9 million edX sessions: Khan-style tablet drawing held attention better than slides or code screencasts; shorter videos far better [M, engagement only] https://dl.acm.org/doi/10.1145/2556325.2566239 . Conversational wording ("you", "your") beat formal wording: retention d = 0.30, transfer d = 0.54 (meta-analysis) [M] https://link.springer.com/article/10.1007/s10648-013-9228-0 | Write to him in second person ("your bot", "your bill"). Build the diagram or table in the order the reasoning happens, row by row, not all at once |
| **One hint per step, last hint is the whole solution.** Each step of a multi-step item has its own hint; seeing all hints gives a full worked example; learner should self-explain each hint [S] https://blog.khanacademy.org/how-should-people-practice-on-khan-academy/ | Median problem: hint 1 is "put the numbers in order", hint 2 finds the middle. The blog models the self-explanation: we order them so the middle one really is the middle | Bottom-out hints act as worked examples when the learner processes them [M] Shih 2008, see ai-tutoring.md 2c | Every practice item is written with its step list first; hints are those steps, served one at a time (already the faiz-hint rungs) |
| **The tutor diagnoses before it helps, and checks every claim with a tool.** Khanmigo Lite's published prompt: find which part the student is stuck on first; never solve the actual problem, use a similar example; after 3 or more help requests with no effort, stop hinting and zoom out; "use SymPy to evaluate every one of the students claims" [S] https://baoyu.io/blog/prompt-engineering/tutor-me-prompt (third-party copy of the GPT's instructions) | On a wrong step: do not give the answer, ask how he got that step | Khan's A/B tests: learner history +6.1% next-item correctness; shorter replies cut 3 s with no accuracy loss; adding problem-type examples did nothing [M-self] https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/ | Claude checks his numbers by running Python, never by eye. "Where are you stuck: the formula, the numbers, or what the number means?" before any hint |

### 2. 3Blue1Brown (Grant Sanderson)
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **Concrete before abstract.** "Resist the temptation to start with the general abstract thing" and fill it with examples later [S] https://confengine.com/conferences/odsc-india-2019/proposal/10273/concrete-before-abstract | Essence of Calculus starts from one circle's area, sliced into rings, before any derivative is named [S] https://www.3blue1brown.com/lessons/essence-of-calculus/ | Concreteness fading: start concrete, fade to the abstract form in steps (systematic review) [S, review] https://eric.ed.gov/?id=EJ1036777 | Every mechanism starts from one real prompt with real numbers; the general rule is the last line, not the first |
| **"You could have invented this."** The stated goal of the calculus series is that you feel you could have discovered it; the lesson follows the path a curious person would take [S] same lesson page | Area of a circle: thin rings, unroll each ring to a strip, the strips stack into a triangle, area = pi r^2 falls out | Inventing first prepares people to learn the formula later [M] Schwartz and Martin 2004 (skill-methods.md A2) | Hybrid search: "pure meaning search misses order ID 4471-B. What would you add?" He proposes keyword matching before it is named BM25 |
| **Why you should care in 30 seconds; one real distribution on screen.** His contest rules: the reason to care must be clear "within the first 30 seconds" [S] https://www.3blue1brown.com/blog/some1 . In the GPT video, temperature is shown on GPT-3's real top-20 next-word probabilities, reshaped live as the knob moves [S] https://medium.com/lazy-by-design/but-what-is-a-gpt-visual-intro-to-transformers-3blue1brown-d078447b8ef4 (summary of the video) | Temperature is not defined; it is shown changing a real list of words | Seductive, irrelevant openings hurt transfer (below, Rey 2012); a relevant hook does not | First line of every part names the decision or the failure, in one sentence |

### 3. Math Academy (Justin Skycak)
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **Knowledge points: tiny steps, each a worked example then 2 to 5 questions of the same shape.** Lessons are an introduction plus 3 to 4 KPs of rising difficulty; content "about 10x more finely scaffolded" than a textbook (about 1,000 steps for calculus vs 100) [S] The Math Academy Way pp. 165, 217 https://www.justinmath.com/files/the-math-academy-way.pdf | "Exponents with rational bases": KP1 writes 4 x 4 x 4 as 4^3; later KPs raise generality | Worked examples for novices [M] van Gog 2011 (skill-methods.md) | A token-cost lesson: KP1 one call; KP2 calls per day; KP3 with caching. Each KP has its own example and questions |
| **Minimum effective dose of explanation, then problems within minutes.** Start with the simplest case, ramp in difficulty and generality; every problem gets feedback [S] https://www.justinmath.com/cognitive-science-of-learning-minimizing-cognitive-load/ | About 3 worked examples per lesson, each followed by about 3 questions, so doing outweighs reading [S] Math Academy Way p. 183 | Doing gave 6x the learning of reading [M] Koedinger 2015 (teaching-structure.md) | Explanation stops the moment he has enough to try question 1 |
| **Hide which example to copy; keep confusable ideas apart.** Reviews are mixed so the matching example is not obvious; "non-interference": related, confusable topics are spaced apart when first taught [S] Math Academy Way pp. 223, 247 | Precision and recall are not introduced in the same session | Interleaving at review time d = 0.79 to 0.83 [M] (skill-methods.md) | Teach precision one day and recall days later; mix them only in review |

### 4. Brilliant
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **Problem first, simplest version first.** A pretest before the procedure; build intuition with visuals, manipulation and concrete computation, starting from the simplest version of the idea; one concept per lesson [S] https://brilliant.org/about/ | Stated design; lessons open on a puzzle, not a definition | Try-first plus explanation after beats explanation alone for transfer [M] Kapur 2014 (skill-methods.md) | Open with a pick: "Which of these two retrieval results would a user click?" |
| **Consequence as feedback.** Inspired by Super Mario: "You fall into the pit and die", not a text box explaining the jump [S] https://blog.brilliant.org/hand-crafted-machine-made/ | The learner sees what their choice does | Feedback that shows the result is elaborated feedback (g = 0.49 vs 0.05 for right/wrong only) [M] Van der Kleij 2015 (ai-tutoring.md) | Wrong cache TTL answer shows the bill and hit rate it produces, then the reason |
| **Many problems per concept, with edge cases.** 50+ concepts per intro course, 20+ problems per concept ramping into edge cases [M-self] same blog | Volume of varied items per idea | Varied surfaces expose deep structure [S] Atkinson 2000 (skill-methods.md) | Each concept gets a bank of variants (numbers, domain) so review is never the same item |

### 5. CS50 (David Malan)
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **One physical demonstration that carries a number.** Aims for at least one memorable demo per class: lockers, doors, students on stage [S] https://www.developing.dev/p/harvard-professor-cs50-what-matters | Phone book: page by page, two pages at a time, then tear in half and throw half away; 1,024 pages take 10 halvings; doubling the book adds one step; chart of n, n/2, log n [S] https://cs50.harvard.edu/x/2020/notes/0/ | Three algorithms on the same object is a contrasting case (teaching-methods.md 1c) | Retrieval over 1 million chunks: scan all vs index; show steps for 1k, 1M, 1B side by side |
| **Two versions of the same problem.** "Less comfortable" Mario or Cash vs "more comfortable" Mario or Credit; the learner chooses; the higher score counts [S] https://cs50.harvard.edu/x/2024/psets/1/ | Same concept, two depths, no penalty for trying the harder one | Right difficulty is the core of deliberate practice [S] (skill-methods.md A2) | Every lab brief has a base target and a stretch target (e.g., stretch: half the budget) |
| **Specs with expected input and output.** Covered in skill-methods.md B (Cash pseudocode, check50) | | | |

### 6. Andrej Karpathy
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **Open with a list of puzzles one mechanism explains.** The tokenizer lecture opens on strange behaviours: cannot spell, cannot reverse a string, bad at arithmetic, halts on `<|endoftext|>`; the answer to each is "tokenization" [S] https://simonwillison.net/2024/Feb/20/lets-build-the-gpt-tokenizer/ | Five puzzles, one cause, then build the cause | Curiosity from a gap he already feels; each puzzle is a later check item | LLM-behaviour units open with 3 real failures he may have seen (counts letters wrong, Urdu costs more, changes answer on rerun) |
| **Build the smallest real thing, and keep the bug in.** micrograd grows from one expression; a bug appears when a value is used twice (`b = a + a` gives the wrong gradient), then is fixed with `+=` on camera [S] https://github.com/karpathy/micrograd ; lecture https://karpathy.ai/zero-to-hero.html | The learner sees the error, its symptom and its fix | Erroneous examples help once there is some prior knowledge (large effect) [M] Große and Renkl 2007 (skill-methods.md) | Worked code examples include one real, labelled mistake and the check that caught it |
| **Numeric sanity checks with expected values.** "A Recipe for Training Neural Networks": check loss at start equals -log(1/n_classes); overfit one batch of 2 to 3 examples to zero; "become one with the data"; lists bugs he hit (corrupted labels, duplicates) [S] https://karpathy.github.io/2019/04/25/recipe/ | A number you can predict before running | Prediction then reveal (teaching-methods.md 1d) | Eval checks with expected values: a judge that says "pass" to everything scores TNR = 0; a random judge on a 50/50 set scores about 50% |

### 7. Visual and interactive explainers (Alammar, Distill, Ciechanowski, Case, Victor)
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **Black box first, then pop it open one layer at a time, with fixed sizes.** The Illustrated Transformer: translator as one box, then encoder and decoder stacks, then self-attention; sizes stay the same all the way (512-wide vectors, 64-wide queries, 8 heads); one sentence carries attention: "The animal didn't cross the street because it was too tired" [S] https://jalammar.github.io/illustrated-transformer/ | Every new layer is placed inside the picture already seen | Signalling and segmenting (teaching-methods.md 2c, 2d) | RAG explained as one box (question in, answer out), then retriever and generator, then chunker and reranker; same example question throughout |
| **Problem, then the part that fixes it ("but ... therefore").** Mechanical Watch: a wound spring spins the hand too fast and runs out; therefore gears; but speed is still untamed; therefore escapement; but it needs a push; therefore the balance wheel. Sliders let you wind and adjust [S] https://ciechanow.ski/mechanical-watch/ . Nicky Case names the "therefore and but" structure and "show, then tell" (pictures, examples, analogy) [S] https://ncase.me/StanfordTalk/transcript.html | Each component arrives as the answer to a failure just shown | Telling works better after learners have met the problem [M] Schwartz and Bransford 1998 http://aaalab.stanford.edu/assets/papers/earlier/A_time_for_telling.pdf | System design parts: naive pipeline, show the failure with numbers, add one component, show the new numbers. Never a finished diagram first |
| **Up and down the ladder of abstraction.** Bret Victor: run one car on one road (concrete); show its whole trajectory; step back down; then show all versions of the rule at once and all road bends at once; insight comes "in the transitions between them" [S] https://worrydream.com/LadderOfAbstraction/ | One run, then a sweep over one knob, then back to one run | Interactive articles: promising, but "limited empirical evaluation" and many readers never touch the controls [S] https://distill.pub/2020/communicating-with-interactive-articles/ | One prompt at T = 0.7 (one run), then a table over T = 0 to 2 (the sweep), then back to the single case that matters. A table does the sweep; no widget needed |

Distill's "Research Debt" frames all of this: good explanation "often involves transforming the idea",
not polishing it [S] https://distill.pub/2017/research-debt/

### 8. Julia Evans (wizard zines)
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **Start concrete, prove every claim, say why before what.** Her 13 patterns in confusing explanations include: starting abstract, jargon that means nothing ("Git is cryptographically secure"), unsupported statements, too many concepts at once, "what" without "why", unrealistic examples, strained analogies [S] https://jvns.ca/blog/confusing-explanations/ | Fix for unsupported claims: "prove that your statements are true" with a runnable example | Curse of knowledge (teaching-methods.md 2f); seductive details cut transfer [M] Rey 2012 below | Every claim in a part is either run in front of him or cited. "Hybrid search is better" never appears without the recall numbers |
| **Label the wrong way before showing it.** Frame mistakes as an experiment ("what if we try X?"), a stated misconception, or a personal error story [S] same post | Readers are not left copying the broken version | Refutation text (teaching-methods.md 2g) | Bad designs are headed "Bad, and why" (matches the Hello Interview Bad/Good/Great in skill-methods.md) |
| **Keep analogies to one or two sentences.** Implicit ones ("events flow from producer to consumer") beat a long Mississippi River comparison [S] same post | | Seductive details [M] | An analogy is one line plus where it breaks (his D2 rule, ai-tutoring.md 4d) |

### 9. Feynman and Barbara Oakley
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **Explain it back in plain words, find the gap, go back.** The "Feynman technique" is a 2011 packaging by Scott Young, not Feynman's own method [S] https://www.scotthyoung.com/blog/the-feynman-technique-explained/ . Feynman did keep a "notebook of things I don't know about" [S] same | One-line explain-back after a given answer | Self-explanation (teaching-methods.md 1a); given answers retained 1/3 without explain-back (his D7) | Already his explain-back rule. Add: a gap he names goes to the recall queue |
| **Brilliant lectures without feedback fail most students.** Feynman's own preface: "I don't think I did very well by the students"; there was no feedback from students to lecturer [S] https://www.feynmanlectures.caltech.edu/III_91.html | The most admired physics lectures, judged by their author on exam results | Step feedback roughly doubles tutoring effect [M] VanLehn 2011 (ai-tutoring.md) | Beauty of explanation is never the test. The test is his first-try score on the next item |
| **Look away and recall; beware illusions of competence.** Rereading and highlighting feel like learning because the answer is on the page; look away and recall instead. Learning How to Learn: over 4 million learners [M-self] https://www.classcentral.com/course/coursera-learning-how-to-learn-2161 ; technique [S] https://singjupost.com/transcript-barbara-oakley-on-learning-how-to-learn-at-tedxoaklanduniversity/ | Recall the key idea before the next section | Retrieval 80% vs 36% [M] (skill-methods.md) | Before part 2 starts: "Without scrolling: what did the temperature do to the gap between scores?" |

### 10. Hamel Husain and Chip Huyen (practitioner writing)
| Technique | Real example | Why it works | Transfer |
|---|---|---|---|
| **One real product, real traces, real tools on screen.** Hamel's evals post runs on Rechat's "Lucy" assistant: whack-a-mole failures, unit-test assertions (regex for exposed UUIDs; exactly one listing returned), screenshots of the trace viewer and the before/after error dashboard; "Keep it simple" [S] https://hamel.dev/blog/posts/evals/ | NurtureBoss date handling 33% to 95% (skill-methods.md C1) | Realistic examples (Julia pattern 5); worked examples drawn from the real domain [S] | Every E item is built from traces of one running product, with its real messiness (typos, half answers) |
| **Every decision priced.** Chip Huyen: GPT-4 at $0.624 per prediction vs GPT-3.5 at $0.004; at DoorDash's 10 billion predictions a day the cheap model still costs $40 million a day; 1 output token 0.58 s vs 26 tokens 1.43 s (p50), so chain-of-thought costs latency [S, her measurements] https://huyenchip.com/2023/04/11/llm-engineering.html | The scale multiplication makes the decision obvious | Numbers in the brief (teaching-structure.md A8) | P items always end at scale: per call, per day, per month, and the one number that flips the choice |

### 11. Others that transfer
| Resource | Technique | Example | Transfer |
|---|---|---|---|
| **Nand2Tetris** | The answer key ships with the task: every chip comes with a test script (.tst) and a compare file (.cmp) of correct outputs [S] https://www.nand2tetris.org/project01 | Build a gate, run the given test, see which row differs | Every C and E item ships with its expected output; he sees exactly which row he got wrong |
| **Exercism mentoring** | 1 to 3 ideas per round, biggest first; answer what the student asked for; only concepts they have met; do not hand over a solution [S] https://exercism.org/docs/mentoring/how-to-give-great-feedback | Mentor reads the student's question before the code | Feedback on his design: at most 3 points, biggest first |
| **Project Euler, LeetCode** | Solve first, then the forum of other approaches unlocks (skill-methods.md B) | | Expert design unlocks after his attempt |

---

## Part A. Catalogue of craft techniques

| # | Technique | What it is | From | Example | Evidence | Skills |
|---|---|---|---|---|---|---|
| T1 | Decision hook | First line names the decision or failure and the stake in money or users | 3B1B 30-second rule, ScaleDojo | "Your bot gives 3 refund amounts for one ticket" | [S]; seductive openings hurt [M] | all |
| T2 | Puzzle list | 3 to 5 odd behaviours, one mechanism explains all | Karpathy tokenizer | Spelling, arithmetic, Urdu cost: tokens | [S] | L |
| T3 | Predict first | A pick with a number before any explanation | Brilliant pretest, Karpathy loss-at-init | "At T = 1, how many of 1,000 answers are wrong?" | [M] Kapur; teaching-methods.md 1d | L, P |
| T4 | Concrete, then the rule | Real case with numbers first; the general rule last | 3B1B, Julia, Case | Four word scores before "softmax" is named | [S, review] Fyfe 2014 | all |
| T5 | Could have invented it | Pose the gap so he proposes the fix before it is named | 3B1B | He proposes keyword search before "BM25" | [M] Schwartz and Martin 2004 | D, L |
| T6 | Problem, then component | Each part arrives as the fix to a failure just shown | Ciechanowski, Case | Naive RAG misses order IDs, therefore hybrid | [M] Schwartz and Bransford 1998 | D |
| T7 | Black box, then open | Whole system as one box, then one layer at a time | Alammar | RAG box, then retriever and generator | [S] | D, L |
| T8 | Fixed sizes and one running example | Same numbers and same example across every layer | Alammar (512, 64, 8) | Same question and same 1,000 calls/day throughout | [S] | all |
| T9 | Sweep one knob | One run, then a table across a knob, then back to one run | Victor | T = 0, 0.5, 1, 2 in one table | [S]; interactivity evidence thin [S] | L, P |
| T10 | Three ways on one object | Compare naive, better, best on the same data | Malan phone book | Scan vs index for 1k, 1M, 1B chunks | [M] contrasting cases | D, P |
| T11 | Knowledge points | Split a lesson into 3 to 4 tiny steps, each example plus 2 to 5 questions | Math Academy | Cost per call, per day, with cache | [S]; [M] worked examples | P, C |
| T12 | Minimum effective dose | Stop explaining as soon as question 1 is answerable | Math Academy | Under 150 words before his first answer | [M] Koedinger 6x | all |
| T13 | Step hints, bottom-out last | Hints are the example's steps, one at a time | Khan | Hint 1: which formula; hint 2: substitute | [M] Shih 2008 | all |
| T14 | Diagnose before help | Ask where he is stuck before any hint | Khanmigo Lite | "Formula, numbers or meaning?" | [S] | all |
| T15 | Tool-checked claims | Every number he gives is checked by running code | Khanmigo (SymPy) | Python recomputes his cost | [M] LLM maths errors (ai-tutoring.md) | P, C, E |
| T16 | Consequence feedback | Show what his choice does, then why | Brilliant (Mario pit) | His TTL gives $X and Y% hit rate | [M] elaborated feedback g = 0.49 | P, D |
| T17 | Two depths | Base and stretch version of the same item; best counts | CS50 | Stretch: same brief at half budget | [S] | D, P |
| T18 | Keep the bug in | Worked example shows a real mistake, symptom and fix | Karpathy micrograd | A join that doubles rows, caught by a count check | [M] Große and Renkl | C, E |
| T19 | Sanity check with expected value | Before running, state what a correct result must be | Karpathy recipe | Always-pass judge: TNR = 0 | [S] | E, C, P |
| T20 | Real traces, real mess | Examples come from one real product with real noise | Hamel | Lucy traces, UUID assertion | [S]; unrealistic examples confuse [S] | E |
| T21 | Price every decision at scale | Per call, per day, per month, and the flip point | Chip Huyen | $0.004 x 10 billion = $40M a day | [S] | P, D |
| T22 | Answer key ships with the task | Expected output given; he sees which row differs | Nand2Tetris .cmp | Expected judge labels for 12 traces | [S] | C, E |
| T23 | Label the wrong way | A bad version is headed as bad before it is shown | Julia, Hello Interview | "Bad: fixed 512-token chunks, because..." | [S]; refutation text | D, C |
| T24 | Short analogy with a break point | One or two sentences, plus where it fails | Julia, Case | "Temperature is a lottery; but it cannot add a word the model scored zero" | [S]; teaching-methods.md 2e | L |
| T25 | Second person, spoken register | "You", "your bot"; plain verbs | Khan | "Your bill doubles" not "costs increase" | [M] d = 0.30 retention, 0.54 transfer | all |
| T26 | Look-away recall | Before the next part, recall the last one without scrolling | Oakley | "What did T do to the score gap?" | [M] retrieval | all |
| T27 | Space confusable pairs | Do not teach look-alike ideas in the same session | Math Academy non-interference | Precision and recall on different days | [S]; interleave later [M] | E |
| T28 | 1 to 3 feedback points | Biggest first, only concepts he has met | Exercism | Design review: 3 points maximum | [S]; ai-tutoring.md 4f | D, C |

---

## Part B. The explanation standard

Every explanation, worked example and practice item must pass this before it is sent. It is a checklist
for the checker script (ai-tutoring.md 4g), not advice. Each line names its technique.

**Opening**
1. First line is a decision or failure with a number or a stake (T1). No definition first.
2. He answers something (a pick or a number) before any explanation (T3). Skipped only for untaught facts (ai-tutoring.md 1d).

**Body**
3. Concrete case with real numbers before the general rule; the rule is at most 3 lines, at the end (T4).
4. One running example with fixed numbers for the whole part (T8). No new example mid-part.
5. At most one new term; it is defined in plain words the moment it appears (Julia pattern 6).
6. Every claim is shown by a run, a table or a source (Julia pattern 10). Numbers were computed by code (T15).
7. If a component or rule is introduced, the failure it fixes is shown first (T6).
8. At least one comparison: naive vs better, or the same thing across a knob (T9, T10).
9. Consequence stated in money, time or users at the scale in the brief (T21).
10. One boundary: where this stops being true (T24, skill-methods.md C2 step 6).
11. A wrong version, if shown, is labelled wrong before it appears (T23).
12. Analogy only if needed: one or two sentences plus its break point (T24).
13. Second person, short sentences, no filler, no hype words ("powerful", "crucial") (T25; Case's cut-10% rule).
14. Under 150 words of explanation before his first answer; under 250 per segment (T12, teaching-structure.md).

**Practice item**
15. Same shape as the worked example just shown; surface can differ (ai-tutoring.md 4a).
16. Written with its step list, answer key and expected output first (T13, T22).
17. Asks for a decision or a judgment with a reason, not a definition.
18. A base and a stretch version exist (T17).
19. Feedback on a wrong answer shows the consequence of his choice, then the reason, in at most 3 points (T16, T28).

**Close**
20. One recall question filed for spaced review (T26).

### Before and after: why temperature changes an LLM's answers

**Before** (the usual explanation; fails items 1, 2, 3, 5, 6, 8, 9, 10, 17):
> Temperature is a hyperparameter that controls the randomness of the model's output by scaling the
> logits before the softmax function. Lower temperature makes outputs more deterministic, while higher
> temperature increases creativity and diversity. It typically ranges from 0 to 2. Use low values for
> factual tasks and higher values for creative tasks.

Four undefined terms, no numbers, "creativity" is asserted, nothing for him to do, no decision.

**After** (numbers computed in Python, 2026-09-24):

> **Your support bot answers "What is the capital of Pakistan?" 1,000 times a day.** The setting is
> temperature 1.0, the default.
>
> **Pick first:** how many of the 1,000 answers start with the wrong city? (a) about 0 (b) about 20
> (c) about 150 (d) about 350
>
> Here is what the model has before it writes the next word. It gives each candidate a score:
>
> | Next word | Score | Chance at T = 0.5 | T = 1.0 | T = 2.0 |
> |---|---|---|---|---|
> | Islamabad | 5.0 | 97.9% | 83.1% | 57.9% |
> | Karachi | 3.0 | 1.8% | 11.2% | 21.3% |
> | Lahore | 2.0 | 0.2% | 4.1% | 12.9% |
> | "a" | 1.0 | 0.0% | 1.5% | 7.8% |
>
> The model then draws one word, like a lottery with those chances. Temperature is the number every
> score is divided by before the chances are worked out. Divide by 0.5 and the gaps between scores
> double, so the leader takes almost everything. Divide by 2 and the gaps halve, so the others catch up.
>
> **What it costs you, per 1,000 calls:** Karachi or Lahore at T = 0.5: about 20. At T = 1.0: about 153.
> At T = 2.0: about 342. The answer was (c).
>
> **Where this stops:** temperature only reshuffles the model's own scores. If the model scored Karachi
> highest, T = 0 says Karachi 1,000 times out of 1,000: consistent, and consistently wrong. And T = 0 can
> still vary slightly on real servers, because of how requests are batched [S]
> https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
>
> **The decision:** fact lookups, extraction and support: 0 to 0.3. Naming a product or drafting
> options: 0.7 to 1.0. The trade: lower means the same answer every time, including the same mistake;
> higher means variety, with more answers off target.
>
> **Your turn:** your eval shows the bot gives 3 different refund amounts for the same ticket across
> 5 runs. Which knob first, and what will it not fix?

Checklist pass: hook with stake (1), pick first (2), table before rule (3), one example throughout (4),
one new term defined in place (5), numbers run (6), sweep across a knob (8), cost at 1,000 calls (9),
boundary (10), judgment question with trade-off (17). Recall card: "Temperature divides the scores:
small T widens the gaps, large T narrows them. It cannot fix a wrong top score."

The same shape works for hybrid search: hook (a customer types order ID 4471-B and meaning search
returns a returns-policy page), pick first (which of 3 retrievers finds it), a table of recall@5 for
meaning-only, keyword-only and hybrid on 50 real queries split into ID queries and question queries,
the rule last, the boundary (hybrid adds a merge step and a second index to run).

---

## Part C. What the best resources consistently avoid

| Avoid | Who avoids it, and evidence |
|---|---|
| Opening with a definition or general framework | Sanderson, Case, Julia pattern 9 [S]; concreteness fading review [S] |
| Interesting but irrelevant material (jokes, history, decorative pictures, long analogies) | Rey 2012 meta-analysis, 39 effects: seductive details lower retention (small to medium) and transfer (medium) [M] https://eric.ed.gov/?id=EJ986386 ; Khan "not too fancy" [S]; Julia patterns 3 and 4 [S] |
| Several new ideas in one explanation | Julia pattern 8 [S]; Math Academy knowledge points and non-interference [S] |
| Claims without proof ("X is better") | Julia pattern 10 [S]; Karpathy states expected values [S] |
| Features without the problem they solve | Julia pattern 13 (Kubernetes homepage) [S]; Ciechanowski and Case introduce parts only as fixes [S] |
| Toy examples that do not look like real use | Julia pattern 5 [S]; Hamel uses real traces [S]. Toy numbers are fine when the shape is real (Alammar's 6-word vocabulary) |
| Long explanation before the learner acts | Math Academy minimum effective dose [S]; Guo: engagement falls after 6 minutes [M] |
| "Do you understand this?" as the check | Sal Khan on why his cousins preferred video [S]; Graesser: students say yes when they do not [M] (ai-tutoring.md) |
| Handing over the full solution, or more than 3 points of feedback | Exercism [S]; Khanmigo Lite [S]; Bastani −17% (ai-tutoring.md) [M] |
| Judging the explanation by how good it feels | Feynman's preface on his own lectures [S]; Oakley's illusions of competence [S]; Bastani students did not feel they learned less [M] |
| Interactivity for its own sake | Case: use interactives only where they work best [S]; Distill review: limited evidence, many readers never interact [S] |
| Showing a wrong method without saying it is wrong | Julia pattern 12 [S] |

---

## Gaps
- Most craft claims are [S]: teachers describing their own practice. Measured support comes from the
  general findings they match (conversational style, seductive details, worked examples, try-first,
  feedback), not from tests of the resources themselves.
- Guo 2014 measured engagement (watch time, attempting problems), not learning.
- The Khanmigo Lite prompt was read from a third-party copy, not a Khan Academy page.
- Math Academy's internal writing guide for explanations is not public; its craft here is inferred from
  The Math Academy Way and Skycak's posts.
- Videos (3Blue1Brown, Karpathy, CS50) were read through notes, transcripts and summaries, not watched;
  the 3Blue1Brown temperature scene is described from a secondary summary.
- Exercism's "how to mentor" page returned 403; the guidance comes from its "how to give great feedback" page.
- No study tests these techniques on AI-engineering topics or on adult self-learners specifically.
