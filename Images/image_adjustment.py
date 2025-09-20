import cv2
import numpy as np

# Load the image
image = cv2.imread('image.jpg')

# Convert the image to YCrCb color space
ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

# Split the YCrCb image into its components
y, cr, cb = cv2.split(ycrcb_image)

# Apply contrast adjustment to the Y component
alpha = 1.5  # Contrast control (1.0-3.0)
beta = 0  # Brightness control (0-100)
y_contrasted = cv2.convertScaleAbs(y, alpha=alpha, beta=beta)

# Merge the contrast-adjusted Y component with the Cr and Cb components
contrasted_ycrcb_image = cv2.merge([y_contrasted, cr, cb])

# Convert the contrast-adjusted YCrCb image back to BGR color space
contrasted_image = cv2.cvtColor(contrasted_ycrcb_image, cv2.COLOR_YCrCb2BGR)

# Display the original and contrast-adjusted images
cv2.imshow('Original Image', image)
cv2.imshow('Contrasted Image', contrasted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the contrast-adjusted image
cv2.imwrite('contrasted_image.jpg', contrasted_image)