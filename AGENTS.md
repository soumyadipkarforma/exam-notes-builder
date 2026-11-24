# AGENTS.md

This folder is the **exam-notes-builder** skill. To build exam notes for any course, read `skills/exam-notes-builder/SKILL.md` and follow its phases in order; every phase has a gate that must pass before the next.

After editing anything in `skills/` or `agents/`, run `python tools/build_plugin.py` to regenerate `plugin/`.

Hard rules:
- Never pass LaTeX through shell `sed` or heredocs; use file-edit tools or Python script files.
- Build after every change: 0 errors, 0 undefined references, no overfull box > 3 pt.
- Never invent past-paper questions or years.
- Keep the 12 pt roomy layout of `skills/exam-notes-builder/templates/ocwnotes.sty`; never shrink text to make things fit.
- Start a course with `python skills/exam-notes-builder/scripts/new_course.py`; check every build with `python skills/exam-notes-builder/scripts/gates.py <notes_dir>` and fix the first FAIL it prints.
- Small models: follow `skills/exam-notes-builder/reference/runbook.md` step by step; one section at a time; re-read `skills/exam-notes-builder/reference/style-rules.md` and `skills/exam-notes-builder/reference/subject-adaptation.md` before each.

exam-notes-builder by Soumyadip Karforma (https://github.com/soumyadipkarforma/exam-notes-builder), MIT.
