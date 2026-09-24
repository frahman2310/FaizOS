# Post-mortem: why the FaizOS teaching system failed

Written 2026-09-24, after the research base was complete. Every claim about what happened cites the
record (`docs/learning-evidence.md`: rules C1 to C45, the session ledger, git history). Every claim about
why it failed cites the research (`docs/research/curricula/*.md`, primary sources in
`private/research-base/`). Written by the system's author, Claude, about its own design.

## The answer in one paragraph

The system failed because one AI played every role that proven courses give to separate, expert,
tested parts: it chose the curriculum, invented the teaching method, wrote the explanations and examples,
made up the numbers, set the questions, marked the answers and judged its own success. None of those
layers was anchored to an outside reference. When Faiz objected, the system patched the symptom with a
new rule instead of questioning the design, so it kept oscillating between extremes (explain everything,
then explain nothing) and grew more complicated with each fix. The research is blunt about this: the AI
tutors that helped learners had an expert solution built in and a sequence fixed by the platform; the ones
that harmed learners let the model improvise (ai-tutoring.md, section 3 and 5).

---

## 1. Fourteen teaching methods in fifty days

| # | Dates | Method | Result (ledger) |
|---|---|---|---|
| 1 | 08-06 to 08-13 | v1 "brick" modules, 20 ML modules in a week | 149 of 172 first try (87%), later found shallow |
| 2 | 08-22 | write the code from an empty file | "I don't understand a single word" |
| 3 | 08-24 | one self-explaining file with comments | passed after two fixes; "zero experience with python" |
| 4 | 09-03 | rebuilt as chat blocks plus a file | 10 of 17; "Not inside the file" |
| 5 | 09-04 | drill file, then a 300-line trace file | 1 of 3, then rejected unopened |
| 6 | 09-11 | Python bootcamp in chat | 69 of 88 (78%); "exactly what I needed" |
| 7 | 09-11 | big multi-part rounds | 35 of 45; "I will never need to write code" |
| 8 | 09-12 | one 51-question message | 5 answered; "Divide these 5 parts" |
| 9 | 09-14 | the part template | 16 of 20 with it, 3 of 11 without it the same day |
| 10 | 09-14 to 09-22 | validated scripts, decision builds | 41 of 45, 31 of 40, 31 of 40 |
| 11 | 09-22 | quality-pass template (question bank, worked chains) | L7 Round 1 |
| 12 | 09-23 | open investigation of a real system | stopped after 6 moves: "makes no sense" |
| 13 | 09-24 | staged investigation | "i don't understand this at all" |
| 14 | 09-24 | curriculum map, then per-skill methods | not yet taught |

The method changed on average every 3.6 days. Every framework course studied keeps one format for every
unit (teaching-structure.md, pattern A6), and the teaching literature lists "changing the unit format
between units" as a known cause of drop-out (Part C). He named it himself on 09-14: "The method is
inconsistent, you keep deviating, its incoherent and haphazard" (C28).

## 2. The root causes

### Cause 1. The AI designed the pedagogy as it went
Every method in the table was invented in the conversation, usually in response to the last complaint.
The rulebook reached 251 lines and 45 rules he had to state, several of which contradicted each other:
"make the lessons longer" (C6) against "hate long files" (C21); "I modify working code" (C14) against
"I will never need to write code" (C24) against "code needs to be learnt" (C44); "just build" (C37)
against "I don't mind predicting" (C39), superseded the same day.
- **Evidence:** in the controlled LLM-tutor studies, the design choice that separated help from harm was
  that "a platform, not the prompt, fixed the order of steps" (ai-tutoring.md). OpenAI says its own
  prompt-based study mode gives "inconsistent behavior" across conversations. Proven courses are designed
  once, by teaching experts, and refined on thousands of learners (teaching-structure.md).
- **Why it happened:** the system had no borrowed structure to return to, so each correction became a new
  local rule rather than a question about the design.

