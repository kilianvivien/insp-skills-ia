"""
Generic PDF-to-Markdown cleaning script.
Before running, edit the two TODO sections below to match your document.
"""
import re

def clean_text(text):
    pages = text.split('\x0c')
    cleaned_content = []

    # TODO: replace with the actual repeating header text found in your PDF
    # e.g. r'My Organization Name' or r'ANNUAL REPORT \d{4}'
    header_pattern = re.compile(r'REPLACE_WITH_HEADER_PATTERN')

    for page in pages:
        if not page.strip():
            continue

        lines = page.split('\n')
        # Remove repeating page header
        lines = [line for line in lines if not header_pattern.search(line)]

        # Remove standalone page numbers near the bottom of each page
        for i in range(len(lines) - 1, max(-1, len(lines) - 10), -1):
            if re.match(r'^\s*\d+\s*$', lines[i]):
                lines[i] = ""
                break

        page_text = "\n".join(lines)
        cleaned_content.append(page_text)

    full_text = "\n".join(cleaned_content)

    # Fix hyphenation across line breaks (e.g. "some-\nword" → "someword")
    full_text = re.sub(r'(\w)\-\n\s*(\w)', r'\1\2', full_text)

    # --- Heading detection ---
    # TODO: adjust patterns to match your document's heading style

    def format_h1(match):
        return "\n# " + match.group(0).strip() + "\n"

    # H1: all-caps lines, standalone known section names, "1 - TITLE" style
    h1_patterns = [
        r'^\s*TABLE OF CONTENTS\s*$',
        r'^\s*INTRODUCTION\s*$',
        r'^\s*CONCLUSION\s*$',
        r'^\s*APPENDIX\s*$',
        r'^\s*\d+\s*[-–]\s*[A-Z\s]+\s*$',   # "1 - SECTION TITLE"
        r'^\s*EK-\d+\s*$',                    # "EK-1" style appendix
    ]
    for pattern in h1_patterns:
        full_text = re.compile(pattern, re.MULTILINE).sub(format_h1, full_text)

    def format_h2(match):
        return "\n## " + match.group(0).strip() + "\n"

    # H2: "1.1. Title" or "1.1 Title"
    h2_pattern = r'^\s*\d+\.\d+\.?\s+\S[^\n]+$'
    full_text = re.compile(h2_pattern, re.MULTILINE).sub(format_h2, full_text)

    # Join paragraph lines split across line breaks
    lines = full_text.split('\n')
    processed_lines = []
    for i in range(len(lines)):
        line = lines[i].strip()
        if not line:
            processed_lines.append("")
            continue
        if line.startswith('#'):
            processed_lines.append(line)
            continue
        if re.match(r'^\d+\s*\.\s+', line):
            processed_lines.append("- " + line)
            continue
        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if (line and line[-1] not in '.!?:'
                    and next_line
                    and not next_line.startswith('#')
                    and not re.match(r'^\d+\s*\.\s+', next_line)):
                lines[i + 1] = line + " " + next_line
                continue
        processed_lines.append(line)

    final_text = "\n".join(processed_lines)
    # Clean up TOC dots
    final_text = re.sub(r'\.\s?\.\s?\.\.+', '...', final_text)
    # Collapse excessive blank lines
    final_text = re.sub(r'\n{3,}', '\n\n', final_text)
    return final_text


if __name__ == "__main__":
    with open('raw_text.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    md = clean_text(content)
    output_file = 'source.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Conversion complete: {output_file}")
