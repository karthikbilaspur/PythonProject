import time
import os

def opening_crawl(text: str) -> None:
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Display the crawl
    lines = text.split('\n')
    for line in lines:
        print(line)
        time.sleep(2)  # Wait for 2 seconds

    # Scroll the text upwards
    for _ in range(10):
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in lines:
            print(' ' * 10 + line)
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in lines:
            print(' ' * 5 + line)
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in lines:
            print(line)
        time.sleep(0.5)

# Example usage
text = """
Episode IV

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

opening_crawl(text)