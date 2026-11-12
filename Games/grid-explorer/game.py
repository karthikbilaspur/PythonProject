import random
import time
import os
import subprocess
from typing import TypeAlias

Position: TypeAlias = tuple[int, int]

def clear_screen():
    subprocess.run(['cmd', '/c', 'cls'] if os.name == 'nt' else ['clear'], check=False)

def create_grid(size: int, _num_obstacles: int, _num_bombs: int) -> list[list[str]]:
    del _num_obstacles
    del _num_bombs
    grid: list[list[str]] = [[' ' for _ in range(size)] for _ in range(size)]
    return grid

def get_random_pos(size: int, taken: set[Position]) -> Position:
    while True:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)
        if (r, c) not in taken:
            return (r, c)

def display_grid(
    _grid: list[list[str]],
    size: int,
    explorer_pos: Position,
    obstacles: set[Position],
    bombs: set[Position],
    treasure_pos: Position,
    show_all: bool = False,
):
    del _grid
    print("    " + "   ".join([str(i) for i in range(size)]))
    print("  +" + "---+" * size)
    for r in range(size):
        row_str = f"{r} |"
        for c in range(size):
            if (r, c) == explorer_pos:
                row_str += " E |"
            elif show_all and (r, c) == treasure_pos:
                row_str += " T |"
            elif show_all and (r, c) in obstacles:
                row_str += " X |"
            elif show_all and (r, c) in bombs:
                row_str += " B |"
            elif (r, c) in obstacles and show_all:
                row_str += " X |"
            else:
                # Hide everything, but show obstacles if you already bumped into them? 
                # For simplicity, we show obstacles as you explore - let's show them always so game is fair
                if (r, c) in obstacles:
                    row_str += " X |"
                else:
                    row_str += "   |"
        print(row_str)
        print("  +" + "---+" * size)

def play_game():
    clear_screen()
    print("="*40)
    print("      🏴‍☠️  GRID EXPLORER - ENHANCED  🏴‍☠️")
    print("="*40)
    print("1. Easy   - 5x5, 3 Walls, 1 Bomb")
    print("2. Medium - 7x7, 8 Walls, 3 Bombs")
    print("3. Hard   - 10x10, 15 Walls, 5 Bombs")
    print("="*40)
    choice = input("Choose Level (1/2/3): ").strip()

    if choice == '1':
        size, num_obstacles, num_bombs, lives = 5, 3, 1, 3
        level_name = "EASY"
    elif choice == '2':
        size, num_obstacles, num_bombs, lives = 7, 8, 3, 3
        level_name = "MEDIUM"
    elif choice == '3':
        size, num_obstacles, num_bombs, lives = 10, 15, 5, 3
        level_name = "HARD"
    else:
        print("Invalid! Starting Easy...")
        size, num_obstacles, num_bombs, lives = 5, 3, 1, 3
        level_name = "EASY"

    grid = create_grid(size, num_obstacles, num_bombs)

    taken: set[Position] = set()
    treasure_pos: Position = get_random_pos(size, taken)
    taken.add(treasure_pos)

    obstacles: set[Position] = set()
    for _ in range(num_obstacles):
        p: Position = get_random_pos(size, taken)
        obstacles.add(p)
        taken.add(p)

    bombs: set[Position] = set()
    for _ in range(num_bombs):
        p = get_random_pos(size, taken)
        bombs.add(p)
        taken.add(p)

    explorer_pos: Position = get_random_pos(size, taken)

    score = 1000
    moves = 0
    start_time = time.time()
    visited_bombs: set[Position] = set()

    print(f"\nWelcome! Level: {level_name}")
    print("Legend: E = You, X = Wall, T = Treasure (Hidden), B = Bomb (Hidden)")
    print("Commands: up / down / left / right / quit")
    print("Tip: Bombs are hidden! If you step on one, you lose 1 life.")
    input("Press Enter to start...")

    while True:
        clear_screen()
        print(f"LEVEL: {level_name} | ❤️ Lives: {lives} | ⭐ Score: {score} | 🎯 Moves: {moves}")
        print(f"Position: {explorer_pos}")
        
        # Distance + Hot/Cold
        explorer_row, explorer_col = explorer_pos
        treasure_row, treasure_col = treasure_pos
        distance = abs(explorer_row - treasure_row) + abs(explorer_col - treasure_col)
        if distance == 1:
            print("🔥🔥 VERY HOT! Treasure is RIGHT next to you!")
        elif distance <= 3:
            print("🔥 Hot! You are close!")
        elif distance <= 5:
            print("🌡️ Warm... Keep going")
        elif distance <= 8:
            print("❄️ Cold...")
        else:
            print("🧊 FREEZING! Very far!")

        display_grid(grid, size, explorer_pos, obstacles, bombs, treasure_pos, show_all=False)

        move = input("\nYour move (up/down/left/right/quit): ").lower().strip()

        if move == 'quit':
            print(f"\nYou quit! Treasure was at {treasure_pos}")
            display_grid(grid, size, explorer_pos, obstacles, bombs, treasure_pos, show_all=True)
            break

        if move not in ['up', 'down', 'left', 'right']:
            print("Invalid move! Use up/down/left/right")
            time.sleep(1)
            continue

        r, c = explorer_pos
        new_r, new_c = r, c

        if move == 'up': new_r -= 1
        elif move == 'down': new_r += 1
        elif move == 'left': new_c -= 1
        elif move == 'right': new_c += 1

        # Wall Check - Border
        if not (0 <= new_r < size and 0 <= new_c < size):
            print("🧱 Ouch! You hit the border wall!")
            time.sleep(1)
            continue

        # Wall Check - Obstacle
        if (new_r, new_c) in obstacles:
            print("🧱 Ouch! There's a rock wall (X) there! Can't go!")
            time.sleep(1)
            continue

        # Valid Move
        explorer_pos = (new_r, new_c)
        moves += 1
        score = max(0, score - 10)  # -10 per move

        # Check Bomb
        if explorer_pos in bombs and explorer_pos not in visited_bombs:
            visited_bombs.add(explorer_pos)
            lives -= 1
            score = max(0, score - 100)
            print("\n💣 BOOM! You stepped on a BOMB! -1 Life, -100 Score!")
            if lives <= 0:
                clear_screen()
                print("💀 GAME OVER! You ran out of lives!")
                print(f"Treasure was at {treasure_pos}")
                display_grid(grid, size, explorer_pos, obstacles, bombs, treasure_pos, show_all=True)
                break
            time.sleep(2)
            continue

        # Check Treasure
        if explorer_pos == treasure_pos:
            end_time = time.time()
            total_time = int(end_time - start_time)
            clear_screen()
            print("\n🎉🎉 CONGRATULATIONS! YOU FOUND THE TREASURE! 🎉🎉")
            display_grid(grid, size, explorer_pos, obstacles, bombs, treasure_pos, show_all=True)
            print(f"\n🏆 Level: {level_name}")
            print(f"⭐ Final Score: {score}")
            print(f"🎯 Total Moves: {moves}")
            print(f"⏱️ Time Taken: {total_time} seconds")
            print(f"❤️ Lives Left: {lives}")
            break

if __name__ == "__main__":
    while True:
        play_game()
        again = input("\nDo you want to play again? (y/n): ").lower().strip()
        if again != 'y':
            print("Thanks for playing Grid Explorer! Bye! 👋")
            break