Image to Text (OCR)
Run: python image_to_text.py
Install: pip install Pillow pytesseract
You ALSO need Tesseract installed on your computer:
 - Windows: https://github.com/UB-Mannheim/tesseract/wiki - tick 'Add to PATH' during install
 - Mac: brew install tesseract
 - Linux: sudo apt install tesseract-ocr
Fixed vs original:
 - Removed Windows-only '\\\\' path and input() prompt that froze the GUI
 - Auto-finds tesseract via PATH, shows a clear error if missing
 - Skips non-image files instead of crashing on .txt files
 - Creates destination folder if it doesn't exist
