# Steganography LSB - Improved

Run

```bash
pip install Pillow
python stego_lsb.py
# 1 = Hide, 2 = Extract, 3 = Check capacity
```

What Was Fixed

| Original Bug | Fix |

|---|---|
| Extract needed exact `message_length` | Stores 32-bit length header - extract needs no length |
| `ord(char)` = ASCII only, emoji broke | UTF-8 bytes - emoji / Hindi / any unicode works |
| Capacity check wrong | Correct: `pixels * 3 channels - header` |
| Only Red channel (1 bit/pixel) | Uses R+G+B = index3x capacityindex |
| Hardcoded `input.png` / `Hello, World!` | Interactive menu + custom paths |
| Saving as JPG would destroy data | Forces PNG + warning |

How It Works
For each pixel (R,G,B):
  replace LSB with next message bit
  e.g. R=10101010 + bit 1 -> 10101011
Header: first 32 bits = message length in bytes

Example
Hide: "Hello 👋" in input.png -> hidden.png
Extract hidden.png -> "Hello 👋"
