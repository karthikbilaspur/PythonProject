import random
import time
import os

# Constants
GRID_SIZE = 20
NUM_ORGANISMS = 10
NUM_RESOURCES = 20
ENERGY_THRESHOLD = 5

# Rules dictionary
RULES = {
    'low_energy': lambda energy: random.choice(['move_left', 'stay']),
    'medium_energy': lambda energy: 'reproduce' if energy > ENERGY_THRESHOLD / 2 else 'move_right',
    'high_energy': lambda energy: 'reproduce' if energy >= ENERGY_THRESHOLD else 'move_right'
}

class Organism:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def apply_rule(self):
        if self.energy < ENERGY_THRESHOLD / 3:
            return RULES['low_energy'](self.energy)
        elif self.energy < ENERGY_THRESHOLD:
            return RULES['medium_energy'](self.energy)
        else:
            return RULES['high_energy'](self.energy)

    def move_left(self, grid):
        if self.x > 0 and grid[self.y][self.x - 1] is None:
            grid[self.y][self.x] = None
            self.x -= 1
            grid[self.y][self.x] = self

    def move_right(self, grid):
        if self.x < GRID_SIZE - 1 and grid[self.y][self.x + 1] is None:
            grid[self.y][self.x] = None
            self.x += 1
            grid[self.y][self.x] = self

    def reproduce(self, grid):
        if self.energy >= ENERGY_THRESHOLD:
            self.energy -= ENERGY_THRESHOLD
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and grid[new_y][new_x] is None:
                    new_organism = Organism(new_x, new_y, ENERGY_THRESHOLD / 2)
                    grid[new_y][new_x] = new_organism
                    break

def initialize_grid():
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    organisms = []
    resources = []
    for _ in range(NUM_ORGANISMS):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        organism = Organism(x, y, random.randint(1, ENERGY_THRESHOLD))
        grid[y][x] = organism
        organisms.append(organism)
    for _ in range(NUM_RESOURCES):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[y][x] is None:
            resources.append((x, y))
    return grid, organisms, resources

def simulate(grid, organisms, resources):
    iterations = 100
    for i in range(iterations):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Iteration {i+1}")
        for row in grid:
            print(' '.join(['O' if cell else '.' for cell in row]))
        print()
        for organism in organisms:
            action = organism.apply_rule()
            if action == 'move_left':
                organism.move_left(grid)
            elif action == 'move_right':
                organism.move_right(grid)
            elif action == 'reproduce':
                organism.reproduce(grid)
            organism.energy += 0.1  # Gradually increase energy over time
        time.sleep(0.5)

grid, organisms, resources = initialize_grid()
simulate(grid, organisms, resources)