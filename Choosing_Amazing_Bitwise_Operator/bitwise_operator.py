def bitwise_operations(a, b):
    print(f"Binary representation of {a}: {bin(a)}")
    print(f"Binary representation of {b}: {bin(b)}")

    # Bitwise AND
    and_result = a & b
    print(f"Bitwise AND: {a} & {b} = {and_result} ({bin(and_result)})")

    # Bitwise OR
    or_result = a | b
    print(f"Bitwise OR: {a} | {b} = {or_result} ({bin(or_result)})")

    # Bitwise XOR
    xor_result = a ^ b
    print(f"Bitwise XOR: {a} ^ {b} = {xor_result} ({bin(xor_result)})")

    # Bitwise NOT
    not_result_a = ~a
    not_result_b = ~b
    print(f"Bitwise NOT: ~{a} = {not_result_a} ({bin(not_result_a)})")
    print(f"Bitwise NOT: ~{b} = {not_result_b} ({bin(not_result_b)})")

    # Left Shift
    left_shift_result = a << 2
    print(f"Left Shift: {a} << 2 = {left_shift_result} ({bin(left_shift_result)})")

    # Right Shift
    right_shift_result = a >> 2
    print(f"Right Shift: {a} >> 2 = {right_shift_result} ({bin(right_shift_result)})")

def main():
    while True:
        print("Bitwise Operations Menu:")
        print("1. Perform bitwise operations")
        print("2. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                a = int(input("Enter the first number: "))
                b = int(input("Enter the second number: "))
                bitwise_operations(a, b)
            except ValueError:
                print("Invalid input. Please enter integers.")
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()