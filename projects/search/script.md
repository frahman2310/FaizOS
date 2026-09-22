# Lesson 7 · search · teaching script
Goal: retrieval from scratch, then vectors. Skills: retrieval-metrics, retrieval-decision,
chunking-strategies, contextual-retrieval, pgvector-limits. Number: Recall@5, MRR, recall vs chunk size.

Carry-over from L6: four adjustments, from docs/learning-evidence.md
- Before any question asking which way a wrong number bends a decision (or what a number proves), show one worked chain of the same kind on other numbers in the part. L6 Round 2 went 0/3 first try on exactly these (E12).
- Build: write and run the model first and take every given from its output. L6 Decision 4 stated a scan share that clashed with Decision 3 and needed a correction.
- Build: no prediction step; after the last pick, build and run at once ("Idw predict, just build", C37). Show him the combined effect when two picks each add cost; in L6 two individually fine picks broke the budget together.
- First lesson under C38/C39: every part follows the new template (counts for rates, How it works for formulas, Worked chain before direction questions, 3+ bank questions tagged in the Key); every decision has 2+ realistic difficulties and a prediction with all its data.
Also: his weakest L6 answers were complement counts (how many did NOT agree) and GROUP BY one pile vs many. Cohen's kappa was not taught in L6; teach it where agreement between two labellers comes up.
