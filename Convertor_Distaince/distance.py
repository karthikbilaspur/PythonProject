import math

def calculate_distance(point1, point2):
    """
    Calculates the Euclidean distance between two points.

    Args:
        point1 (list): The coordinates of the first point.
        point2 (list): The coordinates of the second point.

    Returns:
        float: The distance between the two points.
    """
    if len(point1) != len(point2):
        raise ValueError("Both points must have the same number of dimensions")

    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


def calculate_multiple_distances(points):
    """
    Calculates the distances between multiple points.

    Args:
        points (list): A list of points, where each point is a list of coordinates.

    Returns:
        list: A list of distances between each pair of points.
    """
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = calculate_distance(points[i], points[j])
            distances.append((f"Point {i+1} to Point {j+1}", distance))
    return distances


def convert_units(distance, unit):
    """
    Converts the distance to a different unit.

    Args:
        distance (float): The distance to convert.
        unit (str): The unit to convert to (e.g. "km", "miles", "meters").

    Returns:
        float: The distance in the specified unit.
    """
    conversions = {
        "km": 1 / 1000,
        "miles": 1 / 1609.34,
        "meters": 1
    }
    return distance * conversions[unit]


def main():
    print("Distance Calculator")
    print("1. Calculate distance between two points")
    print("2. Calculate distances between multiple points")
    print("3. Convert units")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("1. 2D Distance")
        print("2. 3D Distance")
        dimension = input("Enter your choice: ")

        if dimension == '1':
            x1 = float(input("Enter x-coordinate of point 1: "))
            y1 = float(input("Enter y-coordinate of point 1: "))
            x2 = float(input("Enter x-coordinate of point 2: "))
            y2 = float(input("Enter y-coordinate of point 2: "))

            point1 = [x1, y1]
            point2 = [x2, y2]

            distance = calculate_distance(point1, point2)
            print(f"The distance between ({x1}, {y1}) and ({x2}, {y2}) is {distance:.2f} units")

            unit = input("Enter unit to convert to (km, miles, meters): ")
            converted_distance = convert_units(distance, unit)
            print(f"The distance in {unit} is {converted_distance:.2f}")

        elif dimension == '2':
            x1 = float(input("Enter x-coordinate of point 1: "))
            y1 = float(input("Enter y-coordinate of point 1: "))
            z1 = float(input("Enter z-coordinate of point 1: "))
            x2 = float(input("Enter x-coordinate of point 2: "))
            y2 = float(input("Enter y-coordinate of point 2: "))
            z2 = float(input("Enter z-coordinate of point 2: "))

            point1 = [x1, y1, z1]
            point2 = [x2, y2, z2]

            distance = calculate_distance(point1, point2)
            print(f"The distance between ({x1}, {y1}, {z1}) and ({x2}, {y2}, {z2}) is {distance:.2f} units")

            unit = input("Enter unit to convert to (km, miles, meters): ")
            converted_distance = convert_units(distance, unit)
            print(f"The distance in {unit} is {converted_distance:.2f}")

    elif choice == '2':
        num_points = int(input("Enter the number of points: "))
        points = []
        for i in range(num_points):
            point = []
            for j in range(3):
                coord = float(input(f"Enter coordinate {j+1} of point {i+1}: "))
                point.append(coord)
            points.append(point)

        distances = calculate_multiple_distances(points)
        for distance in distances:
            print(f"{distance[0]}: {distance[1]:.2f} units")

    elif choice == '3':
        distance = float(input("Enter the distance: "))
        unit = input("Enter unit to convert to (km, miles, meters): ")
        converted_distance = convert_units(distance, unit)
        print(f"The distance in {unit} is {converted_distance:.2f}")


if __name__ == "__main__":
    main()