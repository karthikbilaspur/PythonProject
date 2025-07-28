import pygame

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Paddle(pygame.Rect):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT - 20, 100, 20)
        self.speed = 5

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

class Ball(pygame.Rect):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT / 2, 20, 20)
        self.speed_x = 5
        self.speed_y = -5

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x < 0 or self.x > WIDTH - self.width:
            self.speed_x *= -1
        if self.y < 0:
            self.speed_y *= -1

class Brick(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30)
        self.health = 2

    def hit(self):
        self.health -= 1

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = [Brick(10 + i * 90, 10 + j * 40) for i in range(8) for j in range(5)]
    score = 0
    lives = 3

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-paddle.speed)
        if keys[pygame.K_RIGHT]:
            paddle.move(paddle.speed)

        ball.move()
        if ball.colliderect(paddle):
            ball.speed_y *= -1
        for brick in bricks[:]:
            if ball.colliderect(brick):
                ball.speed_y *= -1
                brick.hit()
                if brick.health <= 0:
                    bricks.remove(brick)
                    score += 10

        if ball.y > HEIGHT:
            lives -= 1
            ball.x = WIDTH / 2
            ball.y = HEIGHT / 2
            ball.speed_y *= -1
            if lives <= 0:
                print("Game Over! Final Score:", score)
                running = False

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        for brick in bricks:
            pygame.draw.rect(screen, GREEN if brick.health > 1 else RED, brick)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}, Lives: {lives}", True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()