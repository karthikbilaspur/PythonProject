import math
import time
import argparse
from typing import List

class DoorPuzzle:
    """
    Classic 100 Doors problem:
    - n doors, all closed.
    - Pass i (1..n): toggle every i-th door.
    - Which doors stay open?
    Answer: Perfect squares. Door k is toggled once per divisor of k,
    and only perfect squares have an odd number of divisors.
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("n must be a positive integer")
        self.n = n
        self.doors: List[bool] = [False] * (n + 1)  # 1-indexed, doors[0] unused
        self._simulated = False

    # ---------- Fast math solution: O(sqrt(n)) ----------
    def count_open_doors(self) -> List[int]:
        """Return open doors using math. O(sqrt(n))."""
        return [i * i for i in range(1, int(math.isqrt(self.n)) + 1)]

    # ---------- Brute-force simulation: O(n log n) ----------
    def simulate_doors(self, step: bool = False, delay: float = 0.3) -> List[bool]:
        """Simulate all passes. Returns doors[1:]."""
        self.doors = [False] * (self.n + 1)
        start = time.perf_counter()

        for i in range(1, self.n + 1):
            for j in range(i, self.n + 1, i):
                self.doors[j] = not self.doors[j]

            if step:
                print(f"\nPass {i:>3}: toggled every {i}th door")
                self.print_grid()
                time.sleep(delay)

        elapsed = time.perf_counter() - start
        print(f"\nSimulation took {elapsed:.6f}s for n={self.n}")
        self._simulated = True
        return self.doors[1:]

    def get_open_doors(self) -> List[int]:
        """Open doors from current simulated state."""
        if not self._simulated:
            self.simulate_doors()
        return [i for i in range(1, self.n + 1) if self.doors[i]]

    # ---------- Verification ----------
    def verify(self) -> bool:
        """Check math solution == simulation."""
        math_result = self.count_open_doors()
        sim_result = self.get_open_doors()
        ok = math_result == sim_result
        print(f"Math: {math_result}")
        print(f"Sim : {sim_result}")
        print("✅ Match!" if ok else "❌ MISMATCH!")
        return ok

    # ---------- Visualization ----------
    def print_grid(self, cols: int = 10):
        """Pretty grid: 🟩 = open, ⬛ = closed."""
        for i in range(1, self.n + 1):
            symbol = "🟩" if self.doors[i] else "⬛"
            print(f"{symbol} {i:>3}  ", end="")
            if i % cols == 0:
                print()
        print()

    def visualize_doors(self):
        if not self._simulated:
            self.simulate_doors()
        print(f"\nFinal state (n={self.n}):")
        self.print_grid()
        for i in range(1, self.n + 1):
            print(f"Door {i:>3}: {'Open  🟩' if self.doors[i] else 'Closed ⬛'}")

    def print_results(self):
        open_doors = self.count_open_doors()
        print(f"Doors that remain open (calculated): {open_doors}")
        print(f"Number of open doors: {len(open_doors)}  (= floor(sqrt({self.n})) = {math.isqrt(self.n)})")
        print("\nWhy? Door k is toggled once per divisor. "
              "Only perfect squares have an odd # of divisors.")
        print("Verifying with simulation...")
        self.verify()

    def benchmark(self):
        """Compare math vs simulation speed."""
        t0 = time.perf_counter()
        math_res = self.count_open_doors()
        t_math = time.perf_counter() - t0

        t0 = time.perf_counter()
        self.simulate_doors()
        t_sim = time.perf_counter() - t0

        print(f"\nBenchmark (n={self.n}):")
        print(f"  Math:       {t_math:.6f}s  -> {len(math_res)} doors")
        print(f"  Simulation: {t_sim:.6f}s")
        if t_math > 0:
            print(f"  Math is {t_sim / t_math:,.0f}x faster")

def main():
    parser = argparse.ArgumentParser(description="100 Doors Puzzle")
    parser.add_argument("n", type=int, nargs="?", help="Number of doors")
    parser.add_argument("--step", action="store_true", help="Show each pass step-by-step")
    parser.add_argument("--visual", action="store_true", help="Show final grid + door list")
    parser.add_argument("--benchmark", action="store_true", help="Compare math vs simulation speed")
    args = parser.parse_args()

    n = args.n
    if n is None:
        try:
            n = int(input("Enter the number of doors: "))
        except ValueError:
            print("Please enter a positive integer.")
            return

    puzzle = DoorPuzzle(n)
    print(f"\n=== {n} Doors Puzzle ===\n")
    puzzle.print_results()

    if args.benchmark:
        puzzle.benchmark()

    if args.visual:
        puzzle.visualize_doors()
    elif args.step:
        # Re-run with animation if user asked for step mode
        puzzle.simulate_doors(step=True)
        print("\nFinal open doors:", puzzle.get_open_doors())

if __name__ == "__main__":
    main()