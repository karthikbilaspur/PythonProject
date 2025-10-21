def decimal_to_binary(n):
    """Convert decimal to binary."""
    return bin(n)[2:]


def decimal_to_octal(n):
    """Convert decimal to octal."""
    return oct(n)[2:]


def decimal_to_hexadecimal(n):
    """Convert decimal to hexadecimal."""
    return hex(n)[2:]


def binary_to_decimal(n):
    """Convert binary to decimal."""
    return int(n, 2)


def octal_to_decimal(n):
    """Convert octal to decimal."""
    return int(n, 8)


def hexadecimal_to_decimal(n):
    """Convert hexadecimal to decimal."""
    return int(n, 16)


def binary_to_octal(n):
    """Convert binary to octal."""
    decimal = binary_to_decimal(n)
    return decimal_to_octal(decimal)


def binary_to_hexadecimal(n):
    """Convert binary to hexadecimal."""
    decimal = binary_to_decimal(n)
    return decimal_to_hexadecimal(decimal)


def octal_to_binary(n):
    """Convert octal to binary."""
    decimal = octal_to_decimal(n)
    return decimal_to_binary(decimal)


def octal_to_hexadecimal(n):
    """Convert octal to hexadecimal."""
    decimal = octal_to_decimal(n)
    return decimal_to_hexadecimal(decimal)


def hexadecimal_to_binary(n):
    """Convert hexadecimal to binary."""
    decimal = hexadecimal_to_decimal(n)
    return decimal_to_binary(decimal)


def hexadecimal_to_octal(n):
    """Convert hexadecimal to octal."""
    decimal = hexadecimal_to_decimal(n)
    return decimal_to_octal(decimal)


def main():
    while True:
        print("Number Conversion Menu:")
        print("1. Decimal to Binary")
        print("2. Decimal to Octal")
        print("3. Decimal to Hexadecimal")
        print("4. Binary to Decimal")
        print("5. Octal to Decimal")
        print("6. Hexadecimal to Decimal")
        print("7. Binary to Octal")
        print("8. Binary to Hexadecimal")
        print("9. Octal to Binary")
        print("10. Octal to Hexadecimal")
        print("11. Hexadecimal to Binary")
        print("12. Hexadecimal to Octal")
        print("13. Quit")

        choice = input("Enter your choice: ")

        if choice == "13":
            break

        num = input("Enter the number: ")

        if choice == "1":
            print(f"The binary representation of {num} is {decimal_to_binary(int(num))}")
        elif choice == "2":
            print(f"The octal representation of {num} is {decimal_to_octal(int(num))}")
        elif choice == "3":
            print(f"The hexadecimal representation of {num} is {decimal_to_hexadecimal(int(num))}")
        elif choice == "4":
            print(f"The decimal representation of {num} is {binary_to_decimal(num)}")
        elif choice == "5":
            print(f"The decimal representation of {num} is {octal_to_decimal(num)}")
        elif choice == "6":
            print(f"The decimal representation of {num} is {hexadecimal_to_decimal(num)}")
        elif choice == "7":
            print(f"The octal representation of {num} is {binary_to_octal(num)}")
        elif choice == "8":
            print(f"The hexadecimal representation of {num} is {binary_to_hexadecimal(num)}")
        elif choice == "9":
            print(f"The binary representation of {num} is {octal_to_binary(num)}")
        elif choice == "10":
            print(f"The hexadecimal representation of {num} is {octal_to_hexadecimal(num)}")
        elif choice == "11":
            print(f"The binary representation of {num} is {hexadecimal_to_binary(num)}")
        elif choice == "12":
            print(f"The octal representation of {num} is {hexadecimal_to_octal(num)}")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()