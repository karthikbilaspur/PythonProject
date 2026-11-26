# Binary Search Suite

Combined from your 3 files into ONE runnable file.

## What's inside
- `binary_search_suite.py` - single file, everything included

## 3 Original Versions (preserved as-is)
1. `binary_search_recursive(arr, target, low, high)` - recursive
2. `binary_search_iterative(arr, target)` - iterative, typed + docstring
3. `binary_search(arr, target)` - generic iterative

## NEW - Built from them
- `binary_search_trace(arr, target)` - step-by-step table: low/high/mid/decision
- `compare_all(arr, target)` - runs all 3, shows they agree + recursive call count
- `demo()` - tests 23, 2, 91, 100 (not found), 16
- `interactive()` - enter your own sorted array + targets

## How to run
python binary_search_suite.py

## Complexity
Time: O(log n) | Space: O(1) iterative, O(log n) recursive
Requirement: array MUST be sorted
