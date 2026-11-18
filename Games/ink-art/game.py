import pygame
import sys
import random
import math
from typing import TypedDict

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ink Art Puzzle Adventure")
clock = pygame.time.Clock()

# Colors - ink / paper aesthetic
PAPER = (245, 240, 230)
INK = (20, 20, 25)
RED = (200, 40, 40)
BLUE = (40, 90, 200)
GOLD = (220, 170, 40)
GREEN = (40, 160, 90)
PURPLE = (130, 60, 180)
GRAY = (150, 145, 135)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 72)

# --- Player ---
player_size = 40
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_trail: list[tuple[int, int]] = []  # ink trail behind you

# --- Ink Blots / Puzzle ---
# You must collect them IN ORDER - red, blue, green, purple...
# Collecting out of order costs you!
COLORS: list[tuple[str, tuple[int, int, int]]] = [
    ("RED", RED),
    ("BLUE", BLUE),
    ("GREEN", GREEN),
    ("PURPLE", PURPLE),
    ("GOLD", GOLD),
]


class InkBlot(TypedDict):
    x: int
    y: int
    size: int
    name: str
    color: tuple[int, int, int]
    pulse: float
    collected: bool


current_target_idx = 0
ink_blots: list[InkBlot] = []
combo = 0
best_combo = 0

def spawn_blots():
    global ink_blots
    ink_blots = []
    # Spawn 5 blots, scattered, not overlapping player start
    positions: list[tuple[int, int]] = []
    for name, color in COLORS:
        for _ in range(100):  # try to find non-overlapping spot
            x = random.randint(20, WIDTH - 120)
            y = random.randint(60, HEIGHT - 120)
            # Don't spawn too close to player or other blots
            if math.hypot(x - player_x, y - player_y) < 150:
                continue
            if any(math.hypot(x - px, y - py) < 110 for px, py in positions):
                continue
            positions.append((x, y))
            break
        else:
            x, y = random.randint(20, WIDTH - 120), random.randint(60, HEIGHT - 120)
            positions.append((x, y))
        ink_blots.append({
            "x": x, "y": y, "size": 70,
            "name": name, "color": color,
            "pulse": random.uniform(0, math.pi * 2),
            "collected": False,
        })

spawn_blots()

# --- Game state ---
score = 0
level = 1
lives = 3
time_left = 30
level_complete = False
game_over = False
shake = 0
message = ""
message_timer = 0

def next_level():
    global level, time_left, current_target_idx, level_complete, combo
    level += 1
    time_left = max(15, 30 - level * 2)  # gets harder
    current_target_idx = 0
    combo = 0
    level_complete = False
    spawn_blots()

def reset_game():
    global score, level, lives, time_left, current_target_idx, combo, game_over, level_complete
    score = 0
    level = 1
    lives = 3
    time_left = 30
    current_target_idx = 0
    combo = 0
    game_over = False
    level_complete = False
    spawn_blots()

