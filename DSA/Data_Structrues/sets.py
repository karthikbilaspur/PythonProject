class Set:
    def __init__(self):
        self.data: set[int] = set()

    def add(self, value: int):
        self.data.add(value)

    def remove(self, value: int):
        if value in self.data:
            self.data.remove(value)
        else:
            print("Value not found in set")

    def union(self, other_set: "Set") -> set[int]:
        return self.data.union(other_set.data)

    def intersection(self, other_set: "Set") -> set[int]:
        return self.data.intersection(other_set.data)

    def difference(self, other_set: "Set") -> set[int]:
        return self.data.difference(other_set.data)

    def is_subset(self, other_set: "Set") -> bool:
        return self.data.issubset(other_set.data)

    def is_superset(self, other_set: "Set") -> bool:
        return self.data.issuperset(other_set.data)

    def print_set(self):
        print(self.data)

# Create two sets
s1 = Set()
s1.add(1)
s1.add(2)
s1.add(3)
s1.add(4)

s2 = Set()
s2.add(3)
s2.add(4)
s2.add(5)
s2.add(6)

# Print the sets
print("Set 1:")
s1.print_set()
print("Set 2:")
s2.print_set()

# Perform set operations
print("Union:")
print(s1.union(s2))
print("Intersection:")
print(s1.intersection(s2))
print("Difference:")
print(s1.difference(s2))

# Check subset and superset
print("Is Set 1 a superset of Set 2?")
print(s1.is_superset(s2))
print("Is Set 2 a subset of Set 1?")
print(s2.is_subset(s1))