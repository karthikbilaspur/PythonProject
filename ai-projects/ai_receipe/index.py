import sqlite3
import random
import tweepy
import nltk
from nltk.tokenize import word_tokenize
import requests
from getpass import getpass
import bcrypt

# Connect to SQLite database
conn = sqlite3.connect("recipes.db")
c = conn.cursor()

# Create table for recipes
c.execute("""CREATE TABLE IF NOT EXISTS recipes (
            name text,
            ingredients text,
            instructions text,
            rating real
            )""")

# Create table for users
c.execute("""CREATE TABLE IF NOT EXISTS users (
            username text,
            password text
            )""")

# Create table for bookmarks
c.execute("""CREATE TABLE IF NOT EXISTS bookmarks (
            username text,
            recipe text
            )""")

class RecipeApp:
    def __init__(self):
        self.logged_in_user = None

    def add_recipe_to_database(self, recipe):
        c.execute("INSERT INTO recipes VALUES (?, ?, ?, ?)",
                  (recipe["name"], ", ".join(recipe["ingredients"]), "\n".join(recipe["instructions"]), 0))
        conn.commit()

    def view_recipes_in_database(self):
        c.execute("SELECT * FROM recipes")
        recipes = c.fetchall()
        for recipe in recipes:
            print(f"Name: {recipe[0]}")
            print(f"Ingredients: {recipe[1]}")
            print(f"Instructions: {recipe[2]}")
            print(f"Rating: {recipe[3]}")
            print()

    def suggest_recipes(self, ingredients):
        c.execute("SELECT * FROM recipes")
        recipes = c.fetchall()
        suggested_recipes = []
        for recipe in recipes:
            recipe_ingredients = recipe[1].split(", ")
            if all(ingredient in ingredients for ingredient in recipe_ingredients):
                suggested_recipes.append(recipe[0])
        return suggested_recipes

    def generate_grocery_list(self, recipe):
        c.execute("SELECT ingredients FROM recipes WHERE name = ?", (recipe,))
        ingredients = c.fetchone()[0].split(", ")
        return ingredients

    def rate_recipe(self, recipe, rating):
        c.execute("UPDATE recipes SET rating = ? WHERE name = ?", (rating, recipe))
        conn.commit()

    def share_recipe_on_twitter(self, recipe):
        consumer_key = "your_consumer_key_here"
        consumer_secret = "your_consumer_secret_here"
        access_token = "your_access_token_here"
        access_token_secret = "your_access_token_secret_here"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        c.execute("SELECT * FROM recipes WHERE name = ?", (recipe,))
        recipe_details = c.fetchone()
        tweet = f"Check out this recipe for {recipe_details[0]}! Ingredients: {recipe_details[1]}. Instructions: {recipe_details[2]}"
        api.update_status(tweet)

    def tokenize_recipe(self, recipe):
        tokens = word_tokenize(recipe)
        return tokens

    def register_user(self):
        username = input("Enter a username: ")
        password = getpass("Enter a password: ")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully!")

    def login_user(self):
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()
        if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
            self.logged_in_user = username
            print("Logged in successfully!")
        else:
            print("Invalid username or password.")

    def bookmark_recipe(self, recipe):
        c.execute("INSERT INTO bookmarks VALUES (?, ?)", (self.logged_in_user, recipe))
        conn.commit()
        print("Recipe bookmarked successfully!")

    def view_bookmarks(self):
        c.execute("SELECT recipe FROM bookmarks WHERE username = ?", (self.logged_in_user,))
        bookmarks = c.fetchall()
        for bookmark in bookmarks:
            print(bookmark[0])

def main():
    app = RecipeApp()

    while True:
        if app.logged_in_user is None:
            print("1. Register")
            print("2. Login")
            print("3. Quit")
            choice = input("Enter your choice: ")
            if choice == "1":
                app.register_user()
            elif choice == "2":
                app.login_user()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("1. View recipes")
            print("2. Add recipe")
            print("3. Suggest recipes")
            print("4. Generate grocery list")
            print("5. Rate recipe")
            print("6. Share recipe on Twitter")
            print("7. Tokenize recipe")
            print("8. Bookmark recipe")
            print("9. View bookmarks")
            print("10. Logout")
            print("11. Quit")
            choice = input("Enter your choice: ")
            if choice == "1":
                app.view_recipes_in_database()
            elif choice == "2":
                recipe_name = input("Enter recipe name: ")
                ingredients = input("Enter ingredients (comma-separated): ").split(",")
                ingredients = [ingredient.strip() for ingredient in ingredients]
                instructions = input("Enter instructions (comma-separated): ").split(",")
                instructions = [instruction.strip() for instruction in instructions]
                recipe = {"name": recipe_name, "ingredients": ingredients, "instructions": instructions}
                app.add_recipe_to_database(recipe)
            elif choice == "3":
                ingredients = input("Enter ingredients (comma-separated): ").split(",")
                ingredients = [ingredient.strip() for ingredient in ingredients]
                suggested_recipes = app.suggest_recipes(ingredients)
                print("Suggested recipes:")
                for recipe in suggested_recipes:
                    print(recipe)
            elif choice == "4":
                recipe = input("Enter recipe name: ")
                grocery_list = app.generate_grocery_list(recipe)
                print("Grocery list:")
                for ingredient in grocery_list:
                    print(ingredient)
            elif choice == "5":
                recipe = input("Enter recipe name: ")
                rating = float(input("Enter rating (1-5): "))
                app.rate_recipe(recipe, rating)
            elif choice == "6":
                recipe = input("Enter recipe name: ")
                app.share_recipe_on_twitter(recipe)
            elif choice == "7":
                recipe = input("Enter recipe: ")
                tokens = app.tokenize_recipe(recipe)
                print("Tokens:")
                for token in tokens:
                    print(token)
            elif choice == "8":
                recipe = input("Enter recipe name: ")
                app.bookmark_recipe(recipe)
            elif choice == "9":
                app.view_bookmarks()
            elif choice == "10":
                app.logged_in_user = None
            elif choice == "11":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()