class CrypticLanguage:
    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def caesar_encrypt(self, text, shift):
        encrypted_text = ''
        for char in text:
            if char.isalpha():
                index = self.alphabet.index(char.lower())
                new_index = (index + shift) % 26
                if char.isupper():
                    encrypted_text += self.alphabet[new_index].upper()
                else:
                    encrypted_text += self.alphabet[new_index]
            else:
                encrypted_text += char
        return encrypted_text

    def caesar_decrypt(self, text, shift):
        return self.caesar_encrypt(text, -shift)

    def vigenere_encrypt(self, text, key):
        encrypted_text = ''
        key_index = 0
        key = key.lower()
        for char in text:
            if char.isalpha():
                shift = self.alphabet.index(key[key_index % len(key)])
                index = self.alphabet.index(char.lower())
                new_index = (index + shift) % 26
                if char.isupper():
                    encrypted_text += self.alphabet[new_index].upper()
                else:
                    encrypted_text += self.alphabet[new_index]
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, text, key):
        decrypted_text = ''
        key_index = 0
        key = key.lower()
        for char in text:
            if char.isalpha():
                shift = self.alphabet.index(key[key_index % len(key)])
                index = self.alphabet.index(char.lower())
                new_index = (index - shift) % 26
                if char.isupper():
                    decrypted_text += self.alphabet[new_index].upper()
                else:
                    decrypted_text += self.alphabet[new_index]
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text

def main():
    cryptic_language = CrypticLanguage()
    while True:
        print("\n1. Caesar Cipher Encrypt")
        print("2. Caesar Cipher Decrypt")
        print("3. Vigenère Cipher Encrypt")
        print("4. Vigenère Cipher Decrypt")
        print("5. Quit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            text = input("Enter the text to encrypt: ")
            shift = int(input("Enter the shift value: "))
            print(cryptic_language.caesar_encrypt(text, shift))
        elif choice == "2":
            text = input("Enter the text to decrypt: ")
            shift = int(input("Enter the shift value: "))
            print(cryptic_language.caesar_decrypt(text, shift))
        elif choice == "3":
            text = input("Enter the text to encrypt: ")
            key = input("Enter the key: ")
            print(cryptic_language.vigenere_encrypt(text, key))
        elif choice == "4":
            text = input("Enter the text to decrypt: ")
            key = input("Enter the key: ")
            print(cryptic_language.vigenere_decrypt(text, key))
        elif choice == "5":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()