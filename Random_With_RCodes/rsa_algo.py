def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Calculate the Greatest Common Divisor of two numbers."""
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(a: int, b: int) -> int:
    """Calculate the multiplicative inverse of a modulo b."""
    s1, s2, m = 1, 0, b
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        s1, s2 = s2, s1 - q * s2
    return s1 % m


def powermod(x: int, y: int, p: int) -> int:
    """Calculate x raised to the power y modulo p."""
    res = 1
    x = x % p
    while y > 0:
        if y % 2 == 1:
            res = (res * x) % p
        y //= 2
        x = (x * x) % p
    return res


def get_prime_number(prompt: str) -> int:
    """Get a prime number from the user."""
    while True:
        try:
            num = int(input(prompt))
            if is_prime(num):
                return num
            else:
                print(num, 'is not a prime number')
        except ValueError:
            print('Invalid input. Please enter a number.')


def get_coprime_number(prompt: str, phi_n: int) -> int:
    """Get a number that is coprime with phi_n."""
    while True:
        try:
            num = int(input(prompt))
            if gcd(num, phi_n) == 1:
                return num
            else:
                print('The number is not coprime with', phi_n)
        except ValueError:
            print('Invalid input. Please enter a number.')


def encrypt_message(message: str, a: int, n: int) -> tuple[str, list[int]]:
    """Encrypt a message using the public key (n, a)."""
    encrypted_string = ""
    encrypted_num = []
    for ch in message:
        if ch != ' ':
            m = ord(ch) - 97
            e = powermod(m, a, n)
            encrypted_num.append(e)
            encrypted_string += chr(e % 26 + 97)
        else:
            encrypted_string += ' '
    return encrypted_string, encrypted_num


def decrypt_message(encrypted_string: str, encrypted_num: list[int], b: int, n: int) -> str:
    """Decrypt a message using the private key (n, b)."""
    decrypted = ''
    j = 0
    for ch in encrypted_string:
        if ch != ' ':
            e = encrypted_num[j]
            m = powermod(e, b, n)
            ch = chr(m + 97)
            decrypted += ch
            j += 1
        else:
            decrypted += ' '
    return decrypted


def main():
    while True:
        print('RSA Encryption Algorithm')
        print('------------------------')
        print('1. Enter prime numbers')
        print('2. Use predefined prime numbers')
        print('3. Exit')
        choice = input('Enter your choice: ')
        
        if choice == '1':
            p = get_prime_number('Enter a prime number: ')
            q = get_prime_number('Enter a different prime number: ')
            while p * q <= 26:
                print('The product of the prime numbers should be greater than 26.')
                q = get_prime_number('Enter a different prime number: ')
            
            n = p * q
            phi_n = (p - 1) * (q - 1)
            a = get_coprime_number(f'Enter a number such that Greatest Common Divisor with {phi_n} is 1: ', phi_n)
            b = multiplicative_inverse(a, phi_n)
            
        elif choice == '2':
            p, q, a, b = 13, 17, 5, 77
            n = p * q
            phi_n = (p - 1) * (q - 1)
            
        elif choice == '3':
            break
            
        else:
            print('Invalid choice. Please try again.')
            continue
        
        message = input('Enter the message to be encrypted (lower case): ').lower()
        encrypted_string, encrypted_num = encrypt_message(message, a, n)
        print('Encrypted message is:', encrypted_string)
        
        choice = input("Do you want to decrypt it too? (y/n): ")
        if choice.lower() == 'y':
            decrypted = decrypt_message(encrypted_string, encrypted_num, b, n)
            print("Decrypted message is:", decrypted)
        
        choice = input("Do you want to continue? (y/n): ")
        if choice.lower() != 'y':
            break


if __name__ == '__main__':
    main()