# The research base

Completed 2026-09-24. Two layers: **findings** (committed here, in `docs/research/`) and **sources**
(third-party full texts and repos, kept locally in `private/`, git-ignored, never published).

## Findings (read these first)

| File | Question it answers |
|---|---|
| `structures/INTEGRATED.md` | **The final specification: five skill structures, one shared layer, start order, the week** |
| `structures/{code,llm-behaviour,production,evaluation,system-design}.md` | One structure per kind of learning, each from its own experts |
| `structures/review.md` | The independent review that tested the five for optimality |
| `recommended-method.md` | **The answer: the most effective combination of methods, per skill, with sources and measures** |
| `postmortem.md` | What went wrong with FaizOS's teaching system, and why, against all of the research below |
| `curricula/method-effectiveness.md` | Every teaching component ranked by evidence (effect sizes, independent vs researcher-made tests); platforms decomposed |
| `curricula/scaledojo-method-analysis.md` | ScaleDojo measured from its own content: chapters, 1,085 quiz items, 358 answer pairs, labs; adopt, change or skip |
| `curricula/teaching-craft.md` | 28 craft techniques from Khan Academy, 3Blue1Brown, CS50, Karpathy, Alammar and others; a 20-item explanation standard |
| `curricula/curriculum-design.md` | What to teach, in what order, to what level; prerequisite graph of 40 concepts; levels and milestones per skill; job data |
| `curricula/skill-methods.md` | The proven method for each of the five skills, the worked-example ladder, fading rules, the week |
| `curricula/judgement-training.md` | How professions train judgement (medicine, business, law, design, aviation, chess, software) and 35-minute session designs for system design and evaluation |
| `curricula/ai-tutoring.md` | How an AI tutor should behave, from controlled studies; what separated tutors that helped from tutors that harmed |
| `curricula/teaching-structure.md` | How the best-evidenced courses structure a unit; what not to do |
| `curricula/expert-curricula.md` | The order 16 expert AI-engineering curricula agree on |
| `curricula/huggingface.md` | Every Hugging Face course, unit by unit, with fit ratings |
| `curricula/scaledojo.md` | The ScaleDojo platform, course and labs |
| `curricula/curriculum-map.md` | The draft map (v2): five skills, five methods, 12 modules. To be revised against curriculum-design.md before use |
| `teaching-methods.md`, `adaptation.md` | The first research pass (09-22), partly superseded by the files above |

## Sources (local, private)

| Folder | Files | Words | What it holds |
|---|---|---|---|
| `private/scaledojo/` | 538 | 344,467 | All 356 chapters of 5 courses; 1,085 quiz questions with answers and explanations; 358 weak/strong answer pairs; 6 lab level lists; unlocked level details; 181 public pages (wiki, 124 blog posts, papers). Index: `INDEX.md` |
| `private/research-base/evaluation/` | 202 + 7 repos | 444,428 | Hamel Husain, Shreya Shankar, Eugene Yan, Anthropic, OpenAI, HF evaluation guidebook, the course homework repos (Recipe Bot, Cartwheel). Index with "How evaluation is taught" |
| `private/research-base/code/` | 1,044 + 1 repo | 726,562 | CS50P (all weeks and 40 problem sets), code-reading and debugging research, steering AI assistants (Prompt Problems, CS1-LLM), Exercism. Index with "How code is taught" |
| `private/research-base/system-design/` | 321 + 5 repos | 306,668 | system-design-primer, Anthropic cookbook agent patterns, Microsoft courses, 12-factor-agents; reference notes on Hello Interview, ByteByteGo, Huyen, Yan, Fowler. Index with "the frames experts use" |
| `private/research-base/production-and-llm-behaviour/` | 64 | 266,595 | Google SRE book and workbook, inference and cost guides, HF LLM Course ch. 1-2, three Karpathy transcripts |
| `private/research-base/learning-methods/` | 43 | 474,000 | The Math Academy Way, Khan Academy research, and the primary papers (worked examples, fading, productive failure, comparison, retrieval, spacing, interleaving, 4C/ID, deliberate practice) |

About 2.5 million words of primary material, every file headed with its source URL and fetch date.

## Known limits
- Lab level details on ScaleDojo beyond level 1 were not collected (the browser safety check blocked bulk
  reading; Architect's Sandbox is on, so levels open directly on the site).
- Paywalled: Hello Interview premium breakdowns (including its only GenAI one), Hamel and Shreya's course
  reader, Chip Huyen's book chapters, several ACM papers.
- Instagram captions were analysed on 09-01 but not saved raw; re-scraping was rate-limited.
- Self-reported platform numbers (Math Academy, Khan, Maven, ScaleDojo) are marked as such in every file.
