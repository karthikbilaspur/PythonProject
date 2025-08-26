# 2048 Game

A simple implementation of the popular puzzle game 2048 using Python and Tkinter.

Features
Gameplay: Use the W, A, S, and D keys to move tiles up, left, down, and right, respectively.
Scoring: The game keeps track of your score, which increases as you merge tiles.
Undo: You can undo your last move by clicking the "Undo" button.
Restart: You can restart the game by clicking the "Restart" button.
AI Modes: The game includes two AI modes: Random AI and Minimax AI. The Random AI makes random moves, while the Minimax AI uses the minimax algorithm to make moves.

Requirements
Python 3.x
Tkinter (comes bundled with Python)

How to Run
Save the 2048.py and logic.py files in the same directory.
Run the 2048.py file using Python (e.g., python 2048.py).
The game window will appear, and you can start playing.

Code Structure
The code is divided into two files:
2048.py: This file contains the game logic and GUI implementation using Tkinter.
logic.py: This file contains the game logic and AI implementation.

AI Implementation
The game includes two AI modes:
Random AI: This AI makes random moves.
Minimax AI: This AI uses the minimax algorithm to make moves. The minimax algorithm evaluates the game state and predicts the best move based on the evaluation.
