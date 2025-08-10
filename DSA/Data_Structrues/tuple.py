class Tuple:
    def __init__(self, *args):
        self.data = args

    def get(self, index):
        if index < len(self.data):
            return self.data[index]
        else:
            print("Index out of range")

    def length(self):
        return len(self.data)

    def print_tuple(self):
        print(self.data)

    def index_of(self, value):
        try:
            return self.data.index(value)
        except ValueError:
            print("Value not found in tuple")

    def count(self, value):
        return self.data.count(value)

# Create a tuple
t = Tuple(1, 2, 3, 4, 5, 2, 3)

# Print the tuple
print("Tuple:")
t.print_tuple()

# Get a value
print("Value at index 2:")
print(t.get(2))

# Get the length
print("Length of tuple:")
print(t.length())

# Get the index of a value
print("Index of value 3:")
print(t.index_of(3))

# Count occurrences of a value
print("Count of value 2:")
print(t.count(2))