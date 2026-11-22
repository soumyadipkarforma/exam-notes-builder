# Chapter structure

Every chapter follows this order. Copy the skeleton and fill every `<<...>>`.

1. **Chapter intro**: what the unit is about, and which past questions come from it, with years and marks.
2. **One `\section` per syllabus topic**, named in the examiner's words:
   1. Intuition (a paragraph of plain words, no symbols yet)
   2. Definitions (symbols, units, sign conventions) plus a `remark` on notation differences between books
   3. Derivation with every line and the figure the examiner expects
   4. `keybox` with the result, tagged with exam years
   5. `tipbox` with the trap or wording
   6. Three worked examples: direct, past-paper, twisted
3. **Further solved questions (older papers and books)**: every question type from `COVERAGE.md` for this chapter not already solved.
4. **Concepts and strategy**: physical picture; how to recognise the question type; a step-by-step plan for any unseen problem; traps.
5. **Problems** (`psetbox`) with answers and book references.

```latex
\chapter{<<Unit topic>>}\label{ch:<<key>>}
<<What this unit is and why it matters. Past questions: 2023 Q3(a) 6 marks, 2024 Q2(b) 6 marks, 2025 Q3 18 marks.>>

\section{<<Topic in the examiner's words>>}\label{sec:<<key>>}
<<Intuition: the physical picture, 4-8 sentences, before any formula.>>

\begin{definition}[<<Name>>]
<<Precise definition with symbols, units and sign convention.>>
\end{definition}

\begin{remark}[Notation]
<<How the prescribed books differ, and which notation these notes use.>>
\end{remark}

\subsection{Derivation}
<<Say what we are going to do and why.>>
\begin{center}
\begin{tikzpicture}
<<figure: axes, forces, coordinates, positive directions>>
\end{tikzpicture}
\end{center}
<<Step 1, naming the law:>>
\begin{align}
<<line>> &= <<line>>\\
         &= <<line>>
\end{align}
<<Step 2 ... every line, every integral evaluated.>>

\begin{keybox}[<<Result>> (<<Dec 2023, Dec 2025>>)]
\[ <<boxed result>> \]
<<What the result means, its limits of validity.>>
\end{keybox}

\begin{tipbox}
<<The exact wording/trap examiners use; what earns or loses marks.>>
\end{tipbox}

\begin{example}[<<Direct>>]
<<Question.>>
\end{example}
\begin{solution}
<<Formula symbolically; numbers with units; boxed answer with units; one-line interpretation.>>
\end{solution}

\begin{example}[<<Past paper: Dec 2024 Q2(a)>>]
<<Question exactly as printed.>>
\end{example}
\begin{solution}
<<Full model answer as it should be written in the hall.>>
\end{solution}

\begin{example}[<<Twisted: reversed / combined / unusual function>>]
<<Question.>>
\end{example}
\begin{solution}
<<Full answer.>>
\end{solution}

\section{Further solved questions (older papers and books)}
<<Every remaining question type, fully worked.>>

\section{Concepts and strategy}\label{sec:<<key>>concept}
\begin{keybox}[The physical picture]
<<The whole unit in plain words: what is happening and why the methods work.>>
\end{keybox}
\textbf{How to recognise the question type.}
\begin{itemize}
\item <<If the question has feature X, use method Y, because Z.>>
\end{itemize}
\textbf{Plan for any unseen problem of this kind.}
\begin{enumerate}
\item <<Draw the figure, choose coordinates>>
\item <<Write the governing law>>
\item <<Reduce to a standard form>>
\item <<Solve; check units, limits and signs>>
\end{enumerate}
\textbf{Traps.}
\begin{itemize}
\item <<Sign convention / factor of 2 / what is not conserved / when the formula fails.>>
\end{itemize}

\begin{psetbox}
\begin{enumerate}
\item <<Problem.>> \emph{Ans.} <<answer>>
\item <<Book: Author Ch. N, problems a-b; online problem set>>
\end{enumerate}
\end{psetbox}
```
