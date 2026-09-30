import pygame
import sys
import random
import numpy as np
from dataclasses import dataclass

# --- Config ---
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_GAP = 120
PIPE_WIDTH = 52
FPS = 60

@dataclass
class Config:
    bird_color: tuple = (255, 255, 0)
    pipe_color: tuple = (50, 205, 50)
    bg_color: tuple = (135, 206, 235)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.size = 24
        self.vel = 0

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        # floor / ceiling collision
        if self.y < 0:
            self.y = 0
            self.vel = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(80, 300)
        self.passed = False

    def update(self):
        self.x -= 2

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

    def collides_with(self, bird: Bird):
        bird_rect = bird.rect()
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.y)
        bottom_rect = pygame.Rect(self.x, self.y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

class NeuralNetwork:
    """Simple 3-input -> 1-output network for demo. Random, not trained."""
    def __init__(self):
        self.weights = np.random.randn(3)
        self.bias = np.random.randn()

    def should_flap(self, bird_y_norm, pipe_x_norm, pipe_y_norm):
        inputs = np.array([bird_y_norm, pipe_x_norm, pipe_y_norm])
        # sigmoid
        z = np.dot(inputs, self.weights) + self.bias
        return 1 / (1 + np.exp(-z)) > 0.5

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    bird = Bird()
    pipes = [Pipe(300)]
    score = 0
    high_score = 0
    game_active = True
    use_ai = False
    nn = NeuralNetwork()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.flap()
                if event.key == pygame.K_a: # Toggle AI
                    use_ai = not use_ai

        # --- Game Logic ---
        if game_active:
            bird.update()

            # AI control
            if use_ai and pipes:
                closest = pipes[0]
                inputs = (
                    bird.y / SCREEN_HEIGHT,
                    closest.x / SCREEN_WIDTH,
                    closest.y / SCREEN_HEIGHT
                )
                if nn.should_flap(*inputs):
                    bird.flap()

            # Pipes
            for p in pipes:
                p.update()
                if p.collides_with(bird) or bird.y + bird.size > 450:
                    game_active = False

                if not p.passed and p.x < bird.x:
                    p.passed = True
                    score += 1

            pipes = [p for p in pipes if not p.is_off_screen()]
            if not pipes or pipes[-1].x < SCREEN_WIDTH - 150:
                pipes.append(Pipe(SCREEN_WIDTH))

            # Floor hit
            if bird.y + bird.size >= 450:
                game_active = False

        else: # Game Over
            high_score = max(high_score, score)
            pygame.time.wait(800)
            # reset
            bird = Bird()
            pipes = [Pipe(300)]
            score = 0
            game_active = True

        # --- Draw ---
        screen.fill(Config.bg_color)
        for p in pipes:
            pygame.draw.rect(screen, Config.pipe_color, (p.x, 0, PIPE_WIDTH, p.y))
            pygame.draw.rect(screen, Config.pipe_color, (p.x, p.y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - p.y - PIPE_GAP))

        pygame.draw.rect(screen, Config.bird_color, bird.rect())
        pygame.draw.rect(screen, (225, 215, 188), (0, 450, SCREEN_WIDTH, 62))

        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10, 10))
        mode_text = font.render(f"{'AI' if use_ai else 'HUMAN'} [A to toggle] [SPACE to flap]", True, (0,0,0))
        screen.blit(mode_text, (10, SCREEN_HEIGHT - 25))

        if not game_active:
            over = font.render(f"Game Over! High: {high_score}", True, (255,0,0))
            screen.blit(over, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()