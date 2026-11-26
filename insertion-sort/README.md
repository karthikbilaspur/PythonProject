# Insertion Sort

 How to Run
bash
python index.py

 How It Works
Take one card at a time (like sorting playing cards in hand) and insert it into the correct spot in the already-sorted left part. Shift bigger elements right to make room.

 Example
64 34 25 12 22 11 90\nTake 34, insert before 64 -> 34 64 25 12 22 11 90\nTake 25, insert at front -> 25 34 64 12 22 11 90\n... until sorted

 Features

- `insertion_sort(arr, trace=False)` - sorts and returns sorted list
- `trace=True` - prints every step / pass / swap
- `demo()` - tests unsorted, reverse, already-sorted, duplicates
- `interactive()` - enter your own numbers

 Complexity
Time: O(n^2) worst/average, O(n) best (already sorted) | Space: O(1) | Stable: Yes | In-place: Yes
