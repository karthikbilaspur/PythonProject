def binary_search_recursive(arr: list, target: int, low: int, high: int) -> int:

    if low > high:
        return -1

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)


def main():
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    index = binary_search_recursive(arr, target, 0, len(arr) - 1)

    if index != -1:
        print(f"Element {target} found at index {index}")
    else:
        print(f"Element {target} not found in the array")


if __name__ == "__main__":
    main()