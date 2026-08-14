# Capstone audit, auto scored

Scored from the systems and experiments tables. A rung counts only when database rows back
it, and every rung prints the rule it was scored by. Regenerated on every session close;
hand editing is pointless and the generator will not flatter.

**1 solid, 0 partial, 7 missing.**

## Rung 1: From scratch fundamentals [SOLID]
- Evidence: 44 shipped study systems
- Scoring rule: 20 or more shipped study systems

## Rung 2: A working system others can run [MISSING]
- Evidence: no shipped product system row
- Scoring rule: a shipped systems row of kind 'product' with a repo or deployed URL

## Rung 3: A trained model with a reported metric [MISSING]
- Evidence: no trained_model system with a metric
- Scoring rule: a trained_model system with a metric and 3 or more seeded experiment runs

## Rung 4: A measured performance win [MISSING]
- Evidence: no kernel system with metric and baseline
- Scoring rule: a kernel system whose measured metric differs from its reference baseline

## Rung 5: A reproduction of a published result [MISSING]
- Evidence: no system whose seeded mean matches its published baseline within the spread
- Scoring rule: a system with 3 or more seeds whose mean metric sits within the seed spread of its recorded published baseline

## Rung 6: A merged open source contribution [MISSING]
- Evidence: no shipped systems row titled 'PR: <repo>' (ship one when a PR merges)
- Scoring rule: a shipped systems row titled 'PR: <repo>' with the PR URL as repo_url

## Rung 7: An eval harness with results [MISSING]
- Evidence: no system with a measured eval metric (perplexity, pass@k, accuracy, recall, precision, CORE)
- Scoring rule: a system carrying a real measured eval family metric

## Rung 8: A capstone artifact with a number [MISSING]
- Evidence: no product system
- Scoring rule: a shipped product system carrying a real metric (users, revenue, installs)

The fastest path from PARTIAL and MISSING to SOLID is unchanged: one rented GPU hour
produces the first real metrics (rungs 3, 5, 7), a benchmarked kernel closes 4, a
merged PR closes 6, and shipping FaizOS v2 as a product with a user count closes 2 and 8.
