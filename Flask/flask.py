from flask import Flask, request, jsonify
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import urllib.request

app = Flask(__name__)

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def compare_images(img1, img2):
    # Convert images to grayscale
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM
    score = ssim(gray_img1, gray_img2, full=True)[0]
    return score * 100

def detect_faces(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
    return faces

@app.route('/compare', methods=['POST'])
def compare():
    # Get images from request
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Read images
    img1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)

    # Resize images
    img1 = cv2.resize(img1, (256, 256))
    img2 = cv2.resize(img2, (256, 256))

    # Compare images
    similarity = compare_images(img1, img2)

    return jsonify({'similarity': similarity})

@app.route('/face_compare', methods=['POST'])
def face_compare():
    # Get images from request
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Read images
    img1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)

    # Detect faces
    faces1 = detect_faces(img1)
    faces2 = detect_faces(img2)

    if len(faces1) > 0 and len(faces2) > 0:
        # Extract face regions
        x1, y1, w1, h1 = faces1[0]
        x2, y2, w2, h2 = faces2[0]
        face1 = img1[y1:y1+h1, x1:x1+w1]
        face2 = img2[y2:y2+h2, x2:x2+w2]

        # Resize face regions
        face1 = cv2.resize(face1, (face2.shape[1], face2.shape[0]))

        # Compare face regions
        similarity = compare_images(face1, face2)

        return jsonify({'similarity': similarity})
    else:
        return jsonify({'error': 'No faces detected'})

@app.route('/face_compare_url', methods=['POST'])
def face_compare_url():
    # Get image URLs from request
    url1 = request.json['url1']
    url2 = request.json['url2']

    # Read images from URLs
    req1 = urllib.request.urlopen(url1)
    arr1 = np.asarray(bytearray(req1.read()), dtype=np.uint8)
    img1 = cv2.imdecode(arr1, cv2.IMREAD_COLOR)

    req2 = urllib.request.urlopen(url2)
    arr2 = np.asarray(bytearray(req2.read()), dtype=np.uint8)
    img2 = cv2.imdecode(arr2, cv2.IMREAD_COLOR)

    # Detect faces
    faces1 = detect_faces(img1)
    faces2 = detect_faces(img2)

    if len(faces1) > 0 and len(faces2) > 0:
        # Extract face regions
        x1, y1, w1, h1 = faces1[0]
        x2, y2, w2, h2 = faces2[0]
        face1 = img1[y1:y1+h1, x1:x1+w1]
        face2 = img2[y2:y2+h2, x2:x2+w2]

        # Resize face regions
        face1 = cv2.resize(face1, (face2.shape[1], face2.shape[0]))

        # Compare face regions
        similarity = compare_images(face1, face2)

        return jsonify({'similarity': similarity})
    else:
        return jsonify({'error': 'No faces detected' similarity': 'No faces detected'})

if __name__ == '__main__':
    app.run(debug=True)
    