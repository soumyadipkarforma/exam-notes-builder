# Strict grading rubric (human examiner style)

Grade every step. Read the whole answer before marking; do not reward a correct final number reached by wrong working.

## Mark split
- **3-mark short part**: law or formula (1), working (1), result with units or the stated conclusion (1).
- **6-mark derivation**: figure and assumptions (1–2), law applied and every intermediate line (2–3), result boxed and interpreted (1–2).
- **10-mark derivation**: figure and set-up (2), equation of motion with every step (5), solution and discussion (3).
- **Numerical**: formula symbolically (1–2), substitution with units (1–2), answer with units and sensible figures (1).

## Deductions
| Fault | Deduction |
|---|---|
| A step that carries marks is skipped | −0.5 to −1.5 |
| "Show that" answered by quoting the result | −1.5 (up to all method marks) |
| Sketch asked for but only described | −2.5 (all figure marks) |
| Rule or theorem used without saying which | −0.5 to −1 |
| "Find/derive" with no derivation | −2 |
| Missing or wrong units | −0.5 |
| Wrong sign or factor, method right | −1 |
| Final answer wrong, method right | keep method marks, lose result marks |
| Vector given without direction | −0.5 |
| Conclusion or interpretation missing where asked | −0.5 to −1 |

## Classify every lost mark
- **N, notes gap**: the method, result, derivation step, figure or example is missing, wrong or unclear in the notes. *Fix the notes.*
- **R, findability**: it is in the notes but the test-taker did not find it (buried, wrong heading, missing keywords, no cross-reference). *Retitle, add the question-type name to the heading, add a line to "How to recognise", add `\ref`s.*
- **S, slip**: the notes are right and findable; the test-taker erred. *No change, unless it is a common trap worth adding to "Traps".*

## Report format
```
## <<Paper>> by <<test-taker>>: exam <<x>>/<<max>>, all <<y>>/<<total>>
Q1 <<marks>>. (a) 3. (b) 2: <<what was lost and why>> [S]
Q2 <<marks>>. (a) 4.5: <<missing step>> [N: notes §3.2 skip the separation step]
...
### Fixes required
- [N] <<file:section>>: <<what to add>>
- [R] <<file:section>>: <<what to retitle or cross-reference>>
```
