#!/usr/bin/env python3
"""Pull teaching exchanges out of a Claude Code transcript: each assistant message that asked
Faiz questions, paired with his next typed reply. Deterministic, stdlib only.

Usage:
  python3 scripts/extract_teaching.py TRANSCRIPT.jsonl            print exchanges after the last reflect
  python3 scripts/extract_teaching.py TRANSCRIPT.jsonl --all      print every exchange
  python3 scripts/extract_teaching.py TRANSCRIPT.jsonl --count    print how many exchanges exist
  python3 scripts/extract_teaching.py TRANSCRIPT.jsonl --mark     record all current exchanges as reflected
"""
import json
import os
import sys

ROOT = "/Users/faizr/AI OS for Learning"
STATE = os.path.join(ROOT, "docs", "reflect-state.json")
ASKED = ("**Your turn", "Your turn.", "**Your pick.**", "**Your call.**", "Change one decision", "**Your move.**", "**Your judgement.**")


def typed_text(content):
    """The human-typed text of a user entry, or None for tool results and hook/system noise."""
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        if any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
            return None
        text = "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    else:
        return None
    text = text.strip()
    if not text or text.startswith("<") or "[SYSTEM NOTIFICATION" in text:
        return None
    return text


def exchanges(path):
    """Every typed reply that follows teaching. kind is 'answer' when the message before it asked
    questions, 'follow-up' when it came after a hint, a correction or a build result."""
    out, texts, teaching = [], [], False
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        content = (e.get("message") or {}).get("content")
        if e.get("type") == "assistant" and isinstance(content, list):
            texts += [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
        elif e.get("type") == "user":
            reply = typed_text(content)
            if reply is None:
                continue
            said = "\n".join(texts)
            if any(a in said for a in ASKED):
                out.append({"ts": e.get("timestamp", ""), "kind": "answer", "asked": said, "reply": reply})
                teaching = True
            elif teaching and said.strip():
                out.append({"ts": e.get("timestamp", ""), "kind": "follow-up", "asked": said, "reply": reply})
            texts = []
    return out


def load_state():
    try:
        return json.load(open(STATE))
    except (OSError, ValueError):
        return {}


def main(argv):
    path = argv[1]
    key = os.path.basename(path)
    ex = exchanges(path)
    state = load_state()
    if "--count" in argv:
        print(len(ex))
        return
    if "--mark" in argv:
        state[key] = len(ex)
        json.dump(state, open(STATE, "w"), indent=2)
        print(f"marked {len(ex)} exchanges in {key} as reflected")
        return
    start = 0 if "--all" in argv else state.get(key, 0)
    for i, x in enumerate(ex[start:], start + 1):
        print(f"===== exchange {i}  {x['ts'][:16]}  {x['kind']}")
        print("----- ASKED (tail)")
        print(x["asked"][-2500:])
        print("----- HE REPLIED")
        print(x["reply"])


if __name__ == "__main__":
    main(sys.argv)
