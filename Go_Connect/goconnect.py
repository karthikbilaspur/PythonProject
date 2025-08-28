def create_board(size: int) -> list:
    """Creates a 2D list representing the game board."""
    return [[' ' for _ in range(size)] for _ in range(size)]


def display_board(board: list) -> None:
    """Prints the current state of the game board."""
    size = len(board)
    for row in board:
        print(' | '.join(row))
        print('-' * (size * 4 - 1))


def check_win(board: list, row: int, col: int, win_length: int = 5) -> bool:
    """Checks if the current player has won the game."""
    size = len(board)
    player = board[row][col]

    # Check horizontal
    for i in range(max(0, col - win_length + 1), min(size, col + win_length)):
        if board[row][i:i + win_length] == [player] * win_length:
            return True

    # Check vertical
    for i in range(max(0, row - win_length + 1), min(size, row + win_length)):
        if all(board[i + j][col] == player for j in range(win_length)):
            return True

    # Check diagonal (top-left to bottom-right)
    if check_diagonal(board, row, col, player, win_length, 1):
        return True

    # Check diagonal (bottom-left to top-right)
    if check_diagonal(board, row, col, player, win_length, -1):
        return True

    return False


def check_diagonal(board: list, row: int, col: int, player: str, win_length: int, direction: int) -> bool:
    """Checks if the current player has won in a diagonal direction."""
    size = len(board)
    for i in range(max(0, row - win_length + 1), min(size - win_length + 1, row + 1)):
        if all(board[i + j * direction][col + j] == player for j in range(win_length)):
            return True
    return False


def is_board_full(board: list) -> bool:
    """Checks if the game board is full."""
    return all(board[row][col] != ' ' for row in range(len(board)) for col in range(len(board[0])))


def get_valid_input(prompt: str, min_value: int, max_value: int) -> int:
    """Gets a valid integer input from the user."""
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print("Invalid input. Please enter a value within the range.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def gomoku() -> None:
    """Plays the game of Gomoku."""
    size = 15
    board = create_board(size)
    player = 'X'

    while True:
        display_board(board)

        if is_board_full(board):
            print("It's a draw!")
            break

        row = get_valid_input(f"Player {player}, enter row (0-{size - 1}): ", 0, size - 1)
        col = get_valid_input(f"Player {player}, enter column (0-{size - 1}): ", 0, size - 1)

        if board[row][col] == ' ':
            board[row][col] = player

            if check_win(board, row, col):
                display_board(board)
                print(f"Player {player} wins!")
                break

            player = 'O' if player == 'X' else 'X'
        else:
            print("Invalid move. Try again.")


if __name__ == "__main__":
    gomoku()