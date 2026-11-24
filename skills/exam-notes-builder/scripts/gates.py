"""Build a LaTeX book and check the build gates, with plain PASS/FAIL output and fix hints.

Usage:
  python gates.py <notes_dir or file.tex> [--max-overfull 3] [--no-build]
  python gates.py --selftest

Builds with latexmk if it works, otherwise pdflatex three times (MiKTeX without Perl).
Then reads the .log and checks:
  1. errors            (lines starting with "!")       must be 0
  2. undefined         (references, citations, macros) must be 0
  3. overfull boxes    wider than --max-overfull pt     must be 0
Each problem is printed with the source file and line LaTeX reports, plus a hint.
Exit code 0 when every gate passes, 1 otherwise. Works on Windows, macOS and Linux.
"""
import os
import re
import shutil
import subprocess
import sys

HINTS = [
    (r"Unicode character .*U\+000[0-9A-F]\)|Text line contains an invalid character", "An invisible control character in the source: a shell turned a backslash sequence (\\v, \\f, \\t, \\b) into one. Retype the macro with a file-editing tool or a Python script, never through sed/echo/heredoc."),
    (r"Package \S+ Error: .*undefined in families|Unknown option", "A package was given an option it does not have. Remove the option (check the package documentation) or use the package's own option name."),
    (r"Undefined control sequence", "A macro is not defined. Check spelling, or define it in main.tex with \\providecommand. If it looks like 'rac' instead of '\\frac', a shell ate the backslash: edit with a file tool or Python, never sed/heredoc."),
    (r"Missing \$ inserted", "Maths used outside $...$ (e.g. _ or ^ in text), or a blank line inside a display."),
    (r"Extra \}|Missing \} inserted|Runaway argument|File ended while scanning", "Unbalanced braces { }. Count them on the reported line and the line before."),
    (r"Environment .* undefined", "Unknown \\begin{...}. Use only environments from ocwnotes.sty: definition, theorem, example, solution, remark, keybox, tipbox, psetbox, ftab."),
    (r"\\begin\{.*\} on input line .* ended by \\end", "A \\begin{X} is closed by the wrong \\end{Y}. Match every begin/end pair."),
    (r"Misplaced alignment tab", "An & outside a table or align environment. Write \\& in text."),
    (r"File `.*' not found", "Missing file: an \\include/\\input name or an image path is wrong, or a package is not installed."),
    (r"Reference .* undefined", "\\ref to a label that does not exist yet. grep for \\label{ and use the real key, or write the target chapter first."),
    (r"Citation .* undefined", "\\cite without a bibliography entry. These notes should not cite: write the content instead."),
    (r"Overfull", "Too wide. Split a long display with aligned/&=, move long inline maths to a display, use width=0.8\\linewidth for plots, tabularx for tables. Never shrink the font."),
]


def hint(msg):
    for pat, h in HINTS:
        if re.search(pat, msg):
            return h
    return "Read the log around this line; fix the first error first, then rebuild."


def run(cmd, cwd):
    try:
        return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900).returncode
    except (OSError, subprocess.TimeoutExpired):
        return None


def build(tex):
    d, name = os.path.dirname(os.path.abspath(tex)), os.path.basename(tex)
    if shutil.which("latexmk"):
        rc = run(["latexmk", "-pdf", "-interaction=nonstopmode", name], d)
        if rc is not None and os.path.exists(os.path.join(d, name[:-4] + ".log")):
            return
    if not shutil.which("pdflatex"):
        sys.exit("FAIL: neither latexmk nor pdflatex found. Install a TeX distribution (Phase S of SKILL.md).")
    for _ in range(3):
        run(["pdflatex", "-interaction=nonstopmode", name], d)


PROJECT = set()  # basenames of the book's own .tex files; set in main()


def source_at(log, pos):
    """Name of the book's .tex file LaTeX had open at log position pos (approximate: last one opened before pos)."""
    files = [os.path.basename(f.replace("\\", "/"))
             for f in re.findall(r"\(([^()\n]*?\.tex)(?=[\s)])", log[:pos])]  # paths may contain spaces
    own = [f for f in files if not PROJECT or f in PROJECT]  # skip package files such as tcbposter.code.tex
    return own[-1] if own else "?"


