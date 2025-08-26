# Face Recognition API

A Flask API that provides three endpoints for:
Image comparison
Face comparison
Face comparison from URLs
Key Features:
Uses OpenCV for image processing and face detection
Uses scikit-image for calculating structural similarity index (SSIM)
Returns similarity percentage in JSON response
Endpoints:
/compare: Compares two images
/face_compare: Compares faces in two images
/face_compare_url: Compares faces in two images from URLs
