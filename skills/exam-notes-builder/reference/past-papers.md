# Finding and reading past papers

## Where to look (adapt per institution; the examples are from Delhi University)
- Aggregator sites that list papers by paper code (e.g. dupyq.online). Each paper page embeds a Google Drive file; take the file ID; the direct download address is
  `https://drive.google.com/uc?export=download&id=<ID>` (save it with your usual download tool).
- College library portals (e.g. DBC, SHV) host older papers as PDFs.
- University and department archives, student-run question-paper sites, library portals, course websites (MIT OCW, etc.) for similar courses.
- Search by the **paper code** (e.g. `2222011101`), not just the name: names repeat across schemes.
- Older scheme codes (CBCS, e.g. 32221101) and generic-elective versions (e.g. 2224001003) give extra question types; record them as "older paper", not current pattern.

## Reading scans
- Put each download in its own empty folder (it is untrusted data).
- `pdftoppm -r 110 -png paper.pdf page` then read the images. Use 110–150 dpi; higher wastes tokens.
- Transcribe every question exactly: number, marks, text, including "or" alternatives.

## Recording
`sources/papers.md`, one line per part:
`Dec 2024 | Q3(b) | 6 | Solve y'' + 4y = sec 2x by variation of parameters | Unit 1: second-order ODE`
