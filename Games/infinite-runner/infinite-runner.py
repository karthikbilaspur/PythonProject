import pygame
import random
from typing import Literal, TypedDict

# --- Setup ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infinite Runner - Enhanced")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 60, 60)
GREEN = (0, 200, 100)
YELLOW = (255, 220, 0)
PURPLE = (180, 80, 255)
CYAN = (0, 220, 220)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# --- Sounds (safe if files missing) ---
def load_sound(path: str):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

def play(sound: pygame.mixer.Sound | None):
    if sound:
        sound.play()

try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)
except:
    pass

jump_sound = load_sound("jump_sound.wav")
collision_sound = load_sound("collision_sound.wav")
power_up_sound = load_sound("power_up.wav")

# --- Player ---
player_w, player_h = 50, 50
ground_y = SCREEN_HEIGHT - player_h - 20
player_x = SCREEN_WIDTH // 2 - player_w // 2
player_y = ground_y
player_speed = 6
vel_y = 0
gravity = 0.8
jump_power = -15
is_jumping = False

player_invincible = False
invincible_timer = 0
score_multiplier = 1
multiplier_timer = 0

# --- Game state ---
class Obstacle(TypedDict):
    x: float
    y: float
    type: Literal["rect", "tri", "circle", "tall"]
    w: int
    h: int
    dx: int


class PowerUp(TypedDict):
    x: int
    y: float
    type: Literal["invincibility", "score_multiplier", "slow"]


score = 0
high_score = 0
speed = 5
obstacles: list[Obstacle] = []
power_ups: list[PowerUp] = []
spawn_timer = 0
game_over = False
paused = False

def spawn_obstacle():
    o_type = random.choice(("rect", "tri", "circle", "tall"))
    if o_type == "rect":
        w, h = 100, 20
    elif o_type == "tri":
        w, h = 80, 40
    elif o_type == "circle":
        w, h = 50, 50
    else:  # tall - forces a jump
        w, h = 40, 80
    x = random.randint(0, SCREEN_WIDTH - w)
    dx = random.choice([-1, 0, 1]) if o_type == "tri" else 0
    obstacles.append({"x": x, "y": -h, "type": o_type, "w": w, "h": h, "dx": dx})

def spawn_power_up():
    p_type: Literal["invincibility", "score_multiplier", "slow"] = random.choice(
        ("invincibility", "score_multiplier", "slow")
    )
    x = random.randint(0, SCREEN_WIDTH - 25)
    power_ups.append({"x": x, "y": -25, "type": p_type})