### Cause 2. One method for five different kinds of skill
Until 09-24 every skill was taught the same way: explain, then five questions. Then, overcorrecting,
everything became open investigation. Faiz diagnosed this himself (C44, handwritten notes): evaluation,
system design and code are applied and core, LLM behaviour is understanding, production is applied maths.
- **Evidence:** facts, concepts, procedures and judgement are learned by different methods (skill-methods.md
  section A). Worked examples beat problem solving for complex material, but answering first beats worked
  examples for simple facts, and the effect flips as expertise grows (Chen, Kalyuga and Sweller 2015,
  element interactivity: d = .65 one way, d = .96 the other). Judgement is trained by committing to a
  decision and comparing it with an expert's, decision by decision (judgement-training.md), which the
  explain-then-quiz format never did.

### Cause 3. His own reasoning was designed out, then left unsupported
In the lesson format he only answered questions whose answers I already held. Build decisions were
multiple choice with my key; "decisions cannot be this obvious" (C35). He said it directly: the system
was "suppressing the use and development of my cognitive ability" (C40, C44). The investigation then went
to the opposite extreme: a real system, no frame, no worked example, no expert answer to compare against.
It failed within six moves (C41 to C43).
- **Evidence:** attempting before being taught builds deeper understanding (Kapur 2014: equal procedural
  knowledge, better conceptual understanding d = 2.00 and transfer d = 1.52), but only when the attempt is
  followed by comparison with expert solutions or teaching built on the attempt (Loibl, Roll and Rummel
  2017: without that, "no or negative effects"). Minimal guidance underperforms for novices (Kirschner,
  Sweller and Clark 2006). The lessons had comparison without attempt; the investigation had attempt
  without comparison. Neither had both.

### Cause 4. No expert material: the AI wrote everything, including the numbers
Explanations, examples, pictures, scenarios and build "givens" were all written by me. The builds ran in
"modelled worlds" with invented rates (93% catch, 2% false alarm); in L6 two of my own givens contradicted
each other (Decision 3 vs 4). My lesson script on meaning search predicted it would beat word search; the
first real measurement showed the opposite. Research digests I produced contained citation errors that the
checking agents later caught (the 80% vs 36% figure, the "53 studies", "similar gains").
- **Evidence:** plain GPT-4 made logic errors in 42% of solutions in the Bastani trial, and students did not
  notice they had learned less (ai-tutoring.md). Experts leave out about 70% of their own decision steps when
  they teach; training built from captured expert reasoning scored g = 0.87 (curriculum-design.md). The fix
  in both literatures is the same: expert-authored, checked material prepared before the session.

### Cause 5. It measured what was easy, not what matters
Progress was counted as first-try accuracy on my own questions, and skills were "banked" by rows in a
database: 66 ML skills marked understood after one week. There were no delayed retention checks, no
transfer tests on unseen problems, no outside benchmark, and the pass bar was 4 of 5 on one check.
- **Evidence:** tests written by the teacher show about three times the effect of independent tests (0.84 vs
  0.27, curriculum-design.md). Mastery learning works best with a 91 to 100% bar and a delayed recheck
  (0.64 vs 0.44 to 0.49). The checker enforced features of the message (sentence counts, character limits,
  a regular expression for "Worked chain") rather than whether he learned, so the system got better at
  producing compliant messages, not at producing learning.

### Cause 6. "No repetition" was applied as "no retrieval"
He said "i just don't like repitition" (C27) and "ik this dont repeat" (C22), meaning: do not re-teach
what I know. The system turned that into never returning to old material, so spaced review and
interleaving, the two best-evidenced techniques, were absent from lessons. A review database existed but
chat teaching never used it.
- **Evidence:** practice testing and distributed practice are the only two techniques rated high utility
  (Dunlosky et al. 2013). Interleaved practice: 74% vs 42% a month later (Rohrer 2015), 61% vs 38% in a
  787-student trial (Rohrer 2020). The distinction the system missed: re-testing is not re-teaching.

### Cause 7. The curriculum was invented, not derived
The course was planned by me three times (20 modules of ML theory, then 20 lessons, then 11), aimed at
"covering" 133 skills at 5% per lesson. Week one taught FlashAttention, FSDP and GRPO to someone who had
never programmed.
- **Evidence:** expert AI-engineering curricula agree on an order (16 stages, expert-curricula.md) that
  starts from how LLMs behave and evaluation, not model internals. Job data: fine-tuning appears in 13.8%
  of AI-engineer postings, evaluation in 59.7%, agents in 55.4% (curriculum-design.md). Whole tasks in
  classes of rising difficulty (4C/ID, d = 0.79) is the best-evidenced way to sequence, and coverage is not.

