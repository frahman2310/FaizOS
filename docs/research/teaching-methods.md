# Teaching methods: what the research says (for FaizOS chat lessons)

Researched 2026-09-22. Written for one learner: finance undergraduate, no coding background, learns AI
engineering by reading and judging code and making design decisions, one part per chat message.

Today's brief from the learner: questions should be more analytical and thought provoking; explanations
must be more specific and much clearer, with all the background and context. Current question mix is
mostly "compute a business number", "classify", and "someone broke it: crash / quietly wrong / fine".
He is strong at arithmetic (about 88% first try) and weak at "which way does a wrong number bend the
decision" (0/3 recently). He dislikes repetition, jargon and long files.

Grades: **strong** = several meta-analyses or a large consistent literature. **moderate** = one
meta-analysis or several good experiments with known limits. **weak** = few studies, lab only, or
reasoning by extension.

## The short version

1. His arithmetic questions are recall-plus-procedure. They feel analytical but mostly test a skill he
   already has. Replace most of them with questions that need a causal chain: predict, compare two
   cases, find the error, or trace a wrong number to a decision.
2. The direction-question failures are a missing worked chain, not a missing skill. Show one fully
   worked direction chain, then fade it, then ask cold.
3. Explanations fail novices when they skip the goal or the consequence. Every explanation needs three
   parts: what the thing is for, how it works in one concrete case, and what changes in money or
   decisions if it goes wrong.
4. Asking before telling works, but only if the telling comes right after and builds on his answer.

## 1. Questions that build analytical thinking

### 1a. Self-explanation prompts: strong
Asking the learner to explain why a step or a result holds. Meta-analysis of 64 reports: g = 0.55
(Bisra et al. 2018). Chi's ICAP framework explains why: "constructive" tasks (producing something not
in the text) beat "active" ones (picking, highlighting) which beat "passive" reading.
- Backfires: open "explain this" prompts with no target produce vague answers. Focused prompts
  ("which line causes this, and why") beat generic ones. Adds time, so use on the key step only.
- AI example: "The judge scores 4/5 but the answer is wrong. Point at the one line that let that
  happen, and say in one sentence why that line allows it."

### 1b. Elaborative interrogation ("why is this true?"): moderate
Dunlosky et al. 2013 rate it moderate utility. Works only when the learner has some prior knowledge;
with none, it is no better than rereading (Woloshyn, Pressley and colleagues 1994).
- Backfires: asking "why" about a mechanism he has not seen yet produces guessing, not thinking.
- Use it one step after he has seen the mechanism, not before.
- AI example: "Why does the cache key include the model name and not just the prompt?"

### 1c. Contrasting cases: moderate to strong
Two cases that are the same except one feature. Meta-analysis: d = 0.50 for comparing cases over
studying single cases (Alfieri, Nokes-Malach, Schunn 2013). Schwartz and Bransford 1998: comparing
cases first, then being told the principle, gave much better transfer a week later than either alone.
- Backfires: if the cases differ in several ways, the learner cannot see which difference matters.
  The comparison must be followed by the explanation (the "time for telling").
- AI example: "Two judges. Same prompt, same model. Judge A sees the reference answer, Judge B does
  not. On 200 support tickets, which one's errors cost you more money, and why?"
- This is the best single upgrade for his direction weakness: vary one number, ask what moves.

### 1d. Predict, then reveal: moderate
Making a prediction before seeing the outcome boosts learning, mainly for outcomes that surprise
(Brod 2021 review; Brod et al. 2018). The surprise drives attention to the correct answer.
- Backfires: if the prediction is a coin flip with no reasoning, there is little gain. Ask for the
  prediction and a one-line reason. If the answer is never revealed quickly, the benefit is lost.
- AI example: "Before I run it: if we cut the retry limit from 3 to 1, does the monthly bill go up,
  down, or stay? One line why." Then run it and show the number.
- Note: his own evidence log already shows builds skip this step (C37). It is cheap to add.

