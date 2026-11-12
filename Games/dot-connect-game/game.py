import pygame
import sys
import random
import json
import math
from typing import Any
from dataclasses import dataclass, asdict

# --- Config ---
WIDTH, HEIGHT = 900, 650
TOP_BAR = 48
DOT_RADIUS = 12
HOVER_RADIUS = 18
LINE_WIDTH = 3

# --- Colors ---
WHITE: tuple[int, int, int] = (255, 255, 255)
BG: tuple[int, int, int] = (248, 249, 251)
BLACK: tuple[int, int, int] = (30, 30, 30)
GRAY: tuple[int, int, int] = (180, 180, 180)
RED: tuple[int, int, int] = (231, 76, 60)
GREEN: tuple[int, int, int] = (46, 204, 113)
BLUE: tuple[int, int, int] = (52, 152, 219)
ORANGE: tuple[int, int, int] = (230, 126, 34)
PURPLE: tuple[int, int, int] = (155, 89, 182)
PALETTE: list[tuple[int, int, int]] = [BLACK, RED, GREEN, BLUE, ORANGE, PURPLE]
PALETTE_NAMES: list[str] = ["Black", "Red", "Green", "Blue", "Orange", "Purple"]

SAVE_FILE = "save.json"

@dataclass
class Dot:
    x: float
    y: float
    r: int = DOT_RADIUS

    def distance_to(self, x: float, y: float) -> float:
        return math.hypot(self.x - x, self.y - y)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Dot":
        return cls(data["x"], data["y"])

@dataclass
class Line:
    start_idx: int
    end_idx: int
    color: tuple[int, int, int] = BLACK
    width: int = LINE_WIDTH

    def to_dict(self) -> dict[str, Any]:
        return {"start": self.start_idx, "end": self.end_idx,
                "color": list(self.color), "width": self.width}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Line":
        return cls(data["start"], data["end"],
                   tuple(data.get("color", BLACK)), data.get("width", LINE_WIDTH))

def generate_dots(mode: str, n: int = 9) -> list[Dot]:
    """Generate a layout of dots."""
    dots: list[Dot] = []
    if mode == "grid":
        cols, rows = 3, 3
        for r in range(rows):
            for c in range(cols):
                dots.append(Dot(150 + c * 250, 150 + r * 200))
    elif mode == "circle":
        cx, cy, rad = WIDTH // 2, (HEIGHT + TOP_BAR) // 2, 220
        for i in range(10):
            a = 2 * math.pi * i / 10 - math.pi / 2
            dots.append(Dot(cx + rad * math.cos(a), cy + rad * math.sin(a)))
    elif mode == "random":
        attempts = 0
        while len(dots) < n and attempts < 500:
            attempts += 1
            x = random.randint(60, WIDTH - 60)
            y = random.randint(TOP_BAR + 60, HEIGHT - 60)
            if all(d.distance_to(x, y) > 70 for d in dots):
                dots.append(Dot(x, y))
    return dots

def save_state(dots: list[Dot], lines: list[Line], filename: str = SAVE_FILE) -> None:
    data = {
        "dots": [d.to_dict() for d in dots],
        "lines": [l.to_dict() for l in lines],
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(dots)} dots, {len(lines)} lines -> {filename}")

