# Exam Notes Builder

An agent skill that turns a **syllabus + textbooks + past papers** into **complete, examiner-proof exam notes** (LaTeX → PDF) for any course, proves they are complete with notes-only mock exams graded by a strict examiner, and finishes with a short **Exam Core** revision book.

It works for any subject: physics, mathematics, chemistry, biology, computer science, engineering, economics, law, history, languages. The method is the same; `reference/subject-adaptation.md` says what a "derivation", "figure" or "numerical" becomes in your subject.

## What you get
- **Full notes**: one chapter per syllabus unit, in a fixed order: intuition → definitions → full derivation/proof/model answer with figure → key results → three worked examples (direct, past paper, twisted) → further solved questions → *Concepts and strategy* → problems with answers.
- **Appendices**: every recent past paper solved as model answers, a "writing answers for full marks" guide, a formula/fact sheet.
- **Proof of completeness**: a syllabus checklist, a content check of the PDF, independent re-derivation of every answer, a parallel line-by-line full-marks review, and mock papers (book, old-paper, unseen, cross-course "fusion") sat by weak notes-only test-takers and graded step by step. Every lost mark is classed as a notes gap (fix), a findability problem (fix) or a student slip.
- **Exam Core**: a book about a third of the size, extracted automatically (must-know derivations in full, key-result boxes, every past-paper example, strategy sections, formula sheet).
- A clean, roomy, print-friendly layout (12 pt Times, black and white).

## Install

### Claude Code (plugin, recommended)
```
/plugin install exam-notes-builder --marketplace soumyadipkarforma/exam-notes-builder
```
(Older Claude Code: `/plugin marketplace add soumyadipkarforma/exam-notes-builder`, then `/plugin install exam-notes-builder@exam-notes-builder`.) The plugin stores its scripts and templates as Markdown; the skill unpacks them into `exam-tools/` on first use.
This installs the skill and its six subagents (notes-writer, solution-verifier, paper-setter, notes-only-student, strict-grader, visual-checker). Then, in a folder with your syllabus, books and papers:

> Use the exam-notes-builder skill to make complete exam notes for <course>, <institution>, paper code <code>. The syllabus, books and past papers are in this folder.

### Claude Code (skill only)
```bash
git clone https://github.com/soumyadipkarforma/exam-notes-builder
cp -r exam-notes-builder/skills/exam-notes-builder ~/.claude/skills/
cp exam-notes-builder/agents/*.md ~/.claude/agents/      # optional subagents
```

### Claude.ai / Claude Desktop
Zip the folder `skills/exam-notes-builder` and upload it under **Settings → Capabilities → Skills** (code execution must be on).

