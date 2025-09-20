import cv2
import numpy as np

def detect_color_rgb(image_path, color):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if color == 'red':
        lower_bound = np.array([0, 100, 100])
        upper_bound = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_bound, upper_bound)

        lower_bound = np.array([160, 100, 100])
        upper_bound = np.array([179, 255, 255])
        mask2 = cv2.inRange(hsv, lower_bound, upper_bound)

        mask = cv2.bitwise_or(mask1, mask2)

    elif color == 'green':
        lower_bound = np.array([40, 40, 40])
        upper_bound = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

    elif color == 'blue':
        lower_bound = np.array([100, 50, 50])
        upper_bound = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

    result = cv2.bitwise_and(image, image, mask=mask)
    return result

def detect_color_hsl(image_path, color):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if color == 'red':
        lower_bound = np.array([0, 50, 50])
        upper_bound = np.array([10, 100, 100])
        mask1 = cv2.inRange(hsv, lower_bound, upper_bound)

        lower_bound = np.array([160, 50, 50])
        upper_bound = np.array([179, 100, 100])
        mask2 = cv2.inRange(hsv, lower_bound, upper_bound)

        mask = cv2.bitwise_or(mask1, mask2)

    elif color == 'green':
        lower_bound = np.array([40, 40, 40])
        upper_bound = np.array([80, 100, 100])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

    elif color == 'blue':
        lower_bound = np.array([100, 50, 50])
        upper_bound = np.array([130, 100, 100])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

    result = cv2.bitwise_and(image, image, mask=mask)
    return result

def detect_color_rgba(image_path, color):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image.shape[2] == 4:
        b, g, r, a = cv2.split(image)

        if color == 'red':
            mask = cv2.inRange(r, 200, 255)
        elif color == 'green':
            mask = cv2.inRange(g, 200, 255)
        elif color == 'blue':
            mask = cv2.inRange(b, 200, 255)

        result = cv2.bitwise_and(image, image, mask=mask)
        return result
    else:
        return None

def main():
    image_path = input("Enter the image path: ")
    color_model = input("Enter the color model (rgb/hsl/rgba): ")
    color = input("Enter the color (red/green/blue): ")

    if color_model == 'rgb':
        result = detect_color_rgb(image_path, color)
    elif color_model == 'hsl':
        result = detect_color_hsl(image_path, color)
    elif color_model == 'rgba':
        result = detect_color_rgba(image_path, color)
    else:
        print("Invalid color model.")
        return

    if result is not None:
        cv2.imshow('Result', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No alpha channel found in the image.")

if __name__ == "__main__":
    main()