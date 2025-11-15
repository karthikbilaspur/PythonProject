from PIL import Image

def hide_message(image_path: str, message: str, output_path: str):
    """
    Hide a message in an image using LSB substitution.
    """
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    # Convert the image to RGB
    img = img.convert('RGB')
    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Check if the image is large enough to hide the message
    if len(binary_message) > len(img.getdata()):
        raise ValueError("Need larger image size")
    # Hide the message
    hidden_img = img.copy()
    x, y = 0, 0
    for bit in binary_message:
        raw_pixel = img.getpixel((x, y))
        # Ensure we have a 3-tuple of ints (some modes can return int, floats or shorter tuples)
        if isinstance(raw_pixel, int):
            pixel = (int(raw_pixel), 0, 0)
        else:
            pixel = tuple(int(c) for c in raw_pixel)
            if len(pixel) < 3:
                pixel = pixel + (0,) * (3 - len(pixel))
        # Hide the bit in the least significant bit of the red channel
        if bit == '1':
            r = pixel[0] | 1
        else:
            r = pixel[0] & 0xFE  # clears LSB without producing negative numbers
        hidden_img.putpixel((x, y), (int(r), int(pixel[1]), int(pixel[2])))
        # Move to the next pixel
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1
    # Save the hidden image
    hidden_img.save(output_path)

def extract_message(image_path: str, message_length: int) -> str:
    """
    Extract a hidden message from an image.
    """
    # Open the image
    img = Image.open(image_path)
    # Convert the image to RGB
    img = img.convert('RGB')
    # Extract the message
    binary_message = ''
    x, y = 0, 0
    for _ in range(message_length * 8):
        pixel = img.getpixel((x, y))
        # Extract the least significant bit of the pixel
        bit = pixel[0] & 1
        binary_message += str(bit)
        # Move to the next pixel
        if x == img.size[0] - 1:
            x = 0
            y += 1
        else:
            x += 1
    # Convert the binary message to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    return message

# Example usage
image_path = 'input.png'
message = 'Hello, World!'
output_path = 'hidden.png'

hide_message(image_path, message, output_path)
extracted_message = extract_message(output_path, len(message))
print(extracted_message)