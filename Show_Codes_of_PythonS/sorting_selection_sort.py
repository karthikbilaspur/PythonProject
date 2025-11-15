def selection_sort(arr: list[int]) -> list[int]:
    """Sort an array in ascending order using Selection Sort."""
    # Iterate over the array
    for i in range(len(arr)):
        # Initialize minimum index and value
        min_idx = i
        min_val = arr[i]
        swapped = False
        
        # Find the minimum element in the unsorted part of the array
        for j in range(i + 1, len(arr)):
            if arr[j] < min_val:
                min_idx = j
                min_val = arr[j]
                swapped = True
        
        # If no swaps were made, the array is already sorted
        if not swapped:
            break
        
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr