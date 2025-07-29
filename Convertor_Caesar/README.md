# Caesar Cipher Program Summary

This program implements a Caesar cipher, a type of substitution cipher where each letter in the plaintext is shifted a certain number of positions down the alphabet. The program includes the following features:
Encryption: Shifts the input text by a specified number of positions to produce the ciphertext.
Decryption: Shifts the ciphertext back by the same number of positions to recover the plaintext.
Random Shift: Allows the user to generate a random shift value for encryption.
Brute-Force Attack: Attempts to decrypt the ciphertext by trying all possible shift values (0-25).
The program uses a menu-driven interface, allowing users to:
Encrypt text
Decrypt text
Perform a brute-force attack
Quit the program
Key Functions
caesar_cipher(text, shift, mode): Encrypts or decrypts the input text using the Caesar cipher algorithm.
brute_force_attack(ciphertext): Attempts to decrypt the ciphertext by trying all possible shift values.
Example Use Cases
Encrypting a message with a specified shift value
Decrypting a ciphertext with a known shift value
Using a brute-force attack to decrypt a ciphertext without knowing the shift value.
