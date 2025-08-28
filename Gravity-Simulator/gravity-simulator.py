import pygame
import math
import random

# Constants
G = 0.1  # Gravity constant
WIDTH, HEIGHT = 800, 600

class Planet:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)

    def apply_gravity(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return
        force = G * self.mass * other.mass / dist**2
        angle = math.atan2(dy, dx)
        self.vel_x += force * math.cos(angle) / self.mass
        self.vel_y += force * math.sin(angle) / self.mass

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Boundary checking
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vel_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vel_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    planets = [
        Planet(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(10, 100), random.randint(5, 20), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) for _ in range(10)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i in range(len(planets)):
            for j in range(i+1, len(planets)):
                planets[i].apply_gravity(planets[j])
                planets[j].apply_gravity(planets[i])

        for planet in planets:
            planet.update()
            planet.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()