### Cause 8. Building the system crowded out learning
FaizOS grew to 5 hooks, 7 scripts, 3 agents, 39 MCP tools, 20 database tables and about 220 commits, most
of them about the teaching machinery. Much of his time went into diagnosing the teacher rather than
learning the subject; he eventually said "Edtech is complex and layered. We have no knowledge of it"
(09-24).
- **Evidence:** proven platforms separate the product from the learner's time; completion depends on a
  fixed rhythm and visible end (teaching-structure.md Part C, "no end in sight" is Launch School's biggest
  source of anxiety).

## 3. Why it kept happening: the feedback loop optimised the wrong target

The reflect loop was built to learn from his answers, but in practice it learned from his complaints.
Each complaint became a rule; each rule became a check; each check shaped the next message. That loop
optimises for his satisfaction with the last message, which is a real signal but a lagging and local one,
and it has no view of the outcome that matters: can he, a week later, do a task he was not trained on?
Because nothing measured that, the system could not tell a better method from a more comfortable one, and
it swung between opposites. The research-grounding came late (from 09-22) and was at first used to
justify designs already chosen rather than to choose them.

## 4. What worked, and survives

| What | Evidence it worked |
|---|---|
| Short questions in one steady rhythm (bootcamp) | 69 of 88; "this is exactly what I needed" |
| The part template (problem, fix, example, picture, paths, questions) | 24 of 30 vs 3 of 11 without it the same day (A12, A13) |
| Decisions with numbers and trade-offs | "I liked the build part" (C32) |
| Plain words and the glossary gate | jargon complaints stopped after C33 |
| Pointing at his own earlier answer when stuck | 15 of 17 (D1) |
| Two-option rewording for direction questions | 3 of 3 in L7 after 0 of 3 open (E12) |
| Real data and real measurement | the case-01 lab contradicted my prediction, which is the point |

## 5. What the evidence says the system must be instead

1. **Borrow the curriculum and the method; the AI does not design either.** Order from expert curricula
   and job data; structure from 4C/ID and mastery learning; per-skill methods from skill-methods.md.
2. **Five skills, five methods** (C44), with worked examples as the backbone for the applied three (C45):
   worked example, completion, backward fading, independent problem, new variation.
3. **Attempt, then compare with an expert, every time his judgement is trained**: commit, write the reason,
   see the expert decision by decision, answer a changed-fact question, short after-action review
   (judgement-training.md).
4. **Expert material, prepared and checked before the session.** Worked examples from ScaleDojo (30
   worked-example chapters), Hamel and Shreya's homework, Hello Interview, CS50P, SRE, CFA-style problems.
   The AI only cuts the in-between rungs from them and names the source.
5. **A fixed sequence enforced by the system, not chosen by the AI in the moment.**
6. **Measure learning, not messages:** 90% bar, a delayed recheck at 7 days, a first-step placement test,
   an outside task per level, and his prediction of his own score before each check.
7. **Spaced retrieval and interleaving built in**, kept separate from re-teaching.
8. **Small machinery.** A tracker and a schedule, not a new rule for every complaint. Rules change only
   when the measured outcome says so.

## 6. Corrections to earlier research found while checking sources

- The "80% vs 36%" recall figure is Karpicke and Roediger 2008, not Roediger and Karpicke 2006.
- The Sinha and Kapur meta-analysis figure is 166 comparisons (d = 0.36, up to 0.58 with fidelity); "53
  studies" is not in the source.
- Chen, Kalyuga and Sweller 2015 used immediate tests only.
- Kalyuga's rapid first-step test cuts test time by 3.2 to 4.9 times (not 2.5), correlation up to .92.
- Rittle-Johnson and Star 2007: comparison improved procedural flexibility; conceptual knowledge showed no
  difference (not "similar gains").
- Schwartz and Bransford 1998: one condition beat three separate controls, not a two-arm comparison.
- Bloom's 2 sigma does not replicate; tutoring is worth about 0.3 to 0.8 SD.
- Math Academy page references: pp. 75-76 (structure, fail-twice), 183 (7 practice problems per example),
  397-398 (2 to 5 questions per step), 218-223 (subgoal labels, expertise reversal); its efficiency and
  pass-rate figures are self-reported.
