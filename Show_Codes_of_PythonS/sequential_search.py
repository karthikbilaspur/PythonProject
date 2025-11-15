def sequential_search(arr: list[int], target: int) -> int:
    
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1


def main():
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    index = sequential_search(arr, target)

    if index != -1:
        print(f"Element {target} found at index {index}")
    else:
        print(f"Element {target} not found in the array")


if __name__ == "__main__":
    main()