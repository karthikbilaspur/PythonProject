from PyPDF2 import PdfReader, PdfWriter
import os

def merge_pdfs():
    pdf_files = input("Enter the paths to the PDF files to merge (separated by commas): ")
    pdf_files = [file.strip() for file in pdf_files.split(',')]
    output_file = input("Enter the output file name: ")

    pdf_writer = PdfWriter()
    for file in pdf_files:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"PDFs merged successfully. Output file: {output_file}")

def split_pdf():
    pdf_file = input("Enter the path to the PDF file to split: ")
    output_prefix = input("Enter the output file prefix: ")

    pdf_reader = PdfReader(pdf_file)
    for page in range(len(pdf_reader.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page])
        with open(f"{output_prefix}_{page+1}.pdf", 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

    print(f"PDF split successfully. Output files: {output_prefix}_*.pdf")

def add_watermark():
    pdf_file = input("Enter the path to the PDF file: ")
    watermark_file = input("Enter the path to the watermark PDF file: ")
    output_file = input("Enter the output file name: ")

    pdf_reader = PdfReader(pdf_file)
    watermark_reader = PdfReader(watermark_file)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        page.merge_page(watermark_reader.pages[0])
        pdf_writer.add_page(page)

    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"Watermark added successfully. Output file: {output_file}")

def rotate_pdf():
    pdf_file = input("Enter the path to the PDF file: ")
    rotation = input("Enter the rotation (clockwise/counterclockwise): ")
    output_file = input("Enter the output file name: ")

    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        if rotation.lower() == 'clockwise':
            page.rotate(90)
        elif rotation.lower() == 'counterclockwise':
            page.rotate(-90)
        pdf_writer.add_page(page)

    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"PDF rotated successfully. Output file: {output_file}")

def encrypt_pdf():
    pdf_file = input("Enter the path to the PDF file: ")
    password = input("Enter the password: ")
    output_file = input("Enter the output file name: ")

    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.encrypt(password)

    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"PDF encrypted successfully. Output file: {output_file}")

def reorder_pdf():
    pdf_file = input("Enter the path to the PDF file: ")
    page_order = input("Enter the page order (separated by commas): ")
    page_order = [int(page) - 1 for page in page_order.split(',')]
    output_file = input("Enter the output file name: ")

    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()

    for page in page_order:
        pdf_writer.add_page(pdf_reader.pages[page])

    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"PDF pages reordered successfully. Output file: {output_file}")

def main():
    while True:
        print("PDF Utilities")
        print("1. Merge PDFs")
        print("2. Split PDF")
        print("3. Add Watermark")
        print("4. Rotate PDF")
        print("5. Encrypt PDF")
        print("6. Reorder PDF Pages")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            merge_pdfs()
        elif choice == '2':
            split_pdf()
        elif choice == '3':
            add_watermark()
        elif choice == '4':
            rotate_pdf()
        elif choice == '5':
            encrypt_pdf()
        elif choice == '6':
            reorder_pdf()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()