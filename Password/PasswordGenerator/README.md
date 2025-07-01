Password Generator README
Overview
A Python script to generate strong, random passwords with customizable options.
Features
Generate passwords with specified length (default: 12)
Include/exclude uppercase letters, digits, and symbols
Ensure at least one character from each selected set
Shuffle password characters for maximum randomness
Usage
Command Line
Run the script directly to generate a password with default options:
Bash
python password_generator.py
Importing as a Module
Import the generate_password function in your own Python script:
Python
from password_generator import generate_password

password = generate_password(length=16, use_upper=True, use_digits=True, use_symbols=False)
print(password)
Options
length: Password length (default: 12)
use_upper: Include uppercase letters (default: True)
use_digits: Include digits (default: True)
use_symbols: Include symbols (default: True)
Requirements
Python 3.x
random and string modules (included in Python Standard Library)
Example Output
Code
Generated password: 4S$eJ#8dGpL2aB
Notes
Ensure at least one character set is selected to avoid errors.
Password length should be at least 4 to accommodate one character from each selected set.
License
This script is released under the MIT License. Feel free to modify and distribute.
