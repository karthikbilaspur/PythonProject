import cv2
import numpy as np

# Load the image
image = cv2.imread('image.jpg')

# Display the original image
cv2.imshow('Original Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply blur to the image
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
cv2.imshow('Blurred Image', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply edge detection to the image
edges = cv2.Canny(image, 100, 200)
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the processed images
cv2.imwrite('grayscale_image.jpg', gray_image)
cv2.imwrite('blurred_image.jpg', blurred_image)
cv2.imwrite('edges.jpg', edges)