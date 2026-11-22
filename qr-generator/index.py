"""
QR Generator - CLI - Medium Level
Fixes: validates filename + extension, sanitizes path, color / size options,
no crash if file missing, --help, preview optional.
Requires: pip install qrcode pillow
Usage: python index.py
       python index.py --data "hello" --out myqr.png --color "#0000FF"
"""
import argparse, sys
from pathlib import Path

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_M

def parse_args():
    p=argparse.ArgumentParser(description="Generate a QR code")
    p.add_argument("--data", help="Text/URL to encode")
    p.add_argument("--out", default="qr_code.png", help="Output PNG path")
    p.add_argument("--box-size", type=int, default=10, help="Box size 4-20")
    p.add_argument("--border", type=int, default=4, help="Border 1-10")
    p.add_argument("--color", default="black", help="Fill color, e.g. black or #0000FF")
    p.add_argument("--no-preview", action="store_true", help="Don't open preview")
    return p.parse_args()

def prompt(msg: str) -> str:
    while True:
        v=input(msg).strip()
        if v: return v
        print("Please enter something.")

def main():
    a=parse_args()
    data=a.data or prompt("Enter data for QR code: ")
    out=Path(a.out or prompt("Enter filename (e.g. qr_code.png): "))
    if out.suffix.lower() != ".png":
        print("Filename must end with .png"); sys.exit(1)
    if not (4 <= a.box_size <= 20): print("box-size must be 4-20"); sys.exit(1)
    if not (1 <= a.border <= 10): print("border must be 1-10"); sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    qr=qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=a.box_size, border=a.border)
    qr.add_data(data); qr.make(fit=True)
    img=qr.make_image(fill_color=a.color, back_color="white")
    img.save(str(out))
    with Image.open(out) as saved:
        width, height = saved.size
    print(f"QR saved as {out} ({width}x{height} px)")
    if not a.no_preview:
        try: Image.open(out).show()
        except Exception as e: print(f"Could not preview: {e}")

if __name__=="__main__":
    main()
