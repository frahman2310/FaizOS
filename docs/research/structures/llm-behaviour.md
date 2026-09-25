# Learning structure: how LLMs behave

> **Amended 2026-09-24:** the independent review (`review.md`) kept this structure with changes. Where this file disagrees with `INTEGRATED.md` (plain step names, shared recall queue, one mastery rule, start order, the week), `INTEGRATED.md` wins.


Written 2026-09-24. One skill: tokens, sampling and temperature, context windows, hallucination, pricing,
and how models are pretrained and post-trained, at the level of concepts and facts to remember.
Builds on `../recommended-method.md`, `../postmortem.md` and `../curricula/` (method-effectiveness,
skill-methods, ai-tutoring, teaching-craft, curriculum-design). Numbers already there are cited, not repeated.

**Tags.** [M] measured (with who measured it). [S] stated by the expert, no numbers. [SR] self-reported by
the product or its makers. **Grades** as in method-effectiveness.md: A strong, B moderate, C weak, D none.

---

## 1. What kind of learning this is, and what the new experts add

**Kind.** Two things at once: (a) a small set of **concepts that fight intuition** (the model generates,
it does not look up; temperature reshapes probabilities; the model has no memory between calls), and
(b) a larger set of **facts** that must stay available (about 3.5 English characters per token for Claude,
output tokens cost more than input, prices and window sizes change). Physics education research calls
(a) conceptual change: the learner already holds a wrong model, and telling him the right one does not
remove the wrong one. That is why this skill needs its own structure. Like the applied skills it starts from a
**worked demonstration** (the mechanism shown on a real run, quoted from a named expert: section 2); what it adds
is a **refutation of the wrong model with his own runs as the evidence**, and **facts kept by spaced cards**.
(Corrected 2026-09-25: an earlier line set this skill apart from worked examples; see section 2.)

### What the new experts add

