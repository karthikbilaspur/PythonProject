import chess
import chess.pgn
import random
from stockfish import Stockfish
import tkinter as tk
from tkinter import messagebox

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.engine = Stockfish("/path/to/stockfish.exe", parameters={"Threads": 4, "Hash": 1024})
        self.root = tk.Tk()
        self.root.title("Chess Game")
        self.label = tk.Label(self.root, text="Enter your move (e.g. e2e4): ")
        self.label.pack()
        self.entry = tk.Entry(self.root, width=10)
        self.entry.pack()
        self.button = tk.Button(self.root, text="Make Move", command=self.make_move)
        self.button.pack()
        self.text_box = tk.Text(self.root, height=20, width=40)
        self.text_box.pack()
        self.update_board()
        self.move_history = []

    def update_board(self):
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, str(self.board))

    def make_move(self):
        move = self.entry.get()
        try:
            move = chess.Move.from_uci(move)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move.uci())
                self.update_board()
                self.ai_move()
            else:
                messagebox.showerror("Invalid Move", "Invalid move. Please try again.")
        except ValueError:
            messagebox.showerror("Invalid Move", "Invalid move. Please try again.")

    def ai_move(self):
        self.engine.set_fen_position(self.board.fen())
        move = self.engine.get_best_move()
        move = chess.Move.from_uci(move)
        self.board.push(move)
        self.move_history.append(move.uci())
        self.update_board()
        if self.board.is_game_over():
            self.game_over()

    def game_over(self):
        result = self.board.result()
        if result == "1-0":
            message = "Game over. White wins!"
        elif result == "0-1":
            message = "Game over. Black wins!"
        else:
            message = "Game over. Draw!"
        messagebox.showinfo("Game Over", message)
        self.save_game()

    def save_game(self):
        with open("game.pgn", "w") as f:
            game = chess.pgn.Game.from_board(self.board)
            f.write(str(game))

    def start_game(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = ChessGame()
    game.start_game()