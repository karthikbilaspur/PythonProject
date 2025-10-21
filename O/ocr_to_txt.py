from PIL import Image
import pytesseract

def ocr_to_text(image_path):
    try:
         # Specify the path to the Tesseract-OCR executable (if not in PATH)
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Open the image using Pillow
        img = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(img)
        
        return text
    
    except Exception as e:
        return str(e)