### 1e. Error-finding (erroneous examples): moderate
Solutions with a planted error to find, explain and fix. Delayed-test benefit over normal practice
(McLaren, Adams, Mayer 2016); the immediate test often shows no difference. Barbieri et al. 2023 (math
worked examples, g = 0.48 overall) coded correct vs incorrect examples as moderators.
- Backfires: novices who have not yet seen correct examples get confused ("confrustion"). Use after
  one correct example, and prompt him to explain the error, not just spot it.
- His current "crash / quietly wrong / fine" question is a weak version: it asks for a category, not
  a mechanism. Upgrade it: "quietly wrong, in which direction, and who notices first?"

### 1f. Problem first, instruction second (productive failure): moderate
Meta-analysis of 166 comparisons: d = 0.36 for conceptual understanding and transfer, up to 0.58 when
designed well, with no loss on procedure (Sinha and Kapur 2021). Loibl, Roll, Rummel 2017: it only
works when the task uses contrasting cases or the teaching builds directly on the learner's attempts.
- Backfires: failure with no follow-up teaching is just failure. Very low prior knowledge plus a hard
  open problem overloads.
- AI example: "You have 10,000 answers and budget to hand-check 100. How would you pick the 100?"
  Then teach stratified sampling using his answer as the starting point.

### 1g. Deep-level reasoning questions: moderate
Question stems that force links between parts ("how does X cause Y", "what happens to Y when X
changes") improved learning from watched material across school and college (Craig, Gholson and
colleagues 2006, 2009). Shallow stems ("what is X") did not.

### 1h. Fermi estimates, "what would have to be true", counterfactuals, trade-offs: weak
No meta-analysis found. They are sensible extensions of self-explanation and contrasting cases, and
consulting and finance interviews use them widely, but treat them as untested. Use them because they
force a causal chain, not because of direct evidence.
- "What would have to be true" example: "For the cheap model to be the right choice here, what would
  the error rate have to be below? Show the break-even."
- Trade-off example: "Doubling the eval set cuts your noise by only about 30% (square root of 2) but doubles cost. At what decision
  size is it worth it?"

### What does NOT build analytical thinking
- More arithmetic when he already gets 88% first try. It feels like practice but is mostly
  performance, not learning (Bjork and Bjork 2011).
- Pure classification ("which type is this") without a "why" tail. That is recognition.
- Why-questions before he has the facts they need (1b).

### Fixing the direction weakness (the 0/3)
No study targets "which way does an error bend a decision" directly, so this is inference from 1a, 1c,
1d and worked-example research (moderate by extension).
1. One fully worked chain, written as a short numbered sequence: error in input, which way the
   measured number moves, which way the decision moves, what it costs. Four links, each one line.
2. Next time, the same chain with one link blank (fading, Renkl). Then two blank.
3. Then a contrasting pair: same system, the error flips sign. He must say both directions.
4. Only then a cold direction question.
Keep every link in business words: "the judge is too lenient, so measured accuracy reads high, so we
ship too early, so bad answers reach customers."

## 2. Explanations that land for a novice

### 2a. Worked examples first, then fade: strong
Studying worked solutions beats solving from scratch for novices (Sweller; Barbieri et al. 2023,
g = 0.48). Fading steps out over time triggers self-explanation and eases the move to independent
work (Renkl, Atkinson).
- **Expertise reversal (strong, Kalyuga):** the same full worked detail that helps a novice hurts
  someone who already knows it. This is why he hates repetition. Rule: full detail on new ideas,
  one-line reminder on known ones, nothing on mastered ones.

### 2b. Cognitive load and coherence: strong
Extra interesting but irrelevant material ("seductive details") hurts learning; meta-analysis finds a
small to moderate negative effect (Sundararajan and Adesope 2020). Cut side stories, trivia and
history that do not feed the decision.
- This does not conflict with "more context". Context that the decision needs is essential; context
  that is merely interesting is harmful. Test each sentence: does he need it to answer the question?

### 2c. Signalling: moderate
Cues that point at what matters help, mostly for low prior knowledge learners (Richter, Scheiter,
Eitel 2016, r = 0.17). In chat: bold the one term that matters, name the line number he should look
at, say "the key point is" once.

### 2d. Segmenting: moderate
Learner-paced chunks beat one continuous block, g about 0.32 to 0.36 (Rey et al. 2019). One part per
message already does this. Keep it.

