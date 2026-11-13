"""
algorithms.py — Sorting, Searching & Graph Algorithms in one place
=================================================================
All 9 algorithms from your snippets, cleaned up + unified:

Searching:
  1. linear_search
  2. binary_search  (needs sorted array)

Sorting:
  3. bubble_sort
  4. selection_sort
  5. insertion_sort
  6. shell_sort
  7. merge_sort
  8. quick_sort

Graph:
  9. dijkstra

Run:
    python index.py            -> interactive menu
    python index.py --demo     -> run all demos
    python index.py --test     -> run correctness tests
    python index.py --bench    -> benchmark all sorts
"""

import sys
import heapq
import random
import time
from typing import List, Dict, Callable, cast

# ------------------------------------------------------------------
# SEARCHING
# ------------------------------------------------------------------

def linear_search(arr: List[int], target: int) -> int:
    """Return index of target, or -1. Works on UNSORTED arrays. O(n)."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


def binary_search(arr: List[int], target: int) -> int:
    """Return index of target, or -1. Requires SORTED array. O(log n)."""
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


# ------------------------------------------------------------------
# SORTING — all return a NEW sorted list (no surprise mutation)
# ------------------------------------------------------------------

def bubble_sort(arr: List[int]) -> List[int]:
    """O(n^2). Simple, slow. Good for learning, bad for real data."""
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:  # early exit if already sorted
            break
    return a


def selection_sort(arr: List[int]) -> List[int]:
    """O(n^2). Few swaps, many comparisons."""
    a = arr.copy()
    for i in range(len(a)):
        min_index = i
        for j in range(i + 1, len(a)):
            if a[j] < a[min_index]:
                min_index = j
        a[i], a[min_index] = a[min_index], a[i]
    return a


def insertion_sort(arr: List[int]) -> List[int]:
    """O(n^2) worst, O(n) if nearly sorted. Great for small / almost-sorted data."""
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def shell_sort(arr: List[int]) -> List[int]:
    """O(n log n) ~ O(n^2). Insertion sort with gaps — much faster than plain insertion."""
    a = arr.copy()
    gap = len(a) // 2
    while gap > 0:
        for i in range(gap, len(a)):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2
    return a


def merge_sort(arr: List[int]) -> List[int]:
    """O(n log n). Stable, predictable. Uses extra memory."""
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    merged: List[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr: List[int]) -> List[int]:
    """O(n log n) avg, O(n^2) worst. Fast in practice, not stable."""
    if len(arr) <= 1:
        return arr.copy()
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# ------------------------------------------------------------------
# GRAPH — DIJKSTRA
# ------------------------------------------------------------------

def dijkstra(graph: Dict[str, Dict[str, int]], start: str) -> Dict[str, int]:
    """
    Shortest distance from `start` to every other node.
    graph = {'A': {'B': 1, 'C': 4}, ...}  weights must be >= 0
    Returns: {'A': 0, 'B': 1, 'C': 3, 'D': 4}
    """
    if start not in graph:
        raise ValueError(f"Start node '{start}' not in graph")
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            if weight < 0:
                raise ValueError("Dijkstra does not work with negative weights")
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances


# ------------------------------------------------------------------
# DEMO / TEST / BENCHMARK
# ------------------------------------------------------------------

SORTS: Dict[str, Callable[..., List[int]]] = {
    "bubble_sort": bubble_sort,
    "selection_sort": selection_sort,
    "insertion_sort": insertion_sort,
    "shell_sort": shell_sort,
    "merge_sort": merge_sort,
    "quick_sort": quick_sort,
    "python_sorted (built-in)": sorted,
}

SAMPLE_SORT = [64, 34, 25, 12, 22, 11, 90]
SAMPLE_SEARCH = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
SAMPLE_GRAPH = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

def demo():
    print("=== SEARCHING ===")
    print(f"Array: {SAMPLE_SEARCH}")
    print(f"linear_search(..., 23) = {linear_search(SAMPLE_SEARCH, 23)}")
    print(f"binary_search(..., 23) = {binary_search(SAMPLE_SEARCH, 23)}")
    print(f"binary_search(..., 99) = {binary_search(SAMPLE_SEARCH, 99)}  (not found)")
    print("\n=== SORTING ===")
    print(f"Input: {SAMPLE_SORT}")
    for name, fn in SORTS.items():
        print(f"{name:28} -> {fn(SAMPLE_SORT)}")
    print("\n=== DIJKSTRA ===")
    print(f"Graph: {SAMPLE_GRAPH}")
    print(f"From A: {dijkstra(SAMPLE_GRAPH, 'A')}")
    print("Meaning: A->A=0, A->B=1, A->C=3 (A-B-C), A->D=4 (A-B-C-D)")

def test():
    cases: List[List[int]] = [
        [],
        [1],
        [3, 1, 2],
        [5, 5, 5],
        [9, 8, 7, 6],
        [64, 34, 25, 12, 22, 11, 90],
        list(range(100, 0, -1)),
    ]
    passed = failed = 0
    for name, fn in SORTS.items():
        for c in cases:
            if fn(c) == sorted(c):
                passed += 1
            else:
                failed += 1
                print(f"FAIL {name} on {c[:10]}")
    search_cases: List[tuple[List[int], int, int]] = [
        (SAMPLE_SEARCH, 23, 5),
        (SAMPLE_SEARCH, 2, 0),
        (SAMPLE_SEARCH, 99, -1),
        ([], 1, -1),
    ]
    for arr, target, expected in search_cases:
        for fn in [linear_search, binary_search]:
            ok = fn(arr, target) == expected
            passed += ok; failed += (not ok)
            if not ok:
                print(f"FAIL {fn.__name__}({arr}, {target})")
    assert dijkstra(SAMPLE_GRAPH, 'A') == {'A': 0, 'B': 1, 'C': 3, 'D': 4}, "dijkstra failed"
    passed += 1
    print(f"Tests: {passed} passed, {failed} failed")
    return failed == 0

def benchmark(n: int = 2000, seed: int = 42):
    print(f"\nBenchmark — sorting {n} random numbers (lower = faster)")
    print(f"{'Algorithm':28} {'Time (s)':>10}  {'Complexity'}")
    print("-" * 60)
    random.seed(seed)
    data = [random.randint(0, 10000) for _ in range(n)]
    complexities = {
        "bubble_sort": "O(n^2)", "selection_sort": "O(n^2)", "insertion_sort": "O(n^2)",
        "shell_sort": "O(n log n)~", "merge_sort": "O(n log n)", "quick_sort": "O(n log n) avg",
        "python_sorted (built-in)": "O(n log n)",
    }
    results: list[tuple[float, str]] = []
    for name, fn in SORTS.items():
        start = time.perf_counter()
        fn(data)
        elapsed = time.perf_counter() - start
        results.append((elapsed, name))
        print(f"{name:28} {elapsed:10.4f}  {complexities[name]}")
    results.sort()
    print(f"\nWinner: {results[0][1]} ({results[0][0]:.4f}s)  |  Slowest: {results[-1][1]} ({results[-1][0]:.4f}s)")

def menu():
    while True:
        print("\n=== ALGORITHMS PLAYGROUND ===")
        print("1. Demo all algorithms")
        print("2. Run tests")
        print("3. Benchmark sorts")
        print("4. Try your own numbers (sort)")
        print("5. Try your own search")
        print("6. Try Dijkstra")
        print("7. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            demo()
        elif choice == "2":
            test()
        elif choice == "3":
            try:
                n = int(input("How many numbers? [2000]: ") or 2000)
            except ValueError:
                n = 2000
            benchmark(n)
        elif choice == "4":
            try:
                nums = [int(x) for x in input("Enter numbers separated by space: ").split()]
                print(f"Original: {nums}")
                for name, fn in SORTS.items():
                    print(f"{name:28} -> {fn(nums)}")
            except ValueError:
                print("Please enter only numbers.")
        elif choice == "5":
            try:
                nums = [int(x) for x in input("Enter SORTED numbers separated by space: ").split()]
                target = int(input("Target: "))
                print(f"linear_search = {linear_search(nums, target)}")
                print(f"binary_search = {binary_search(nums, target)}")
            except ValueError:
                print("Please enter only numbers.")
        elif choice == "6":
            print("Sample graph:", SAMPLE_GRAPH)
            start = input("Start node [A]: ").strip() or "A"
            try:
                print(dijkstra(SAMPLE_GRAPH, start))
            except ValueError as e:
                print(e)
        elif choice == "7":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--test" in sys.argv:
        test()
    elif "--bench" in sys.argv:
        benchmark()
    else:
        menu()