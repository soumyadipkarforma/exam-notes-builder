# templates/example_chapter.tex

Save as `templates/example_chapter.tex`

````latex
% EXAMPLE CHAPTER (shape to copy, not content). A finished chapter from a real course:
% University of Delhi GE-1(i) Fundamentals of Calculus, chapter on limits, continuity and differentiability.
% Notice: intro listing past questions -> per topic: intuition, definition, theorem + proof, figure, keybox,
% tipbox, direct / past-paper / twisted examples -> Concepts and strategy -> problems with answers.
% 
ef{ch:pre}, 
ef{sec:pre-*} etc. point to other chapters of that book and are undefined here.

\chapter{Limits, Continuity and Differentiability}\label{ch:lim}

Question 1 of every paper opens with this chapter. In four papers it has been asked as
\begin{itemize}
\item \textbf{show that a limit does not exist} by finding unequal one-sided limits: $\frac{e^{1/x}-e^{-1/x}}{e^{1/x}+e^{-1/x}}$ (DU 1264), $\frac{e^{1/x}-1}{e^{1/x}+1}$ (DU 2414), $\frac{x-|x|}{x}$ (DU 12910);
\item \textbf{evaluate a limit}: $x^2\sin\frac1{x^2}$ and $\frac{3\sin^{-1}x}{4x}$ (DU 3553), $\frac{x-1}{\sqrt x-1}$ (DU 12910);
\item \textbf{examine the continuity of a piecewise function} at its joining points and classify each discontinuity (DU 1264, DU 2414, DU 12910);
\item \textbf{examine continuity and differentiability at $0$} of $x^2\cos\frac1x$ (DU 3553) and of $x\,\frac{e^{1/x}-e^{-1/x}}{e^{1/x}+e^{-1/x}}$ (DU 12910).
\end{itemize}
These are the easiest 7.5 marks in the paper, but they are also the ones where a strict examiner deducts for missing words: ``left-hand limit'', ``right-hand limit'', ``since they are unequal, the limit does not exist'', ``$f(a)$ is defined and equals the limit''. This chapter gives the definitions in the exact form the examiner expects, the tools (one-sided limits, the squeeze theorem, standard limits), and model answers to every past question.

The background you need is in Chapter~\ref{ch:pre}: absolute value (\S\ref{sec:pre-num}), the limits of $e^{1/x}$ (\S\ref{sec:pre-exp}) and the standard limits (\S\ref{sec:pre-calc}).

\section{The idea of a limit}\label{sec:lim-idea}

\subsection{Intuition}
Consider $f(x)=\dfrac{x^2-1}{x-1}$. At $x=1$ the formula gives $\frac00$, which means nothing, so $f(1)$ is not defined. But for every $x\ne1$ we may cancel: $f(x)=x+1$. Put $x=0.9,\ 0.99,\ 0.999$ and you get $1.9,\ 1.99,\ 1.999$; put $x=1.1,\ 1.01,\ 1.001$ and you get $2.1,\ 2.01,\ 2.001$. The values crowd around $2$ from both sides. We say that the \emph{limit of $f(x)$ as $x$ tends to $1$ is $2$}, and write $\lim_{x\to1}f(x)=2$.

Two points about this example are the whole content of the definition:
\begin{enumerate}
\item The limit does \emph{not} care what happens \emph{at} $x=1$. Here $f(1)$ does not even exist, yet the limit does. The limit only looks at $x$ near $1$, with $x\ne1$.
\item ``Crowd around $2$'' must mean: \emph{as close to $2$ as anyone demands}, provided $x$ is close enough to $1$. Getting ``near $2$'' is not enough; $f(x)$ is also near $2.0001$, but $2.0001$ is not the limit, because if someone demands that $f(x)$ be within $0.00001$ of $2.0001$, points close to $1$ fail.
\end{enumerate}
The second point is turned into a precise definition with two small positive numbers, $\varepsilon$ (how close the values must be) and $\delta$ (how close $x$ must be).

\subsection{The \texorpdfstring{$\varepsilon$--$\delta$}{epsilon-delta} definition}
\begin{definition}[Limit]
Let $f$ be defined on an open interval containing $a$, except possibly at $a$ itself. We say $\lim_{x\to a}f(x)=L$ if for every $\varepsilon>0$ there exists $\delta>0$ such that
\[
0<|x-a|<\delta\quad\Longrightarrow\quad |f(x)-L|<\varepsilon .
\]
\end{definition}
Read it as a game. Your opponent chooses a tolerance $\varepsilon>0$, as small as they like. You must reply with a $\delta>0$ such that every $x$ within $\delta$ of $a$ (but not equal to $a$, that is the ``$0<$'') has $f(x)$ within $\varepsilon$ of $L$. If you can always reply, the limit is $L$. The condition $0<|x-a|$ is the formal version of ``the limit does not care about $x=a$''.

\begin{center}
\begin{tikzpicture}[scale=1.45]
\fill[black!10] (2.0,0)--(3.0,0)--(3.0,3.5)--(2.0,3.5)--cycle;
\fill[black!22] (0,0.9)--(5.0,0.9)--(5.0,1.6)--(0,1.6)--cycle;
\draw[-Latex] (-0.3,0)--(5.4,0) node[right]{$x$};
\draw[-Latex] (0,-0.3)--(0,3.8) node[above]{$y$};
\draw[thick,domain=0.4:4.6,smooth] plot(\x,{0.5+0.12*\x*\x});
\draw[dashed] (2.5,0)--(2.5,1.25)--(0,1.25);
\draw (0,0.9)--(-0.08,0.9) node[left]{$L-\varepsilon$};
\draw (0,1.6)--(-0.08,1.6) node[left]{$L+\varepsilon$};
\node[left] at (-0.08,1.25){$L$};
\draw (2.0,0)--(2.0,-0.08) node[below left,inner sep=1pt]{$a-\delta$};
\draw (3.0,0)--(3.0,-0.08) node[below right,inner sep=1pt]{$a+\delta$};
\node[below] at (2.5,-0.05){$a$};
\draw[fill=white] (2.5,1.25) circle(2pt);
\node[align=left,font=\small,anchor=west] at (5.1,1.25){every $x$ in the light strip\\lands in the dark band};
\end{tikzpicture}
\end{center}
In the figure the dark horizontal band is $|y-L|<\varepsilon$ and the light vertical strip is $|x-a|<\delta$. The definition says: shrink the band as much as you like; you can always find a strip so narrow that the graph over the strip (apart from the point at $a$, drawn hollow) stays inside the band.

