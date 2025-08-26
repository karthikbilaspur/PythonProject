import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
ALIEN_SIZE = 50
LASER_SIZE = 10

# Set up some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the fonts
font = pygame.font.Font(None, 36)

# Set up the player
player = pygame.Rect(WIDTH / 2, HEIGHT - PLAYER_SIZE * 2, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 5
player_shield = 100

# Set up the bullets
bullets = []
bullet_speed = 5

# Set up the laser
laser_charged = False
laser_beam = pygame.Rect(0, 0, LASER_SIZE, HEIGHT)

# Set up the aliens
aliens = []
alien_speed = 2
alien_spawn_time = 0
alien_wave = 1

# Set up the score
score = 0
combo = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.centerx, player.top, BULLET_SIZE, BULLET_SIZE))
            if event.key == pygame.K_LSHIFT and laser_charged:
                laser_beam.x = player.centerx
                laser_beam.y = 0
                for alien in aliens:
                    if alien.colliderect(laser_beam):
                        aliens.remove(alien)
                        score += 10
                laser_charged = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Charge the laser
    if keys[pygame.K_LSHIFT] and not laser_charged:
        laser_charged = True

    # Move the bullets
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Spawn aliens
    current_time = pygame.time.get_ticks()
    if current_time - alien_spawn_time > 1000 / alien_wave:
        alien_spawn_time = current_time
        aliens.append(pygame.Rect(random.randint(0, WIDTH - ALIEN_SIZE), 0, ALIEN_SIZE, ALIEN_SIZE))

    # Move aliens
    for alien in aliens:
        alien.y += alien_speed
        if alien.y > HEIGHT:
            aliens.remove(alien)
            player_shield -= 10
            combo = 0

    # Check for collisions
    for bullet in bullets:
        for alien in aliens:
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 1
                combo += 1
                if combo % 10 == 0:
                    score += 10

    for alien in aliens:
        if alien.colliderect(player):
            aliens.remove(alien)
            player_shield -= 20
            combo = 0

    # Check for game over
    if player_shield <= 0:
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH / 2 - 50, HEIGHT / 2))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH / 2 - 50, HEIGHT / 2 + 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    # Increase alien wave
    if score > alien_wave * 100:
        alien_wave += 1

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, GREEN, player)
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    for alien in aliens:
        pygame.draw.rect(screen, RED, alien)
    if laser_charged:
        pygame.draw.rect(screen, BLUE, (player.centerx, player.top, LASER_SIZE, LASER_SIZE))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    shield_text = font.render(f"Shield: {player_shield}", True, WHITE)
    screen.blit(shield_text, (10, 50))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

    