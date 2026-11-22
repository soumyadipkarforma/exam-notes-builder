# Style rules

Examples below come from a physics course. For other subjects, read `subject-adaptation.md` for what each rule becomes (a derivation may be a proof, a mechanism, an algorithm or an essay plan; a figure may be a diagram, timeline or table).

## The reader
A student who will not open the textbook, revising under time pressure, who must reproduce answers in the exam hall. Every sentence must help them understand, remember, or write an answer that earns marks.

## Completeness (decides marks)
1. **Every derivation complete.** Write each algebraic line and name the law used. Steps that real graders deducted for when they were skipped, and which must always be written:
   - the separation and integration after a substitution in an ODE (`(1−v²)dx = 2vx dv`, then integrate both sides);
   - the auxiliary equation `m² + 2γm + ω₀² = 0` before its roots;
   - the epsilon–delta line `ε_ijk ε_klm = δ_il δ_jm − δ_im δ_jl` before using it;
   - momentum at `t` and at `t + dt` written out in full (rocket);
   - integrals evaluated (`∫₀ᴸ y² dy = L³/3`), not "integrating we get";
   - for a maximum: differentiate, set to zero, solve (resonance frequency);
   - the trial solution substituted and coefficients compared (forced oscillator), not the amplitude quoted.
2. **"Show that" results are derived** from first principles in the notes, even if they are also on the formula sheet (`grad(1/r)` from `∂(1/r)/∂x = −x/r³`; FWHM from `exp(−x²/2σ²) = 1/2`).
3. **Every figure an examiner asks for is drawn** (TikZ/pgfplots): free-body diagrams, Lissajous figures, resonance curves, damping cases, normal modes, beats, orbits. A described figure earns zero for the figure.
4. **Assumptions and conventions stated**: frictionless, small angle, rolling without slipping (`v = Rω`), which damping symbol (`γ = b/m` or `β = b/2m`), the sign of `dm`.
5. **Numericals**: formula symbolically, numbers with units, answer with units and sensible significant figures; the constants used (`g = 9.8 m/s²`).
6. **Vectors**: magnitude and direction. **Series**: interval of convergence. **Results**: a one-line interpretation.

## Depth (lets students handle unseen questions)
- Open each idea with the physical picture in plain words before any mathematics.
- Explain *why* each method works (why an integrating factor makes an equation exact; why the CM frame simplifies a collision).
- Give the recognition test: which features of a question point to which method.
- Give a general plan for any problem of the type, then apply it.
- List traps examiners set, each with the correct reasoning.
- Cross-reference related ideas in other chapters with `\ref` (the damped-oscillator ODE appears in both the ODE chapter and the oscillations chapter).
- **Not too concise.** Prose surrounds every equation: what we are about to do, and what the result means. Bare formula lists belong only in the formula sheet. A section with fewer than ~150 words of explanation, excluding equations and examples, is too thin.

## Language
- Short sentences, active voice, present tense, one idea per paragraph.
- Define every symbol when it first appears in a section.
- No filler ("clearly", "obviously", "it is interesting to note").
- Consistent notation within a book; a `remark` explains where books differ.

## Layout (`templates/ocwnotes.sty`)
- 12 pt Times text and maths (newtx), line spread 1.22, block paragraphs with 8 pt between them.
- Body text at normal size. `\small` only inside figures; never shrink tables or paragraphs to fit; instead let tables wrap (`tabularx`) and split long equations (`aligned`, or a second display).
- Headings: "Chapter N" plus the title; numbered sections (17 pt) and subsections (14 pt).
- Boxes: `keybox` for results to memorise (grey panel, left rule, title on its own line); `tipbox` for exam notes; `psetbox` for problems; `solution` is indented under a faint rule. No long derivations inside boxes.
- Plots scale to the text width (`width=0.8\linewidth`), never a fixed width wider than about 13 cm.
- Black and white: curves differ by line style; grey fills of at most `black!4`–`gray!25`.
