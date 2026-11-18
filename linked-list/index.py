"""
All Data Structures in One File
--------------------------------
1. Singly Linked List
2. Doubly Linked List
3. Circular Linked List (Singly)
4. Circular Doubly Linked List
5. Stack
6. Queue
"""

# =====================================================================
# SHARED NODE
# One Node works for all lists: singly lists just ignore `prev`.
# =====================================================================
from typing import Optional


class Node:
    def __init__(self, data: object):
        self.data = data
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None

    def __repr__(self):
        return f"Node({self.data})"


# =====================================================================
# 1. SINGLY LINKED LIST
# =====================================================================
class LinkedList:
    """Linear singly linked list."""
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def insert_at_head(self, data: object):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at_tail(self, data: object):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            if current is not None:
                while current.next is not None:
                    current = current.next
                current.next = new_node
        self.size += 1

    # alias so all lists have same API
    append = insert_at_tail
    prepend = insert_at_head

    def delete(self, data: object):
        if self.is_empty():
            return "List is empty"
        if self.head is not None and self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return
        current = self.head
        while current is not None and current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return
            current = current.next

    def search(self, data: object):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def display(self):
        if self.is_empty():
            print("List is empty")
            return
        current = self.head
        while current:
            print(current.data, end=" -> " if current.next else "\n")
            current = current.next


# =====================================================================
# 2. DOUBLY LINKED LIST
# =====================================================================
class DoublyLinkedList:
    """Linear doubly linked list."""
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0

    def append(self, data: object):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, data: object):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def delete(self, data: object):
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
                    if self.tail:
                        self.tail.next = None
                else:
                    assert current.prev is not None and current.next is not None
                    current.prev.next = current.next
                    current.next.prev = current.prev
                self.size -= 1
                return
            current = current.next

    def search(self, data: object):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" <-> " if current.next else "\n")
            current = current.next

    def print_reverse(self):
        current = self.tail
        while current:
            print(current.data, end=" <-> " if current.prev else "\n")
            current = current.prev


# =====================================================================
# 3. CIRCULAR LINKED LIST (SINGLY)
# =====================================================================
class CircularLinkedList:
    """Circular singly linked list. Last node -> head."""
    def __init__(self):
        self.head = None

    def append(self, data: object):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            assert current is not None
            while current.next != self.head:
                assert current.next is not None
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def delete(self, data: object):
        if not self.head:
            return
        if self.head.data == data:
            if self.head.next == self.head:
                self.head = None
            else:
                current = self.head
                while current.next != self.head:
                    assert current.next is not None
                    current = current.next
                current.next = self.head.next
                self.head = self.head.next
        else:
            current = self.head
            while current.next != self.head:
                assert current.next is not None
                if current.next.data == data:
                    current.next = current.next.next
                    return
                current = current.next

    def print_list(self):
        if not self.head:
            print("List is empty")
            return
        current = self.head
        while True:
            assert current is not None
            print(current.data, end=" -> ")
            current = current.next
            assert current is not None
            if current == self.head:
                print("(back to head)")
                break


# =====================================================================
# 4. CIRCULAR DOUBLY LINKED LIST
# =====================================================================
class CircularDoublyLinkedList:
    """Circular doubly linked list. head.prev = tail, tail.next = head."""
    def __init__(self):
        self.head = None

    def append(self, data: object):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            tail = self.head.prev
            assert tail is not None
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def prepend(self, data: object):
        self.append(data)
        assert self.head is not None
        self.head = self.head.prev  # new node becomes head

    def delete(self, data: object):
        if not self.head:
            return
        current = self.head
        while True:
            assert current is not None
            if current.data == data:
                if current.next == current:  # only one node
                    self.head = None
                else:
                    prev_node = current.prev
                    next_node = current.next
                    assert prev_node is not None
                    assert next_node is not None
                    prev_node.next = next_node
                    next_node.prev = prev_node
                    if current == self.head:
                        self.head = current.next
                return
            current = current.next
            if current == self.head:
                break

    def print_list(self):
        if not self.head:
            print("List is empty")
            return
        current = self.head
        while True:
            assert current is not None
            print(current.data, end=" <-> ")
            current = current.next
            if current == self.head:
                print("(back to head)")
                break

    def print_reverse(self):
        if not self.head:
            print("List is empty")
            return
        current = self.head.prev
        while True:
            assert current is not None
            print(current.data, end=" <-> ")
            current = current.prev
            if current == self.head.prev:
                print("(back to tail)")
                break


# =====================================================================
# 5. STACK (LIFO) - using Python list
# =====================================================================
class Stack:
    """Dynamic stack."""
    def __init__(self):
        self.stack: list[object] = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, data: object):
        self.stack.append(data)

    def pop(self):
        if self.is_empty():
            return "Stack is empty"
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return "Stack is empty"
        return self.stack[-1]

    def display(self):
        if self.is_empty():
            print("Stack is empty")
        else:
            print(self.stack)


# =====================================================================
# 6. QUEUE (FIFO) - using linked list
# BUG FIXED: was `self.queue.is_empty()` -> now `self.is_empty()`
# =====================================================================
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def enqueue(self, data: object):
        new_node = Node(data)
        if self.is_empty():  # FIXED
            self.front = self.rear = new_node
        else:
            assert self.rear is not None
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return "Queue is empty"
        assert self.front is not None
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return temp.data

    def peek(self):
        if self.is_empty():
            return "Queue is empty"
        assert self.front is not None
        return self.front.data

    def display(self):
        if self.is_empty():
            print("Queue is empty")
            return
        current = self.front
        while current:
            print(current.data, end=" ")
            current = current.next
        print()


# =====================================================================
# DEMO / EXAMPLE USAGE
# =====================================================================
if __name__ == "__main__":
    print("--- Singly Linked List ---")
    ll = LinkedList()
    ll.insert_at_tail(1); ll.insert_at_tail(2); ll.insert_at_tail(3); ll.insert_at_head(0)
    ll.display()
    print("Search 2:", ll.search(2))
    ll.delete(2); ll.display()

    print("\n--- Doubly Linked List ---")
    dll = DoublyLinkedList()
    dll.append(1); dll.append(2); dll.append(3); dll.prepend(0)
    dll.print_list(); dll.print_reverse()
    dll.delete(2); dll.print_list()

    print("\n--- Circular Linked List ---")
    cll = CircularLinkedList()
    cll.append(1); cll.append(2); cll.append(3); cll.append(4)
    cll.print_list(); cll.delete(3); cll.print_list()

    print("\n--- Circular Doubly Linked List ---")
    cdll = CircularDoublyLinkedList()
    cdll.append(1); cdll.append(2); cdll.append(3); cdll.prepend(0)
    cdll.print_list(); cdll.print_reverse()
    cdll.delete(2); cdll.print_list()

    print("\n--- Stack ---")
    s = Stack()
    s.push(1); s.push(2); s.push(3); s.display()
    print("Peek:", s.peek(), "| Pop:", s.pop()); s.display()

    print("\n--- Queue ---")
    q = Queue()
    q.enqueue(1); q.enqueue(2); q.enqueue(3); q.display()
    print("Peek:", q.peek(), "| Dequeue:", q.dequeue()); q.display()
