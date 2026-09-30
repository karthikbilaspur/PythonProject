import heapq
import random
from collections import deque
from typing import Optional, TypeAlias


Position: TypeAlias = tuple[int, int]
Path: TypeAlias = list[Position]
Maze: TypeAlias = list[list[bool]]


class MazeSolver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.rows: int = len(maze)
        self.cols: int = len(maze[0])
        self.start: Position = (0, 0)
        self.goal: Position = (self.rows - 1, self.cols - 1)

    def is_valid_move(self, row: int, col: int) -> bool:
        return (0 <= row < self.rows) and (0 <= col < self.cols) and not self.maze[row][col]

    def dfs_maze_solver(self) -> Optional[Path]:
        visited = [[False]*self.cols for _ in range(self.rows)]
        stack: list[Position] = [self.start]
        visited[self.start[0]][self.start[1]] = True
        parent: dict[Position, Optional[Position]] = {self.start: None}

        while stack:
            row, col = stack.pop()
            if (row, col) == self.goal:
                path: Path = []
                while (row, col) != self.start:
                    path.append((row, col))
                    parent_position = parent[(row, col)]
                    assert parent_position is not None
                    row, col = parent_position
                path.append(self.start)
                path.reverse()
                return path

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                if self.is_valid_move(new_row, new_col) and not visited[new_row][new_col]:
                    stack.append((new_row, new_col))
                    visited[new_row][new_col] = True
                    parent[(new_row, new_col)] = (row, col)

        return None

    def bfs_maze_solver(self) -> Optional[Path]:
        visited = [[False]*self.cols for _ in range(self.rows)]
        queue = deque([self.start])
        visited[self.start[0]][self.start[1]] = True
        parent: dict[Position, Optional[Position]] = {self.start: None}

        while queue:
            row, col = queue.popleft()
            if (row, col) == self.goal:
                path: Path = []
                while (row, col) != self.start:
                    path.append((row, col))
                    parent_position = parent[(row, col)]
                    assert parent_position is not None
                    row, col = parent_position
                path.append(self.start)
                path.reverse()
                return path

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                if self.is_valid_move(new_row, new_col) and not visited[new_row][new_col]:
                    queue.append((new_row, new_col))
                    visited[new_row][new_col] = True
                    parent[(new_row, new_col)] = (row, col)

        return None

    def astar_maze_solver(self) -> Optional[Path]:
        open_set: list[tuple[int, Position]] = []
        closed_set: set[Position] = set()
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start)}
        parent: dict[Position, Position] = {}
        heapq.heappush(open_set, (f_score[self.start], self.start))

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == self.goal:
                path: Path = []
                while current in parent:
                    path.append(current)
                    current = parent[current]
                path.append(self.start)
                return path[::-1]

            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def heuristic(self, node: Position) -> int:
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])

    def get_neighbors(self, node: Position) -> list[Position]:
        row, col = node
        neighbors: list[Position] = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_move(new_row, new_col):
                neighbors.append((new_row, new_col))
        return neighbors

    def print_maze(self, path: Optional[Path] = None) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                if path and (row, col) in path:
                    print('*', end=' ')
                elif self.maze[row][col]:
                    print('#', end=' ')
                else:
                    print('.', end=' ')
            print()


def generate_random_maze(rows: int, cols: int, obstacle_probability: float) -> Maze:
    maze = [[random.random() < obstacle_probability for _ in range(cols)] for _ in range(rows)]
    maze[0][0] = False  # Ensure start point is not blocked
    maze[rows - 1][cols - 1] = False  # Ensure goal point is not blocked
    return maze


def main():
    rows = 10
    cols = 10
    obstacle_probability = 0.2

    maze = generate_random_maze(rows, cols, obstacle_probability)
    print("Random Maze:")
    MazeSolver(maze).print_maze()

    maze_solver = MazeSolver(maze)
    path_dfs = maze_solver.dfs_maze_solver()
    path_bfs = maze_solver.bfs_maze_solver()
    path_astar = maze_solver.astar_maze_solver()

    print("\nDFS Path:")
    if path_dfs:
        maze_solver.print_maze(path_dfs)
    else:
        print("No path found")

    print("\nBFS Path:")
    if path_bfs:
        maze_solver.print_maze(path_bfs)
    else:
        print("No path found")

    print("\nA* Path:")
    if path_astar:
        maze_solver.print_maze(path_astar)
    else:
        print("No path found")


if __name__ == "__main__":
    main()