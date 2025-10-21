import cv2
import numpy as np

def load_yolo():
    try:
        net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        classes = []
        with open("coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        return net, classes, output_layers
    except Exception as e:
        print(f"Error loading YOLO model: {str(e)}")
        return None, None, None

def detect_objects(img: np.ndarray, net: cv2.dnn.Net, output_layers: list) -> tuple:
    try:
        height, width, _ = img.shape
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        return outs
    except Exception as e:
        print(f"Error detecting objects: {str(e)}")
        return None


def draw_boxes(img, outs, classes):
    try:
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * img.shape[1])
                    center_y = int(detection[1] * img.shape[0])
                    w = int(detection[2] * img.shape[1])
                    h = int(detection[3] * img.shape[0])
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_SIMPLEX
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i], 2))
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label + " " + confidence, (x, y + 20), font, 1, color, 2)
        return img
    except Exception as e:
        print(f"Error drawing boxes: {str(e)}")
        return img

def main():
    net, classes, output_layers = load_yolo()
    if net is None or classes is None or output_layers is None:
        return

    cap = cv2.VideoCapture(0)  # Use 0 for default camera
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, img = cap.read()
        if not ret:
            print("Cannot receive frame")
            break

        outs = detect_objects(img, net, output_layers)
        if outs is not None:
            img = draw_boxes(img, outs, classes)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()