\begin{example}[An $\varepsilon$--$\delta$ proof]
Prove from the definition that $\lim_{x\to2}(3x-1)=5$.
\end{example}
\begin{solution}
Let $\varepsilon>0$ be given. We need $|(3x-1)-5|<\varepsilon$, that is $|3x-6|<\varepsilon$, that is $3|x-2|<\varepsilon$, that is $|x-2|<\varepsilon/3$. So choose $\delta=\varepsilon/3$. Then
\[
0<|x-2|<\delta\ \Longrightarrow\ |(3x-1)-5|=3|x-2|<3\delta=\varepsilon .
\]
Since $\varepsilon>0$ was arbitrary, $\lim_{x\to2}(3x-1)=5$ by definition.
\end{solution}

\begin{example}[A quadratic]
Prove that $\lim_{x\to3}x^2=9$.
\end{example}
\begin{solution}
Let $\varepsilon>0$. We have $|x^2-9|=|x-3|\,|x+3|$. The factor $|x+3|$ is not constant, so first restrict $x$: if $|x-3|<1$ then $2<x<4$, so $|x+3|<7$. Then $|x^2-9|<7|x-3|$, which is $<\varepsilon$ when $|x-3|<\varepsilon/7$. Choose $\delta=\min\{1,\varepsilon/7\}$. For $0<|x-3|<\delta$ both restrictions hold, so $|x^2-9|<7\cdot\frac{\varepsilon}{7}=\varepsilon$. Hence $\lim_{x\to3}x^2=9$.
\end{solution}

\begin{tipbox}
The DU papers so far have not asked for an $\varepsilon$--$\delta$ proof, but the syllabus includes the definition, and ``define the limit of a function'' is a natural 2-mark start to a part. Write it exactly as in the definition above, including ``$0<|x-a|<\delta$''.
\end{tipbox}

\section{One-sided limits}\label{sec:lim-onesided}

Many functions behave differently on the two sides of a point: $|x|/x$ is $1$ for $x>0$ and $-1$ for $x<0$. To handle this we look at each side separately.

\begin{definition}[Left-hand and right-hand limits]
$\lim_{x\to a^+}f(x)=L$ (the \emph{right-hand limit}, RHL) if for every $\varepsilon>0$ there is $\delta>0$ with $|f(x)-L|<\varepsilon$ whenever $a<x<a+\delta$.\\
$\lim_{x\to a^-}f(x)=L$ (the \emph{left-hand limit}, LHL) if for every $\varepsilon>0$ there is $\delta>0$ with $|f(x)-L|<\varepsilon$ whenever $a-\delta<x<a$.
\end{definition}
In practice the RHL is computed by putting $x=a+h$ and letting $h\to0$ through positive values, the LHL by putting $x=a-h$, $h\to0^+$:
\[
\text{RHL}=\lim_{h\to0^+}f(a+h),\qquad \text{LHL}=\lim_{h\to0^+}f(a-h).
\]
\begin{keybox}[Existence of a limit]
$\displaystyle\lim_{x\to a}f(x)$ exists and equals $L$ \quad$\iff$\quad $\displaystyle\lim_{x\to a^-}f(x)$ and $\displaystyle\lim_{x\to a^+}f(x)$ both exist and both equal $L$.\\[4pt]
So to \textbf{show that a limit does not exist}, show that one of the one-sided limits does not exist, or that $\text{LHL}\ne\text{RHL}$.
\end{keybox}
\emph{Why it is true.} If the two-sided limit is $L$, the $\delta$ that works for $0<|x-a|<\delta$ also works for each side separately. Conversely, if both sides have limit $L$ with $\delta_1$ (left) and $\delta_2$ (right) for a given $\varepsilon$, then $\delta=\min\{\delta_1,\delta_2\}$ works for both sides at once.

\subsection{The three past-paper ``does not exist'' questions}

\begin{example}[DU 2414 Q1(a)(i)]
Establish that $\displaystyle\lim_{x\to0}\frac{e^{1/x}-1}{e^{1/x}+1}$ does not exist.
\end{example}
\begin{solution}
Let $f(x)=\dfrac{e^{1/x}-1}{e^{1/x}+1}$, $x\ne0$. We find the two one-sided limits at $0$.

\textbf{Right-hand limit.} As $x\to0^+$, $\frac1x\to+\infty$, so $e^{1/x}\to\infty$ and $e^{-1/x}\to0$. Divide numerator and denominator by $e^{1/x}$:
\[
\lim_{x\to0^+}f(x)=\lim_{x\to0^+}\frac{1-e^{-1/x}}{1+e^{-1/x}}=\frac{1-0}{1+0}=1 .
\]
\textbf{Left-hand limit.} As $x\to0^-$, $\frac1x\to-\infty$, so $e^{1/x}\to0$:
\[
\lim_{x\to0^-}f(x)=\frac{0-1}{0+1}=-1 .
\]
Since $\text{RHL}=1\ne-1=\text{LHL}$, $\lim_{x\to0}f(x)$ does not exist.
\end{solution}
Notice the method. On the side where $e^{1/x}$ blows up, divide by $e^{1/x}$ so that every term either stays finite or goes to $0$; on the other side substitute $e^{1/x}\to0$ directly. You must \emph{not} write $\frac{\infty-1}{\infty+1}=1$: $\frac\infty\infty$ is not a number, and the examiner deducts for it.

\begin{example}[DU 1264 Q1(a)(i)]
Establish that $\displaystyle\lim_{x\to0}\frac{e^{1/x}-e^{-1/x}}{e^{1/x}+e^{-1/x}}$ does not exist.
\end{example}
\begin{solution}
Let $f(x)=\dfrac{e^{1/x}-e^{-1/x}}{e^{1/x}+e^{-1/x}}$, $x\ne0$.

