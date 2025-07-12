
import string
import secrets
import numpy as np
from collections import defaultdict
from typing import DefaultDict
import re

class PasswordGenerator:
    def __init__(self, password_length: int = 12):
        self.password_length = password_length
        self.transition_matrix: DefaultDict[str, DefaultDict[str, float]] = defaultdict(lambda: defaultdict(int))
        self.states = string.ascii_letters + string.digits + string.punctuation

    def train(self, passwords: list[str]):
        for password in passwords:
            for i in range(len(password) - 1):
                self.transition_matrix[password[i]][password[i + 1]] += 1

        for state in self.transition_matrix:
            total_transitions = sum(self.transition_matrix[state].values())
            for next_state in self.transition_matrix[state]:
                self.transition_matrix[state][next_state] /= total_transitions

    def generate_password(self):
        password = [secrets.choice(list(self.states))]
        for _ in range(self.password_length - 1):
            current_state = password[-1]
            next_states = list(self.transition_matrix[current_state].keys())
            next_state_probabilities = list(self.transition_matrix[current_state].values())
            next_state = np.random.choice(next_states, p=next_state_probabilities)
            password.append(next_state)

        return ''.join(password)

    def generate_password_with_requirements(self, use_uppercase: bool = True, use_numbers: bool = True, use_special_chars: bool = True):
        characters = string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_special_chars:
            characters += string.punctuation

        password: list[str] = []
        if use_uppercase:
            password.append(secrets.choice(string.ascii_uppercase))
        if use_numbers:
            password.append(secrets.choice(string.digits))
        if use_special_chars:
            password.append(secrets.choice(string.punctuation))
        password.append(secrets.choice(string.ascii_lowercase))

        for _ in range(self.password_length - len(password)):
            password.append(secrets.choice(characters))

        secrets.SystemRandom().shuffle(password)
        return ''.join(password)

    from typing import Union, Tuple, List

    def check_password_strength(self, password: str) -> Union[str, Tuple[str, List[str]]]:
        strength = 0
        errors: list[str] = []

        if len(password) < 8:
            errors.append("Password should be at least 8 characters long")
        else:
            strength += 1

        if not re.search("[a-z]", password):
            errors.append("Password should have at least one lowercase letter")
        else:
            strength += 1

        if not re.search("[A-Z]", password):
            errors.append("Password should have at least one uppercase letter")
        else:
            strength += 1

        if not re.search("[0-9]", password):
            errors.append("Password should have at least one number")
        else:
            strength += 1

        if not re.search("[^A-Za-z0-9]", password):
            errors.append("Password should have at least one special character")
        else:
            strength += 1

        if strength == 5:
            return "Strong"
        elif strength >= 3:
            return "Medium"
        else:
            return "Weak", errors

def main():
    generator = PasswordGenerator(password_length=12)

    print("Password Generator Menu:")
    print("1. Generate Password using Markov Chain")
    print("2. Generate Password with Requirements")
    print("3. Check Password Strength")
    print("4. Train Markov Chain Model")

    choice = input("Enter your choice: ")

    if choice == "1":
        passwords = ["P@ssw0rd!", "S3cur1ty!", "Str0ngP@ssw0rd!"]
        generator.train(passwords)
        print(generator.generate_password())
    elif choice == "2":
        use_uppercase = input("Include uppercase letters? (yes/no): ").lower() == "yes"
        use_numbers = input("Include numbers? (yes/no): ").lower() == "yes"
        use_special_chars = input("Include special characters? (yes/no): ").lower() == "yes"
        print(generator.generate_password_with_requirements(use_uppercase, use_numbers, use_special_chars))
    elif choice == "3":
        password = input("Enter password to check strength: ")
        strength = generator.check_password_strength(password)
        if isinstance(strength, tuple):
            print(f"Password strength: {strength[0]}")
            print("Errors:")
            for error in strength[1]:
                print(error)
        else:
            print(f"Password strength: {strength}")
    elif choice == "4":
        passwords = input("Enter passwords to train model (comma-separated): ").split(',')
        generator.train(passwords)
        print("Model trained successfully")

if __name__ == "__main__":
    main()