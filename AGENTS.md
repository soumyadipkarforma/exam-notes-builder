# AGENTS.md

This folder is the **exam-notes-builder** skill. To build exam notes for any course, read `SKILL.md` and follow its phases in order; every phase has a gate that must pass before the next.

Hard rules:
- Never pass LaTeX through shell `sed` or heredocs; use file-edit tools or Python script files.
- Build after every change: 0 errors, 0 undefined references, no overfull box > 3 pt.
- Never invent past-paper questions or years.
- Keep the 12 pt roomy layout of `templates/ocwnotes.sty`; never shrink text to make things fit.
- Small models: one chapter at a time; re-read `reference/style-rules.md` and `reference/subject-adaptation.md` before each.
