class Node:
    """Represents a node in the linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Represents a linear linked list."""
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        """Checks if the list is empty."""
        return self.size == 0

    def insert_at_head(self, data):
        """Inserts a new node at the head of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at_tail(self, data):
        """Inserts a new node at the tail of the list."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def delete(self, data):
        """Deletes the first occurrence of the node with the given data."""
        if self.is_empty():
            return "List is empty"
        elif self.head.data == data:
            self.head = self.head.next
            self.size -= 1
        else:
            current = self.head
            while current.next:
                if current.next.data == data:
                    current.next = current.next.next
                    self.size -= 1
                    return
                current = current.next

    def search(self, data):
        """Searches for the node with the given data."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def display(self):
        """Displays the elements of the list."""
        if self.is_empty():
            print("List is empty")
        else:
            current = self.head
            while current:
                print(current.data, end=" ")
                current = current.next
            print()


# Example usage
ll = LinkedList()
ll.insert_at_tail(1)
ll.insert_at_tail(2)
ll.insert_at_tail(3)
ll.insert_at_head(0)
ll.display()  # Output: 0 1 2 3
print(ll.search(2))  # Output: True
ll.delete(2)