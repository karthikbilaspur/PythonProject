import tkinter as tk
from random import randint

class LudoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ludo Game")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.players = ["blue", "red", "green", "yellow"]
        self.current_player = 0
        self.tokens = []
        self.positions = [0, 0, 0, 0]
        self.create_board()
        self.create_tokens()
        self.roll_dice_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_dice_button.pack()
        self.player_turn_label = tk.Label(self.root, text="Player 1's Turn")
        self.player_turn_label.pack()
        self.dice_label = tk.Label(self.root, text="")
        self.dice_label.pack()
        self.game_over_label = tk.Label(self.root, text="")
        self.game_over_label.pack()

    def create_board(self):
        # Draw the game board
        for i in range(20):
            x = (i % 5) * 80
            y = (i // 5) * 80
            self.canvas.create_rectangle(x, y, x+80, y+80, outline="black")

    def create_tokens(self):
        # Create player tokens
        for i in range(4):
            token = self.canvas.create_oval(10, 10, 30, 30, fill=self.players[i])
            self.tokens.append(token)
            self.canvas.coords(token, (i % 4) * 80 + 20, (i // 4) * 80 + 20, (i % 4) * 80 + 40, (i // 4) * 80 + 40)

    def roll_dice(self):
        # Roll the dice and move the token
        roll = randint(1, 6)
        self.dice_label.config(text=f"Dice Roll: {roll}")
        self.move_token(self.current_player, roll)
        self.current_player = (self.current_player + 1) % 4
        self.player_turn_label.config(text=f"Player {(self.current_player + 1)}'s Turn")

    def move_token(self, player, steps):
        # Update token position based on dice roll
        self.positions[player] += steps
        if self.positions[player] >= 20:
            self.game_over(player)
        else:
            x = (self.positions[player] % 5) * 80 + 20
            y = (self.positions[player] // 5) * 80 + 20
            self.canvas.coords(self.tokens[player], x, y, x+20, y+20)

    def game_over(self, player):
        # Game over logic
        self.game_over_label.config(text=f"Player {player+1} Wins!")
        self.roll_dice_button.config(state="disabled")

    def reset_game(self):
        # Reset the game
        self.current_player = 0
        self.positions = [0, 0, 0, 0]
        self.game_over_label.config(text="")
        self.roll_dice_button.config(state="normal")
        self.player_turn_label.config(text="Player 1's Turn")
        for i in range(4):
            self.canvas.coords(self.tokens[i], (i % 4) * 80 + 20, (i // 4) * 80 + 20, (i % 4) * 80 + 40, (i // 4) * 80 + 40)

root = tk.Tk()
game = LudoGame(root)
reset_button = tk.Button(root, text="Reset Game", command=game.reset_game)
reset_button.pack()
root.mainloop()