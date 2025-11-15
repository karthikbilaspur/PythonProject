def binary_search_iterative(arr: list, target: int) -> int:
    """
    Searches for an element in a sorted array using iterative binary search.

    Args:
        arr (list): A sorted list of elements.
        target (int): The element to search for.

    Returns:
        int: The index of the target element if found, -1 otherwise.
    """
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def main():
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    index = binary_search_iterative(arr, target)

    if index != -1:
        print(f"Element {target} found at index {index}")
    else:
        print(f"Element {target} not found in the array")


if __name__ == "__main__":
    main()