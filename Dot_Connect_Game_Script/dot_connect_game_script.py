import pygame
import sys
import random
import json

# Constants
WIDTH, HEIGHT = 800, 600
DOT_RADIUS = 10
LINE_WIDTH = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, x, y):
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5

    def to_dict(self):
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data):
        return cls(data["x"], data["y"])

def save_lines(lines, filename):
    data = []
    for line in lines:
        data.append({"start": line[0].to_dict(), "end": line[1].to_dict()})
    with open(filename, "w") as f:
        json.dump(data, f)

def load_lines(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            lines = []
            for line_data in data:
                start_dot = Dot.from_dict(line_data["start"])
                end_dot = Dot.from_dict(line_data["end"])
                lines.append((start_dot, end_dot))
            return lines
    except FileNotFoundError:
        print("No save file found")
        return []

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    dots = [
        Dot(100, 100),
        Dot(300, 100),
        Dot(500, 100),
        Dot(100, 300),
        Dot(300, 300),
        Dot(500, 300),
        Dot(100, 500),
        Dot(300, 500),
        Dot(500, 500),
    ]

    lines = []
    start_dot = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for dot in dots:
                    if dot.distance_to(*event.pos) < DOT_RADIUS:
                        start_dot = dot
                        break
                else:
                    start_dot = None
            elif event.type == pygame.MOUSEBUTTONUP:
                if start_dot:
                    for dot in dots:
                        if dot.distance_to(*event.pos) < DOT_RADIUS and dot != start_dot:
                            lines.append((start_dot, dot))
                            break
                    start_dot = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lines = []
                elif event.key == pygame.K_s:
                    save_lines(lines, "save.json")
                elif event.key == pygame.K_l:
                    lines = load_lines("save.json")

        screen.fill(WHITE)
        for dot in dots:
            pygame.draw.circle(screen, BLACK, (dot.x, dot.y), DOT_RADIUS)
        for line in lines:
            pygame.draw.line(screen, BLACK, (line[0].x, line[0].y), (line[1].x, line[1].y), LINE_WIDTH)
        if start_dot:
            pygame.draw.line(screen, RED, (start_dot.x, start_dot.y), pygame.mouse.get_pos(), LINE_WIDTH)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()