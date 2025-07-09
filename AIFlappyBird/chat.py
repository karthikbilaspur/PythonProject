import pygame
import sys
import random
import numpy as np

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
bird_color = (255, 255, 255)
pipe_color = (50, 205, 50)
bg_color = (135, 206, 235)

# Pygame setup
pygame.init()
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Bird
bird_x = 50
bird_y = 256
bird_size = 20

# Pipes
pipe_width = 50
pipe_gap = 100
pipe_x = 300
pipe_y = random.randint(100, 300)

class NeuralNetwork:
    def __init__(self):
        self.weights = np.random.rand(3, 2)

    def forward(self, inputs):
        return np.dot(inputs, self.weights)

def draw_floor():
    pygame.draw.rect(screen, (225, 215, 188), (0, 450, screen_width, 62))

def draw_bird(bird_y):
    pygame.draw.rect(screen, bird_color, (bird_x, bird_y, bird_size, bird_size))

def draw_pipes(pipe_x, pipe_y):
    pygame.draw.rect(screen, pipe_color, (pipe_x, 0, pipe_width, pipe_y))
    pygame.draw.rect(screen, pipe_color, (pipe_x, pipe_y + pipe_gap, pipe_width, screen_height - pipe_y - pipe_gap))

def draw_text(text, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

def main():
    global bird_movement, game_active, score, high_score, pipe_x, pipe_y
    neural_network = NeuralNetwork()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(bg_color)

        if game_active:
            bird_movement += gravity
            bird_y = bird_y + bird_movement
            if bird_y > 450:
                bird_y = 450
                game_active = False

            pipe_x -= 2
            if pipe_x < -pipe_width:
                pipe_x = 300
                pipe_y = random.randint(100, 300)
                score += 1

            inputs = np.array([bird_y / screen_height, pipe_x / screen_width, pipe_y / screen_height])
            outputs = neural_network.forward(inputs)
            if outputs[0] > outputs[1]:
                bird_movement = -6

            draw_bird(bird_y)
            draw_pipes(pipe_x, pipe_y)
            draw_floor()
            draw_text(str(score), screen_width // 2 - 10, 50)

            if (pipe_x < bird_x + bird_size and
                pipe_x + pipe_width > bird_x and
                (bird_y < pipe_y or bird_y + bird_size > pipe_y + pipe_gap)):
                game_active = False

        else:
            if score > high_score:
                high_score = score
            draw_text("Game Over", screen_width // 2 - 75, screen_height // 2 - 50)
            draw_text("Score: " + str(score), screen_width // 2 - 50, screen_height // 2)
            draw_text("High Score: " + str(high_score), screen_width // 2 - 75, screen_height // 2 + 50)
            pygame.display.update()
            pygame.time.wait(2000)
            score = 0
            pipe_x = 300
            pipe_y = random.randint(100, 300)
            bird_y = 256
            bird_movement = 0
            game_active = True

        pygame.display.update()
        clock.tick(120)

if __name__ == "__main__":
    main()