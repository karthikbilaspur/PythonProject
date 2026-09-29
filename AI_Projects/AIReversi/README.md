Reversi Game
A simple implementation of the classic Reversi game with an AI opponent using the Minimax algorithm with alpha-beta pruning.
Game Description
Reversi is a two-player strategy board game where players take turns placing tiles, trying to capture their opponent's tiles by sandwiching them between their own. The goal is to have the most tiles on the board when it's full or your opponent can't make a move.
Features
Play against an AI opponent using the Minimax algorithm with alpha-beta pruning
Adjustable AI strength by changing the max_depth variable
Simple command-line interface for playing the game
Requirements
Python 3.x
NumPy library
How to Play
Clone the repository and navigate to the game directory
Run the game using python main.py
Enter your moves in the format "row column" (e.g., "4 4")
The AI will make its moves automatically
The game ends when the board is full or there are no more valid moves left
AI Strength
The AI's strength can be adjusted by changing the max_depth variable in the Minimax class. A higher value will make the AI stronger but slower.
Contributing
Contributions are welcome! If you'd like to improve the game or add new features, feel free to fork the repository and submit a pull request.
License
This game is licensed under the MIT License. See LICENSE for details.
