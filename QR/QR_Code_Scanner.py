import qrcode
from PIL import Image
import os

class QRCodeGenerator:
    def __init__(self):
        self.data = None
        self.filename = None

    def get_data(self):
        while True:
            self.data = input("Enter the data for the QR code: ")
            if self.data:
                break
            else:
                print("Please enter some data.")

    def get_filename(self):
        while True:
            self.filename = input("Enter the filename for the QR code (e.g., qr_code.png): ")
            if self.filename.endswith(".png"):
                break
            else:
                print("Please enter a filename with a .png extension.")

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
        qr.add_data(self.data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(self.filename)
        print(f"QR code saved as {self.filename}")

    def display_qr_code(self):
        if os.path.exists(self.filename):
            img = Image.open(self.filename)
            img.show()
        else:
            print("QR code file not found.")

    def run(self):
        self.get_data()
        self.get_filename()
        self.generate_qr_code()
        self.display_qr_code()

if __name__ == "__main__":
    qr_code_generator = QRCodeGenerator()
    qr_code_generator.run()