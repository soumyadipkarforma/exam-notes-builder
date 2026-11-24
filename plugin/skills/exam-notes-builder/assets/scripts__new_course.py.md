# scripts/new_course.py

Save as `scripts/new_course.py`

````python
"""Create the folder and every starting file for a new course, so no phase starts from a blank page.

Usage:
  python new_course.py <course_dir> --code "PHY101" --title "Classical Mechanics" --short "Mechanics" \
      --term "B.Sc. Physics, Semester I" [--layout classic|palatino|modern] --chapters "c1_kinematics:Kinematics" "c2_newton:Newton's Laws"
  python new_course.py --selftest

Creates (never overwrites an existing non-empty folder):
  main.tex (from templates/main.tex, filled in), ocwnotes.sty, one stub per chapter
  (\\chapter{Title}\\label{ch:<key>}), c0_guide/cA_pyq/cB_fullmarks/cC_formulas stubs,
  PROGRESS.md (phase table), COVERAGE.md, syllabus_checklist.tsv, core.txt,
  sources/books/, sources/papers/, sources/papers.md, sources/census.md.
Then run:  python gates.py <course_dir>   (an empty book must already build).
Layouts: classic (Times, default), palatino (Palatino), modern (Times, sans-serif headings); all share the
same sizes, spacing and boxes, so the layout can be changed later by editing one word in main.tex.

Part of exam-notes-builder by Soumyadip Karforma (https://github.com/soumyadipkarforma/exam-notes-builder).
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "..", "templates")
LAYOUTS = ("classic", "palatino", "modern")
BRAND = "Made with exam-notes-builder by Soumyadip Karforma: https://github.com/soumyadipkarforma/exam-notes-builder"

PROGRESS = """<!-- {brand} -->
# PROGRESS: {title} ({code})
One line per phase. Update the line when a gate passes. Never mark a gate passed without running its check.

| Phase | Gate | Status | Date | What is left |
|---|---|---|---|---|
| S Tools | every tool check succeeds; versions below | todo | | |
| 0 Intake | syllabus verbatim, exam pattern from a real paper, book list | todo | | |
| 1 Sources | every past question typed and mapped (sources/papers.md, sources/census.md) | todo | | |
| 2 Coverage | every COVERAGE.md row has a planned place; syllabus_checklist.tsv written | todo | | |
| 3 Chapters | each chapter builds; syllabus_check.py reports nothing missing | todo | | |
| 4 Appendices | gates.py: ALL GATES PASS | todo | | |
| 5 Verify | every answer re-derived; zero open issues | todo | | |
| 6 Mock exams | latest grade report: zero N, zero R | todo | | |
| 7 Visual | full contact-sheet pass, every report fixed or rejected by zoom | todo | | |
| 8 Exam Core | core built, PDFs copied, honest report given | todo | | |

## Tool versions (Phase S)

## Syllabus (verbatim, Phase 0)

## Exam pattern (from a real paper, Phase 0)

