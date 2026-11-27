import random

def print_board(board: list[str]) -> None:
    print()
    for i in range(0, 9, 3):
        row = " | ".join(board[i:i+3])
        print(f" {row} ")
        if i < 6:
            print("---+---+---")
    print()

def check_winner(board: list[str], mark: str) -> bool:
    wins = [
        (0,1,2), (3,4,5), (6,7,8),  # rows
        (0,3,6), (1,4,7), (2,5,8),  # columns
        (0,4,8), (2,4,6),           # diagonals
    ]
    return any(board[a] == board[b] == board[c] == mark for a, b, c in wins)

def is_full(board: list[str]) -> bool:
    return all(cell in ("X", "O") for cell in board)

def get_player_move(board: list[str], mark: str) -> int:
    while True:
        try:
            move = int(input(f"Player {mark}, pick a spot (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Pick a number between 1 and 9.")
            elif board[move] in ("X", "O"):
                print("That spot is taken, try another.")
            else:
                return move
        except ValueError:
            print("Enter a number, not text.")

def get_computer_move(board: list[str], computer: str, human: str) -> int:
    # 1. Win if possible
    for i in range(9):
        if board[i] not in ("X", "O"):
            board[i] = computer
            if check_winner(board, computer):
                board[i] = str(i + 1)
                return i
            board[i] = str(i + 1)
    # 2. Block player win
    for i in range(9):
        if board[i] not in ("X", "O"):
            board[i] = human
            if check_winner(board, human):
                board[i] = str(i + 1)
                return i
            board[i] = str(i + 1)
    # 3. Take centre, then corner, then random
    if board[4] not in ("X", "O"):
        return 4
    corners = [i for i in (0, 2, 6, 8) if board[i] not in ("X", "O")]
    if corners:
        return random.choice(corners)
    free = [i for i in range(9) if board[i] not in ("X", "O")]
    return random.choice(free)

def play_game(mode: str) -> None:
    board = [str(i + 1) for i in range(9)]
    current = "X"
    print_board(board)
    while True:
        if mode == "2" and current == "O":
            print("Computer (O) is thinking...")
            move = get_computer_move(board, "O", "X")
        else:
            move = get_player_move(board, current)
        board[move] = current
        print_board(board)
        if check_winner(board, current):
            if mode == "2" and current == "O":
                print("Computer wins! Better luck next time.")
            else:
                print(f"Player {current} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break
        current = "O" if current == "X" else "X"

def main():
    print("=" * 30)
    print("   TIC-TAC-TOE")
    print("=" * 30)
    print("\nSpots are numbered 1-9 like this:")
    print_board([str(i + 1) for i in range(9)])
    while True:
        print("1. Two players")
        print("2. Play vs computer")
        print("3. Quit")
        choice = input(">> pick 1 / 2 / 3: ").strip()
        if choice == "1":
            play_game("1")
        elif choice == "2":
            play_game("2")
        elif choice == "3":
            print("\nThanks for playing!")
            break
        else:
            print("Pick 1, 2 or 3.")
        print("-" * 30)
        again = input("Play again? (Y/n): ").strip().lower()
        if again == "n":
            print("\nThanks for playing!")
            break

if __name__ == "__main__":
    main()