| Expert, finding | Evidence | What it changes here |
|---|---|---|
| **Hake 1998**: 62 physics courses, 6,542 students, same concept test (Force Concept Inventory). Traditional courses: normalized gain 0.23 ± 0.04; interactive-engagement courses: 0.48 ± 0.14 | [M] independent standardized test, but courses not randomized https://eric.ed.gov/?id=ED441679 | Measure this skill the same way: a concept inventory before and after, reported as normalized gain. Target the interactive band |
| **Mazur, Peer Instruction**: gain rose from 0.25 (last lecture year) to 0.49 (first PI year) and 0.74 by 1997, same test | [M] one course, not randomized https://web.mit.edu/jbelcher/www/TEALref/Crouch_Mazur.pdf | Superseded 2026-09-25: no ConcepTest votes or revotes in units; the idea kept is "one concept question with a reason", asked after the worked demonstration (section 2) |
| **ConcepTest difficulty rule**: 35 to 70% should be right before discussion; below 35% the question is ambiguous or the concept missing; above 70% little to gain | [S] same paper, sec. on ConcepTest design | Superseded 2026-09-25: not used. The pre-question is unscored and comes before teaching, so it has no band; try steps aim at about 80% right first time, alarm under 70% (section 2, `engine.py tries`) |
| **Crouch, Fagen, Callan, Mazur 2004**: correct outcomes on a later test: no demo 61%, watched 70%, predicted first 77%, predicted and discussed 82%. Correct **explanations**: 22%, 24%, 30%, 32%. Prediction costs about 2 minutes | [M] researcher test https://www.otffeo.on.ca/wp-content/uploads/sites/2/2014/11/Mazur_demo-article.pdf | **Challenge to the current plan**: predict-run lifts "what happens" but leaves "why" at 30%. The explanation must be written, checked against the source, and refuted if wrong |
| **Interactive lecture demonstrations** (Sokoloff, Thornton): predict on a sheet, discuss, watch, compare with the prediction | [S] method https://pages.uoregon.edu/sokoloff/ILDbook0116.pdf ; gains reported on the FMCE [M, authors' own] | The prediction is written down before the run, and compared line by line after |
| **Refutation texts**: state the wrong idea, flag it wrong, give the right one with evidence. Tippett's 20-year review: consistently beats plain explanation | [S] review https://eric.ed.gov/?id=EJ905216 ; pre-registered meta-analysis, 71 articles, 294 effect sizes, advantage held across 26 moderators [M] https://experts.nau.edu/en/publications/the-effectiveness-of-refutation-text-in-confronting-scientific-mi/ ; g = 0.41 (Schroeder and Kucera 2022, teaching-methods.md 2g) | Every misconception item ends with a 4-line refutation using his own run as the evidence |
| **Posner et al. 1982**: change needs dissatisfaction with the old idea, and a new one that is intelligible, plausible and fruitful | [S] theory, over 10,000 citations https://onlinelibrary.wiley.com/doi/10.1002/sce.3730660207 | Order inside a unit: the run creates the dissatisfaction; the explanation must also pay off (a cost or a risk) |
| **Chi 2008**: three kinds of change. False beliefs yield to refutation; flawed models to many small revisions; **category mistakes** (a process taken for a thing) are the hardest | [S] theory https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chi_concpetualchangechapter_0.pdf | "The model is a database I query" is a category mistake: a thing that stores answers vs a process that samples the next token. It is taught first and revisited in every unit |
| **Users' wrong models of LLMs**: information retrieval is the most common mental model; users expect database lookup, search, calculation, and web access by default | [M] qualitative studies, review https://arxiv.org/abs/2510.25662 | The concept inventory's distractors come from these, then from his own wrong answers |
| **Adams and Wieman 2011**: concept tests are built from learners' own words in interviews, then checked item by item | [S] method https://eric.ed.gov/?id=EJ925667 | Inventory distractors are rewritten from his actual wrong answers after the first pass |
| **Quantum Country** (Matuschak and Nielsen), 112 questions inside an essay: after about 30 minutes of total review most readers held nearly all answers for 2+ weeks; 1 hour, 5+ weeks; 1.5 hours, 9+ weeks. Without review at one month: hard questions 42% recalled, easy 89% | [SR] makers' own data, observational https://notes.andymatuschak.org/z93QR51f6HAUPLVDxE6KT1T ; they state no controlled with-vs-without comparison yet https://notes.andymatuschak.org/zt1TyUANyt84UkQVBJjWEGZ3JUd2HP92r65 ; reading overhead 35 to 50% (same page) | Cards are embedded in the unit (not a separate deck made later) and written by an expert; total review time per card is small |
| **Matuschak, "How to write good prompts"**: focused, precise, consistent, tractable, effortful; for concepts, ask from several angles (attributes, similarities, parts, causes, significance); 5 to 10 prompts per source on first pass | [S] https://andymatuschak.org/prompts/ | Card-writing rules (section 5) |
| **Wozniak, 20 rules**: understand before memorizing; minimum information; avoid sets and lists; fight interference; give sources; **date-stamp volatile facts** | [S] https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge | Prices and window sizes get a date and a source on the card |
| **FSRS** scheduler: better recall prediction than SM-2 in about 99.6% of about 10,000 real collections | [M] open benchmark https://github.com/open-spaced-repetition/srs-benchmark ; "20 to 30% fewer reviews for the same retention" [S] https://expertium.github.io/Benchmark.html | Replace the fixed 1, 3, 7, 21 day ladder with FSRS at 90% target retention |
| **Butler 2010**: repeated testing beat restudy a week later on new inferential questions, including a different domain | [M] researcher tests https://pubmed.ncbi.nlm.nih.gov/20804289/ | Some cards ask "why" and "what follows", not only "what", so recall carries to new cases |
| **Olah, "Research Debt"**: good explanation is "distillation", work in its own right | [S] https://distill.pub/2017/research-debt/ | Explanations come from checked sources (Karpathy, Huyen, HF), never improvised. Karpathy, 3Blue1Brown and Alammar craft is already in teaching-craft.md (puzzle list, concrete first, fixed sizes) and is reused, not repeated |

### Corrections found while building this
- `private/research-base/.../INDEX.md` says Huyen's temperature example uses logits [1, 2]. The source uses
  **[1, 3]**; [0.12, 0.88] at T = 1 and [0.02, 0.98] at T = 0.5 are right for [1, 3] (checked by running softmax).
