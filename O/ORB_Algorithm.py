import cv2
import numpy as np
import os

# Load the images
path = input('Enter the path of the image: ')
image = cv2.imread(path)
if image is None:
    print("Error loading image")
    exit()

path2 = input('Enter the path for testing image: ')
test_image = cv2.imread(path2)
if test_image is None:
    print("Error loading test image")
    exit()

# Resizing the images
image = cv2.resize(image, (600, 600))
test_image = cv2.resize(test_image, (600, 600))

# Convert the images to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
test_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

# Display the given and test image
image_stack = np.concatenate((image, test_image), axis=1)
cv2.imshow('image VS test_image', image_stack)

# Implementing the ORB algorithm
orb = cv2.ORB_create()

train_keypoints, train_descriptor = orb.detectAndCompute(gray, None)
test_keypoints, test_descriptor = orb.detectAndCompute(test_gray, None)

keypoints = np.copy(image)
cv2.drawKeypoints(image, train_keypoints, keypoints, color=(0, 255, 0))

# Display image with keypoints
cv2.imshow('keypoints', keypoints)
print("Number of Keypoints Detected In The Image: ", len(train_keypoints))

# Create a Brute Force Matcher object.
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Perform the matching between the ORB descriptors of the training image and the test image
matches = bf.match(train_descriptor, test_descriptor)

# The matches with shorter distance are the ones we want.
matches = sorted(matches, key=lambda x: x.distance)

result = cv2.drawMatches(image, train_keypoints, test_image,
                         test_keypoints, matches[:100], None, flags=2)

# Display the best matching points
cv2.imshow('result', result)

# Save the result
image_name = os.path.basename(path)
image_path = os.path.splitext(image_name)[0]
output_dir = "./ORB Algorithm"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output = os.path.join(output_dir, f"{image_path}(featureMatched).jpg")
cv2.imwrite(output, result)

print("\nNumber of Matching Keypoints Between The input image and Test Image: ", len(matches))
cv2.waitKey(0)
cv2.destroyAllWindows()