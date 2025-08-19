
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
DOT_RADIUS = 10
LINE_WIDTH = 2

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the dots
dots = [
    (100, 100),
    (300, 100),
    (500, 100),
    (100, 300),
    (300, 300),
    (500, 300),
    (100, 500),
    (300, 500),
    (500, 500),
]

# Set up the lines
lines = []

# Set up the start and end dots
start_dot = None
end_dot = None

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for dot in dots:
                if ((dot[0] - event.pos[0]) ** 2 + (dot[1] - event.pos[1]) ** 2) ** 0.5 < DOT_RADIUS:
                    start_dot = dot
                    break
            else:
                start_dot = None
        elif event.type == pygame.MOUSEBUTTONUP:
            for dot in dots:
                if ((dot[0] - event.pos[0]) ** 2 + (dot[1] - event.pos[1]) ** 2) ** 0.5 < DOT_RADIUS and start_dot:
                    end_dot = dot
                    lines.append((start_dot, end_dot))
                    start_dot = None
                    end_dot = None
                    break
            else:
                start_dot = None
                end_dot = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                lines = []
            elif event.key == pygame.K_s:
                # Save the current state of the game
                with open("save.txt", "w") as f:
                    for line in lines:
                        f.write(f"{line[0][0]} {line[0][1]} {line[1][0]} {line[1][1]}\n")
            elif event.key == pygame.K_l:
                # Load a saved state of the game
                try:
                    with open("save.txt", "r") as f:
                        lines = []
                        for line in f.readlines():
                            x1, y1, x2, y2 = map(int, line.split())
                            lines.append(((x1, y1), (x2, y2)))
                except FileNotFoundError:
                    print("No save file found")

    # Draw everything
    screen.fill(WHITE)
    for dot in dots:
        pygame.draw.circle(screen, BLACK, dot, DOT_RADIUS)
    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], LINE_WIDTH)
    if start_dot:
        pygame.draw.line(screen, RED, start_dot, pygame.mouse.get_pos(), LINE_WIDTH)

    # Draw the start and end dots
    if start_dot:
        pygame.draw.circle(screen, GREEN, start_dot, DOT_RADIUS)
    if end_dot:
        pygame.draw.circle(screen, GREEN, end_dot, DOT_RADIUS)

    # Update the display
    pygame.display.flip()