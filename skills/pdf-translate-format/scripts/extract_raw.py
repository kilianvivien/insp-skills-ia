import pdfplumber
import sys

input_pdf = sys.argv[1] if len(sys.argv) > 1 else "INPUT.pdf"

with pdfplumber.open(input_pdf) as pdf:
    text = ""
    for page in pdf.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\x0c"

with open("raw_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Extracted {len(text)} characters to raw_text.txt")
