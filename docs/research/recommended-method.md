# The recommended method

Written 2026-09-24 from the complete research base (`RESEARCH-BASE.md`). This is the evidence's answer to
"which method or combination of methods is most effective for Faiz". It is a design specification, not
yet built. Each choice names its evidence file in `curricula/` and its grade: **strong** (independent
replicated studies), **moderate** (consistent studies, some researcher-made tests), **weak** (few studies or
self-reported).

## 1. The verdict

No single method is best. The only learning products with independent evidence that they work (Khan
Academy, Cognitive Tutor, ASSISTments) all combine the same four parts, and the best AI-tutor trials add
the same guards (method-effectiveness.md, ai-tutoring.md):

1. **Expert worked solutions and hints**, prepared and checked before the session (strong).
2. **Feedback on each step that explains why**, not just right or wrong (strong: d = 0.99 vs 0.24).
3. **A mastery bar**: 9 of 10, plus a recheck 7 days later (strong for mastery; the high bar moderate).
4. **Spaced retrieval of old material, interleaved** (strong: g = 0.51 to 0.74; interleaving d = 0.79 to 0.83).

On top of these, for the judgement skills (system design, evaluation):

5. **Commit, then compare with an expert, decision by decision; a changed-fact question; a short
   after-action review** (moderate: d = 0.36 to 0.67; without the expert comparison the effect is none or
   negative) (judgement-training.md).

And for the way everything is written and delivered:

6. **The craft standard**: start with a decision not a definition; conversational plain words; one real
   case with real numbers; the rule stated after the example; nothing interesting-but-irrelevant; every
   number produced by running code, never written from memory (teaching-craft.md; conversational d = 0.30
   retention, 0.54 transfer; seductive details lower both).
7. **A fixed sequence enforced by the system, not chosen by the AI tutor in the moment** (ai-tutoring.md:
   the design choice that separated LLM tutors that helped from those that harmed).

Expected size of the whole: about 0.3 to 0.8 SD on delayed checks tied to the course, less on transfer.
Component effects overlap and do not add up. No study covers adult self-learners in AI engineering, so
every effect is carried over from other subjects (method-effectiveness.md).

## 2. One unit, in fixed order (about 25 minutes)

| Step | What happens | Evidence and source |
|---|---|---|
| 1 Recall | 3 old items, spaced (1, 3, 7, 21 days) and mixed across skills; short answer first, then options | spacing, retrieval, interleaving (strong) |
| 2 First-step test + prediction | one new problem, 90 seconds, he writes only his first step and predicts his score for the unit | Kalyuga rapid test r up to .92 (moderate); calibration as a measure |
| 3 Placement | right step and reason → skip the worked example; wrong → full worked example | expertise reversal (moderate) |
| 4 Worked example | an expert's solution showing the reason at every decision, including the rejected option and the dead end; he writes one line explaining the key step | worked examples g = 0.48, self-explanation g = 0.55, expert-reasoning capture g = 0.87 |
| 5 Completion | the same kind of problem with the last steps hidden (backward fading); feedback after each step | Renkl 2002: backward fading drives far transfer (moderate) |
| 6 His attempt | from the third problem of a type: he solves it first, with his reasons | productive failure d = 0.36 (moderate) |
| 7 Expert comparison | his answer beside the expert's, decision by decision; he writes why they differ and which is better for this brief | contrasting cases, only after he knows one method well (novices learned less from side-by-side comparison than from one method at a time) |
| 8 Changed fact | the same brief with one number changed: what moves? | case method hypotheticals, ShadowBox (weak to moderate) |
| 9 Check | 5 items at 9/10 over two checks; short answer before options; realistic wrong options; "not yet" gives new items | mastery (strong), Adesope 2017 on multiple choice |
| 10 Review | 2 lines: what I expected, what happened, why, what I will do next time | after-action review d = 0.67 (moderate) |

Steps 6 to 8 apply to the judgement skills and to any problem type he has seen worked twice.
LLM behaviour mostly skips 4 to 7 (see below).

## 3. Each skill, its method and its sources

