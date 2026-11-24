# Runbook: the whole job as numbered steps

Follow this file line by line when you are a small or fast model, or whenever you are unsure what to do next. Every step says what to read, what to write, which command proves it worked, and what to do if it did not. The scripts do the checking; your job is to write content and react to their output.

Paths: `scripts/...` and `templates/...` are inside this skill folder. In the Claude plugin they are first unpacked to `exam-tools/scripts/...` and `exam-tools/templates/...` (the Setup step in SKILL.md); use those paths there. Write `python` (or `python3` on macOS/Linux if `python` is missing).

## The 12 rules that matter most
1. **One small unit of work at a time**: one section of one chapter, then build. Never write a whole chapter in one go.
2. **Read only what the current step names.** Do not load every reference file or every chapter. Context you do not need makes you worse.
3. **Never invent** a past-paper question, a year, a mark, a quotation, a theorem name or a number. If it is not in `sources/`, label your own question "practice".
4. **Never leave placeholders**: no `...`, `<<...>>`, "similarly", "left to the reader", "proof omitted", "see textbook". The student has no textbook.
5. **Every claimed result is checked by computation** (Step 5.2) before it is written as final.
6. **Edit `.tex` only with a file-writing tool or a Python script file.** Never `sed`, `echo` or heredocs: the shell eats backslashes (`\frac` becomes `rac`, `\v` becomes an invisible character).
7. **Use only the environments and macros that exist**: `definition`, `theorem`, `example` + `solution`, `remark`, `keybox[Title]`, `tipbox`, `psetbox`, `ftab`, and the macros in `ocwnotes.sty`. A new macro goes at the top of your chapter with `\providecommand`.
8. **Build after every section**: `python scripts/gates.py <notes_dir>`. Fix the *first* problem it prints, rebuild, repeat until `ALL GATES PASS`.
9. **Labels are prefixed by the chapter key**: `\label{sec:lim-cont}`, `\label{ex:lim-jump}`. `\ref` only labels that already exist (search for `\label{` first).
10. **Copy the shape of `templates/example_chapter.tex`**, not its content: same order, same boxes, same depth of explanation.
11. **Write the update** in `PROGRESS.md` after every gate, so another session (or you after a restart) can continue.
12. **When stuck twice on the same error, stop and report** the exact `gates.py` output to the user instead of guessing.

## Step 0: Start a course
1. Run `python scripts/new_course.py <course_dir> --code "<code>" --title "<title>" --short "<short>" --term "<programme, term>" --layout classic --chapters "c1_<key>:<Title>" "c2_<key>:<Title>" ...` (one `--chapters` item per syllabus unit or big topic; keys are short lowercase words; `--layout` is `classic`, `palatino` or `modern`: ask the user, default `classic`).
2. Run `python scripts/gates.py <course_dir>`. Expect `ALL GATES PASS` and a WARN about placeholders (normal at this point).
3. Fill `PROGRESS.md` sections *Tool versions*, *Syllabus*, *Exam pattern*, *Books* (Phase S and Phase 0 of SKILL.md).
   - Syllabus: copy every unit line **verbatim** from the official document.
   - Exam pattern: read it from a real paper (total marks, time, compulsory part, choice, marks per part). Never guess.

## Step 1: Sources (read `reference/past-papers.md`)
1. Put papers in `sources/papers/`, books in `sources/books/`.
2. Get text: `pdftotext -layout file.pdf -` . If the text is empty or garbled, the PDF is a scan: render pages with `pdftoppm -r 100 -f N -l N -png file.pdf out` and read the images.
3. Transcribe **every** question into `sources/papers.md`, one line each: `PAPER | Q | marks | exact text | syllabus line`. Tag papers by what is printed on them (year, or serial number if no year is printed).
4. Write `sources/census.md`: group questions into types ("verify Rolle's theorem for a given f", "derive the rocket equation"). One row per type: count, papers, syllabus line.
5. **Check**: every line of `papers.md` has a syllabus line; every type in `census.md` has at least one paper.

