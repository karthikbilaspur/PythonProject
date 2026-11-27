<div align="center">

# 🐍 PythonProject

### A giant, hands-on Python lab: 370+ scripts, apps, games, bots and ML demos in one repo

*From a 40-line bubble sort to an AES-256 file vault, a Flask + TensorFlow digit recognizer, and an AWS cost-cutting Lambda.*

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Projects](https://img.shields.io/badge/Projects-160%2B-8A2BE2?style=for-the-badge)
![Python Files](https://img.shields.io/badge/Python%20Files-370%2B-success?style=for-the-badge)
![Tests](https://img.shields.io/badge/Test%20Files-30-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

[**Featured**](#-featured-projects) ·
[**Catalog**](#-project-catalog) ·
[**Quick Start**](#-quick-start) ·
[**Testing**](#-testing) ·
[**Notes**](#-good-to-know)

</div>

---

## ✨ At a Glance

| 🎮 Games | 🤖 AI Projects | 🧰 Utilities | 🕸️ Scrapers & Trackers | 📊 Data & ML | 🧮 Algorithms |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **28** | **20** | **Dozens** | **Many** | **Many** | **Many** |

Every folder is a self-contained project. Pick one, read its README (where it has one), and run it. There is no framework to learn and nothing to set up globally.

---

## 🏆 Featured Projects

The most complete, structured and tested projects in the repo. They are good places to start.

### 🛡️ [`file-forge`](file-forge): *Safe-by-default file toolkit*
A tested package that merges a pile of standalone scripts into one CLI.
- **Organize** downloads by rule or date, with dry run by default and **undo** for every applied move
- **Dedupe** by size, then partial hash, then full hash, quarantining instead of deleting
- **Vault** encryption with scrypt + chunked **AES-256-GCM** and tamper/truncation detection
- **Carve** JPEG, PNG, PDF and ZIP files out of disk images, with JSON and CSV reports
- **Search** with an incremental SQLite index, BM25 and optional embeddings
- Resumable downloads, a live folder watcher and hash-baseline integrity checks
- `Typer` · `AES-GCM` · `SQLite` · **49 tests**

### ☁️ [`aws-demo-toolkit`](aws-demo-toolkit): *EC2/RDS cleanup + SQS service*
- Lambda handler that safely stops or cleans up **opt-in tagged** EC2 and RDS resources (RDS gets a final snapshot)
- Stateless SQS service behind a **Flask API** with API-key auth and validation
- Tested with `moto`, so no real AWS account is needed

### 📚 [`book`](book): *Library management system*
- Books with copy counts, members, loans with due dates, **fines** and overdue reports
- **SQLite** storage, an `argparse` CLI and a **Flask API** on one shared service layer
- ISBN-10/13 checksum validation, domain errors mapped to HTTP codes, deterministic tests

### ✍️ [`handwritten-recognition`](handwritten-recognition): *Digits + letters recognizer*
- **Flask + TensorFlow** web app with a drawing canvas and image upload
- Single 36-class model or separate digit and letter models
- Top-3 predictions with confidence, a preprocessing preview, REST API and training with augmentation

### 🧑‍🦱 [`face-vision`](face-vision): *Face verification web app*
- Upload two images and get a model-based match result
- **Flask + OpenCV + DeepFace (FaceNet)** with input validation and unit tests

### 📸 [`photo-cleaner`](photo-cleaner): *Smart photo cleaner*
- Offline face and eye-open detection to flag the **best** photos in a gallery
- User accounts with hashed passwords, a SQLAlchemy DB and per-user history

### 📰 [`fake-news-credible-auditor`](fake-news-credible-auditor): *Article credibility pipeline*
- Modular pipeline: fetcher → extractor → scoring → report, plus an evaluation module and CLI

### 🧠 [`ai-projects`](ai-projects): *20 mini AI projects*
Chatbots, game AI, generative music, a voice-enabled assistant and more. See the [AI catalog](#-ai-projects) below.

---

## 📦 Project Catalog

> Folder names link straight to the code.

### 🤖 AI Projects
All live under [`ai-projects/`](ai-projects).

| Project | What it is |
|---|---|
| [`ai_assistant`](ai-projects/ai_assistant) | Assistant with voice mode, quiz engine, word engine, file manager and persistent memory |
| [`ai_interactive`](ai-projects/ai_interactive) | Text-adventure engines and **StoryVerse AI** |
| [`ai_music`](ai-projects/ai_music) | Procedural composer with separate melody, harmony and rhythm engines |
| [`ai_diverse`](ai-projects/ai_diverse) | Keras intent-classifier chatbot with spaCy and a Tkinter GUI |
| [`ai_crop_optimization`](ai-projects/ai_crop_optimization) | Streamlit crop recommender (logistic regression on soil and weather) |
| [`ai_simulation_trading`](ai-projects/ai_simulation_trading) | News sentiment (NLTK + VADER) feeding a random-forest stock-price predictor |
| [`ai_code_review`](ai-projects/ai_code_review) | Zero-dependency static analyzer for Python: style, complexity, security risks and dead code |
| [`ai_image_generator`](ai-projects/ai_image_generator) | Image generation script |
| [`ai_objects`](ai-projects/ai_objects) | Airplane detection in images and video with OpenCV + a Caffe model |
| [`ai_comparative`](ai-projects/ai_comparative) | Comparative and superlative generator for English adjectives |
| [`ai_reversi`](ai-projects/ai_reversi) · [`ai_tron`](ai-projects/ai_tron) · [`ai_tic_tae_toe`](ai-projects/ai_tic_tae_toe) · [`ai_maze`](ai-projects/ai_maze) · [`ai_flappy_bird`](ai-projects/ai_flappy_bird) · [`ai_guess_a_number`](ai-projects/ai_guess_a_number) | Game-playing AIs |
| [`ai_password`](ai-projects/ai_password) · [`ai_calculator`](ai-projects/ai_calculator) · [`ai_address_book`](ai-projects/ai_address_book) · [`ai_receipe`](ai-projects/ai_receipe) | Password engine, calculator, address book and a recipe manager with grocery lists and ratings |

### 🎮 Games
All live under [`Games/`](Games).

| | | | |
|---|---|---|---|
| [Chess](Games/chess) | [Connect Four](Games/connect-four) *(minimax, NumPy and Streamlit versions)* | [Blackjack](Games/blackjack) | [Ludo](Games/ludo-game) |
| [Tower Defense](Games/tower-defense) | [Sudoku Solver](Games/sudoku-solver) | [Scrabble](Games/scrabble-game) | [Mastermind](Games/mastermind) |
| [Match-3](Games/match-3-game) | [Bubble Shooter](Games/bubble-shooter) | [Infinite Runner](Games/infinite-runner) | [Drag Racing](Games/drag-racing) |
| [Maze](Games/maze) | [Memory Game](Games/memory-game) | [Puzzle Game](Games/puzzle-game) | [Door Puzzle](Games/door-puzzle) |
| [Gravity Simulator](Games/gravity-simulator) | [Grid Explorer](Games/grid-explorer) | [Dot Connect](Games/dot-connect-game) | [Go Connect](Games/go-connect) |
| [Ink Art](Games/ink-art) | [Draw Game](Games/draw-game) | [Link Sketch](Games/link-sketch) | [Scissors Game](Games/scissors-game) |
| [Text Adventure](Games/hand-text-based-adventure-game) | [Lyric Game](Games/lyric) | [Linear Search Game](Games/linear-search) | [Game Collection v2](Games/game-collection-v2) |

### 🧮 Algorithms & Data Structures

| Project | Highlights |
|---|---|
| [`super-algo`](super-algo) | Organized library: **dp** (coin change, 0/1 knapsack) · **graph** (A\*, BFS/DFS maze, shortest path) · **puzzles** (N-Queens, Sudoku) · **searching** (binary, KMP, sequential) · **sorting** (5 sorts + a sorting race) |
| [`algorithm`](algorithm) | Algorithms playground |
| [`data-structures`](data-structures) · [`linked-list`](linked-list) · [`queue-lab`](queue-lab) | Core structures, all in one place |
| [`binary-search`](binary-search) · [`sequential-search`](sequential-search) | Search suites |
| [`bubble-sort`](bubble-sort) · [`insertion-sort`](insertion-sort) · [`selection-sort`](selection-sort) · [`merge-sort`](merge-sort) · [`quick-sort`](quick-sort) | Classic sorts |
| [`number`](number) · [`bitwise-operator`](bitwise-operator) · [`palindrome-checker`](palindrome-checker) · [`anagram`](anagram) | Number theory and string utilities (e.g. Fibonacci by matrix exponentiation) |

### 📊 Data Science & Machine Learning

| Project | Highlights |
|---|---|
| [`cancer`](cancer) · [`malaria`](malaria) · [`parkinsons-detection`](parkinsons-detection) · [`heart`](heart) | Health-prediction models. `heart` bundles training, a prediction API and an exercise/food logger |
| [`air-pollution-prediction`](air-pollution-prediction) · [`aqi-app`](aqi-app) | Air-quality analysis and a Streamlit AQI predictor |
| [`power-plant`](power-plant) · [`power-plant-2`](power-plant-2) | Power-plant output predictor |
| [`eda-project`](eda-project) | Load, clean, join and analyze demo CSVs |
| [`sentiment-analysis`](sentiment-analysis) · [`message-spam-detection`](message-spam-detection) · [`n-gram`](n-gram) · [`mega-suite`](mega-suite) | NLP: sentiment, spam, n-grams and text preprocessing |
| [`lane-detection`](lane-detection) · [`parking-space-detection`](parking-space-detection) · [`Blob`](Blob) · [`color-detector-ui`](color-detector-ui) | Computer vision |
| [`customer`](customer) | Customer segmentation datasets |

### 🔐 Security, Network & Crypto

| Project | Highlights |
|---|---|
| [`port-scanner`](port-scanner) · [`port-scanner-2`](port-scanner-2) | TCP port scanners |
| [`password-checker`](password-checker) · [`password-generator`](password-generator) · [`Password`](Password) | Pwned-password checks, generation and management |
| [`stego-isb`](stego-isb) | LSB image steganography |
| [`casear-convertor`](casear-convertor) · [`moorse`](moorse) | Caesar cipher and a full Morse code app |
| [`ssh-automation`](ssh-automation) · [`wifi-password`](wifi-password) · [`network`](network) | SSH host manager, saved-WiFi viewer, network tools |
| [`domain-name`](domain-name) · [`username-search`](username-search) · [`phone`](phone) | Domain availability, username lookup, phone-number parsing |

### 🕸️ Scrapers, Trackers & Market Data

| Project | Highlights |
|---|---|
| [`Trackers/`](Trackers) | **Price**, **pricing**, **product**, **wishlist** and **anime** trackers |
| [`best-seller`](best-seller) · [`product-scraper`](product-scraper) | Amazon best-seller and product scrapers |
| [`imdb-scrapper`](imdb-scrapper) · [`dev-to-scrapper`](dev-to-scrapper) · [`Gradient-Scrapper`](Gradient-Scrapper) · [`slideshare`](slideshare) | Content scrapers and downloaders |
| [`github-search`](github-search) · [`search`](search) · [`search-bot`](search-bot) | GitHub and Google Custom Search tools |
| [`stock-agent`](stock-agent) · [`stock-trailer`](stock-trailer) · [`nse`](nse) | Alpha Vantage, yfinance and NSE market data |
| [`live-update`](live-update) · [`live-conversion`](live-conversion) · [`open-weather`](open-weather) | Live scores, currency conversion, weather |

### 🧰 Productivity, Files & Automation

| Project | Highlights |
|---|---|
| [`backup`](backup) · [`backup-generator`](backup-generator) · [`rename-files`](rename-files) · [`downloader`](downloader) | File management |
| [`csv-to-excel`](csv-to-excel) · [`csv-to-json`](csv-to-json) · [`excel-formatter`](excel-formatter) · [`excel-to-merger`](excel-to-merger) | Spreadsheet and data conversion |
| [`pomodoro`](pomodoro) · [`pomodoro-timer`](pomodoro-timer) · [`time-saver`](time-saver) · [`audio-books`](audio-books) | Time tools and listening-time calculators |
| [`email-studio`](email-studio) · [`email-generator`](email-generator) · [`sms-automation`](sms-automation) · [`wish`](wish) | Email (MailForge Pro on Supabase), SMS and birthday-wisher automation |
| [`lifeops`](lifeops) · [`instavault`](instavault) · [`consolidate-suite`](consolidate-suite) · [`void-suite`](void-suite) · [`intra-tools`](intra-tools) · [`tools`](tools) | Personal dashboards and multi-tool suites |
| [`notepad-silence`](notepad-silence) · [`screen-tools`](screen-tools) · [`mutipe-convertor`](mutipe-convertor) · [`isbn-number`](isbn-number) · [`qr-generator`](qr-generator) | Notepad with spell check, screen capture, unit converter, ISBN and QR tools |
| [`sales-compounder`](sales-compounder) · [`GST`](GST) · [`easy-dinner`](easy-dinner) · [`coffee-machine`](coffee-machine) | Business and simulation systems (sales/inventory, GST, restaurant, beverage machine) |
| [`complaint-system`](complaint-system) · [`login`](login) · [`travel-map-app`](travel-map-app) | Django complaint system, Tkinter login, travel map |

### 🎨 Media, Creative & Fun

| Project | Highlights |
|---|---|
| [`audio`](audio) · [`dynamic-music-generator`](dynamic-music-generator) · [`sound-generation`](sound-generation) | Audio conversion and generation |
| [`Images`](Images) · [`Blending`](Blending) · [`blur-image`](blur-image) · [`GIN`](GIN) | Image toolkit GUI, blending, blur, GIF creator |
| [`animation`](animation) · [`crawl`](crawl) · [`national-flag`](national-flag) · [`emoji`](emoji) | Cellular automaton, Star Wars crawl, turtle flag, emoji picker |
| [`lifecode`](lifecode) · [`language`](language) · [`Advisor`](Advisor) · [`quote-generator`](quote-generator) | Streamlit and CLI curiosities |

### 🗃️ The A-to-Z Archive
Older script collections, grouped by the first letter of the file names:
[`T_Projects_Part1`](T_Projects_Part1) · [`T_Projects_With_Part2`](T_Projects_With_Part2) · [`T_Python_Codes_Part3`](T_Python_Codes_Part3) · [`T_Python_Codes_Part4`](T_Python_Codes_Part4) · [`U_Projects_Of_Python`](U_Projects_Of_Python) · [`V_Based_Python_Codes_Part1`](V_Based_Python_Codes_Part1) · [`W_Codes_Of_Python_Part1`](W_Codes_Of_Python_Part1) · [`W_Codes_Of_Python_Part2`](W_Codes_Of_Python_Part2) · [`W_Codes_Of_Python_Part3`](W_Codes_Of_Python_Part3) · [`Y_Codes`](Y_Codes)

Expect things like a tarot reader, Telegram bot, text summarizer, text-to-speech, hangman, a video-to-audio converter, a video watermarker, a voice assistant, WhatsApp and website automation, WiFi detectors, a Wikipedia scanner, YouTube tools and more.

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/karthikbilaspur/PythonProject.git
cd PythonProject

# 2. Create an isolated environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install only what the project you want needs
cd Games/chess
pip install -r requirements.txt    # if the project has one
python index.py
```

> 💡 **Tip:** the root [`req.txt`](req.txt) is a *union* of dependencies across the whole repo, including heavyweights like TensorFlow, PyTorch and Selenium. Installing all of it is rarely necessary, so install per project instead.

Projects with a `pyproject.toml` are real packages:

```bash
cd file-forge
pip install -e ".[dev]"
fileforge --help
```

---

## 🧪 Testing

About 30 test files across the packaged projects, powered by `pytest`.

```bash
cd file-forge && pip install -e ".[dev]" && pytest         # 49 tests
cd aws-demo-toolkit && pip install -r requirements-dev.txt && pytest   # moto-mocked, no AWS needed
cd book && pip install -r requirements-dev.txt && pytest
```

Projects with tests: `file-forge`, `aws-demo-toolkit`, `book`, `handwritten-recognition`, `face-vision`, `photo-cleaner`, `fake-news-credible-auditor`.

---

## 🗂️ Repository Layout

```text
PythonProject/
├── Games/                  # 28 games (CLI, Pygame, Tkinter, Streamlit)
├── ai-projects/            # 20 AI mini-projects
├── super-algo/             # dp · graph · puzzles · searching · sorting
├── file-forge/             # ⭐ tested package: safe file toolkit
├── aws-demo-toolkit/       # ⭐ tested package: Lambda + SQS + Flask
├── book/                   # ⭐ tested package: library system
├── handwritten-recognition/  face-vision/  photo-cleaner/   # ⭐ Flask apps
├── Trackers/               # price · product · wishlist · anime
├── T_* U_* V_* W_* Y_*     # A-to-Z script archive
├── <100+ single-purpose folders>   # one idea, one folder
├── req.txt                 # union of all dependencies
└── LICENSE                 # MIT
```

---

## ⚠️ Good to Know

- 🔑 **API keys:** several projects need your own keys (OMDb, OpenAI, Alpha Vantage, Google Custom Search, OpenWeatherMap, News API). Placeholders like `YOUR_API_KEY` are in the code. **Never commit real keys.** Use environment variables or a `.env` file.
- 🛰️ **Responsible use:** port scanners, username/phone lookups, scrapers, WiFi tools and face verification are for **systems, accounts and images you own or have explicit permission to test**. Respect each site's terms of service and `robots.txt`.
- 🏦 **Demos are demos:** finance, health-prediction and banking-style projects are learning exercises. They are **not** medical, financial or production-grade software.
- 🧩 **Heavy dependencies:** ML and CV projects (TensorFlow, PyTorch, DeepFace, OpenCV) are large. Use a separate virtual environment per project.
- 🐍 **Python 3.10+** is recommended, since some projects use modern typing syntax.

---

## 🗺️ Roadmap

- [ ] Add a short README to every folder that lacks one
- [ ] Per-project `requirements.txt` so nothing depends on the root `req.txt`
- [ ] Extend `pytest` coverage beyond the seven tested projects
- [ ] GitHub Actions CI to run the test suites on every push
- [ ] Screenshots / GIFs for the GUI and web apps

---

## 🤝 Contributing

Ideas, fixes and new mini-projects are welcome.

1. Fork the repo and create a branch: `git checkout -b feature/my-idea`
2. Keep each project **self-contained** in its own folder with a short README
3. Add tests if the project has logic worth testing
4. Open a pull request describing what it does and how to run it

---

## 📄 License

Released under the **MIT License**. See [`LICENSE`](LICENSE) for details.

<div align="center">

<br/>

**Built with curiosity, one script at a time. 🐍**

If this repo helped or inspired you, consider giving it a ⭐

</div>
