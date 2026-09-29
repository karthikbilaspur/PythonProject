import numpy as np

class Reversi:
    def __init__(self):
        self.board = np.zeros((8, 8))
        self.board[3, 3] = 1
        self.board[3, 4] = -1
        self.board[4, 3] = -1
        self.board[4, 4] = 1
        self.player_turn = 1
        self.move_count = 0

    def is_valid_move(self, row, col):
        if row < 0 or row >= 8 or col < 0 or col >= 8 or self.board[row, col] != 0:
            return False

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            capture = False
            r, c = row + direction[0], col + direction[1]
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == -self.player_turn:
                capture = True
                r += direction[0]
                c += direction[1]
            if capture and 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.player_turn:
                return True

        return False

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row, col] = self.player_turn
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                capture = False
                r, c = row + direction[0], col + direction[1]
                tiles_to_flip = []
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == -self.player_turn:
                    capture = True
                    tiles_to_flip.append((r, c))
                    r += direction[0]
                    c += direction[1]
                if capture and 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.player_turn:
                    for tile in tiles_to_flip:
                        self.board[tile[0], tile[1]] = self.player_turn
            self.player_turn *= -1
            self.move_count += 1

    def evaluate_board(self):
        return np.sum(self.board)

    def get_valid_moves(self):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves

    def undo_move(self, row, col):
        self.board[row, col] = 0
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            capture = False
            r, c = row + direction[0], col + direction[1]
            tiles_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.player_turn:
                capture = True
                tiles_to_flip.append((r, c))
                r += direction[0]
                c += direction[1]
            if capture and 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == -self.player_turn:
                for tile in tiles_to_flip:
                    self.board[tile[0], tile[1]] = self.player_turn
        self.player_turn *= -1
        self.move_count -= 1


class Minimax:
    def __init__(self, game):
        self.game = game
        self.max_depth = 5

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or len(self.game.get_valid_moves()) == 0:
            return self.game.evaluate_board()

        if maximizingPlayer:
            max_eval = float('-inf')
            for move in self.game.get_valid_moves():
                self.game.make_move(move[0], move[1])
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.game.board[move[0], move[1]] = 0
                self.game.undo_move(move[0], move[1])
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.game.get_valid_moves():
                self.game.make_move(move[0], move[1])
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.game.board[move[0], move[1]] = 0
                self.game.undo_move(move[0], move[1])
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        for move in self.game.get_valid_moves():
            self.game.make_move(move[0], move[1])
            score = self.minimax(self.max_depth - 1, float('-inf'), float('inf'), False)
            self.game.board[move[0], move[1]] = 0
            self.game.undo_move(move[0], move[1])
            if score > best_score:
                best_score = score
                best_move = move
        return best_move


def print_board(board):
    print("  A B C D E F G H")
    for i in range(8):
        print(i + 1, end=" ")
        for j in range(8):
            if board[i, j] == 1:
                print("X", end=" ")
            elif board[i, j] == -1:
                print("O", end=" ")
            else:
                print(".", end=" ")
        print()


def main():
    game = Reversi()
    minimax = Minimax(game)
    while game.move_count < 64:
        print_board(game.board)
        if game.player_turn == 1:
            move = input("Enter your move (row and column separated by space, e.g., 4 4): ")
            row, col = map(int, move.split())
            if game.is_valid_move(row - 1, col - 1):
                game.make_move(row - 1, col - 1)
            else:
                print("Invalid move, try again.")
        else:
            move = minimax.get_best_move()
            game.make_move(move[0], move[1])
            print("AI's move: ", move[0] + 1, move[1] + 1)
    print_board(game.board)
    score = game.evaluate_board()
    if score > 0:
        print("You win!")
    elif score < 0:
        print("AI wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    main()