from pdfrw import PdfWriter, PdfReader
import os

def delete_pages(path, del_pages):
    """
    Deletes specified pages from a PDF file.

    Args:
        path (str): Path to the PDF file.
        del_pages (list): List of page numbers to delete.

    Returns:
        None
    """
    pdf_obj = PdfReader(path)
    total_pages = len(pdf_obj.pages)
    print(f"Total Pages in PDF: {total_pages}")

    writer = PdfWriter()
    page_list = [page for page in range(1, total_pages + 1) if page not in del_pages]

    for page in page_list:
        writer.addpage(pdf_obj.pages[page - 1])

    os.remove(path)
    writer.write(path)

def get_pages_to_delete():
    while True:
        try:
            del_pages = input("Enter page numbers to delete (comma-separated): ")
            del_pages = [int(i) for i in del_pages.strip().split(",")]
            return del_pages
        except ValueError:
            print("Invalid input. Please enter page numbers separated_path = os.path.sep.join(path.split(os.path.sep)[:-1])
            output_path = os.path.join(separated_path, f"modified_{os.path.basename(path)}")
            return del_pages, output_path

def main():
    path = input("Enter the path (full or relative) of the PDF file: ")
    del_pages, output_path = get_pages_to_delete()
    delete_pages(path, output_path, del_pages)
    print(f"\nPages {del_pages} have been deleted successfully!!!")

def delete_pages(path, output_path, del_pages):
    pdf_obj = PdfReader(path)
    total_pages = len(pdf_obj.pages)
    print(f"Total Pages in PDF: {total_pages}")

    writer = PdfWriter()
    page_list = [page for page in range(1, total_pages + 1) if page not in del_pages]

    for page in page_list:
        writer.addpage(pdf_obj.pages[page - 1])

    writer.write(output_path)

if __name__ == "__main__":
    main()
    