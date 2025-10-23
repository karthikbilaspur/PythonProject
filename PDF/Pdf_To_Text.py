from PyPDF2 import PdfReader
import pdfplumber

def pdf_to_text_pyPDF2(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text
    except Exception as e:
        print(f"Error using PyPDF2: {e}")
        return None

def pdf_to_text_pdfplumber(pdf_file):
    try:
        text = ''
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error using pdfplumber: {e}")
        return None

def main():
    pdf_file = input("Enter the path to the PDF file: ")
    text_pyPDF2 = pdf_to_text_pyPDF2(pdf_file)
    text_pdfplumber = pdf_to_text_pdfplumber(pdf_file)

    if text_pyPDF2 and text_pdfplumber:
        print("Both methods were successful. Here's the extracted text:")
        print("PyPDF2:")
        print(text_pyPDF2)
        print("\npdfplumber:")
        print(text_pdfplumber)
        with open('output_pyPDF2.txt', 'w') as f:
            f.write(text_pyPDF2)
        with open('output_pdfplumber.txt', 'w') as f:
            f.write(text_pdfplumber)
        print("Text saved to output_pyPDF2.txt and output_pdfplumber.txt")
    elif text_pyPDF2:
        print("PyPDF2 was successful. Here's the extracted text:")
        print(text_pyPDF2)
        with open('output.txt', 'w') as f:
            f.write(text_pyPDF2)
        print("Text saved to output.txt")
    elif text_pdfplumber:
        print("pdfplumber was successful. Here's the extracted text:")
        print(text_pdfplumber)
        with open('output.txt', 'w') as f:
            f.write(text_pdfplumber)
        print("Text saved to output.txt")
    else:
        print("Both methods failed. Please try a different PDF file.")

if __name__ == "__main__":
    main()