## Books (Phase 0)
"""

COVERAGE = """<!-- {brand} -->
# COVERAGE: {title} ({code})
| Syllabus line (verbatim) | Book sections | Past questions (paper Q) | Planned place in notes | Done |
|---|---|---|---|---|
"""

PAPERS = "# Past papers, transcribed\nFormat: `PAPER | Q | marks | question text verbatim | syllabus line`\n\n"
CENSUS = ("# Question-type census\n| # | Question type | Syllabus line | Count | Papers | Where |\n|---|---|---|---|---|---|\n")


def stub(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def create(d, code, title, short, term, chapters, layout="classic"):
    if layout not in LAYOUTS:
        sys.exit("FAIL: --layout must be one of %s" % ", ".join(LAYOUTS))
    if os.path.isdir(d) and os.listdir(d):
        sys.exit("FAIL: %s exists and is not empty; refusing to overwrite." % d)
    for sub in ("", "sources", os.path.join("sources", "books"), os.path.join("sources", "papers")):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    shutil.copy(os.path.join(TPL, "ocwnotes.sty"), d)
    shutil.copy(os.path.join(TPL, "syllabus_checklist.tsv"), d)
    shutil.copy(os.path.join(TPL, "core.txt"), d)
    keys = []
    for spec in chapters:
        fname, _, ctitle = spec.partition(":")
        key = fname.split("_", 1)[-1]
        keys.append(fname)
        stub(os.path.join(d, fname + ".tex"),
             "\\chapter{%s}\\label{ch:%s}\n%% Write this chapter in the order of reference/chapter-structure.md.\n%% %s\n" % (ctitle or key, key, BRAND))
    for fname, ctitle, key in (("c0_guide", "How to Use These Notes", "guide"), ("cA_pyq", "Solved Past Papers", "pyq"),
                               ("cB_fullmarks", "Writing Answers for Full Marks", "fullmarks"),
                               ("cC_formulas", "Formula Sheet", "formulas")):
        stub(os.path.join(d, fname + ".tex"), "\\chapter{%s}\\label{ch:%s}\n%% To be written.\n" % (ctitle, key))
    main = open(os.path.join(TPL, "main.tex"), encoding="utf-8").read()
    head = "%s\\ \\textperiodcentered\\ %s" % (code, term)
    main = (main.replace("<<Course code>>\\ \\textperiodcentered\\ <<Programme>>\\ \\textperiodcentered\\ <<Term>>", head)
                .replace("<<Short course name>>", short).replace("<<Course title>>", title)
                .replace("\\usepackage[classic]{ocwnotes}", "\\usepackage[%s]{ocwnotes}" % layout))
    lines = []
    for ln in main.splitlines():
        if ln.startswith("\\include{c1_<<topic>>}"):
            lines += ["\\include{%s}" % k for k in keys]
        elif ln.startswith("% one \\include per chapter"):
            continue
        else:
            lines.append(ln)
    stub(os.path.join(d, "main.tex"), "\n".join(lines) + "\n")
    fmt = dict(title=title, code=code, brand=BRAND)
    stub(os.path.join(d, "PROGRESS.md"), PROGRESS.format(**fmt))
    stub(os.path.join(d, "COVERAGE.md"), COVERAGE.format(**fmt))
    stub(os.path.join(d, "sources", "papers.md"), PAPERS)
    stub(os.path.join(d, "sources", "census.md"), CENSUS)
    print("created %s (%s layout) with %d chapters. Next: python gates.py %s" % (d, layout, len(keys), d))


def opt(argv, name, default=""):
    return argv[argv.index(name) + 1] if name in argv else default


def selftest():
    d = os.path.join(tempfile.mkdtemp(), "course")
    create(d, "X1", "Test Course", "Test", "Term 1", ["c1_alpha:Alpha", "c2_beta:Beta Topic"], "palatino")
    main = open(os.path.join(d, "main.tex"), encoding="utf-8").read()
    assert "\\usepackage[palatino]{ocwnotes}" in main and "Soumyadip Karforma" in main, main[:300]
    assert "Soumyadip Karforma" in open(os.path.join(d, "PROGRESS.md"), encoding="utf-8").read()
    assert "\\include{c1_alpha}" in main and "\\include{c2_beta}" in main and "<<" not in main.split("\\begin{document}")[0], main
    assert "\\label{ch:beta}" in open(os.path.join(d, "c2_beta.tex"), encoding="utf-8").read()
    for f in ("ocwnotes.sty", "PROGRESS.md", "COVERAGE.md", "core.txt", "syllabus_checklist.tsv", "cA_pyq.tex"):
        assert os.path.exists(os.path.join(d, f)), f
    shutil.rmtree(os.path.dirname(d))
    print("selftest ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest()
    elif not a or a[0].startswith("--"):
        sys.exit(__doc__)
    else:
        chs = []
        if "--chapters" in a:
            i = a.index("--chapters") + 1
            while i < len(a) and not a[i].startswith("--"):
                chs.append(a[i]); i += 1
        create(a[0], opt(a, "--code", "CODE"), opt(a, "--title", "Course Title"), opt(a, "--short", "Course"),
               opt(a, "--term", "Term"), chs or ["c1_topic:First Topic"], opt(a, "--layout", "classic"))
````
