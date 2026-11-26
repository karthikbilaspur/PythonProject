"""
Insertion Sort
Time: O(n^2) worst/average, O(n) best (already sorted) | Space: O(1) | Stable: Yes | In-place: Yes
"""
def insertion_sort(arr: list[int], trace: bool = False) -> list[int]:
    """Builds sorted part left-to-right, inserting each element in place."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        if trace: print(f"\nInsert {key} into {arr[:i]} | Full: {arr}")
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            if trace: print(f"  Shift {arr[j]} right -> {arr}")
            j -= 1
        arr[j+1] = key
        if trace: print(f"  Placed {key} at index {j+1} -> {arr}")
    return arr

def demo():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("="*50); print("INSERTION SORT - DEMO"); print("="*50)
    print(f"Original: {arr}")
    print("\n--- Trace ---")
    result = insertion_sort(arr.copy(), trace=True)
    print(f"\nSorted:   {result}")
    print("\n--- More tests ---")
    for test in [[5,4,3,2,1], [1,2,3,4,5], [3,1,4,1,5,9,2,6]]:
        print(f"{test} -> {insertion_sort(test.copy())}")

def interactive():
    print("\n--- Interactive ---")
    raw = input("Enter numbers separated by space (Enter for default): ").strip()
    arr = [int(x) for x in raw.split()] if raw else [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    result = insertion_sort(arr.copy(), trace=True)
    print(f"Sorted: {result}")

def main():
    demo()
    if input("\nInteractive? (y/n): ").strip().lower()=='y': interactive()
    else: print("Done.")
if __name__=="__main__": main()
