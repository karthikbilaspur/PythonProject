import pygame
import sys
import random
import math
import os
from typing import TypedDict

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 200, 0)
DARK = (40, 40, 40)

TOWER_COST = 50
UPGRADE_COST = 30
KILL_REWARD = 10
ESCAPE_PENALTY = 10
START_MONEY = 100


class WeatherEffect(TypedDict):
    speed: float
    range: float
    label: str


# Weather effects: enemy speed multiplier, tower range multiplier
WEATHER: dict[str, WeatherEffect] = {
    "Sunny": {"speed": 1.0, "range": 1.0, "label": "Sunny - normal"},
    "Rainy": {"speed": 0.5, "range": 0.9, "label": "Rainy - enemies slow, towers slightly shorter range"},
    "Windy": {"speed": 1.3, "range": 1.1, "label": "Windy - enemies fast, towers slightly longer range"},
}

def load_sound(name: str):
    """Return a Sound, or a silent dummy if the file is missing."""
    try:
        if os.path.exists(name):
            return pygame.mixer.Sound(name)
        return None
    except Exception:
        return None

def play(sound: pygame.mixer.Sound | None) -> None:
    if sound:
        try: sound.play()
        except Exception: pass

class Enemy:
    def __init__(self, x: float, y: float, hp: int = 100, base_speed: float = 2.0):
        self.x, self.y = x, y
        self.max_hp = hp
        self.hp = hp
        self.base_speed = base_speed
        self.size = 20

    @property
    def cx(self): return self.x + self.size / 2
    @property
    def cy(self): return self.y + self.size / 2

    def move(self, speed_mult: float) -> None:
        self.x += self.base_speed * speed_mult

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
        # HP bar
        w = self.size
        pygame.draw.rect(screen, GRAY, (self.x, self.y - 8, w, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 8, w * max(0, self.hp / self.max_hp), 5))

class Tower:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y
        self.base_range = 100
        self.damage = 10
        self.level = 1
        self.cooldown = 0  # frames until it can shoot again

    def upgrade_cost(self):
        return UPGRADE_COST * self.level

    def upgrade(self):
        self.level += 1
        self.base_range += 10
        self.damage += 5

    def range(self, range_mult: float) -> float:
        return self.base_range * range_mult

    def draw(self, screen: pygame.Surface, range_mult: float, selected: bool = False) -> None:
        r = int(self.range(range_mult))
        pygame.draw.circle(screen, GREEN, (self.x, self.y), r, 1 if not selected else 2)
        pygame.draw.rect(screen, GREEN, (self.x - 10, self.y - 10, 20, 20))
        # level pips
        for i in range(self.level):
            pygame.draw.rect(screen, YELLOW, (self.x - 10 + i * 6, self.y + 14, 4, 4))

