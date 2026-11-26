<div align="center">

# 🎮 Games

### 28 self-contained Python games: board classics, arcade action, brain teasers and creative toys

*Part of the [PythonProject](../README.md) collection.*

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Games](https://img.shields.io/badge/Games-28-8A2BE2?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

![Pygame](https://img.shields.io/badge/Pygame-1E8449?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![CLI](https://img.shields.io/badge/Terminal-CLI-black?style=flat-square&logo=gnubash&logoColor=white)

[**Game Catalog**](#-game-catalog) ·
[**Quick Start**](#-quick-start) ·
[**Folder Layout**](#-folder-layout) ·
[**Contributing**](#-contributing) ·
[**Notes**](#-good-to-know)

</div>

---

## ✨ Overview

This folder is a playground of small, readable Python games. Each game lives in its own directory and runs on its own, with no shared engine and nothing to set up globally. They are written to be played, read, modified and learned from.

The collection spans several styles of interface:

| Interface | What to expect |
|:---|:---|
| 🖥️ **Terminal (CLI)** | Text-based games that run straight from the command line |
| 🕹️ **Pygame** | Windowed, real-time games with graphics and input handling |
| 🪟 **Tkinter** | Desktop GUI games using Python's built-in toolkit |
| 🌐 **Streamlit** | Browser-based versions that run as a local web app |

---

## 🗂️ Game Catalog

> Click a game name to jump to its folder.

### ♟️ Board & Strategy

| Game | Description |
|:---|:---|
| [**Chess**](chess) | The classic two-player strategy board game |
| [**Connect Four**](connect-four) | Drop discs and line up four. Includes **minimax**, **NumPy** and **Streamlit** versions |
| [**Ludo**](ludo-game) | Race your tokens home in this classic dice-and-board game |
| [**Scrabble**](scrabble-game) | Build words and score points |
| [**Go Connect**](go-connect) | A connection-style strategy game |
| [**Dot Connect**](dot-connect-game) | Link dots to complete the board |
| [**Blackjack**](blackjack) | Beat the dealer without going over 21 |

### 🏹 Arcade & Action

| Game | Description |
|:---|:---|
| [**Tower Defense**](tower-defense) | Place defenses and hold back incoming waves |
| [**Bubble Shooter**](bubble-shooter) | Aim, shoot and pop matching bubbles |
| [**Match-3**](match-3-game) | Swap tiles to line up three or more |
| [**Infinite Runner**](infinite-runner) | Keep running and dodge obstacles as long as you can |
| [**Drag Racing**](drag-racing) | Time your launch and win the straight-line race |

### 🧩 Puzzle & Logic

| Game | Description |
|:---|:---|
| [**Sudoku Solver**](sudoku-solver) | Solve Sudoku grids automatically |
| [**Mastermind**](mastermind) | Crack the hidden code using feedback from each guess |
| [**Maze**](maze) | Find your way through the maze |
| [**Memory Game**](memory-game) | Flip cards and match the pairs |
| [**Puzzle Game**](puzzle-game) | A sliding and arranging style puzzle |
| [**Door Puzzle**](door-puzzle) | Work out which doors to open and in what order |
| [**Grid Explorer**](grid-explorer) | Navigate and explore a grid world |
| [**Linear Search Game**](linear-search) | Learn how linear search works by playing it |

### 🎨 Creative & Simulation

| Game | Description |
|:---|:---|
| [**Gravity Simulator**](gravity-simulator) | Watch bodies move under gravity |
| [**Ink Art**](ink-art) | Create ink-style drawings |
| [**Draw Game**](draw-game) | Sketch and draw interactively |
| [**Link Sketch**](link-sketch) | Draw by linking points |

### 🔤 Word, Text & Misc

| Game | Description |
|:---|:---|
| [**Text Adventure**](hand-text-based-adventure-game) | Explore a story-driven world through typed commands |
| [**Lyric Game**](lyric) | A lyrics guessing game |
| [**Scissors Game**](scissors-game) | A rock-paper-scissors style hand game |
| [**Game Collection v2**](game-collection-v2) | Several mini-games bundled together |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/karthikbilaspur/PythonProject.git
cd PythonProject/Games
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Pick a game and run it

```bash
cd chess
pip install -r requirements.txt    # only if the game has one
python index.py
```

> 💡 **Tip:** entry-point filenames can differ between games. If `index.py` is not present, look for `main.py` or the main `.py` file inside the game's folder.

### Common dependencies

Install only what the game you want needs:

```bash
pip install pygame        # Pygame-based games
pip install numpy         # NumPy-based versions (e.g. Connect Four)
pip install streamlit     # Streamlit versions
streamlit run <app_file>.py
```

Tkinter ships with most Python installers. On some Linux distributions install it with `sudo apt install python3-tk`.

---

## 📁 Folder Layout

```text
Games/
├── chess/                          # Chess
├── connect-four/                   # Minimax, NumPy and Streamlit versions
├── blackjack/                      # Card game
├── ludo-game/                      # Board game
├── tower-defense/                  # Arcade strategy
├── sudoku-solver/                  # Puzzle solver
├── scrabble-game/                  # Word game
├── mastermind/                     # Code-breaking puzzle
├── match-3-game/                   # Tile matching
├── bubble-shooter/                 # Arcade
├── infinite-runner/                # Arcade
├── drag-racing/                    # Racing
├── maze/                           # Maze
├── memory-game/                    # Card matching
├── puzzle-game/                    # Puzzle
├── door-puzzle/                    # Logic puzzle
├── gravity-simulator/              # Simulation
├── grid-explorer/                  # Grid navigation
├── dot-connect-game/               # Connection puzzle
├── go-connect/                     # Strategy
├── ink-art/                        # Creative
├── draw-game/                      # Creative
├── link-sketch/                    # Creative
├── scissors-game/                  # Hand game
├── hand-text-based-adventure-game/ # Text adventure
├── lyric/                          # Lyric guessing
├── linear-search/                  # Algorithm game
└── game-collection-v2/             # Mini-game bundle
```

---

## 🎯 What You Can Learn Here

- **Game loops and event handling** with Pygame and Tkinter
- **Game AI**, such as minimax search in Connect Four
- **Grid and board representations** using lists and NumPy arrays
- **Search and pathfinding** ideas through maze, grid and puzzle games
- **Turning scripts into web apps** with Streamlit
- **Structuring small projects**: one idea, one folder

---

## 🤝 Contributing

Contributions are welcome, whether that is a bug fix, a new game or better documentation.

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-new-game`
3. Add your game in its own folder under `Games/`
4. Include a short README and a `requirements.txt` if it has dependencies
5. Commit your changes and open a pull request

**Ideas for new games:** Snake, Pong, Tic-Tac-Toe, Hangman, Minesweeper, 2048, Tetris.

---

## ⚠️ Good to Know

- 🐍 **Python 3.10+** is recommended.
- 🧩 **Use a virtual environment** so each game's dependencies stay separate.
- 🖼️ **Window-based games** need a desktop environment and will not open on a headless server.
- 🎓 **These are learning projects.** They favor readability over polish and are meant to be explored and changed.

---

## 📄 License

Released under the [MIT License](../LICENSE).

<div align="center">

**Built for learning. Play a game, read the code, then make it better. 🎲**

[⬆ Back to top](#-games)

</div>
