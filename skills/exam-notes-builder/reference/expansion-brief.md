# Brief template: fill the gaps in one chapter (no bloat)

Copy to the course folder, fill the `<<...>>`, and give it to one agent per chapter (or 2 small chapters).

---
You are improving existing LaTeX exam notes for <<course, institution, term>>. The notes must let a student who never opens the textbook answer any exam question, old or new, and write it so a strict examiner cannot deduct marks. The chapters are correct but too terse in places.

## Your job
Add **what is needed and nothing else**:
1. **Missing derivations / proofs / model answers.** Everything the syllabus or a past paper could ask to derive, prove, explain or justify is written in full: every step, the rule or source named at each step, and the figure/diagram the examiner expects. Fill in skipped steps that carry marks.
2. **Missing topics and question types.** Compare the chapter with its syllabus lines (`<<guide chapter file>>`), the solved past papers (`<<past-paper appendix file>>`) and the prescribed books on disk. Add any standard result, method or question type that is missing.
3. **Missing explanation where a method is bare.** 2–5 sentences saying what it is, why it works, and when to use it (how to recognise the question). Only where missing.
4. **Missing worked examples.** At least one per method; full solution, final answer marked, one-line interpretation. Check every number with `python -I -c "..."`.

Do **not**: rewrite or delete correct content, change existing `\label`s, add filler, repeat what is there, add off-syllabus topics unless past papers ask them, or invent past-paper questions/years (label your own "practice").

## Where things go
Follow the chapter structure already used (`<skill>/reference/chapter-structure.md`). Use only environments and macros that exist (`<<list>>`). Read `<skill>/reference/style-rules.md` and `<skill>/reference/subject-adaptation.md` once.

## Sources on disk
<<book files and syllabus file>>. Read pages with `pdftotext -f N -l M "file.pdf" -` (find pages with grep first; keep reads short).

## Editing and building
- Edit **only your assigned file(s)**; others are editing other chapters at the same time.
- Edit `.tex` with the Edit/Write tools, never shell `sed`/heredocs.
- Build into your own folder: `latexmk -pdf -interaction=nonstopmode -outdir=_build_<<name>> main.tex` (or `pdflatex -output-directory=...` three times). Require 0 lines starting `!`, nothing undefined from your files, no overfull box > 3 pt from your files. Then delete `_build_<<name>>` (literal name).

## Report (short)
What you added (titles), what you filled in, anything you could not add, and confirmation of the build gates.
