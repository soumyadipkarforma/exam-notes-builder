# scripts/contact_sheet.py

Save as `scripts/contact_sheet.py`

````python
"""Contact sheets for the visual check (Phase 7).

Renders every page of a PDF and tiles them, several pages per image, with the page
number printed above each page, so a person or a cheap vision subagent can scan a
150-page book in ~20 images. Also splits the sheets into batches, one per parallel
checker, and renders single pages at higher resolution for close-up checks.

  python contact_sheet.py main.pdf sheets/                 # 8 pages per sheet, 45 dpi
  python contact_sheet.py main.pdf sheets/ --batches 4     # also write batches.txt for 4 checkers
  python contact_sheet.py main.pdf sheets/ --zoom 37 52    # pages 37 and 52 at 100 dpi

Needs poppler (pdftoppm) and Pillow (https://pillow.readthedocs.io/en/stable/installation/basic-installation.html).
"""
import argparse
import glob
import os
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw


def render(pdf, dpi, out_prefix, first=None, last=None):
    cmd = ["pdftoppm", "-r", str(dpi), "-png"]
    if first:
        cmd += ["-f", str(first), "-l", str(last or first)]
    subprocess.run(cmd + [pdf, out_prefix], check=True)


def page_number(path):
    return int(os.path.basename(path).rsplit("-", 1)[1].split(".")[0])


def make_sheets(pdf, outdir, per, cols, dpi):
    tmp = tempfile.mkdtemp()
    try:
        render(pdf, dpi, os.path.join(tmp, "p"))
        pages = sorted(glob.glob(os.path.join(tmp, "p-*.png")), key=page_number)
        if not pages:
            raise SystemExit("no pages rendered: is %s a PDF?" % pdf)
        w, h = Image.open(pages[0]).size
        label, gap = 22, 10
        rows = -(-per // cols)
        sheets = []
        for s in range(0, len(pages), per):
            group = pages[s:s + per]
            sheet = Image.new("RGB", (cols * (w + gap) + gap, rows * (h + label + gap) + gap), "#9a9a9a")
            draw = ImageDraw.Draw(sheet)
            for i, p in enumerate(group):
                x = gap + (i % cols) * (w + gap)
                y = gap + (i // cols) * (h + label + gap)
                draw.text((x + 2, y + 4), "page %d" % page_number(p), fill="black")
                sheet.paste(Image.open(p).convert("RGB"), (x, y + label))
            first, last = page_number(group[0]), page_number(group[-1])
            name = os.path.join(outdir, "sheet_%03d-%03d.png" % (first, last))
            sheet.save(name)
            sheets.append(name)
        assert len(sheets) == -(-len(pages) // per)
        return sheets, len(pages)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--per", type=int, default=8, help="pages per sheet (default 8)")
    ap.add_argument("--cols", type=int, default=4, help="pages per row (default 4)")
    ap.add_argument("--dpi", type=int, default=45, help="sheet resolution (default 45)")
    ap.add_argument("--batches", type=int, default=0, help="split sheets into N batches for N parallel checkers")
    ap.add_argument("--zoom", type=int, nargs="+", help="render these pages alone at --zoom-dpi")
    ap.add_argument("--zoom-dpi", type=int, default=100)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    if a.zoom:
        for p in a.zoom:
            render(a.pdf, a.zoom_dpi, os.path.join(a.outdir, "zoom"), p, p)
        print("\n".join(sorted(glob.glob(os.path.join(a.outdir, "zoom-*.png")))))
        return

    sheets, n = make_sheets(a.pdf, a.outdir, a.per, a.cols, a.dpi)
    print("%d pages -> %d sheets in %s" % (n, len(sheets), a.outdir))
    if a.batches:
        k = max(1, min(a.batches, len(sheets)))
        size = -(-len(sheets) // k)
        with open(os.path.join(a.outdir, "batches.txt"), "w") as f:
            for b in range(k):
                part = sheets[b * size:(b + 1) * size]
                if part:
                    f.write("batch %d: %s\n" % (b + 1, " ".join(os.path.abspath(s) for s in part)))
        print(open(os.path.join(a.outdir, "batches.txt")).read())


if __name__ == "__main__":
    main()
````
