r"""Check that a built notes PDF still contains everything in its LaTeX sources.

Usage: python content_check.py <notes_dir> [<notes_dir> ...]
Checks, per notes folder (main.tex + included chapters, main.pdf must be built):
  1. every \include'd file exists and its \chapter title is in the PDF
  2. every \section / \subsection title is in the PDF
  3. every example title and keybox title is in the PDF
  4. number of \begin{example} == number of "Example N.M" labels in the PDF
  5. word volume: PDF words vs source prose words (a large drop means lost text)
Titles are compared on their plain words (LaTeX commands and maths removed).
"""
import re, subprocess, sys, os


def plain(s):
    s = re.sub(r"\\(ref|eqref|label|cite|pageref)\{[^}]*\}", " ", s)  # cross-refs print as numbers
    s = re.sub(r"\\[\^'\"`~]\{?[A-Za-z]\}?|[^\x00-\x7f]", "", s)  # accented letters: drop on both sides (H\^opital vs Hôpital)
    s = re.sub(r"\b(sin|cos|tan|cot|sec|csc|sinh|cosh|tanh|log|exp|ln)\b", " ", s)  # maths names print as text in PDF
    s = re.sub(r"\$[^$]*\$", " ", s)                 # inline maths
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)  # commands
    s = re.sub(r"[{}\\~^_&%]", " ", s)
    return [w.lower() for w in re.findall(r"[A-Za-z]{3,}", s)]


def title_args(src, pattern):
    """Return the balanced-brace argument after each match of pattern."""
    out = []
    for m in re.finditer(pattern, src):
        i, depth, j = m.end(), 1, m.end()
        while j < len(src) and depth:
            depth += {"{": 1, "}": -1}.get(src[j], 0); j += 1
        out.append(src[i:j - 1])
    return out


def opt_args(src, env):
    out = []
    for m in re.finditer(r"\\begin\{" + env + r"\}\[", src):
        i, depth, j = m.end(), 1, m.end()
        while j < len(src) and depth:
            depth += {"[": 1, "]": -1}.get(src[j], 0); j += 1
        out.append(src[i:j - 1])
    return out


def check(d):
    main = open(os.path.join(d, "main.tex"), encoding="utf-8").read()
    files = re.findall(r"^\\include\{([^}]+)\}", main, re.M)
    pdf = subprocess.run(["pdftotext", os.path.join(d, "main.pdf"), "-"], capture_output=True,
                         text=True, encoding="utf-8", errors="ignore").stdout
    pdf_words = " ".join(plain(pdf.replace("-\n", "")))
    problems, n_items, n_examples, src_words = [], 0, 0, 0
    for f in files:
        p = os.path.join(d, f + ".tex")
        if not os.path.exists(p):
            problems.append(f"missing file {f}.tex"); continue
        src = open(p, encoding="utf-8").read()
        src = re.sub(r"(?<!\\)%.*", "", src)
        src_words += len(plain(re.sub(r"\\begin\{(tikzpicture|axis)\}.*?\\end\{\1\}", " ", src, flags=re.S)))
        n_examples += len(re.findall(r"\\begin\{example\}", src))
        items = [("chapter", t) for t in title_args(src, r"\\chapter(?:\[[^\]]*\])?\{")]
        items += [("section", t) for t in title_args(src, r"\\(?:sub)?section\*?\{")]
        items += [("example", t) for t in opt_args(src, "example")]
        items += [("keybox", t) for t in opt_args(src, "keybox")]
        for kind, t in items:
            w = plain(t)
            if len(w) < 2: continue          # nothing checkable (pure maths or one word)
            n_items += 1
            key = " ".join(w[:6])
            if key not in pdf_words:
                problems.append(f"{f}: {kind} not found in PDF: {t[:70]}")
    pdf_examples = len(set(re.findall(r"Example (\d+\.\d+)", pdf)))
    if pdf_examples != n_examples:
        problems.append(f"examples in sources {n_examples}, distinct example labels in PDF {pdf_examples}")
    ratio = len(pdf_words.split()) / max(src_words, 1)
    print(f"{d}: {len(files)} files, {n_items} titles checked, {n_examples} examples, "
          f"PDF/source word ratio {ratio:.2f}")
    if ratio < 0.85:
        problems.append(f"PDF has much less text than the sources (ratio {ratio:.2f})")
    for pr in problems:
        print("  PROBLEM:", pr)
    if not problems:
        print("  OK: nothing missing")
    return not problems


if __name__ == "__main__":
    ok = all([check(d) for d in sys.argv[1:]])
    sys.exit(0 if ok else 1)
