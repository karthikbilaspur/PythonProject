import random
from unittest import result

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.score = {'X': 0, 'O': 0}

    def print_board(self):
        print(' ' + self.board[0] + ' | ' + self.board<meta-citation label='www.datacamp.com' urls='["https:\/\/www.datacamp.com\/tutorial\/minimax-algorithm-for-ai-in-python"]' entity_ids='[""]' /> + ' | ' + self.board<meta-citation label='www.webhi.com' urls='["https:\/\/www.webhi.com\/how-to\/create-an-ai-powered-tic-tac-toe-game\/"]' entity_ids='[""]' />)
        print('-----------')
        print(' ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5])
        print('-----------')
        print(' ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8])

    def check_win(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != ' ':
                return self.board[condition[0]]
        if ' ' not in self.board:
            return 'Tie'
        return False

    def ai_move(self):
        best_score = -1000
        best_move = 0
        for key in range(9):
            if self.board[key] == ' ':
                self.board[key] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[key] = ' '
                if score > best_score:
                    best_score = score
                    best_move = key
        self.board[best_move] = 'O'

    def minimax(self, board: list, depth: int, is_maximizing: bool) -> int:
        result = self.check_win()
        if result:
            if result == 'X':
                return -1
            elif result == 'O':
                return 1
            elif result == 'Tie':
                return 0
        if is_maximizing:
            best_score = -1000
            for key in range(9):
                if board[key] == ' ':
                    board[key] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[key] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = 1000
            for key in range(9):
                if board[key] == ' ':
                    board[key] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[key] = ' '
                    best_score = min(score, best_score)
            return best_score

    def game(self):
        current_player = 'X'
        while True:
            self.print_board()
            try:
                move = int(input("Player " + current_player + ", enter your move (1-9): "))
                if self.board[move - 1] != ' ':
                    print("Invalid move, try again.")
                    continue
                self.board[move - 1] = current_player
                result = self.check_win()
                if result:
                    self.print_board()
                    if result == 'Tie':
                        print("It's a tie!")
                    else:
                        print("Player " + result + " wins!")
                        self.score[result] += 1
                        print("Score - X: " + str(self.score['X']) + ", O: " + str(self.score['O']))
                    break
                current_player = 'O'
                self.ai_move()
                result = self.check_win()
                if result:
                    self.print_board()
                    if result == 'Tie':
                        print("It's a tie!")
                    else:
                        print("Player " + result + " wins!")
                        self.score[result] += 1
                        print("Score - X: " + str(self.score['X']) + ", O: " + str(self.score['O']))
                    break
                current_player = 'X'
            except (ValueError, IndexError):
                print("Invalid input, please enter a number between 1 and 9.")

game = TicTacToe()
game.game()