import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 0, 255, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Bubble:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 20

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Shooter:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT - 50
        self.speed = 5
        self.score = 0

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH:
            self.x = WIDTH

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x - 20, self.y, 40, 20))

def main():
    clock = pygame.time.Clock()
    shooter = Shooter()
    bubbles = [Bubble(random.randint(0, WIDTH), random.randint(0, HEIGHT / 2), random.choice([RED, GREEN, BLUE])) for _ in range(10)]
    shot_bubble = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and shot_bubble is None:
                    shot_bubble = Bubble(shooter.x, shooter.y, random.choice([RED, GREEN, BLUE]))
                    shot_bubble.speed_y = -5

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            shooter.move(-shooter.speed)
        if keys[pygame.K_RIGHT]:
            shooter.move(shooter.speed)

        screen.fill((0, 0, 0))
        shooter.draw()
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {shooter.score}", True, WHITE)
        screen.blit(text, (10, 10))

        for bubble in bubbles[:]:
            bubble.draw()
            if bubble.y > HEIGHT:
                bubbles.remove(bubble)
                shooter.score -= 10

        if shot_bubble:
            shot_bubble.y += shot_bubble.speed_y
            pygame.draw.circle(screen, shot_bubble.color, (shot_bubble.x, shot_bubble.y), shot_bubble.radius)
            if shot_bubble.y < 0:
                shot_bubble = None
            for bubble in bubbles[:]:
                if ((shot_bubble.x - bubble.x) ** 2 + (shot_bubble.y - bubble.y) ** 2) ** 0.5 < shot_bubble.radius + bubble.radius:
                    if shot_bubble.color == bubble.color:
                        bubbles.remove(bubble)
                        shot_bubble = None
                        shooter.score += 10
                    else:
                        bubbles.append(Bubble(shot_bubble.x, shot_bubble.y, shot_bubble.color))
                        shot_bubble = None

        if random.random() < 0.05:
            bubbles.append(Bubble(random.randint(0, WIDTH), 0, random.choice([RED, GREEN, BLUE])))

        for bubble in bubbles:
            bubble.y += 2

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()