- ScaleDojo's temperature chapter says temperature 0 "can occasionally" differ. Thinking Machines measured
  80 distinct completions in 1,000 runs of one prompt at temperature 0 on Qwen3-8B [M]
  https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ . "Occasionally" understates it.
- Every number in a unit comes from a saved run (`learn/demo.py`, `learn/calc.py`, with `--save`), so units
  are written only from recorded outputs (tiktoken and transformers are installed as of 2026-09-25).

---

## 2. The structure

> **Corrected 2026-09-25** after `docs/research/gap-audit-llm-behaviour.md` (F1, F5, F16, F20) and
> `audit-pedagogy.md` (M1). The first version put a scored "commit before any teaching" first and had no
> worked example, citing Chen, Kalyuga and Sweller 2015. That was a misreading: in Chen 2015 students
> **studied** the material for 10 minutes and only **then** recalled it (retrieval after teaching); the
> "low element interactivity" material was single formulas, and tests were same-session only. Nothing in
> the research base supports graded answering before teaching for a novice. What Chen supports here is
> "study, then retrieve" (the cards), and worked examples for novices on material with interacting parts.
> Every expert this file names (Karpathy, Huyen, the Hugging Face course, ScaleDojo) shows the mechanism
> with real numbers first. The unit below restores that order. It is enforced by `learn/check_unit.py`
> (unit format v3: Kind show / try / scored / close).

**Name: the worked-mechanism unit.** One mechanism per unit. Each numbered row is one message. About 20 minutes.

| # | Step (Kind) | What he receives | Rules | Source |
|---|---|---|---|---|
| 1 | **Goal and odd result** (show) | One line: what he will be able to decide by the end, and what it costs in money or risk. Then one real odd result from a run: two contrasting rows that differ in one thing. Then at most **one optional pre-question**: two options or a one-line answer, plus a one-line reason. | At most 3 new ideas, each explained where it first appears. Under about 150 words before the question. The pre-question is never scored, never hinted, no confidence asked. Skip it when he has no intuitive idea to use (for example temperature). | Goal card (teaching-structure.md); contrasting cases (Loibl, Roll and Rummel 2017); pre-questions (teaching-methods.md); productive-failure prior-knowledge condition (Loibl 2017) |
| 2 | **How it works** (show: the worked demonstration) | Opens with the answer to the pre-question and a prepared line for each option. Then the mechanism in 3 to 5 lines, **quoted or closely adapted from a named expert source** (Karpathy, Huyen, Hugging Face, the saved ScaleDojo chapters), shown on the same real run with its numbers (a table; a sweep across one setting where there is one). One everyday picture in one sentence, plus where it breaks. Ends with one focused self-explanation question on the key line, answerable from what is on screen. | Under about 250 words of explanation. Nothing new that the checks do not need. The picture must not plant the category mistake ("a brain", "a search engine"). | Karpathy deep dive (explains, then shows); skill-methods C2 mechanism card; Kapur consolidation; self-explanation on the key step (method-effectiveness row 8) |
| 3 | **Predict** (try) | A new input where the mechanism just taught gives a direction; all data he needs is in the message. He writes a direction, a rough number and a one-line reason. | Derivable from step 2, not a coin flip (C39). Unscored. Prepared Help block. | teaching-methods 1d; method-effectiveness row 15; Crouch 2004 |
| 4 | **Run and compare** (show) | The real output at once. He says how far off he was and which part of step 2 explains the gap. The small-model line goes here, only if the result is a small-model effect. | Answer shown in this message, never later. | method-effectiveness row 15 ("answer shown at once"); recorded-output rule below |
| 5 | **Wrong idea fixed** (try) | Refutation: the wrong idea, "this is wrong", his runs as evidence, the right idea in the words of step 2; then one decision priced at scale that he works out (not a read-back). | Only ideas taught in steps 2 to 4. Made-up scenario numbers on a line starting "Suppose". Prepared Help block. | Refutation texts (Tippett; Schroeder and Kucera g = 0.41); Posner (pay-off); T21 price at scale |
| 6 | **Checks** (try) | 2 or 3 short questions in one message, same mechanism, new surfaces: a direction question (two options), a "why" in one line, a fix. | Every rule needed is in a step body above. About 80% first-try is the target (A9, A12). Prepared Help block. | Retrieval with feedback (method-effectiveness rows 1, 1b); B9; E12 |
| 7 | **New case 1, 2, 3** (scored) | 2 or 3 transfer items, one per message, each on a different surface (a real failure or product situation): a one-line answer and a one-line reason, each marked. | The only scored steps in the session; mastery never rests on one item (review M3). Every answer rests on a show step body. Stuck order: his own earlier answer, the Key's prepared two options, the step's Help block (a second worked example on a new surface), then the Key's worked answer line by line. A part right after a hint gets half its marks. | Butler 2010 transfer; bar on transfer (section 5) |
| 8 | **Close** (close) | "Next time I see X, I do Y." Goes into the recall queue. | Not scored. | INTEGRATED.md |
| Retry | scored | After a miss, the Help blocks, then new-surface items of the same kinds: about 5 to 10 marked parts (may continue in `## Retry 2`), recorded as marks / total. | Only content from steps always sent (show and try bodies, never Help blocks or Keys). | Bloom and Guskey correctives |
| Cold | scored | 7 days later, new surfaces of the same mechanism: about 5 to 10 marked parts (may continue in `## Cold 2`), recorded as marks / total. | Only content from steps always sent. | Mastery with a delayed recheck (method-effectiveness row 7) |
| Cards | | 4 to 6, each answer found in a step body; at least one why card and one boundary card; number cards carry a second surface; dated facts carry date and source. | First return the next day. | Card rules (section 5); Wozniak rule 1 |

