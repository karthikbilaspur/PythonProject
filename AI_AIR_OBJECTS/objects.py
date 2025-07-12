import cv2
import numpy as np

# Load the Caffe model
from InitCaffe import *

# Define constants
patch_size = 25
num_corners = 10
obj_freq = 5

# Load the video capture
# cap = cv2.VideoCapture('NASA_video1.mp4')

# Load a single frame for testing
frame = cv2.imread('frame184.png')

def detect_airplanes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, num_corners, 0.01, 100)
    corners = np.int0(corners)

    positions = []
    for corner in corners:
        x, y = corner.ravel()
        xstart, xend = max(0, x - patch_size), min(frame.shape[1], x + patch_size)
        ystart, yend = max(0, y - patch_size), min(frame.shape[0], y + patch_size)

        cv2.rectangle(frame, (xstart, ystart), (xend, yend), (255, 0, 0), 2)
        img_patch = frame[ystart:yend, xstart:xend]

        transformed_image = transformer.preprocess('data', img_patch)
        net.blobs['data'].data[0, :, :, :] = transformed_image

        output = net.forward()
        output_prob = output['prob'][0]
        top_inds = output_prob.argsort()[::-1][:10]

        airplane_labels = [895, 404, 405, 812]
        for k in range(10):
            if top_inds[k] in airplane_labels and output_prob[top_inds[k]] > 0.0:
                positions.append((x, y))
                break

    for pos in positions:
        xpos, ypos = pos
        cv2.rectangle(frame, (xpos-patch_size, ypos-patch_size), (xpos+patch_size, ypos+patch_size), (0, 255, 0), 2)

    return frame

# Detect airplanes in the frame
frame = detect_airplanes(frame)
cv2.imshow('frame', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()