#!/usr/bin/env python3
"""Check a unit file before any of it is sent. A unit that fails is not taught.

    python3 learn/check_unit.py learn/units/code/01-*.md     # one or more files; exit 1 on any failure

Enforces (docs/research/structures/INTEGRATED.md; docs/research/audit-system.md findings 13-19):
- the skill's own steps in order ('## Step: <name>'), each ending '**Your answer.**' with a '### Key';
- a 'scored:' header naming the scored steps; each scored step's Key starts a line with 'Score:';
- a '## Cold' item (a new problem of the same kind, new numbers or code) with its own Key and 'Score:';
- every number in step text, Keys, cold item and cards comes from a listed run (made by a recorded command)
  or facts.md (verified rows only); a source number counts only inside quotation marks that match the
  source; a scenario fact sits on a line that starts 'given:'; spelled-out numbers are not allowed;
- every fenced code block (other than ```output) appears in a listed program file under 'code:';
- at least one card; watchlist jargon explained right where it is first used.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
ASK = "**Your answer.**"
STEPS = {
    "code": ["Predict", "Trace", "Change", "Find the bug", "Tell the AI", "Close"],
    "llm": ["Odd result", "Pick and say why", "Predict", "Run", "Explain", "Wrong idea fixed", "New case", "Close"],
    "production": ["Guess", "Chain", "Run", "Lever", "Quick set", "Close"],
    "evaluation": ["Warm-up labels", "Label the batch", "Group the failures", "Compare with the expert",
                   "Count and decide", "Close"],
    "design": ["Read the brief", "First design", "Numbers", "Choices", "Compare with the expert", "What if",
               "Decision note", "Close"],
}
OPTIONAL = {("code", "Tell the AI"): 2}          # step: first level at which it is required
NUMBER_WORDS = r"\b(eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)\b"


def header(text):
    h = dict(re.findall(r"(?m)^(\w[\w ]*):\s*(.*)$", text.split("\n## ", 1)[0]))
    for k in ("sources", "runs", "code", "scored"):
        h[k] = [x.strip() for x in h.get(k, "").split(",") if x.strip()]
    return h


def steps(text):
    """[(name, body, key)] for every '## Step: name' block and the '## Cold' item (named 'Cold')."""
    out = []
    for block in re.split(r"(?m)^## ", text)[1:]:
        head, _, rest = block.partition("\n")
        if head.startswith("Step: ") or head.strip() == "Cold":
            body, _, key = rest.partition("### Key")
            out.append((head[6:].strip() if head.startswith("Step: ") else "Cold", body.strip(), key.strip()))
    return out


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
        if re.match(r"\s*(- )?given:", line, flags=re.I):
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
                       f"(or an exact quotation from a source; scenario facts go on a line starting 'given:')")
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
    if skill not in STEPS:
        return [f"unknown skill '{skill}'"]
    all_steps = steps(text)
    found = [s[0] for s in all_steps if s[0] != "Cold"]
    expected = [s for s in STEPS[skill] if level >= OPTIONAL.get((skill, s), 0)]
    if found != [s for s in STEPS[skill] if s in found] or [s for s in expected if s not in found]:
        out.append(f"steps must be, in order: {expected}; found {found}")
    if not h["scored"] or [s for s in h["scored"] if s not in found]:
        out.append(f"'scored:' must list the scored steps (from {found}); got {h['scored']}")
    measured, sources_text = "", ""
    for kind in ("runs", "sources", "code"):
        for rel in h[kind]:
            f = HERE / rel if (HERE / rel).exists() else ROOT / rel
            if not f.exists():
                out.append(f"listed file not found: {rel}")
            elif kind == "runs":
                raw = f.read_text(errors="ignore")
                try:
                    if not json.loads(raw).get("command"):
                        out.append(f"run {rel} does not record the command that produced it")
                except ValueError:
                    out.append(f"run {rel} is not valid JSON")
                measured += raw.replace("\\n", "\n").replace("\\t", "\t")   # JSON escapes hid line-start numbers
            elif kind == "sources":
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
    if not any(s[0] == "Cold" for s in all_steps):
        out.append("missing '## Cold' item: a new problem of the same kind for the 7-day cold check")
    for name, body, key in all_steps:
        where = f"step '{name}'"
        if not body.rstrip().endswith(ASK):
            out.append(f"{where} must end with {ASK}")
        if len(key) < 20 or re.fullmatch(r"(?i)\s*(tbd|todo|\.\.\.)\s*", key):
            out.append(f"{where} has no real ### Key")
        if (name in h["scored"] or name == "Cold") and not re.search(r"(?m)^Score:", key):
            out.append(f"{where} is scored, so its Key needs a line starting 'Score:' (how to mark it)")
        if len(body) > 2000:
            out.append(f"{where} is {len(body)} characters, max 2000")
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
