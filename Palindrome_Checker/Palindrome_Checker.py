
def is_palindrome(s: str) -> bool:
    s = ''.join(c for c in s if c.isalnum()).lower()
    return s == s[::-1]

def palindrome_type(s: str) -> str:
    if is_palindrome(s):
        if len(s) % 2 == 0:
            return "Even-length palindrome"
        else:
            return "Odd-length palindrome"
    else:
        return "Not a palindrome"

def longest_palindromic_substring(s: str) -> str:
    s = ''.join(c for c in s if c.isalnum()).lower()
    longest = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            substr = s[i:j]
            if is_palindrome(substr) and len(substr) > len(longest):
                longest = substr
    return longest

def main():
    while True:
        print("\nPalindrome Checker Menu:")
        print("1. Check if a string is a palindrome")
        print("2. Determine palindrome type")
        print("3. Find longest palindromic substring")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            s = input("Enter a string: ")
            if is_palindrome(s):
                print(f"'{s}' is a palindrome.")
            else:
                print(f"'{s}' is not a palindrome.")
        elif choice == "2":
            s = input("Enter a string: ")
            print(palindrome_type(s))
        elif choice == "3":
            s = input("Enter a string: ")
            print(f"Longest palindromic substring: {longest_palindromic_substring(s)}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
