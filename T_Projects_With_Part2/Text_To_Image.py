from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path:str, text:str, output_path:str, font_path:str='arial.ttf', font_size:int=24, color:tuple=(0, 0, 0), position:tuple=(10, 10)):
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
    # Load the image
    img = Image.open(image_path)

    # Set the font
    font = ImageFont.truetype(font_path, font_size)

    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Draw the text
    draw.text(position, text, font=font, fill=color)

    # Save the image
    img.save(output_path)