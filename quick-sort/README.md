# Quick Sort

 How to Run
bash
python quick_sort.py

 How It Works
Pick a pivot. Partition: everything smaller goes left, bigger goes right. Pivot is now in final place. Recurse on left and right parts.

 Example
64 34 25 12 22 11 90 | pivot=12\nLeft=[11] Mid=[12] Right=[64 34 25 22 90]\nRecurse left/right... -> [11 12 22 25 34 64 90]

 Features

- `quick_sort(arr, trace=False)` - sorts and returns sorted list
- `trace=True` - prints every step / pass / swap
- `demo()` - tests unsorted, reverse, already-sorted, duplicates
- `interactive()` - enter your own numbers

 Complexity
Time: O(n log n) average, O(n^2) worst (bad pivot) | Space: O(log n) | Stable: No | Fastest in practice, used in most libraries
