import pdfplumber
import sys

def convert_pdf_to_text(pdf_path, output_path):
    """Extracts all text from a PDF and saves it to a file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n\\pagebreak\n" # Add page breaks
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(all_text)
        print(f"Successfully extracted text from '{pdf_path}' to '{output_path}'")
    except Exception as e:
        print(f"Error converting PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    pdf_file = "q-pdf-to-markdown.pdf"
    md_file = "converted.md"
    convert_pdf_to_text(pdf_file, md_file) 