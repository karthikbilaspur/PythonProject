class Node:
    """Represents a node in the doubly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Represents a doubly linked list."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        """Appends a new node with the given data to the end of the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, data):
        """Prepends a new node with the given data to the beginning of the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def print_list(self):
        """Prints the elements of the list in forward order."""
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def print_reverse(self):
        """Prints the elements of the list in reverse order."""
        current = self.tail
        while current:
            print(current.data)
            current = current.prev

    def delete(self, data):
        """Deletes the node with the given data from the list."""
        current = self.head
        while current:
            if current.data == data:
                if current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                    else:
                        self.tail = None
                elif current == self.tail:
                    self.tail = current.prev
                    self.tail.next = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                self.size -= 1
                return
            current = current.next

    def search(self, data):
        """Searches for the node with the given data in the list."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False


# Example usage
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)
dll.prepend(0)
print("Forward traversal:")
dll.print_list()
print("Reverse traversal:")
dll.print_reverse()
dll.delete(2)
print("Forward traversal after deletion:")
dll.print_list()
print("Search for 3:")
print(dll.search(3))