---
name: exam-notes-builder
description: Build complete, examiner-proof exam notes for any course or subject (LaTeX to PDF) from a syllabus, textbooks and past papers, then prove them complete with notes-only mock exams graded by a strict examiner, and finish with a short "Exam Core" revision book. Use for requests like "make exam notes", "notes so complete I don't need the book", "solve past papers", "formula sheet", "mock paper", "check my notes cover the syllabus", "short revision version".
---

# Exam Notes Builder

**Goal.** Notes from which a student who never opens the textbook can (1) answer every question an examiner can set, old or new, and (2) write each answer so that a strict, step-marking examiner cannot deduct a mark.
**Done means** a weak, notes-only test-taker plus a strict grader finds *no* deduction caused by the notes (Phase 6), every syllabus line is covered (Phase 3 check), and a short Exam Core exists (Phase 8).

Works for any subject. The examples in the reference files come from a physics course; `reference/subject-adaptation.md` maps every rule to mathematics, chemistry, biology, computer science, engineering, economics, law, history and languages (what a "derivation", a "figure" or a "numerical" becomes).

**Layout is fixed.** Every book uses `templates/ocwnotes.sty` unchanged (pick one of its three layouts in `main.tex`: `\usepackage[classic]{ocwnotes}` Times, `[palatino]` Palatino, `[modern]` Times with sans-serif headings; ask the user which they prefer at intake, default classic; all three have identical sizes, spacing and boxes) and starts from `templates/main.tex` (`\setcourse`, `\notestitle`, `\include` per chapter): 12 pt Times (newtx), "Chapter N" openers, roomy spacing, light grey `keybox`/`tipbox`/`psetbox`, indented `solution`, black-and-white figures at `0.8\linewidth`. Do not design a new layout, change fonts or sizes, or shrink text to fit; copy the `.sty` next to `main.tex` and change only content.

**Small or fast model? Follow `reference/runbook.md`**: the same job as numbered steps, each with the command that proves it worked. The scripts do the checking (`scripts/gates.py` turns the LaTeX log into PASS/FAIL lines with fix hints; `scripts/new_course.py` creates every starting file), so a careful small model that follows the runbook and obeys the scripts produces the same book as a large one. Any model: start a course with `new_course.py`, check every build with `gates.py`.

All scripts are plain Python 3 and run the same on Windows, macOS and Linux (only `run_all.sh` needs a bash shell: Git Bash or WSL on Windows).

Work in phases, in order, starting with Phase S (tools). Each phase ends in a **gate**; do not start the next phase until the gate passes. Keep `PROGRESS.md` in the course folder: one line per phase with status, date, and what is left.

## Contents of this skill
| Path | Use |
|---|---|
| `reference/runbook.md` | **The whole job as numbered steps with checks and recovery. Small models: follow this instead of improvising.** |
| `templates/example_chapter.tex` | A finished chapter from a real course: copy its shape (order, boxes, depth), not its content. |
| `scripts/new_course.py` | Creates a course folder with main.tex, layout, chapter stubs, PROGRESS.md, COVERAGE.md and config files. |
| `scripts/gates.py` | Builds the book and checks the gates: errors, undefined references, overfull boxes, leftover placeholders; prints the file, line and a fix hint for each. |
| `reference/subject-adaptation.md` | How the method maps to your subject. Read first if the course is not physics. |
| `reference/style-rules.md` | How to write. Read before writing any chapter. |
| `reference/chapter-structure.md` | Fixed order of every chapter, with a LaTeX skeleton. |
| `reference/appendices.md` | Solved past papers, full-marks guide, formula/fact sheet. |
| `reference/coverage-matrix.md` | Syllabus × books × past papers table template. |
| `reference/mock-papers.md` | Setting book / old / unseen / fusion papers, with a paper template. |
| `reference/grading-rubric.md` | Strict examiner marking scheme and N/R/S fault classes. |
| `reference/expansion-brief.md` | Brief for parallel agents that fill gaps in chapters (no bloat). |
| `reference/review-brief.md` | Brief for parallel agents that review chapters line by line for full marks. |
| `reference/latex-pitfalls.md` | Build errors met before and their fixes; build gates. |
| `reference/past-papers.md` | Finding, downloading and transcribing past papers. |
| `templates/ocwnotes.sty`, `templates/main.tex` | Layout (12 pt Times, chapter openers, light boxes, roomy spacing) and book skeleton. |
| `templates/syllabus_checklist.tsv`, `templates/core.txt` | Config files for the syllabus check and the Exam Core. |
| `scripts/content_check.py` | Every title/example in the sources appears in the PDF (run after layout changes). |
| `scripts/depth_audit.py` | Flags thin sections (too little explanation). |
| `scripts/syllabus_check.py` | Every syllabus item / standard derivation is present in the notes. |
| `scripts/build_core.py` | Extracts the short Exam Core book from the full notes. |
| `scripts/rag_exam.py`, `scripts/run_all.sh` | Notes-only mock exam sat by tiny local models (any OpenAI-compatible server). |
| `reference/visual-check.md` | Phase 7: contact sheets, parallel cheap checkers, defect list, zoom-and-fix loop. |
| `scripts/contact_sheet.py` | Renders the PDF as contact sheets (8 pages per image), splits them into batches for parallel checkers, zooms single pages. |
| `agents/*.md` (plugin root) | Subagents: notes-writer, solution-verifier, paper-setter, notes-only-student, strict-grader, visual-checker. Installed automatically with the plugin; otherwise copy them to `.claude/agents/`. |

