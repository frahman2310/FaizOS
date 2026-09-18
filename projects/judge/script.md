# Lesson 6 · judge · teaching script
Goal: find what is really failing, then an AI judge you can trust. Skills: error-analysis,
failure-taxonomy, sql-joins-aggregation, sql-window-functions, llm-judge-design, judge-validation,
statistical-gating. Number: failure counts by kind, and the judge's agreement with his own labels.

Carry-over from L5: three adjustments, from docs/learning-evidence.md
- Word every question as a concrete scenario with a one-word or one-number answer. Two L5 questions used abstract nouns ("does the list notice", "how many different setups") and both had to be reworded.
- Ask the Someone broke it question for the label alone unless the value matters; R2-B Q5 asked for both and came back blank.
- Keep every build option a real trade-off (C35) and name in the Key what the winner gives up; L5 D1 and D2 were called out as obvious.
Also: his weakest L5 answers were the baseline moving after a change lands, and least access. Both belong in L6 as one-line reminders inside a part, not as new teaching.
