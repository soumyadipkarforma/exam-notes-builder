# Exam Notes Builder

An agent skill that turns a **syllabus + textbooks + past papers** into **complete, examiner-proof exam notes** (LaTeX → PDF) for any course, proves they are complete with notes-only mock exams graded by a strict examiner, and finishes with a short **Exam Core** revision book.

It works for any subject: physics, mathematics, chemistry, biology, computer science, engineering, economics, law, history, languages. The method is the same; `reference/subject-adaptation.md` says what a "derivation", "figure" or "numerical" becomes in your subject.

## What you get
- **Full notes**: one chapter per syllabus unit, in a fixed order: intuition → definitions → full derivation/proof/model answer with figure → key results → three worked examples (direct, past paper, twisted) → further solved questions → *Concepts and strategy* → problems with answers.
- **Appendices**: every recent past paper solved as model answers, a "writing answers for full marks" guide, a formula/fact sheet.
- **Proof of completeness**: a syllabus checklist, a content check of the PDF, independent re-derivation of every answer, a parallel line-by-line full-marks review, and mock papers (book, old-paper, unseen, cross-course "fusion") sat by weak notes-only test-takers and graded step by step. Every lost mark is classed as a notes gap (fix), a findability problem (fix) or a student slip.
- **Exam Core**: a book about a third of the size, extracted automatically (must-know derivations in full, key-result boxes, every past-paper example, strategy sections, formula sheet).
- A clean, roomy, print-friendly layout (12 pt Times, black and white).

## Use it

### Claude Code
```bash
git clone https://github.com/soumyadipkarforma/exam-notes-builder ~/.claude/skills/exam-notes-builder
```
(Windows: clone into `%USERPROFILE%\.claude\skills\exam-notes-builder`.) Optionally copy `agents/*.md` into your project's `.claude/agents/`. Then, in a folder with your syllabus, books and papers:

> Use the exam-notes-builder skill to make complete exam notes for <course>, <institution>, paper code <code>. The syllabus, books and past papers are in this folder.

### Claude.ai / Claude Desktop
Download this repository as a ZIP and upload it under **Settings → Capabilities → Skills** (code execution must be on). Then ask as above.

### Other agents (Codex, Cursor, Gemini CLI, Aider, ...)
Put this folder in your project and tell the agent: *"Read `exam-notes-builder/SKILL.md` and follow its phases."* `AGENTS.md` points agents there automatically. A small model can follow it one chapter at a time.

### By hand
`SKILL.md` is a readable checklist; the templates and scripts work on their own.

## Requirements
- A TeX distribution with `latexmk`: TeX Live or MiKTeX (on MiKTeX without Perl, run `pdflatex` three times instead).
- Python 3 (standard library only).
- poppler-utils: `pdftotext`, `pdftoppm`.
- Optional, for mock exams with tiny local models: any OpenAI-compatible server with an embeddings endpoint (Lemonade Server, llama.cpp server, Ollama, LM Studio). Tested with 0.6–1.2 B models on a 16 GB laptop.

## Contents
```
SKILL.md                     the procedure: 9 phases, each with a gate
reference/                   style rules, chapter structure, appendices, coverage matrix, mock papers,
                             grading rubric, subject adaptation, expansion and review briefs, LaTeX pitfalls,
                             finding past papers
templates/                   ocwnotes.sty (layout), main.tex (book skeleton),
                             syllabus_checklist.tsv and core.txt (config examples)
scripts/
  content_check.py <dir>     every section/example/box title in the sources appears in the built PDF
  depth_audit.py <dir>       flags sections with too little explanation
  syllabus_check.py <dir>    every item in <dir>/syllabus_checklist.tsv is present in the notes
  build_core.py <dir>        writes <dir>/core_main.tex (the Exam Core) using <dir>/core.txt
  rag_exam.py                notes-only exam with a tiny local model + retrieval
  run_all.sh                 example rotation of models and papers
agents/                      notes-writer, solution-verifier, paper-setter, notes-only-student, strict-grader
```

## Quick script reference
```bash
latexmk -pdf -interaction=nonstopmode main.tex          # build (inside a notes folder)
python scripts/content_check.py Course_Notes            # after layout changes
python scripts/syllabus_check.py Course_Notes           # nothing missing from the syllabus
python scripts/build_core.py Course_Notes && (cd Course_Notes && latexmk -pdf core_main.tex)
RAG_API=http://127.0.0.1:13305/api/v1 python scripts/rag_exam.py <model> paper.md Course_Notes answers/paper__model.md
```

## Origin
Built and battle-tested while writing three ~100–150-page exam books for a first-year university physics programme, including line-by-line review by parallel agents and mock exams sat by 1-billion-parameter models.

## License
MIT. See `LICENSE`.
