def multiply(F, M):
    """Multiplies two 2x2 matrices F and M."""
    x = F[0][0] * M[0][0] + F[0]¹ * M¹[0]
    y = F[0][0] * M[0]¹ + F[0]¹ * M¹ ¹
    z = F¹[0] * M[0][0] + F¹ ¹ * M¹[0]
    w = F¹[0] * M[0]¹ + F¹ ¹ * M¹ ¹

    F[0][0] = x
    F[0]¹ = y
    F¹[0] = z
    F¹ ¹ = w


def power(F, n):
    """Calculates the power of a matrix F raised to n using binary exponentiation."""
    if n == 0 or n == 1:
        return
    M = [[1, 1], [1, 0]]

    power(F, n // 2)
    multiply(F, F)

    if n % 2 != 0:
        multiply(F, M)


def fib(n):
    """Calculates the nth Fibonacci number using matrix exponentiation."""
    F = [[1, 1], [1, 0]]
    if n == 0:
        return 0
    power(F, n - 1)
    return F[0][0]


def fibonacci_generator(n):
    """Generates the first n Fibonacci numbers."""
    for i in range(n):
        print(fib(i), end=" ")


def fibonacci_sequence(n):
    """Returns a list of the first n Fibonacci numbers."""
    return [fib(i) for i in range(n)]


# Example usage
n = 10
print("Fibonacci sequence up to", n, "terms:")
fibonacci_generator(n)
print("\nFibonacci sequence as a list:")
print(fibonacci_sequence(n))