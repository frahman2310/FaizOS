# How judgement professions train judgement, and what the design and evaluation tracks should borrow

Written 2026-09-24. Question: professions that live on judgement (medicine, business, law, architecture,
aviation, the military, chess, software) cannot hand trainees a formula. How do they train it, one session
at a time, and what is the evidence? His words set the target: system design is "logic build-up +
cognitive development", evaluation is "logic + understanding + methods". His two findings set the limits:
explain-then-quiz "suppressed the use and development of my cognitive ability", and a fully open
investigation with no structure failed. Worked examples are his reference point.

Does not repeat: ../teaching-methods.md (self-explanation, contrasting cases, prediction, productive
failure, erroneous examples, retrieval, spacing), teaching-structure.md (unit template), skill-methods.md
(worked-example ladder, the system-design frame in C3, the evaluation anatomy in C1, deliberate practice
meta-analysis numbers). This file adds how the judgement professions run a session, and turns that into a
session design for the two tracks.

Tags: **[M]** measured (study with numbers). **[S]** stated (the method's authors or institution describing
it, or a claim without numbers). **[M-dev]** measured, but by the method's own developers.

---

## 1. Cognitive apprenticeship (Collins, Brown and Newman; Collins, Brown and Holum 1991)

**The idea.** In a craft apprenticeship the work is visible; in school, thinking is invisible. So "the
teacher's thinking must be made visible to the students and the student's thinking must be made visible to
the teacher" [S] https://www.psy.lmu.de/isls-naples/intro/all-webinars/collins/cognitive-apprenticeship.pdf

| Method | What it means in practice | Group |
|---|---|---|
| Modelling | Expert does the task while saying the usually hidden heuristics and control decisions out loud (reading aloud in one voice, commenting in another) | Core |
| Coaching | Expert watches the learner do the task and gives hints, feedback, reminders, new tasks | Core |
| Scaffolding and fading | Expert does the parts the learner cannot yet do, then withdraws; needs an accurate read of the learner's level | Core |
| Articulation | Learner has to say his reasoning (inquiry questions: "why is this summary good and that one poor?") | Focus |
| Reflection | Learner compares his process with the expert's, using an "abstracted replay" that shows only the critical decisions | Focus |
| Exploration | Learner sets and solves his own problems; exploration strategies are taught, not assumed | Autonomy |
Sequencing: global before local (see the whole task first), increasing complexity, increasing diversity. Same source [S].

