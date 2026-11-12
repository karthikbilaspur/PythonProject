import pygame
import sys
import random
import math

# --- Config ---
WIDTH, HEIGHT = 1000, 620
TOP_BAR = 70
FINISH_X = 880
START_X = 60
CAR_W, CAR_H = 64, 34

MAX_SPEED = 11
ACCEL = 0.28
DRAG = 0.08        # natural slowdown when not accelerating
BRAKE = 0.55
BOOST_MULT = 1.6
OVERHEAT_MAX = 100

# --- Colors ---
WHITE = (255, 255, 255)
BG = (45, 52, 54)
ROAD = (99, 110, 114)
ROAD_EDGE = (255, 255, 255)
DASH = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
GREEN = (46, 204, 113)
GRAY = (180, 180, 180)

class Car:
    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        name: str,
        is_player: bool = False,
    ):
        self.x = float(x)
        self.y = y
        self.speed = 0.0
        self.color = color
        self.name = name
        self.is_player = is_player
        self.top_speed = 0
        self.heat = 0
        self.overheated = False
        self.overheat_timer = 0
        self.wheel_rot = 0

    def accelerate(self, amount: float, boost: bool = False) -> None:
        if self.overheated:
            return
        mult = BOOST_MULT if boost else 1.0
        self.speed = min(self.speed + amount * mult, MAX_SPEED * mult)

    def brake(self, amount: float) -> None:
        self.speed = max(self.speed - amount, 0)

    def drag(self, amount: float) -> None:
        self.speed = max(self.speed - amount, 0)

    def update(self) -> None:
        self.x += self.speed
        self.top_speed = max(self.top_speed, self.speed)
        self.wheel_rot += self.speed * 2

        # Heat / overheat logic (player only)
        if self.is_player:
            if self.speed > MAX_SPEED * 0.95:  # boosting
                self.heat += 1.2
            else:
                self.heat = max(0, self.heat - 0.6)

            if self.heat >= OVERHEAT_MAX:
                self.overheated = True
                self.overheat_timer = 70  # ~1.1s stall
                self.heat = 0

            if self.overheated:
                self.speed = 0
                self.overheat_timer -= 1
                if self.overheat_timer <= 0:
                    self.overheated = False

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        # Shadow
        pygame.draw.ellipse(screen, (0, 0, 0, 60), (x, y + CAR_H - 4, CAR_W, 10))
        # Body
        pygame.draw.rect(screen, self.color, (x, y + 8, CAR_W, CAR_H - 8), border_radius=8)
        # Cabin
        pygame.draw.rect(screen, self.color, (x + 14, y, 30, 16), border_radius=6)
        pygame.draw.rect(screen, (180, 220, 255), (x + 18, y + 3, 22, 10), border_radius=3)
        # Headlight
        pygame.draw.circle(screen, YELLOW, (x + CAR_W - 2, y + 18), 4)
        # Wheels
        for wx in (x + 10, x + CAR_W - 18):
            pygame.draw.rect(screen, BLACK, (wx, y + CAR_H - 4, 12, 8), border_radius=3)
            pygame.draw.circle(screen, GRAY, (wx + 6, y + CAR_H), 3)
        # Name
        if self.is_player:
            pygame.draw.rect(screen, GREEN, (x, y - 18, 46, 14), border_radius=4)

