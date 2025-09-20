import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ink Art Puzzle Adventure")

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED = (255, 0, 0)

# Player properties
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_size = 50

# Ink art properties
ink_art_size = 100
ink_art_x, ink_art_y = 100, 100

# Score
score = 0
font = pygame.font.Font(None, 36)

# Main game loop
def game_loop():
    global player_x, player_y, score
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Collision detection with ink art
        if (player_x + player_size > ink_art_x and
            player_x < ink_art_x + ink_art_size and
            player_y + player_size > ink_art_y and
            player_y < ink_art_y + ink_art_size):
            score += 1
            ink_art_x = random.randint(0, WIDTH - ink_art_size)
            ink_art_y = random.randint(0, HEIGHT - ink_art_size)

        # Draw the player and background
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))
        pygame.draw.rect(screen, RED, (ink_art_x, ink_art_y, ink_art_size, ink_art_size))

        # Draw score
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()
sys.exit()