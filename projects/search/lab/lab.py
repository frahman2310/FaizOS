"""The tax search lab: real FBR documents, two ways to search, and a log of every run.

    uv run lab.py ask "what is withheld on my freelance software invoices?" [--method word|meaning] [--size 250]
    uv run lab.py eval [--method word|meaning] [--size 250] [--overlap 0] [--split dev|holdout|all] [--k 5]
    uv run lab.py sql "SELECT ... FROM results ..."

Every eval writes one row per question into lab.db (tables: runs, results, passages, questions),
so any question about a run can be answered in SQL.
"""
import argparse
import json
import math
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
RAW = HERE / "corpus" / "raw"
DB = HERE / "lab.db"
DOCS = {                                   # file stem -> year the document states the law for
    "ordinance_2025": 2025,
    "ratecard_2025": 2025,
    "circular_01_2025-26": 2025,
    "ratecard_2023": 2023,                 # outdated, kept on purpose: real archives hold old versions
}


def norm(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def cut(size, overlap, drop=()):
    """Cut every document (except those in `drop`) into passages of `size` words; each starts `size - overlap` words after the last."""
    passages = []
    for doc, year in DOCS.items():
        if doc in drop:
            continue
        pages = (RAW / f"{doc}.txt").read_text(errors="ignore").split("\f")
        words = [(w, p + 1) for p, page in enumerate(pages) for w in page.split()]
        step = max(1, size - overlap)
        for start in range(0, len(words), step):
            chunk = words[start:start + size]
            passages.append({"id": len(passages), "doc": doc, "year": year, "page": chunk[0][1],
                             "text": " ".join(w for w, _ in chunk)})
            if start + size >= len(words):
                break
    return passages


def tokens(text):
    return re.findall(r"[a-z0-9]+(?:\([0-9a-z]+\))*", text.lower())


class WordSearch:
    """BM25: the Part B rarity weight, plus two refinements (a word said often counts a little more,
    with diminishing returns; long passages are marked down so they cannot win by size alone)."""
    def __init__(self, passages, k1=1.2, b=0.75):
        self.docs = [Counter(tokens(p["text"])) for p in passages]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / len(self.lens)
        found_in = Counter(w for d in self.docs for w in d)
        n = len(self.docs)
        self.weight = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in found_in.items()}
        self.k1, self.b = k1, b

    def scores(self, question):
        q = set(tokens(question))
        out = []
        for d, length in zip(self.docs, self.lens):
            s = 0.0
            for w in q & d.keys():
                tf = d[w]
                s += self.weight[w] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out


class MeaningSearch:
    """Embeddings from a small open model (BAAI/bge-small-en-v1.5, 384 numbers per text), run on the Mac's
    graphics chip and cached per cut. Numbers are scaled to length 1, so closeness is the Part A multiply-and-add."""
    PREFIX = "Represent this sentence for searching relevant passages: "

    def __init__(self, passages, size, overlap, drop=()):
        import numpy as np
        import torch
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="mps" if torch.backends.mps.is_available() else "cpu")
        cache = HERE / "cache" / f"meaning_{size}_{overlap}{'_no_' + '_'.join(sorted(drop)) if drop else ''}.npy"
        if cache.exists():
            self.vecs = np.load(cache)
        else:
            cache.parent.mkdir(exist_ok=True)
            self.vecs = self.model.encode([p["text"] for p in passages], batch_size=32, normalize_embeddings=True)
            np.save(cache, self.vecs)

    def scores(self, question):
        q = self.model.encode([self.PREFIX + question], normalize_embeddings=True)[0]
        return list(self.vecs @ q)


def build(method, size, overlap, drop=()):
    passages = cut(size, overlap, drop)
    engine = WordSearch(passages) if method == "word" else MeaningSearch(passages, size, overlap, drop)
    return passages, engine


def top(passages, engine, question, k):
    s = engine.scores(question)
    order = sorted(range(len(passages)), key=lambda i: -s[i])[:k]
    return [(passages[i], s[i]) for i in order]


def hit(passage, q):
    t = norm(passage["text"])
    return passage["doc"] == q["doc"] and all(norm(a) in t for a in q["anchors"])


def ask(a):
    passages, engine = build(a.method, a.size, a.overlap, a.drop)
    for rank, (p, s) in enumerate(top(passages, engine, a.question, a.k), 1):
        print(f"\n#{rank}  score {s:.3f}   {p['doc']}  (law as of {p['year']}), page {p['page']}, passage {p['id']}")
        print("    " + p["text"][:420] + ("..." if len(p["text"]) > 420 else ""))


