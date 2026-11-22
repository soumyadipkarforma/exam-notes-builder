# scripts/syllabus_check.py

Save as `scripts/syllabus_check.py`

````python
r"""Check every syllabus item against the notes sources.

Usage: python syllabus_check.py <notes_dir> [<notes_dir> ...]
Each notes folder holds syllabus_checklist.tsv: one line per item, "item<TAB>regex" (regex searched
case-insensitively in all *.tex of that folder; # starts a comment). Prints MISSING items; exit 1 if any.
Write one line per syllabus line AND per standard derivation/proof/method a paper can ask for.
shortcut: presence of a regex only, not quality; read the hits for anything marginal.
"""
import glob, os, re, sys


def check(d):
    src = "\n".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(d, "*.tex")))
    rows = [l.rstrip("\n").split("\t", 1) for l in open(os.path.join(d, "syllabus_checklist.tsv"), encoding="utf-8")
            if l.strip() and not l.startswith("#")]
    miss = [n for n, rx in rows if not re.search(rx, src, re.I)]
    print(f"{d}: {len(rows) - len(miss)}/{len(rows)} found")
    for n in miss:
        print("   MISSING:", n)
    return not miss


if __name__ == "__main__":
    sys.exit(0 if all([check(d) for d in sys.argv[1:]]) else 1)
````