Requirements: a TeX distribution with `latexmk`, Python 3, poppler (`pdftotext`, `pdftoppm`) and Pillow. Optional: a local model server for Phase 6. Phase S below checks and installs them.

---

## Phase S: Set up the tools
Before Phase 0, make sure every tool the later phases call is installed, so no phase stops halfway on a missing program.

1. **Check** each one by running it:

   | Tool | Check | Needed for | Official install instructions |
   |---|---|---|---|
   | TeX distribution with `latexmk` | `latexmk -v`, `pdflatex --version` | building every PDF | TeX Live: https://tug.org/texlive/ · MiKTeX (Windows): https://miktex.org/download · MacTeX: https://tug.org/mactex/ |
   | Python 3 | `python --version` (or `python3`) | all scripts | https://www.python.org/downloads/ |
   | poppler (`pdftotext`, `pdftoppm`) | `pdftoppm -v` | reading books and papers, contact sheets | https://poppler.freedesktop.org/ (Windows builds: https://github.com/oschwartz10612/poppler-windows/releases) |
   | Pillow | `python -c "import PIL"` | contact sheets (Phase 7) | https://pillow.readthedocs.io/en/stable/installation/basic-installation.html |
   | Perl (only if `latexmk` fails on MiKTeX) | `perl -v` | `latexmk` on MiKTeX | https://strawberryperl.com/ ; or build with `pdflatex` three times instead |
   | Local model server (optional) | the server's health URL | Phase 6 with tiny models | Lemonade: https://lemonade-server.ai/ · llama.cpp, Ollama or LM Studio: their own sites |

2. **Install what is missing.** Follow the official instructions linked above for the user's operating system, using the system's usual package manager or installer. Ask the user before installing anything: it changes their computer, may need administrator rights, and a TeX distribution is several gigabytes. If you cannot install a tool yourself (no permission, no shell), tell the user exactly which tool is missing and give them its link.
3. **Re-run the checks** until all required tools answer. MiKTeX installs missing LaTeX packages on first use, so the first build can be slow; let it finish.

Do not continue past a missing required tool by working around it (for example writing notes you cannot compile): every gate depends on building and reading the PDF.

**Gate S:** every required check in the table succeeds; record the versions in `PROGRESS.md`.

## Phase 0: Intake
Find, and only ask for what you cannot find:
1. Institution, programme, term, course name and **course/paper code**.
2. The **official syllabus** for exactly this course and scheme. Copy every unit line verbatim into `COVERAGE.md`.
3. The **exam pattern**, read from a real recent paper, never assumed: total marks, time, compulsory part, choice (e.g. "Q1 6×3 compulsory + any 4 of Q2–Q6, 18 each").
4. Prescribed books, and which are on disk (`*.pdf`). Map book chapters to units.
5. Constraints: theory only or practicals, printing (black and white), language, how answers are marked (steps, keywords, structure).

**Gate 0:** syllabus text, the exam pattern from a real paper, and the book list are in `PROGRESS.md`.

