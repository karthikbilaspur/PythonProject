import getpass
import hashlib
import os
import json

class PasswordManager:
    def __init__(self):
        self.passwords = {}
        self.master_password = None

    def create_master_password(self):
        while True:
            password = getpass.getpass("Create a master password: ")
            confirm_password = getpass.getpass("Confirm master password: ")
            if password == confirm_password:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                with open("master_password.txt", "w") as f:
                    f.write(hashed_password)
                self.master_password = password
                print("Master password created successfully!")
                break
            else:
                print("Passwords do not match. Please try again.")

    def login(self):
        while True:
            password = getpass.getpass("Enter master password: ")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            try:
                with open("master_password.txt", "r") as f:
                    stored_hash = f.read()
                if hashed_password == stored_hash:
                    self.master_password = password
                    print("Login successful!")
                    return True
                else:
                    print("Incorrect password. Please try again.")
            except FileNotFoundError:
                print("No master password found. Please create one.")
                return False

    def add_password(self):
        service = input("Enter service name: ")
        if service:
            password = getpass.getpass("Enter password: ")
            if password:
                self.passwords[service] = password
                self.save_passwords()
                print("Password added successfully!")
            else:
                print("Password cannot be empty.")
        else:
            print("Service name cannot be empty.")

    def view_passwords(self):
        for service, password in self.passwords.items():
            print(f"{service}: {password}")

    def delete_password(self):
        service = input("Enter service name: ")
        if service in self.passwords:
            del self.passwords[service]
            self.save_passwords()
            print("Password deleted successfully!")
        else:
            print("Service not found.")

    def save_passwords(self):
        try:
            with open("passwords.json", "w") as f:
                json.dump(self.passwords, f)
        except Exception as e:
            print(f"Error saving passwords: {e}")

    def load_passwords(self):
        try:
            with open("passwords.json", "r") as f:
                self.passwords = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error loading passwords. Passwords file is corrupted.")

def main():
    manager = PasswordManager()
    if not os.path.exists("master_password.txt"):
        manager.create_master_password()
    while True:
        if manager.login():
            manager.load_passwords()
            while True:
                print("\n1. Add password")
                print("2. View passwords")
                print("3. Delete password")
                print("4. Quit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    manager.add_password()
                elif choice == "2":
                    manager.view_passwords()
                elif choice == "3":
                    manager.delete_password()
                elif choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")
            break

if __name__ == "__main__":
    main()