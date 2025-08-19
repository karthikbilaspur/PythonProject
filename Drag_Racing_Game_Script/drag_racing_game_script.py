import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 50
TRACK_WIDTH = 200
FINISH_LINE = 700
MAX_SPEED = 10
ACCELERATION = 0.5

# Set up some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the fonts
font = pygame.font.Font(None, 36)

# Set up the cars
car1_x, car1_y = 100, HEIGHT // 2 - CAR_HEIGHT // 2
car1_speed = 0
car2_x, car2_y = 100, HEIGHT // 2 + CAR_HEIGHT // 2 + 20
car2_speed = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        car1_speed = min(car1_speed + ACCELERATION, MAX_SPEED)
    else:
        car1_speed = max(car1_speed - ACCELERATION, 0)

    car2_speed = min(car2_speed + random.uniform(0, ACCELERATION), MAX_SPEED)
    car1_x += car1_speed
    car2_x += car2_speed

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (int(car1_x), car1_y, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.rect(screen, BLUE, (int(car2_x), car2_y, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.line(screen, (0, 0, 0), (FINISH_LINE, 0), (FINISH_LINE, HEIGHT), 5)
    speed_text = font.render(f"Speed: {int(car1_speed)}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 10))

    # Check for winner
    if car1_x > FINISH_LINE:
        text = font.render("You win!", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break
    elif car2_x > FINISH_LINE:
        text = font.render("Computer wins!", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)