def draw_checkered_finish(screen: pygame.Surface, x: int) -> None:
    for row in range(0, HEIGHT, 20):
        for col in range(2):
            colr = WHITE if (row // 20 + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, colr, (x + col * 10, row, 10, 20))

def draw_text(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    x: int,
    y: int,
    color: pygame.Color | tuple[int, int, int] | tuple[int, int, int, int] = WHITE,
    center: bool = False,
) -> pygame.Surface:
    surf = font.render(text, True, color)
    if center:
        x -= surf.get_width() // 2
        y -= surf.get_height() // 2
    screen.blit(surf, (x, y))
    return surf

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Drag Race — You vs Computer")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Segoe UI", 28, bold=True)
    big_font = pygame.font.SysFont("Segoe UI", 64, bold=True)
    small_font = pygame.font.SysFont("Segoe UI", 16)

    def reset():
        player = Car(START_X, 210, RED, "YOU", is_player=True)
        ai = Car(START_X, 380, BLUE, "CPU")
        return player, ai, "countdown", 180, None, 0  # state, timer, winner, race_time

    player, ai, state, countdown, winner, race_time = reset()

    running = True
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if state == "finished" and event.key == pygame.K_r:
                    player, ai, state, countdown, winner, race_time = reset()
                if state == "countdown" and event.key == pygame.K_SPACE:
                    countdown = 1  # skip countdown

        # --- State logic ---
        if state == "countdown":
            countdown -= 1
            if countdown <= 0:
                state = "racing"

        elif state == "racing":
            race_time += 1

            # --- Player controls ---
            boosting = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
            braking = keys[pygame.K_LSHIFT] or keys[pygame.K_s] or keys[pygame.K_DOWN]

            if boosting:
                player.accelerate(ACCEL, boost=True)
            elif braking:
                player.brake(BRAKE)
            else:
                player.drag(DRAG)

            # --- AI: rubber-banding + mistakes ---
            # If AI is behind, it gets a little faster; if ahead, a little slower
            gap = player.x - ai.x
            ai_accel = ACCEL * random.uniform(0.55, 1.0)
            if gap > 80:      # player ahead -> AI catches up
                ai_accel *= 1.35
            elif gap < -80:   # AI ahead -> AI eases off
                ai_accel *= 0.75

            ai.accelerate(ai_accel)
            if random.random() < 0.012:  # random mistake / brake
                ai.brake(random.uniform(0.5, 1.5))
            else:
                ai.drag(DRAG * 0.5)

            player.update()
            ai.update()

            # --- Finish check ---
            if player.x + CAR_W >= FINISH_X:
                winner, state = player, "finished"
            elif ai.x + CAR_W >= FINISH_X:
                winner, state = ai, "finished"

        # --- Draw ---
        screen.fill(BG)

        # Top HUD
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, TOP_BAR))
        draw_text(screen, font, f"YOU  {int(player.speed*10)} km/h", 20, 20, RED if player.overheated else WHITE)
        draw_text(screen, font, f"CPU  {int(ai.speed*10)} km/h", 280, 20, BLUE)
        draw_text(screen, font, f"Time: {race_time/60:.1f}s", 540, 20, WHITE)
        draw_text(screen, small_font, "SPACE/W/↑ = Boost   SHIFT/S/↓ = Brake   R = Restart   Esc = Quit", 700, 16, GRAY)
        draw_text(screen, small_font, "Don't overheat! Boosting too long stalls you.", 700, 34, YELLOW if player.heat > 70 else GRAY)

        # Heat bar (player)
        pygame.draw.rect(screen, (80, 80, 80), (20, 52, 200, 10), border_radius=5)
        heat_col = RED if player.heat > 80 else (YELLOW if player.heat > 50 else GREEN)
        pygame.draw.rect(screen, heat_col, (20, 52, 200 * player.heat / OVERHEAT_MAX, 10), border_radius=5)
        if player.overheated:
            draw_text(screen, small_font, "OVERHEATED!", 230, 50, RED)

        # Road
        pygame.draw.rect(screen, ROAD, (0, 150, WIDTH, 320))
        pygame.draw.line(screen, ROAD_EDGE, (0, 150), (WIDTH, 150), 3)
        pygame.draw.line(screen, ROAD_EDGE, (0, 470), (WIDTH, 470), 3)
        # Center dashes
        for x in range(0, WIDTH, 50):
            pygame.draw.rect(screen, DASH, (x, 308, 28, 5))
        # Lane labels
        draw_text(screen, small_font, "YOU", 12, 195, WHITE)
        draw_text(screen, small_font, "CPU", 12, 365, WHITE)

        # Start / Finish
        pygame.draw.line(screen, GREEN, (START_X, 150), (START_X, 470), 4)
        draw_checkered_finish(screen, FINISH_X)
        draw_text(screen, small_font, "FINISH", FINISH_X - 18, 130, WHITE)

        # Progress dots (mini-map)
        cars: tuple[tuple[Car, tuple[int, int, int]], ...] = (
            (player, RED),
            (ai, BLUE),
        )
        for car, col in cars:
            prog = max(0, min(1, (car.x - START_X) / (FINISH_X - START_X)))
            pygame.draw.circle(screen, col, (int(60 + prog * 880), 92 if car.is_player else 108), 6)

        player.draw(screen)
        ai.draw(screen)

        # Countdown overlay
        if state == "countdown":
            n = math.ceil(countdown / 60)
            label = str(n) if n > 0 else "GO!"
            col = YELLOW if n > 0 else GREEN
            # Dim
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            draw_text(screen, big_font, label, WIDTH // 2, HEIGHT // 2, col, center=True)
            draw_text(screen, font, "Hold SPACE to boost!", WIDTH // 2, HEIGHT // 2 + 60, WHITE, center=True)

        # Finished overlay
        if state == "finished":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            is_win = winner is player
            draw_text(screen, big_font, "🏆 YOU WIN!" if is_win else "💻 CPU WINS!", WIDTH // 2, HEIGHT // 2 - 60,
                      GREEN if is_win else BLUE, center=True)
            draw_text(screen, font, f"Time: {race_time/60:.2f}s   •   Your top speed: {int(player.top_speed*10)} km/h",
                      WIDTH // 2, HEIGHT // 2 + 10, WHITE, center=True)
            draw_text(screen, font, "Press R to race again  •  Esc to quit",
                      WIDTH // 2, HEIGHT // 2 + 55, YELLOW, center=True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()