## Step 2: Plan (read `reference/coverage-matrix.md`)
1. Fill `COVERAGE.md`: one row per syllabus line, plus one row per census type that is not literally a syllabus line.
2. Fill `syllabus_checklist.tsv`: one line per syllabus line and per standard proof/derivation, with a regex that must appear in the notes (e.g. `Rolle's theorem\tRolle`).
3. In each chapter file, write only the `\section{...}` headings first (examiner's wording), then run gates.

## Step 3: Write one section (repeat for every section)
Read `reference/style-rules.md` once per session and `templates/example_chapter.tex` once per chapter. Then for **one** section:

| Part | What to write | Self-check (answer yes before moving on) |
|---|---|---|
| Intuition | 4–8 plain sentences: what the idea is, why it is needed, a picture in words. No symbols yet. | Could a student who missed the lecture follow it? |
| Definition | `\begin{definition}[Name]` precise statement, every symbol and unit defined. | Is every symbol defined where it first appears? |
| Theorem / law | `\begin{theorem}` with **all** hypotheses. | Are the hypotheses complete (e.g. continuous on [a,b] AND differentiable on (a,b))? |
| Proof / derivation | Every line written; each step names its rule ("by the product rule", "by Newton's second law"). End with `$\square$`. A figure if the examiner expects one. | Is there any "it follows easily", skipped integral or skipped algebra? Remove it. |
| keybox | The result to memorise, tagged with the papers that asked it. | Is the result exactly what the derivation ended with? |
| tipbox | The trap or the wording that earns/loses marks. | Is it specific (not "be careful")? |
| Example 1 direct | Straight use of the result. | Final answer stated in a sentence? |
| Example 2 past paper | **Every** past question of this type, verbatim, tagged (`DU 1264 Q3(a)`). | Is the text identical to `papers.md`? |
| Example 3 twisted | A variant an examiner could set next (changed numbers, reversed question, combined idea). | Is it labelled practice/twisted, not a fake past paper? |

Worked solution format (always):
```
\begin{example}[<tag or "Twisted: ...">]
<question>
\end{example}
\begin{solution}
<Given / to find, in one line.>
<Method: name the theorem or rule, and check its hypotheses.>
<Steps: every line; one display per idea.>
<Check: a quick numerical or limiting-case check.>
<Answer: the result in a sentence (and units).>
\end{solution}
```
After the section: `python scripts/gates.py <notes_dir>` → fix until `ALL GATES PASS`.

## Step 4: Finish a chapter
1. Add **Further solved questions**: every census type of this chapter not yet solved.
2. Add **Concepts and strategy** (a `\section`): how to recognise each question type → the plan to follow → traps. Use bullet points, one per question type.
3. Add `psetbox` problems (8–12) **with answers**.
4. Run `python scripts/depth_audit.py <notes_dir>`; expand any section it flags as thin (explanation, not filler).
5. Run gates; tick the chapter's rows in `COVERAGE.md`.

## Step 5: Verify (do this for every number and every "show that")
1. Re-derive each answer independently, not by rereading your own text.
2. Check with a computation. Use `python -I` with a script file (not `-c` with LaTeX in it). If `sympy` is available:
   ```python
   from sympy import *
   x = symbols('x')
   f = x**3 - 6*x**2 + 11*x - 6
   print(solve(diff(f, x), x))          # Rolle: c = 2 +- 1/sqrt(3)
   print(limit((x - sin(x))/x**3, x, 0)) # 1/6
   ```
   Without sympy: plug numbers in (finite differences for derivatives, a sample point for identities):
   ```python
   import math
   f = lambda x: math.atan(x); h = 1e-6
   print((f(0.3+h) - f(0.3-h))/(2*h), 1/(1+0.3**2))   # must agree to ~1e-9
   ```
3. A printed "prove that" may be misprinted: test it at one sample point **before** writing the proof. If false, say so in one line, prove the intended version, state what the printed one gives.
4. Wrong result found → fix the text, rerun the check, rebuild.

## Step 6: Appendices (read `reference/appendices.md`)
1. `cA_pyq.tex`: every question of every past paper, verbatim, with a full model answer (same format as Step 3). If long, split into `\input` files, one per paper.
2. `cB_fullmarks.tex`: paper pattern; mark split of a typical part; rules; one annotated model answer; a checklist per question type; time plan.
3. `cC_formulas.tex`: `\fsec{...}` headings and `ftab` rows (bold name | formula), one item per row.
4. `c0_guide.tex`: exam pattern, question-type table (type, how many papers, chapter), how chapters are built, study plan.
5. Gates must pass with no WARN about placeholders.

## Step 7: Prove it works (Phase 6 of SKILL.md)
1. Set an **unseen** paper in the real pattern (`reference/mock-papers.md`) and its answer key; check the key with Step 5.
2. `pdftotext -layout main.pdf notes.txt`. A notes-only student (smallest model available) may only search and read `notes.txt`, answers every part, and starts each answer with `[notes: <section used>]`, or writes `NOT IN NOTES: <what>`.
3. A grader marks against the key (`reference/grading-rubric.md`): N = notes gap, R = in the notes but not findable, S = slip.
4. Fix every N (add the content) and R (better title, cross-reference, "how to recognise" line). Repeat with a fresh paper until zero N and zero R.

## Step 8: Look at every page (read `reference/visual-check.md`)
1. `python scripts/contact_sheet.py main.pdf _sheets --batches 4`; read the sheet images (or give each batch to a cheap vision checker).
2. Zoom each suspect page: `python scripts/contact_sheet.py main.pdf _sheets --zoom N`. Fix, rebuild, zoom again.
3. Graph labels crossed by curves: see the last section of `reference/latex-pitfalls.md`.

## Step 9: Deliver
1. Write `core.txt` (`must:` regex of must-know section titles; `past:` regex of past-paper tags). Run `python scripts/build_core.py <notes_dir>`, then build `core_main.tex` and run `python scripts/gates.py <notes_dir>/core_main.tex`.
2. Copy `main.pdf` and `core_main.pdf` to clear names; clean with `latexmk -c`.
3. Report honestly: what was verified, what was not, the mock score, any misprinted questions.

## If something goes wrong
| Symptom | Do this |
|---|---|
| `gates.py` prints FAIL | Fix only the first item, using its hint and the file/line it names. Rebuild. |
| The same error twice after fixing | Open the file at the reported line ±5 lines; check braces `{}` and `\begin`/`\end` pairs; if still stuck, report to the user. |
| `\frac` shows as `rac`, invisible characters | The shell ate backslashes. Rewrite those lines with a file tool. |
| A label is undefined | Search for `\label{` to find the real key; or the chapter with it is not written yet (leave it, it resolves later). |
| A figure overlaps text | Move the label (`anchor=`), widen the plot to `0.8\linewidth`, or put labels after the curves (latex-pitfalls.md). |
| You are running out of context | Write `PROGRESS.md` (what is done, the next step), then continue in a fresh session from it. |
| A tool is missing | Phase S of SKILL.md; ask the user before installing. |
| Unsure whether something is on the syllabus | It is in scope if the syllabus line or any past paper asks it; otherwise leave it out. |
