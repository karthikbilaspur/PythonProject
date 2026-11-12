# ♟️ Chess vs Engine

A playable chess game built with Python — play against Stockfish (or a fallback random bot) in a clean, clickable Tkinter GUI.

No more typing moves like e2e4. Just click a piece, then click where you want to go.

Python
python-chess
Stockfish
License

✨ Features
Clickable board — click a piece to see legal moves, click again to move
Visual highlights for selected square, last move, legal moves, and check
Play as White or Black — engine moves first if you choose Black
3 Difficulty levels — Easy / Medium / Hard (Elo + depth)
Promotion, castling, en passant handled automatically via python-chess
Live evaluation — shows centipawn eval or mate-in-N in the status bar
Move list in SAN notation (e.g. 1. e4 e5 2. Nf3 ...)
Undo — takes back your move + the engine's reply
Save PGN — exports a timestamped .pgn file with headers
Graceful fallback — if Stockfish isn't found, it plays with a random-move bot so the app still runs
🚀 Quick Start

1. Install dependencies
pip install python-chess stockfish
2. Download Stockfish
Download Stockfish from stockfishchess.org and unzip it.

3. Point the app at Stockfish
Open main.py (or wherever your ChessGame class lives) and update this line:

self.engine_path = r"C:\path\to\stockfish.exe"  # <-- change this
Examples:

 Windows

self.engine_path = r"C:\Users\you\Downloads\stockfish\stockfish-windows-x86-64-avx2.exe"

macOS / Linux

self.engine_path = "/usr/local/bin/stockfish"
Tip: If you skip this step, the game still works — it will just use a random-move bot and print a warning in the console.

4.Run it
python main.py
🎮 How to Play
Action How
Move Click your piece → dots show legal moves → click a highlighted square
Capture Click an enemy piece highlighted as a legal target
Deselect Click any other square
New Game Click New Game (respects your Side + Difficulty choice)
Undo Click Undo — takes back 2 ply (you + engine)
Save Game Click Save PGN — creates game_YYYYMMDD_HHMMSS.pgn
Promotion: Currently auto-promotes to Queen. See Roadmap for the chooser popup.

⚙️ Difficulty
Level Elo Depth Feels like
Easy 800 8 Beginner / casual
Medium 1400 14 Club player
Hard 2200 20 Strong / near-master
Change it in the dropdown before clicking New Game.

📁 Project Structure
chess-game/
├── main.py            # ChessGame class + Tkinter UI
├── README.md          # This file
└── game_*.pgn         # Saved games (created when you click Save PGN)
📝 Example PGN Output
[Event "Casual vs Engine"]
[Site "?"]
[Date "2026.11.12"]
[Round "-"]
[White "Player"]
[Black "Engine"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 1-0
🛠️ Troubleshooting
Stockfish not found in console?

Check self.engine_path is correct and the file is executable.
On macOS/Linux, run chmod +x /path/to/stockfish.
ModuleNotFoundError: No module named 'chess'?

pip install python-chess stockfish
Board looks too small / fonts missing?

The app uses Segoe UI Symbol for pieces. On Linux/macOS, it will fall back to your system symbol font — pieces still render, just in a different style.
Engine is too slow on Hard?

Lower Hash in _init_engine() from 512 to 256, or use Medium.
🗺️ Roadmap
 Promotion chooser popup (Q / R / B / N)
 Drag-and-drop moves
 Eval bar + best-move arrow
 customtkinter dark theme
 Timers / clock
 Load PGN / FEN to resume a game
 Sound effects
🤝 Contributing
PRs welcome! Good first issues: promotion chooser, drag-and-drop, eval bar.

📄 License
MIT — do whatever you want with it, just keep the credit.

Made with python-chess + tkinter + stockfish.