def evaluate(a):
    questions = [json.loads(l) for l in (HERE / "questions.jsonl").read_text().splitlines() if l.strip()]
    if a.split != "all":
        questions = [q for q in questions if q["split"] == a.split]
    rewrites = json.loads((HERE / a.rewrites).read_text()) if a.rewrites else {}
    passages, engine = build(a.method, a.size, a.overlap, a.drop)
    db = connect()
    config = f"method={a.method} size={a.size} overlap={a.overlap} split={a.split} k={a.k}"
    config += "".join(f" drop={d}" for d in a.drop) + (f" rewrites={a.rewrites}" if a.rewrites else "")
    run = db.execute("INSERT INTO runs (config, method, size, overlap, split, k, passages) VALUES (?,?,?,?,?,?,?)",
                     (config, a.method, a.size, a.overlap, a.split, a.k, len(passages))).lastrowid
    db.executemany("INSERT OR IGNORE INTO passages VALUES (?,?,?,?,?,?,?)",
                   [(p["id"], a.size, a.overlap, p["doc"], p["year"], p["page"], p["text"]) for p in passages])
    rows = []
    for q in questions:
        ranked = top(passages, engine, rewrites.get(q["id"], q["question"]), a.k)
        rank = next((i for i, (p, _) in enumerate(ranked, 1) if hit(p, q)), 0)
        first = ranked[0][0]
        rows.append((run, q["id"], rank, first["doc"], first["year"], first["id"],
                     json.dumps([p["id"] for p, _ in ranked])))
    db.executemany("INSERT INTO results VALUES (?,?,?,?,?,?,?)", rows)
    db.commit()
    report(db, run, len(passages))


def report(db, run, n_passages):
    (config,) = db.execute("SELECT config FROM runs WHERE id=?", (run,)).fetchone()
    print(f"\nrun {run}: {config}   ({n_passages:,} passages)")
    slices = [("all questions", "1=1"),
              ("worded like the law", "q.wording='law'"), ("worded like a client", "q.wording='client'"),
              ("answer changed since 2023", "q.changed=1"), ("answer unchanged", "q.changed=0")]
    print(f"  {'':28}{'n':>4}  {'Recall@k':>9}  {'MRR':>6}  {'top is 2023 card':>17}")
    for label, where in slices:
        n, rec, mrr, stale = db.execute(f"""
            SELECT COUNT(*), AVG(r.rank > 0), AVG(CASE WHEN r.rank > 0 THEN 1.0 / r.rank ELSE 0 END),
                   SUM(r.top_year = 2023)
            FROM results r JOIN questions q ON q.id = r.question WHERE r.run = ? AND {where}""", (run,)).fetchone()
        if n:
            print(f"  {label:28}{n:>4}  {rec:>9.0%}  {mrr:>6.2f}  {stale:>9} of {n}")


def sql(a):
    db = connect()
    cur = db.execute(a.query)
    cols = [c[0] for c in cur.description or []]
    rows = cur.fetchall()
    widths = [max(len(str(c)), *(len(str(r[i])[:60]) for r in rows)) if rows else len(c) for i, c in enumerate(cols)]
    print("  ".join(c.ljust(w) for c, w in zip(cols, widths)))
    for r in rows[:200]:
        print("  ".join(str(v)[:60].ljust(w) for v, w in zip(r, widths)))
    print(f"({len(rows)} rows)")


def connect():
    db = sqlite3.connect(DB)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, config TEXT, method TEXT, size INT, overlap INT,
            split TEXT, k INT, passages INT, at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS results (run INT, question TEXT, rank INT, top_doc TEXT, top_year INT,
            top_passage INT, top_k TEXT);
        CREATE TABLE IF NOT EXISTS passages (id INT, size INT, overlap INT, doc TEXT, year INT, page INT, text TEXT,
            PRIMARY KEY (id, size, overlap));
        CREATE TABLE IF NOT EXISTS questions (id TEXT PRIMARY KEY, question TEXT, anchors TEXT, doc TEXT,
            answer TEXT, wording TEXT, changed INT, topic TEXT, split TEXT);
    """)
    qfile = HERE / "questions.jsonl"
    if qfile.exists():
        db.executemany("INSERT OR REPLACE INTO questions VALUES (?,?,?,?,?,?,?,?,?)",
                       [(q["id"], q["question"], json.dumps(q["anchors"]), q["doc"], q["answer"], q["wording"],
                         int(q["changed"]), q["topic"], q["split"])
                        for q in map(json.loads, filter(str.strip, qfile.read_text().splitlines()))])
    return db


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("ask", "eval"):
        p = sub.add_parser(name)
        if name == "ask":
            p.add_argument("question")
        p.add_argument("--method", choices=["word", "meaning"], default="word")
        p.add_argument("--size", type=int, default=250)
        p.add_argument("--overlap", type=int, default=0)
        p.add_argument("--k", type=int, default=5)
        p.add_argument("--drop", action="append", default=[], choices=list(DOCS), help="leave a document out")
        if name == "eval":
            p.add_argument("--split", default="dev", choices=["dev", "holdout", "all"])
            p.add_argument("--rewrites", help="JSON file mapping question id to the text search receives instead")
    sub.add_parser("sql").add_argument("query")
    a = ap.parse_args()
    {"ask": ask, "eval": evaluate, "sql": sql}[a.cmd](a)
