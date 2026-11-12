# 🏴‍☠️ Grid Explorer

A fun terminal-based treasure hunt game. You are the explorer E on a hidden grid. Find the treasure T before you run out of lives!

No libraries needed — just pure Python.

🎮 How to Play
Save the game as game.py
Run it:
python game.py
Choose a level
Move with commands:
up / down / left / right
Type quit anytime to exit
Type y to play again, n to stop
🗺️ Legend
Symbol - Meaning
E - You - The Explorer
T - Treasure - Hidden, find this to win!
X - Wall / Rock - You cannot walk through it
B - Bomb - Hidden! Step on it and you lose a life
Bombs and Treasure are hidden until the game ends. Walls are visible so you can plan your path.

🎚️ Levels
Level Grid Size Walls Bombs Lives
1.Easy 5 x 5 3 1 3
2. Medium 7 x 7 8 3 3
3. Hard 10 x 10 15 5 3
🔥 Hot / Cold Radar
The game tells you how close you are to the treasure after every move:

🔥🔥 VERY HOT! — Treasure is right next to you (distance = 1)
🔥 Hot! — You are close (distance <= 3)
🌡️ Warm... — Getting closer (distance <= 5)
❄️ Cold... — Still far (distance <= 8)
🧊 FREEZING! — Very far away
Distance is calculated as Manhattan Distance:

distance = |your_row - treasure_row| + |your_col - treasure_col|
⭐ Scoring System
You start with 1000 points.

Action Score Change
Every move -10 points
Step on a Bomb -100 points + -1 Life
Find the Treasure Game ends, you keep your remaining score
Goal: Find the treasure in the fewest moves possible to keep a high score!

❤️ Lives System
You start with 3 lives
Stepping on a hidden bomb costs 1 life
If lives reach 0, it's GAME OVER
Stepping on the same bomb twice does NOT cost you again
🧱 Walls & Movement
You cannot walk outside the grid — you'll get You hit the border wall!
You cannot walk through X walls — you'll get There's a rock wall there!
Invalid commands like jump will show Invalid move!
🏆 Winning
When you step on the treasure cell, you win and see:

🎉 CONGRATULATIONS! YOU FOUND THE TREASURE!
🏆 Level: HARD
⭐ Final Score: 720
🎯 Total Moves: 18
⏱️ Time Taken: 45 seconds
❤️ Lives Left: 2
🛠️ Requirements
Python 3.6+
No external packages needed
Uses only random, time, os (built-in)
💡 Future Ideas
 Moving enemies that chase you
 2-Player mode
 Coins / Power-ups to gain extra lives
 Save High Score to a file
 Fog of war — only see nearby cells
📁 Project Structure
Grid-Explorer/
├── game.py       # The main game code
└── README.md     # This file
Made with ❤️ in Python. Happy Hunting!