\textbf{RHL.} As $x\to0^+$, $e^{1/x}\to\infty$ and $e^{-1/x}\to0$. Dividing above and below by $e^{1/x}$,
\[
\lim_{x\to0^+}f(x)=\lim_{x\to0^+}\frac{1-e^{-2/x}}{1+e^{-2/x}}=\frac{1-0}{1+0}=1 .
\]
\textbf{LHL.} As $x\to0^-$, $e^{1/x}\to0$ and $e^{-1/x}\to\infty$. Dividing above and below by $e^{-1/x}$,
\[
\lim_{x\to0^-}f(x)=\lim_{x\to0^-}\frac{e^{2/x}-1}{e^{2/x}+1}=\frac{0-1}{0+1}=-1 .
\]
$\text{RHL}\ne\text{LHL}$, hence the limit does not exist.
\end{solution}
(The function is $\tanh\frac1x$, \S\ref{sec:pre-exp}; its graph jumps from $-1$ to $1$ across $x=0$.)

\begin{example}[DU 12910 Q1(a)(i)]
Show that $\displaystyle\lim_{x\to0}\frac{x-|x|}{x}$ does not exist.
\end{example}
\begin{solution}
For $x>0$, $|x|=x$, so $\dfrac{x-|x|}{x}=\dfrac{x-x}{x}=0$. For $x<0$, $|x|=-x$, so $\dfrac{x-|x|}{x}=\dfrac{x+x}{x}=2$. Hence
\[
\lim_{x\to0^+}\frac{x-|x|}{x}=0,\qquad \lim_{x\to0^-}\frac{x-|x|}{x}=2 .
\]
The one-sided limits are unequal, so the limit does not exist.
\end{solution}

\begin{example}[Twisted: greatest integer]
Does $\lim_{x\to2}[x]$ exist? Does $\lim_{x\to 2.5}[x]$?
\end{example}
\begin{solution}
For $1\le x<2$, $[x]=1$; for $2\le x<3$, $[x]=2$. So $\lim_{x\to2^-}[x]=1$ and $\lim_{x\to2^+}[x]=2$: unequal, the limit at $2$ does not exist. Near $2.5$ (say on $(2,3)$) $[x]=2$ is constant, so $\lim_{x\to2.5}[x]=2$. In general $\lim_{x\to a}[x]$ fails to exist exactly at the integers.
\end{solution}

\section{Computing limits}\label{sec:lim-comp}

\subsection{Limit theorems}
\begin{theorem}[Algebra of limits]
If $\lim_{x\to a}f(x)=L$ and $\lim_{x\to a}g(x)=M$, then
\[
\lim(f\pm g)=L\pm M,\qquad \lim(cf)=cL,\qquad \lim(fg)=LM,\qquad \lim\frac fg=\frac LM\ \ (M\ne0).
\]
\end{theorem}
\emph{Proof of the sum rule} (the others are similar). Given $\varepsilon>0$, choose $\delta_1$ with $|f(x)-L|<\varepsilon/2$ for $0<|x-a|<\delta_1$, and $\delta_2$ with $|g(x)-M|<\varepsilon/2$ for $0<|x-a|<\delta_2$. With $\delta=\min\{\delta_1,\delta_2\}$ and $0<|x-a|<\delta$, the triangle inequality gives
\[
|(f+g)(x)-(L+M)|\le|f(x)-L|+|g(x)-M|<\tfrac\varepsilon2+\tfrac\varepsilon2=\varepsilon. \qquad\square
\]
The theorems only apply when the separate limits \emph{exist}. $\lim_{x\to0}x\sin\frac1x$ cannot be done as $(\lim x)(\lim\sin\frac1x)$, because $\lim_{x\to0}\sin\frac1x$ does not exist. That is what the squeeze theorem is for.

\subsection{Techniques for \texorpdfstring{$\frac00$}{0/0}}
When direct substitution gives $\frac00$, the formula must be changed before substituting. The three algebraic tools are:
\begin{enumerate}
\item \textbf{Factorise and cancel.} $\displaystyle\lim_{x\to2}\frac{x^3-8}{x^2-4}=\lim_{x\to2}\frac{(x-2)(x^2+2x+4)}{(x-2)(x+2)}=\frac{12}{4}=3$. (Cancelling is allowed because the limit never uses $x=2$.)
\item \textbf{Rationalise} (multiply by the conjugate).
\item \textbf{Reduce to a standard limit} ($\frac{\sin x}{x}\to1$ and its relatives, \S\ref{sec:pre-calc}).
\end{enumerate}
L'Hospital's rule (Chapter~\ref{ch:tay}) is a fourth tool, but in Q1 the examiner expects the elementary methods.

\begin{example}[DU 12910 Q1(a)(ii)]
Evaluate $\displaystyle\lim_{x\to1}\frac{x-1}{\sqrt x-1}$.
\end{example}
\begin{solution}
Direct substitution gives $\frac00$. For $x>0$, $x\ne1$, multiply numerator and denominator by $\sqrt x+1$:
\[
\frac{x-1}{\sqrt x-1}=\frac{(x-1)(\sqrt x+1)}{(\sqrt x-1)(\sqrt x+1)}=\frac{(x-1)(\sqrt x+1)}{x-1}=\sqrt x+1 .
\]
Hence $\displaystyle\lim_{x\to1}\frac{x-1}{\sqrt x-1}=\lim_{x\to1}(\sqrt x+1)=2$.
(Alternatively, $x-1=(\sqrt x-1)(\sqrt x+1)$ is a difference of squares.)
\end{solution}

\begin{example}[DU 3553 Q1(a)(ii)]
Evaluate $\displaystyle\lim_{x\to0}\frac{3\sin^{-1}x}{4x}$.
\end{example}
\begin{solution}
Put $\theta=\sin^{-1}x$, so $x=\sin\theta$, and $\theta\to0$ as $x\to0$ (because $\sin^{-1}$ is continuous and $\sin^{-1}0=0$). Then
\[
\lim_{x\to0}\frac{\sin^{-1}x}{x}=\lim_{\theta\to0}\frac{\theta}{\sin\theta}=\lim_{\theta\to0}\frac{1}{\sin\theta/\theta}=\frac11=1 .
\]
Therefore $\displaystyle\lim_{x\to0}\frac{3\sin^{-1}x}{4x}=\frac34\lim_{x\to0}\frac{\sin^{-1}x}{x}=\frac34$.
\end{solution}