**Extra show steps and file order.** When a mechanism needs more than 3 new ideas, split it: add a further
show step after Run and compare (llm-01 adds "One piece at a time"), so no show step lists more than 3 in its
`New:` line. In the unit file, every `## Help:` block sits after the Close step, as in the other skills' units
(the guard counts steps by their place in the file).

**No skipping (corrected 2026-09-25).** Every step is sent, in order; the guard (`hooks/teaching-guard.py`)
blocks a skipped step, and steps 2 to 5 all state facts the checks, scored items and cards use. A right
pre-question answer is recorded and changes nothing. "ik this" or "move on" means send the next step now,
without extra feedback. (The earlier placement rule, which let steps 3 and 4 or steps 2 to 4 be skipped, is withdrawn.)

**Scoring.** Scored: the New case steps, the Retry items and the Cold items only. Tracked, never gating: the pre-question
answer, reason quality, confidence, first-try rate per step (alarm under 70%).

**Stuck order** (INTEGRATED 2.4): his own earlier answer, two options, the step's prepared Help block, then the
answer with the reason, said back. Every picture is checked against the mechanism: "autocomplete trained on
the internet" is allowed; "a brain that thinks" and "a search engine" are not, because they plant the
category mistake this skill exists to remove.

**Recorded-output rule.** Every output shown comes from `learn/demo.py` or `learn/calc.py` runs saved in
`learn/runs/` with the command that made them, or from verified `learn/facts.md` rows. Never an invented
output. The demo model is Qwen2.5-0.5B-Instruct (tiny, chat-trained); each unit says so once and marks small-model effects.

### Why this differs from the other four skills

| | Evaluation, system design, code | Production | **LLM behaviour** |
|---|---|---|---|
| Backbone | Worked example, faded | Worked numeric solution, faded fast | **Worked demonstration of the mechanism on a real run**, quoted from a named expert, then a refutation of the wrong model |
| His first act | Studies an example | Reads the exhibit | **Reads the goal and a real odd result**; at most one unscored pre-question, answered in the next message |
| The expert answer | An expert's solution | The exact number | **The measured run plus the source's quoted mechanism**, in a step body he reads |
| Main error type | Missing steps | Wrong substitution | **A confident wrong model** (tracked by confidence) |
| Retention | Spaced mixed problems | Spaced mixed problems | **Expert-drafted cards on FSRS**, the largest deck of any skill |
| Unit length | 25 min | 25 min | about 20 min |

