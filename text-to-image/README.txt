Add Text to Image
Run: python add_text_to_image.py  (shows usage)
Or import it:
  from add_text_to_image import add_text_to_image
  add_text_to_image("input.jpg", "Hello!", "output.jpg", font_size=40, color=(255, 0, 0))
Install: pip install Pillow
Fixed vs original:
 - Converts to RGB so RGBA / PNG images don't crash on save
 - Falls back to default font if arial.ttf is missing
 - Added a runnable demo / usage message