\subsection{The squeeze (sandwich) theorem}
\begin{theorem}[Squeeze theorem]
If $g(x)\le f(x)\le h(x)$ for all $x\ne a$ in an open interval around $a$, and $\lim_{x\to a}g(x)=\lim_{x\to a}h(x)=L$, then $\lim_{x\to a}f(x)=L$.
\end{theorem}
\emph{Proof.} Given $\varepsilon>0$ choose $\delta$ so small that, for $0<|x-a|<\delta$, the inequality $g\le f\le h$ holds and $L-\varepsilon<g(x)$ and $h(x)<L+\varepsilon$. Then $L-\varepsilon<g(x)\le f(x)\le h(x)<L+\varepsilon$, i.e.\ $|f(x)-L|<\varepsilon$. $\square$

The most common use: \emph{a quantity tending to $0$, times a bounded quantity, tends to $0$}. If $|f(x)|\le M|g(x)|$ and $g(x)\to0$, then $-M|g(x)|\le f(x)\le M|g(x)|$ squeezes $f(x)\to0$.

\begin{center}
\begin{tikzpicture}[xscale=2.6,yscale=1.6]
\draw[-Latex] (-1.4,0)--(1.5,0) node[right]{$x$};
\draw[-Latex] (0,-1.5)--(0,1.7) node[above]{$y$};
\draw[dashed,domain=-1.15:1.15,smooth] plot(\x,{\x*\x}) node[right]{$y=x^2$};
\draw[dashed,domain=-1.15:1.15,smooth] plot(\x,{-\x*\x}) node[right]{$y=-x^2$};
\draw[thick,domain=0.2:1.15,samples=300,smooth] plot(\x,{\x*\x*sin(1/(\x*\x) r)});
\draw[thick,domain=-1.15:-0.2,samples=300,smooth] plot(\x,{\x*\x*sin(1/(\x*\x) r)});
\fill (0,0) circle(0.9pt);
\end{tikzpicture}

{\small The solid curve $y=x^2\sin\frac1{x^2}$ oscillates ever faster near $0$ but stays between the dashed parabolas $y=\pm x^2$, so it is forced to $0$.}
\end{center}

\begin{example}[DU 3553 Q1(a)(i)]
Evaluate $\displaystyle\lim_{x\to0}x^2\sin\frac{1}{x^2}$.
\end{example}
\begin{solution}
The limit $\lim_{x\to0}\sin\frac1{x^2}$ does not exist (the sine oscillates between $-1$ and $1$ infinitely often near $0$), so the product rule cannot be used. Instead, for every $x\ne0$,
\[
-1\le\sin\frac1{x^2}\le1\quad\Longrightarrow\quad -x^2\le x^2\sin\frac1{x^2}\le x^2 .
\]
Since $\lim_{x\to0}(-x^2)=0=\lim_{x\to0}x^2$, the squeeze theorem gives $\displaystyle\lim_{x\to0}x^2\sin\frac1{x^2}=0$.
\end{solution}

\begin{example}[Twisted]
Find $\displaystyle\lim_{x\to0}\frac{\sin 5x}{\sin 3x}$ and $\displaystyle\lim_{x\to0}\frac{1-\cos 4x}{x^2}$.
\end{example}
\begin{solution}
$\dfrac{\sin5x}{\sin3x}=\dfrac{\sin5x}{5x}\cdot\dfrac{3x}{\sin3x}\cdot\dfrac53\to1\cdot1\cdot\dfrac53=\dfrac53$.\\[3pt]
$1-\cos4x=2\sin^22x$, so $\dfrac{1-\cos4x}{x^2}=2\cdot\left(\dfrac{\sin2x}{2x}\right)^2\cdot4\to8$.
\end{solution}

\subsection{Limits involving infinity}
$\lim_{x\to\infty}f(x)=L$ means $f(x)$ is within $\varepsilon$ of $L$ for all sufficiently large $x$; $\lim_{x\to a}f(x)=\infty$ means $f(x)$ exceeds any given number for $x$ close enough to $a$. These are used for asymptotes in Chapter~\ref{ch:cur}. For a rational function as $x\to\pm\infty$, divide numerator and denominator by the highest power of $x$ in the denominator:
\[
\lim_{x\to\infty}\frac{3x^2+1}{2x^2-x}=\lim_{x\to\infty}\frac{3+1/x^2}{2-1/x}=\frac32,\qquad \lim_{x\to\infty}\frac{x+1}{x^2+3}=\lim_{x\to\infty}\frac{1/x+1/x^2}{1+3/x^2}=0 .
\]
Writing $\infty$ for a limit is a statement that the limit \emph{does not exist} in a particular way; it is not a number, and $\infty-\infty$ or $\frac\infty\infty$ have no value.

\section{Continuity}\label{sec:lim-cont}

\subsection{Definition}
Intuitively a function is continuous if its graph can be drawn without lifting the pen. Precisely:
\begin{definition}[Continuity at a point]
$f$ is \emph{continuous at $a$} if
\[
\lim_{x\to a}f(x)=f(a),
\]
that is, (i) $f(a)$ is defined, (ii) $\lim_{x\to a}f(x)$ exists, and (iii) the two are equal. In $\varepsilon$--$\delta$ form: for every $\varepsilon>0$ there is $\delta>0$ with $|f(x)-f(a)|<\varepsilon$ whenever $|x-a|<\delta$.
\end{definition}
(Here $0<$ is not needed in front of $|x-a|$: at $x=a$ the inequality $|f(a)-f(a)|<\varepsilon$ is automatic.)

\begin{keybox}[Test for continuity at a point $a$]
Compute \quad $\text{LHL}=\lim_{h\to0^+}f(a-h)$,\quad $\text{RHL}=\lim_{h\to0^+}f(a+h)$,\quad and $f(a)$.\\[3pt]
$f$ is continuous at $a$ \quad$\iff$\quad $\text{LHL}=\text{RHL}=f(a)$.
\end{keybox}
$f$ is \emph{continuous on an open interval} if it is continuous at every point of it, and \emph{continuous on $[a,b]$} if in addition it is right-continuous at $a$ ($\lim_{x\to a^+}f(x)=f(a)$) and left-continuous at $b$ ($\lim_{x\to b^-}f(x)=f(b)$). At an end point of the domain only the one side inside the domain is checked.

\begin{theorem}[Continuous functions]
Polynomials, $\sin x$, $\cos x$, $e^x$ are continuous on $\R$; $\log x$ on $(0,\infty)$; $\sqrt x$ on $[0,\infty)$; a rational function wherever its denominator is not zero; $\sin^{-1}x$, $\cos^{-1}x$ on $[-1,1]$, $\tan^{-1}x$ on $\R$. Sums, differences, products, quotients (where the denominator is non-zero) and compositions of continuous functions are continuous.
\end{theorem}
This theorem is why piecewise questions only ask about the \emph{joining points}: inside each piece the formula is a polynomial (or another continuous function), so it is automatically continuous there. Say so in your answer, in one sentence.

