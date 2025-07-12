import random
import string

def generate_password(length: int = 12, use_upper: bool = True, use_digits: bool = True, use_symbols: bool = True):
    """
    Generate a random password with the given options.
    :param length: Length of the password
    :param use_upper: Include uppercase letters
    :param use_digits: Include digits
    :param use_symbols: Include symbols
    :return: Generated password as a string
    """
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ''
    digits = string.digits if use_digits else ''
    symbols = string.punctuation if use_symbols else ''
    
    all_chars = lower + upper + digits + symbols
    if not all_chars:
        raise ValueError("At least one character set must be selected.")
    
    # Ensure at least one character from each selected set
    from typing import List
    password: List[str] = []
    if use_upper:
        password.append(random.choice(upper))
    if use_digits:
        password.append(random.choice(digits))
    if use_symbols:
        password.append(random.choice(symbols))
    password.append(random.choice(lower))
    
    # Fill the rest of the password length
    while len(password) < length:
        password.append(random.choice(all_chars))
    
    random.shuffle(password)
    return ''.join(password[:length])

if __name__ == "__main__":
    print("Generated password:", generate_password())