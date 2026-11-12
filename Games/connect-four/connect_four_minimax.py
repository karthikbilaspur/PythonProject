import numpy as np
import random

class Connect4:
    def __init__(self):
        self.board = np.zeros((6, 7))
        self.turn = 1

    def print_board(self):
        print(" 1 | 2 | 3 | 4 | 5 | 6 | 7")
        for row in self.board:
            for cell in row:
                if cell == 0:
                    print(" . ", end="|")
                elif cell == 1:
                    print(" X ", end="|")
                else:
                    print(" O ", end="|")
            print("\n")

    def is_valid(self, column):
        return self.board[0, column] == 0

    def get_next_open_row(self, column):
        for row in range(5, -1, -1):
            if self.board[row, column] == 0:
                return row

    def drop_piece(self, column, piece):
        row = self.get_next_open_row(column)
        self.board[row, column] = piece

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(7-3):
            for r in range(6):
                if self.board[r, c] == piece and self.board[r, c+1] == piece and self.board[r, c+2] == piece and self.board[r, c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6-3):
                if self.board[r, c] == piece and self.board[r+1, c] == piece and self.board[r+2, c] == piece and self.board[r+3, c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(7-3):
            for r in range(6-3):
                if self.board[r, c] == piece and self.board[r+1, c+1] == piece and self.board[r+2, c+2] == piece and self.board[r+3, c+3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(7-3):
            for r in range(3, 6):
                if self.board[r, c] == piece and self.board[r-1, c+1] == piece and self.board[r-2, c+2] == piece and self.board[r-3, c+3] == piece:
                    return True

    def evaluate_position(self):
        score = 0
        # Check horizontal locations
        for c in range(7-3):
            for r in range(6):
                window = [self.board[r, c+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Check vertical locations
        for c in range(7):
            for r in range(6-3):
                window = [self.board[r+i, c] for i in range(4)]
                score += self.evaluate_window(window)

        # Check positively sloped diagonals
        for c in range(7-3):
            for r in range(6-3):
                window = [self.board[r+i, c+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Check negatively sloped diagonals
        for c in range(7-3):
            for r in range(3, 6):
                window = [self.board[r-i, c+i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        score = 0
        if window.count(2) == 4:
            score -= 100
        elif window.count(2) == 3 and window.count(0) == 1:
            score -= 5
        elif window.count(2) == 2 and window.count(0) == 2:
            score -= 2
        if window.count(1) == 4:
            score += 100
        elif window.count(1) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(1) == 2 and window.count(0) == 2:
            score += 2
        return score

    def minimax(self, depth, maximizingPlayer):
        if self.winning_move(1):
            return float('inf')
        elif self.winning_move(2):
            return float('-inf')
        elif depth == 0:
            return self.evaluate_position()

        if maximizingPlayer:
            bestScore = float('-inf')
            for column in range(7):
                if self.is_valid(column):
                    row = self.get_next_open_row(column)
                    self.drop_piece(column, 1)
                    score = self.minimax(depth-1, False)
                    self.board[row, column] = 0
                    bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = float('inf')
            for column in range(7):
                if self.is_valid(column):
                    row = self.get_next_open_row(column)
                    self.drop_piece(column, 2)
                    score = self.minimax(depth-1, True)
                    self.board[row, column] = 0
                    bestScore = min(score, bestScore)
            return bestScore

    def play(self):
        while True:
            self.print_board()
            if self.turn == 1:
                column = int(input("Player 1, choose a column: ")) - 1
                if self.is_valid(column):
                    self.drop_piece(column, 1)
                    if self.winning_move(1):
                        self.print_board()
                        print("Player 1 wins!")
                        break
                    self.turn = 2
                else:
                    print("Invalid move, try again.")
            else:
                bestScore = float('-inf')
                bestColumn = 0
                for column in range(7):
                    if self.is_valid(column):
                        row = self.get_next_open_row(column)
                        self.drop_piece(column, 2)
                        score = self.minimax(5, True)
                        self.board[row, column] = 0
                        if score > bestScore:
                            bestScore = score
                            bestColumn = column
                self.drop_piece(bestColumn, 2)
                if self.winning_move(2):
                    self.print_board()
                    print("Player 2 wins!")
                    break
                self.turn = 1

if __name__ == "__main__":
    game = Connect4()
    game.play()