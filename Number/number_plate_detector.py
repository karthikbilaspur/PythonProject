import cv2
import numpy as np
import pytesseract

# Load the image
def load_image(image_path):
    image = cv2.imread(image_path)
    return image

# Convert image to grayscale
def convert_to_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

# Apply threshold to segment out the license plate
def apply_threshold(gray):
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

# Find contours of the license plate
def find_contours(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# Draw rectangle around the license plate
def draw_rectangle(image, contours):
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w)/h
        if area > 1000 and aspect_ratio > 2 and aspect_ratio < 6:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            return x, y, w, h
    return None

# Extract the license plate region
def extract_license_plate(image, x, y, w, h):
    license_plate = image[y:y+h, x:x+w]
    return license_plate

# Recognize the text on the license plate
def recognize_text(license_plate):
    text = pytesseract.image_to_string(license_plate, lang='eng', config='--psm 11')
    return text.strip()

# Main function
def detect_number_plate(image_path):
    image = load_image(image_path)
    gray = convert_to_grayscale(image)
    thresh = apply_threshold(gray)
    contours = find_contours(thresh)
    license_plate_coords = draw_rectangle(image, contours)
    if license_plate_coords:
        x, y, w, h = license_plate_coords
        license_plate = extract_license_plate(image, x, y, w, h)
        text = recognize_text(license_plate)
        cv2.imshow('License Plate', license_plate)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return text
    else:
        return "License plate not detected"

# Test the function
image_path = 'image.jpg'
print(detect_number_plate(image_path))