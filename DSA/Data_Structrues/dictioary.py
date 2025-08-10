class Dictionary:
    def __init__(self):
        self.data = {}

    def add(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def update(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            print("Key not found")

    def delete(self, key):
        if key in self.data:
            del self.data[key]
        else:
            print("Key not found")

    def print_dict(self):
        for key, value in self.data.items():
            print(f"{key}: {value}")

    def sort_by_keys(self):
        return dict(sorted(self.data.items()))

    def sort_by_values(self):
        return dict(sorted(self.data.items(), key=lambda item: item[1]))

# Create a dictionary
d = Dictionary()
d.add("apple", 5)
d.add("banana", 10)
d.add("cherry", 3)
d.add("date", 8)

# Print the dictionary
print("Dictionary:")
d.print_dict()

# Get a value
print("\nGet value of 'apple':")
print(d.get("apple"))

# Update a value
d.update("apple", 6)
print("\nUpdated dictionary:")
d.print_dict()

# Delete a key-value pair
d.delete("banana")
print("\nDictionary after deletion:")
d.print_dict()

# Sort the dictionary by keys
print("\nDictionary sorted by keys:")
print(d.sort_by_keys())

# Sort the dictionary by values
print("\nDictionary sorted by values:")
print(d.sort_by_values())