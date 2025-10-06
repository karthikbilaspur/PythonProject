
import random
import operator

def is_valid(board, row, col, num):
    # Check if 'num' can be placed in the given position without violating the rules
    for i in range(len(board)):
        if board[row][i] == num or board[i][col] == num:
            return False
    return True

def solve_kenken(board):
    # Function to solve the KenKen puzzle using backtracking
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                for num in range(1, len(board) + 1):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_kenken(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def generate_kenken_puzzle(size, difficulty):
    # Function to generate a KenKen puzzle
    board = [[0 for _ in range(size)] for _ in range(size)]
    solve_kenken(board)

    # Remove numbers from the board to create the puzzle
    for i in range(size):
        for j in range(size):
            if random.random() < difficulty:
                board[i][j] = 0

    return board

def generate_cage_constraints(size, num_cages):
    # Function to generate cage constraints
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    cages = []
    for _ in range(num_cages):
        num_cells = random.randint(2, 4)
        cells = []
        for _ in range(num_cells):
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            cells.append((row, col))

        op = random.choice(list(operations.keys()))
        target = random.randint(1, 10)

        cages.append({
            'cells': cells,
            'operation': op,
            'target': target
        })

    return cages

def print_board(board):
    # Function to pretty print the KenKen board
    for row in board:
        print(" ".join(str(num) if num != 0 else "-" for num in row))
    print()

def print_cage_constraints(cages):
    # Function to print cage constraints
    for i, cage in enumerate(cages):
        print(f"Cage {i + 1}:")
        print(f"Cells: {cage['cells']}")
        print(f"Operation: {cage['operation']}")
        print(f"Target: {cage['target']}")
        print()

def main():
    size = int(input("Enter the size of the grid (e.g., 4 for a 4x4 puzzle): "))
    difficulty = float(input("Enter the difficulty level (e.g., 0.5 for 50% of numbers hidden): "))
    num_cages = int(input("Enter the number of cage constraints: "))

    kenken_puzzle = generate_kenken_puzzle(size, difficulty)
    cages = generate_cage_constraints(size, num_cages)

    print("KenKen Puzzle:")
    print_board(kenken_puzzle)
    print("Cage Constraints:")
    print_cage_constraints(cages)

    solved_board = [row[:] for row in kenken_puzzle]
    if solve_kenken(solved_board):
        print("Solved KenKen Puzzle:")
        print_board(solved_board)
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()
