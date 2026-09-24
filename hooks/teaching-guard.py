#!/usr/bin/env python3
"""Stop hook: a question to Faiz may only be sent if it comes, verbatim, from checked material.

v2 (learn/units): see unit_step(). Legacy lesson scripts (below) are kept for the archived method.

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
    text = last_assistant_text(data["transcript_path"])
    if re.search(r"(?i)your answer", text):
        return unit_step(text)                # checked even on a retry: the correction must itself be right
    if data.get("stop_hook_active"):
        return
    from check_lesson_script import parts, problems, START_MARKERS, ASK_MARKERS
    if not any(a in text for a in ASK_MARKERS):
        return
    starts = [text.index(m) for m in START_MARKERS if m in text]
    if not starts:
        reason = "A teaching part or build was sent without the faiz-teach template."
    else:
        sent = norm(text[min(starts):])
        reason = "This teaching part or build does not come from a validated lesson script (projects/*/script.md)."
        for path in glob.glob(os.path.join(ROOT, "projects", "*", "script.md")):
            for part_id, new, body, key, status in parts(open(path).read()):
                found = [body.index(m) for m in START_MARKERS if m in body]
                if not found:
                    continue
                scripted = norm(body[min(found):])
                if scripted and scripted in sent:
                    errs = problems(part_id, new, body, key, "")
                    if not errs:
                        return
                    reason = f"Part {part_id} in {path} fails validation: " + "; ".join(errs)
    print(json.dumps({
        "decision": "block",
        "reason": reason + " Write or fix the part in the lesson script, run "
                  "scripts/check_lesson_script.py until it passes, then send the part verbatim.",
    }))


def unit_step(text):
    """Unit steps (learn/units): the message must hold exactly one step of a checked unit, verbatim, as its last
    text, the next one in order; no answer-key text anywhere; feedback on his last answer may come before it.
    Fails closed: any error here blocks. The hook runs after the message is shown, so a block asks for a
    correction in the next message; it cannot unsend."""
    def block(reason):
        print(json.dumps({"decision": "block", "reason": reason + " Send exactly one step of a checked unit "
                          "(learn/units, passing learn/check_unit.py), verbatim, as the whole of the message after "
                          "any short feedback, in the unit's order."}))
    try:
        sys.path.insert(0, os.path.join(ROOT, "learn"))
        from check_unit import steps, problems as unit_problems
        sent = norm(text)
        matches = []
        for path in glob.glob(os.path.join(ROOT, "learn", "units", "*", "*.md")):
            unit = open(path).read()
            for i, (name, body, key) in enumerate(steps(unit)):
                b = norm(body)
                if b and b in sent:
                    matches.append((path, i, name, b, key))
                for line in key.splitlines():
                    if len(norm(line)) >= 25 and norm(line) in sent:
                        return block(f"Answer-key text from {os.path.basename(path)} appears in the message.")
        if not matches:
            return block("A question asking for his answer does not come from a checked unit.")
        if len(matches) > 1:
            return block("More than one step in one message.")
        path, i, name, b, key = matches[0]
        after = sent[sent.index(b) + len(b):].strip()
        before = sent[:sent.index(b)]
        if after:
            return block(f"Text was added after step '{name}'.")
        if re.search(r"(?i)your answer", before) or "?" in before:
            return block("A question appears before the step; feedback before a step only says what was right or wrong.")
        if len(before) > 400:
            return block("The feedback before the step is longer than 400 characters (at most 3 short points).")
        errs = unit_problems(path)
        if errs:
            return block(f"Unit {os.path.basename(path)} fails its check: " + "; ".join(errs[:3]) + ".")
        cursor_file = os.path.join(ROOT, "learn", "data", "cursor.json")
        cur = json.load(open(cursor_file)) if os.path.exists(cursor_file) else {}
        cold = name.startswith("Cold")
        if not cold:
            same = cur.get("unit") == path
            finished = cur.get("finished", True)
            if same and i <= cur.get("index", -1):
                return block(f"Step '{name}' was already sent; steps go forward only.")
            if not same and not finished:
                return block(f"The unit {os.path.basename(cur['unit'])} is not finished (its Close step is not sent).")
            if not same and i != 0:
                return block(f"A unit starts at its first step, not '{name}'.")
            total = len([s for s in steps(open(path).read()) if not s[0].startswith("Cold")])
            os.makedirs(os.path.dirname(cursor_file), exist_ok=True)
            json.dump({"unit": path, "index": i, "finished": i == total - 1}, open(cursor_file, "w"))
    except Exception as e:                    # fail closed for unit steps
        return block(f"The step check itself failed ({type(e).__name__}).")


try:
    main()
except Exception:
    pass
