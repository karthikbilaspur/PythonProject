import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up display variables
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FPS = 10

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up font
FONT = pygame.font.Font(None, 36)

class SnakeGame:
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.apple = self.generate_apple()
        self.obstacles = self.generate_obstacles()

    def generate_apple(self):
        return (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

    def generate_obstacles(self):
        obstacles = []
        for _ in range(10):
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            if (x, y) not in self.snake and (x, y) != self.apple:
                obstacles.append((x, y))
        return obstacles

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.direction = 'RIGHT'

            head = self.snake[-1]
            if self.direction == 'UP':
                new_head = (head[0], head[1] - BLOCK_SIZE)
            elif self.direction == 'DOWN':
                new_head = (head[0], head[1] + BLOCK_SIZE)
            elif self.direction == 'LEFT':
                new_head = (head[0] - BLOCK_SIZE, head[1])
            elif self.direction == 'RIGHT':
                new_head = (head[0] + BLOCK_SIZE, head[1])

            self.snake.append(new_head)
            if self.snake[-1] == self.apple:
                self.apple = self.generate_apple()
            else:
                self.snake.pop(0)

            if (self.snake[-1][0] < 0 or self.snake[-1][0] >= WIDTH or
                    self.snake[-1][1] < 0 or self.snake[-1][1] >= HEIGHT or
                    self.snake[-1] in self.snake[:-1] or
                    self.snake[-1] in self.obstacles):
                print("Game Over!")
                pygame.quit()
                sys.exit()

            self.display.fill(BLACK)
            for pos in self.snake:
                pygame.draw.rect(self.display, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, RED, (self.apple[0], self.apple[1], BLOCK_SIZE, BLOCK_SIZE))
            for obstacle in self.obstacles:
                pygame.draw.rect(self.display, BLUE, (obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE))
            text = FONT.render(f'Score: {len(self.snake)}', True, WHITE)
            self.display.blit(text, (10, 10))
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = SnakeGame()
    game.play()