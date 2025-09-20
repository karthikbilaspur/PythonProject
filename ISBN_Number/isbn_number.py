import re
import requests

def validate_isbn(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) == 10:
        try:
            int(isbn[:-1])
        except ValueError:
            return False
        check_digit = isbn[-1]
        if check_digit.upper() == "X":
            check_digit = 10
        else:
            try:
                check_digit = int(check_digit)
            except ValueError:
                return False
        sum = 0
        for i in range(10):
            sum += (10 - i) * int(isbn[i])
        return sum % 11 == check_digit
    elif len(isbn) == 13:
        try:
            int(isbn)
        except ValueError:
            return False
        sum = 0
        for i in range(12):
            digit = int(isbn[i])
            if i % 2 == 0:
                sum += digit
            else:
                sum += digit * 3
        check_digit = 10 - (sum % 10)
        if check_digit == 10:
            check_digit = 0
        return check_digit == int(isbn[-1])
    else:
        return False

def find_isbn(title=None, author=None):
    api_url = "https://www.googleapis.com/books/v1/volumes"
    params = {}
    if title:
        params["q"] = f"intitle:{title}"
    if author:
        if "q" in params:
            params["q"] += f" inauthor:{author}"
        else:
            params["q"] = f"inauthor:{author}"
    response = requests.get(api_url, params=params)
    data = response.json()
    if "items" in data:
        isbn_numbers = []
        for book in data["items"]:
            if "industryIdentifiers" in book["volumeInfo"]:
                for identifier in book["volumeInfo"]["industryIdentifiers"]:
                    if identifier["type"] == "ISBN_10" or identifier["type"] == "ISBN_13":
                        isbn_numbers.append(identifier["identifier"])
        return isbn_numbers
    else:
        return []

def main():
    while True:
        print("1. Validate ISBN number")
        print("2. Find ISBN number")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            isbn = input("Enter the ISBN number: ")
            if validate_isbn(isbn):
                print("The ISBN number is valid.")
            else:
                print("The ISBN number is not valid.")
        elif choice == "2":
            title = input("Enter the book title (optional): ")
            author = input("Enter the author (optional): ")
            isbn_numbers = find_isbn(title or None, author or None)
            if isbn_numbers:
                print("ISBN numbers found:")
                for isbn in isbn_numbers:
                    print(isbn)
            else:
                print("No ISBN numbers found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()