# Merge Sort

 How to Run
`bash
python merge_sort.py
`

 How It Works
Divide and Conquer: Split array in half again and again until 1 element (already sorted). Then merge halves back in sorted order.

 Example
`
64 34 25 12 22 11 90\nSplit -> [64 34 25] | [12 22 11 90]\nSplit -> ... until singles\nMerge -> [25 34 64] + [11 12 22 90] -> [11 12 22 25 34 64 90]
`

 Features

- `merge_sort(arr, trace=False)` - sorts and returns sorted list
- `trace=True` - prints every step / pass / swap
- `demo()` - tests unsorted, reverse, already-sorted, duplicates
- `interactive()` - enter your own numbers

 Complexity
Time: O(n log n) always | Space: O(n) extra | Stable: Yes | Best for large data, guaranteed fast
