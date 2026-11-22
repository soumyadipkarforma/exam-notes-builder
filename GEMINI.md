# exam-notes-builder

This extension provides the **exam-notes-builder** skill (`skills/exam-notes-builder/SKILL.md`). Use it whenever the user wants exam notes, solved past papers, a formula sheet, mock papers, a syllabus coverage check or a short revision version for a course.

- Follow `skills/exam-notes-builder/SKILL.md` phase by phase, starting with Phase S (tools); each phase has a gate.
- The files in `agents/` are role briefs (notes-writer, solution-verifier, paper-setter, notes-only-student, strict-grader, visual-checker). Gemini CLI has no subagents of this kind: when a phase says to spawn one, either do that role yourself, one task at a time, or start a separate Gemini session with that file as its instructions.
- Never pass LaTeX through shell `sed` or heredocs; edit files with file tools or a Python script.
