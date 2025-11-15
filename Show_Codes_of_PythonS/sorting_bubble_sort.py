def bubble_sort(arr: list[int]) -> list[int]:
    """Sort an array in ascending order using Bubble Sort."""
    n = len(arr)
    for i in range(n):
        # Flag to track if any swaps were made
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no swaps were made, the array is already sorted
        if not swapped:
            break
    
    return arr

