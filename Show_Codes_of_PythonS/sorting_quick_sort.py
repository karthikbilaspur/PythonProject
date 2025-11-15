def quick_sort(arr: list[int]) -> list[int]:
    """Sort an array in ascending order using Quick Sort."""
    # Base case: If the array has 1 or fewer elements, it's already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose a pivot element (in this case, the median of three elements)
    pivot = median_of_three(arr, 0, len(arr) // 2, len(arr) - 1)
    
    # Partition the array around the pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Recursively sort the left and right partitions
    return quick_sort(left) + middle + quick_sort(right)

def median_of_three(arr: list[int], low: int, mid: int, high: int) -> int:
    """Return the median of three elements."""
    if arr[low] < arr[mid]:
        if arr[mid] < arr[high]:
            return arr[mid]
        elif arr[low] < arr[high]:
            return arr[high]
        else:
            return arr[low]
    else:
        if arr[low] < arr[high]:
            return arr[low]
        elif arr[mid] < arr[high]:
            return arr[high]
        else:
            return arr[mid]
