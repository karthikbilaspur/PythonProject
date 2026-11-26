# Sequential Search (Linear Search)

 How to Run

```bash

python index.py
```

 How It Works
Check each element one by one from left to right.
Stop when found, or after checking all elements.

arr = [34, 7, 23, 32, 5]
target = 23
34 != 23 -> next
7  != 23 -> next
23 == 23 -> FOUND at index 2

 Features
`sequential_search(arr, target)` - returns (index, steps)
`sequential_search_trace()` - step-by-step table
`demo()` - tests found, first/last, not-found cases
 `interactive()` - enter your own array + target

 Complexity

- Time: O(n) worst/average, O(1) best (first element)
- Space: O(1)
- Works on UNSORTED arrays - unlike Binary Search
- Best for: small arrays, unsorted data, one-time search
