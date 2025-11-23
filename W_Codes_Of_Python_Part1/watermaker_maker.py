import cv2
import numpy as np
from PIL import Image

def add_watermark(image_path: str, watermark_path: str, output_path: str, position: tuple[int, int], opacity: float=0.5):
    image = cv2.imread(image_path)
    watermark = cv2.imread(watermark_path)

    # Resize watermark if necessary
    h, w, _ = image.shape
    wh, ww, _ = watermark.shape
    if wh > h or ww > w:
        scale = min(h / wh, w / ww)
        watermark = cv2.resize(watermark, (int(ww * scale), int(wh * scale)))

    # Get dimensions of watermark
    wh, ww, _ = watermark.shape

    # Calculate position
    x, y = position
    if x + ww > w:
        x = w - ww
    if y + wh > h:
        y = h - wh

    # Add watermark
    roi = image[y:y+wh, x:x+ww]
    result = cv2.addWeighted(roi, 1, watermark, opacity, 0)
    image[y:y+wh, x:x+ww] = result

    # Save output
    cv2.imwrite(output_path, image)

def main():
    image_path = input("Enter the path to the image: ")
    watermark_path = input("Enter the path to the watermark: ")
    output_path = input("Enter the output path: ")
    position = (10, 10)  # Default position
    opacity = 0.5  # Default opacity

    add_watermark(image_path, watermark_path, output_path, position, opacity)
    print("Watermark added successfully!")

if __name__ == "__main__":
    main()