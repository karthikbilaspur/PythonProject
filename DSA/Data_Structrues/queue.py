class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, value):
        self.data.append(value)

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return None
        return self.data.pop(0)

    def peek(self):
        if self.is_empty():
            print("Queue is empty")
            return None
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def print_queue(self):
        print(self.data)

# Create a queue
q = Queue()
q.enqueue(5)
q.enqueue(10)
q.enqueue(3)
q.enqueue(8)

# Print the queue
print("Queue:")
q.print_queue()

# Dequeue a value
print("Dequeued value:")
print(q.dequeue())

# Print the queue after dequeue
print("Queue after dequeue:")
q.print_queue()

# Peek the front value
print("Front value:")
print(q.peek())

# Check if the queue is empty
print("Is queue empty?")
print(q.is_empty())

# Get the size of the queue
print("Queue size:")
print(q.size())