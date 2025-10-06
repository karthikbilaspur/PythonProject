import pygame
import random
from collections import deque

# Window dimensions
WIDTH, HEIGHT = 800, 600
# Maze dimensions
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True]  # top, right, bottom, left

class Maze:
    def __init__(self):
        self.cells = [[Cell(x, y) for y in range(ROWS)] for x in range(COLS)]
        self.generate_maze()

    def generate_maze(self):
        stack = []
        current = self.cells[0][0]
        current.visited = True
        stack.append(current)

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_wall(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        if cell.x > 0 and not self.cells[cell.x - 1][cell.y].visited:
            neighbors.append(self.cells[cell.x - 1][cell.y])
        if cell.x < COLS - 1 and not self.cells[cell.x + 1][cell.y].visited:
            neighbors.append(self.cells[cell.x + 1][cell.y])
        if cell.y > 0 and not self.cells[cell.x][cell.y - 1].visited:
            neighbors.append(self.cells[cell.x][cell.y - 1])
        if cell.y < ROWS - 1 and not self.cells[cell.x][cell.y + 1].visited:
            neighbors.append(self.cells[cell.x][cell.y + 1])
        return neighbors

    def remove_wall(self, cell1, cell2):
        if cell1.x == cell2.x:  # vertical wall
            if cell1.y < cell2.y:
                cell1.walls[2] = False
                cell2.walls[0] = False
            else:
                cell1.walls[0] = False
                cell2.walls[2] = False
        elif cell1.y == cell2.y:  # horizontal wall
            if cell1.x < cell2.x:
                cell1.walls[1] = False
                cell2.walls[3] = False
            else:
                cell1.walls[3] = False
                cell2.walls[1] = False

def draw_maze(maze, screen):
    screen.fill(WHITE)
    for x in range(COLS):
        for y in range(ROWS):
            cell = maze.cells[x][y]
            if cell.walls[0]:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, y * CELL_SIZE))
            if cell.walls[1]:
                pygame.draw.line(screen, BLACK, ((x + 1) * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
            if cell.walls[2]:
                pygame.draw.line(screen, BLACK, ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), (x * CELL_SIZE, (y + 1) * CELL_SIZE))
            if cell.walls[3]:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, (y + 1) * CELL_SIZE), (x * CELL_SIZE, y * CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    maze = Maze()
    player_pos = [0, 0]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if player_pos[0] > 0 and not maze.cells[player_pos[0]][player_pos[1]].walls[3]:
                        player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if player_pos[0] < COLS - 1 and not maze.cells[player_pos[0]][player_pos[1]].walls[1]:
                        player_pos[0] += 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if player_pos[1] > 0 and not maze.cells[player_pos[0]][player_pos[1]].walls[0]:
                        player_pos[1] -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if player_pos[1] < ROWS - 1 and not maze.cells[player_pos[0]][player_pos[1]].walls[2]:
                        player_pos[1] += 1
                elif event.key == pygame.K_r:
                    maze = Maze()
                    player_pos = [0, 0]

        draw_maze(maze, screen)
        pygame.draw.rect(screen, RED, (player_pos[0] * CELL_SIZE + CELL_SIZE // 4, player_pos[1] * CELL_SIZE + CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()