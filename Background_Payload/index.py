import os
import secrets
import string

# Passwords ko store karne ke liye ek dictionary
passwords = {}

def generate_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def add_password():
    service = input("Enter service name (e.g. Facebook, Gmail): ")
    username = input("Enter username: ")
    password = input("Enter password (or press Enter to generate one): ")
    if password == "":
        password = generate_password(12)
        print(f"Generated password: {password}")
    passwords[service] = {"username": username, "password": password}
    print(f"Password for {service} added successfully!")

def view_passwords():
    print("Your Passwords:")
    for service, credentials in passwords.items():
        print(f"Service: {service}")
        print(f"Username: {credentials['username']}")
        print(f"Password: {credentials['password']}")
        print("------------------------")

def retrieve_password():
    service = input("Enter service name: ")
    if service in passwords:
        print(f"Username: {passwords[service]['username']}")
        print(f"Password: {passwords[service]['password']}")
    else:
        print(f"No password found for {service}")

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("Password Manager")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Retrieve Password")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_password()
            input("Press Enter to continue...")
        elif choice == "2":
            view_passwords()
            input("Press Enter to continue...")
        elif choice == "3":
            retrieve_password()
            input("Press Enter to continue...")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()