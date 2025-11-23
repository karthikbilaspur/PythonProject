import cv2
import numpy as np

def add_watermark(video_file: str, watermark_file: str, output_file: str) -> None:
    """
    Adds a watermark to a video file.

    Args:
        video_file (str): Path to the video file.
        watermark_file (str): Path to the watermark image file.
        output_file (str): Path to the output video file.
    """
    # Load video and watermark
    video = cv2.VideoCapture(video_file)
    watermark = cv2.imread(watermark_file)

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Loop through frames
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Add watermark
        h, w, _ = watermark.shape
        x = width - w - 10
        y = height - h - 10
        roi = frame[y:y+h, x:x+w]
        result = cv2.addWeighted(roi, 1, watermark, 0.5, 0)
        frame[y:y+h, x:x+w] = result

        # Write output frame
        output.write(frame)

    # Release resources
    video.release()
    output.release()

def main():
    video_file = input("Enter the path to the video file: ")
    watermark_file = input("Enter the path to the watermark image file: ")
    output_file = input("Enter the path to the output video file: ")

    try:
        add_watermark(video_file, watermark_file, output_file)
        print(f"Watermark added to video: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()