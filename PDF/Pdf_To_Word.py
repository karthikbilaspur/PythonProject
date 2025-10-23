import pdfplumber
from docx import Document

def pdf_to_word(pdf_file, word_file):
    text = ''
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    document = Document()
    document.add_paragraph(text)
    document.save(word_file)

def main():
    pdf_file = input("Enter the path to the PDF file: ")
    word_file = pdf_file.replace('.pdf', '.docx')
    pdf_to_word(pdf_file, word_file)
    print(f"PDF converted to Word successfully. Output file: {word_file}")

if __name__ == "__main__":
    main()