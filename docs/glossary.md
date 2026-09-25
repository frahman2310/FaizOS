# Glossary

Words Faiz has been taught, with the plain meaning used in lessons. The lesson checker reads this.
A word on the watchlist may only appear in a part if it is listed under Taught, or if the part
explains it in plain words where it first appears (followed within the same sentence by "means",
"is", "called", or a bracket).

## Taught
list: things in a row in square brackets
dict: labels paired with values in curly brackets
loop: running the inside once for each item (for)
try: run this, and if it crashes do the except part instead
p50: the middle time when all times are lined up
p95: the 95th time out of 100 when lined up fastest to slowest
provider: the AI company you call
timeout: how long you are willing to wait before giving up
retry: trying the same call again after a failure
backoff: waiting a bit longer before each retry
URL: a web address that runs a machine on a computer that is always on
health check: an address the hosting company visits to ask if your app works
image: a sealed box holding your app plus everything it needs (Docker image)
cold start: the wait while a switched-off app starts again
travel time: the round trip from the user to the always-on computer
host: the company running the always-on computer
test case: one real input paired with the text a correct answer must include
assert: a line that stops the program when its yes-or-no check is false
regression: a failure that was fixed coming back later
pass rate: the share of test cases that pass
gate: an automatic check every proposed change must pass before it is allowed in
baseline: the score of the version people are using today, measured on the same cases
GitHub Actions: the service that starts a fresh computer and runs the gate on every proposed change
OIDC: proving which project a run belongs to, so it gets a pass that expires instead of a stored password
secret: a password stored in a service's settings, readable by every run
summariser: the machine that turns a supplier email into a one-line invoice note
judge: a second AI that marks each output pass or fail against one written rule
catch rate: of the notes a person marked FAIL, the share the judge also marked FAIL (tools name this TPR or TNR depending on which label they call positive; say "catch rate")
clear rate: of the notes a person marked PASS, the share the judge also marked PASS (say "clear rate")
wobble: how far a rate measured on a set of cases can sit from the true rate by luck alone
true rate: the rate on every case the firm will ever see, not just the ones measured

model: the AI program that produces the answers, e.g. Claude or the small Qwen model on this Mac
token: one piece of text the model reads or writes, often part of a word; you pay per token
prompt: all the text sent to the model in one call, including any earlier conversation

## Watchlist
prompt, ship, deploy, eval, eval set, test case, pass rate, regression, merge, commit, repo,
repository, pipeline, CI, GitHub Actions, workflow, gate, API, endpoint, token, model, latency,
throughput, summariser, assertion, assert, benchmark, baseline, held-out, dataset, credential,
secret, OIDC, IAM, permission, role, environment variable, production, staging, branch, pull request, TPR, TNR, sample, true rate, kappa, tokenizer, temperature, p50, median, fsrs, sampling, logprob, softmax, context window, greedy, parsons, trace table, regex
