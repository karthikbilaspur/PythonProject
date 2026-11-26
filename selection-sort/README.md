# Selection Sort

 How to Run
bash
python selection_sort.py

 How It Works
Each pass, scan the unsorted part, find the smallest element, swap it to the front. Sorted part grows from left, unsorted shrinks.

 Example

64 34 25 12 22 11 90\nMin of all = 11, swap with 64 -> 11 34 25 12 22 64 90\nMin of rest = 12, swap with 34 -> 11 12 25 34 22 64 90\n... until sorted

 Features

- `selection_sort(arr, trace=False)` - sorts and returns sorted list
- `trace=True` - prints every step / pass / swap
- `demo()` - tests unsorted, reverse, already-sorted, duplicates
- `interactive()` - enter your own numbers

 Complexity
Time: O(n^2) always (even if sorted) | Space: O(1) | Stable: No | In-place: Yes | Fewest swaps: at most n-1 swaps