### 2e. Analogies: moderate
Help when the mapping is made explicit and the learner is shown where the analogy breaks (Richland
and Simms 2015). A bare analogy can import the wrong structure.
- For him, finance analogies map well: eval set as audit sample, judge as auditor, cache as
  pre-computed report, token cost as unit cost. Always add one line: "where this analogy breaks".

### 2f. Curse of knowledge: moderate
Experts are worse than intermediates at predicting how hard a task is for novices, and simple
debiasing does not fix it (Hinds 1999). Practical fix: check each explanation for undefined terms and
skipped steps before sending. Any term he has not met gets a plain definition in the same sentence.

### 2g. Refutation text: moderate
When a common wrong belief exists, state it, say it is wrong, and say what is true and why. g = 0.41
(Schroeder and Kucera 2022). Useful for direction errors: "You might think a stricter judge makes the
model look better. It does the opposite, because..."

### What "full context" means in practice
Every new idea, in this order, each in one to three sentences:
1. **Goal:** what problem this solves, in money or risk terms.
2. **Mechanism:** how it works, shown on one concrete case with real numbers.
3. **Consequence:** what goes wrong, and in which direction, if it is missing or broken.
4. **Where it sits:** which earlier part it connects to (one line).
Skipping 1 or 3 is the most common cause of "I read it but it didn't land".

## 3. Catching and keeping attention in text

| Idea | Evidence | Grade |
|---|---|---|
| Curiosity (a question he wants answered before the answer) | Curious states improve memory for the answer and for nearby material; answers to high-curiosity questions recalled better 10 days later (Kang et al. 2009; Gruber et al. 2014) | moderate |
| Prediction before reveal | Surprise from a wrong prediction drives encoding (Brod 2021) | moderate |
| Pre-questions | Big gain for the questioned content, g = 0.66, but no gain for unasked content, g = 0.01 (Pan and Carpenter 2023) | strong |
| Generation (producing beats reading) | d about 0.40 (Bertsch et al. 2007) | strong |
| Desirable difficulties | Spacing, interleaving, testing, varied practice hurt in-session performance but help later (Bjork and Bjork 2011) | strong |
| Stakes (a real cost or customer at risk) | Plausible, supported indirectly by curiosity work | weak |
| Stories and narrative openers | Can help, but off-topic stories are seductive details and hurt | weak, often harmful |
| Learning styles (visual vs verbal matching) | No support for matching (Pashler et al. 2008) | folklore |

Pre-question lesson: a pre-question only primes the thing it asks about. So ask about the core idea of
the part, never about a side detail.

## 4. Retention without repeating what he knows

- **Retrieval practice: strong.** Testing beats restudying across many conditions (Adesope et al.
  2017; Dunlosky et al. 2013 rate it high utility).
- **Spacing: strong.** The best gap grows with how long he must remember it (Cepeda et al. 2006).
- **Interleaving: moderate.** g = 0.42 overall; strongest when the categories are easily confused and
  the material is complex; can backfire on simple word material (Brunmair and Richter 2019).

How to fit these in without repetition:
1. **Retrieve inside new work, not as a review block.** A new lesson's question uses an old idea as
   one link in the chain. He must recall it to answer, but the question is new.
