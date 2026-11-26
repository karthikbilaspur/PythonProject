"""
Sequential Search (Linear Search)
Searches one by one from left to right.
Time: O(n) worst | O(1) best | Space: O(1)
"""
def sequential_search(arr: list[int], target: int) -> tuple[int, int]:
    """Returns index of target, or -1. Also returns steps taken."""
    for i, val in enumerate(arr):
        if val == target:
            return i, i+1
    return -1, len(arr)

def sequential_search_trace(arr: list[int], target:int)-> tuple[int, int]:
    print(f"\nSearching for {target} in {arr}")
    print(f"{'Step':<6}{'Index':<7}{'Value':<7}Result")
    print("-"*40)
    for i, val in enumerate(arr, 1):
        if val == target:
            print(f"{i:<6}{arr.index(val) if False else i-1:<7}{val:<7}FOUND!")
            return i-1, i
        print(f"{i:<6}{i-1:<7}{val:<7}not match -> next")
    print("Not found - checked all elements.")
    return -1, len(arr)

def demo():
    arr = [34, 7, 23, 32, 5, 62, 32, 2]
    print("="*45); print("SEQUENTIAL SEARCH - DEMO"); print("="*45)
    print(f"Array (unsorted is OK): {arr}")
    for t in [23, 2, 99]:
        sequential_search_trace(arr, t)
        idx, steps = sequential_search(arr, t)
        print(f"Result: index={idx}, steps={steps}")

def interactive():
    print("\n--- Interactive ---")
    raw = input("Enter numbers separated by space (Enter for default): ").strip()
    arr = [int(x) for x in raw.split()] if raw else [34, 7, 23, 32, 5, 62, 32, 2]
    print(f"Array: {arr}")
    while True:
        t = input("Target (q to quit): ").strip()
        if t.lower()=='q': break
        try: target=int(t)
        except: print("Enter integer."); continue
        sequential_search_trace(arr, target)

def main():
    demo()
    if input("\nInteractive? (y/n): ").strip().lower()=='y': interactive()
    else: print("Done.")
if __name__=="__main__": main()
