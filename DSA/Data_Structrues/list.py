from typing import Any

class List:
    def __init__(self):
        self.data: list[Any] = []

    def append(self, value: Any):
        self.data.append(value)

    def insert(self, index: int, value: Any):
        self.data.insert(index, value)

    def delete(self, index: int):
        if index < len(self.data):
            del self.data[index]
        else:
            print("Index out of range")

    def get(self, index: int):
        if index < len(self.data):
            return self.data[index]
        else:
            print("Index out of range")

    def update(self, index: int, value: Any):
        if index < len(self.data):
            self.data[index] = value
        else:
            print("Index out of range")

    def print_list(self):
        print(self.data)

    def sort(self):
        self.data.sort()

    def reverse(self):
        self.data.reverse()

# Create a list
l = List()
l.append(5)
l.append(10)
l.append(3)
l.append(8)

# Print the list
print("List:")
l.print_list()

# Insert a value
l.insert(2, 7)
print("List after insertion:")
l.print_list()

# Delete a value
l.delete(1)
print("List after deletion:")
l.print_list()

# Get a value
print("Value at index 1:")
print(l.get(1))

# Update a value
l.update(1, 9)
print("List after update:")
l.print_list()

# Sort the list
l.sort()
print("Sorted list:")
l.print_list()

# Reverse the list
l.reverse()
print("Reversed list:")
l.print_list()