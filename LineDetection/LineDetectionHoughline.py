import cv2
import numpy as np
from tkinter import filedialog
import tkinter as tk

# Function to apply Hough Transform
def apply_hough_transform(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 500)
    
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    
    cv2.imwrite('houghlines.jpg', img)
    cv2.imshow("Hough Lines", img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

# Function to apply Probabilistic Hough Transform
def apply_probabilistic_hough_transform(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    
    cv2.imwrite('probabilistic_houghlines.jpg', img)
    cv2.imshow("Probabilistic Hough Lines", img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

# Function to select image and apply transform
def select_image_and_apply_transform(transform_type):
    image_path = filedialog.askopenfilename()
    if transform_type == "hough":
        apply_hough_transform(image_path)
    elif transform_type == "probabilistic_hough":
        apply_probabilistic_hough_transform(image_path)

# Create main window
window = tk.Tk()
window.title("Line Detection using Hough Transform")
window.geometry('380x150')

# Create label and buttons
label = tk.Label(window, text="Choose a transform type:")
label.grid(row=0, column=0, columnspan=2)

hough_button = tk.Button(window, text="Hough Transform", command=lambda: select_image_and_apply_transform("hough"))
hough_button.grid(row=1, column=0)

probabilistic_hough_button = tk.Button(window, text="Probabilistic Hough Transform", command=lambda: select_image_and_apply_transform("probabilistic_hough"))
probabilistic_hough_button.grid(row=2, column=0)

output_label = tk.Label(window, text="Output images will be saved in the working directory.")
output_label.grid(row=3, column=0, columnspan=2)

window.mainloop()