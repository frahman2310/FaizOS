---
description: The venture evidence engine. Ingest, classify, corroborate, score, activate (WIP limit 1), review.
argument-hint: [ingest | score | activate <id> | review]
---
The pipeline gathers evidence; he makes the decision. Never recommend which venture to pick.

**ingest.** Call `faizos_venture_ingest` (stage 1 fetch from the free tier sources). Then
call `faizos_venture_pending` and classify each pending item yourself: the job to be done,
importance 1 to 5, dissatisfaction 1 to 5. Save with `faizos_venture_classify_save`. Every
record keeps its source URL and raw excerpt; never summarise without the evidence.

**score.** Call `faizos_venture_score` (stages 3 and 4). Present:
- Opportunities that PASSED corroboration (2 or more independent source families), with their
  evidence, URLs, and the six axis scores.
- What FAILED the gate and exactly why. The failures teach as much as the passes.
Do not rank beyond the weighted score. Do not recommend.

**activate <id>.** Call `faizos_venture_activate`. The database allows exactly one active
venture; if the slot is taken the tool will refuse and say so. On success, hand the emitted
14 day v0 milestone spine to Build Mode: `/faiz-build venture:<id>`.

**review.** The 14 day gate. Call `faizos_venture_review` to fetch the active venture and its
metric. Exactly three outcomes, he picks: continue (new 14 day metric), park (written
reason), kill (post mortem, which the tool writes back to insights). No fourth option, no
silent drift.

Constraints that stand until he clears them: the UK student visa question and the Pakistan
payment rail question gate ANY monetisation. Building and evidence gathering are fine;
acting commercially on the output is not, yet.
