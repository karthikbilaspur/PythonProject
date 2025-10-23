import PyPDF2

def encrypt_pdf():
    # Get PDF file name
    pdf_file_name = input("Enter the EXACT name of the PDF file in this FOLDER: ")
    pdf_file = pdf_file_name + ".pdf"

    try:
        # Read the PDF file
        pdf = PyPDF2.PdfFileReader(pdf_file)

        # Create a PDF writer object
        writer = PyPDF2.PdfFileWriter()

        # Add all pages to the writer
        for page_num in range(pdf.numPages):
            writer.addPage(pdf.getPage(page_num))

        # Get passwords
        owner_password = input("Enter password for OWNER: ")
        user_password = input("Enter password for USER: ")

        # Encrypt the PDF
        writer.encrypt(user_pwd=user_password, owner_pwd=owner_password, use_128bit=True)

        # Get new PDF file name
        new_pdf_name = input("Enter new ENCRYPTED PDF name: ") + '.pdf'

        # Write the encrypted PDF to a new file
        with open(new_pdf_name, 'wb') as encrypted_pdf:
            writer.write(encrypted_pdf)

        print(f"Encrypted PDF saved as {new_pdf_name}")

    except FileNotFoundError:
        print("The PDF file was not found. Please ensure it's in the same directory as this script.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    encrypt_pdf()