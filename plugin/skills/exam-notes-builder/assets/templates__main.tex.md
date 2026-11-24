# templates/main.tex

Save as `templates/main.tex`

````latex
% Book skeleton using templates/ocwnotes.sty (copy the .sty next to this file).
% Made with exam-notes-builder by Soumyadip Karforma: https://github.com/soumyadipkarforma/exam-notes-builder
\documentclass[12pt,a4paper,oneside]{book}
\usepackage[classic]{ocwnotes}   % layout: classic (Times) | palatino (Palatino) | modern (Times + sans headings)
% subject macros: define every macro you use here, e.g.
% \newcommand{\vp}{\mathbf{p}}
\setcourse{<<Course code>>\ \textperiodcentered\ <<Programme>>\ \textperiodcentered\ <<Term>>}{<<Short course name>>}

\begin{document}
\notestitle{<<Course code>>\ \textperiodcentered\ <<Programme>>\ \textperiodcentered\ <<Term>>}{<<Course title>>}{Complete Exam Notes}
  {Unit 1\quad <<topics>>\\[4pt]Unit 2\quad <<topics>>\\[4pt]Appendices\quad Solved papers <<years>>, full marks, formulas}
  {Based on <<books>>.\\ Worked examples, exam notes and problems in every chapter.}

\tableofcontents
\include{c0_guide}      % syllabus map, exam pattern, question frequency, study plan
\include{c1_<<topic>>}
% one \include per chapter
\appendix
\include{cA_pyq}        % solved past papers
\include{cB_fullmarks}  % writing answers for full marks
\include{cC_formulas}   % formula / fact sheet
\end{document}
````
