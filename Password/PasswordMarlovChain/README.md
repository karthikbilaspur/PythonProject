
Password Generator README
Overview
A Python script to generate strong, random passwords using Markov Chain and customizable requirements. It also includes a password strength checker.
Features
Generate passwords using Markov Chain model
Generate passwords with customizable requirements (uppercase, numbers, special characters)
Check password strength (weak, medium, strong)
Train Markov Chain model with provided passwords
Usage
Command Line
Run the script directly to access the password generator menu:
Bash
python password_generator.py
Menu Options
Generate Password using Markov Chain: Train the model with provided passwords and generate a password.
Generate Password with Requirements: Generate a password with customizable requirements (uppercase, numbers, special characters).
Check Password Strength: Check the strength of a provided password.
Train Markov Chain Model: Train the model with provided passwords.
Requirements
Python 3.x
secrets, numpy, re, and collections modules (included in Python Standard Library)
Example Output
Code
Password Generator Menu:
1. Generate Password using Markov Chain
2. Generate Password with Requirements
3. Check Password Strength
4. Train Markov Chain Model
Enter your choice: 2
Include uppercase letters? (yes/no): yes
Include numbers? (yes/no): yes
Include special characters? (yes/no): yes
Generated password: G#4dJ7pL$aB8
Notes
The Markov Chain model requires training data to generate passwords.
Password strength is checked based on length, uppercase, lowercase, numbers, and special characters.
License
This script is released under the MIT License. Feel free to modify and distribute.