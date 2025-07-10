import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
TRACK_RADIUS = 200
PLAYER_SIZE = 10
SPEED = 2
POWER_UP_SIZE = 10

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.trail = []
        self.angle = 0
        self.speed = SPEED
        self.score = 0
        self.power_up = False

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.trail.append((self.x, self.y))

    def turn(self, direction):
        if direction == 'left':
            self.angle -= 0.1
        elif direction == 'right':
            self.angle += 0.1

class PowerUp:
    def __init__(self):
        self.x = random.uniform(WIDTH / 2 - TRACK_RADIUS, WIDTH / 2 + TRACK_RADIUS)
        self.y = random.uniform(HEIGHT / 2 - TRACK_RADIUS, HEIGHT / 2 + TRACK_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), POWER_UP_SIZE)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.player1 = Player(WIDTH / 2 + TRACK_RADIUS, HEIGHT / 2, RED)
        self.player2 = Player(WIDTH / 2 - TRACK_RADIUS, HEIGHT / 2, BLUE)
        self.power_up = PowerUp()
        self.running = True

    def draw(self):
        self.screen.fill(WHITE)
        pygame.draw.circle(self.screen, (0, 0, 0), (WIDTH // 2, HEIGHT // 2), TRACK_RADIUS, 1)
        for player in [self.player1, self.player2]:
            for pos in player.trail:
                pygame.draw.circle(self.screen, player.color, (int(pos[0]), int(pos[1])), 2)
            pygame.draw.circle(self.screen, player.color, (int(player.x), int(player.y)), PLAYER_SIZE)
        self.power_up.draw(self.screen)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.player1.score} - {self.player2.score}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player1.turn('left')
        if keys[pygame.K_s]:
            self.player1.turn('right')
        if keys[pygame.K_UP]:
            self.player2.turn('left')
        if keys[pygame.K_DOWN]:
            self.player2.turn('right')
        self.player1.move()
        self.player2.move()

        # Check for collisions
        for player in [self.player1, self.player2]:
            if math.hypot(player.x - WIDTH / 2, player.y - HEIGHT / 2) > TRACK_RADIUS:
                if player == self.player1:
                    self.player2.score += 1
                else:
                    self.player1.score += 1
                self.reset_game()
            for other_player in [self.player1, self.player2]:
                if other_player != player:
                    for pos in other_player.trail:
                        if math.hypot(player.x - pos[0], player.y - pos[1]) < PLAYER_SIZE:
                            if player == self.player1:
                                self.player2.score += 1
                            else:
                                self.player1.score += 1
                            self.reset_game()

        # Check for power-up collision
        for player in [self.player1, self.player2]:
            if math.hypot(player.x - self.power_up.x, player.y - self.power_up.y) < PLAYER_SIZE + POWER_UP_SIZE:
                player.power_up = True
                self.power_up = PowerUp()

        # Apply power-up effect
        for player in [self.player1, self.player2]:
            if player.power_up:
                player.speed = SPEED * 2
                player.power_up = False
            else:
                player.speed = SPEED

    def reset_game(self):
        self.player1.x = WIDTH / 2 + TRACK_RADIUS
        self.player1.y = HEIGHT / 2
        self.player1.angle = 0
        self.player1.tandem = False
        self.player2.x = WIDTH / 2 - TRACK_RADIUS
        self.player2.y = HEIGHT / 2
        self.player2.angle = 0
        self.player2.tandem = False
        self.player1.trail = []
        self.player2.trail = []
        self.power_up = PowerUp()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()