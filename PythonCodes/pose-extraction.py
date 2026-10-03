import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

# Define the snake's initial position and direction
snake_pos = [(200, 200), (220, 200), (240, 200)]
direction = 'right'

# Define the food's position
food_pos = (400, 300)

# Define the score
score = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale and apply thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the center of the contours
    centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            centers.append((cx, cy))

    # Determine the direction based on the centers
    if len(centers) > 1:
        dx = centers[0][0] - centers[1][0]
        dy = centers[0][1] - centers[1][1]

        if abs(dx) > abs(dy):
            if dx > 0:
                direction = 'left'
            else:
                direction = 'right'
        else:
            if dy > 0:
                direction = 'up'
            else:
                direction = 'down'

    # Update the snake's position
    head = snake_pos[-1]
    if direction == 'up':
        new_head = (head[0], head[1] - 20)
    elif direction == 'down':
        new_head = (head[0], head[1] + 20)
    elif direction == 'left':
        new_head = (head[0] - 20, head[1])
    elif direction == 'right':
        new_head = (head[0] + 20, head[1])

    snake_pos.append(new_head)

    # Check for collision with food
    if snake_pos[-1] == food_pos:
        score += 1
        food_pos = (np.random.randint(0, 800) // 20 * 20, np.random.randint(0, 600) // 20 * 20)
    else:
        snake_pos.pop(0)

    # Check for collision with edge or self
    if (snake_pos[-1][0] < 0 or snake_pos[-1][0] >= 800 or
        snake_pos[-1][1] < 0 or snake_pos[-1][1] >= 600 or
        snake_pos[-1] in snake_pos[:-1]):
        print(f"Game Over! Your score is {score}.")
        break

    # Draw the snake and food
    frame = np.zeros((600, 800, 3), np.uint8)
    for pos in snake_pos:
        cv2.rectangle(frame, (pos[0], pos[1]), (pos[0] + 20, pos[1] + 20), (0, 255, 0), -1)
    cv2.rectangle(frame, (food_pos[0], food_pos[1]), (food_pos[0] + 20, food_pos[1] + 20), (0, 0, 255), -1)

    cv2.imshow('Snake Game', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()