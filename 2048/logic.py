import random

# Constants
GRID_SIZE = 4
TARGET_TILE = 2048

def start_game():
    mat = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_2(mat)
    add_new_2(mat)
    return mat

def add_new_2(mat: list[list[int]]) -> None:
    r, c = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    while mat[r][c] != 0:
        r, c = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    mat[r][c] = 2

def get_current_state(mat: list[list[int]]) -> str:
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if mat[i][j] == TARGET_TILE:
                return 'WON'
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if mat[i][j] == 0:
                return 'GAME NOT OVER'
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE-1):
            if mat[i][j] == mat[i][j+1]:
                return 'GAME NOT OVER'
    for i in range(GRID_SIZE-1):
        for j in range(GRID_SIZE):
            if mat[i][j] == mat[i+1][j]:
                return 'GAME NOT OVER'
    return 'LOST'

def get_score(mat: list[list[int]]) -> int:
    score = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            score += mat[i][j]
    return score

def compress(mat: list[list[int]]):
    new_mat = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    changed = False
    for i in range(GRID_SIZE):
        pos = 0
        for j in range(GRID_SIZE):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1
    return new_mat, changed

def merge(mat: list[list[int]]) -> tuple[list[list[int]], bool]:
    changed = False
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                changed = True
    return mat, changed

def reverse(mat: list[list[int]]) -> list[list[int]]:
    return [row[::-1] for row in mat]

def transpose(mat: list[list[int]]) -> list[list[int]]:
    return list(map(list, zip(*mat)))

def move_left(mat: list[list[int]]) -> tuple[list[list[int]], bool]:
    new_mat, changed1 = compress(mat)
    new_mat, changed2 = merge(new_mat)
    new_mat, _ = compress(new_mat)
    return new_mat, changed1 or changed2

def move_right(mat: list[list[int]]) -> tuple[list[list[int]], bool]:
    reversed_mat = reverse(mat)
    moved_mat, changed = move_left(reversed_mat)
    return reverse(moved_mat), changed

def move_up(mat: list[list[int]]) -> tuple[list[list[int]], bool]:
    transposed = transpose(mat)
    moved_mat, changed = move_left(transposed)
    return transpose(moved_mat), changed

def move_down(mat: list[list[int]]) -> tuple[list[list[int]], bool]:
    transposed = transpose(mat)
    moved_mat, changed = move_right(transposed)
    return transpose(moved_mat), changed

def random_ai_move(mat: list[list[int]]) -> list[list[int]]:
    moves = ['w', 'a', 's', 'd']
    move = random.choice(moves)
    if move == 'w':
        mat, _ = move_up(mat)
    elif move == 'a':
        mat, _ = move_left(mat)
    elif move == 's':
        mat, _ = move_down(mat)
    else:
        mat, _ = move_right(mat)
    return mat

def minimax_ai_move(mat: list[list[int]]) -> list[list[int]]:
    best_score = -float('inf')
    best_move = None
    for move in ['w', 'a', 's', 'd']:
        new_mat: list[list[int]] = [row[:] for row in mat]
        if move == 'w':
            new_mat, _ = move_up(new_mat)
        elif move == 'a':
            new_mat, _ = move_left(new_mat)
        elif move == 's':
            new_mat, _ = move_down(new_mat)
        else:
            new_mat, _ = move_right(new_mat)
        score = minimax(new_mat, 0, False)
        if score > best_score:
            best_score = score
            best_move = move
    if best_move == 'w':
        mat, _ = move_up(mat)
    elif best_move == 'a':
        mat, _ = move_left(mat)
    elif best_move == 's':
        mat, _ = move_down(mat)
    else:
        mat, _ = move_right(mat)
    return mat

def minimax(mat: list[list[int]], depth: int, is_maximizing: bool) -> int:
    if get_current_state(mat) != "GAME NOT OVER":
        if get_current_state(mat) == "WON":
            return 10000
        else:
            return -10000

    if is_maximizing:
        best_score = -float('inf')
        for move in ['w', 'a', 's', 'd']:
            new_mat = [row[:] for row in mat]
            if move == 'w':
                new_mat, _ = move_up(new_mat)
            elif move == 'a':
                new_mat, _ = move_left(new_mat)
            elif move == 's':
                new_mat, _ = move_down(new_mat)
            else:
                new_mat, _ = move_right(new_mat)
            score = minimax(new_mat, depth + 1, False)
            best_score = max(score, best_score)
        return int(best_score)
    else:
        best_score = float('inf')
        for _ in range(4):  # 4 possible new tile positions
            new_mat = [row[:] for row in mat]
            add_new_2(new_mat)
            score = minimax(new_mat, depth + 1, True)
            best_score = min(score, best_score)
        return int(best_score)    