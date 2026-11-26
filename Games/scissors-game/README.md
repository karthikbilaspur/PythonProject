# Scissors-Paper Python Project

One runnable file combining your 2 games.

 Files

- `index.py` - main game (run this)
- `README.md` - this file

 How to Run

```bash
python index.py
```

 Game Modes

 1. Rock Paper Scissors Lizard Spock (Classic)

Choices: rock, paper, scissors, lizard, spock

| Choice | Beats |

|---|---|
| rock | scissors, lizard |
| paper | rock, spock |
| scissors | paper, lizard |
| lizard | paper, spock |
| spock | rock, scissors |

2.Scissors Paper Water Gun Stone (Custom)
Choices: scissors, paper, water, gun, stone

| Choice | Beats |

|---|---|
| scissors | paper, gun |
| paper | stone, water |
| water | gun, scissors |
| gun | stone, paper |
| stone | scissors, water |

 Features

- Mode picker at start (1 / 2 / q)
- Score tracking: You / Computer / Ties
- Round history (last 5 rounds with `s`)
- Win explanation, e.g. "Rock crushes Scissors"
- Input validation - invalid choice asks again
- `q` to quit anytime, `s` to see score
- Play another mode without restarting

 How It Works
Same logic as your original files:

```python
if user_choice == computer_choice:
    tie
elif computer_choice in beats[user_choice]:
    you win
else:
    computer wins
```

Each choice beats 2 and loses to 2, so the game is balanced.

 Requirements

- Python 3.8+
- Only standard library (`random`) - no install needed
