def create_board(size: int) -> list[list[str]]:
    """Creates a 2D list representing the game board."""
    return [[' ' for _ in range(size)] for _ in range(size)]

def display_board(board: list[list[str]]) -> None:
    """Prints the current state of the game board."""
    size = len(board)
    for r, row in enumerate(board):
        print(' | '.join(row))
        if r < size - 1:
            print('-' * (size * 4 - 1))

def check_win(board: list[list[str]], row: int, col: int, win_length: int = 5) -> bool:
    """Checks if the current player has won the game."""
    size = len(board)
    player = board[row][col]

    # (dr, dc) for horizontal, vertical, and both diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1

        # Forward
        r, c = row + dr, col + dc
        while 0 <= r < size and 0 <= c < size and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        # Backward
        r, c = row - dr, col - dc
        while 0 <= r < size and 0 <= c < size and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= win_length:
            return True

    return False

def is_board_full(board: list[list[str]]) -> bool:
    """Checks if the game board is full."""
    return all(cell != ' ' for row in board for cell in row)

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