class Stack:
    """Represents a dynamic stack."""
    def __init__(self):
        self.stack = []

    def is_empty(self):
        """Checks if the stack is empty."""
        return len(self.stack) == 0

    def push(self, data):
        """Adds an element to the top of the stack."""
        self.stack.append(data)

    def pop(self):
        """Removes an element from the top of the stack."""
        if self.is_empty():
            return "Stack is empty"
        else:
            return self.stack.pop()

    def peek(self):
        """Returns the top element of the stack without removing it."""
        if self.is_empty():
            return "Stack is empty"
        else:
            return self.stack[-1]

    def display(self):
        """Displays the elements of the stack."""
        if self.is_empty():
            print("Stack is empty")
        else:
            print(self.stack)


# Example usage
s = Stack()
s.push(1)
s.push(2)
s.push(3)
s.display()  # Output: [1, 2, 3]
print(s.peek())  # Output: 3
print(s.pop())  # Output: 3
s.display()  # Output: [1, 2]