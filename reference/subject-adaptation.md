# Adapting the method to any subject

The phases, gates, chapter order and grading classes are the same for every subject. What changes is what a "derivation", a "figure", a "numerical" and a "key result" mean, and how examiners give marks.

| Subject | "Derivation" (written in full, every step) | "Figure" the examiner expects | "Numerical" / applied question | Key-result box holds | Typical traps |
|---|---|---|---|---|---|
| Physics, engineering | derivation from laws, every algebraic line, law named | free-body diagram, circuit, graph, field lines | formula, substitution with units, answer with units | boxed law/result with validity | sign conventions, units, small-angle assumptions |
| Mathematics, statistics | proof or full method (each step justified by a theorem/definition) | sketch of region, graph, Venn/tree diagram | worked computation with checks | theorem statement with hypotheses | missing hypothesis, domain, constant of integration |
| Chemistry | mechanism with arrows, derivation of rate/equilibrium laws | structure, mechanism, energy profile, apparatus | stoichiometry/equilibrium calculation with units and sig figs | named reaction, rule, equation | conditions, stereochemistry, significant figures |
| Biology, medicine | process step by step (pathway, cycle, mechanism) | labelled diagram, flow chart of pathway | data interpretation, genetics ratios | definitions, key stages, numbers to memorise | precise terminology, labels, units |
| Computer science | algorithm with pseudocode, correctness argument, complexity derivation | trace table, data-structure diagram, automaton | trace on an input, complexity count | algorithm + complexity + invariant | off-by-one, edge cases, best vs worst case |
| Economics, finance | model derivation (equilibrium, optimisation, multiplier) | demand/supply or IS-LM diagram, shifts labelled | worked calculation (elasticity, NPV) | model result and assumptions | which curve shifts, ceteris paribus, real vs nominal |
| Law | structured answer: issue, rule (statute/case), application, conclusion | none; a statute/case table instead | problem question applied to facts | rule + leading case + citation | missing authority, wrong jurisdiction |
| History, social sciences, humanities | model essay plan: thesis, argued paragraphs with evidence, counter-argument, conclusion | timeline, map, comparison table | source analysis (provenance, content, context) | dates, names, causes/consequences, historiography | description instead of argument, no evidence, no judgement |
| Languages, literature | model answers with quotation analysis; grammar rule with examples | none; tables of forms | translation/composition with marking points | rule/paradigm, key quotations | register, tense, unsupported claims |

## How the writing rules translate
- **"Every step written"** = every reasoning step an examiner awards: in an essay each paragraph's point–evidence–explanation; in a proof each justified line; in an algorithm each invariant.
- **"Show that"** = any "explain / justify / prove / account for" question: the notes contain the full answer, not the conclusion.
- **Figures** = whatever diagram or table earns marks in that subject. A described figure earns nothing.
- **Units and numbers** = units in sciences; dates, names and citations in humanities and law.
- **Concepts and strategy** = the big picture of the unit, how to recognise each question type from its wording ("assess", "compare", "to what extent", "derive", "trace"), a plan for any unseen question, traps.
- **Formula sheet** becomes a fact sheet: definitions, dates, cases, reactions, rules, one per row.

## Mock exams
- Tiny models are still useful in essay subjects: they reveal facts, arguments and evidence the notes lack (write "NOT IN NOTES").
- The strict grader marks to the subject's real scheme (levels of response for essays, IRAC for law, method marks for calculations). Put that scheme into `grading-rubric.md` for the course before grading.

## Layout
`ocwnotes.sty` is subject-neutral; drop the vector macros in non-STEM courses. For essay subjects use `example` + `solution` as "question + model answer", and `keybox` for facts and frameworks.
