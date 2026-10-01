def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def print_inverted_star_pattern(n):
    for i in range(n, 0, -1):
        print("* " * i)

def main():
    numbers = []
    n = int(input("Enter the number of elements: "))
    for i in range(n):
        num = int(input(f"Enter element {i+1}: "))
        numbers.append(num)

    print("Original list:", numbers)
    sorted_numbers = bubble_sort(numbers)
    print("Sorted list:", sorted_numbers)

    print("\nInverted Star Pattern:")
    print_inverted_star_pattern(n)

if __name__ == "__main__":
    main()