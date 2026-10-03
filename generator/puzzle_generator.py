import random

# Define puzzle types
puzzle_types = ["Array", "String", "Math"]

# Define puzzle difficulties
difficulties = ["Easy", "Medium", "Hard"]

# Define puzzle templates
puzzle_templates = {
    "Array": {
        "Easy": [
            {"problem": "Find the sum of all elements in an array.", "function": "sum_array", "params": ["arr"]},
            {"problem": "Find the maximum element in an array.", "function": "max_array", "params": ["arr"]},
            {"problem": "Find the minimum element in an array.", "function": "min_array", "params": ["arr"]},
        ],
        "Medium": [
            {"problem": "Find the second largest element in an array.", "function": "second_largest", "params": ["arr"]},
            {"problem": "Reverse an array.", "function": "reverse_array", "params": ["arr"]},
            {"problem": "Find the average of all elements in an array.", "function": "average_array", "params": ["arr"]},
        ],
        "Hard": [
            {"problem": "Find the longest increasing subsequence in an array.", "function": "longest_increasing_subsequence", "params": ["arr"]},
            {"problem": "Find the maximum subarray sum.", "function": "max_subarray_sum", "params": ["arr"]},
            {"problem": "Find the minimum window that contains all elements of another array.", "function": "min_window", "params": ["arr1", "arr2"]},
        ],
    },
    "String": {
        "Easy": [
            {"problem": "Reverse a string.", "function": "reverse_string", "params": ["s"]},
            {"problem": "Check if a string is palindrome.", "function": "is_palindrome", "params": ["s"]},
            {"problem": "Count the number of vowels in a string.", "function": "count_vowels", "params": ["s"]},
        ],
        "Medium": [
            {"problem": "Find the first non-repeating character in a string.", "function": "first_non_repeating", "params": ["s"]},
            {"problem": "Check if two strings are anagrams.", "function": "are_anagrams", "params": ["s1", "s2"]},
            {"problem": "Find the longest common prefix between two strings.", "function": "longest_common_prefix", "params": ["s1", "s2"]},
        ],
        "Hard": [
            {"problem": "Find the longest common substring between two strings.", "function": "longest_common_substring", "params": ["s1", "s2"]},
            {"problem": "Find the minimum window substring that contains all characters of another string.", "function": "min_window_substring", "params": ["s1", "s2"]},
            {"problem": "Implement a regular expression matcher.", "function": "regex_matcher", "params": ["s", "pattern"]},
        ],
    },
    "Math": {
        "Easy": [
            {"problem": "Check if a number is prime.", "function": "is_prime", "params": ["n"]},
            {"problem": "Find the factorial of a number.", "function": "factorial", "params": ["n"]},
            {"problem": "Find the greatest common divisor of two numbers.", "function": "gcd", "params": ["a", "b"]},
        ],
        "Medium": [
            {"problem": "Check if a number is a perfect square.", "function": "is_perfect_square", "params": ["n"]},
            {"problem": "Find the nth Fibonacci number.", "function": "fibonacci", "params": ["n"]},
            {"problem": "Check if a number is a power of two.", "function": "is_power_of_two", "params": ["n"]},
        ],
        "Hard": [
            {"problem": "Find the modular inverse of a number.", "function": "modular_inverse", "params": ["a", "m"]},
            {"problem": "Implement the Sieve of Eratosthenes algorithm.", "function": "sieve_of_eratosthenes", "params": ["n"]},
            {"problem": "Find the discrete logarithm of a number.", "function": "discrete_logarithm", "params": ["a", "b", "m"]},
        ],
    },
}

def generate_puzzle():
    puzzle_type = random.choice(puzzle_types)
    difficulty = random.choice(difficulties)
    puzzle = random.choice(puzzle_templates[puzzle_type][difficulty])
    return {
        "type": puzzle_type,
        "difficulty": difficulty,
        "problem": puzzle["problem"],
        "function": puzzle["function"],
        "params": puzzle["params"],
    }

def main():
    puzzle = generate_puzzle()
    print("Type:", puzzle["type"])
    print("Difficulty:", puzzle["difficulty"])
    print("Problem:", puzzle["problem"])
    print("Function:", puzzle["function"])
    print("Params:", puzzle["params"])

if __name__ == "__main__":
    main()