# scripts/build_core.py

Save as `scripts/build_core.py`

````python
r"""Build an "Exam Core" book from a full notes book (no new content: everything is extracted).

Usage: python build_core.py <notes_dir>     -> writes <notes_dir>/core_main.tex and <notes_dir>/core/*.tex
Per chapter it keeps:
  * must-know sections in full (title matches 'must:' in <notes_dir>/core.txt) and the "Concepts and strategy" section;
  * from every other section: its keyboxes and its past-paper examples (title has a year/paper tag) with solutions.
Appendices: formula sheet and full-marks guide in full. Refs to labels not in the core print "(full notes)".
shortcut: section choice is by title regex; edit core.txt when chapters are renamed.
"""
import os, re, sys

PAST_DEFAULT = r"\b(19|20)\d\d\b|past paper|PYQ"


def load_cfg(d):
    """<notes_dir>/core.txt: 'must: <regex of section/subsection titles kept in full>', optional 'past: <regex>'."""
    cfg = {"past": PAST_DEFAULT}
    for line in open(os.path.join(d, "core.txt"), encoding="utf-8"):
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            cfg[k.strip()] = v.strip()
    assert "must" in cfg, "core.txt needs a 'must:' line"
    return cfg["must"], re.compile(cfg["past"])


KEYBOX = re.compile(r"\\begin\{keybox\}.*?\\end\{keybox\}", re.S)
EXAMPLE = re.compile(r"\\begin\{example\}(\[[^\n]*?\])?.*?\\end\{example\}(\s*\\begin\{solution\}.*?\\end\{solution\})?", re.S)
PSET = re.compile(r"\\begin\{psetbox\}.*?\\end\{psetbox\}", re.S)

REFFIX = r"""
% refs to material left out of the core point back to the full notes
\makeatletter
\AtBeginDocument{%
\let\coreoldref\ref \renewcommand{\ref}[1]{\@ifundefined{r@#1}{(full notes)}{\coreoldref{#1}}}%
\let\coreoldeqref\eqref \renewcommand{\eqref}[1]{\@ifundefined{r@#1}{(full notes)}{\coreoldeqref{#1}}}}
\makeatother
"""

INTRO = r"""\chapter{How to Use the Exam Core}
This is the short version of the full notes: everything here is copied from them, nothing is new.
\begin{itemize}
\item \textbf{Must-know derivations} appear in full, exactly as you should write them in the exam.
\item \textbf{Key-result boxes} from every other section give the results you quote.
\item \textbf{Past-paper examples} (marked with their year) show every question type DU has set.
\item \textbf{Concepts and strategy} at the end of each chapter tells you how to recognise and attack each question.
\end{itemize}
Learn this book first. When something here is unclear, or a reference says ``(full notes)'', open the same chapter of the full notes.
The formula sheet and the full-marks guide are at the end.
"""


def braced(s):
    """Return (text inside the first {...} of s, index just after it), respecting nested braces."""
    i = s.find("{")
    depth = 0
    for j in range(i, len(s)):
        depth += {"{": 1, "}": -1}.get(s[j], 0)
        if depth == 0:
            return s[i + 1:j], j + 1
    raise ValueError("unbalanced braces: " + s[:80])


def chapter_core(src, must, PAST):
    src = PSET.sub("", re.sub(r"(?<!\\)%.*", "", src))
    parts = re.split(r"(?=\\section\*?\{)", src)
    out = [parts[0].strip()]  # chapter heading, intro and chapter-level macros
    for p in parts[1:]:
        title, end = braced(p)
        if re.search(must, title) or "Concepts and strategy" in title:
            # derivations in full; practice (non past-paper) examples dropped
            out.append(EXAMPLE.sub(lambda e: e.group(0) if e.group(1) and PAST.search(e.group(1)) else "", p).strip())
            continue
        head = p[:end] + (re.match(r"\s*\\label\{[^}]*\}", p[end:]) or re.match("", "")).group(0)
        body = []
        for i, sp in enumerate(re.split(r"(?=\\subsection\*?\{)", p)):
            st = braced(sp)[0] if i else ""
            if i and re.search(must, st):  # must-know subsection: in full, minus practice examples
                body.append(EXAMPLE.sub(lambda e: e.group(0) if e.group(1) and PAST.search(e.group(1)) else "", sp).strip())
                continue
            items = [(k.start(), k.group(0)) for k in KEYBOX.finditer(sp)]
            items += [(e.start(), e.group(0)) for e in EXAMPLE.finditer(sp) if e.group(1) and PAST.search(e.group(1))]
            body += [t for _, t in sorted(items)]
        if body:
            out.append(head + "\n" + "\n\n".join(body))
    return "\n\n".join(out) + "\n"


def build(d):
    name = os.path.basename(os.path.normpath(d))
    must, past = load_cfg(d)
    main = open(os.path.join(d, "main.tex"), encoding="utf-8").read()
    files = re.findall(r"^\\include\{([^}]+)\}", main, re.M)
    os.makedirs(os.path.join(d, "core"), exist_ok=True)
    inc = ["core/c_intro"]
    open(os.path.join(d, "core", "c_intro.tex"), "w", encoding="utf-8").write(INTRO)
    appendix_done = False
    for f in files:
        src = open(os.path.join(d, f + ".tex"), encoding="utf-8").read()
        if re.search(r"guide|pyq|questions|school", f):
            continue
        if re.search(r"formulas|fullmarks", f):
            if not appendix_done:
                inc.append("APPENDIX"); appendix_done = True
            open(os.path.join(d, "core", "c_" + f + ".tex"), "w", encoding="utf-8").write(src)
        else:
            open(os.path.join(d, "core", "c_" + f + ".tex"), "w", encoding="utf-8").write(chapter_core(src, must, past))
        inc.append("core/c_" + f)
    pre, body = main.split(r"\begin{document}", 1)
    body = re.sub(r"^\\include\{[^}]+\}\s*$\n?", "", body, flags=re.M)
    body = body.replace(r"\appendix", "")
    body = re.sub(r"\{Complete Exam Notes\}", "{Exam Core: what to learn for full marks}", body)
    lines = "\n".join(r"\appendix" if i == "APPENDIX" else r"\include{%s}" % i for i in inc)
    body = body.replace(r"\end{document}", lines + "\n\\end{document}")
    open(os.path.join(d, "core_main.tex"), "w", encoding="utf-8").write(pre + REFFIX + r"\begin{document}" + body)
    print(name, "core files:", len(inc) - 1)


if __name__ == "__main__":
    for d in sys.argv[1:]:
        build(d)
````
