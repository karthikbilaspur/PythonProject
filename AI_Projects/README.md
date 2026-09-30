# 🤖 AI Projects

A collection of 21 Python projects covering chatbots, machine learning, game AI, generative AI, NLP and developer tools. Each folder is self-contained and has its own README with more detail.

Part of [PythonProject](https://github.com/karthikbilaspur/PythonProject).

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Chatbots](#-chatbots)
- [Machine Learning & Data](#-machine-learning--data)
- [Game AI](#-game-ai)
- [Generative & Creative AI](#-generative--creative-ai)
- [Tools & Utilities](#-tools--utilities)

- [Getting Started](#-getting-started)
- [Concepts Covered](#-concepts-covered)
- [Known Issues](#-known-issues)

- [Contributing](#-contributing)

## 📊 Project Overview

| Category | Projects |
|----------|----------|

| Chatbots | `aI_chatbot` (6 variants), `ai_diverse` |
| ML & Data | `AI_Crop_Optimization`, `AI_Simulation_Trading`, `AI_Objects` |
| Game AI | `ai_flappy_bird`, `ai_guess_a_number`, `ai_maze`, `ai_reversi`, `ai_tic_tae_toe`, `ai_tron` |
| Generative & Creative | `AI_Interactive`, `ai_music`, `ai_image_generator` |
| Tools & Utilities | `ai_assistant`, `ai_password`, `aI_code_review`, `ai_calculator`, `ai_address_bok`, `ai_receipe`, `AI_Comparative` |

---

## 💬 Chatbots

 `aI_chatbot/`: Six chatbot approaches, from simple to advanced

| Variant | Approach | Key Tech |
|---------|----------|----------|

| `rule based/` | Keyword matching against a dictionary of intents | `random` only, no dependencies |
| `normal_chatbot/` | Neural network intent classifier trained on `instensts.json` | Keras, NLTK, bag-of-words, pickle |
| `customer_chatbot/` | Naive Bayes intent classifier; escalates issues to support via a POST request | scikit-learn, NLTK, TF-IDF, requests |
| `ai_powered_chatbots/` | Transformer-based intent classification plus VADER sentiment analysis | Hugging Face Transformers, PyTorch, NLTK |
| `virtual_assitance/` | Assistant for time, date, weather, news and web search | requests, OpenWeatherMap API, News API |
| `transaction_chatbot/` | Banking-style flows: auth, balance, bill pay, transfers, payment gateways, translation | requests, hashlib |

> The weather and news assistant needs your own API keys, and the banking chatbot calls placeholder endpoints. Treat it as a design demo, not a working banking client.

 `ai_diverse/`: Chatbot with a GUI
Keras intent classifier with spaCy and a Tkinter chat window (`chatbot.py`).

---

## 📈 Machine Learning & Data

 `AI_Crop_Optimization/`: Crop recommendation app
A Streamlit app (`streamlight.py`) that predicts the best crop from soil and weather inputs: N, P, K, temperature, humidity, pH and rainfall. Uses `LogisticRegression` with `StandardScaler` and shows a classification report. Includes the dataset (`data.xlsx`) and an exploration notebook (`agriculture.ipynb`).

```bash
streamlit run streamlight.py
```

 `AI_Simulation_Trading/`: Sentiment-driven trading simulation
Pulls stock history with `yfinance`, scores news sentiment with NLTK VADER, trains a Random Forest classifier and simulates trades, printing final capital and accuracy.

 `AI_Objects/`: Airplane detection
OpenCV plus a pre-trained Caffe model that detects airplanes in images and video by classifying patches around corner feature points (`detect_airplanes`).

---

## 🎮 Game AI

| Project | AI Technique | Tech |

|---------|-------------|------|

| `ai_flappy_bird/` | A neural network controls the bird (`chat.py`) | Pygame, NumPy |
| `ai_guess_a_number/` | AI guesses your number using binary search, with 3 difficulty levels | Python standard library |
| `ai_maze/` | Solves mazes with DFS, BFS and A\*, and can generate random mazes | `collections.deque`, `heapq` |
| `ai_reversi/` | Minimax with alpha-beta pruning; adjustable difficulty via `max_depth` | NumPy |
| `ai_tic_tae_toe/` | Play vs AI or vs a human in the browser, with score tracking | `http.server` (no dependencies) |
| `ai_tron/` | Two-player light-cycle game with power-ups and scoring | Pygame |

---

## 🎨 Generative & Creative AI

 `AI_Interactive/`: Interactive storytelling and text adventures

- `storyverse_ai/` has four story generators built on a T5 model from Hugging Face:
  - `chronicle_weavier.py`: freeform stories with story memory, user profiles, 1-5 ratings and Markdown export.
  - `vault_of_genesis.py`: a branching RPG built as a state machine, with HP, inventory and multiple endings.
  - `echo_scripe.py`: a minimalist, infinite story loop.
  - `storyverse.py`: all three merged into one engine.
- `adventure_engine/` is a dataclass-based text adventure engine with an effect system, a requirement system (a chest needs a key), save/load to JSON, and multiple endings.
- `adventure_simple_pro/` is a lighter version with inventory, three endings and input validation.

 `ai_music/`: Algorithmic music composer
Three engines combined by `composer.py`:

- Melody: Markov-chain melodies with seed support.
- Harmony: chord-based harmonies in 5 styles (classical, jazz, pop, minor, blues).
- Rhythm: genre-aware rhythm patterns with time-signature handling.

Run `main.py` for the CLI. Compositions are exported as JSON.

 `ai_image_generator/`
Tkinter desktop app for text-to-image generation (Stable Diffusion via `diffusers`, plus a DALL-E Mini option) with brightness and contrast editing and save-to-disk.

---

## 🛠️ Tools & Utilities

 `ai_assistant/`: Adaptive vocabulary trainer
A self-learning word system:

- `brain.py`: WordNet hints and definitions, level detection, weakness analysis and SM-2 spaced repetition, backed by SQLite.
- `word_engine.py`: word operations and category tracking.
- `quiz_engine.py`: adaptive quiz mixing your `words.json` with the OpenTDB API, with auto-hints after repeated failures.
- `voice_mode.py`: optional voice quiz (pyttsx3).
- `app.py`: FastAPI endpoints (`/`, `/random_word`, `/search`).
- `main.py`: CLI entry point.

 `ai_password/`: Password generator and strength analyzer

- `password_engine.py`: secure (via `secrets`), Markov-based, pattern-based, memorable (word-phrase) and combined "extreme" modes.
- `strength_analyzer.py`: entropy and crack-time estimates.
- `main.py`: CLI menu. `app.py`: FastAPI endpoints (`/gen_secure`, `/gen_memorable`, `/gen_extreme`, `/check`).

 `aI_code_review/`: Static code reviewers
Zero-dependency reviewers built on Python's `ast` module.

- `PythonCode/`: flags unused imports, undefined variables, PEP 8 naming problems, long functions and high cyclomatic complexity.
- `TwoLanguageReview/`: unified `review_code(code, language)` API covering Python and Java (structure, line length, method length, naming).

 `ai_calculator/`
Tkinter calculators. `calculator/` is a basic one; `ai/` adds scientific functions, a length unit converter and natural-language math questions.

 `ai_address_bok/`
Tkinter contact manager backed by SQLite, with add, update, delete and search.

 `ai_receipe/`
Recipe manager with user registration and login (bcrypt), ingredient-based recipe suggestions, grocery lists, ratings, bookmarks, NLTK tokenization and sharing to Twitter via Tweepy.

 `AI_Comparative/`
Rule-based generator for comparative and superlative adjectives (`tall → taller / tallest`, `beautiful → more / most beautiful`), with irregular forms and a syllable counter. Standard library only.

---

## 🚀 Getting Started

```bash
git clone https://github.com/karthikbilaspur/PythonProject.git
cd PythonProject/AI_Projects

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

Install dependencies per project, since they differ widely:

```bash
# Examples
pip install streamlit scikit-learn pandas numpy          # AI_Crop_Optimization
pip install pygame numpy                                 # ai_flappy_bird, ai_tron
pip install transformers torch                           # AI_Interactive/storyverse_ai
pip install fastapi uvicorn                              # ai_password, ai_assistant
pip install nltk keras                                   # chatbots

python -m nltk.downloader punkt wordnet vader_lexicon    # NLTK data
```

Then run a project:

```bash
cd ai_maze
python maze.py
```

Requires Python 3.8+. Projects with a `requirements.txt` (`ai_music`, `ai_password`, `aI_chatbot/ai_powered_chatbots`) can use `pip install -r requirements.txt`.

## 🧠 Concepts Covered

- NLP: intent classification, TF-IDF, bag-of-words, sentiment analysis (VADER), T5 text generation, tokenization
- Machine learning: Logistic Regression, Naive Bayes, Random Forest, neural networks (Keras, PyTorch)
- Search & game AI: DFS, BFS, A\*, Minimax with alpha-beta pruning, binary search
- Generative AI: Stable Diffusion, transformer text generation, Markov-chain music
- Software design: dataclasses, state machines, modular engines, REST APIs (FastAPI), SQLite, GUI apps (Tkinter), AST analysis
- Learning systems: spaced repetition (SM-2), adaptive difficulty

## ⚠️ Known Issues

Worth fixing to make the folder easier to use:

- Some READMEs name scripts that differ from the actual files (for example `AI_Objects` mentions `detect_airplanes.py` but the file is `objects.py`; `AI_Comparative` mentions `adjective.py` but the file is `script.py`).
- `AI_Objects/objects.py` imports `InitCaffe`, which is not included, so it will not run as is. The pre-trained Caffe model is also not included.
- `AI_Interactive/storyverse_ai/README.md` mentions `storyverse_unified.py`, but the file is `storyverse.py`. `chronicle_weavier.py` and `echo_scripe.py` have spelling variations in their names.
- `AI_Crop_Optimization/READEME.md` is misspelled and refers to `app.py`, but the app file is `streamlight.py`.
- `aI_chatbot/rule based/README.md` is empty.
- `pip install ... pickle json hashlib` in some READMEs is wrong; those are built into Python.
- Several projects have no `requirements.txt`.

## 🤝 Contributing

Fork the repo, create a branch, and open a pull request. Bug fixes, new projects and documentation improvements are welcome.

## 📫 Contact

GitHub: [@karthikbilaspur](https://github.com/karthikbilaspur)

---

⭐ If you find these projects useful, consider starring the repo!
