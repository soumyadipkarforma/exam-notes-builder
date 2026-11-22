"""Notes-only RAG exam: tiny local models answer mock papers using retrieved chunks of the notes.
Works with any OpenAI-compatible server that has /embeddings and /chat/completions (Lemonade, llama.cpp
server, Ollama's OpenAI endpoint, LM Studio).

Usage: python rag_exam.py <model> <paper.md> <notes_dir>[,<notes_dir>...] <out.md>
Env:   RAG_API   (default http://127.0.0.1:13305/api/v1, Lemonade)
       RAG_EMBED (default nomic-embed-text-v1-GGUF; uses the search_document:/search_query: prefixes)
"""
import json, math, os, re, sys, urllib.request, urllib.error

API = os.environ.get("RAG_API", "http://127.0.0.1:13305/api/v1")
EMB = os.environ.get("RAG_EMBED", "nomic-embed-text-v1-GGUF")
TOPK = 6


def post(path, body, timeout=900):
    req = urllib.request.Request(API + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def chunks_for(d):
    out, subj = [], os.path.basename(os.path.normpath(d))
    for f in sorted(os.listdir(d)):
        if not f.endswith(".tex") or f in ("main.tex", "core_main.tex"):
            continue
        text = open(os.path.join(d, f), encoding="utf-8").read()
        # split at sections/subsections/examples so each chunk is one idea
        parts = re.split(r"(?=\\(?:section|subsection|subsubsection)\*?\{|\\begin\{example\})", text)
        buf = ""
        for p in parts:
            if len(buf) + len(p) > 1200 and buf:
                out.append((f"{subj}/{f}", buf)); buf = ""
            buf += p
            while len(buf) > 1500:  # hard cap, with overlap
                out.append((f"{subj}/{f}", buf[:1400])); buf = buf[1100:]
        if buf.strip():
            out.append((f"{subj}/{f}", buf))
    return out


def embed(texts):
    vecs = []
    for t in texts:  # one at a time: the embedder's batch is 512 tokens
        n = 800
        while True:
            try:
                r = post("/embeddings", {"model": EMB, "input": [t[:n]]}); break
            except urllib.error.HTTPError:
                if n < 100: raise
                n //= 2  # shortcut: LaTeX tokenises densely, so halve until it fits the 512-token batch
        vecs.append(r["data"][0]["embedding"])
    return vecs


def index(d):
    cache = os.path.join(os.path.dirname(os.path.abspath(sys.argv[4])), f"index_{os.path.basename(os.path.normpath(d))}.json")
    ch = chunks_for(d)
    if os.path.exists(cache):
        data = json.load(open(cache))
        if len(data["chunks"]) == len(ch) and [c[1] for c in data["chunks"]] == [c[1] for c in ch]:
            return data
    data = {"chunks": ch, "vecs": embed(["search_document: " + c[1] for c in ch])}
    json.dump(data, open(cache, "w"))
    return data


def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) + 1e-9)


def words(s):
    return set(w for w in re.findall(r"[a-z]{4,}", s.lower()))


def retrieve(idx, q):
    qv = embed(["search_query: " + q])[0]
    qw = words(q)
    scored = []
    for (src, txt), v in zip(idx["chunks"], idx["vecs"]):
        kw = len(qw & words(txt)) / (len(qw) + 1)
        scored.append((cos(qv, v) + 0.3 * kw, src, txt))
    scored.sort(reverse=True)
    return scored[:TOPK]


def parse_paper(path):
    """Yield (label, question text) for every part."""
    q, items = None, []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip()
        m = re.match(r"^Q(\d+)\.\s*(.*)", line)
        if m:
            q = m.group(1); stem = m.group(2); continue
        m = re.match(r"^\(([a-z])\)\s*(.*)", line)
        if m and q:
            items.append((f"Q{q}({m.group(1)})", m.group(2)))
    return items


SYS = ("You are a student writing a university exam. You know NOTHING except the "
       "study-notes excerpts given to you (LaTeX source). Use only methods, facts and results that appear "
       "in the excerpts. Write a complete exam answer: state the law, theorem, rule or source used, show every "
       "step of the working or argument, give numbers with units, and clearly mark the final answer. If the excerpts do not "
       "contain something you need, write a line 'NOT IN NOTES: <what is missing>' and then do your best.")


def main():
    model, paper, dirs, out = sys.argv[1:5]
    subs = dirs.split(",")
    subj = ", ".join(os.path.basename(os.path.normpath(s)) for s in subs)
    idxs = {s: index(s) for s in subs}
    parts = parse_paper(paper)
    done = set()
    if os.path.exists(out):
        done = set(re.findall(r"^## (Q\d+\([a-z]\))", open(out, encoding="utf-8").read(), re.M))
    fh = open(out, "a", encoding="utf-8")
    if not done:
        fh.write(f"# Answers: {os.path.basename(paper)} by {model} (RAG over {subj} notes, top {TOPK} chunks)\n\n")
    for label, qtext in parts:
        if label in done:
            continue
        hits = []
        for s in subs:
            hits += retrieve(idxs[s], qtext)
        hits.sort(reverse=True)
        hits = hits[:TOPK]
        ctx = "\n\n".join(f"[Excerpt {i+1}: {src}]\n{txt}" for i, (_, src, txt) in enumerate(hits))
        user = f"NOTES EXCERPTS:\n{ctx}\n\nEXAM QUESTION {label}: {qtext}\n\nWrite your full answer."
        if "qwen3" in model.lower():
            user += " /no_think"
        try:
            r = post("/chat/completions", {"model": model, "temperature": 0.2, "max_tokens": 1400,
                                           "messages": [{"role": "system", "content": SYS},
                                                        {"role": "user", "content": user}]})
            ans = r["choices"][0]["message"]["content"]
        except Exception as e:  # keep going; grader sees the failure
            ans = f"[GENERATION FAILED: {e}]"
        ans = re.sub(r"<think>.*?</think>", "", ans, flags=re.S).strip()
        fh.write(f"## {label}\n**Q:** {qtext}\n\n*Retrieved:* {', '.join(src for _, src, _ in hits)}\n\n{ans}\n\n")
        fh.flush()
        print(label, "done", flush=True)


if __name__ == "__main__":
    main()
