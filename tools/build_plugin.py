"""Build plugin/ : the Markdown-only copy of this repository that is submitted to the
Claude plugin directory.

The directory accepts only Markdown, text, JSON and images from unverified publishers,
so every script and template is wrapped in a Markdown file under
plugin/skills/exam-notes-builder/assets/, and SKILL.md gets a short "unpack" step.
The real files stay in skills/exam-notes-builder/ for git users and other agents.

Run after any change to skills/ or agents/:   python tools/build_plugin.py
The script then unpacks plugin/ again and checks every file round-trips exactly.
"""
import pathlib
import re
import shutil
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "skills" / "exam-notes-builder"
OUT = ROOT / "plugin"
SKILL_OUT = OUT / "skills" / "exam-notes-builder"
TEXT_OK = {".md"}
FENCE = "````"
LANG = {".py": "python", ".sh": "bash", ".tex": "latex", ".sty": "latex", ".tsv": "text", ".txt": "text"}

UNPACK = '''
## Setup: unpack the tools (plugin install only)
In this plugin the scripts and templates are stored as Markdown in `assets/` (the plugin directory accepts only Markdown). Once per project, before Phase 0, write each one out: every `assets/*.md` names its target path on a line starting with `Save as`, followed by one code block. Write that block, unchanged, to `exam-tools/<path>` in the project folder. Everywhere below, `scripts/...` and `templates/...` mean `exam-tools/scripts/...` and `exam-tools/templates/...`. This Python does it (save it as `exam-tools/unpack.py`, run `python exam-tools/unpack.py <this skill folder>/assets exam-tools`):

```python
import pathlib, re, sys
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
for f in sorted(src.glob("*.md")):
    t = f.read_text(encoding="utf-8")
    path = re.search(r"^Save as `([^`]+)`", t, re.M).group(1)
    code = re.search(r"^````[^\\n]*\\n(.*?)^````[ \\t]*$", t, re.S | re.M).group(1)
    p = out / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(code, encoding="utf-8", newline="\\n")
    print("wrote", p)
```
If you have the full repository (github.com/soumyadipkarforma/exam-notes-builder), the files already exist in `skills/exam-notes-builder/`; skip this step.
'''


def norm(text):
    return text.replace("\r\n", "\n")


def wrap(rel, text):
    assert FENCE not in text, rel
    if not text.endswith("\n"):
        text += "\n"
    return "# %s\n\nSave as `%s`\n\n%s%s\n%s%s\n" % (rel, rel, FENCE, LANG.get(pathlib.Path(rel).suffix, "text"), text, FENCE)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / ".claude-plugin").mkdir(parents=True)
    shutil.copy(ROOT / "tools" / "plugin.json", OUT / ".claude-plugin" / "plugin.json")
    shutil.copy(ROOT / "tools" / "icon.png", OUT / ".claude-plugin" / "icon.png")
    shutil.copytree(ROOT / "agents", OUT / "agents")
    shutil.copy(ROOT / "LICENSE", OUT / "LICENSE")
    wrapped = {}
    for f in sorted(SRC.rglob("*")):
        if f.is_dir():
            continue
        rel = f.relative_to(SRC).as_posix()
        text = norm(f.read_text(encoding="utf-8"))
        if f.suffix in TEXT_OK:
            if rel == "SKILL.md":
                cut = text.index("## Contents of this skill")
                text = text[:cut] + UNPACK.lstrip("\n") + "\n" + text[cut:]
                text = text.replace("| `reference/subject-adaptation.md` |",
                                    "| `assets/*.md` | Scripts and templates as Markdown; unpack them first (Setup above). |\n| `reference/subject-adaptation.md` |", 1)
            dest = SKILL_OUT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8", newline="\n")
        else:
            name = rel.replace("/", "__") + ".md"
            (SKILL_OUT / "assets").mkdir(parents=True, exist_ok=True)
            (SKILL_OUT / "assets" / name).write_text(wrap(rel, text), encoding="utf-8", newline="\n")
            wrapped[rel] = text
    (OUT / "README.md").write_text(
        "# exam-notes-builder (plugin)\n\n"
        "Builds complete, examiner-proof exam notes (LaTeX to PDF) for any course from a syllabus, textbooks and past papers, "
        "proves them complete with notes-only mock exams, checks every page visually, and produces a short Exam Core.\n\n"
        "This folder is generated from the repository by `tools/build_plugin.py`; scripts and templates are stored as Markdown in "
        "`skills/exam-notes-builder/assets/` and unpacked by the skill. Full documentation: "
        "https://github.com/soumyadipkarforma/exam-notes-builder\n\n## Install\n\n```\n"
        "/plugin install exam-notes-builder --marketplace soumyadipkarforma/exam-notes-builder\n```\n",
        encoding="utf-8", newline="\n")
    return wrapped


def check(wrapped):
    code = re.search(r"```python\n(.*?)\n```\n", UNPACK, re.S).group(1)
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        (tmp / "unpack.py").write_text(code, encoding="utf-8")
        import subprocess, sys
        subprocess.run([sys.executable, str(tmp / "unpack.py"), str(SKILL_OUT / "assets"), str(tmp / "out")],
                       check=True)
        for rel, text in wrapped.items():
            got = (tmp / "out" / rel).read_text(encoding="utf-8")
            assert got == text, "round-trip mismatch: " + rel
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bad = [p for p in OUT.rglob("*") if p.is_file() and p.suffix not in {".md", ".json", ".png"} and p.name != "LICENSE"]
    assert not bad, bad
    print("plugin/ built: %d files wrapped, round-trip exact, only .md/.json/.png" % len(wrapped))


if __name__ == "__main__":
    check(build())