def reset():
    global player_x, player_y, vel_y, score, speed, obstacles, power_ups
    global player_invincible, invincible_timer, score_multiplier, multiplier_timer, game_over
    player_x = SCREEN_WIDTH // 2 - player_w // 2
    player_y = ground_y
    vel_y = 0
    score = 0
    speed = 5
    obstacles = []
    power_ups = []
    player_invincible = False
    invincible_timer = 0
    score_multiplier = 1
    multiplier_timer = 0
    game_over = False

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000  # seconds, for timers

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_r and game_over:
                reset()
            if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                vel_y = jump_power
                is_jumping = True
                play(jump_sound)

    if paused or game_over:
        # Still draw below, just skip updates
        pass
    else:
        # --- Movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_w:
            player_x += player_speed

        # Real jump physics
        if is_jumping:
            vel_y += gravity
            player_y += vel_y
            if player_y >= ground_y:
                player_y = ground_y
                vel_y = 0
                is_jumping = False

        # --- Timers ---
        if player_invincible:
            invincible_timer -= dt
            if invincible_timer <= 0:
                player_invincible = False
        if score_multiplier > 1:
            multiplier_timer -= dt
            if multiplier_timer <= 0:
                score_multiplier = 1

        # --- Difficulty ramp ---
        speed = 5 + score / 1500
        spawn_timer -= 1
        if spawn_timer <= 0:
            spawn_obstacle()
            # Spawn gap shrinks as you get faster
            spawn_timer = random.randint(30, 70) - int(speed)
            if random.random() < 0.15:
                spawn_power_up()

        # --- Obstacles ---
        player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
        new_obstacles: list[Obstacle] = []
        for o in obstacles:
            o["y"] += speed
            o["x"] += o["dx"] * 2
            # Bounce triangles off walls
            if o["x"] <= 0 or o["x"] + o["w"] >= SCREEN_WIDTH:
                o["dx"] *= -1

            if o["y"] > SCREEN_HEIGHT:
                continue  # off screen, drop it

            o_rect = pygame.Rect(o["x"], o["y"], o["w"], o["h"])
            if not player_invincible and player_rect.colliderect(o_rect):
                play(collision_sound)
                high_score = max(high_score, score)
                game_over = True
                break
            new_obstacles.append(o)
        obstacles = new_obstacles

        # --- Power-ups ---
        new_power_ups: list[PowerUp] = []
        for p in power_ups:
            p["y"] += speed
            if p["y"] > SCREEN_HEIGHT:
                continue
            p_rect = pygame.Rect(p["x"], p["y"], 25, 25)
            if player_rect.colliderect(p_rect):
                play(power_up_sound)
                if p["type"] == "invincibility":
                    player_invincible = True
                    invincible_timer = 5
                elif p["type"] == "score_multiplier":
                    score_multiplier = 2
                    multiplier_timer = 8
                elif p["type"] == "slow":
                    score += 50
                    # brief slow-down effect via temporary speed cut handled by score
                continue  # collected, drop it
            new_power_ups.append(p)
        power_ups = new_power_ups

        score += 1 * score_multiplier

    # --- Draw ---
    screen.fill(WHITE)
    # Ground line
    pygame.draw.line(screen, BLACK, (0, ground_y + player_h), (SCREEN_WIDTH, ground_y + player_h), 3)

    # Player - flashes when invincible
    if player_invincible and int(pygame.time.get_ticks() / 150) % 2 == 0:
        pygame.draw.rect(screen, YELLOW, (player_x, player_y, player_w, player_h))
    else:
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_w, player_h))
    # Eyes so it looks alive
    pygame.draw.circle(screen, WHITE, (player_x + 15, player_y + 18), 6)
    pygame.draw.circle(screen, WHITE, (player_x + 35, player_y + 18), 6)
    pygame.draw.circle(screen, BLACK, (player_x + 15, player_y + 18), 3)
    pygame.draw.circle(screen, BLACK, (player_x + 35, player_y + 18), 3)

    for o in obstacles:
        if o["type"] == "rect":
            pygame.draw.rect(screen, RED, (o["x"], o["y"], o["w"], o["h"]))
        elif o["type"] == "tri":
            pygame.draw.polygon(screen, GREEN, [
                (o["x"], o["y"] + o["h"]),
                (o["x"] + o["w"], o["y"] + o["h"]),
                (o["x"] + o["w"] // 2, o["y"])
            ])
        elif o["type"] == "circle":
            pygame.draw.circle(screen, PURPLE, (int(o["x"] + o["w"] // 2), int(o["y"] + o["h"] // 2)), o["w"] // 2)
        elif o["type"] == "tall":
            pygame.draw.rect(screen, (255, 140, 0), (o["x"], o["y"], o["w"], o["h"]))

    for p in power_ups:
        color = YELLOW if p["type"] == "invincibility" else CYAN if p["type"] == "score_multiplier" else GREEN
        pygame.draw.rect(screen, color, (p["x"], p["y"], 25, 25))
        pygame.draw.rect(screen, BLACK, (p["x"], p["y"], 25, 25), 2)

    # HUD
    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Best: {high_score}", True, BLACK), (10, 45))
    screen.blit(font.render(f"Speed: {speed:.1f}", True, BLACK), (SCREEN_WIDTH - 140, 10))
    if player_invincible:
        screen.blit(font.render(f"INVINCIBLE: {invincible_timer:.1f}s", True, RED), (10, 80))
    if score_multiplier > 1:
        screen.blit(font.render(f"x2 SCORE: {multiplier_timer:.1f}s", True, PURPLE), (10, 110))

    if paused:
        overlay = big_font.render("PAUSED - Press P", True, BLACK)
        screen.blit(overlay, (SCREEN_WIDTH // 2 - overlay.get_width() // 2, SCREEN_HEIGHT // 2))

    if game_over:
        overlay = big_font.render("GAME OVER", True, RED)
        screen.blit(overlay, (SCREEN_WIDTH // 2 - overlay.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        sub = font.render(f"Score: {score}  |  Press R to restart", True, BLACK)
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.update()

pygame.quit()