\subsection{Types of discontinuity}\label{sec:lim-types}
If $f$ is not continuous at $a$, it is \emph{discontinuous} at $a$. The papers ask you to ``classify'' or ``discuss the type'' of each discontinuity, so learn these names.

\begin{keybox}[Classification of discontinuities]
\textbf{Removable discontinuity.} $\text{LHL}=\text{RHL}$ (the limit exists) but either $f(a)$ is not defined or $f(a)\ne$ the limit. It can be removed by redefining $f(a)$ as the limit.\\[3pt]
\textbf{Discontinuity of the first kind (jump).} LHL and RHL both exist (finite) but $\text{LHL}\ne\text{RHL}$. The jump is $\text{RHL}-\text{LHL}$.\\[3pt]
\textbf{Discontinuity of the second kind.} At least one of LHL, RHL does not exist (it is infinite, or the function oscillates). Example: $\frac1x$ at $0$ (infinite), $\sin\frac1x$ at $0$ (oscillatory).\\[3pt]
A \emph{mixed} discontinuity: one side exists and the other does not (counted as second kind). Some books also call a removable discontinuity a discontinuity of the first kind; when that happens say ``removable discontinuity of the first kind''.
\end{keybox}

\begin{center}
\begin{tikzpicture}[scale=0.82]
\begin{scope}
\draw[-Latex] (-0.2,0)--(3.2,0); \draw[-Latex] (0,-0.2)--(0,2.6);
\draw[thick] (0.2,0.5) .. controls (1,1.0) .. (1.5,1.3) .. controls (2,1.6) .. (2.9,1.8);
\draw[fill=white] (1.5,1.3) circle(2.2pt); \fill (1.5,2.2) circle(2.2pt);
\draw[dashed] (1.5,0)--(1.5,1.2); \node[below] at (1.5,0){$a$};
\node[below,font=\small] at (1.5,-0.5){removable};
\end{scope}
\begin{scope}[xshift=4.2cm]
\draw[-Latex] (-0.2,0)--(3.2,0); \draw[-Latex] (0,-0.2)--(0,2.6);
\draw[thick] (0.2,0.5)--(1.5,1.0); \draw[thick] (1.5,1.9)--(2.9,2.3);
\fill (1.5,1.0) circle(2.2pt); \draw[fill=white] (1.5,1.9) circle(2.2pt);
\draw[dashed] (1.5,0)--(1.5,1.0); \node[below] at (1.5,0){$a$};
\node[below,font=\small] at (1.5,-0.5){first kind (jump)};
\end{scope}
\begin{scope}[xshift=8.4cm]
\draw[-Latex] (-0.2,0)--(3.2,0); \draw[-Latex] (0,-0.2)--(0,2.6);
\draw[thick,domain=0.2:1.25,smooth] plot(\x,{0.25/(1.5-\x)});
\draw[thick,domain=1.75:2.9,smooth] plot(\x,{0.25/(\x-1.5)});
\draw[dashed] (1.5,0)--(1.5,2.5); \node[below] at (1.5,0){$a$};
\node[below,font=\small] at (1.5,-0.5){second kind (infinite)};
\end{scope}
\end{tikzpicture}
\end{center}

\subsection{Piecewise functions: the past-paper questions}
Every piecewise question is answered in the same four steps:
\begin{enumerate}
\item One sentence: on each open piece $f$ is a polynomial, hence continuous; only the joining points need checking.
\item At each joining point $a$, decide which formula applies \emph{to the left} ($x<a$), \emph{to the right} ($x>a$) and \emph{at} $a$ (look at $\le$, $<$).
\item Compute LHL, RHL, $f(a)$ and compare.
\item Conclude: continuous, or discontinuous with its type.
\end{enumerate}

\begin{example}[DU 12910 Q1(b)]
Examine the continuity at $x=1$ and $x=2$ of
\[
f(x)=\begin{cases}2x,&0\le x\le1\\ 2-x,&1<x\le2\\ x^2-2x,&x>2\end{cases}
\]
and state the type of discontinuity, if any.
\end{example}
\begin{solution}
Each piece is a polynomial, so $f$ is continuous on $(0,1)$, $(1,2)$ and $(2,\infty)$; we check $x=1$ and $x=2$.

\textbf{At $x=1$.} $f(1)=2(1)=2$ (first piece, since $1\le1$).
\[
\text{LHL}=\lim_{h\to0^+}f(1-h)=\lim_{h\to0^+}2(1-h)=2,
\]
\[
\text{RHL}=\lim_{h\to0^+}f(1+h)=\lim_{h\to0^+}\bigl(2-(1+h)\bigr)=1 .
\]
$\text{LHL}=2\ne1=\text{RHL}$. Both one-sided limits exist but are unequal, so $f$ is discontinuous at $x=1$ with a \textbf{discontinuity of the first kind (jump)} of size $1-2=-1$. ($f$ is left-continuous there, since $\text{LHL}=f(1)$.)

\textbf{At $x=2$.} $f(2)=2-2=0$ (second piece).
\[
\text{LHL}=\lim_{h\to0^+}\bigl(2-(2-h)\bigr)=\lim_{h\to0^+}h=0,\qquad \text{RHL}=\lim_{h\to0^+}\bigl((2+h)^2-2(2+h)\bigr)=4-4=0 .
\]
$\text{LHL}=\text{RHL}=f(2)=0$, so $f$ is continuous at $x=2$.
\end{solution}

\begin{example}[DU 1264 Q1(a)(ii)]
Examine the continuity of
\[
g(x)=\begin{cases}-x^2,&x\le0\\ 5x-4,&0<x\le1\\ 4x^2-3x,&1<x<2\\ 3x+4,&x\ge2\end{cases}
\]
at $x=0,1,2$ and discuss the type of discontinuities, if any.
\end{example}
\begin{solution}
Each piece is a polynomial, so $g$ is continuous except possibly at $0,1,2$.