**One session, start to finish (Schoenfeld's college maths problem-solving course, as described by Collins et al.):**
1. Students bring hard problems; at the start of class he tries one cold, thinking aloud, sometimes floundering, so they see dead ends and recovery, not just the clean path.
2. Collective solving: students generate options; he manages which option to pursue and when to switch (he holds the control decisions, they hold the moves).
3. Small groups solve; he circulates as consultant asking only three questions: **what are you doing, why are you doing it, how will success at it help you solve the problem?** Students start asking these of themselves (fading).
4. Postmortem: he recounts the solution as an abstracted replay (heuristics used, where alternatives were generated, why one was chosen), then students do the same for their homework and the class compares student and expert processes.
Source: same PDF [S].

**Evidence.** Reciprocal teaching (the reading version: teacher models questioning, summarising,
clarifying, predicting, then hands the teacher role to students): comprehension rose from 15% to 85%
accuracy after about 20 sessions, still 60% six months later [M, as reported in Collins et al.] same PDF.
Review of 16 studies: median effect 0.32 on standardised tests, 0.88 on experimenter tests [M]
https://eric.ed.gov/?id=EJ500529 . Whole-framework effects are not measured as one package; the evidence is
for its parts [S].

---

## 2. Medicine: training clinical judgement

| Method | How it runs | Evidence |
|---|---|---|
| **Illness scripts** | Experts store diseases as scripts: enabling conditions, the fault, the consequences (signs). Teaching makes students build and compare scripts for look-alike diseases | Theory well supported; produced the script concordance test [S] https://pubmed.ncbi.nlm.nih.gov/25180878/ |
| **Script concordance test (SCT)** | "If you were thinking of hypothesis X, and you now find Y, X becomes..." rated -2 (almost ruled out) to +2 (almost certain). Credit is given in proportion to how many panel experts chose that answer, so partial credit exists where experts disagree | Format [S] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6002295/ ; review: good internal consistency, weak evidence on response process and on effects on learning [M/S] https://pubmed.ncbi.nlm.nih.gov/21401680/ ; can be gamed by always answering 0 [S] PMC6002295 |
| **Structured (deliberate) reflection** | Learner gives a first diagnosis, then fills a table: findings that support it, findings against it, findings expected but absent; then lists alternatives and repeats the table for each; then ranks | Year 4 students, n = 46: reflection scored lower immediately (0.48 vs 0.61 and 0.62) but higher one week later (0.66 vs 0.52 and 0.48); only the reflection group improved from immediate to delayed test [M] https://pubmed.ncbi.nlm.nih.gov/22515754/ . Procedure [S] https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/medu.13829 |
| **Modelled reflection** | Learner studies a worked-out reflection table by an expert on one case, then reflects on the next | Years 5 and 6, n = 115: modelled and cued reflection beat free reflection, with less effort [M] https://pubmed.ncbi.nlm.nih.gov/25039736/ . Year 3 novices, n = 80: modelled reflection did not beat free reflection, and all groups scored very low on related unstudied ("adjacent") diseases [M] https://pubmed.ncbi.nlm.nih.gov/30917406/ |
| **Reflection against availability bias** | Residents saw cases, then look-alike cases with different diagnoses | Second-year residents made more errors on look-alikes (1.55 vs 2.19 of 4); reflection raised accuracy on them to 2.03 to 2.31 [M] https://pubmed.ncbi.nlm.nih.gov/20841533/ |
| **SNAPPS (learner thinks aloud to the expert)** | Learner presents a case in six steps: Summarise, Narrow the differential, Analyse it, Probe the preceptor about uncertainties, Plan, Select an issue for self-study | Randomised, 64 students: SNAPPS group expressed more reasoning and uncertainty in every outcome category, presentations no longer [M] https://pubmed.ncbi.nlm.nih.gov/19318792/ |
| **Deliberate practice with feedback (Ericsson)** | Coach-designed tasks at the edge of ability, immediate feedback, repetition. Experience alone is weakly linked to performance | [S] https://pubmed.ncbi.nlm.nih.gov/18778378/ . 32 of 62 evaluations found quality falls with years in practice; only 2 found it rises [M] https://pubmed.ncbi.nlm.nih.gov/15710959/ . Simulation with deliberate practice vs traditional clinical teaching, 14 studies: effect 0.71 [M] https://pmc.ncbi.nlm.nih.gov/articles/PMC3102783/ |
| **Case-based learning** | Small groups work a patient case, learning science around it | 104 papers: students and teachers like it; effect on learning vs other methods "inconclusive" [M, review] https://pubmed.ncbi.nlm.nih.gov/22578051/ |
| **Morbidity and mortality conference** | Case of a bad outcome presented briefly, the decision points and what could be improved discussed without blame, follow-up actions tracked | 59 studies, average quality 6.7 of 18; preparation and follow-up matter as much as the discussion [M, review] https://pubmed.ncbi.nlm.nih.gov/37851458/ |

**One session (structured reflection, as run in the Mamede experiments):** read a case, write a first
diagnosis quickly, fill the support / against / expected-but-absent table, list alternatives and fill the
table for each, rank, then see the correct diagnosis. Later sessions test new cases of the same diseases a
week later. Lesson for us: the method **costs accuracy today and pays a week later**, so judge it on delayed
tests, not on how the session felt.

---

## 3. Business and law: the case method and the Socratic method

**HBS case method, one class.** Before class: a 10 to 20 page case "written from the viewpoint of a real
person leading a real organization", ending at "a key decision to be made"; individual preparation, then a
small discussion group in the morning [S] https://www.hbs.edu/mba/academic-experience/the-case-method .
In class (80 minutes): the instructor frames the session, then cold calls one student to open with a broad
question about the crux of the case; the opening answer can run 1 to 10 minutes; the instructor plans key
questions for each segment in advance and steers with follow-ups that "dig into the logic and evidence" or
"spotlight differing viewpoints"; students do most of the talking [S]
https://www.hbs.edu/teaching/case-method/leading-in-the-classroom/Pages/Cold-Calling.aspx . About 500 cases
over two years [S] (HBS page above). Christensen's frame: the teacher's three skills are questioning,
listening and responding [S] https://www.hbs.edu/faculty/Pages/item.aspx?num=4884 .

**Law, one class (case-dialogue / Socratic).** The professor calls on a student to summarise an assigned
case (facts, issue, holding, reasoning), questions the gaps, then changes the facts into hypotheticals and
asks whether the outcome changes; the skill is spotting which facts are legally decisive [S]
https://www.usnews.com/education/best-graduate-schools/top-law-schools/articles/2019-04-04/what-is-the-socratic-method-and-why-do-law-schools-use-it .
The Carnegie report calls it law's signature pedagogy: it "drills students, over and over, in first
abstracting from natural contexts, then operating upon the facts so abstracted" by rules, but leaves out
real context, consequences and ethics [S]
https://archive.carnegiefoundation.org/publications/pdfs/elibrary/elibrary_pdf_632.pdf .

**Evidence.** No controlled study of the MBA or law versions was found. Nearby measured evidence: case
studies beat other delivery on exam questions in a biology course [M]
https://pubmed.ncbi.nlm.nih.gov/25949753/ ; high-school case-method courses raised civic interest vs
comparison courses [M-dev] https://www.hbs.edu/case-method-project/Pages/default.aspx . Treat both methods
as **proven formats with weak outcome evidence**. What they contribute that is testable: commit to a
decision before discussion (cold call), and **change one fact and ask what changes** (hypotheticals).

---

## 4. Architecture and design: the studio and the crit

**Forms.** Desk crit (one to one at the student's desk, frequent, on work in progress), pin-up (work on the
wall, peers and tutor comment), and interim and final juries with outside critics [S]
https://www.jonkolko.com/phd/writing/25-09-08-the-style-and-goals-of-design-critique-pedagogy ; the desk crit
is the core teaching event [S]
https://www.cambridge.org/core/journals/ai-edam/article/abs/design-studio-crit-teacherstudent-communication/B63767DF1732146A648F0D6BC41CD88D .

**One desk crit (Schön's Quist and Petra).** Petra shows her stuck school design. Quist lays tracing paper
over **her** drawing and redraws it while talking, reframing the problem, testing moves and reading their consequences, so she sees the reasoning applied to her own
work rather than to a fresh expert design [S]
https://punyamishra.com/wp-content/uploads/2017/09/schon-reflective-conversation.pdf .
Schön's line: the student "cannot be taught what he needs to know, but he can be coached" [S].

**Evidence.**
| Finding | Source |
|---|---|
| Crits are often experienced as high stress, with fear and humiliation reported | [S] Kolko, above |
| Parallel beats serial: 33 novices made 5 prototype ads; getting critique on several at once (parallel) beat critique after each one (serial) on click-through and expert ratings, gave more diverse designs and a rise in self-efficacy; nearly half of serial participants reacted badly to critique, no parallel ones did | [M] https://aaalab.stanford.edu/assets/papers/2010/Parallel_Prototyping_leads_to_better_design_results.pdf |
| People shown one design rate it higher and criticise less than when it sits among three alternatives | [M] https://www.billbuxton.com/rightDesign.pdf |
| Calibrated peer review (Stanford HCI MOOC): students grade staff-graded samples, see the staff grade and reason, repeat until close (up to 5), then grade peers and self. 42.9% of grades within 5% of staff, 65.5% within 10%; self-grades 7% above staff; feedback on one's grading bias improved later accuracy | [M] https://hci.stanford.edu/publications/2013/Kulkarni-peerassessment.pdf |

Lesson: critique works best **on several options at once**, with the critic working on the learner's own
artefact, and judging skill itself can be trained by **calibration against expert grades**.

---

## 5. Aviation and the military

| Method | How it runs | Evidence |
|---|---|---|
| **After-action review (AAR)** | Facilitated, after every event, four parts: what was supposed to happen, what actually happened (gather every viewpoint), why the difference, what to sustain and what to change. Not a critique: participants "self-discover" and learn more than from one viewpoint | [S] https://pinnacle-leaders.com/wp-content/uploads/2018/02/Leaders_Guide_to_AAR.pdf . 46 samples, N = 2,136: debriefs improve performance about 25% (d = 0.67); stronger with alignment, facilitation and structure [M] https://pubmed.ncbi.nlm.nih.gov/23516804/ |
| **Recognition-primed decision (Klein)** | Not a training method but a finding about judgement: 26 fireground commanders, 156 decision points; over 80% were made by recognising the situation as typical and taking the typical action; under 12% compared options | [M] https://journals.sagepub.com/doi/10.1177/154193128603000616 . Implication: judgement is built from many recognised cases plus the cues that mark them |
| **ShadowBox** | A scenario stops at decision points. Trainee ranks the options (or priorities, or cues to watch) and writes the reason. Then sees the expert panel's ranking **and reasons**, and reflects on the gap. No expert needs to be in the room | Marines, 3 hours, paper, N = 59: 28% closer match to experts than control; soldiers, 1 hour, tablet: 21%; firefighters: about 18% [M-dev] https://journals.sagepub.com/doi/10.1177/1555343416636515 ; https://www.psychologytoday.com/us/blog/seeing-what-others-dont/202105/shadowbox-training-making-better-decisions |
| **Think Like a Commander (US Army)** | Short tactical vignettes repeated as "cognitive battle drills": the officer analyses the situation, then models his understanding and decisions on expert tacticians' thinking patterns | Significant gains in rapidly identifying the critical information needed for a decision [M, Army Research Institute; effect sizes not read] https://apps.dtic.mil/sti/tr/pdf/ADA428347.pdf |
| **Tactical decision game** | A map and a few paragraphs; something unexpected happens; about 2 minutes to give orders; then sketch the plan and defend the reasoning | [S] https://en.wikipedia.org/wiki/Tactical_decision_game ; https://www.mca-marines.org/gazette/designing-good-tdgs/ |
| **Scenario-based flight training** | Manoeuvres taught inside realistic flights with decisions, not as isolated drills | 30 student pilots (groups self-selected, not random): scenario group better on 6 of 7 measures, 3.1 fewer aircraft hours [M, weak design] https://www.faa.gov/sites/faa.gov/files/training_testing/training/fits/research/SBT_final.pdf |

---

## 6. Chess: master games and "guess the move"

**One session (solitaire chess / guess the move):** take a master game, cover the moves, play the winner's
side; at each move write your choice (and your reason), then uncover the master's move; score it (master
move full credit, reasonable move partial); where you differ, analyse why the master's move is better
[S] https://www.mark-weeks.com/aboutcom/aa05f18.htm ; https://ignitechess.com/guess-the-move .

**Evidence.**
- 2 samples of rated players (n = 375 combined): **serious study alone** was the strongest predictor of rating; grandmasters logged about 5,000 hours of it in their first decade, about 5 times intermediate players; all activities together explained about 40% of rating variance. Serious study is chosen to "discriminate between stronger and weaker solutions" to the same position, which tournament play cannot offer [M, correlational] http://www.chrest.info/Fribourg_Cours_Expertise/Articles-www/II%20Donnees%20empiriques/CharnessEtal2005ACP.pdf
- Reanalysis: deliberate practice explained about 34% of chess variance, so most variance lies elsewhere [M] https://gwern.net/doc/psychology/chess/2014-hambrick.pdf
- De Groot: stronger players did not look at more moves, only better ones [S, summarised] https://www.scientificamerican.com/article/the-expert-mind/

Chess is the cleanest version of the pattern: **the learner commits, then compares against an expert
choice, one decision at a time, on a real game**.

---

## 7. Software engineering: how the trade trains design judgement

| Practice | How it trains judgement | Evidence |
|---|---|---|
| **Code review** | Reviewer comments on a concrete change; at Google, review was introduced for education and readability; average comments per change fall as engineers gain experience | [M, interviews and logs] https://sback.it/publications/icse2018seip.pdf . At Microsoft (873 programmers surveyed): reviews find fewer defects than expected and deliver knowledge transfer and alternative solutions instead [M] https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/ |
| **Design docs and design review** | Sections: context and scope, goals and non-goals, the design, **alternatives considered**, cross-cutting concerns. Review brings "the combined experience of the organization" into a design early; authors re-read their docs a year or two later | [S] https://www.industrialempathy.com/posts/design-docs-at-google/ |
| **Architecture decision records (ADRs)** | One short record per decision: title, status, context, decision, consequences. One record's consequences become the next one's context | [S] https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html |
| **Blameless postmortems** | Written after incidents: impact, root causes, actions, reviewed by seniors. Learning uses: postmortem of the month, reading clubs on old incidents, and **Wheel of Misfortune**, where new engineers role-play a past incident | [S] https://sre.google/sre-book/postmortem-culture/ |
| **Pairing** | Two engineers on one task | 18 studies: small quality gain, and the gain is on complex tasks at higher effort [M] https://www.sciencedirect.com/science/article/abs/pii/S0950584909000123 |
| **Synthesis from real decisions** | "Write five design documents, and pull the similarities out": strategy is induced from concrete designs | [S] https://lethain.com/good-engineering-strategy-is-boring/ |

How seniors learned system design, as the trade itself describes it: by writing and defending real design
docs, reading others' docs and postmortems, and being reviewed [S, sources above]. No controlled study of
system-design teaching was found. The artefacts (design doc with alternatives, ADR, postmortem) are the
usable part: they are **reasoning written down at the decision level**.

---

## 8. Synthesis

### 8a. The shared structure
Every profession above runs some version of the same loop:

| Step | Medicine | Business / law | Design | Aviation / military | Chess | Software |
|---|---|---|---|---|---|---|
| 1 Realistic case with a decision | Patient case | Case ending at a decision | Brief | Scenario / vignette | Master game | Incident, design brief |
| 2 Learner commits first | First diagnosis, SNAPPS | Cold call | Own drawing | Rank options, give orders | Guess the move | Draft design doc |
| 3 Reasoning made explicit | Reflection table | Defend under questioning | Talk through the drawing | Write reasons | Write reason | Alternatives considered |
| 4 Compare with expert reasoning, per decision | Correct diagnosis, modelled reflection | Instructor steering | Critic redraws on your work | Expert ranking and reasons | Master's move | Review comments |
| 5 Vary a fact | Look-alike cases | Hypotheticals | Alternatives in parallel | Unexpected event | New position | What-if in review |
| 6 Structured reflection | Delayed retest | Wrap-up | Next iteration | AAR 4 questions | Analyse the gap | Postmortem actions |
| 7 Harder, more varied case | New diseases | Next case (500) | Next project | Next scenario | Next game | Next system |

Two findings from the evidence change how the loop is run:
1. **Judgement is mostly recognition of typical cases and their cues** (Klein, over 80%; illness scripts; chess chunks). So volume of varied cases matters, and the expert's reasoning must be shown as **cue → what it means → what to do**, not only as the final answer.
2. **Experience without feedback does not build it** (Choudhry, 32 of 62; Ericsson). The comparison against expert reasoning, per decision, is the active part (ShadowBox 18 to 28%; debriefs d = 0.67; calibration in Kulkarni).
And one warning: look-alike cases cause confident errors (Mamede 2010), so the case set must include
look-alikes with different answers, with the reflection table as the fix.

### 8b. Making the tutor's reasoning visible without handing over the answer
| Technique | What the tutor does | From |
|---|---|---|
| Commit, then reveal | Nothing expert is shown on this case until he has written his choice and reason | ShadowBox, HBS cold call, guess the move |
| Reveal per decision, not per solution | At decision point 1, show the expert's ranking and reason for that point only; he then continues to point 2 | ShadowBox, guess the move |
| Model on a parallel case | Tutor thinks aloud through case A (same structure, different surface); he does case B | Collins modelling, Mamede modelled reflection |
| Process questions, not content hints | When stuck, only: what are you doing, why, how will it help? | Schoenfeld |
| Expert works on his draft | Tutor edits his design in place, narrating each change and its reason, rather than showing a separate expert design | Schön (Quist and Petra), code review |
| Show the cues | Tutor names what he noticed in the brief or trace that triggered each move ("p95 of 800 ms rules out a second LLM call") | Klein, ShadowBox, illness scripts |
| Show dead ends | Tutor's worked reasoning includes one option tried and dropped, with why | Schoenfeld |
| Abstracted replay | After the reveal, a 3 to 5 line replay of only the decisive choices | Collins |
| Partial credit where experts differ | Grade against a spread of expert answers, not one key | SCT |

### 8c. System-design track: one session (35 minutes)
Uses the fixed frame and worked-example ladder in skill-methods.md C3; this is how a session inside it runs
once he is past the first two worked examples. Tutor prepares: brief with numbers, 3 decision points each
with 3 to 4 options, expert ranking and reason per point, one parallel case, one changed fact.

| Min | Step | What happens | From (evidence tag) |
|---|---|---|---|
| 0-3 | Case | Brief written as a protagonist with a decision and numbers ("support lead at a 50,000-ticket-a-day firm must choose...") | HBS case [S]; scenario training [M, weak] |
| 3-5 | Cold open | He writes the one number or constraint that will drive the design, and why | HBS cold call [S]; SNAPPS "narrow" [M] |
| 5-17 | His design | He fills the frame. At each of the 3 decision points he ranks the options and writes one reason and the cue he used. Tutor only asks Schoenfeld's three questions if he stalls | ShadowBox [M-dev]; Schoenfeld [S] |
| 17-25 | Reveal, per decision | For each point: expert ranking, the cue, the reason, and one dropped option. Then tutor edits **his** design in place, narrating each change. Nothing is shown before he commits | ShadowBox [M-dev]; Quist and Petra [S]; Tohidi, several options compared [M] |
| 25-30 | Change one fact | "Tenant data must never cross, and budget halves." Which components change, which stay, why? He answers first, expert after | Law hypotheticals [S]; tactical decision game [S]; Think Like a Commander [M] |
| 30-35 | AAR | Four lines: what I expected the design to be, what the expert design was, why they differ, what I keep and change. Then one "cue → move" rule into the spaced queue (for example "multi-tenant plus retrieval → filter by tenant before ranking") | AAR [M, d = 0.67]; illness scripts as cue rules [S] |
Next session: harder or more varied brief, and every 4th brief is a look-alike with a different right
answer, done with the reflection table (evidence for my design, against it, what I would expect to see if it
were right but do not, the alternative). Judge progress by a cold brief a week later, not in-session
feelings (Mamede 2012 [M]).

### 8d. Evaluation track: one session (35 minutes)
Uses the method in skill-methods.md C1 (read, note, group, count, turn into a check, measure the checker).
Tutor prepares: 25 real traces from one product with expert pass/fail labels and one-line reasons, 4
SCT-style items, one decision the analysis feeds.

| Min | Step | What happens | From (evidence tag) |
|---|---|---|---|
| 0-2 | Case | The product, the decision ("ship to 5 more clients or not"), the cost of one failure | HBS case [S]; M&M framing [S] |
| 2-7 | Calibrate | He labels 3 expert-labelled traces one at a time; after each he sees the expert label and reason. If he disagrees on 2 or more, 2 more calibration traces | Calibrated peer review [M] |
| 7-19 | Label | 15 traces: pass/fail plus a free-text note. For 3 traces he marks as hard: the reflection table (evidence for fail, against, expected but absent, alternative failure type) | Hamel's open coding (C1); structured reflection [M] |
| 19-24 | Judgement items | 4 SCT items: "You think the failure is retrieval. New fact: the right chunk was ranked 3rd of 5. Retrieval as cause: -2 to +2?" Scored against the expert spread with the reason | Script concordance test [M/S] |
| 24-31 | Compare | His agreement with the expert labels as a number (and his bias: too lenient or too strict). Then only the disagreements, each with the expert's cue and reason. He writes for each: whose label is right and why | ShadowBox [M-dev]; Kulkarni bias feedback [M]; Collins reflection [S] |
| 31-35 | AAR | What I expected the failure rate to be, what it was, why the gap, what I change in how I label. One "cue → label" rule into the spaced queue | AAR [M]; illness scripts [S] |
Next session: same product with a new batch (agreement should rise), then a new product. Every few weeks
the case is a published evaluation failure run as a Wheel of Misfortune: he gets the traces the team had,
makes the call, then reads what actually happened [S, Google SRE].

### 8e. Why this answers his two findings
- Old system suppressed his thinking: in both sessions he commits a ranked choice, a reason and a cue before any expert reasoning appears, every time.
- Open investigation failed: the case, the decision points, the frame, and the expert reasoning to compare against are all fixed in advance; the only open part is his own reasoning.
- Worked examples stay: the parallel modelled case and the per-decision reveal are worked examples cut into pieces he meets after committing.

---

## Gaps and limits
- No controlled study was found for the HBS case method, law's Socratic method, the studio crit, or system-design teaching itself; those formats are used here for their structure, and every session element leans on a measured method from another field.
- ShadowBox numbers come from its developers and small samples; the Army and FAA studies are small and not all randomised.
- Case-based learning in medicine: learning effect inconclusive (BEME review). The measured gains come from specific moves inside cases (reflection, modelled reflection, debriefing), which is what the sessions use.
- For true novices (Mamede 2019) modelled reflection did not beat free reflection; the reflection table should come after the first worked examples, not before.
- Mamede 2012 and SCT are medical; the transfer to trace labelling is by analogy, not tested.
- Not read in full: the Think Like a Commander effect sizes (DTIC server refused connection); Schön's book (the Quist and Petra account is from a chapter excerpt).
