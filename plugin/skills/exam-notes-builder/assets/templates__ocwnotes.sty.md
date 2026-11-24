# templates/ocwnotes.sty

Save as `templates/ocwnotes.sty`

````latex
% ocwnotes.sty: the house layout for exam notes (black & white, print friendly), modelled on MIT OCW notes.
% Part of exam-notes-builder by Soumyadip Karforma (https://github.com/soumyadipkarforma/exam-notes-builder), MIT licence.
% 12 pt text and maths, "Chapter N" openers (22/30 pt), 17/14 pt section heads,
% italic running head, line spread 1.22, block paragraphs, light grey key boxes, B&W plots.
% Use it unchanged for every book; never shrink text to make things fit.
%
% Layouts (choose one in main.tex; all share sizes, spacing, boxes and environments, so content never changes):
%   \usepackage{ocwnotes}            classic  : Times text and maths (newtx), serif headings  [default]
%   \usepackage[palatino]{ocwnotes}  palatino : Palatino text and maths (newpx), serif headings, warmer book look
%   \usepackage[modern]{ocwnotes}    modern   : Times text and maths, sans-serif headings, ruled chapter openers
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{ocwnotes}[2026/11/24 exam-notes layout v2]
\def\ocw@layout{classic}
\DeclareOption{classic}{\def\ocw@layout{classic}}
\DeclareOption{palatino}{\def\ocw@layout{palatino}}
\DeclareOption{modern}{\def\ocw@layout{modern}}
\DeclareOption*{\PackageWarning{ocwnotes}{Unknown layout `\CurrentOption'; using classic}}
\ProcessOptions\relax
% works with pdfLaTeX, XeLaTeX and LuaLaTeX
\def\ocw@iflayout#1{\def\ocw@tmp{#1}\ifx\ocw@tmp\ocw@layout\expandafter\@firstoftwo\else\expandafter\@secondoftwo\fi}

% ---------- page and type ----------
\RequirePackage[a4paper,top=2.6cm,bottom=2.6cm,left=2.7cm,right=2.7cm,headsep=0.8cm,footskip=1.1cm]{geometry}
\RequirePackage[T1]{fontenc}
\RequirePackage{amsmath,amsthm,mathtools}
\ocw@iflayout{palatino}
  {\RequirePackage[scaled=0.92]{newpxtext}\RequirePackage[scaled=0.92]{newpxmath}}   % Palatino, scaled to Times widths
  % (Palatino is ~8% wider with a taller x-height; at 0.92 it reads as large as Times and a book written in one layout fits in all three)
  {\RequirePackage{newtxtext}\RequirePackage[varvw]{newtxmath}}   % Times text and maths (provides \mathbb, \oint)
\RequirePackage{bm,cancel}
\RequirePackage[final]{microtype}
\RequirePackage{enumitem,booktabs,array,multicol,tabularx,xltabular}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,shapes.geometric,positioning,calc,decorations.markings,3d}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.17}
\RequirePackage{listings}
\RequirePackage[most]{tcolorbox}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec,titletoc}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{xurl}
\linespread{1.22}
% paragraphs with long inline maths stretch their spaces instead of running into the margin
\setlength{\emergencystretch}{3em}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt plus 2pt}
\setlist{itemsep=5pt,topsep=6pt,leftmargin=*}
% full-width tables must not take the paragraph indent
\RequirePackage{etoolbox}
\BeforeBeginEnvironment{tabularx}{\par\noindent}
\setlength{\abovedisplayskip}{11pt plus 3pt}
\setlength{\belowdisplayskip}{11pt plus 3pt}

% ---------- plots: black & white ----------
\pgfplotsset{
  every axis/.append style={axis lines=middle, grid=none, line width=0.5pt,
    tick label style={font=\footnotesize, fill=white, inner sep=1pt}, label style={font=\normalsize},
    scaled ticks=false, tick label style={/pgf/number format/fixed},
    legend style={font=\footnotesize, draw=black!60, fill=white}},
  cycle list={{black,solid,thick},{black,dashed,thick},{black,dotted,very thick},
              {black,dashdotted,thick},{gray,solid,thick}}
}

% ---------- course identity (running head and title page) ----------
\newcommand{\coursecode}{}
\newcommand{\courseshort}{}
\newcommand{\setcourse}[2]{\renewcommand{\coursecode}{#1}\renewcommand{\courseshort}{#2}}

% ---------- headings ----------
\titleformat{\chapter}[display]
  {\normalfont\bfseries\raggedright}
  {\fontsize{22}{26}\selectfont\chaptertitlename\ \thechapter}
  {16pt}
  {\fontsize{30}{36}\selectfont}
\titleformat{name=\chapter,numberless}[display]
  {\normalfont\bfseries\raggedright}{}{0pt}{\fontsize{30}{36}\selectfont}
\titlespacing*{\chapter}{0pt}{40pt}{30pt}
\titleformat{\section}{\normalfont\fontsize{17}{21}\selectfont\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\fontsize{14}{17}\selectfont\bfseries}{\thesubsection}{0.9em}{}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries}{\thesubsubsection}{0.7em}{}
\titleformat{\paragraph}[runin]{\normalfont\normalsize\bfseries}{}{0pt}{}[.]
\titlespacing*{\section}{0pt}{28pt plus 4pt minus 2pt}{10pt}
\titlespacing*{\subsection}{0pt}{20pt plus 3pt minus 2pt}{7pt}
\ocw@iflayout{modern}{%
  \titleformat{\chapter}[display]
    {\normalfont\sffamily\bfseries\raggedright}
    {\fontsize{22}{26}\selectfont\chaptertitlename\ \thechapter}
    {10pt}
    {\titlerule[1.2pt]\vspace{10pt}\fontsize{30}{36}\selectfont}
  \titleformat{name=\chapter,numberless}[display]
    {\normalfont\sffamily\bfseries\raggedright}{}{0pt}{\titlerule[1.2pt]\vspace{10pt}\fontsize{30}{36}\selectfont}
  \titleformat{\section}{\normalfont\sffamily\fontsize{17}{21}\selectfont\bfseries}{\thesection}{1em}{}
  \titleformat{\subsection}{\normalfont\sffamily\fontsize{14}{17}\selectfont\bfseries}{\thesubsection}{0.9em}{}
  \titleformat{\subsubsection}{\normalfont\sffamily\normalsize\bfseries}{\thesubsubsection}{0.7em}{}
}{}

% ---------- table of contents ----------
\titlecontents{chapter}[0pt]{\addvspace{7pt}\bfseries}
  {\makebox[5.6em][l]{\scshape\mdseries Chapter \thecontentslabel}}{}{\hfill\contentspage}
\titlecontents{section}[5.6em]{\addvspace{2pt}}{\makebox[2.8em][l]{\thecontentslabel}}{}
  {\titlerule*[0.7pc]{.}\contentspage}
\setcounter{tocdepth}{1}
\g@addto@macro\appendix{%
  \renewcommand{\chaptername}{Appendix}%
  \titlecontents{chapter}[0pt]{\addvspace{7pt}\bfseries}
    {\makebox[5.6em][l]{\scshape\mdseries Appendix \thecontentslabel}}{}{\hfill\contentspage}}

% ---------- running heads ----------
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\chaptermark}[1]{\markboth{\MakeUppercase{\chaptername\ \thechapter.\ #1}}{}}
\renewcommand{\sectionmark}[1]{}
\fancyhead[L]{\small\itshape\leftmark}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\setlength{\headheight}{14pt}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\thepage}\renewcommand{\headrulewidth}{0pt}}

% ---------- boxes (light, rule-based) ----------
% keybox: result to memorise. Grey panel with a strong left rule, run-in small-caps title.
\newtcolorbox{keybox}[1][Key result]{enhanced, breakable, sharp corners,
  colback=black!4, colframe=black, boxrule=0pt, leftrule=2.2pt,
  left=4mm, right=4mm, top=3mm, bottom=3mm, before skip=14pt, after skip=14pt,
  fonttitle=\bfseries\scshape, coltitle=black, attach title to upper={\par\smallskip}, title={#1}}
% tipbox: exam note. No fill, thin left rule, italic label.
\newtcolorbox{tipbox}[1][Exam note]{enhanced, breakable, sharp corners,
  colback=white, colframe=black!70, boxrule=0pt, leftrule=0.8pt,
  left=4mm, right=1mm, top=1.5mm, bottom=1.5mm, before skip=12pt, after skip=12pt,
  fonttitle=\itshape\bfseries, coltitle=black, attach title to upper={:\ }, title={#1}}
% psetbox: problem set. Top and bottom rules only.
\newtcolorbox{psetbox}[1][Problems]{enhanced, breakable, sharp corners,
  colback=white, colframe=black, boxrule=0pt, toprule=0.8pt, bottomrule=0.8pt,
  left=0mm, right=0mm, top=3mm, bottom=3mm, before skip=18pt, after skip=12pt,
  fonttitle=\bfseries\scshape, coltitle=black, attach title to upper={\par\smallskip}, title={#1}}

\lstset{basicstyle=\ttfamily\footnotesize, columns=fullflexible, keepspaces=true,
  frame=lines, rulecolor=\color{black}, numbers=left, numberstyle=\tiny,
  keywordstyle=\bfseries, commentstyle=\itshape, showstringspaces=false,
  breaklines=true, language=Python, upquote=true}

% ---------- theorem-like environments ----------
\newtheoremstyle{notes}{14pt}{8pt}{\normalfont}{0pt}{\bfseries}{.}{0.6em}{\thmname{#1}\thmnumber{ #2}\thmnote{\ \normalfont(#3)}}
\theoremstyle{notes}
\newtheorem{definition}{Definition}[chapter]
\newtheorem{example}{Example}[chapter]
\newtheorem{theorem}{Theorem}[chapter]
\newtheorem{remark}{Remark}[chapter]
% Solution: indented under a thin rule, ends with a small square.
\newenvironment{solution}
  {\par\vspace{-2pt}\begin{tcolorbox}[enhanced, breakable, sharp corners, colback=white,
     colframe=black!35, boxrule=0pt, leftrule=0.6pt, left=4mm, right=0mm, top=1mm, bottom=1mm,
     before skip=4pt, after skip=14pt]\textit{Solution.}\ }
  {\hfill$\square$\end{tcolorbox}}

% ---------- generic macros ----------
\newcommand{\R}{\mathbb{R}}
\newcommand{\vA}{\mathbf{A}}
\newcommand{\vB}{\mathbf{B}}
\newcommand{\vC}{\mathbf{C}}
\newcommand{\vD}{\mathbf{D}}
\newcommand{\vF}{\mathbf{F}}
\newcommand{\vE}{\mathbf{E}}
\newcommand{\vr}{\mathbf{r}}
\let\vv\relax\newcommand{\vv}{\mathbf{v}}
\newcommand{\vn}{\hat{\mathbf{n}}}
\newcommand{\ihat}{\hat{\mathbf{i}}}
\newcommand{\jhat}{\hat{\mathbf{j}}}
\newcommand{\khat}{\hat{\mathbf{k}}}
\newcommand{\grad}{\nabla}
\newcommand{\dive}{\nabla\cdot}
\newcommand{\curl}{\nabla\times}
\newcommand{\lap}{\nabla^2}
\newcommand{\dd}{\,\mathrm{d}}
\newcommand{\D}[2]{\frac{\mathrm{d}#1}{\mathrm{d}#2}}
\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\E}{\mathrm{E}}
\newcommand{\Var}{\mathrm{Var}}

% ---------- formula sheet ----------
\newcommand{\fsec}[1]{\par\medskip\noindent{\large\bfseries #1}\par\nobreak\vspace{1pt}\hrule\nobreak\vspace{3pt}}
\newenvironment{ftab}{\par\renewcommand{\arraystretch}{1.9}%
  \xltabular{\linewidth}{@{}>{\raggedright\arraybackslash\bfseries}p{4.2cm}X@{}}}
  {\endxltabular\vspace{4pt}}

% ---------- title page ----------
% \notestitle{course line}{title}{subtitle}{lecture list}{based-on line}
\newcommand{\notestitle}[5]{%
\begin{titlepage}\raggedright
\vspace*{1.5cm}
\rule{\linewidth}{1.2pt}\par\vspace{6pt}
{\scshape #1\par}\vspace{1.6cm}
{\fontsize{30}{36}\selectfont\bfseries #2\par}\vspace{0.4cm}
{\Large #3\par}\vspace{0.8cm}
\rule{\linewidth}{0.4pt}\par\vspace{0.8cm}
{\large #4\par}
\vfill
\rule{\linewidth}{0.4pt}\par\vspace{4pt}
{#5\par}
\vspace{10pt}
{\footnotesize\itshape Made with exam-notes-builder by Soumyadip Karforma \textperiodcentered\ \url{https://github.com/soumyadipkarforma/exam-notes-builder}\par}
\end{titlepage}}

% ---------- branding in the PDF properties ----------
\AtBeginDocument{\hypersetup{pdfcreator={exam-notes-builder by Soumyadip Karforma (github.com/soumyadipkarforma/exam-notes-builder)}}}
\endinput
````