def load_state(filename: str = SAVE_FILE) -> tuple[list[Dot] | None, list[Line] | None]:
    try:
        with open(filename) as f:
            data = json.load(f)
        dots = [Dot.from_dict(d) for d in data.get("dots", [])]
        lines = [Line.from_dict(l) for l in data.get("lines", [])]
        print(f"Loaded {len(dots)} dots, {len(lines)} lines")
        return dots, lines
    except FileNotFoundError:
        print("No save file found.")
        return None, None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Save file corrupt: {e}")
        return None, None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect the Dots — Draw, Undo, Save")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Segoe UI", 16)
    small_font = pygame.font.SysFont("Segoe UI", 13)

    dots = generate_dots("grid")
    lines: list[Line] = []
    history: list[Line] = []  # for redo if needed

    start_idx = None
    dragging = False
    hover_idx = None
    color_idx = 0
    add_mode = False
    dragging_dot = None  # move existing dot with Shift+drag

    def find_dot(pos: tuple[int, int], radius: float = HOVER_RADIUS) -> int | None:
        for i, d in enumerate(dots):
            if d.distance_to(*pos) < radius:
                return i
        return None

    def find_line(pos: tuple[int, int], thresh: float = 6) -> int | None:
        """Find line near mouse for right-click delete."""
        mx, my = pos
        for i in reversed(range(len(lines))):
            a, b = dots[lines[i].start_idx], dots[lines[i].end_idx]
            # distance point-to-segment
            dx, dy = b.x - a.x, b.y - a.y
            if dx == 0 and dy == 0:
                continue
            t = max(0, min(1, ((mx - a.x) * dx + (my - a.y) * dy) / (dx*dx + dy*dy)))
            px, py = a.x + t*dx, a.y + t*dy
            if math.hypot(mx - px, my - py) < thresh:
                return i
        return None

    def add_line(a: int, b: int) -> None:
        if a == b:
            return
        # prevent duplicates (both directions)
        for l in lines:
            if {l.start_idx, l.end_idx} == {a, b}:
                return
        lines.append(Line(a, b, PALETTE[color_idx]))
        history.clear()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                hover_idx = find_dot(event.pos)
                if dragging_dot is not None:
                    dots[dragging_dot].x, dots[dragging_dot].y = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Right click: delete line under cursor
                if event.button == 3:
                    idx = find_line(event.pos)
                    if idx is not None:
                        lines.pop(idx)
                    continue

                # Shift+drag: move a dot
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    dragging_dot = find_dot(event.pos)
                    continue

                # Add-dot mode
                if add_mode:
                    if event.pos[1] > TOP_BAR:
                        dots.append(Dot(*event.pos))
                    continue

                # Normal: start drawing
                idx = find_dot(event.pos)
                if idx is not None:
                    start_idx = idx
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_dot = None
                    if dragging and start_idx is not None:
                        end_idx = find_dot(event.pos)
                        if end_idx is not None:
                            add_line(start_idx, end_idx)
                    start_idx = None
                    dragging = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lines.clear()
                elif event.key == pygame.K_u or (event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if lines:
                        history.append(lines.pop())
                elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if history:
                        lines.append(history.pop())
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_state(dots, lines)
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    d, l = load_state()
                    if d is not None:
                        dots, lines = d, l
                elif event.key == pygame.K_a:
                    add_mode = not add_mode
                    print(f"Add-dot mode: {'ON (click to add)' if add_mode else 'OFF'}")
                elif event.key == pygame.K_1:
                    dots = generate_dots("grid")
                    lines.clear()
                elif event.key == pygame.K_2:
                    dots = generate_dots("random", 12)
                    lines.clear()
                elif event.key == pygame.K_3:
                    dots = generate_dots("circle")
                    lines.clear()
                elif event.key in (pygame.K_c,):
                    color_idx = (color_idx + 1) % len(PALETTE)
                elif pygame.K_4 <= event.key <= pygame.K_9:
                    # 4-9 also cycle colors quickly if you want direct keys
                    pass
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # --- Draw ---
        screen.fill(BG)

        # Top bar
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, TOP_BAR))
        pygame.draw.line(screen, GRAY, (0, TOP_BAR), (WIDTH, TOP_BAR), 1)

        info = f"Lines: {len(lines)}  •  Dots: {len(dots)}  •  Color: {PALETTE_NAMES[color_idx]}"
        screen.blit(font.render(info, True, BLACK), (12, 12))

        help_text = "Drag dot→dot  •  Shift+drag: move dot  •  Right-click line: delete  •  U: undo  •  A: add dot  •  1:Grid 2:Random 3:Circle  •  C: color  •  Ctrl+S / Ctrl+L"
        screen.blit(small_font.render(help_text, True, (100, 100, 100)), (12, TOP_BAR + HEIGHT - 28))

        # Color swatches
        for i, col in enumerate(PALETTE):
            x = WIDTH - 30 * (len(PALETTE) - i) - 10
            rect = pygame.Rect(x, 10, 22, 22)
            pygame.draw.circle(screen, col, rect.center, 11)
            if i == color_idx:
                pygame.draw.circle(screen, BLACK, rect.center, 14, 2)

        # Lines
        for line in lines:
            a, b = dots[line.start_idx], dots[line.end_idx]
            pygame.draw.line(screen, line.color, (a.x, a.y), (b.x, b.y), line.width)

        # Preview line while dragging
        if dragging and start_idx is not None:
            a = dots[start_idx]
            pygame.draw.line(screen, PALETTE[color_idx], (a.x, a.y), mouse_pos, LINE_WIDTH)
            pygame.draw.circle(screen, PALETTE[color_idx], mouse_pos, 5)

        # Dots
        for i, d in enumerate(dots):
            is_hover = (i == hover_idx)
            is_start = (i == start_idx)
            col = RED if is_start else (BLUE if is_hover else BLACK)
            radius = DOT_RADIUS + (3 if is_hover or is_start else 0)
            pygame.draw.circle(screen, WHITE, (int(d.x), int(d.y)), radius + 2)
            pygame.draw.circle(screen, col, (int(d.x), int(d.y)), radius)

        if add_mode:
            screen.blit(font.render("＋ ADD DOT MODE — click anywhere to add a dot (press A to exit)", True, RED), (12, TOP_BAR + 8))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()