\textbf{At $x=0$.} $g(0)=-0^2=0$. $\text{LHL}=\lim_{h\to0^+}\bigl(-(-h)^2\bigr)=0$. $\text{RHL}=\lim_{h\to0^+}(5h-4)=-4$.\\
$\text{LHL}\ne\text{RHL}$, both finite: \textbf{discontinuity of the first kind (jump)} at $0$.

\textbf{At $x=1$.} $g(1)=5-4=1$. $\text{LHL}=\lim_{h\to0^+}\bigl(5(1-h)-4\bigr)=1$. $\text{RHL}=\lim_{h\to0^+}\bigl(4(1+h)^2-3(1+h)\bigr)=4-3=1$.\\
$\text{LHL}=\text{RHL}=g(1)=1$: $g$ is \textbf{continuous} at $1$.

\textbf{At $x=2$.} $g(2)=3(2)+4=10$. $\text{LHL}=\lim_{h\to0^+}\bigl(4(2-h)^2-3(2-h)\bigr)=16-6=10$. $\text{RHL}=\lim_{h\to0^+}\bigl(3(2+h)+4\bigr)=10$.\\
$\text{LHL}=\text{RHL}=g(2)$: $g$ is \textbf{continuous} at $2$.

So $g$ is continuous everywhere except at $x=0$, where it has a jump discontinuity.
\end{solution}

\begin{example}[DU 2414 Q1(a)(ii)]
Examine the continuity of
\[
f(x)=\begin{cases}0,&x=0,\ \tfrac12\\ \tfrac12-x,&0<x<\tfrac12\\ 4x^2-1,&\tfrac12<x<\tfrac34\\ 1-x^2,&\tfrac34\le x\le1\end{cases}
\]
at $x=0,\frac12,\frac34$ and $1$. Classify the discontinuities, if any.
\end{example}
\begin{solution}
The domain is $[0,1]$. On each open piece $f$ is a polynomial, so only the four listed points need checking.

\textbf{At $x=0$} (left end of the domain, so only the right side). $f(0)=0$ and
$\text{RHL}=\lim_{h\to0^+}\bigl(\tfrac12-h\bigr)=\tfrac12\ne f(0)$.
$f$ is discontinuous at $0$. The right-hand limit exists but differs from the value; since only one side is available, this is a \textbf{removable discontinuity} (redefining $f(0)=\frac12$ makes $f$ right-continuous at $0$).

\textbf{At $x=\frac12$.} $f(\frac12)=0$.
$\text{LHL}=\lim_{h\to0^+}\bigl(\tfrac12-(\tfrac12-h)\bigr)=\lim h=0$;
$\text{RHL}=\lim_{h\to0^+}\bigl(4(\tfrac12+h)^2-1\bigr)=4\cdot\tfrac14-1=0$.
$\text{LHL}=\text{RHL}=f(\frac12)=0$: \textbf{continuous} at $\frac12$.

\textbf{At $x=\frac34$.} $f(\frac34)=1-\frac9{16}=\frac7{16}$.
$\text{LHL}=\lim_{h\to0^+}\bigl(4(\tfrac34-h)^2-1\bigr)=4\cdot\tfrac9{16}-1=\tfrac54$;
$\text{RHL}=\lim_{h\to0^+}\bigl(1-(\tfrac34+h)^2\bigr)=\tfrac7{16}$.
$\text{LHL}=\frac54\ne\frac7{16}=\text{RHL}$, both finite: \textbf{discontinuity of the first kind (jump)} at $\frac34$ ($f$ is right-continuous there).

\textbf{At $x=1$} (right end, only the left side). $f(1)=1-1=0$ and $\text{LHL}=\lim_{h\to0^+}\bigl(1-(1-h)^2\bigr)=0=f(1)$: $f$ is \textbf{continuous} (from the left) at $1$.
\end{solution}
\begin{tipbox}
At an end point of the domain some books call the failure at $x=0$ above ``a discontinuity of the first kind from the right''. Either name earns the marks if you state clearly what the one-sided limit and the value are. What loses marks is saying ``LHL does not exist'' at $x=0$ and stopping: there is no left side in the domain, so the LHL is simply not considered.
\end{tipbox}

\begin{example}[Twisted: find the constant]
Find $k$ so that $f(x)=\begin{cases}kx+1,&x\le3\\ 3x-5,&x>3\end{cases}$ is continuous at $x=3$.
\end{example}
\begin{solution}
$f(3)=\text{LHL}=3k+1$ and $\text{RHL}=9-5=4$. Continuity needs $3k+1=4$, so $k=1$.
\end{solution}

\begin{example}[Removable discontinuity]
Classify the discontinuity of $f(x)=\dfrac{\sin x}{x}$ $(x\ne0)$, $f(0)=0$, at $x=0$.
\end{example}
\begin{solution}
$\lim_{x\to0}\frac{\sin x}{x}=1$, so LHL $=$ RHL $=1$, but $f(0)=0\ne1$. The limit exists and differs from the value: a \textbf{removable discontinuity}. Redefining $f(0)=1$ makes $f$ continuous.
\end{solution}

\section{Differentiability}\label{sec:lim-diff}

\subsection{Definition and one-sided derivatives}
\begin{definition}[Derivative]
$f$ is \emph{differentiable at $a$} if the limit
\[
f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}
\]
exists (as a finite number). Geometrically it is the slope of the tangent to $y=f(x)$ at $(a,f(a))$: the limit of the slopes of chords joining $(a,f(a))$ to nearby points $(a+h,f(a+h))$.
\end{definition}
Since this is a limit, it exists exactly when the two one-sided versions exist and agree:
\begin{keybox}[Left and right derivatives]
$\displaystyle Rf'(a)=\lim_{h\to0^+}\frac{f(a+h)-f(a)}{h},\qquad Lf'(a)=\lim_{h\to0^+}\frac{f(a-h)-f(a)}{-h}.$\\[4pt]
$f$ is differentiable at $a$ \quad$\iff$\quad $Lf'(a)$ and $Rf'(a)$ exist (finite) and $Lf'(a)=Rf'(a)$; then $f'(a)$ is their common value.
\end{keybox}
Note the $-h$ in the denominator of $Lf'(a)$: the step from $a$ to $a-h$ is $-h$. Forgetting the minus sign is the most common error in these questions and gives the wrong sign for $Lf'$.

