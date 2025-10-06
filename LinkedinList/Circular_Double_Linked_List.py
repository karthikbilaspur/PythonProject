class Node:
    """Represents a node in the circular doubly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class CircularDoublyLinkedList:
    """Represents a circular doubly linked list."""
    def __init__(self):
        self.head = None

    def append(self, data):
        """Appends a new node with the given data to the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.prev = current
            new_node.next = self.head
            self.head.prev = new_node

    def prepend(self, data):
        """Prepends a new node with the given data to the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.prev = current
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def print_list(self):
        """Prints the elements of the list."""
        current = self.head
        while True:
            print(current.data)
            current = current.next
            if current == self.head:
                break

    def print_reverse(self):
        """Prints the elements of the list in reverse order."""
        current = self.head.prev
        while True:
            print(current.data)
            current = current.prev
            if current == self.head.prev:
                break

    def delete(self, data):
        """Deletes the node with the given data from the list."""
        if self.head:
            current = self.head
            while True:
                if current.data == data:
                    if current == self.head:
                        if current.next == self.head:
                            self.head = None
                        else:
                            current.prev.next = current.next
                            current.next.prev = current.prev
                            self.head = current.next
                    else:
                        current.prev.next = current.next
                        current.next.prev = current.prev
                    return
                current = current.next
                if current == self.head:
                    break


# Example usage
cdll = CircularDoublyLinkedList()
cdll.append(1)
cdll.append(2)
cdll.append(3)
cdll.prepend(0)
print("Forward traversal:")
cdll.print_list()
print("Reverse traversal:")
cdll.print_reverse()
cdll.delete(2)
print("Forward traversal after deletion:")
cdll.print_list()