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
    texts, final = [], []
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
                texts, final = [], []
            else:
                final = []                    # text before a tool call is narration, not the final message
        elif e.get("type") == "assistant" and isinstance(content, list):
            t = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
            texts += t
            final += t
    last_assistant_text.final = "\n".join(final)
    return "\n".join(texts)


def main():
    data = json.load(sys.stdin)
    text = last_assistant_text(data["transcript_path"])
    if re.search(r"\*\*Your answer[.:]?\*\*", text):   # the unit's question marker only; "look at your answer" is help
        return unit_step(text, last_assistant_text.final)   # checked even on a retry
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


def unit_step(text, final=None):
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
        from check_unit import steps, is_extra, problems as unit_problems
        sent = norm(text)
        matches = []
        for path in glob.glob(os.path.join(ROOT, "learn", "units", "*", "*.md")):
            unit = open(path).read()
            shown = " ".join(norm(b) for _, b, _ in steps(unit))     # key lines also in a step are not secret
            for i, (name, body, key) in enumerate(steps(unit)):
                b = norm(body)
                if b and b in sent:
                    matches.append((path, i, name, b, key))
                for line in key.splitlines():
                    if len(norm(line)) >= 25 and norm(line) in sent and norm(line) not in shown:
                        return block(f"Answer-key text from {os.path.basename(path)} appears in the message.")
        if not matches:
            return block("A question asking for his answer does not come from a checked unit.")
        if len(matches) > 1:
            return block("More than one step in one message.")
        path, i, name, b, key = matches[0]
        last = norm(final if final is not None else text)   # order and length: the final message only
        if b not in last:
            return block(f"Step '{name}' must be in the final message, after any tool use.")
        after = last[last.index(b) + len(b):].strip()
        before = last[:last.index(b)]
        if after:
            return block(f"Text was added after step '{name}'.")
        if re.search(r"\*\*Your answer", before) or "?" in before:
            return block("A question appears before the step; feedback before a step only says what was right or wrong.")
        if len(before) > 600:
            return block("The feedback before the step is longer than 600 characters (at most 3 short points).")
        errs = unit_problems(path)
        if errs:
            return block(f"Unit {os.path.basename(path)} fails its check: " + "; ".join(errs[:3]) + ".")
        cursor_file = os.path.join(ROOT, "learn", "data", "cursor.json")
        cur = json.load(open(cursor_file)) if os.path.exists(cursor_file) else {}
        if not is_extra(name):                # Help, Retry and Cold blocks are sent when needed, outside the order
            same = cur.get("unit") == path
            finished = cur.get("finished", True)
            if not same and not finished:
                return block(f"The unit {os.path.basename(cur['unit'])} is not finished (its Close step is not sent).")
            if not same and i != 0:
                return block(f"A unit starts at its first step, not '{name}'.")
            if same and i > cur.get("index", -1) + 1:
                return block(f"Step '{name}' skips a step: send the steps in order, show and try before scored.")
            total = len([s for s in steps(open(path).read()) if not is_extra(s[0])])
            os.makedirs(os.path.dirname(cursor_file), exist_ok=True)
            i = max(i, cur.get("index", -1)) if same else i
            json.dump({"unit": path, "index": i, "finished": i == total - 1 or (same and cur.get("finished", False))},
                      open(cursor_file, "w"))
    except Exception as e:                    # fail closed for unit steps
        return block(f"The step check itself failed ({type(e).__name__}).")


try:
    main()
except Exception:
    pass
