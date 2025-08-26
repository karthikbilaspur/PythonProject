import pygame
import sys

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

# Colors
bg_color = (135, 206, 235)
floor_color = (224, 215, 188)

# Fonts
font = pygame.font.Font('freesansbold.ttf', 24)

# Floor
floor_x_pos = 0
floor_y_pos = 450

# Bird
bird_x_pos = 50
bird_y_pos = 256
bird_size = 20

# Pipes
pipe_x_pos = 300
pipe_y_pos = 200
pipe_gap = 100
pipe_width = 50

def draw_floor():
    pygame.draw.rect(screen, floor_color, (floor_x_pos, floor_y_pos, 288, 62))
    pygame.draw.rect(screen, floor_color, (floor_x_pos + 288, floor_y_pos, 288, 62))

def draw_bird():
    pygame.draw.rect(screen, (255, 255, 255), (bird_x_pos, bird_y_pos, bird_size, bird_size))

def draw_pipes():
    pygame.draw.rect(screen, (0, 255, 0), (pipe_x_pos, 0, pipe_width, pipe_y_pos))
    pygame.draw.rect(screen, (0, 255, 0), (pipe_x_pos, pipe_y_pos + pipe_gap, pipe_width, 512 - pipe_y_pos - pipe_gap))

def check_collision():
    if bird_y_pos < 0 or bird_y_pos > floor_y_pos - bird_size:
        return True
    if pipe_x_pos < bird_x_pos + bird_size and pipe_x_pos + pipe_width > bird_x_pos:
        if bird_y_pos < pipe_y_pos or bird_y_pos + bird_size > pipe_y_pos + pipe_gap:
            return True
    return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_x_pos = 300
                bird_y_pos = 256
                bird_movement = 0
                score = 0

    screen.fill(bg_color)

    if game_active:
        # Bird Movement
        bird_movement += gravity
        bird_y_pos += bird_movement

        # Pipe Movement
        pipe_x_pos -= 2
        if pipe_x_pos < -pipe_width:
            pipe_x_pos = 300
            score += 1

        # Collision Detection
        if check_collision():
            game_active = False

        # Draw Everything
        draw_bird()
        draw_pipes()
        draw_floor()

        # Update Floor Position
        floor_x_pos -= 1
        if floor_x_pos < -288:
            floor_x_pos = 0

        # Display Score
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (144, 50))

    else:
        # Display Game Over Screen
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (80, 256))
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (80, 300))
        if score > high_score:
            high_score = score
        high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
        screen.blit(high_score_text, (80, 350))

    pygame.display.update()
    clock.tick(120)