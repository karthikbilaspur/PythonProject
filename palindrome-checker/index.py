def _clean(s: str) -> str:
    """Keep only alphanumerics, lowercased. Used for all comparisons."""
    return ''.join(c for c in s if c.isalnum()).lower()


def is_palindrome(s: str) -> bool:
    cleaned = _clean(s)
    # Two-pointer check: O(n) time, O(1) extra (besides cleaned string).
    # s == s[::-1] also works, but this avoids building a second copy.
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True


def palindrome_type(s: str) -> str:
    cleaned = _clean(s)

    if not cleaned:
        return "Empty string (no alphanumeric characters)"

    if not is_palindrome(s):
        return "Not a palindrome"

    # FIX: use len(cleaned), NOT len(s).
    # Example: "A man, a plan, a canal: Panama"
    #   len(s) = 30 (even) -> old code said "Even-length"
    #   len(cleaned) = 21 (odd) -> correct answer is "Odd-length"
    if len(cleaned) % 2 == 0:
        return "Even-length palindrome"
    else:
        return "Odd-length palindrome"


def longest_palindromic_substring(s: str) -> str:
    """
    Return the longest palindromic substring, as it appears in the
    ORIGINAL string (original casing / spaces / punctuation preserved).

    Example:
        s = "Madam, I'm Adam, hello"
        cleaned = "madamimadamhello"
        longest cleaned palindrome = "madamimadam" (indices 0..10)
        returned = "Madam, I'm Adam"  (original slice covering those chars)

    Algorithm: expand-around-center, O(n^2) time, O(n) space.
    For every position, expand outward for odd-length (center = i)
    and even-length (center between i and i+1) palindromes.
    """
    if not s:
        return ""

    # Build cleaned string + map: cleaned_index -> original_index
    cleaned_chars: list[str] = []
    orig_indices: list[int] = []  # orig_indices[k] = index in s of cleaned_chars[k]
    for idx, ch in enumerate(s):
        if ch.isalnum():
            cleaned_chars.append(ch.lower())
            orig_indices.append(idx)

    cleaned = ''.join(cleaned_chars)
    n = len(cleaned)
    if n == 0:
        return ""
    if n == 1:
        return s[orig_indices[0]:orig_indices[0] + 1]

    # best = (start, end) in CLEANED coordinates, end exclusive
    best_start, best_end = 0, 1

    def expand(left: int, right: int):
        """Expand while cleaned[left:right+1] is a palindrome. Return (l, r) exclusive."""
        while left >= 0 and right < n and cleaned[left] == cleaned[right]:
            left -= 1
            right += 1
        # left/right went one step too far
        return left + 1, right

    for center in range(n):
        # Odd-length: center is a single character, e.g. "racecar"
        start, end = expand(center, center)
        if end - start > best_end - best_start:
            best_start, best_end = start, end

        # Even-length: center is between center and center+1, e.g. "abba"
        start, end = expand(center, center + 1)
        if end - start > best_end - best_start:
            best_start, best_end = start, end

    # Map back to ORIGINAL string slice (includes any punctuation/spaces
    # between the first and last alphanumeric chars of the palindrome).
    orig_start = orig_indices[best_start]
    orig_end = orig_indices[best_end - 1] + 1  # +1 to make it exclusive
    return s[orig_start:orig_end]


def main():
    while True:
        print("\nPalindrome Checker Menu:")
        print("1. Check if a string is a palindrome")
        print("2. Determine palindrome type")
        print("3. Find longest palindromic substring")
        print("4. Quit")
        try:
            choice = input("Enter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if choice == "1":
            try:
                s = input("Enter a string: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            if is_palindrome(s):
                print(f"'{s}' is a palindrome.")
            else:
                print(f"'{s}' is not a palindrome.")
        elif choice == "2":
            try:
                s = input("Enter a string: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            print(palindrome_type(s))
        elif choice == "3":
            try:
                s = input("Enter a string: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            result = longest_palindromic_substring(s)
            if result:
                print(f"Longest palindromic substring: '{result}'")
            else:
                print("No palindromic substring found (no alphanumeric characters).")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()