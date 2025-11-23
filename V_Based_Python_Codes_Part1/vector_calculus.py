import math

class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def add(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot_product(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other: "Vector") -> "Vector":
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        magnitude = self.magnitude()
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)

def main():
    # Create vectors
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)

    # Vector addition
    v_add = v1.add(v2)
    print(f"v1 + v2 = {v_add}")

    # Vector subtraction
    v_subtract = v1.subtract(v2)
    print(f"v1 - v2 = {v_subtract}")

    # Dot product
    dot_product = v1.dot_product(v2)
    print(f"v1 · v2 = {dot_product}")

    # Cross product
    cross_product = v1.cross_product(v2)
    print(f"v1 × v2 = {cross_product}")

    # Magnitude
    magnitude = v1.magnitude()
    print(f"|v1| = {magnitude}")

    # Normalization
    normalized_v1 = v1.normalize()
    print(f"v1 (normalized) = {normalized_v1}")

if __name__ == "__main__":
    main()