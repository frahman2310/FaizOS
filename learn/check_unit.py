#!/usr/bin/env python3
"""Check a unit file before any of it is sent. A unit that fails is not taught.

    python3 learn/check_unit.py learn/units/code/01-*.md     # one or more files; exit 1 on any failure

Unit format v3 (docs/research/structures/INTEGRATED.md section 2.3; the six audits of 2026-09-25):
- '## Step: <name>' blocks in teaching order. Each Key has 'Kind: show|try|scored|close'.
  show = worked example or explanation (I do), never scored, Key lists 'New:' ideas (at most 3);
  try = guided practice (we do), unscored, aimed at about 80% right;
  scored = independent item (you do), listed in the header 'scored:', Key has 'Score:';
  close = his one-line rule.
- The first step is a show; every scored step comes after at least one show AND one try; the last is close.
- '## Help: <step name>': a prepared second worked example on a new surface for when he is stuck (at least one).
- '## Retry' (after a miss, new surface) and '## Cold' (7 days later): scored, each with 'Score:'.
- Every step body (code included) is at most 2600 characters; any code block has a '**How this ... works'
  block (C48); every step ends '**Your answer.**'.
- Numbers come from listed runs or verified facts.md rows (exact quotes of sources allowed; scenario facts on
  a line starting 'given:'); no spelled-out numbers; code blocks appear in listed programs (code skill);
  ```output lines appear in runs; at least one card, number/code cards with a second surface.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
ASK = "**Your answer.**"
SKILLS = ("code", "llm", "production", "evaluation", "design")
KINDS = ("show", "try", "scored", "close")
MAX_NEW = 3                                      # new ideas per show step (Rosenshine small steps; his A11)
MAX_BODY = 2600                                  # characters per message, code included (his B8; eval audit F23)
NUMBER_WORDS = r"\b(eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)\b"


def header(text):
    h = dict(re.findall(r"(?m)^(\w[\w ]*):\s*(.*)$", text.split("\n## ", 1)[0]))
    for k in ("sources", "runs", "code", "scored"):
        h[k] = [x.strip() for x in h.get(k, "").split(",") if x.strip()]
    return h


def steps(text):
    """[(name, body, key)] for every '## Step: name' block, then 'Help: X', 'Retry' and 'Cold' blocks by name."""
    out = []
    for block in re.split(r"(?m)^## ", text)[1:]:
        head, _, rest = block.partition("\n")
        head = head.strip()
        if head.startswith("Step: ") or head.startswith("Help: ") or head in ("Cold", "Retry"):
            body, _, key = rest.partition("### Key")
            out.append((head[6:].strip() if head.startswith("Step: ") else head, body.strip(), key.strip()))
    return out


def kind(key):
    m = re.search(r"(?m)^Kind:\s*(\w+)", key)
    return m.group(1).lower() if m else None


def is_extra(name):
    """Blocks outside the teaching order: sent only when needed (stuck, missed, 7 days later)."""
    return name in ("Cold", "Retry") or name.startswith("Help: ")


def cards(text):
    block = text.split("## Cards", 1)[1] if "## Cards" in text else ""
    return re.findall(r"(?m)^- (Q: .+ \| A: .+)$", block)


def numbers(text):
    return {n.rstrip(".,").replace(",", "") for n in re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", text)}


def facts_numbers():
    """Numbers from verified rows of facts.md (rows marked 'unverified' do not count)."""
    return numbers("\n".join(l for l in (HERE / "facts.md").read_text().splitlines() if "unverified" not in l.lower()))


def check_numbers(where, text, known, sources_text):
    out = []
    prose = re.sub(r"(?ms)^```(\w*)\n.*?^```", lambda m: m.group(0) if m.group(1) == "output" else " ", text)  # code: checked against programs
    for line in prose.splitlines():
        if re.match(r"\s*(- |> )?(given:|suppose\b)", line, flags=re.I):   # a stated hypothetical, not a fact
            continue
        if re.search(NUMBER_WORDS, line, flags=re.I):
            out.append(f"{where}: spelled-out number in '{line.strip()[:60]}' (write it as digits, traced)")
        quoted = " ".join(q for q in re.findall(r'"([^"]{8,})"|“([^”]{8,})”', line) for q in q if q)
        for n in numbers(line):
            if n in known or re.fullmatch(r"\d", n):
                continue
            if n in numbers(quoted) and any(q.strip() and q.strip() in sources_text
                                            for q in re.findall(r'"([^"]{8,})"', line)):
                continue
            out.append(f"{where}: number {n} is not in a listed run or verified facts.md row "
                       f"(or an exact quotation from a source; a made-up scenario number goes on a line starting 'Suppose')")
    return out


def problems(path):
    path = Path(path)
    text = path.read_text()
    h = header(text)
    out = []
    skill = h.get("skill")
    try:
        level = int(h.get("level", "1"))
    except ValueError:
        return ["'level:' must be a whole number"]
    if skill not in SKILLS:
        return [f"unknown skill '{skill}'"]
    all_steps = steps(text)
    order = [(n, kind(k)) for n, b, k in all_steps if not is_extra(n)]
    names = [n for n, _ in order]
    if not order:
        return ["no '## Step:' blocks"]
    for n, k in order:
        if k not in KINDS:
            out.append(f"step '{n}': its Key needs 'Kind: show|try|scored|close' (got {k})")
    if order[0][1] != "show":
        out.append(f"the first step must be a show (explain and show before asking); got '{order[0][0]}' ({order[0][1]})")
    if order[-1][1] != "close":
        out.append(f"the last step must be the close; got '{order[-1][0]}'")
    seen = set()
    for n, k in order:
        if k == "scored" and not {"show", "try"} <= seen:
            out.append(f"scored step '{n}' comes before at least one show and one try (I do, we do, then you do)")
        seen.add(k)
    marked = [n for n, k in order if k == "scored"]
    if not h["scored"] or sorted(h["scored"]) != sorted(marked):
        out.append(f"'scored:' must list exactly the steps with Kind: scored {marked}; got {h['scored']}")
    for n, b, k in all_steps:
        if kind(k) == "show":
            m = re.search(r"(?m)^New:\s*(.*)$", k)
            new = [x for x in (m.group(1).split(",") if m else []) if x.strip() and x.strip() != "-"]
            if not m:
                out.append(f"show step '{n}': its Key needs a 'New:' line listing the new ideas it adds ('-' if none)")
            elif len(new) > MAX_NEW:
                out.append(f"show step '{n}' adds {len(new)} new ideas, max {MAX_NEW}: split it")
    for extra in ("Retry", "Cold"):
        if extra not in [n for n, _, _ in all_steps]:
            out.append(f"missing '## {extra}' item (new surface, same kind; scored with a 'Score:' line)")
    helps = [n for n, _, _ in all_steps if n.startswith("Help: ")]
    if not helps:
        out.append("no '## Help: <step name>' block (a prepared second worked example for when he is stuck)")
    for hname in helps:
        if hname[6:] not in names:
            out.append(f"'{hname}' names a step that does not exist")
    measured, sources_text = "", ""
    for part in ("runs", "sources", "code"):
        for rel in h[part]:
            f = HERE / rel if (HERE / rel).exists() else ROOT / rel
            if not f.exists():
                out.append(f"listed file not found: {rel}")
            elif part == "runs":
                raw = f.read_text(errors="ignore")
                try:
                    if not json.loads(raw).get("command"):
                        out.append(f"run {rel} does not record the command that produced it")
                except ValueError:
                    out.append(f"run {rel} is not valid JSON")
                measured += raw.replace("\\n", "\n").replace("\\t", "\t")   # JSON escapes hid line-start numbers
            elif part == "sources":
                sources_text += re.sub(r"\s+", " ", f.read_text(errors="ignore"))
    programs = ""
    for rel in h["code"]:
        base = HERE / rel
        for f in ([base] if base.is_file() else sorted(base.rglob("*.py")) if base.exists() else []):
            programs += f.read_text(errors="ignore")
    known = numbers(measured) | facts_numbers()
    try:
        from check_lesson_script import glossary
        taught, watch = glossary()
    except Exception as e:
        return [f"glossary unavailable ({e}); fix docs/glossary.md or scripts/check_lesson_script.py"]

    def jargon_problems(body):
        """A watchlist word not yet taught must be explained AFTER it in the same sentence."""
        plain = re.sub(r"```.*?```|`[^`]*`", " ", body, flags=re.S).lower()
        errs = []
        for term in watch:
            if term in taught:
                continue
            m = re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", plain)
            if not m:
                continue
            rest = re.split(r"(?<=[.!?])\s", plain[m.end():], maxsplit=1)[0]
            if not re.match(r"\s*(\(|,? (which |that )?(means|is called|is a|is an|is the|are the|, meaning)\b|:)", rest):
                errs.append(f"'{term}' is not taught yet and is not explained right after it (in brackets or 'means ...')")
        return errs
    for name, body, key in all_steps:
        where = f"step '{name}'"
        if not body.rstrip().endswith(ASK):
            out.append(f"{where} must end with {ASK}")
        if len(key) < 20 or re.fullmatch(r"(?i)\s*(tbd|todo|\.\.\.)\s*", key):
            out.append(f"{where} has no real ### Key")
        if (kind(key) == "scored" or name in ("Cold", "Retry")) and not re.search(r"(?m)^Score:", key):
            out.append(f"{where} is scored, so its Key needs a line starting 'Score:' (how to mark it)")
        if len(body) > MAX_BODY:
            out.append(f"{where} is {len(body)} characters with code, max {MAX_BODY}: split it")
        if re.search(r"```(python|sql)", body) and "**How this" not in body:
            out.append(f"{where} shows code without a '**How this code works' explanation (C48)")
        if re.search(r"(?m)^\s*(- )?given:", body):
            out.append(f"{where}: 'given:' is a checker tag for the Key; in the text he reads, name the source instead")
        out += [f"{where}: {j}" for j in jargon_problems(body)]
        out += check_numbers(where, body, known, sources_text)
        out += check_numbers(f"{where} Key", key, known, sources_text)
        for code in re.findall(r"```(\w*)\n(.*?)```", body, flags=re.S):
            lang, block = code
            if lang == "output":
                missing = [l for l in block.strip().splitlines() if l.strip() and l.strip() not in measured]
                if missing:
                    out.append(f"{where}: output line not in a listed run: '{missing[0][:50]}'")
            elif skill == "code":
                lines = [l.strip() for l in block.strip().splitlines() if l.strip() and not l.strip().startswith("#")]
                absent = [l for l in lines if l not in programs]
                if absent:
                    out.append(f"{where}: code line not in the listed programs: '{absent[0][:50]}'")
    cs = cards(text)
    if not cs:
        out.append("no card in '## Cards' ('- Q: ... | A: ...', variants joined by ' || ')")
    for c in cs:
        out += check_numbers("card", c, known, sources_text)
        if re.search(r"\d|`", c) and " || " not in c:      # INTEGRATED 2.1: never the same surface
            out.append(f"card with a number or code needs a second variant (' || Q: ... | A: ...'): '{c[:50]}'")
    return out


def main(paths):
    bad = 0
    for p in paths:
        try:
            errs = problems(p)
        except Exception as e:
            errs = [f"checker error: {type(e).__name__}: {e}"]
        print(("PASS  " if not errs else "FAIL  ") + str(p))
        for e in errs:
            print("      " + e)
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