def parse(log, max_overfull=3.0):
    log = log.replace("\r\n", "\n")
    log = re.sub(r"(?m)^(.{79})\n", r"\1", log)  # TeX wraps log lines at 79 chars; rejoin long paths
    errors, undefined, overfull = [], [], []
    for m in re.finditer(r"^! (.*)$", log, re.M):
        line = re.search(r"^l\.(\d+)", log[m.end():m.end() + 2000], re.M)
        errors.append((source_at(log, m.start()), line.group(1) if line else "?", m.group(1)))
    for m in re.finditer(r"LaTeX Warning: (Reference|Citation) `([^']+)' on page \S+ undefined on input line (\d+)", log):
        undefined.append((source_at(log, m.start()), m.group(3), "%s `%s' undefined" % (m.group(1), m.group(2))))
    for m in re.finditer(r"Overfull \\hbox \(([\d.]+)pt too wide\) (?:in paragraph at lines (\d+)--\d+|detected at line (\d+))", log):
        if float(m.group(1)) > max_overfull:
            overfull.append((source_at(log, m.start()), m.group(2) or m.group(3), "Overfull by %spt" % m.group(1)))
    return errors, undefined, overfull


def report(errors, undefined, overfull, max_overfull):
    ok = True
    for name, items in (("errors", errors), ("undefined references/citations", undefined),
                        ("overfull boxes > %gpt" % max_overfull, overfull)):
        seen = []
        for it in items:
            if it not in seen:
                seen.append(it)
        print("%s %s: %d" % ("PASS" if not seen else "FAIL", name, len(seen)))
        for f, line, msg in seen[:15]:
            print("   %s line %s: %s\n      hint: %s" % (f, line, msg, hint(msg)))
        if len(seen) > 15:
            print("   ... %d more (fix these first, then rebuild)" % (len(seen) - 15))
        ok = ok and not seen
    print("ALL GATES PASS" if ok else "GATES FAIL: fix the FIRST problem listed, rebuild, run gates again.")
    return ok


def selftest():
    log = ("(./main.tex (./c1_intro.tex\n! Undefined control sequence.\nl.12 \\vom\n"
           "LaTeX Warning: Reference `ch:x' on page 3 undefined on input line 40.\n"
           "Overfull \\hbox (2.5pt too wide) in paragraph at lines 5--6\n"
           "Overfull \\hbox (13.2pt too wide) detected at line 77\n))")
    e, u, o = parse(log, 3)
    assert e == [("c1_intro.tex", "12", "Undefined control sequence.")], e
    assert u == [("c1_intro.tex", "40", "Reference `ch:x' undefined")], u
    assert o == [("c1_intro.tex", "77", "Overfull by 13.2pt")], o
    assert "backslash" in hint("Undefined control sequence.")
    print("selftest ok")


def main(argv):
    if "--selftest" in argv:
        return selftest()
    mo = 3.0
    if "--max-overfull" in argv:
        i = argv.index("--max-overfull")
        mo = float(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    tex = args[0]
    if os.path.isdir(tex):
        tex = os.path.join(tex, "main.tex")
    if not os.path.exists(tex):
        sys.exit("FAIL: %s not found" % tex)
    PROJECT.update(f for f in os.listdir(os.path.dirname(os.path.abspath(tex))) if f.endswith(".tex"))
    if "--no-build" not in argv:
        build(tex)
    logf = tex[:-4] + ".log"
    if not os.path.exists(logf):
        sys.exit("FAIL: no log file %s (the build did not run)" % logf)
    log = open(logf, encoding="latin-1").read()
    ok = report(*parse(log, mo), mo)
    d = os.path.dirname(os.path.abspath(tex))
    left = [f for f in sorted(os.listdir(d)) if f.endswith(".tex") and
            re.search(r"<<[^>]*>>|To be written", open(os.path.join(d, f), encoding="utf-8", errors="replace").read())]
    if left:
        print("WARN unfinished placeholders (<<...>> or 'To be written') in: " + ", ".join(left))
    pdf = tex[:-4] + ".pdf"
    if os.path.exists(pdf):
        print("PDF: %s" % pdf)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
