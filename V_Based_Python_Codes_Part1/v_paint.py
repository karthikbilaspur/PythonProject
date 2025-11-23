import cv2
import numpy as np

# Define constants
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAPTURE_DEVICE = 0  # Default camera device

# Define color ranges in HSV
COLOR_RANGES = [
    [5, 107, 0, 19, 255, 255],  # orange
    [133, 56, 0, 159, 156, 255],  # purple
    [57, 76, 0, 100, 255, 255],  # green
    [90, 48, 0, 118, 255, 255]   # blue
]

# Define color values in BGR
COLOR_VALUES = [
    [51, 153, 255],  # orange
    [255, 0, 255],    # purple
    [0, 255, 0],      # green
    [255, 0, 0]       # blue
]

class ColorTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAPTURE_DEVICE)
        self.cap.set(3, FRAME_WIDTH)
        self.cap.set(4, FRAME_HEIGHT)
        self.cap.set(10, 150)
        self.points = []

    def find_color(self, img: np.ndarray) -> list:
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        points = []
        for i, color_range in enumerate(COLOR_RANGES):
            lower = np.array(color_range[:3])
            upper = np.array(color_range[3:])
            mask = cv2.inRange(img_hsv, lower, upper)
            x, y = self.get_contours(mask)
            if x != 0 and y != 0:
                points.append([x, y, i])
                cv2.circle(img, (x, y), 15, COLOR_VALUES[i], cv2.FILLED)
        return points

    def get_contours(self, img: np.ndarray) -> tuple:
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        x, y = 0, 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, _, _ = cv2.boundingRect(approx)
                x += _ // 2
        return x, y

    def draw_on_canvas(self, img: np.ndarray) -> None:
        for point in self.points:
            cv2.circle(img, (point[0], point[1]), 10, COLOR_VALUES[point[2]], cv2.FILLED)

    def run(self):
        while True:
            success, img = self.cap.read()
            if not success:
                break
            img_result = img.copy()
            points = self.find_color(img)
            self.points.extend(points)
            self.draw_on_canvas(img_result)
            cv2.imshow("Result", img_result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = ColorTracker()
    tracker.run()