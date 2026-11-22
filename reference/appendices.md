# Appendices

## A. Solved past papers
- Short title in `[]` so the running head fits: `\chapter[Past Papers 2023--2025: Solutions]{Solved Past Papers 2023--2025}`.
- First section: a table of the papers (exam, paper number, pattern) and a topic-frequency table (topic × year).
- Then one section per paper, every question in the printed order, each with a model answer: law named, every step, boxed answer with units.
- A long derivation that is already a model answer in a chapter may be shortened to its first line, key step and result, plus "full derivation: Section \ref{...}". Never skip short questions.

```latex
\chapter[Past Papers <<years>>: Solutions]{Solved Past Papers <<years>>}\label{app:pyq}
\section{The papers}
<<pattern; table: exam | paper no. | pattern>>
\section{Topic frequency}
<<tabularx: topic | 2023 | 2024 | 2025>>
\section{<<Month Year>> (paper code <<code>>)}
\subsection*{Q1 (compulsory)}
\textbf{(a)} <<question as printed>>\par
<<model answer>>
```

## B. Writing answers for full marks
1. **How marks are given**: the mark split for derivations (figure and assumptions / law and working / result) and numericals (formula / substitution with units / answer with units).
2. **Rules that protect every mark** (keybox, 6–7 items): figure first; state assumptions; name the law; never quote what you are asked to derive; numbers with units; vectors with direction; interpret.
3. **Model answer**: one full standard derivation written exactly as in the hall.
4. **Checklist table** (`xltabular`): every standard question type → the steps the examiner looks for.
5. **Time plan** from the exam pattern (about 2 minutes per mark).

## C. Formula sheet
- `\fsec{Chapter name}` heading, then an `ftab` table: name on the left in bold, one formula per row on the right.
- Never several formulas crowded in one cell; split into rows.
- Optional: a school-level prerequisites sheet (identities, standard integrals, trigonometry).

```latex
\chapter{Formula Sheet}
\fsec{Damped oscillations}
\begin{ftab}
Equation of motion & $\ddot x+2\beta\dot x+\omega_0^2x=0$, \ $\beta=b/2m$\\
Underdamped & $x=A_0e^{-\beta t}\cos(\omega_dt+\phi)$, \ $\omega_d=\sqrt{\omega_0^2-\beta^2}$\\
\end{ftab}
```
