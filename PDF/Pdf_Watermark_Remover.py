import os
from PIL import Image
from pdf2image import convert_from_path
from fpdf import FPDF
import numpy as np
from skimage import io

def is_watermark_pixel(pixel):
    r, g, b = pixel
    return 120 < r < 254 and 120 < g < 254 and 120 < b < 254

def remove_watermark(image_path):
    img = Image.open(image_path)
    img_array = np.array(img)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            if is_watermark_pixel(img_array[i, j]):
                img_array[i, j] = [255, 255, 255]
    return Image.fromarray(img_array)

def process_pdf(pdf_file):
    output_dir = os.path.dirname(pdf_file)
    output_file = os.path.basename(pdf_file)
    output_file = os.path.splitext(output_file)[0]
    img_dir = os.path.join(output_dir, 'images')
    os.makedirs(img_dir, exist_ok=True)

    images = convert_from_path(pdf_file)
    for i, img in enumerate(images):
        img_path = os.path.join(img_dir, f'page_{i+1}.jpg')
        img = remove_watermark(np.array(img))
        img.save(img_path)

    pdf = FPDF()
    w, h = 0, 0
    for i in range(1, len(images) + 1):
        img_path = os.path.join(img_dir, f'page_{i}.jpg')
        if os.path.exists(img_path):
            if i == 1:
                cover = Image.open(img_path)
                w, h = cover.size
                pdf = FPDF(unit="pt", format=[w, h])
            pdf.add_page()
            pdf.image(img_path, 0, 0, w, h)
    pdf.output(os.path.join(output_dir, f'{output_file}_processed.pdf'), "F")

pdf_file = input('Enter the PDF file location: ')
process_pdf(pdf_file)
print("Done!")