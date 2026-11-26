"""
Binary Search Suite - Combined from 3 versions
1. Recursive
2. Iterative (typed + docstring)
3. Generic / Simple iterative

Features:
- All 3 original implementations preserved
- Step-by-step trace (great for learning / viva)
- Side-by-side comparison + call-count comparison
- Interactive menu + auto demo
- Works on any sorted list
"""

# ---------- 1. Recursive (from File 1) ----------
def binary_search_recursive(arr: list, target: int, low: int, high: int) -> int:
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)


# ---------- 2. Iterative Typed (from File 2) ----------
def binary_search_iterative(arr: list, target: int) -> int:
    """
    Searches for an element in a sorted array using iterative binary search.
    Args:
        arr (list): A sorted list of elements.
        target (int): The element to search for.
    Returns:
        int: The index of the target element if found, -1 otherwise.
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# ---------- 3. Generic / Simple (from File 3) ----------
def binary_search(arr, target):
    """
    Searches for an element in a sorted array using binary search.
    Args:
        arr (list): A sorted list of elements.
        target: The element to search for.
    Returns:
        int: The index of the target element if found, -1 otherwise.
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# ---------- NEW: Something built from them - Trace + Comparison ----------
def binary_search_trace(arr, target):
    """Prints every step: low, high, mid, arr[mid] and decision."""
    low, high = 0, len(arr) - 1
    step = 1
    print(f"\nSearching for {target} in {arr}")
    print(f"{'Step':<6}{'low':<6}{'high':<6}{'mid':<6}{'arr[mid]':<9}Decision")
    print("-" * 55)
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            print(f"{step:<6}{low:<6}{high:<6}{mid:<6}{arr[mid]:<9}FOUND!")
            return mid
        elif arr[mid] < target:
            print(f"{step:<6}{low:<6}{high:<6}{mid:<6}{arr[mid]:<9}arr[mid] < target -> go RIGHT")
            low = mid + 1
        else:
            print(f"{step:<6}{low:<6}{high:<6}{mid:<6}{arr[mid]:<9}arr[mid] > target -> go LEFT")
            high = mid - 1
        step += 1
    print("Not found - search space exhausted.")
    return -1


def _count_recursive(arr, target, low, high, counter):
    counter[0] += 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return _count_recursive(arr, target, mid + 1, high, counter)
    else:
        return _count_recursive(arr, target, low, mid - 1, counter)


def compare_all(arr, target):
    """Runs all 3 and shows they agree."""
    c = [0]
    r1 = binary_search_recursive(arr, target, 0, len(arr) - 1)
    # recount for recursive
    c2 = [0]
    _count_recursive(arr, target, 0, len(arr) - 1, c2)
    r2 = binary_search_iterative(arr, target)
    r3 = binary_search(arr, target)
    print(f"\nTarget: {target}")
    print(f"  Recursive : index {r1}  (calls: {c2[0]})")
    print(f"  Iterative : index {r2}")
    print(f"  Generic   : index {r3}")
    print(f"  All agree: {r1 == r2 == r3}")
    return r1


def demo():
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    print("=" * 55)
    print("BINARY SEARCH SUITE - DEMO")
    print("=" * 55)
    for target in [23, 2, 91, 100, 16]:
        binary_search_trace(arr, target)
        compare_all(arr, target)
    print("\nNote: Array MUST be sorted for binary search to work.")
    print("Time: O(log n) | Space: O(1) iterative, O(log n) recursive (call stack)")


def interactive():
    print("\n--- Interactive Mode ---")
    print("Enter sorted numbers separated by space (or press Enter for default)")
    raw = input("Array: ").strip()
    if raw:
        try:
            arr = sorted([int(x) for x in raw.split()])
        except ValueError:
            print("Invalid input, using default array.")
            arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    else:
        arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    print(f"Using sorted array: {arr}")
    while True:
        t = input("Target to search (q to quit): ").strip()
        if t.lower() == 'q':
            break
        try:
            target = int(t)
        except ValueError:
            print("Enter an integer or q.")
            continue
        binary_search_trace(arr, target)
        compare_all(arr, target)


def main():
    demo()
    print("\n" + "=" * 55)
    choice = input("Run interactive mode? (y/n): ").strip().lower()
    if choice == 'y':
        interactive()
    else:
        print("Done. Run again and choose y for interactive mode.")


if __name__ == "__main__":
    main()
