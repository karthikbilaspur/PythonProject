"""
Steganography LSB - IMPROVED
Fixes vs original:
  - No length stored -> extract needed exact len, else garbage. Now stores 32-bit length header.
  - Only ASCII (ord) -> broke on emoji/unicode. Now UTF-8 bytes.
  - Capacity check wrong: len(bits) > pixels (1 bit/pixel in R only) -> now correct: need bits <= pixels*1 + header, and uses ALL 3 channels (R,G,B) = 3x capacity.
  - No CLI, hardcoded paths -> now menu + hide/extract + capacity check.
  - No PNG warning: saving as JPG destroys LSB -> forces PNG.
Run: python stego_lsb.py
Needs: pip install Pillow
"""
from PIL import Image
import os
from collections.abc import Iterable
from typing import cast

def _to_bits(data: bytes):
    return ''.join(f'{b:08b}' for b in data)
def _from_bits(bits: str):
    return bytes(int(bits[i:i+8],2) for i in range(0,len(bits)-8+1,8))

def capacity_bytes(img: Image.Image):
    w,h=img.size; return (w*h*3 - 32)//8  # 3 channels, minus 32-bit header

def hide_message(image_path: str, message: str, output_path: str) -> str:
    if not output_path.lower().endswith('.png'):
        output_path = os.path.splitext(output_path)[0]+'.png'
        print(f"Note: forced PNG ({output_path}) - JPG destroys hidden data!")
    img=Image.open(image_path).convert('RGB')
    msg_bytes=message.encode('utf-8')
    cap=capacity_bytes(img)
    if len(msg_bytes)>cap: raise ValueError(f"Message too big: {len(msg_bytes)} bytes, capacity {cap} bytes. Use larger image.")
    # Header: 32-bit length + message bits
    payload=_to_bits(len(msg_bytes).to_bytes(4,'big')+msg_bytes)
    pixels: list[tuple[int, int, int]] = list(
        cast(Iterable[tuple[int, int, int]], img.getdata())
    )
    new_pixels: list[tuple[int, int, int]] = []
    bit_idx=0
    for r,g,b in pixels:
        vals: list[int] = []
        for v in (r,g,b):
            if bit_idx<len(payload):
                v=(v & 0xFE) | int(payload[bit_idx]); bit_idx+=1
            vals.append(v)
        new_pixels.append((vals[0], vals[1], vals[2]))
    out=Image.new('RGB', img.size); out.putdata(new_pixels); out.save(output_path)
    print(f"Hidden {len(msg_bytes)} bytes ({len(message)} chars) in {output_path} | Capacity: {cap} bytes")
    return output_path

def extract_message(image_path: str) -> str:
    img=Image.open(image_path).convert('RGB')
    pixels: Iterable[tuple[int, int, int]] = cast(
        Iterable[tuple[int, int, int]], img.getdata()
    )
    bits=''.join(str(v & 1) for px in pixels for v in px)
    length=int(bits[:32],2)
    if length>capacity_bytes(img): raise ValueError("No hidden message found / corrupted image")
    msg_bits=bits[32:32+length*8]
    return _from_bits(msg_bits).decode('utf-8')

def main():
    print("="*45); print("  LSB STEGANOGRAPHY - Hide Message in Image"); print("="*45)
    while True:
        print("\n1. Hide message  2. Extract message  3. Check capacity  q. Quit")
        c=input("Choice: ").strip().lower()
        if c=='q': break
        elif c=='1':
            src=input("Input image (PNG): ").strip() or 'input.png'
            msg=input("Secret message: ")
            out=input("Output (hidden.png): ").strip() or 'hidden.png'
            try: hide_message(src, msg, out)
            except Exception as e: print(f"Error: {e}")
        elif c=='2':
            src=input("Image with hidden message: ").strip() or 'hidden.png'
            try: print(f"\nExtracted: {extract_message(src)}")
            except Exception as e: print(f"Error: {e}")
        elif c=='3':
            src=input("Image: ").strip() or 'input.png'
            try:
                img=Image.open(src).convert('RGB')
                print(f"Capacity: {capacity_bytes(img)} bytes (~{capacity_bytes(img)} chars)")
            except Exception as e: print(f"Error: {e}")

if __name__=="__main__": main()
