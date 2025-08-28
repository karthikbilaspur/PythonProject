import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fpdf import FPDF
from PIL import Image

def download_article(url, output_dir, filename):
    # Set up Chrome options
    options = Options()
    options.headless = True

    # Set up Chrome driver
    driver = webdriver.Chrome(options=options)

    # Navigate to the article page
    driver.get(url)

    # Get the article title
    title = driver.title

    # Get the article content
    article_content = driver.find_element_by_tag_name("article")

    # Take a screenshot of the article content
    screenshot_path = os.path.join(output_dir, "article_screenshot.png")
    article_content.screenshot(screenshot_path)

    # Close the browser
    driver.quit()

    # Optimize the image
    optimize_image(screenshot_path)

    # Convert the screenshot to PDF
    convert_to_pdf(screenshot_path, os.path.join(output_dir, filename), title)

def optimize_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Optimize the image
    image.save(image_path, optimize=True, quality=90)

def convert_to_pdf(image_path, pdf_path, title):
    # Create a PDF object
    pdf = FPDF()

    # Add a page to the PDF
    pdf.add_page()

    # Set the title of the PDF
    pdf.set_title(title)

    # Set the author of the PDF
    pdf.set_author("GeeksforGeeks")

    # Set the subject of the PDF
    pdf.set_subject("Article")

    # Add the image to the PDF
    pdf.image(image_path, x=0, y=0, w=210, h=297)

    # Save the PDF
    pdf.output(pdf_path, "F")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_dir = input("Enter the output directory: ")
        filename = input("Enter the filename: ")
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        download_article(url, output_dir, filename)
    else:
        print("Please provide the URL of the article")