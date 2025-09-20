from typing import List

def shell_sort(arr: List[int]) -> List[int]:
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

print(shell_sort([64, 34, 25, 12, 22, 11, 90]))