def show_message(text: str, duration: float = 1.5) -> None:
    global message, message_timer
    message = text
    message_timer = duration

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or level_complete):
                if game_over:
                    reset_game()
                else:
                    next_level()
            if event.key == pygame.K_SPACE and level_complete:
                next_level()

    if not game_over and not level_complete:
        # --- Movement (with bounds!) ---
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += player_speed

        player_x = max(0, min(WIDTH - player_size, player_x + dx))
        player_y = max(0, min(HEIGHT - player_size, player_y + dy))

        # Ink trail
        player_trail.append((player_x + player_size // 2, player_y + player_size // 2))
        if len(player_trail) > 25:
            player_trail.pop(0)

        # --- Timer ---
        time_left -= dt
        if time_left <= 0:
            lives -= 1
            show_message("TIME UP! -1 Life")
            shake = 15
            if lives <= 0:
                game_over = True
            else:
                time_left = 30
                current_target_idx = 0
                combo = 0

        # --- Collision - ONE hit per blot, not every frame ---
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for blot in ink_blots:
            if blot["collected"]:
                continue
            blot_rect = pygame.Rect(blot["x"], blot["y"], blot["size"], blot["size"])
            if player_rect.colliderect(blot_rect):
                # Is it the CORRECT next color?
                expected_name = COLORS[current_target_idx][0]
                if blot["name"] == expected_name:
                    blot["collected"] = True
                    combo += 1
                    best_combo = max(best_combo, combo)
                    points = 100 * combo + level * 50
                    score += points
                    show_message(f"+{points}  {blot['name']}!  Combo x{combo}")
                    current_target_idx += 1

                    if current_target_idx >= len(COLORS):
                        # Level complete!
                        bonus = int(time_left) * 10
                        score += bonus
                        show_message(f"LEVEL CLEAR! +{bonus} time bonus")
                        level_complete = True
                else:
                    # Wrong blot!
                    lives -= 1
                    combo = 0
                    shake = 15
                    show_message(f"WRONG! Needed {expected_name}, got {blot['name']}")
                    # Knock player back a bit
                    player_x = WIDTH // 2
                    player_y = HEIGHT // 2
                    if lives <= 0:
                        game_over = True

        # Animate blots
        for blot in ink_blots:
            blot["pulse"] += dt * 3

    if message_timer > 0:
        message_timer -= dt

    # --- Draw ---
    # Screen shake
    shake_x = random.randint(-shake, shake) if shake > 0 else 0
    shake_y = random.randint(-shake, shake) if shake > 0 else 0
    if shake > 0:
        shake -= 1

    screen.fill(PAPER)

    # Paper texture dots
    for x in range(0, WIDTH, 40):
        for y in range(0, HEIGHT, 40):
            pygame.draw.circle(screen, (235, 228, 215), (x, y), 1)

    # Ink trail (fading)
    for i, (tx, ty) in enumerate(player_trail):
        alpha = i / len(player_trail)
        size = int(4 + alpha * 10)
        pygame.draw.circle(screen, (180, 180, 190), (tx + shake_x, ty + shake_y), size)

    # Target hint at top
    if not game_over and not level_complete:
        target_name, target_color = COLORS[current_target_idx]
        hint = small_font.render(f"Collect in order:  →  {target_name}  →", True, target_color)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 10))

        # Order display - shows full sequence
        for i, (name, color) in enumerate(COLORS):
            x = 20 + i * 90
            y = HEIGHT - 45
            w = 70
            if i < current_target_idx:
                # Done - draw check
                pygame.draw.rect(screen, color, (x, y, w, 25))
                txt = small_font.render("✓ " + name[:3], True, PAPER)
            elif i == current_target_idx:
                # Current - pulsing
                pulse = int(5 + math.sin(pygame.time.get_ticks() / 150) * 3)
                pygame.draw.rect(screen, color, (x - pulse, y - pulse, w + pulse*2, 25 + pulse*2))
                txt = small_font.render(name[:3], True, PAPER)
            else:
                pygame.draw.rect(screen, GRAY, (x, y, w, 25))
                txt = small_font.render(name[:3], True, WHITE)
            screen.blit(txt, (x + 8, y + 3))

    # Blots - organic ink blob shape
    for blot in ink_blots:
        if blot["collected"]:
            continue
        cx, cy = blot["x"] + blot["size"] // 2, blot["y"] + blot["size"] // 2
        pulse_size = blot["size"] // 2 + int(math.sin(blot["pulse"]) * 4)
        is_target = blot["name"] == COLORS[current_target_idx][0] if current_target_idx < len(COLORS) else False

        # Outer glow if it's the target
        if is_target:
            pygame.draw.circle(screen, blot["color"], (cx + shake_x, cy + shake_y), pulse_size + 12, 3)

        # Blobby ink shape - 8 wobbly points
        points = []
        for a in range(8):
            angle = a / 8 * math.pi * 2
            r = pulse_size + math.sin(blot["pulse"] + a) * 6
            points.append((cx + math.cos(angle) * r + shake_x, cy + math.sin(angle) * r + shake_y))
        pygame.draw.polygon(screen, blot["color"], points)
        # Inner highlight
        pygame.draw.circle(screen, PAPER, (cx - 10 + shake_x, cy - 10 + shake_y), 8)
        # Name label
        label = small_font.render(blot["name"], True, PAPER)
        screen.blit(label, (cx - label.get_width() // 2 + shake_x, cy - 8 + shake_y))

    # Player - ink brush square
    pygame.draw.rect(screen, INK, (player_x + shake_x, player_y + shake_y, player_size, player_size), border_radius=8)
    pygame.draw.rect(screen, PAPER, (player_x + 8 + shake_x, player_y + 8 + shake_y, player_size - 16, player_size - 16), border_radius=4)
    # Eyes
    pygame.draw.circle(screen, INK, (player_x + 14 + shake_x, player_y + 18 + shake_y), 4)
    pygame.draw.circle(screen, INK, (player_x + 26 + shake_x, player_y + 18 + shake_y), 4)

    # HUD
    screen.blit(font.render(f"Score: {score}", True, INK), (10, 10))
    screen.blit(small_font.render(f"Level {level}  |  Lives: {'♥' * lives}  |  Combo x{combo}", True, INK), (10, 45))
    # Timer bar
    timer_color = RED if time_left < 10 else INK
    pygame.draw.rect(screen, GRAY, (WIDTH - 210, 10, 200, 20), 2)
    pygame.draw.rect(screen, timer_color, (WIDTH - 208, 12, int(196 * max(0, time_left) / 30), 16))
    timer_txt = small_font.render(f"{max(0, int(time_left))}s", True, timer_color)
    screen.blit(timer_txt, (WIDTH - 45, 35))

    # Message popup
    if message_timer > 0:
        msg = font.render(message, True, INK)
        # White pill behind it
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - msg.get_width()//2 - 10, 70, msg.get_width() + 20, 36), border_radius=18)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 72))

    # Overlays
    if level_complete:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((245, 240, 230, 200))
        screen.blit(overlay, (0, 0))
        title = big_font.render("LEVEL CLEAR!", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
        sub = font.render(f"Score: {score}  |  Best Combo: x{best_combo}", True, INK)
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2))
        hint2 = font.render("Press SPACE for next level", True, INK)
        screen.blit(hint2, (WIDTH//2 - hint2.get_width()//2, HEIGHT//2 + 50))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 20, 25, 180))
        screen.blit(overlay, (0, 0))
        title = big_font.render("GAME OVER", True, RED)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
        sub = font.render(f"Final Score: {score}  |  Reached Level {level}", True, WHITE)
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2))
        hint2 = font.render("Press R to play again", True, WHITE)
        screen.blit(hint2, (WIDTH//2 - hint2.get_width()//2, HEIGHT//2 + 50))

    pygame.display.update()

pygame.quit()
sys.exit()