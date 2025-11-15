def insertion_sort(arr: list[int]) -> list[int]:
    """Sort an array in ascending order using Insertion Sort."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Shift elements greater than key to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        # Insert key at its correct position
        arr[j + 1] = key
    
    return arr

# Example usage
arr = [12, 11, 13, 5, 6]
print("Original array:", arr)
sorted_arr = insertion_sort(arr)
print("Sorted array:", sorted_arr)