---

## 3. Progression

### Concept map order

Rule: the category shift comes first (Chi), because every later concept makes sense only once "it samples the
next token from a learned distribution" replaces "it looks things up". After that, order follows
prerequisites and the order the sources use (Karpathy's deep dive: data, tokens, network, inference, base
model, post-training, hallucination, thinking tokens).

| # | Concept (curriculum-design code) | Needs | Core wrong model it breaks | Demonstration |
|---|---|---|---|---|
| 1 | Next-token prediction; the model is a fixed file of weights | none | "it looks things up / searches / remembers you" | Base-model completion of a half sentence, 5 runs |
| 2 | Tokens (B1) | 1 | "a token is a word"; "all languages cost the same" | English vs Urdu token count of the same sentence; spelling a word letter by letter |
| 3 | Logits, softmax, sampling, temperature, top-p (B2) | 2 | "temperature = creativity dial"; "temperature 0 is deterministic" | Huyen's [1, 3] logits by hand, then 20 runs at T 0 and T 1 |
| 4 | Context window and statelessness (B1, B7) | 2 | "the model remembers our last chat"; "bigger window = uses all of it equally" | Two calls without history; a fact placed at start, middle, end of a long input |
| 5 | Pricing and latency by token | 2, 4 | "input and output cost the same"; "thinking is free" | Token-count call; cost of one call and of 1,000 calls/day from the dated price table |
| 6 | Pretraining (B3) | 1 | "it was taught facts one by one"; "it knows today's news" | Knowledge-cutoff question with and without the fact in context |
| 7 | Post-training: SFT, RLHF, the assistant persona, sycophancy (B3) | 6 | "fine-tuning is how you add knowledge"; "politeness = correctness" | Base vs instruct model on the same prompt; pushback test on a right answer |
| 8 | Hallucination (B3) | 3, 6, 7 | "it lies / it is a bug that will be patched"; "high confidence = correct" | Logprobs on a partly covered question; grounding with a quote |
| 9 | Thinking tokens and reasoning models | 3, 5 | "reasoning happens outside the tokens" | Same word problem answered in one token vs worked out (Karpathy "models need tokens to think") |
| 10 | Bridge to B4 to B8 (embeddings, prompting, tools, context engineering, prompt vs RAG vs fine-tune) | 1 to 9 | handled in the next level | per curriculum-design.md |

### Levels (milestones from curriculum-design.md, made observable)

| Level | He can | Observable milestone | Concepts |
|---|---|---|---|
| **1 Novice** (about 6 weeks) | Predict the direction of one change with the mechanism | Inventory 9/10 with correct reasons; 20 predict-then-run items at 80%+ right direction with a reason; 7-day cold recheck held | 1 to 5 |
| **2 Competent** (about 6 weeks) | Explain a real failure from the mechanism and name the kind of fix | 3 of 4 unseen real failures explained correctly (tokenization, sampling, missing context, post-training habit) and fix type named | 6 to 9 |
| **3 Proficient** (runs inside design units) | Choose prompt, RAG, tool or fine-tune with the mechanism as reason; predict where a model will fail before testing | Written choice for 2 new cases confirmed by a run (curriculum-design.md) | 10 and B4 to B8 |

---

## 4. Practice formats, one example each

**A. Direction check** (a try or scored item, after the worked demonstration; corrected 2026-09-25: the earlier
4-option ConcepTest vote is not used in units, F30). Two options at most, then a one-line reason.
> You set temperature to 0.2 instead of 1.0 for an FBR tax assistant. Does the likeliest next token's share
> go up or down? One-line reason.
Right: up; the rest shrink. A wrong reason names the misconception ("it thinks more carefully", "it looks up"),
which the Help block then answers.

**B. Predict, run, explain** (Sokoloff and Thornton, Crouch 2004).
> Predict: the sentence "How much tax do I owe on my salary?" in English and in Urdu. Which uses more
> tokens with the o200k tokenizer, and by roughly how many times? Run: tutor counts both.
> Explain: why (one to three lines). Source to compare: Petrov et al. 2023, gaps up to 15 times between
> languages https://arxiv.org/abs/2305.15425 ; tiktoken cookbook "Comparing encodings".
> Price: at the dated price table, what does that ratio do to the cost of 10,000 Urdu questions a month?
(No numbers are written here: they come from the run.)

