from typing import Optional

class Node:
    def __init__(self, data: int):
        self.data = data
        self.next: Optional['Node'] = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data: int):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()

    def sort(self):
        current = self.head
        while current:
            next_node = current.next
            while next_node:
                if current.data > next_node.data:
                    current.data, next_node.data = next_node.data, current.data
                next_node = next_node.next
            current = current.next

# Create a linked list
ll = LinkedList()
ll.append(64)
ll.append(34)
ll.append(25)
ll.append(12)
ll.append(22)
ll.append(11)
ll.append(90)

# Print the linked list
print("Linked List:")
ll.print_list()

# Sort the linked list
ll.sort()

# Print the sorted linked list
print("Sorted Linked List:")
ll.print_list()