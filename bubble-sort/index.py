"""
Bubble Sort
Time: O(n^2) worst/average, O(n) best (already sorted, with early-stop) | Space: O(1) | Stable: Yes | In-place: Yes
"""
def bubble_sort(arr: list[int], trace: bool = False) -> list[int]:
    """Sorts by repeatedly swapping adjacent out-of-order elements."""
    n = len(arr)
    for i in range(n):
        swapped = False
        if trace: print(f"\nPass {i+1}:")
        for j in range(0, n-i-1):
            if trace: print(f"  Compare {arr[j]} vs {arr[j+1]}", end="")
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
                if trace: print(f" -> SWAP -> {arr}")
            elif trace: print(" -> ok")
        if trace: print(f"  After pass {i+1}: {arr}")
        if not swapped:
            if trace: print("  No swaps - already sorted, stopping early!")
            break
    return arr

def demo():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("="*50); print("BUBBLE SORT - DEMO"); print("="*50)
    print(f"Original: {arr}")
    print("\n--- Trace ---")
    result = bubble_sort(arr.copy(), trace=True)
    print(f"\nSorted:   {result}")
    print("\n--- More tests ---")
    for test in [[5,4,3,2,1], [1,2,3,4,5], [3,1,4,1,5,9,2,6]]:
        print(f"{test} -> {bubble_sort(test.copy())}")

def interactive():
    print("\n--- Interactive ---")
    raw = input("Enter numbers separated by space (Enter for default): ").strip()
    arr = [int(x) for x in raw.split()] if raw else [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    result = bubble_sort(arr.copy(), trace=True)
    print(f"Sorted: {result}")

def main():
    demo()
    if input("\nInteractive? (y/n): ").strip().lower()=='y': interactive()
    else: print("Done.")
if __name__=="__main__": main()
