# Setting mock papers

Use the real exam pattern (marks, number of parts, choice). For the test, tell the test-taker to attempt every question.

## Four kinds
| Kind | Source | Purpose |
|---|---|---|
| Book | end-of-chapter problems in the prescribed books | tests that book-style problems can be answered without the book |
| Old paper | older-scheme papers, other colleges, generic elective | tests question types not seen in the last 3 years |
| Unseen | new twists: different function, reversed question ("find the force law from the orbit"), concept ("explain why"), unusual units | tests understanding, not recall |
| Fusion | each question mixes 2–3 subjects taken together (e.g. divergence theorem → Gauss's law → tunnel through the Earth is SHM; ODE solution of a forced damped oscillator; Lorentz invariance of wave phase → Doppler) | tests transfer between subjects |

Rules:
- Never reuse a question solved word-for-word in the notes.
- Cover every unit; each long question has 2–3 parts of different types (derivation, numerical, concept).
- Write the answer key while setting and check every number (`python -I -c ...`).

## Paper template
```
# Mock Paper <<CODE>>: <<Course>> (<<kind>>)
Time <<3 hours>>. Max marks <<90>>. Q1 compulsory + any <<four>> of Q2-Q6 (<<18>> each).
FOR THIS TEST: ATTEMPT EVERY QUESTION.

Q1. Attempt all parts. (6 x 3 = 18)
(a) ...
(b) ...

Q2. (6 + 6 + 6)
(a) ...
```
Keep each part on one line starting with `(a)`, `(b)` under a `Qn.` line: `scripts/rag_exam.py` parses this format.