## Phase 1: Sources
1. **Past papers** (`reference/past-papers.md`): the last 3 years of the current scheme plus at least 5 older ones (older scheme, other colleges, related courses). Transcribe every question into `sources/papers.md` as `YEAR | Q | marks | text | syllabus line`.
2. **Books**: extract the table of contents and end-of-chapter problems (`pdftotext -f A -l B book.pdf -`). Record 5–10 representative questions per syllabus line.
3. **Question-type census**: group every past question into types ("solve a Bernoulli ODE", "derive the rocket equation", "explain the causes of X", "distinguish A and B", "apply rule R to a case"). Count frequency, note the years.

**Gate 1:** every past question has a type and a syllabus line; every syllabus line has book sections.

## Phase 2: Coverage matrix
Fill `reference/coverage-matrix.md` into `COVERAGE.md`. Add rows for anything examiners asked that sits inside a syllabus topic without being printed: examiners ask these.
Also write `syllabus_checklist.tsv` in the notes folder (template in `templates/`): one line per syllabus line **and** per standard derivation/proof/method/essay a paper can ask for, each with a regex that must occur in the notes.

**Gate 2:** every row has a planned location in the notes.

## Phase 3: Chapters
One chapter per syllabus unit or major topic, written by you or by `notes-writer` subagents (one per chapter; each edits only its own file; see *Agents and usage budget* below), **always in the order of `reference/chapter-structure.md`**:
intro (with past-question years) → for each topic: intuition → definitions → full derivation / proof / worked method / model argument with its figure → key result box → tip → three worked examples (direct, past paper, twisted) → further solved questions → **Concepts and strategy** (the big picture, how to recognise the question type, a plan for any unseen question, traps) → problems with answers.

**Length.** Notes must teach, not list. Every section explains *why* in prose before and after the formal content. Aim for 1.5–3 pages per syllabus line. A section that is only formulas/bullet points and an example is too short (`scripts/depth_audit.py` flags these). Do not bloat either: add what an examiner can ask, nothing else.

**Gate 3 (each chapter):** `python scripts/gates.py <notes_dir>` prints ALL GATES PASS; every `COVERAGE.md` row assigned to it is ticked; `python scripts/syllabus_check.py <notes_dir>` reports nothing missing at the end of the phase.

## Phase 4: Appendices
Solved past papers (every question of the last 3 years as a model answer), Writing Answers for Full Marks (mark split, rules, one model answer, a per-question-type checklist, a time plan), Formula/Fact Sheet (one item per row, `ftab`). See `reference/appendices.md`.

**Gate 4:** `python scripts/gates.py <notes_dir>` prints ALL GATES PASS with no placeholder warning (zero errors, zero undefined references, no overfull box wider than 3 pt; `reference/latex-pitfalls.md`).

## Phase 5: Verify every answer, and review for full marks
1. For each worked example and practice answer, re-derive it independently (by hand or `python -I`): numbers, units, signs, factors of 2, facts, dates, citations, and that the answer answers the question asked. Use `solution-verifier` per chapter.
2. Then run a **full-marks review**: parallel reviewers following `reference/review-brief.md`, one per 2–3 chapters (~60–90 KB of source each), each editing only its files. They fix errors, fill skipped steps and add missing past-paper question types. Check a sample of their fixes yourself.
3. Never invent past-paper questions or data. If a question's data had to be reconstructed from its known answer, say so in the appendix.
4. **Check every printed "prove that" before writing its answer** (numerically, e.g. at one sample point). Papers contain misprints: if the printed identity is false, say so in one line, prove the evident intended version, and state what the printed version actually gives.

**Gate 5:** zero open issues; reviewers' reports checked.

## Phase 6: Prove completeness with mock exams
1. **Set papers** (`reference/mock-papers.md`) in the real pattern, never reusing a question solved word-for-word in the notes: a *book*, an *old-paper* and an *unseen* paper per course. For courses taken together, add a *fusion* paper where every question mixes two or three courses. Write and check the answer key while setting.
2. **Sit them notes-only**:
   - *Tiny local models with retrieval* (`scripts/rag_exam.py`, any OpenAI-compatible server with embeddings): weak at the subject, good at following instructions, so a right answer can only come from the notes. Tested on a 16 GB laptop through Lemonade Server: `LFM2.5-1.2B-Instruct-GGUF`, `unsloth/Llama-3.2-1B-Instruct-GGUF:Q4_K_M`, `Qwen3-0.6B-GGUF` (add `/no_think`), embedder `nomic-embed-text-v1-GGUF`. Rotate so each model sits one paper per course (`scripts/run_all.sh`).
   - *Notes-only agents* (`agents/notes-only-student.md`, small model): read only the notes folder, no web, no prior knowledge, full exam-length answers. Cheapest setup: `pdftotext -layout main.pdf notes.txt`, then one Haiku-class agent that may only Grep and Read line ranges of `notes.txt`, answers every part of an unseen paper, and starts each answer with `[notes: <section used>]` so findability is visible; grade against a key you checked while setting.
   - Tiny models often write "NOT IN NOTES" for things that are there: check every flag with a grep before calling it a gap.