2. **Change the surface, keep the structure.** Same principle (for example "a biased measure bends
   the decision"), new system: judge, cache, retriever, cost model. This is interleaving plus
   transfer, and never feels like a repeat.
3. **Space by success.** An idea he got right cold gets a longer gap; one he missed comes back in the
   next lesson inside a different system.
4. **Drop mastered ideas from explanations** (expertise reversal) but keep them in question chains.

## Question design checklist (for each chat question)

1. Does answering need a causal chain of at least two links? If it is one lookup or one calculation,
   upgrade it.
2. Is the answer revealed straight after, with the reasoning, and built on what he said?
3. Is every term already defined, or defined in the question?
4. Is there a concrete number or case, not an abstract "suppose"?
5. For direction questions: has he seen a worked chain of this shape before? If not, show one first.

## Upgrade templates (from his current types)

- **Compute a number** becomes: "Compute X. Now the input is 20% off in this direction. Does the
  decision change? At what error does it flip?"
- **Classify** becomes: "Two cases, one difference. Which is riskier, and what single change makes
  the other one riskier?"
- **Crash / quietly wrong / fine** becomes: "Quietly wrong in which direction? Who finds out first,
  and how much has it cost by then?"

## Sources

- Dunlosky et al. 2013, learning techniques review: https://journals.sagepub.com/doi/abs/10.1177/1529100612453266 (PDF: https://www.wku.edu/senate/documents/improving_student_learning_dunlosky_2013.pdf)
- Bisra et al. 2018, self-explanation meta-analysis: https://link.springer.com/article/10.1007/s10648-018-9434-x
- Chi and Wylie 2014, ICAP: https://www.tandfonline.com/doi/abs/10.1080/00461520.2014.965823
- Woloshyn et al. 1994, elaborative interrogation and prior knowledge: https://onlinelibrary.wiley.com/doi/abs/10.1002/acp.2350080104
- Alfieri, Nokes-Malach, Schunn 2013, case comparison meta-analysis: https://www.lrdc.pitt.edu/schunn/papers/ContrastingCasesMeta-AlfieriEtAl2013.pdf
- Schwartz and Bransford 1998, A time for telling: http://aaalab.stanford.edu/assets/papers/earlier/A_time_for_telling.pdf
- Brod 2021, predicting as a learning strategy: https://link.springer.com/article/10.3758/s13423-021-01904-1
- Brod et al. 2018, prediction and surprise: https://www.sciencedirect.com/science/article/abs/pii/S0959475217303468
- McLaren, Adams, Mayer 2016, erroneous examples delayed effect: https://link.springer.com/article/10.1007/s40593-015-0064-x
- Barbieri et al. 2023, worked examples meta-analysis: https://link.springer.com/article/10.1007/s10648-023-09745-1
- Sinha and Kapur 2021, productive failure meta-analysis: https://journals.sagepub.com/doi/10.3102/00346543211019105
- Loibl, Roll, Rummel 2017, when problem-solving-first works: https://link.springer.com/article/10.1007/s10648-016-9379-x
- Craig et al. 2006 and deep-level questions summary: https://learnlab.org/wiki/index.php?title=Deep-level_question
- Kalyuga, expertise reversal: https://link.springer.com/article/10.1007/s11251-009-9102-0
- Sundararajan and Adesope 2020, seductive details: https://link.springer.com/article/10.1007/s10648-020-09522-4
- Richter, Scheiter, Eitel 2016, signalling: https://www.sciencedirect.com/science/article/abs/pii/S1747938X15000664
- Rey et al. 2019, segmenting: https://link.springer.com/article/10.1007/s10648-018-9456-4
- Richland and Simms 2015, analogy: https://wires.onlinelibrary.wiley.com/doi/abs/10.1002/wcs.1336
- Hinds 1999, curse of expertise: https://www.researchgate.net/publication/232555027_The_curse_of_expertise_The_effects_of_expertise_and_debiasing_methods_on_prediction_of_novice_performance
- Schroeder and Kucera 2022, refutation text: https://pubmed.ncbi.nlm.nih.gov/35095236/
- Kang et al. 2009, curiosity: https://pubmed.ncbi.nlm.nih.gov/19619181/
- Gruber et al. 2014, curiosity and memory: https://www.sciencedirect.com/science/article/pii/S0896627314008046
- Pan and Carpenter 2023, pre-questions: https://link.springer.com/article/10.1007/s10648-023-09814-5
- Bertsch et al. 2007, generation effect: https://link.springer.com/article/10.3758/BF03193441
- Bjork and Bjork 2011, desirable difficulties: https://www.researchgate.net/publication/284097727_Making_things_hard_on_yourself_but_in_a_good_way_Creating_desirable_difficulties_to_enhance_learning
- Pashler et al. 2008, learning styles: https://journals.sagepub.com/doi/10.1111/j.1539-6053.2009.01038.x
- Adesope et al. 2017, practice testing meta-analysis: https://journals.sagepub.com/doi/abs/10.3102/0034654316689306
- Cepeda et al. 2006, spacing: https://digitalcommons.usf.edu/psy_facpub/1771/
- Brunmair and Richter 2019, interleaving: https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf
