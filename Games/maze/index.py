import pygame
import random
from collections import deque

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (50, 100, 255)
YELLOW = (255, 220, 0)

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = False
        # top, right, bottom, left
        self.walls = [True, True, True, True]

class Maze:
    def __init__(self):
        self.cells = [[Cell(x, y) for y in range(ROWS)] for x in range(COLS)]
        self.generate_maze()
        self.surface = self.render_to_surface()

    def generate_maze(self):
        stack = [self.cells[0][0]]
        self.cells[0][0].visited = True

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                nxt = random.choice(neighbors)
                self.remove_wall(current, nxt)
                nxt.visited = True
                stack.append(nxt)
            else:
                stack.pop()

    def get_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        x, y = cell.x, cell.y
        if x > 0 and not self.cells[x - 1][y].visited:
            neighbors.append(self.cells[x - 1][y])
        if x < COLS - 1 and not self.cells[x + 1][y].visited:
            neighbors.append(self.cells[x + 1][y])
        if y > 0 and not self.cells[x][y - 1].visited:
            neighbors.append(self.cells[x][y - 1])
        if y < ROWS - 1 and not self.cells[x][y + 1].visited:
            neighbors.append(self.cells[x][y + 1])
        return neighbors

    def remove_wall(self, c1: Cell, c2: Cell) -> None:
        dx, dy = c2.x - c1.x, c2.y - c1.y
        if dx == 1:   # c2 is right of c1
            c1.walls[1] = c2.walls[3] = False
        elif dx == -1: # c2 is left
            c1.walls[3] = c2.walls[1] = False
        elif dy == 1:  # c2 is below
            c1.walls[2] = c2.walls[0] = False
        elif dy == -1: # c2 is above
            c1.walls[0] = c2.walls[2] = False

    def render_to_surface(self) -> pygame.Surface:
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill(WHITE)
        for x in range(COLS):
            for y in range(ROWS):
                cell = self.cells[x][y]
                px, py = x * CELL_SIZE, y * CELL_SIZE
                if cell.walls[0]:
                    pygame.draw.line(surf, BLACK, (px, py), (px + CELL_SIZE, py), 2)
                if cell.walls[1]:
                    pygame.draw.line(surf, BLACK, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE), 2)
                if cell.walls[2]:
                    pygame.draw.line(surf, BLACK, (px, py + CELL_SIZE), (px + CELL_SIZE, py + CELL_SIZE), 2)
                if cell.walls[3]:
                    pygame.draw.line(surf, BLACK, (px, py), (px, py + CELL_SIZE), 2)
        return surf

    def solve_bfs(self, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """Returns list of (x, y) from start to goal."""
        queue: deque[tuple[int, int]] = deque([start])
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        while queue:
            cur = queue.popleft()
            if cur == goal:
                break
            x, y = cur
            cell = self.cells[x][y]
            # (dx, dy, wall_index)
            for dx, dy, wall in [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]:
                if not cell.walls[wall]:
                    nxt = (x + dx, y + dy)
                    if nxt not in came_from:
                        came_from[nxt] = cur
                        queue.append(nxt)
        # Reconstruct path
        path: list[tuple[int, int]] = []
        cur: tuple[int, int] | None = goal
        while cur is not None:
            path.append(cur)
            cur = came_from.get(cur)
        return path[::-1]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze - Arrow keys / WASD to move, R = new maze, H = hint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    maze = Maze()
    player_pos = [0, 0]
    goal = (COLS - 1, ROWS - 1)
    moves = 0
    start_time = pygame.time.get_ticks()
    won = False
    show_hint = False
    hint_path = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and not won:
                dx, dy, wall = 0, 0, None
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    dx, wall = -1, 3
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    dx, wall = 1, 1
                elif event.key in (pygame.K_UP, pygame.K_w):
                    dy, wall = -1, 0
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    dy, wall = 1, 2
                elif event.key == pygame.K_r:
                    maze = Maze()
                    player_pos = [0, 0]
                    moves = 0
                    start_time = pygame.time.get_ticks()
                    show_hint = False
                elif event.key == pygame.K_h:
                    show_hint = not show_hint
                    if show_hint:
                        hint_path = maze.solve_bfs(tuple(player_pos), goal)

                if wall is not None:
                    x, y = player_pos
                    if not maze.cells[x][y].walls[wall]:
                        player_pos[0] += dx
                        player_pos[1] += dy
                        moves += 1
                        show_hint = False
                        if tuple(player_pos) == goal:
                            won = True

            elif event.type == pygame.KEYDOWN and won:
                if event.key == pygame.K_r:
                    maze = Maze()
                    player_pos = [0, 0]
                    moves = 0
                    start_time = pygame.time.get_ticks()
                    won = False
                    show_hint = False

        # Draw
        screen.blit(maze.surface, (0, 0))

        # Goal
        gx, gy = goal
        pygame.draw.rect(screen, GREEN, (gx * CELL_SIZE + 2, gy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))

        # Hint path
        if show_hint and hint_path:
            for hx, hy in hint_path[1:]:
                pygame.draw.circle(screen, YELLOW, (hx * CELL_SIZE + CELL_SIZE // 2, hy * CELL_SIZE + CELL_SIZE // 2), 3)

        # Player
        pygame.draw.rect(screen, RED, (player_pos[0] * CELL_SIZE + 5, player_pos[1] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))

        # HUD
        elapsed = 0 if won else (pygame.time.get_ticks() - start_time) // 1000
        if won:
            elapsed = (pygame.time.get_ticks() - start_time) // 1000  # freeze? use stored time instead
        hud = font.render(f"Moves: {moves}  Time: {elapsed}s  |  R: New Maze  H: Hint", True, BLACK)
        # HUD background so it doesn't get hidden by walls
        pygame.draw.rect(screen, WHITE, (0, 0, hud.get_width() + 10, 30))
        screen.blit(hud, (5, 5))

        if won:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            msg = font.render(f"You escaped in {moves} moves! Press R to play again.", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()