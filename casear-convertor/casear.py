import random
import string

def caesar_cipher(text: str, shift: int, mode: str = 'encrypt') -> str:
    """
    Encrypts or decrypts the input text using a Caesar cipher.

    Args:
        text (str): The input text to encrypt or decrypt.
        shift (int): The number of positions to shift the alphabet.
        mode (str, optional): 'encrypt' or 'decrypt'. Defaults to 'encrypt'.

    Returns:
        str: The encrypted or decrypted text.
    """
    alphabet = string.ascii_lowercase
    result = ''

    for char in text:
        if char.isalpha():
            index = alphabet.index(char.lower())
            if mode == 'encrypt':
                new_index = (index + shift) % 26
            elif mode == 'decrypt':
                new_index = (index - shift) % 26
            else:
                raise ValueError("Invalid mode. Use 'encrypt' or 'decrypt'.")

            if char.isupper():
                result += alphabet[new_index].upper()
            else:
                result += alphabet[new_index]
        else:
            result += char

    return result


def brute_force_attack(ciphertext: str) -> None:
    """
    Attempts to decrypt the ciphertext using all possible shift values.

    Args:
        ciphertext (str): The ciphertext to decrypt.
    """
    for shift in range(26):
        plaintext = caesar_cipher(ciphertext, shift, mode='decrypt')
        print(f"Shift: {shift}, Plaintext: {plaintext}")


def main():
    while True:
        print("\nCaesar Cipher Menu:")
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Brute-force attack")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            text = input("Enter the text to encrypt: ")
            shift = input("Enter the shift value (or 'random' for a random shift): ")
            if shift.lower() == 'random':
                shift = random.randint(1, 25)
                print(f"Random shift: {shift}")
            else:
                shift = int(shift)
            ciphertext = caesar_cipher(text, shift)
            print(f"Ciphertext: {ciphertext}")
        elif choice == '2':
            ciphertext = input("Enter the ciphertext to decrypt: ")
            shift = int(input("Enter the shift value: "))
            plaintext = caesar_cipher(ciphertext, shift, mode='decrypt')
            print(f"Plaintext: {plaintext}")
        elif choice == '3':
            ciphertext = input("Enter the ciphertext to attack: ")
            brute_force_attack(ciphertext)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()