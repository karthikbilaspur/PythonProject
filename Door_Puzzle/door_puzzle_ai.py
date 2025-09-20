import math
import time
from typing import List

class DoorPuzzle:
    def __init__(self, n: int):
        """
        Initialize the DoorPuzzle class.

        Args:
            n (int): The number of doors.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")
        self.n = n
        self.doors = [False] * (n + 1)  # Initialize doors as closed (False)

    def count_open_doors(self) -> List[int]:
        """
        Calculate the number of doors that remain open after n iterations.

        Returns:
            list: A list of door numbers that remain open.
        """
        open_doors = [i * i for i in range(1, int(math.sqrt(self.n)) + 1) if i * i <= self.n]
        return open_doors

    def simulate_doors(self) -> List[bool]:
        """
        Simulate the 100 Doors puzzle and return the final state of the doors.

        Returns:
            list: A list of boolean values representing the final state of the doors.
        """
        start_time = time.time()
        for i in range(1, self.n + 1):
            for j in range(i, self.n + 1, i):
                self.doors[j] = not self.doors[j]  # Toggle door state
        end_time = time.time()
        print(f"Simulation took {end_time - start_time:.6f} seconds")
        return self.doors[1:]  # Return doors 1 to n

    def print_results(self) -> None:
        """
        Print the results of the DoorPuzzle simulation.
        """
        open_doors = self.count_open_doors()
        print("Doors that remain open (calculated):", open_doors)
        print("Number of open doors:", len(open_doors))

        # Simulate the doors and verify the result
        doors = self.simulate_doors()
        simulated_open_doors = [i + 1 for i, door in enumerate(doors) if door]
        print("Doors that remain open (simulated):", simulated_open_doors)
        if open_doors != simulated_open_doors:
            print("Warning: Calculated and simulated results do not match")

    def visualize_doors(self) -> None:
        """
        Visualize the final state of the doors.
        """
        doors = self.simulate_doors()
        for i, door in enumerate(doors):
            print(f"Door {i + 1}: {'Open' if door else 'Closed'}")

def main() -> None:
    n = int(input("Enter the number of doors: "))
    puzzle = DoorPuzzle(n)
    print("\nResults:")
    puzzle.print_results()
    print("\nDoor States:")
    puzzle.visualize_doors()

if __name__ == "__main__":
    main()