**C. Refutation item** (Tippett; teaching-methods.md 2g).
> **Wrong idea:** "Temperature 0 gives the same answer every time."
> **This is wrong.** It removes sampling randomness only.
> **What is true:** the numbers the model computes can shift with how the server batches requests, so near-tied
> tokens can flip and the text can split from there. Anthropic: "Even with temperature set to 0, the results
> will not be fully deterministic" (anthropic-glossary.md).
> **Evidence:** your run of 20 calls, plus Thinking Machines: 80 distinct outputs in 1,000 runs at T = 0.
> **So what:** a test that compares exact strings will fail at random; check meaning or structure instead.

**D. Spaced-repetition cards**, one concept from several angles (Matuschak lenses). Concept 3, temperature:
| Lens | Front | Back |
|---|---|---|
| Mechanism | Temperature divides the logits by T before which step? | Softmax |
| Cause, effect | Lower T does what to the top token's probability? | Raises it (distribution sharpens) |
| Worked number | Logits [1, 3], T = 1: the likelier token's probability? | 0.88 (Huyen; [1, 3] not [1, 2]) |
| Boundary | Name one reason T = 0 output can still change between calls. | Batch-dependent numerics on the server |
| Consequence | Why not assert exact-string equality in an LLM test at T = 0? | Outputs can differ; compare meaning or structure |

**E. Explain a real failure** (Level 2 transfer, Butler 2010 inferential questions).
> Real output: asked how many "r"s are in "strawberry", the model says 2. Name the mechanism and the fix
> type. (Expected: tokenization; the model sees chunks, not letters; fix: have it spell the word out first
> or call code. Source: Karpathy deep dive, "tokenization revisited".)

**F. Estimate, then check** (his numeracy strength; teaching-craft "every decision priced").
> Before the token-count call: guess the input tokens of this 2-page FBR circular, then the monthly bill at
> 500 questions a day. Then the call, then the bill with the dated price. Log the gap.

---

## 5. Assessment

### The LLM Behaviour Concept Inventory (LBCI, draft 1)

Format per item: one question, 4 options, a one-line reason, a confidence 1 to 5. Scored twice: **answer**
and **reason** (Crouch 2004 showed the two can be 47 points apart). Given at week 0 (baseline), at the end
of each level, and cold 30 days later. Distractors are replaced by his own wrong answers after the first
pass (Adams and Wieman). It is a home-made test, so its gains will look larger than on an outside test
(0.84 vs 0.27, curriculum-design.md): it guides; the outside tasks in section 7 judge.

| # | Item (short) | Right answer | Misconception targeted | Source |
|---|---|---|---|---|
| 1 | Where does the answer to "capital of Australia" come from? | Next-token probabilities learned from training text | Lookup in a database or the web | https://arxiv.org/abs/2510.25662 ; Karpathy intro (two files) |
| 2 | Same prompt, temperature 0, 1,000 calls: how many distinct outputs? | Possibly many; not guaranteed 1 | T = 0 is deterministic | Anthropic glossary; Thinking Machines |
| 3 | Same question in English and Urdu: which costs more? | Urdu, often several times | A token is a word; languages cost the same | Petrov 2023; Anthropic 3.5 chars/token |
| 4 | Why does a model miscount letters in a word? | It sees tokens, not letters | It cannot read / it is careless | Karpathy deep dive |
| 5 | Yesterday's chat: does the model remember it today via the API? | Only if the text is sent again | The model learns from each chat | Anthropic context windows; Karpathy intro |
| 6 | 30 documents in context, the answer is in the middle one: effect? | Accuracy often drops vs start or end | A bigger window is used evenly | Lost in the Middle https://arxiv.org/abs/2307.03172 |
| 7 | The model gives an answer with 99% token probability: is it right? | Not necessarily; confidence is not correctness | High probability = true | OpenAI logprobs cookbook (99.14% on a partly covered question) |
| 8 | Main reason models state false facts fluently? | Trained and scored in ways that reward guessing over "I don't know" | Lying, or a bug to be patched | Kalai et al. 2025 https://arxiv.org/abs/2509.04664 |
| 9 | Fine-tune on 1,000 new facts: likely effect? | Learned slowly, and raises hallucination | Fine-tuning is how you add knowledge | Gekhman 2024 via Weng https://lilianweng.github.io/posts/2024-07-07-hallucination/ |
| 10 | A reasoning model thinks 5,000 tokens to answer in 200: what is billed? | The thinking tokens too, as output, at the higher output rate | Thinking is free; input and output cost the same | OpenAI reasoning guide; anthropic-pricing.md (Sonnet 5: $2 in / $10 out per million, 2026-09) |