class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tower Defense - Merged")
        self.font = pygame.font.Font(None, 30)
        self.small = pygame.font.Font(None, 22)
        self.clock = pygame.time.Clock()

        self.enemy_sound = load_sound('enemy_sound.wav')
        self.tower_sound = load_sound('tower_sound.wav')
        self.score_sound = load_sound('score_sound.wav')
        self.upgrade_sound = load_sound('tower_sound.wav')
        try:
            if os.path.exists('background_music.mp3'):
                pygame.mixer.music.load('background_music.mp3')
                pygame.mixer.music.play(-1)
        except Exception:
            pass

        self.reset()

    def reset(self):
        self.enemies: list[Enemy] = []
        self.towers: list[Tower] = []
        self.score = 0
        self.money = START_MONEY
        self.multiplier = 1.0
        self.weather = "Sunny"
        self.weather_timer = 0
        self.spawn_timer = 0
        self.wave = 1
        self.paused = False
        self.chat_messages: list[str] = []
        self.chat_input = ""
        self.typing = False
        self.message = "Left-click: place tower (50g) | Right-click tower: upgrade | T: chat | P: pause | R: restart"

    # --- helpers ---
    def tower_at(self, pos: tuple[float, float]) -> Tower | None:
        for t in self.towers:
            if math.hypot(t.x - pos[0], t.y - pos[1]) < 20:
                return t
        return None

    def send_chat(self):
        text = self.chat_input.strip()
        if text:
            self.chat_messages.append(f"Player: {text}")
            self.chat_messages = self.chat_messages[-5:]
        self.chat_input = ""
        self.typing = False

    # --- main loop ---
    def run(self):
        while True:
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_RETURN:
                        self.send_chat()
                    elif event.key == pygame.K_ESCAPE:
                        self.typing = False; self.chat_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.chat_input = self.chat_input[:-1]
                    elif event.unicode and len(self.chat_input) < 60:
                        self.chat_input += event.unicode
                    continue
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_t:
                    self.typing = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.typing:
                    continue
                if event.button == 1:  # place tower
                    if self.money < TOWER_COST:
                        self.message = "Not enough money! Need 50g."
                        continue
                    if self.tower_at(event.pos):
                        self.message = "Already a tower there!"
                        continue
                    self.towers.append(Tower(*event.pos))
                    self.money -= TOWER_COST
                    play(self.tower_sound)
                    self.message = f"Tower placed (-{TOWER_COST}g)"
                elif event.button == 3:  # upgrade
                    t = self.tower_at(event.pos)
                    if t:
                        cost = t.upgrade_cost()
                        if self.money < cost:
                            self.message = f"Upgrade costs {cost}g - not enough money!"
                        else:
                            self.money -= cost
                            t.upgrade()
                            play(self.upgrade_sound)
                            self.message = f"Tower upgraded to Lv.{t.level} (-{cost}g)"

    def update(self):
        # --- weather: change every ~8 seconds ---
        self.weather_timer += 1
        if self.weather_timer > 60 * 8:
            self.weather_timer = 0
            self.weather = random.choice(list(WEATHER.keys()))
            self.message = WEATHER[self.weather]["label"]
        speed_mult = WEATHER[self.weather]["speed"]
        range_mult = WEATHER[self.weather]["range"]

        # --- spawn: gets faster / tankier each wave ---
        self.spawn_timer += 1
        spawn_every = max(20, 60 - self.wave * 3)
        if self.spawn_timer >= spawn_every:
            self.spawn_timer = 0
            hp = 100 + (self.wave - 1) * 20
            speed = 2.0 + min(1.5, (self.wave - 1) * 0.1)
            self.enemies.append(Enemy(0, random.randint(0, HEIGHT - 40), hp=hp, base_speed=speed))
            play(self.enemy_sound)

        # --- move enemies, handle escapes (iterate over a copy) ---
        for e in self.enemies[:]:
            e.move(speed_mult)
            if e.x > WIDTH:
                self.enemies.remove(e)
                self.score -= ESCAPE_PENALTY
                self.multiplier = max(1.0, self.multiplier - 0.1)  # escaping resets some bonus
                self.message = f"Enemy escaped! -{ESCAPE_PENALTY} score"

        # --- towers shoot: one target, with cooldown ---
        for t in self.towers:
            if t.cooldown > 0:
                t.cooldown -= 1
                continue
            target = None
            for e in self.enemies:
                if math.hypot(t.x - e.cx, t.y - e.cy) < t.range(range_mult):
                    target = e
                    break
            if target:
                target.hp -= t.damage
                t.cooldown = 15  # ~4 shots/sec
                if target.hp <= 0:
                    if target in self.enemies:
                        self.enemies.remove(target)
                    reward = int(KILL_REWARD * self.multiplier)
                    self.score += reward
                    self.money += reward
                    self.multiplier = round(self.multiplier + 0.1, 1)
                    play(self.score_sound)

        # --- wave: every 15 kills, next wave ---
        # (simple: wave = kills-based via score threshold)
        self.wave = 1 + (self.score // 150)

    def draw(self):
        s = self.screen
        s.fill(WHITE)
        for e in self.enemies: e.draw(s)
        for t in self.towers:
            sel = False
            t.draw(s, WEATHER[self.weather]["range"], selected=sel)

        lines = [
            f"Score: {int(self.score)}",
            f"Money: {int(self.money)}g",
            f"Weather: {self.weather}",
            f"Multiplier: {self.multiplier:.1f}x",
            f"Wave: {self.wave}  |  Towers: {len(self.towers)}  |  Enemies: {len(self.enemies)}",
        ]
        y = 10
        for line in lines:
            s.blit(self.font.render(line, True, BLACK), (10, y)); y += 30

        # status message
        s.blit(self.small.render(self.message, True, DARK), (10, y + 4)); y += 26

        # chat
        cy = y + 8
        for msg in self.chat_messages:
            s.blit(self.small.render(msg, True, BLACK), (10, cy)); cy += 22
        if self.typing:
            s.blit(self.small.render(f"> {self.chat_input}_", True, BLUE), (10, cy))
        else:
            s.blit(self.small.render("Press T to chat | P pause | R restart", True, GRAY), (10, cy))

        if self.paused:
            overlay = self.font.render("PAUSED - press P to resume", True, RED)
            s.blit(overlay, (WIDTH // 2 - 180, HEIGHT // 2))

        # controls footer
        s.blit(self.small.render("Left-click: place (50g)  |  Right-click tower: upgrade  |  Towers shoot nearest in range", True, GRAY), (10, HEIGHT - 24))

if __name__ == "__main__":
    Game().run()
