def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

print(linear_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23))