### Mastery criteria

| Unit | Bar |
|---|---|
| A concept | Its unit's New case items (2 or 3 surfaces, answer and reason) at the bar, then its Cold items at the bar 7 days later |
| A level | LBCI items for that level 9/10 on answer **and** reason; same bar again at a cold 7-day recheck |
| A card | Recalled at an interval of 21 days or more |
| Not yet | A unit below the bar gets its Help blocks, then its Retry items (SKILL.md step 5). Confidence is recorded for calibration only and never demotes (corrected 2026-09-25) |

### Retention plan

**Card-writing rules** (Matuschak, Wozniak, adapted):
1. No card before the concept is understood (Wozniak 1): cards come after the worked demonstration, the run and the refutation.
2. One fact or one link per card; the answer is a word, a number or one short line (minimum information).
3. The same question always has the same answer (consistent); no "list the five..." cards (avoid sets).
4. For each concept, cover at least 3 lenses: mechanism, consequence, boundary. Add a contrast card when
   two ideas get confused (temperature vs top-p; context window vs training data).
5. At least one card per concept asks why or what follows (Butler: tested inference carries to new cases).
6. A card for a volatile fact carries its date and source ("Sonnet 5 output price, anthropic-pricing, 2026-09").
   Memorize ratios and directions; look up exact prices live.
7. Every card names its source file. A card from a refutation keeps the wrong idea on the back ("not X").
8. He may reword or delete any card; the tutor checks rewrites against rules 2 to 7.
9. About 5 per concept, 4 to 6 per unit; about 50 for Level 1.

**Schedule.** FSRS with target retention 0.9 (the `fsrs` Python package); new cards enter after the unit and first
return the next day. Fallback if FSRS is not wired in: the fixed 1, 3, 7, 21, 60 day ladder already planned.
Daily card time is capped at 5 minutes; if the cap is hit twice in a week, stop adding new cards for 3 days.
Lapsed cards are not re-taught by the tutor; the concept's refutation is shown once, then the card returns.

---

## 6. Weekly dose and session length

| | Weeks 1 to 6 (Level 1) | Weeks 7 to 12 (Level 2) | After |
|---|---|---|---|
| LLM units | as the sitting order gives them (INTEGRATED.md; one new unit per sitting in weeks 1 and 2; sittings, not weekdays, C47), about 20 min | as the sitting order gives them | Inside design and eval units |
| Cards | 3 to 5 min daily | 3 to 5 min daily | 2 to 3 min daily |
| Predict-and-run inside other skills | 1 per week | 2 per week | as needed |
| Total | about 70 min/week | about 55 min/week | about 30 min/week |

Why early: expert curricula put this skill first (expert-curricula.md), and every other skill leans on it. Why
about 20 minutes: one concept per unit; the Crouch 2004 prediction step adds only about 2 minutes; units longer
than one concept broke his attention before (postmortem, method 8). Weekly counts here are superseded by the
sitting order in INTEGRATED.md and `engine.py` (corrected 2026-09-25).

---

## 7. Measures that show it is working

