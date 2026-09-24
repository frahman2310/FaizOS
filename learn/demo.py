"""Live demonstrations for the LLM-behaviour units. Every number a unit shows comes from here, and every
run is saved to runs/ with its inputs, so the unit checker can trace each number back to a run.

    uv run demo.py next "The capital of Pakistan is" --k 5
    uv run demo.py tokens "withholding tax on non-filers"
    uv run demo.py sample "Name one city in Pakistan:" --temps 0 0.7 1.5 --n 10
    uv run demo.py chat "What did I just tell you my name was?"      # a fresh call, no memory

The model is Qwen2.5-0.5B-Instruct, small and local: its behaviour shows the mechanism, not the quality of
frontier models (units must say so when a result is a small-model effect). Qwen's chat format adds a default
hidden instruction ("You are Qwen, created by Alibaba Cloud...") when no system text is given; chat and sample
runs save the full text sent so units show it. Token counts use two real tokenizers (OpenAI o200k and Qwen); Claude's tokenizer is not
public, so Claude counts come from the dated fact sheet (facts.md), never from here.
"""
import argparse
import datetime
import json
from pathlib import Path

HERE = Path(__file__).parent
RUNS = HERE / "runs"
MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
_cache = {}
NAME = None                     # set by --save


def model():
    if "m" not in _cache:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        dev = "mps" if torch.backends.mps.is_available() else "cpu"
        tok = AutoTokenizer.from_pretrained(MODEL)
        m = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32).to(dev).eval()
        _cache.update(m=m, tok=tok, dev=dev)
    return _cache["m"], _cache["tok"], _cache["dev"]


def save(kind, inputs, output, name=None):
    """Save a run with the exact command that made it; --save NAME gives it a readable file name."""
    import shlex
    import sys
    RUNS.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path = RUNS / (f"{name}.json" if name else f"{stamp}-{kind}.json")
    command = "uv run demo.py " + shlex.join(a for a in sys.argv[1:])
    path.write_text(json.dumps({"kind": kind, "model": MODEL, "command": command, "made": stamp,
                                "inputs": inputs, "output": output}, indent=1, ensure_ascii=False))
    return path


def next_tokens(prompt, k=5):
    """The model's probability for each possible next token, top k."""
    import torch
    m, tok, dev = model()
    ids = tok(prompt, return_tensors="pt").to(dev)
    with torch.no_grad():
        probs = torch.softmax(m(**ids).logits[0, -1].float(), dim=-1)
    top = torch.topk(probs, k)
    out = [{"token": tok.decode([int(i)]), "prob": round(float(p), 4), "percent": round(float(p) * 100, 1)}
           for p, i in zip(top.values, top.indices)]
    return out, save("next", {"prompt": prompt, "k": k, "note": "first-piece chances only; tokens are not whole words"}, out, NAME)


def tokens(text):
    import tiktoken
    _, tok, _ = model()
    o200k = tiktoken.get_encoding("o200k_base")
    out = {
        "characters": len(text),
        "words": len(text.split()),
        "openai_o200k": [o200k.decode([t]) for t in o200k.encode(text)],
        "qwen": [tok.decode([t]) for t in tok(text)["input_ids"]],
    }
    out["openai_o200k_count"] = len(out["openai_o200k"])
    out["qwen_count"] = len(out["qwen"])
    return out, save("tokens", {"text": text}, out, NAME)


def sample(prompt, temps=(0.0, 0.7, 1.5), n=10, max_new=12, seed=0):
    """n answers at each temperature (0 means always take the most likely token)."""
    import torch
    m, tok, dev = model()
    chat = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
    ids = tok(chat, return_tensors="pt").to(dev)
    out = {}
    for t in temps:
        torch.manual_seed(seed)
        answers = []
        for _ in range(n):
            kw = dict(do_sample=False) if t == 0 else dict(do_sample=True, temperature=float(t), top_k=0, top_p=1.0)
            with torch.no_grad():
                g = m.generate(**ids, max_new_tokens=max_new, pad_token_id=tok.eos_token_id, **kw)
            answers.append(tok.decode(g[0, ids["input_ids"].shape[1]:], skip_special_tokens=True).strip())
        out[str(t)] = {"answers": answers, "distinct": len(set(answers))}
    return out, save("sample", {"prompt": prompt, "temps": list(temps), "n": n, "max_new": max_new, "seed": seed,
                                "decoding": "temperature 0 = greedy (always the likeliest token), not the provider's sampler",
                                "full_text_sent": chat}, out, NAME)


def chat(prompt, max_new=40):
    """One fresh call with no earlier messages: shows that the model keeps no memory between calls."""
    m, tok, dev = model()
    text = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
    ids = tok(text, return_tensors="pt").to(dev)
    g = m.generate(**ids, max_new_tokens=max_new, do_sample=False, pad_token_id=tok.eos_token_id)
    out = tok.decode(g[0, ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    return out, save("chat", {"prompt": prompt, "max_new": max_new, "full_text_sent": text}, out, NAME)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("next"); p.add_argument("prompt"); p.add_argument("--k", type=int, default=5)
    p = sub.add_parser("tokens"); p.add_argument("text")
    p = sub.add_parser("sample"); p.add_argument("prompt"); p.add_argument("--temps", type=float, nargs="+", default=[0, 0.7, 1.5])
    p.add_argument("--n", type=int, default=10); p.add_argument("--max-new", type=int, default=12)
    p = sub.add_parser("chat"); p.add_argument("prompt")
    for sp in sub.choices.values():
        sp.add_argument("--save", help="file name for the run, without .json")
    a = ap.parse_args()
    NAME = a.save
    if a.cmd == "next":
        r, path = next_tokens(a.prompt, a.k)
    elif a.cmd == "tokens":
        r, path = tokens(a.text)
    elif a.cmd == "sample":
        r, path = sample(a.prompt, tuple(a.temps), a.n, a.max_new)
    else:
        r, path = chat(a.prompt)
    print(json.dumps(r, indent=1, ensure_ascii=False))
    print(f"(saved {path.relative_to(HERE)})")
