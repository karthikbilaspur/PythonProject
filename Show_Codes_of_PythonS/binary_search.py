def binary_search(arr, target):
    """
    Searches for an element in a sorted array using binary search.

    Args:
        arr (list): A sorted list of elements.
        target: The element to search for.

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


# Example usage
if __name__ == "__main__":
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23

    result = binary_search(arr, target)

    if result != -1:
        print(f"Element {target} found at index {result}")
    else:
        print(f"Element {target} not found in the array")