\begin{center}
\begin{tikzpicture}[scale=1.0]
\draw[-Latex] (-2.4,0)--(2.6,0) node[right]{$x$};
\draw[-Latex] (0,-0.3)--(0,2.4) node[above]{$y$};
\draw[thick] (-2,2)--(0,0)--(2,2);
\node[font=\small] at (-1.6,0.35){slope $-1$}; \node[font=\small] at (1.6,0.35){slope $+1$};
\node[below right] at (0,0){$O$}; \node[right] at (2,2){$y=|x|$};
\end{tikzpicture}
\end{center}

\begin{example}[The standard counterexample]
Show that $f(x)=|x|$ is continuous but not differentiable at $0$.
\end{example}
\begin{solution}
\emph{Continuity.} $\lim_{x\to0^\pm}|x|=0=f(0)$, so $f$ is continuous at $0$.

\emph{Differentiability.} $Rf'(0)=\lim_{h\to0^+}\frac{|h|-0}{h}=\lim\frac hh=1$ and $Lf'(0)=\lim_{h\to0^+}\frac{|-h|-0}{-h}=\lim\frac{h}{-h}=-1$. Since $Lf'(0)\ne Rf'(0)$, $f$ is not differentiable at $0$. The graph has a corner there: two different one-sided tangents.
\end{solution}

\subsection{Differentiability implies continuity}
\begin{theorem}
If $f$ is differentiable at $a$, then $f$ is continuous at $a$.
\end{theorem}
\emph{Proof.} For $h\ne0$,
\[
f(a+h)-f(a)=\frac{f(a+h)-f(a)}{h}\cdot h .
\]
As $h\to0$ the first factor tends to $f'(a)$ (a finite number) and the second to $0$. By the product rule for limits, $\lim_{h\to0}\bigl(f(a+h)-f(a)\bigr)=f'(a)\cdot0=0$, i.e.\ $\lim_{x\to a}f(x)=f(a)$. So $f$ is continuous at $a$. $\square$

The converse is \emph{false}: $|x|$ is continuous at $0$ but not differentiable there. So:
\begin{keybox}[Logic of a ``continuity and differentiability'' question]
differentiable $\Longrightarrow$ continuous;\qquad not continuous $\Longrightarrow$ not differentiable;\\
continuous $\not\Longrightarrow$ differentiable (check $Lf'$ and $Rf'$ separately).
\end{keybox}
So in a question that asks for both, check continuity first. If $f$ is discontinuous at $a$ you may stop: it cannot be differentiable there (quote the theorem).

\subsection{The past-paper questions}

\begin{example}[DU 3553 Q1(b)]
Examine the continuity and differentiability of
$f(x)=\begin{cases}x^2\cos\dfrac1x,&x\ne0\\ 0,&x=0.\end{cases}$
\end{example}
\begin{solution}
\textbf{For $x\ne0$.} $x^2$ and $\cos\frac1x$ are continuous and differentiable for $x\ne0$ (composition and product of differentiable functions), so $f$ is continuous and differentiable at every $x\ne0$, with
\[
f'(x)=2x\cos\frac1x+x^2\left(-\sin\frac1x\right)\left(-\frac1{x^2}\right)=2x\cos\frac1x+\sin\frac1x .
\]
\textbf{Continuity at $0$.} Since $|\cos\frac1x|\le1$, $\ -x^2\le x^2\cos\frac1x\le x^2$ for $x\ne0$. Both bounds tend to $0$, so by the squeeze theorem $\lim_{x\to0}f(x)=0=f(0)$. Hence $f$ is continuous at $0$.

\textbf{Differentiability at $0$.}
\[
f'(0)=\lim_{h\to0}\frac{f(h)-f(0)}{h}=\lim_{h\to0}\frac{h^2\cos\frac1h-0}{h}=\lim_{h\to0}h\cos\frac1h=0,
\]
again by squeezing ($-|h|\le h\cos\frac1h\le|h|$). The limit is the same from both sides (it is a two-sided limit), so $f$ is differentiable at $0$ with $f'(0)=0$.

\textbf{Conclusion.} $f$ is continuous and differentiable at every real $x$.
\end{solution}
\begin{remark}
Although $f'$ exists everywhere, $f'$ is \emph{not continuous} at $0$: $f'(x)=2x\cos\frac1x+\sin\frac1x$ and $\sin\frac1x$ has no limit as $x\to0$. This makes a good extra line in an answer (``$f$ is differentiable but not continuously differentiable at $0$'').
\end{remark}

\begin{example}[DU 12910 Q1(c)]
Discuss the differentiability at $x=0$ of $f(x)=x\,\dfrac{e^{1/x}-e^{-1/x}}{e^{1/x}+e^{-1/x}}$, $x\ne0$, and $f(0)=0$.
\end{example}
\begin{solution}
\textbf{Right derivative.}
\[
Rf'(0)=\lim_{h\to0^+}\frac{f(h)-f(0)}{h}=\lim_{h\to0^+}\frac{e^{1/h}-e^{-1/h}}{e^{1/h}+e^{-1/h}}=\lim_{h\to0^+}\frac{1-e^{-2/h}}{1+e^{-2/h}}=\frac{1-0}{1+0}=1,
\]
dividing by $e^{1/h}$, since $e^{-2/h}\to0$ as $h\to0^+$.

\textbf{Left derivative.}
\[
Lf'(0)=\lim_{h\to0^+}\frac{f(-h)-f(0)}{-h}=\lim_{h\to0^+}\frac{-h\,\dfrac{e^{-1/h}-e^{1/h}}{e^{-1/h}+e^{1/h}}}{-h}=\lim_{h\to0^+}\frac{e^{-1/h}-e^{1/h}}{e^{-1/h}+e^{1/h}} .
\]
Divide by $e^{1/h}$: $\lim_{h\to0^+}\dfrac{e^{-2/h}-1}{e^{-2/h}+1}=\dfrac{0-1}{0+1}=-1$.

Since $Lf'(0)=-1\ne1=Rf'(0)$, $f$ is \textbf{not differentiable} at $x=0$.

\emph{Continuity at $0$} (worth adding): $\bigl|\frac{e^{1/x}-e^{-1/x}}{e^{1/x}+e^{-1/x}}\bigr|<1$ for $x\ne0$ (numerator smaller in size than the positive denominator), so $|f(x)|<|x|\to0=f(0)$. So $f$ is continuous but not differentiable at $0$, exactly like $|x|$: for small $x$, $f(x)\approx|x|$.
\end{solution}

