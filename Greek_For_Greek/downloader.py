import sys
import os
from selenium import webdriver
from PIL import Image
from fpdf import FPDF

def get_html(url):
    path = "article_image.png"
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome("chromedriver_win32/chromedriver.exe", options=options)
    driver.get(url)
    try:
        required_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size(1366, required_height)
        article_element = driver.find_element_by_tag_name("article")
        article_element.screenshot(path)
        convert_image_to_pdf(path)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

def convert_image_to_pdf(path):
    try:
        cover = Image.open(path)
        cover.save(path, optimize=True, quality=90)  # Optimize image
        width, height = cover.size
        margin = 20
        pdf = FPDF(unit="pt", format=[width + 2 * margin, height + 2 * margin])
        pdf.add_page()
        pdf.set_title("GeeksforGeeks Article")
        pdf.set_author("GeeksforGeeks")
        pdf.set_subject("Article")
        pdf.image(path, margin, margin)
        output_dir = input("Enter output directory (default=current directory): ")
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            output_dir = "."
        pdf_filename = input("Enter filename (default=article.pdf): ")
        if not pdf_filename:
            pdf_filename = "article.pdf"
        if not pdf_filename.endswith(".pdf"):
            pdf_filename += ".pdf"
        pdf.output(os.path.join(output_dir, pdf_filename), "F")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = " ".join(sys.argv[1:])
    else:
        url = input("Enter URL: ")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    get_html(url)
    try:
        os.remove("article_image.png")
    except FileNotFoundError:
        pass