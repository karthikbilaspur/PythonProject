class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def enqueue(self, data):
        new_node = Node(data)
        if self.queue.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return "Queue is empty"
        else:
            temp = self.front
            self.front = self.front.next
            if self.front is None:
                self.rear = None
            self.size -= 1
            return temp.data

    def peek(self):
        if self.is_empty():
            return "Queue is empty"
        else:
            return self.front.data

    def display(self):
        if self.is_empty():
            print("Queue is empty")
        else:
            current = self.front
            while current:
                print(current.data, end=" ")
                current = current.next
            print()


# Example usage
q = Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
q.display()  # Output: 1 2 3
print(q.peek())  # Output: 1
print(q.dequeue())  # Output: 1
q.display()  # Output: 2 3