import numpy as np
import random

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.add_new_tile()
        self.add_new_tile()
        self.score = 0

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.grid[i, j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i, j] = 2 if random.random() < 0.9 else 4

    def compress(self):
        new_grid = np.zeros((4, 4), dtype=int)
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.grid[i, j] != 0:
                    new_grid[i, pos] = self.grid[i, j]
                    pos += 1
        self.grid = new_grid

    def merge(self):
        for i in range(4):
            for j in range(3):
                if self.grid[i, j] == self.grid[i, j + 1] and self.grid[i, j] != 0:
                    self.grid[i, j] *= 2
                    self.grid[i, j + 1] = 0
                    self.score += self.grid[i, j]

    def reverse(self):
        self.grid = np.fliplr(self.grid)

    def transpose(self):
        self.grid = self.grid.T

    def check_empty_cells(self):
        return any(0 in row for row in self.grid)

    def game_state(self):
        for i in range(3):
            for j in range(3):
                if self.grid[i, j] == self.grid[i + 1, j] or self.grid[i, j] == self.grid[i, j + 1]:
                    return 'GAME NOT OVER'
        for i in range(3):
            for j in range(3):
                if self.grid[i + 1, j] == self.grid[i, j] or self.grid[i, j + 1] == self.grid[i, j]:
                    return 'GAME NOT OVER'
        for i in range(4):
            if self.grid[i, 3] == self.grid[i, 2] or self.grid[3, i] == self.grid[2, i]:
                return 'GAME NOT OVER'
        return 'LOST'

    def left(self):
        self.compress()
        self.merge()
        self.compress()

    def right(self):
        self.reverse()
        self.compress()
        self.merge()
        self.compress()
        self.reverse()

    def up(self):
        self.transpose()
        self.compress()
        self.merge()
        self.compress()
        self.transpose()

    def down(self):
        self.transpose()
        self.reverse()
        self.compress()
        self.merge()
        self.compress()
        self.reverse()
        self.transpose()

    def play(self, move):
        if move == 'left':
            self.left()
        elif move == 'right':
            self.right()
        elif move == 'up':
            self.up()
        elif move == 'down':
            self.down()
        self.add_new_tile()

    def get_grid(self):
        return self.grid

    def get_score(self):
        return self.score

def ai_play(game):
    moves = ['left', 'right', 'up', 'down']
    best_move = None
    best_score = -np.inf
    for move in moves:
        game_copy = Game2048()
        game_copy.grid = np.copy(game.grid)
        game_copy.score = game.score
        game_copy.play(move)
        score = game_copy.get_score()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

game = Game2048()
while True:
    print("Score:", game.get_score())
    print(game.get_grid())
    move = ai_play(game)
    print("AI's move:", move)
    game.play(move)
    if game.game_state() == 'LOST':
        print("Game Over!")
        print("Final Score:", game.get_score())
        break