3. **Grade** with `agents/strict-grader.md` and `reference/grading-rubric.md`. Classify every lost mark as **N** (notes gap) → fix the notes; **R** (in the notes but not findable) → retitle, cross-reference, add to "how to recognise"; **S** (test-taker slip) → no change unless it is a common trap.
4. Patch N and R, rebuild, re-verify the patched parts. Repeat with fresh papers until a round has zero N and zero R.

**Gate 6:** the latest grade report has zero N and zero R deductions.

## Phase 7: Visual check
Compiling cleanly does not mean the pages look right. Follow `reference/visual-check.md`:
1. `python scripts/contact_sheet.py main.pdf _sheets --batches 4` renders the book as contact sheets (8 pages per image, each labelled with its PDF page number) and splits them into batches.
2. Spawn one `visual-checker` subagent (cheapest vision model, e.g. Haiku) per batch, all in one message so they run in parallel. Each reports `page N | kind | what is wrong`. Without subagents, check the sheets yourself one by one.
3. Zoom on every reported page (`--zoom N`, 100 dpi) to confirm or reject it, fix the source, rebuild, zoom again. Never shrink body text to make things fit.

**Gate 7:** a full pass of sheets; every report fixed (confirmed by a zoom after the fix) or rejected by a zoom.

## Phase 8: Exam Core and delivery
1. Students find a 150-page book overwhelming. Build a short **Exam Core** extracted from the full notes (nothing new, so it cannot drift): write `core.txt` in the notes folder (`must:` regex of the must-know derivation section/subsection titles; optional `past:` regex for past-paper example titles), then `python scripts/build_core.py <notes_dir>` and `latexmk -pdf core_main.tex`. It keeps the must-know sections in full (minus practice examples), every key-result box, every past-paper example with its solution, each chapter's Concepts and strategy, the formula sheet and the full-marks guide. Typical size: a third of the full book. Rebuild it whenever the notes change.
2. Copy the final PDFs (full notes and Exam Core) to the course folder root with clear names, run `latexmk -c`, keep `COVERAGE.md`, `PROGRESS.md`, papers, keys and grade reports.
3. Tell the student how to study: past-paper topic table → must-know derivations → key boxes + Concepts and strategy + past-paper examples → formula sheet; the full notes are the reference.
4. Report honestly what was verified and what was not.

## Rules for every phase
- Edit `.tex` files with an editor tool or a Python script file. **Never** pass LaTeX through shell `sed` or heredocs: the shell eats backslashes.
- Compile after every chapter and fix errors immediately.
- Tag every examined result with its years. Never invent a past-paper question or year; label made-up ones "practice".
- Black-and-white friendly. No information carried by colour alone.
- Parallel agents: one file set per agent, own build directory, literal paths when deleting.
- **Agents and usage budget.** Users often have a usage cap; parallel agents on the strongest model can exhaust it on one course (seven at once did). Defaults: write chapters yourself or with at most 2–3 agents at a time; mid-tier model for writing, the cheapest for visual checks and notes-only students; ask the user before a larger fan-out. Brief each agent leanly: point to *one* finished chapter as the style model and put the facts it needs (past questions, verified answers, labels) in the prompt, instead of having every agent reread everything. Each agent saves its file section by section, so work survives an interruption, and builds a standalone test file (`_t_<key>.tex` = the preamble of `main.tex` + `\input{<its file>}`), never `main.tex`, while others are editing.
- When the user says "make sure nothing is missed", the answer is the syllabus check plus Phase 6, not a longer reread.
- After any layout change, run `scripts/content_check.py <notes_dir>` (every section, example and box title must appear in the PDF text).

---
exam-notes-builder by Soumyadip Karforma · https://github.com/soumyadipkarforma/exam-notes-builder · MIT licence. Keep the "Made with exam-notes-builder" line that the layout prints on title pages.
