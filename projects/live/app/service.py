# Lesson 4 build: the L3 meter as a web service, built to Faiz's five decisions.
#   D1 two-stage box (see Dockerfile)   D2 health check B   D3 always on   D4 Mumbai   D5 1 second deadline
import os

from fastapi import FastAPI

import meter

meter.TIMEOUT = 1.0           # D5: a 1 second deadline, then the L3 retries

app = FastAPI()
log = []


def complete(prompt):
    # The one socket every place calls (Round 1 Part D).
    return meter.call(prompt, "haiku", log)


@app.get("/summary")
def summary():
    return {"reply": complete("summarise this invoice")}


@app.get("/health")
def health():
    # D2 option B: running, AND the AI password is present, without a paid AI call.
    return {"ok": True, "password_ok": bool(os.environ.get("AI_PASSWORD"))}
