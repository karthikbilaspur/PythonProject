import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 50
TRACK_WIDTH = 200
FINISH_LINE = 700
MAX_SPEED = 10
ACCELERATION = 0.5
BRAKING = 1.5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Car:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.speed = 0
        self.color = color

    def accelerate(self, amount):
        self.speed = min(self.speed + amount, MAX_SPEED)

    def decelerate(self, amount):
        self.speed = max(self.speed - amount, 0)

    def brake(self, amount):
        self.speed = max(self.speed - amount, 0)

def draw_text(screen, font, text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    car1 = Car(100, HEIGHT // 2 - CAR_HEIGHT // 2, RED)
    car2 = Car(100, HEIGHT // 2 + CAR_HEIGHT // 2 + 20, BLUE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            car1.accelerate(ACCELERATION)
        if keys[pygame.K_LSHIFT]:
            car1.brake(BRAKING)
        if not keys[pygame.K_SPACE] and not keys[pygame.K_LSHIFT]:
            car1.decelerate(ACCELERATION)

        car2.accelerate(random.uniform(0, ACCELERATION))
        if random.random() < 0.1:
            car2.brake(random.uniform(0, BRAKING))

        car1.x += car1.speed
        car2.x += car2.speed

        screen.fill(WHITE)
        pygame.draw.rect(screen, car1.color, (int(car1.x), car1.y, CAR_WIDTH, CAR_HEIGHT))
        pygame.draw.rect(screen, car2.color, (int(car2.x), car2.y, CAR_WIDTH, CAR_HEIGHT))
        pygame.draw.line(screen, (0, 0, 0), (FINISH_LINE, 0), (FINISH_LINE, HEIGHT), 5)
        draw_text(screen, font, f"Speed: {int(car1.speed)}", 10, 10)

        if car1.x > FINISH_LINE:
            draw_text(screen, font, "You win!", WIDTH // 2 - 50, HEIGHT // 2 - 18)
            pygame.display.flip()
            pygame.time.wait(2000)
            break
        elif car2.x > FINISH_LINE:
            draw_text(screen, font, "Computer wins!", WIDTH // 2 - 75, HEIGHT // 2 - 18)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            break

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()