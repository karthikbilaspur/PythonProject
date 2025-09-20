from PIL import Image

def image_to_ascii(image_path, width=80):
    img = Image.open(image_path)
    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width)
    img = img.resize((width, height))
    img = img.convert('L')

    ascii_chars = '@%#*+=-:. '

    ascii_str = ''
    for y in range(img.height):
        for x in range(img.width):
            pixel_value = img.getpixel((x, y))
            ascii_str += ascii_chars[int((len(ascii_chars) - 1) * (1 - pixel_value / 255))]
        ascii_str += '\n'

    return ascii_str

def main():
    image_path = input("Enter the path to the image file: ")
    width = int(input("Enter the width of the ASCII art (default=80): ") or 80)
    ascii_art = image_to_ascii(image_path, width)
    print(ascii_art)

    save = input("Do you want to save the ASCII art to a file? (yes/no): ")
    if save.lower() == 'yes':
        with open('ascii_art.txt', 'w') as f:
            f.write(ascii_art)
        print("ASCII art saved to ascii_art.txt")

if __name__ == "__main__":
    main()