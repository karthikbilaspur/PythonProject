import time, os, shutil, subprocess

YELLOW="\033[93m\033[1m"; BLUE="\033[94m\033[1m"; RESET="\033[0m"

DEFAULT_TEXT = """Episode IV

THE UMBRA PROJECT

In a distant corner of the galaxy,
a secret research facility has been
working on a top-secret project
known as "Umbra".

The project, led by the brilliant
but reclusive scientist Dr. Elara Vex,
aims to harness the power of dark
energy to create a new source of
unlimited clean energy.

But as the project nears completion,
a rogue faction within the facility
threatens to sabotage the entire
operation, plunging the galaxy
into chaos.
"""

def clear():
    subprocess.run(['cls' if os.name == 'nt' else 'clear'], check=False)
def show_intro():
    clear()
    print(f"\n\n\n{BLUE}{'A long time ago in a galaxy far,'}\n{'far away....':^40}{RESET}")
    time.sleep(2.5)
    clear()
    print(f"\n\n\n{YELLOW}{'STAR WARS':^60}\n{'':^60}\n{'OPENING CRAWL':^60}{RESET}")
    time.sleep(2)

def opening_crawl(text: str, speed: float = 0.35):
    """Real crawl: lines rise from bottom, shrink toward centre = perspective."""
    show_intro()
    lines = [l for l in text.strip().split('\n')]
    width = shutil.get_terminal_size().columns
    height = shutil.get_terminal_size().lines
    # Pad so text starts below screen
    frames = [""]*height + lines + [""]*height
    try:
        for offset in range(len(frames)):
            clear()
            visible = frames[offset:offset+height]
            for i, line in enumerate(visible):
                # Perspective: top lines are narrower / more indented
                progress = i / max(1, height)  # 0 top -> 1 bottom
                indent = int((1-progress)*18)
                max_len = max(20, width - indent*2 - 4)
                line = line.strip()
                if len(line) > max_len: line = line[:max_len]
                print(" "*indent + f"{YELLOW}{line:^{max_len}}{RESET}")
            time.sleep(speed)
    except KeyboardInterrupt:
        clear(); print(f"{YELLOW}May the Force be with you. (Ctrl+C to exit){RESET}"); return
    clear(); print(f"\n\n{YELLOW}{'May the Force be with you.':^60}{RESET}\n"); time.sleep(1.5)

def main():
    print("="*50); print("  STAR WARS OPENING CRAWL"); print("="*50)
    print("1. Play default (Umbra Project)  2. Type your own  3. Load from .txt file  q. Quit")
    c=input("Choice: ").strip().lower()
    if c=='1': opening_crawl(DEFAULT_TEXT)
    elif c=='2':
        print("Type your crawl, end with empty line + 'END' on its own line:")
        buf: list[str] = []
        while True:
            l=input()
            if l.strip()=='END': break
            buf.append(l)
        opening_crawl("\n".join(buf) or DEFAULT_TEXT)
    elif c=='3':
        path=input("Text file path: ").strip()
        try:
            with open(path, encoding='utf-8') as f: opening_crawl(f.read())
        except Exception as e: print(f"Error: {e}")
    else: print("May the Force be with you!")

if __name__=="__main__": main()