### OpenAI Codex
The repository is also a Codex plugin (root `plugin.json`; skills found in `skills/`) and a Codex marketplace (`.agents/plugins/marketplace.json`). Add it with
```
codex plugin marketplace add soumyadipkarforma/exam-notes-builder
```
then install **exam-notes-builder** from the Plugins Directory in the ChatGPT desktop app ([Codex plugin docs](https://developers.openai.com/codex/plugins)). Skill only: copy `skills/exam-notes-builder` into `~/.codex/skills/` or your project's `.agents/skills/`.

### Gemini CLI
The repository is a Gemini CLI extension (`gemini-extension.json`, context file `GEMINI.md`; the skill in `skills/` is discovered automatically):
```
gemini extensions install https://github.com/soumyadipkarforma/exam-notes-builder
```
([Gemini CLI extension docs](https://geminicli.com/docs/extensions/)). Skill only: copy `skills/exam-notes-builder` into `.gemini/skills/` (project) or `~/.gemini/skills/` (user).

### Cursor, GitHub Copilot, VS Code and other Agent Skills tools
`skills/exam-notes-builder/` follows the open [Agent Skills](https://agentskills.io) format. Copy it into the folder your tool reads, for example `.agents/skills/` (shared by several tools), `.cursor/skills/` (Cursor) or `.github/skills/` (GitHub Copilot).

### Any other agent (Aider, plain chat models, ...)
Put this repository in your project and tell the agent: *"Read `skills/exam-notes-builder/SKILL.md` and follow its phases."* `AGENTS.md` points agents there automatically. A small model can follow it one chapter at a time.

## Requirements
- A TeX distribution with `latexmk`: TeX Live or MiKTeX (on MiKTeX without Perl, run `pdflatex` three times instead).
- Python 3. [Pillow](https://pillow.readthedocs.io/en/stable/installation/basic-installation.html) for the contact sheets; everything else uses the standard library.
- poppler-utils: `pdftotext`, `pdftoppm`.
- Optional, for mock exams with tiny local models: any OpenAI-compatible server with an embeddings endpoint (Lemonade Server, llama.cpp server, Ollama, LM Studio). Tested with 0.6–1.2 B models on a 16 GB laptop.

## Two layouts, one source
- `skills/exam-notes-builder/` and `agents/` are the source: real `.py`, `.sty`, `.tex` files, used by git users and other agents.
- `plugin/` is generated from them by `python tools/build_plugin.py`: scripts and templates are wrapped as Markdown, because the Claude plugin directory accepts only Markdown, JSON and images from unverified publishers. This is the folder submitted to the directory. Rebuild it after every change; the script checks that every file unpacks back byte for byte.

## Contents
```
.claude-plugin/marketplace.json   this repository as a marketplace; lists the plugin in plugin/
plugin/                           generated plugin (submit this folder to the directory)
tools/                            build_plugin.py, plugin.json and icon.png used to build plugin/
plugin.json, .agents/plugins/     Codex plugin manifest and Codex marketplace (read the skill from skills/)
gemini-extension.json, GEMINI.md  Gemini CLI extension
agents/                           notes-writer, solution-verifier, paper-setter, notes-only-student,
                                  strict-grader, visual-checker (cheap, runs on Haiku)
skills/exam-notes-builder/
  SKILL.md                        the procedure: 9 phases, each with a gate
  reference/                      style rules, chapter structure, appendices, coverage matrix, mock papers,
                                  grading rubric, subject adaptation, briefs, LaTeX pitfalls, past papers,
                                  visual check
  templates/                      ocwnotes.sty (layout), main.tex (book skeleton), config examples
  scripts/
    content_check.py <dir>        every section/example/box title in the sources appears in the built PDF
    depth_audit.py <dir>          flags sections with too little explanation
    syllabus_check.py <dir>       every item in <dir>/syllabus_checklist.tsv is present in the notes
    build_core.py <dir>           writes <dir>/core_main.tex (the Exam Core) using <dir>/core.txt
    contact_sheet.py pdf out/     contact sheets for the visual check (8 pages per image, batches, zoom)
    rag_exam.py, run_all.sh       notes-only exam with a tiny local model + retrieval
```

## Visual check in one minute
```bash
S=skills/exam-notes-builder/scripts
python $S/contact_sheet.py Course_Notes/main.pdf _sheets --batches 4   # ~19 images for 150 pages
# Claude Code: one visual-checker subagent per batch, in parallel; each reports "page N | kind | problem"
python $S/contact_sheet.py Course_Notes/main.pdf _sheets --zoom 42 77  # confirm at 100 dpi, then fix
```

## Quick script reference
```bash
S=skills/exam-notes-builder/scripts
latexmk -pdf -interaction=nonstopmode main.tex          # build (inside a notes folder)
python $S/content_check.py Course_Notes                 # after layout changes
python $S/syllabus_check.py Course_Notes                # nothing missing from the syllabus
python $S/build_core.py Course_Notes && (cd Course_Notes && latexmk -pdf core_main.tex)
RAG_API=http://127.0.0.1:13305/api/v1 python $S/rag_exam.py <model> paper.md Course_Notes answers/paper__model.md
```

## Origin
Built and battle-tested while writing three ~100–150-page exam books for a first-year university physics programme, including line-by-line review by parallel agents and mock exams sat by 1-billion-parameter models.

## License
MIT. See `LICENSE`.
