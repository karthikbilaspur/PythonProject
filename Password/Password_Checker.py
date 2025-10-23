import re

def check_password_strength(password):
    strength = 0
    errors = []

    # Check password length
    if len(password) < 8:
        errors.append("Password should be at least 8 characters long")
    else:
        strength += 1

    # Check for uppercase letters
    if not re.search("[A-Z]", password):
        errors.append("Password should have at least one uppercase letter")
    else:
        strength += 1

    # Check for lowercase letters
    if not re.search("[a-z]", password):
        errors.append("Password should have at least one lowercase letter")
    else:
        strength += 1

    # Check for numbers
    if not re.search("[0-9]", password):
        errors.append("Password should have at least one number")
    else:
        strength += 1

    # Check for special characters
    if not re.search("[!@#$%^&*()_+=-{};:'<>,./?]", password):
        errors.append("Password should have at least one special character")
    else:
        strength += 1

    if strength == 5:
        return "Strong"
    elif strength >= 3:
        return "Medium"
    else:
        return "Weak"

def main():
    password = input("Enter a password: ")
    strength = check_password_strength(password)
    print(f"Password strength: {strength}")

    if strength != "Strong":
        print("Suggestions:")
        if len(password) < 8:
            print("- Make the password at least 8 characters long")
        if not re.search("[A-Z]", password):
            print("- Add at least one uppercase letter")
        if not re.search("[a-z]", password):
            print("- Add at least one lowercase letter")
        if not re.search("[0-9]", password):
            print("- Add at least one number")
        if not re.search("[!@#$%^&*()_+=-{};:'<>,./?]", password):
            print("- Add at least one special character")

if __name__ == "__main__":
    main()