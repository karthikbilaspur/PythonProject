# EXTREME PASSWORD AI - Secure Edition

This clubs your 3 password files into 1 secure extreme engine.

## Why Club Them?

You had:
- File 1: `random` - **INSECURE**, length truncation bug
- File 2: Markov - **CRASHES** if state unknown, mixes `numpy` + `secrets`, train double-divides
- File 3: Best version but pattern validation wrong

**Verdict:** Club them into 1 - they are versions of same job, not 3 engines like music project.

## Structure

```
extreme_password_ai/
├── password_engine.py   # EXTREME - clubs all 3, fixed secure
│   ├── generate_secure()       # From File 1 but uses secrets
│   ├── generate_markov()       # From File 2/3 but with fallback
│   ├── generate_from_pattern() # From File 3 fixed
│   ├── generate_memorable()    # NEW - Correct-Horse-Battery
│   └── generate_extreme()      # NEW - best of all
├── strength_analyzer.py # FIXED - consistent Dict return, entropy + crack time
├── main.py              # CLI menu 8 options
├── app.py               # FastAPI web API
├── requirements.txt
└── README.md
```

## Immediate Bugs Fixed

### File 1 Bug:
```python
# BEFORE - insecure + truncates required chars
import random
password = [upper, digit, symbol, lower]
return ''.join(password[:length]) # length=3 -> loses 1 required

# AFTER - secure + validates length
import secrets
if length < len(required_sets): raise ValueError
secrets.SystemRandom().shuffle(password)
```

### File 2 Bug:
```python
# BEFORE - crashes
next_state = np.random.choice(...) # no fallback if state missing

# AFTER - fallback + no numpy
if transitions: weighted_choice with secrets
else: secrets.choice(all_chars)
```

### File 2 Train Bug:
```python
# BEFORE - double divides on second train
self.matrix[state][next] /= total # already divided

# AFTER - recounts fresh
temp_counts -> then convert to prob
```

### File 3 Bug:
```python
# BEFORE - allows 'abc' as pattern
all(ch in "LUDS" or ch.isalnum() for ch in pattern)

# AFTER - only LUDS + allowed literals -_ .@#!
if ch in char_sets: ok
elif ch in allowed_literals: ok
else: raise ValueError
```

## How to Run

```bash
pip install -r requirements.txt
python main.py

# Menu:
# 1 = Secure (File 1 fixed)
# 2 = Markov (File 2 fixed)
# 3 = Pattern (File 3 fixed)
# 4 = Memorable - NEW
# 5 = EXTREME - NEW best
# 6 = Check strength
```

## Security Notes

- **Never use `random` for passwords** - always `secrets`
- **Never use `np.random` for passwords** - not cryptographically secure
- Always validate `length >= required_sets`
- `check_strength` now returns consistent dict with entropy bits + crack time estimation

## Example

```
Secure: k7$Fp2!qZx9@
Pattern ULLDDS: Abc12!@
Memorable: Correct-Horse-Battery-Staple-42!
Extreme: 7f$K9pL2@QwX8!R1
Strength: Very Strong (6/6) - 85.2 bits - 1000 years crack time
```

## Next Extreme Ideas

- [ ] Add haveibeenpwned API check
- [ ] Add passphrase generator with diceware
- [ ] Export to encrypted vault file
- [ ] Web UI with copy button

This follows same philosophy as your word and music AI - but here clubbing is correct because 3 files were versions, not engines.
