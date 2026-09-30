# Multi-Tab Calculator (Python + tkinter)

A desktop calculator built with Python's standard-library `tkinter`. It combines a basic calculator, a scientific calculator, a unit converter, and a plain-English word-problem solver in one window. It has no third-party dependencies.

## Features

| Tab | What it does |

|-----|--------------|
| Basic | `+ - * /`, parentheses, decimals, clear and delete |
| Scientific | `sin cos tan log ln sqrt`, `x²`, `1/x`, `eˣ`, `^`, `π`, `e`, modulo (`%`) |
| Converter | Length, Weight and Temperature with From/To dropdowns and a swap button |
| Word Problems | Type "5 plus 3 times 2" or "20 percent of 150" and get an answer |

Extras

- Degrees / Radians toggle for trig functions
- Light and dark themes
- Shared history panel (double-click an entry to copy its result)
- Keyboard support: `Enter` to calculate, `Esc` to clear
- Friendly inline error messages (no crashing pop-ups)
- Resizable window

## Security: no `eval()`

Calculators often evaluate input with Python's `eval()`, which can run arbitrary code. This project instead parses input with the `ast` module and evaluates only a whitelist:

- numbers and the operators `+ - * / %`
- parentheses and unary `+` / `-`
- constants `pi` and `e`
- functions `sin cos tan log ln sqrt exp abs`

Anything else (for example `__import__("os")`) is rejected with an error. Exponents are capped at 1000, so inputs like `999` can't freeze the app.

## Requirements

- Python 3.8 or newer
- `tkinter` (bundled with most Python installs)

On some Linux distributions `tkinter` is a separate package:

```bash
sudo apt install python3-tk
```

## Getting started

```bash
git clone https://github.com/karthikbilaspur/PythonProject.git
cd PythonProject          # then into the folder that contains calculator.py
python calculator.py
```

## Usage examples

Scientific tab (Degrees mode)

sin(30)            → 0.5
sqrt(16)+2^3       → 12
10 % 3             → 1

Word Problems tab

5 plus 3 times 2       → 11
20 percent of 150      → 30
square root of 81      → 9
7 squared              → 49
10 divided by 4        → 2.5

Converter tab

100 Celsius → Fahrenheit   = 212
5 Kilometer → Mile         = 3.10685596

## Project structure

`calculator.py` is a single file organised into these parts:

| Section | Purpose |

|---------|---------|
| `safe_eval`, `fmt`, `friendly_error` | Safe expression evaluation, number formatting, error messages |
| `CalculatorTab` | One class powering both the Basic and Scientific tabs (only the button layout differs) |
| `UNITS`, `ConverterTab` | Data-driven unit converter |
| `words_to_expression`, `AITab` | Rule-based English-to-expression parser |
| `App` | Main window, theme, angle mode, history panel |

### Adding a new unit

Add one line to the `UNITS` dictionary, using a factor relative to the base unit (meter or kilogram):

```python
"Length": {..., "Yard": 0.9144},
```

## Limitations

- The "Word Problems" tab is rule-based, not a real AI model. It understands only the phrases in `WORD_RULES`.
- `%` on the Scientific tab is modulo, not percentage.
- The dark theme uses ttk's `clam` theme, so its appearance varies slightly by OS.

## Roadmap

- [ ] Inverse trig functions (`asin`, `acos`, `atan`) and factorial
- [ ] Memory buttons (M+, M-, MR)
- [ ] More converter categories (volume, speed, currency via an API)
- [ ] Unit tests for `safe_eval` and the word parser
- [ ] Optional LLM-backed word problems, with the current parser as an offline fallback

## Contributing

Issues and pull requests are welcome. If you add a feature, please include a few example inputs and expected outputs.

## License

Add the license of your choice (for example MIT) here.
