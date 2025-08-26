import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class FileEncryptor:
    def __init__(self):
        self.key = None
        self.salt = os.urandom(16)

    def generate_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_file(self, filename):
        f = Fernet(self.key)
        with open(filename, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filename, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self, filename):
        f = Fernet(self.key)
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(filename, 'wb') as file:
            file.write(decrypted_data)

    def train_ai_model(self, passwords):
        # Train a random forest classifier to predict password strength
        X = np.array([self.password_strength(password) for password in passwords])
        y = np.array([self.password_label(password) for password in passwords])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        return model

    def password_strength(self, password):
        # Calculate password strength based on length, complexity, and randomness
        strength = 0
        if len(password) > 8:
            strength += 1
        if any(char.isdigit() for char in password):
            strength += 1
        if any(char.isupper() for char in password):
            strength += 1
        if any(char.islower() for char in password):
            strength += 1
        return [strength]

    def password_label(self, password):
        # Label password as weak or strong
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            return 0
        else:
            return 1

def main():
    encryptor = FileEncryptor()
    password = getpass.getpass("Enter password: ")
    encryptor.generate_key(password)
    while True:
        print("1. Encrypt file")
        print("2. Decrypt file")
        print("3. Train AI model")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            filename = input("Enter the filename: ")
            encryptor.encrypt_file(filename)
            print("File encrypted successfully")
        elif choice == "2":
            filename = input("Enter the filename: ")
            encryptor.decrypt_file(filename)
            print("File decrypted successfully")
        elif choice == "3":
            passwords = ["password123", "Password123!", "weak", "StrongP@ssw0rd"]
            model = encryptor.train_ai_model(passwords)
            print("AI model trained successfully")
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()