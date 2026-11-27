from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path: str, text: str, output_path: str, font_path: str = "arial.ttf", font_size: int = 24, color: tuple[int, int, int] = (0, 0, 0), position: tuple[int, int] = (10, 10)):
    """
    Adds text to an image.

    Args:
        image_path (str): Path to the input image.
        text (str): Text to add to the image.
        output_path (str): Path to save the output image.
        font_path (str, optional): Path to the font file. Defaults to 'arial.ttf'.
        font_size (int, optional): Font size. Defaults to 24.
        color (tuple, optional): Text color (R, G, B). Defaults to (0, 0, 0).
        position (tuple, optional): Text position (x, y). Defaults to (10, 10).
    """
    img = Image.open(image_path).convert("RGB")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except (OSError, IOError):
        print(f"Font '{font_path}' not found, using default font.")
        font = ImageFont.load_default()
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=color)
    img.save(output_path)
    print(f"Saved to {output_path}")
    return output_path

if __name__ == "__main__":
    # Demo - change these paths to your own image
    # add_text_to_image("input.jpg", "Hello World!", "output.jpg", font_size=40, color=(255, 0, 0))
    print("Import this file and call:")
    print('  add_text_to_image("input.jpg", "Hello!", "output.jpg")')
