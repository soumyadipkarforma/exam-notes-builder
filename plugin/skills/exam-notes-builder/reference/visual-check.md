# Visual check of the built PDF (Phase 7)

LaTeX can compile with zero errors and still print a page a student cannot use: a figure label on top of a curve, tick labels colliding, a table running into the margin, a box split with one line on the next page, a half-empty page before a big figure. These are only found by looking. Reading 150 pages one by one is slow and expensive, so look at **contact sheets** (many pages per image) first, and zoom in only where something looks wrong.

## 1. Make the sheets
```bash
python <skill>/scripts/contact_sheet.py main.pdf _sheets --batches 4
```
- 8 pages per sheet (4 × 2) at 45 dpi: a 150-page book becomes ~19 images. Each page carries its PDF page number ("page 41") above it; use that number, not the printed folio, when you zoom or report.
- `--batches N` writes `_sheets/batches.txt`: the sheets split into N groups, one per checker.
- At 45 dpi body text is not readable, and does not need to be: layout faults (overlaps, overflow, gaps, crowded figures) are visible. Use `--per 4 --cols 2 --dpi 70` for a figure-heavy book if the figures look too small to judge.

## 2. Check the sheets with cheap parallel subagents
Spawn one `visual-checker` subagent per batch, **all in the same message** so they run in parallel. It runs on the cheapest vision-capable model (Haiku): spotting a label on a curve does not need a large model, and the main agent confirms every report anyway. Give each one only its line of `batches.txt`:

> Check these contact sheets of a printed study book for layout defects, following your instructions. Sheets: <paths from one batch line>. Zoom with: `python <skill>/scripts/contact_sheet.py <pdf> _sheets --zoom <pages>`.

Batch size: 4–6 sheets (32–48 pages) per checker. More checkers in parallel is faster and costs the same in total. Without subagents (or on a small model), check the sheets yourself one at a time with the same list below.

## 3. What counts as a defect
| Look for | Typical cause | Fix |
|---|---|---|
| Text or a label on top of a curve, axis or another label | pgfplots/TikZ node placed by hand | Move the node (`above left`, `pos=`), or put the legend outside (`legend pos=outer north east`) |
| Tick labels running into each other or into the curve | too many ticks, long numbers | Fewer `xtick`s, `scaled ticks=false`, white fill on tick labels (default in `ocwnotes.sty`) |
| A figure much smaller than its neighbours, or text in it that is unreadable when printed | `width` too small, `scale` | `width=0.8\linewidth`; never below 0.6 |
| Equation, table or URL sticking into the right margin | long display, wide `tabular` | Break with `aligned`/`multline`, use `tabularx`, `\allowbreak` |
| Mostly empty page followed by a figure or long box | float or unbreakable box pushed down | `[htbp]`, make the box `breakable`, move the figure |
| A heading alone at the bottom of a page, or a box with one line on the next page | page break in a bad place | `\needspace`, reorder, a shorter paragraph above |
| Box or solution frame running off the page or overlapping the footer | unbreakable tcolorbox longer than a page | `breakable` |
| Blank page in the middle of a chapter | `\cleardoublepage`, stray `\newpage` | Remove it |
| Running head or page number missing on a body page | `\thispagestyle` misuse | Remove the override |

Not defects: chapter openers (big gap on top by design), a short last page of a chapter, the title page.

## 4. Report format (checker → main agent)
One line per suspected defect, most serious first, nothing else:
```
page 42 | figure | legend box covers the dashed curve near the top right | zoom
page 77 | margin | display equation runs past the right edge | zoom
```
If a batch is clean, the report is `clean: pages 1-40`.

## 5. Confirm and fix (main agent)
1. Zoom on every reported page: `--zoom 42 77` renders those pages at 100 dpi. Small models report false positives (a dashed line read as an overlap); the zoom decides.
2. Fix the source, rebuild, re-render only the changed pages with `--zoom`, and look again.
3. Never shrink body text or a figure below 0.6 of the line width to make something fit.

**Gate 7:** a full pass of sheets with every report either fixed (zoom after the fix) or rejected (zoom shows no defect). Record the result in `PROGRESS.md`.
