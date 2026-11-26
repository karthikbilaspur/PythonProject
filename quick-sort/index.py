"""
Quick Sort
Time: O(n log n) average, O(n^2) worst (bad pivot) | Space: O(log n) | Stable: No | Fastest in practice, used in most libraries
"""
def quick_sort(arr: list[int], trace: bool = False, depth: int = 0) -> list[int]:
    """Pick pivot, put smaller left / bigger right, recurse on both sides."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]  # middle pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    if trace: print(f"{'  '*depth}Pivot={pivot} | {arr} -> Left {left} | Mid {middle} | Right {right}")
    return quick_sort(left, trace, depth+1) + middle + quick_sort(right, trace, depth+1)

def demo():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("="*50); print("QUICK SORT - DEMO"); print("="*50)
    print(f"Original: {arr}")
    print("\n--- Trace ---")
    result = quick_sort(arr.copy(), trace=True)
    print(f"\nSorted:   {result}")
    print("\n--- More tests ---")
    for test in [[5,4,3,2,1], [1,2,3,4,5], [3,1,4,1,5,9,2,6]]:
        print(f"{test} -> {quick_sort(test.copy())}")

def interactive():
    print("\n--- Interactive ---")
    raw = input("Enter numbers separated by space (Enter for default): ").strip()
    arr = [int(x) for x in raw.split()] if raw else [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    result = quick_sort(arr.copy(), trace=True)
    print(f"Sorted: {result}")

def main():
    demo()
    if input("\nInteractive? (y/n): ").strip().lower()=='y': interactive()
    else: print("Done.")
if __name__=="__main__": main()
