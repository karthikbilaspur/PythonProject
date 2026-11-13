# Algorithms Playground

All 9 classic algorithms in one clean Python file — searching, sorting, and Dijkstra's shortest path — with demos, tests, benchmarks, and an interactive menu.

Files
File Description
algorithms.py The whole project. Run this.
README.md This file.
No other files needed. No external dependencies — just Python's standard library.

Requirements
Python 3.9+
python --version
or on Mac / Linux:

python3 --version
That's it. No pip install needed.

How to run

1. Interactive menu (easiest)
python algorithms.py
You get a menu:

=== ALGORITHMS PLAYGROUND ===

1. Demo all algorithms
2. Run tests
3. Benchmark sorts
4. Try your own numbers (sort)
5. Try your own search
6. Try Dijkstra
7. Exit
Try option 4 — type your own numbers like 64 34 25 12 22 11 90 and see all 6 sorts run on them.

2.One-shot commands
python algorithms.py --demo     # run all 9 algorithms on sample data
python algorithms.py --test     # run 58 correctness tests
python algorithms.py --bench    # race all sorts on 2,000 random numbers

What's inside
Searching
Function Needs Time When to use
linear_search(arr, target) Any array O(n) Small / unsorted data
binary_search(arr, target) Sorted array O(log n) Large sorted data
Both return the index of the target, or -1 if not found.

from algorithms import linear_search, binary_search

arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
linear_search(arr, 23)  # -> 5
binary_search(arr, 23)  # -> 5
binary_search(arr, 99)  # -> -1
Sorting
All 6 sorts take a list and return a new sorted list. They do not mutate your input.

Function Time (worst) Stable? Best for
bubble_sort(arr) O(n²) Yes Learning only — too slow for real data
selection_sort(arr) O(n²) No When swaps are expensive
insertion_sort(arr) O(n²), O(n) if nearly sorted Yes Small / nearly-sorted data
shell_sort(arr) O(n log n) No Faster version of insertion sort
merge_sort(arr) O(n log n) Yes Predictable, stable, uses extra memory
quick_sort(arr) O(n log n) avg, O(n²) worst No Fast in practice
from algorithms import bubble_sort, merge_sort, quick_sort

data = [64, 34, 25, 12, 22, 11, 90]
bubble_sort(data)  # -> [11, 12, 22, 25, 34, 64, 90]
merge_sort(data)   # -> [11, 12, 22, 25, 34, 64, 90]
quick_sort(data)   # -> [11, 12, 22, 25, 34, 64, 90]
print(data)        # -> [64, 34, 25, 12, 22, 11, 90]  (unchanged!)
Graph — Dijkstra's Shortest Path
from algorithms import dijkstra

graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

dijkstra(graph, 'A')
-> {'A': 0, 'B': 1, 'C': 3, 'D': 4}
 Meaning: A->C is 3 via A-B-C, not 4 direct.
          A->D is 4 via A-B-C-D.
Rules:

Edge weights must be >= 0. Negative weights raise a ValueError — use Bellman-Ford for those.
Start node must exist in the graph, or it raises a ValueError.
Returns a dict of {node: shortest_distance_from_start}.
Example output
--demo
=== SEARCHING ===
Array: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
linear_search(..., 23) = 5
binary_search(..., 23) = 5

=== SORTING ===
Input: [64, 34, 25, 12, 22, 11, 90]
bubble_sort                  -> [11, 12, 22, 25, 34, 64, 90]
merge_sort                   -> [11, 12, 22, 25, 34, 64, 90]
quick_sort                   -> [11, 12, 22, 25, 34, 64, 90]

=== DIJKSTRA ===

From A: {'A': 0, 'B': 1, 'C': 3, 'D': 4}

--bench (2,000 random numbers)

Benchmark — sorting 2000 random numbers (lower = faster)

Algorithm                      Time (s)  Complexity

------------------------------------------------------------
bubble_sort                      0.2260  O(n^2)
selection_sort                   0.1015  O(n^2)
insertion_sort                   0.1002  O(n^2)
shell_sort                       0.0044  O(n log n)~
merge_sort                       0.0045  O(n log n)
quick_sort                       0.0033  O(n log n) avg
python_sorted (built-in)         0.0002  O(n log n)

Winner: python_sorted (built-in) (0.0002s) | Slowest: bubble_sort (0.2260s)
Takeaway: bubble sort is ~1,000x slower than Python's built-in sorted(). In real code, use sorted() / .sort().

--test
Tests: 58 passed, 0 failed
Tests cover: empty list, single element, duplicates, reverse-sorted, already sorted, random data, search hits/misses, and the Dijkstra sample graph.

How to use it as a library
You don't have to run the menu — just import what you need:

in your own file, in the same folder:
from algorithms import merge_sort, binary_search, dijkstra

print(merge_sort([5, 2, 9, 1]))       # [1, 2, 5, 9]
print(binary_search([1, 2, 5, 9], 5))  # 2
What was fixed vs. the original snippets

Issue in originals Fix in this file
Sorts mutated the input list in-place All sorts now return a new list, input unchanged
bubble_sort never stopped early Added early-exit if no swaps in a pass
dijkstra crashed on bad start node Raises a clear ValueError
dijkstra silently broke on negative weights Raises a clear ValueError
No type hints / docs Every function has type hints + docstring + Big-O
9 separate snippets, no way to compare One file + --demo, --test, --bench

Troubleshooting
Problem Fix
python: command not found Try python3 algorithms.py on Mac / Linux
ModuleNotFoundError You don't need any installs — this uses only the standard library. Make sure you're running the file from its own folder.
binary_search returns -1 for a value that's there Your array must be sorted first. Sort it, then search.
dijkstra raises ValueError: negative weights Dijkstra can't handle negative weights. Use Bellman-Ford instead.
Customizing
Benchmark size: python algorithms.py --bench uses 2,000 numbers. In the menu, option 3 asks you how many you want.
Your own graph: In the menu, option 6 uses the sample graph. To use your own, import dijkstra and pass your graph dict (see example above).
Add a new algorithm: Add a function, then add it to the SORTS dict near the bottom — it will automatically appear in demo, tests, and benchmark.
Cheat sheet — which one do I pick?
Searching a small list? → linear_search
Searching a large sorted list? → binary_search
Sorting for real code? → Python's built-in sorted()
Learning / interview? → Know merge_sort + quick_sort + binary_search cold
Nearly sorted data? → insertion_sort
Shortest path, no negative weights? → dijkstra
