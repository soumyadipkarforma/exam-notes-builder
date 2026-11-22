r"""Find thin chapters/sections: prose words per section, examples and figures per chapter.
Usage: python depth_audit.py <notes_dir> [...]   (run from anywhere)
A section with < 180 words of prose outside examples/figures/problems is flagged as thin.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_check import plain

SKIP = re.compile(r"(guide|pyq|questions|formulas|school|fullmarks)")
for d in sys.argv[1:]:
    main = open(os.path.join(d, "main.tex"), encoding="utf-8").read()
    print("==", d)
    for f in re.findall(r"^\\include\{([^}]+)\}", main, re.M):
        if SKIP.search(f):
            continue
        src = open(os.path.join(d, f + ".tex"), encoding="utf-8").read()
        ex = len(re.findall(r"\\begin\{example\}", src))
        figs = len(re.findall(r"\\begin\{tikzpicture\}", src))
        thin = []
        secs = re.split(r"\\section\*?\{", src)[1:]
        for s in secs:
            title = s[:s.find("}")]
            body = re.sub(r"\\begin\{(example|solution|tikzpicture|psetbox)\}.*?\\end\{\1\}", " ", s, flags=re.S)
            n = len(plain(body))
            if n < 180 and "Further" not in title:
                thin.append(f"{title[:40]} ({n})")
        print(f"  {f:22s} words {len(plain(src)):5d}  examples {ex:3d}  figures {figs:2d}  sections {len(secs):2d}")
        for t in thin:
            print("      thin:", t)