\begin{example}[Twisted: $x\sin\frac1x$]
Show that $f(x)=x\sin\frac1x$ $(x\ne0)$, $f(0)=0$, is continuous but not differentiable at $0$.
\end{example}
\begin{solution}
Continuity: $|x\sin\frac1x|\le|x|\to0$, so $\lim_{x\to0}f(x)=0=f(0)$. Differentiability: $\frac{f(h)-f(0)}{h}=\sin\frac1h$, which oscillates between $-1$ and $1$ as $h\to0$ and has no limit (take $h=\frac{1}{n\pi}$ giving $0$, and $h=\frac{1}{2n\pi+\pi/2}$ giving $1$). So $f'(0)$ does not exist.
\end{solution}
Compare the three functions $x\sin\frac1x$ (continuous, not differentiable), $x^2\sin\frac1x$ or $x^2\cos\frac1x$ (differentiable, $f'$ not continuous) and $\sin\frac1x$ (not even continuous at $0$, any value $f(0)$, discontinuity of the second kind). Each extra power of $x$ buys one more degree of smoothness.

\begin{example}[Twisted: a piecewise function]
Is $f(x)=\begin{cases}x^2,&x\le1\\ 2x-1,&x>1\end{cases}$ differentiable at $x=1$?
\end{example}
\begin{solution}
$f(1)=1$; LHL $=1$, RHL $=2-1=1$: continuous.
$Rf'(1)=\lim_{h\to0^+}\frac{2(1+h)-1-1}{h}=2$;
$Lf'(1)=\lim_{h\to0^+}\frac{(1-h)^2-1}{-h}=\lim_{h\to0^+}\frac{-2h+h^2}{-h}=\lim(2-h)=2$.
Equal, so $f$ is differentiable at $1$ with $f'(1)=2$ (the line $y=2x-1$ is the tangent to $y=x^2$ at $(1,1)$).
\end{solution}

\section{Concepts and strategy}
\begin{itemize}
\item \textbf{Recognise the question.} ``Show the limit does not exist'' $\Rightarrow$ find LHL and RHL and show they differ. ``Evaluate'' $\Rightarrow$ factorise, rationalise, standard limit or squeeze. ``Examine continuity'' $\Rightarrow$ LHL, RHL, $f(a)$ at each joining point. ``Differentiability'' $\Rightarrow$ continuity first, then $Lf'(a)$ and $Rf'(a)$.
\item \textbf{Signals for two sides:} $|x|$, $\sqrt{x^2}$, $e^{1/x}$, $[x]$, a piecewise definition. Each forces you to split at the critical point.
\item \textbf{$e^{1/x}$ technique:} on the side where it blows up ($x\to0^+$ for $e^{1/x}$) divide by it; on the other side it tends to $0$; never write $\frac\infty\infty$.
\item \textbf{Bounded times small:} $x^n\sin\frac1x$, $x^n\cos\frac1{x^2}$ and the like are squeezed between $\pm|x|^n$.
\item \textbf{Classify every discontinuity} with its name and the reason (``both one-sided limits exist and are unequal, so a jump''). Unclassified discontinuities lose marks when the question says ``type''.
\item \textbf{Words that earn marks:} ``LHL $=\dots$, RHL $=\dots$, $f(a)=\dots$''; ``since LHL $\ne$ RHL, the limit does not exist''; ``since LHL $=$ RHL $=f(a)$, $f$ is continuous at $a$''; ``$Lf'(a)\ne Rf'(a)$, so $f$ is not differentiable at $a$''.
\item \textbf{Unseen variant plan:} any new function in this part is handled by the same three computations: one-sided limits, value, one-sided difference quotients.
\item \textbf{Traps:} the $-h$ in $Lf'$; using the wrong piece at a joining point (read $\le$ against $<$); cancelling to get a limit and then claiming the function is continuous where it is undefined.
\end{itemize}

\begin{psetbox}
\begin{enumerate}
\item Show that $\displaystyle\lim_{x\to0}\frac{|x|}{x}$ does not exist. \emph{Ans.} RHL $=1$, LHL $=-1$.
\item Show that $\displaystyle\lim_{x\to0}\frac{1}{1+e^{1/x}}$ does not exist. \emph{Ans.} RHL $=0$, LHL $=1$.
\item Evaluate $\displaystyle\lim_{x\to0}\frac{\sqrt{1+x}-1}{x}$, $\displaystyle\lim_{x\to0}\frac{\tan3x}{\sin2x}$, $\displaystyle\lim_{x\to0}x\cos\frac1{x}$. \emph{Ans.} $\frac12$, $\frac32$, $0$.
\item Prove from the definition that $\lim_{x\to1}(5x+2)=7$. \emph{Ans.} $\delta=\varepsilon/5$.
\item Examine the continuity of $f(x)=\begin{cases}x,&0\le x<1\\ 2-x,&1\le x\le2\\ x-\frac12x^2,&x>2\end{cases}$ at $x=1,2$. \emph{Ans.} Continuous at $1$; at $2$: $f(2)=0$, LHL $=0$, RHL $=0$, continuous.
\item Classify the discontinuity at $0$ of (a) $\dfrac{x^2+x}{x}$ $(x\ne0)$, $f(0)=0$; (b) $e^{1/x}$; (c) $\cos\frac1x$. \emph{Ans.} (a) removable (limit $1$); (b) second kind (RHL infinite, LHL $=0$); (c) second kind (oscillatory).
\item Find $a,b$ so that $f(x)=\begin{cases}ax+b,&x<1\\ 3,&x=1\\ x^2+b,&x>1\end{cases}$ is continuous at $1$. \emph{Ans.} $a+b=3=1+b$, so $b=2$, $a=1$.
\item Discuss the differentiability at $0$ of $f(x)=x\,\dfrac{e^{1/x}-1}{e^{1/x}+1}$, $f(0)=0$. \emph{Ans.} $Rf'(0)=1$, $Lf'(0)=-1$: continuous, not differentiable.
\item Show that $f(x)=|x-2|+|x|$ is continuous everywhere and find where it is not differentiable. \emph{Ans.} Not differentiable at $x=0$ and $x=2$.
\item Is $f(x)=x^2\sin\frac1x$ $(x\ne0)$, $f(0)=0$ differentiable at $0$? Is $f'$ continuous at $0$? \emph{Ans.} Yes, $f'(0)=0$; no.
\end{enumerate}
\end{psetbox}
````
