import random
import heapq

class GameOfFifteen:
    def __init__(self):
        self.tiles = list(range(1, 16)) + [0]
        random.shuffle(self.tiles)
        while not self.is_solvable(self.tiles):
            random.shuffle(self.tiles)
        self.tiles = [self.tiles[i:i+4] for i in range(0, 16, 4)]
        self.move_count = 0

    def print_board(self):
        for row in self.tiles:
            print(' '.join(str(tile) if tile != 0 else '_' for tile in row))

    def is_valid_move(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def get_empty_space(self):
        for i in range(4):
            for j in range(4):
                if self.tiles[i][j] == 0:
                    return i, j

    def make_move(self, direction):
        x, y = self.get_empty_space()
        if direction == 'up' and x > 0:
            self.tiles[x][y], self.tiles[x-1][y] = self.tiles[x-1][y], self.tiles[x][y]
            self.move_count += 1
        elif direction == 'down' and x < 3:
            self.tiles[x][y], self.tiles[x+1][y] = self.tiles[x+1][y], self.tiles[x][y]
            self.move_count += 1
        elif direction == 'left' and y > 0:
            self.tiles[x][y], self.tiles[x][y-1] = self.tiles[x][y-1], self.tiles[x][y]
            self.move_count += 1
        elif direction == 'right' and y < 3:
            self.tiles[x][y], self.tiles[x][y+1] = self.tiles[x][y+1], self.tiles[x][y]
            self.move_count += 1
        else:
            print("Invalid move!")

    def check_win(self):
        flat_tiles = [tile for row in self.tiles for tile in row]
        return flat_tiles == list(range(1, 16)) + [0]

    def is_solvable(self, tiles):
        inversion_count = 0
        for i in range(len(tiles)):
            for j in range(i+1, len(tiles)):
                if tiles[i] > tiles[j] and tiles[i] != 0 and tiles[j] != 0:
                    inversion_count += 1
        return inversion_count % 2 == 0

    def get_hint(self):
        # Use A* search algorithm to find the next best move
        queue = []
        heapq.heappush(queue, (0, self.tiles))
        visited = set()
        while queue:
            _, current_tiles = heapq.heappop(queue)
            current_tiles_tuple = tuple(tile for row in current_tiles for tile in row)
            if current_tiles_tuple in visited:
                continue
            visited.add(current_tiles_tuple)
            if self.check_win_tiles(current_tiles):
                return self.get_move_from_tiles(current_tiles)
            for direction in ['up', 'down', 'left', 'right']:
                new_tiles = self.get_new_tiles(current_tiles, direction)
                if new_tiles:
                    heapq.heappush(queue, (self.get_heuristic(new_tiles), new_tiles))
        return None

    def check_win_tiles(self, tiles):
        flat_tiles = [tile for row in tiles for tile in row]
        return flat_tiles == list(range(1, 16)) + [0]

    def get_move_from_tiles(self, tiles):
        # Find the move that leads to the winning state
        for direction in ['up', 'down', 'left', 'right']:
            new_tiles = self.get_new_tiles(self.tiles, direction)
            if new_tiles and new_tiles == tiles:
                return direction
        return None

    def get_new_tiles(self, tiles, direction):
        x, y = self.get_empty_space_tiles(tiles)
        if direction == 'up' and x > 0:
            tiles[x][y], tiles[x-1][y] = tiles[x-1][y], tiles[x][y]
            return tiles
        elif direction == 'down' and x < 3:
            tiles[x][y], tiles[x+1][y] = tiles[x+1][y], tiles[x][y]
            return tiles
        elif direction == 'left' and y > 0:
            tiles[x][y], tiles[x][y-1] = tiles[x][y-1], tiles[x][y]
            return tiles
        elif direction == 'right' and y < 3:
            tiles[x][y], tiles[x][y+1] = tiles[x][y+1], tiles[x][y]
            return tiles
        return None

    def get_empty_space_tiles(self, tiles):
        for i in range(4):
            for j in range(4):
                if tiles[i][j] == 0:
                    return i, j

    def get_heuristic(self, tiles):
        # Manhattan distance heuristic
        heuristic = 0
        for i in range(4):
            for j in range(4):
                tile = tiles[i][j]
                if tile != 0:
                    goal_i, goal_j = divmod(tile-1, 4)
                    heuristic += abs(i - goal_i) + abs(j - goal_j)
        return heuristic

def main():
    game = GameOfFifteen()
    while True:
        game.print_board()
        print(f"Move count: {game.move_count}")
        direction = input("Enter direction (up, down, left, right), 'h' for hint, 'r' to restart: ")
        if direction == 'h':
            hint = game.get_hint()
            if hint:
                print(f"Hint: {hint}")
            else:
                print("No hint available!")
        elif direction == 'r':
            game = GameOfFifteen()
        else:
            game.make_move(direction)
            if game.check_win():
                game.print_board()
                print(f"Congratulations! You won in {game.move_count} moves!")
                break

if __name__ == "__main__":
    main()