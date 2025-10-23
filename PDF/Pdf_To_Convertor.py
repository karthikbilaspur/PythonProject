import tabula
import os

def pdf_to_csv(pdf_file, csv_file):
    try:
        tabula.convert_into(pdf_file, csv_file, output_format="csv", pages='all')
        print(f"CSV file saved as {csv_file}")
        return True
    except Exception as e:
        print(f"Error converting PDF to CSV: {e}")
        return False

def validate_pdf_file(pdf_file):
    if not os.path.exists(pdf_file):
        print("File not found. Please try again.")
        return False
    if not pdf_file.endswith('.pdf'):
        print("Invalid file format. Please select a PDF file.")
        return False
    return True

def get_csv_file_name(pdf_file):
    return os.path.splitext(pdf_file)[0] + '.csv'

def main():
    while True:
        pdf_file = input("Enter the path to the PDF file (or 'q' to quit): ")
        if pdf_file.lower() == 'q':
            break
        if not validate_pdf_file(pdf_file):
            continue
        csv_file = get_csv_file_name(pdf_file)
        if pdf_to_csv(pdf_file, csv_file):
            print("PDF to CSV conversion successful!")
        else:
            print("PDF to CSV conversion failed.")

if __name__ == "__main__":
    main()