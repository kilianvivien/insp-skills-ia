---
name: pdf-translate-format
description: Converts a PDF to Markdown, translates it to a target language, and generates a professionally formatted PDF with cover page and styled Table of Contents.
---

# PDF → Translate → Formatted PDF

Convert any PDF into a clean Markdown file, translate it, and produce a professional PDF with cover page and styled Table of Contents.

## Prerequisites

- `python3` with `pdfplumber` (`pip install pdfplumber`)
- `npx` (comes with Node.js)
- `md-to-pdf` (auto-installed via `npx -y md-to-pdf`)

## Usage

Ask the user for:
1. **`INPUT_PDF`** — path to the source PDF (e.g. `report.pdf`)
2. **`TARGET_LANGUAGE`** — language to translate into (e.g. `French`, `English`, `Spanish`)

Derive output names from the input:
- `OUTPUT_MD` = input name without extension + `_translated.md`
- `OUTPUT_PDF` = input name without extension + `_translated.pdf`

---

## Phase 1: PDF to Markdown

### Step 1 — Extract raw text

Write `scripts/extract_raw.py` to disk and run it:

```bash
python3 scripts/extract_raw.py "<INPUT_PDF>"
```

This produces `raw_text.txt` with pages separated by form feed (`\x0c`).

### Step 2 — Detect document structure

Read the first ~100 lines of `raw_text.txt` to identify:
- The **repeating page header** (a line appearing identically on every page)
- The **heading patterns** (all-caps lines, numbered sections like `1 - TITLE` or `1.1. Title`)

### Step 3 — Write and run the cleaning script

Copy `scripts/convert_pdf_to_md.py` to the working directory. Edit it to set:
- `header_pattern` — the repeating header regex found in Step 2
- `h1_patterns` — adjusted for the document's actual heading style

Then run:
```bash
python3 convert_pdf_to_md.py
```

This produces `source.md`.

### Step 4 — Verify

Read `source.md` and check headings, paragraphs, and TOC are clean. Adjust patterns and re-run if needed.

---

## Phase 2: Translation

### Step 5 — Establish a glossary

Read `source.md` and identify proper nouns, acronyms, and recurring terms. State the glossary before translating.

### Step 6 — Translate in parts (~200–300 lines at a time)

Translate each section to **`TARGET_LANGUAGE`**, preserving all Markdown formatting (`#`/`##`, `**bold**`, lists, tables). Save as `part1.md`, `part2.md`, etc.

### Step 7 — Combine

```bash
cat part*.md > OUTPUT_MD
rm part*.md
```

---

## Phase 3: Prepare for PDF

### Step 8 — Add cover page

Insert at the top of `OUTPUT_MD` (fill in real title, author, date from the document):

```html
<div style="text-align: center; margin-top: 100px;">
    <h1 style="border-bottom: none; font-size: 3em;">DOCUMENT TITLE</h1>
    <br><br>
    <h2 style="border-bottom: none;">Subtitle / Organization</h2>
    <br><br><br><br>
    <p style="font-size: 1.2em;">Presented by <strong>Author Name</strong></p>
    <br>
    <p>Date</p>
</div>

<div class="page-break"></div>
```

### Step 9 — Format the Table of Contents

Replace the inline TOC with structured HTML:

```html
<div class="toc">
    <div class="toc-entry toc-main"><span class="toc-title">SECTION TITLE</span><span class="toc-page">PAGE</span></div>
    <div class="toc-entry toc-sub"><span class="toc-title">Subsection title</span><span class="toc-page">PAGE</span></div>
</div>
```

Use `toc-main` for top-level sections and `toc-sub` for subsections. Page numbers from the original PDF.

### Step 10 — Add page breaks

Insert `<div class="page-break"></div>` after the TOC and between major sections.

### Step 11 — Write the stylesheet

Copy `resources/style.css` to the working directory.

---

## Phase 4: Generate PDF

### Step 12 — Generate

```bash
npx -y md-to-pdf OUTPUT_MD --stylesheet style.css --pdf-options '{"format": "A4", "margin": {"top": "2cm", "bottom": "2cm", "left": "2cm", "right": "2cm"}, "printBackground": true}'
```

### Step 13 — Verify

Open the PDF and check: cover page, TOC dot leaders, headings, tables, page breaks.

### Step 14 — Clean up

```bash
rm -f raw_text.txt convert_pdf_to_md.py style.css
```

Keep `source.md` and `OUTPUT_MD`.

---

## Notes

- **Token limits**: Translate in sections of ~200–300 lines to avoid hitting generation limits.
- **Terminology**: Always apply the glossary consistently throughout the translation.
- **Font loading**: The CSS imports Google Fonts — internet connection required during PDF generation.
- **Header detection tip**: If the header isn't obvious, find the most repeated lines with `sort | uniq -c | sort -rn` on the raw text.
