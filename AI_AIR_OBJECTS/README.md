This project uses OpenCV and Caffe to detect airplanes in images and videos. It extracts patches around feature points (corners) and classifies them using a pre-trained Caffe model.
Features
Airplane detection in images and videos
Patch extraction around feature points (corners)
Classification using a pre-trained Caffe model
Visualization of detected airplanes
Requirements
OpenCV 3.x or later
Caffe
Python 3.x or later
NumPy
Installation
Clone the repository: git clone https://github.com/your-username/object-detection.git
Install the required libraries: pip install opencv-python caffe numpy
Download the pre-trained Caffe model and place it in the models directory
Usage
Run the script: python detect_airplanes.py
The script will load a sample image and detect airplanes
The detected airplanes will be visualized on the image