| Measure | How | Healthy | Alarm and action |
|---|---|---|---|
| LBCI normalized gain | (post - pre) / (100 - pre), answers and reasons scored separately | 0.5 or more (above Hake's interactive mean, 0.48) | Under 0.3 (the lecture band): the demos are not breaking the model; rewrite refutations |
| Answer vs reason gap | LBCI answer score minus reason score | 15 points or less | Over 25: he knows what, not why; add explain steps, not more runs |
| First-try rate on try steps | `engine.py tries`, per unit | about 80% | Under 70%: overload; slow down, use the Help blocks, split the unit (the old 35 to 70% first-vote band is withdrawn, 2026-09-25) |
| Confident errors | Wrong answers with confidence 4 or 5 (tracked, never demoting) | Falling to under 10% by week 6 | Flat: the category mistake persists; add a Help block and a refutation line to the next unit |
| Prediction direction | 20 predict-then-run items per level | 80% or more with reasons | Under 60% at week 6 |
| Card retention | True recall on due cards | 85 to 92% (target 90) | Under 80%: cards badly written; rewrite by the rules |
| Cold retention | LBCI 30 days after the level | 80% or more of the post score | Under 70%: more why-cards |
| Transfer | Unseen real failures explained (Level 2) | 3 of 4 | 2 or fewer |
| Early warning | High card recall with a low LBCI | | Cards teach wording, not the concept: replace fact cards with why and boundary cards |

---

## 8. Evidence grade per choice, and exclusions

| Choice | Grade | Basis |
|---|---|---|
| Concept test before and after, normalized gain | B | Hake [M] 6,542 students, not randomized; Adams and Wieman [S] |
| One concept question with a reason, after teaching (no vote or revote) | B | Crouch and Mazur [M] one course; the revote without peers was untested and is dropped |
| Predict before the run | B | Crouch 2004 [M]; Brod review (method-effectiveness row 15) |
| Written explanation checked against the source | B | Crouch 2004: explanations lag outcomes [M]; self-explanation g = 0.55 (recommended-method) |
| Refutation after the run | B | Meta-analysis 294 effects [M]; g = 0.41 [M] |
| Category shift taught first | C | Chi [S]; users' lookup model [M, qualitative] |
| Worked demonstration first, then retrieval (cards); pre-question unscored | B | Chen, Kalyuga, Sweller 2015 [M]: study, then recall, immediate tests only (corrected 2026-09-25: it does not support answering before teaching); worked-example effect for novices |
| Expert-drafted cards embedded in the unit | C | Quantum Country [SR], observational |
| Card rules | C | Matuschak, Wozniak [S]; minimum information widely used, little direct testing |
| Why-cards for transfer | B | Butler 2010 [M] |
| Spaced retrieval itself | A | method-effectiveness.md |
| FSRS over fixed intervals | B | Open benchmark [M] on recall prediction; review savings [S] |
| Price step in every unit | C | teaching-craft.md (Huyen) [S]; fits his strength |

| Excluded | Why |
|---|---|
| Peer discussion (the heart of Peer Instruction) | No peers. The tutor posing as a peer is untested and invites sycophancy (ai-tutoring.md); replaced by a written reason, marked against the unit's Key |
| Watching demos without predicting | Watched demos: 70% vs 61% with none, explanations 24% vs 22% (Crouch 2004) |
| Long video or long reading first (Karpathy 3.5 h) | Supplement only; video replacing teaching 0.28 (method-effectiveness.md). Transcripts are used as quoted sources |
| Deriving attention, backprop or building a GPT | Model internals are not needed to predict behaviour at Levels 1 to 2; expert curricula start from behaviour (postmortem cause 7) |
| Memorizing exact prices and window sizes | Volatile (Wozniak 19); dated cards for ratios, live lookup for exact numbers |
| Imagery and mnemonic tricks (Wozniak 6 to 8) | Built for lists and anatomy; this skill is mechanisms |
| Shared public Anki decks | Not tied to his runs or sources; interference with his own cards |
| Anthropomorphic pictures ("it thinks", "it searches") | Plant the category mistake the skill removes |
| Streaks and XP | Gamification weak for learning (method-effectiveness row 21) |

**Honest limits.** No study tests any of this on LLM concepts or on an adult learning alone with an AI tutor.
Physics effects came from classrooms with peers. Quantum Country data are observational and self-reported.
The LBCI is unvalidated until his wrong answers have been used to rewrite it once.
