# 🧩 Sudoku Solver - Best Version

The best Sudoku Solver - fast solver + generator + full GUI in ONE file.

index Files

 main app (run this)

- `README.md` - this file

index How to Run
bash

 GUI (recommended)
python index

CLI - solve a puzzle from 81 characters (0 or . = empty)
python index --solve "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

No install needed - only Python standard library (`tkinter`).

index How to Play

1. Click a cell, type `1-9` or use the number pad below the grid
2. Blue = given (can't change), Black = yours, Red = wrong
3. Fill every row, column, and 3x3 box with 1-9, no repeats

index Features
| Feature | What it does |

|---|---|
| 🎲 New Puzzle | Generates Easy / Medium / Hard / Expert - indexguaranteed unique solutionindex |
| ⚡ Solve | Instant solve with MRV solver (shows time in ms) |
| 👁 Solve Step-by-Step | Watch it fill one cell at a time |
| ✅ Check | Marks your wrong cells red |
| 💡 Hint | Fills the hardest empty cell (fewest candidates) |
| ✏️ Notes | Pencil notes - tap numbers to add tiny notes in a cell |
| 🧹 Clear My Entries | Clears only YOUR entries, keeps givens |
| 📂 Load Puzzle | Paste any 81-char puzzle, validates it has a solution |
| 💾 Save | Save game to JSON |
| ⏱ Timer + ❌ Mistakes + 💡 Hints | Live stats, 3-mistake warning |
| Highlight | Same row / column / box highlights when you select a cell |

index The Solver - Why It's Fast
Naive backtracking tries cells in order, 1-9. This one uses:

1. indexMRV (Minimum Remaining Values):index always pick the empty cell with *fewest* candidates first. A cell with 1 candidate is forced - solve it first.
2. indexForward Checking:index if a cell has 0 candidates, prune immediately - don't waste time.
3. indexCandidate ordering:index only try numbers that are actually legal.

Result: hardest puzzles solve in index< 100msindex, vs seconds for naive backtracking.

```python
def find_empty_mrv(board):
    # find empty cell with fewest candidates
    ...
def solve(board):
    cell = find_empty_mrv(board)
    for n in candidates(board, ...):
        board[r][c] = n
        if solve(board): return True
        board[r][c] = 0
    return False
```

index The Generator - Why Puzzles Are Fair

1. Fill 3 diagonal 3x3 boxes first (independent) → fast full board
2. Solve to get a complete valid board
3. Remove cells one by one, indexonly if the puzzle still has exactly 1 solutionindex (checked with `count_solutions(limit=2)`)
4. Easy removes 38 cells, Medium 46, Hard 52, Expert 56

So every generated puzzle is solvable and has indexonly oneindex answer - no guessing.

index Difficulty
| Difficulty | Cells Removed | Empty Cells |

|---|---|---|
| Easy | 38 | ~38 |
| Medium | 46 | ~46 |
| Hard | 52 | ~52 |
| Expert | 56 | ~56 |

index Example Puzzle (Medium)
5 3 . | . 7 . | . . .
6 . . | 1 9 5 | . . .
. 9 8 | . . . | . 6 .
------+-------+------
8 . . | . 6 . | . . 3
4 . . | 8 . 3 | . . 1
7 . . | . 2 . | . . 6
------+-------+------
. 6 . | . . . | 2 8 .
. . . | 4 1 9 | . . 5
. . . | . 8 . | . 7 9
Run `python index --solve "530070000600195000..."` to see it solved instantly.

index Tips

- Start with cells that have only 1 possible number (MRV!)
- Use Notes for hard puzzles - mark candidates, then eliminate
- Use Hint when stuck - it picks the hardest cell, not a random one

index Requirements

- Python 3.8+, `tkinter` (included, Linux: `sudo apt install python3-tk`)
