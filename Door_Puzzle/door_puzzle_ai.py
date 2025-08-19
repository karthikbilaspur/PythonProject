import math
import time

class DoorPuzzle:
    def __init__(self, n):
        self.n = n
        self.doors = [False] * (n + 1)  # Initialize doors as closed (False)

    def count_open_doors(self):
        """
        Calculate the number of doors that remain open after n iterations.

        Returns:
            list: A list of door numbers that remain open.
        """
        open_doors = [i * i for i in range(1, int(math.sqrt(self.n)) + 1)]
        return open_doors

    def simulate_doors(self):
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

    def print_results(self):
        open_doors = self.count_open_doors()
        print("Doors that remain open:", open_doors)
        print("Number of open doors:", len(open_doors))

        # Simulate the doors and verify the result
        doors = self.simulate_doors()
        simulated_open_doors = [i + 1 for i, door in enumerate(doors) if door]
        print("Simulated open doors:", simulated_open_doors)
        assert open_doors == simulated_open_doors, "Results do not match"

def main():
    n = 1000  # Change this value to simulate with a different number of doors
    puzzle = DoorPuzzle(n)
    puzzle.print_results()

if __name__ == "__main__":
    main()