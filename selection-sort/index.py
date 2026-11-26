"""
Selection Sort
Time: O(n^2) always (even if sorted) | Space: O(1) | Stable: No | In-place: Yes | Fewest swaps: at most n-1 swaps
"""
def selection_sort(arr: list[int], trace: bool = False) -> list[int]:
    """Each pass, find minimum in unsorted part and swap it to front."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        if trace: print(f"\nPass {i+1}: find min in {arr[i:]}")
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if trace: print(f"  Min = {arr[min_idx]} at index {min_idx}, swap with {arr[i]}")
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if trace: print(f"  After pass {i+1}: {arr}")
    return arr

def demo():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("="*50); print("SELECTION SORT - DEMO"); print("="*50)
    print(f"Original: {arr}")
    print("\n--- Trace ---")
    result = selection_sort(arr.copy(), trace=True)
    print(f"\nSorted:   {result}")
    print("\n--- More tests ---")
    for test in [[5,4,3,2,1], [1,2,3,4,5], [3,1,4,1,5,9,2,6]]:
        print(f"{test} -> {selection_sort(test.copy())}")

def interactive():
    print("\n--- Interactive ---")
    raw = input("Enter numbers separated by space (Enter for default): ").strip()
    arr = [int(x) for x in raw.split()] if raw else [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    result = selection_sort(arr.copy(), trace=True)
    print(f"Sorted: {result}")

def main():
    demo()
    if input("\nInteractive? (y/n): ").strip().lower()=='y': interactive()
    else: print("Done.")
if __name__=="__main__": main()
