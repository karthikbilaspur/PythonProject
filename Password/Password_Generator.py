import string
import secrets

def generate_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def generate_custom_password(length: int = 12, use_uppercase: bool = True, use_numbers: bool = True, use_special_chars: bool = True) -> str:
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def main():
    print("Password Generator")
    print("------------------")
    print("1. Generate a random password")
    print("2. Generate a custom password")
    choice = input("Enter your choice: ")

    if choice == "1":
        length = int(input("Enter the password length (default=12): ") or 12)
        password = generate_password(length)
        print(f"Generated password: {password}")
    elif choice == "2":
        length = int(input("Enter the password length (default=12): ") or 12)
        use_uppercase = input("Use uppercase letters? (yes/no): ").lower() == "yes"
        use_numbers = input("Use numbers? (yes/no): ").lower() == "yes"
        use_special_chars = input("Use special characters? (yes/no): ").lower() == "yes"
        password = generate_custom_password(length, use_uppercase, use_numbers, use_special_chars)
        print(f"Generated password: {password}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()