| Skill | Method | Expert sources (nothing invented) | Checked against |
|---|---|---|---|
| **Evaluation** (core) | full ladder, slow; label real outputs before seeing the expert's labels; agreement computed | Hamel and Shreya's homework repos (Recipe Bot, Cartwheel) and worked walkthroughs; HF evaluation guidebook | expert labels (agreement, TPR/TNR), then the measured failure rate |
| **System design** (core) | 2 worked designs per problem type, then commit-and-compare with a changed fact; design from the brief before seeing ScaleDojo's missions | ScaleDojo's 24 true worked-example chapters (HLD strongest) and client briefs; system-design-primer; Anthropic agent patterns; Hello Interview Bad/Good/Great | expert design, 100-point rubric, the brief's numbers; ScaleDojo's AI review as a second opinion only |
| **Code** (core) | read and trace, then explain, then small edits; predict output; Parsons problems; find the bug with a fixed process; Prompt Problems for steering an AI assistant | CS50P weeks and problem sets; CS1-LLM order (weeks 1-4 reading and tracing); ScaleDojo Forge (hidden tests) | tests passing, then the expert solution |
| **Production** | CFA-style worked numeric solution per formula, faded fast (his strength); "which input flips the decision" | Google SRE book and workbook (error budgets, burn rates); inference cost guides | the exact number, then the expert's lever |
| **LLM behaviour** | predict, run, explain in one line; spaced recall; few worked examples (answering first beats examples for simple facts) | HF LLM Course ch. 1-2; Karpathy transcripts; Alammar-style concrete sizes | the measured run |

## 4. How ScaleDojo is used (from its measured strengths and flaws)

| ScaleDojo element | Verdict | Change |
|---|---|---|
| Weak vs strong answer pairs (358) | **best element**: contrasting cases | he writes his answer first, names the weak answer's type, then scores himself on mechanism, consequence, alternative with its cost, what to check |
| Client briefs with budget, latency, constraints | adopt | none |
| Worked-example chapters (24 true ones) | adopt as the expert answers | fade them: the second example of a type hides steps |
| Quiz bank (1,085) | **flawed**: reading only the options scores 70% (92% in LLD); 69% have absurd distractors; under 10% ask him to apply or judge | use only after rewriting: short answer first, realistic distractors, random positions |
| Chapters | passive (4% ask for a prediction) | read after his first attempt, as the explanation, not before |
| Labs | missions state the answer; last hint gives the solution | design from the brief before opening the missions; any design meeting the numbers passes |
| XP, leaderboard, certificates | skip | weak evidence; certificates reward completion, not skill |

## 5. How the tutor behaves (Claude)

- Works only from material prepared and checked before the session; the unit order is enforced by a
  script, not chosen in the moment.
- Holds the answer until he has committed or two hints have failed; stuck order: his own earlier answer,
  two options, one everyday picture, then the answer with a reason.
- Feedback on each step, at most 3 points, explaining why; stops questioning once he has it.
- Every number comes from running code; every factual claim is traceable to a source file.
- Never changes a skill's format mid-course. Changes happen only when the measures below say so.

## 6. How we know it is working

| Measure | Healthy | Alarm |
|---|---|---|
| 7-day cold recall | 80% or more | under 70% |
| 21-day cold recall | 70% or more | falling |
| Transfer task he did not train on | ScaleDojo lab 70+; 80% agreement with expert labels | below |
| Prediction gap | 10 points or less after 4 weeks | above 20 |
| First-step accuracy | rising within a task class | flat |
| Early warning | unit check above 90% but 7-day recall under 70% means it taught recognition, not learning |

## 7. What the curriculum looks like (curriculum-design.md)

- Each skill has 3 levels (novice, competent, proficient) and 4 classes of tasks of rising complexity
  (4C/ID, d = 0.79); support fades within a class and resets at the next.
- 40 concepts in a prerequisite graph, ordered by the expert consensus and weighted by job data
  (evaluation 60% of postings, agents 55%, retrieval 40%, fine-tuning 14%).
- One running product, the FBR tax assistant, grows through every module capstone and touches all five
  skills; each level ends with one outside task he did not train on (a ScaleDojo lab, HF's GAIA test).

## 8. Deliberately left out

Unstructured AI chat; open research tasks for a novice; points, leaderboards and certificates as goals;
long video or long reading as the main method; peer assessment (no peers); goal-setting exercises (no
effect in a large field test); learning styles (no support); counting "read the chapter" as progress.

## 9. Corrections applied from source checking

Novices benefit less from side-by-side comparison, so comparison comes after the expert method is known;
deliberate practice explains 14% overall and 5% in education (Macnamara 2018 correction), so repetition
alone is weak for judgement; Math Academy's 7 practice problems per example is the author's estimate
(p. 182); the other corrections are listed in `postmortem.md` section 6.
