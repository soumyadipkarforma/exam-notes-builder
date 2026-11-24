# LaTeX pitfalls and checks

## Build
`python scripts/gates.py <notes_dir>` does all of this (latexmk, or pdflatex three times without Perl) and prints PASS/FAIL with file, line and a fix hint. By hand:
```
latexmk -pdf -interaction=nonstopmode main.tex
grep -c '^!' main.log                       # errors: must be 0
grep -ci 'undefined' main.log               # undefined refs/macros: must be 0
grep -oE 'Overfull .hbox \(([0-9.]+)pt' main.log | grep -oE '[0-9.]+' | awk '$1>3'   # must print nothing
latexmk -c                                   # clean when done
```

## Errors met before, and fixes
| Symptom | Cause | Fix |
|---|---|---|
| `\frac` turns into `rac` or a form feed in a file | shell `sed`/heredoc ate backslashes | edit with an editor tool or a Python script file using raw strings |
| `Undefined control sequence \vom` | macro defined in one book's preamble, used in another | define subject macros in each `main.tex` |
| `Reference ch:vector_algebra undefined` | label renamed | grep for `\label{` and use the real key |
| Running head overflows | long chapter title | short title: `\chapter[Short]{Long title}` |
| Table 15 pt too wide | full-width `tabularx` took the paragraph indent | `\BeforeBeginEnvironment{tabularx}{\par\noindent}` (in the style) |
| Table 200 pt too wide in a box | box title run into the first line, then a full-width table | box title on its own line (`attach title to upper={\par\smallskip}`) |
| Long cell will not wrap | inline maths cannot break | split the formula or use `X` columns with `\raggedright` |
| Display equation too wide | too many terms on one line | `aligned` with `&=` breaks, or a second display |
| Long inline equation sticks out | inline maths cannot break | move it to a display |
| Plot too wide | fixed `width=13cm` | `width=0.8\linewidth` |
| `tabular` in a box overflows | fixed `p{}` widths add up to more than the box | `tabularx{\linewidth}` with an `X` column |

## Content check after any layout change
Layout edits must not lose content. Run a check that every `\section`, `\subsection`, example title and keybox title in the `.tex` sources appears in `pdftotext main.pdf -` (normalise spaces and drop LaTeX markup and maths before comparing), that the number of `\begin{example}` in the sources equals the number of "Example N.M" labels in the PDF, and that every `\include`d file appears in the table of contents. `scripts/content_check.py` in this skill does this.

## Figure labels crossed by curves (pgfplots)
`every node/.append style={...}` given in axis options does **not** reach `\node` commands inside the axis, and curves drawn after a label cover it. Fix for a chapter full of graphs: wrap the chapter in `\begingroup ... \endgroup` with `\tikzset{every node/.append style={fill=white,inner sep=1pt,font=\small}}` at the top, and put every `\node` after the last `\addplot` of its axis. Do not use `axis on top` with this: tick numbers would then cover the labels. Do not set the white fill in the house style file globally: it would hide shaded regions in other figures.
