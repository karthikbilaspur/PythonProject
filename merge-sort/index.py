"""
Merge Sort
Time: O(n log n) always | Space: O(n) extra | Stable: Yes | Best for large data, guaranteed fast
"""
def merge_sort(arr: list[int], trace: bool = False, depth: int = 0) -> list[int]:
    """Divide array in half, sort each half, merge sorted halves."""
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    if trace: print(f"{'  '*depth}Split {arr} -> {left} | {right}")
    left = merge_sort(left, trace, depth+1)
    right = merge_sort(right, trace, depth+1)
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:]); merged.extend(right[j:])
    if trace: print(f"{'  '*depth}Merge {left} + {right} -> {merged}")
    return merged

def demo():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("="*50); print("MERGE SORT - DEMO"); print("="*50)
    print(f"Original: {arr}")
    print("\n--- Trace ---")
    result = merge_sort(arr.copy(), trace=True)
    print(f"\nSorted:   {result}")
    print("\n--- More tests ---")
    for test in [[5,4,3,2,1], [1,2,3,4,5], [3,1,4,1,5,9,2,6]]:
        print(f"{test} -> {merge_sort(test.copy())}")

def interactive():
    print("\n--- Interactive ---")
    raw = input("Enter numbers separated by space (Enter for default): ").strip()
    arr = [int(x) for x in raw.split()] if raw else [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    result = merge_sort(arr.copy(), trace=True)
    print(f"Sorted: {result}")

def main():
    demo()
    if input("\nInteractive? (y/n): ").strip().lower()=='y': interactive()
    else: print("Done.")
if __name__=="__main__": main()
