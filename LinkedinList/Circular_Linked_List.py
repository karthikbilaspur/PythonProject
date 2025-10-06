class Node:
    """Represents a node in the circular linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList:
    """Represents a circular linked list."""
    def __init__(self):
        self.head = None

    def append(self, data):
        """Appends a new node with the given data to the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def print_list(self):
        """Prints the elements of the list."""
        current = self.head
        while True:
            print(current.data)
            current = current.next
            if current == self.head:
                break

    def delete(self, data):
        """Deletes the node with the given data from the list."""
        if self.head:
            if self.head.data == data:
                if self.head.next == self.head:
                    self.head = None
                else:
                    current = self.head
                    while current.next != self.head:
                        current = current.next
                    current.next = self.head.next
                    self.head = self.head.next
            else:
                current = self.head
                while current.next != self.head:
                    if current.next.data == data:
                        current.next = current.next.next
                        return
                    current = current.next


# Example usage
cll = CircularLinkedList()
cll.append(1)
cll.append(2)
cll.append(3)
cll.append(4)
print("Circular Linked List:")
cll.print_list()
cll.delete(3)
print("After deletion:")
cll.print_list()