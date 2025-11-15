def merge_sort(arr: list[int]) -> list[int]:
    """Sort an array in ascending order using Merge Sort."""
    # Base case: If the array has 1 or fewer elements, it's already sorted
    if len(arr) <= 1:
        return arr
    
    # Split the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Recursively sort both halves
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)
    
    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    left_idx = right_idx = 0
    
    # Merge smaller elements first
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1
    
    # Append any remaining elements
    merged.extend(left[left_idx:])
    merged.extend(right[right_idx:])
    
    return merged
