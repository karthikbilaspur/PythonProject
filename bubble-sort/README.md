# Bubble Sort

 How to Run
bash
python bubble_sort.py

 How It Works
Compare neighbours, swap if left > right. Largest element 'bubbles' to the end each pass. Repeat until no swaps.

 Example

64 34 25 12 22 11 90\nPass 1: ... -> 34 25 12 22 11 64 90  (90 bubbled to end)\nPass 2: ... -> 25 12 22 11 34 64 90\n... until sorted: 11 12 22 25 34 64 90

 Features

- `bubble_sort(arr, trace=False)` - sorts and returns sorted list
- `trace=True` - prints every step / pass / swap
- `demo()` - tests unsorted, reverse, already-sorted, duplicates
- `interactive()` - enter your own numbers

 Complexity
Time: O(n^2) worst/average, O(n) best (already sorted, with early-stop) | Space: O(1) | Stable: Yes | In-place: Yes
