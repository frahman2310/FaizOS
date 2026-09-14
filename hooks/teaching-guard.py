#!/usr/bin/env python3
"""Stop hook: a teaching part may only be sent if it comes, verbatim, from a validated script.

If the last assistant message contains '**Your turn.**', its text from '**The problem.**' on must
match a part body in some projects/*/script.md that passes check_lesson_script.py. Otherwise the
stop is blocked with the reason. Fails open on any unexpected error; never blocks twice in a row.
"""
import glob
import json
import os
import re
import sys

ROOT = "/Users/faizr/AI OS for Learning"
sys.path.insert(0, os.path.join(ROOT, "scripts"))


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def last_assistant_text(transcript):
    texts = []
    for line in open(transcript):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        msg = e.get("message") or {}
        content = msg.get("content")
        if e.get("type") == "user":
            is_tool_result = isinstance(content, list) and all(
                isinstance(c, dict) and c.get("type") == "tool_result" for c in content)
            if not is_tool_result:
                texts = []
        elif e.get("type") == "assistant" and isinstance(content, list):
            texts += [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
    return "\n".join(texts)


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return
    text = last_assistant_text(data["transcript_path"])
    if "**Your turn.**" not in text:
        return
    if "**The problem.**" not in text:
        reason = "A teaching part was sent without the faiz-teach template (no '**The problem.**')."
    else:
        from check_lesson_script import parts, problems
        sent = norm(text[text.index("**The problem.**"):])
        reason = "This teaching part does not come from a validated lesson script (projects/*/script.md)."
        for path in glob.glob(os.path.join(ROOT, "projects", "*", "script.md")):
            for part_id, new, body, has_key in parts(open(path).read()):
                if "**The problem.**" not in body:
                    continue
                scripted = norm(body[body.index("**The problem.**"):])
                if scripted and scripted in sent:
                    errs = problems(part_id, new, body, has_key)
                    if not errs:
                        return
                    reason = f"Part {part_id} in {path} fails validation: " + "; ".join(errs)
    print(json.dumps({
        "decision": "block",
        "reason": reason + " Write or fix the part in the lesson script, run "
                  "scripts/check_lesson_script.py until it passes, then send the part verbatim.",
    }))


try:
    main()
except Exception:
    pass
