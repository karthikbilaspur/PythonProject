from PIL import Image
import tkinter as tk

class AsciiArtGenerator:
    def __init__(self, image_path, width=80):
        self.image_path = image_path
        self.width = width
        self.ascii_chars = '@%#*+=-:. '

    def generate_ascii_art(self):
        try:
            img = Image.open(self.image_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

        aspect_ratio = img.height / img.width
        height = int(aspect_ratio * self.width)
        img = img.resize((self.width, height))
        img = img.convert('L')

        ascii_str = ''
        for y in range(img.height):
            for x in range(img.width):
                pixel_value = img.getpixel((x, y))
                ascii_str += self.ascii_chars[int((len(self.ascii_chars) - 1) * (1 - pixel_value / 255))]
            ascii_str += '\n'

        return ascii_str

    def save_ascii_art(self, ascii_art, filename='ascii_art.txt'):
        try:
            with open(filename, 'w') as f:
                f.write(ascii_art)
            print(f"ASCII art saved to {filename}")
        except Exception as e:
            print(f"Error saving ASCII art: {e}")

    def display_ascii_art(self, ascii_art):
        root = tk.Tk()
        text_box = tk.Text(root, font=('Monaco', 10))
        text_box.pack(fill='both', expand=True)
        text_box.insert('1.0', ascii_art)
        text_box.config(state='disabled')
        root.geometry('800x600')
        root.title('ASCII Art')
        root.mainloop()

def main():
    image_path = input("Enter the path to the image file: ")
    width = int(input("Enter the width of the ASCII art (default=80): ") or 80)
    generator = AsciiArtGenerator(image_path, width)
    ascii_art = generator.generate_ascii_art()
    if ascii_art:
        print(ascii_art)
        save = input("Do you want to save the ASCII art to a file? (yes/no): ")
        if save.lower() == 'yes':
            filename = input("Enter the filename (default=ascii_art.txt): ") or 'ascii_art.txt'
            generator.save_ascii_art(ascii_art, filename)
        display = input("Do you want to display the ASCII art in a GUI window? (yes/no): ")
        if display.lower() == 'yes':
            generator.display_ascii_art(ascii_art)

if __name__ == "__main__":
    main()