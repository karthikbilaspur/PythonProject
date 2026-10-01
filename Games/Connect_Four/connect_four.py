import numpy as np

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

    def drop_piece(self, column):
        row = self.get_next_open_row(column)
        self.board[row, column] = self.turn

    def winning_move(self):
        # Check horizontal locations for win
        for c in range(7-3):
            for r in range(6):
                if self.board[r, c] == self.turn and self.board[r, c+1] == self.turn and self.board[r, c+2] == self.turn and self.board[r, c+3] == self.turn:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6-3):
                if self.board[r, c] == self.turn and self.board[r+1, c] == self.turn and self.board[r+2, c] == self.turn and self.board[r+3, c] == self.turn:
                    return True

        # Check positively sloped diagonals
        for c in range(7-3):
            for r in range(6-3):
                if self.board[r, c] == self.turn and self.board[r+1, c+1] == self.turn and self.board[r+2, c+2] == self.turn and self.board[r+3, c+3] == self.turn:
                    return True

        # Check negatively sloped diagonals
        for c in range(7-3):
            for r in range(3, 6):
                if self.board[r, c] == self.turn and self.board[r-1, c+1] == self.turn and self.board[r-2, c+2] == self.turn and self.board[r-3, c+3] == self.turn:
                    return True

    def play(self):
        while True:
            self.print_board()
            column = int(input(f"Player {self.turn}, choose a column: ")) - 1
            if self.is_valid(column):
                self.drop_piece(column)
                if self.winning_move():
                    self.print_board()
                    print(f"Player {self.turn} wins!")
                    break
                self.turn = 2 if self.turn == 1 else 1
            else:
                print("Invalid move, try again.")

if __name__ == "__main__":
    game = Connect4()
    game.play()