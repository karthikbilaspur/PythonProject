import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infinite Runner with Customizable Obstacles")

# Load sound effects and background music
pygame.mixer.music.load("background_music.mp3")
jump_sound = pygame.mixer.Sound("jump_sound.wav")
collision_sound = pygame.mixer.Sound("collision_sound.wav")
power_up_sound = pygame.mixer.Sound("power_up.wav")

# Scoring
score = 0
font = pygame.font.Font(None, 36)

# Player attributes
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 20
player_speed = 5
player_invincible = False

# Obstacle attributes
obstacle_width = 100
obstacle_height = 20
obstacle_speed = 5
obstacles = []

# Power-up attributes
power_up_width = 20
power_up_height = 20
power_up_speed = 5
power_ups = []

# Game loop
running = True
clock = pygame.time.Clock()
pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input handling - left and right arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Jumping with Spacebar
    if keys[pygame.K_SPACE] and player_y == SCREEN_HEIGHT - player_height - 20:
        player_y -= 10
        jump_sound.play()

    # Apply gravity
    if player_y < SCREEN_HEIGHT - player_height - 20:
        player_y += 5

    # Add a new obstacle randomly
    if random.randint(0, 100) < 2:
        obstacle_type = random.choice(["rect", "tri", "circle"])
        obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)

        if obstacle_type == "circle":
            obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width - 50)

        obstacles.append((obstacle_x, -obstacle_height, obstacle_type))

    # Add a new power-up randomly
    if random.randint(0, 100) < 1:
        power_up_type = random.choice(["invincibility", "score_multiplier"])
        power_up_x = random.randint(0, SCREEN_WIDTH - power_up_width)
        power_ups.append((power_up_x, -power_up_height, power_up_type))

    # Update obstacle positions
    for i, (obstacle_x, obstacle_y, obstacle_type) in enumerate(obstacles):
        if obstacle_type == "rect":
            obstacles[i] = (obstacle_x, obstacle_y + obstacle_speed)
        elif obstacle_type == "tri":
            obstacles[i] = (obstacle_x + obstacle_speed,
                            obstacle_y + obstacle_speed)
        elif obstacle_type == "circle":
            angle = 0.1
            rotated_obstacle_x = obstacle_x + (obstacle_width // 2)
            rotated_obstacle_y = obstacle_y + (obstacle_height // 2)
            obstacles[i] = (rotated_obstacle_x - obstacle_width // 2 * math.cos(angle),
                            rotated_obstacle_y -
                            obstacle_height // 2 * math.sin(angle),
                            "circle")

        if obstacle_y > SCREEN_HEIGHT:
            del obstacles[i]

        if not player_invincible and obstacle_y + obstacle_height > player_y and obstacle_y < player_y + player_height:
            if obstacle_x + obstacle_width > player_x and obstacle_x < player_x + player_width:
                collision_sound.play()
                running = False

    # Update power-up positions
    for i, (power_up_x, power_up_y, power_up_type) in enumerate(power_ups):
        power_ups[i] = (power_up_x, power_up_y + power_up_speed)

        if power_up_y > SCREEN_HEIGHT:
            del power_ups[i]

        if power_up_y + power_up_height > player_y and power_up_y < player_y + player_height:
            if power_up_x + power_up_width > player_x and power_up_x < player_x + player_width:
                power_up_sound.play()
                if power_up_type == "invincibility":
                    player_invincible = True
                elif power_up_type == "score_multiplier":
                    score += 100
                del power_ups[i]

    # Increase the score
    score += 1

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, (0, 0, 255), (player_x,
                     player_y, player_width, player_height))

    # Draw the obstacles
    for obstacle_x, obstacle_y, obstacle_type in obstacles:
        if obstacle_type == "rect":
            pygame.draw.rect(screen, (255, 0, 0), (obstacle_x,
                             obstacle_y, obstacle_width, obstacle_height))
        elif obstacle_type == "tri":
            pygame.draw.polygon(screen, (0, 255, 0), [(obstacle_x, obstacle_y), (obstacle_x + obstacle_width, obstacle_y),
                                                      (obstacle_x + obstacle_width // 2, obstacle_y + obstacle_height)])
        elif obstacle_type == "circle":
            pygame.draw.circle(screen, (0, 0, 255), (int(obstacle_x + obstacle_width // 2),
                                                     int(obstacle_y + obstacle_height // 2)), obstacle_width // 2)

    # Draw the power-ups
    for power_up_x, power_up_y, power_up_type in power_ups:
        pygame.draw.rect(screen, (255, 255, 0), (power_up_x,
                         power_up_y, power_up_width, power_up_height))

    # Draw the score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()