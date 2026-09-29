
# Maze Solver Project

A Python-based maze solver project that uses Depth-First Search (DFS), Breadth-First Search (BFS), and A\* search algorithms to find paths in a given maze.

## Features

*   **DFS**: Uses a stack-based approach to explore the maze depth-first
*   **BFS**: Uses a queue-based approach to explore the maze level by level
*   **A\* Search**: Uses heuristics to guide the search towards the goal
*   **Maze Visualization**: Prints the maze and path using ASCII characters

## Requirements

*   Python 3.x
*   `heapq` library for A\* search

## Usage

1.  Clone the repository: `git clone https://github.com/your-username/maze-solver.git`
2.  Navigate to the project directory: `cd maze-solver`
3.  Run the script: `python maze_solver.py`

## Example Maze

The example maze is defined as a 2D grid, where 0 represents an open path and 1 represents a wall:
```python
maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0]
]
Customization
Modify the maze variable to define your own maze
Change the start_point and end_point variables to specify the start and end points of the path
Contributing
Contributions are welcome! If you'd like to add new features or improve the existing code, feel free to submit a pull request.
License
This project is licensed under the MIT License. See LICENSE for details.