class BeverageMachine:
    def __init__(self):
        self.tea_leaves = 1000  # grams
        self.coffee = 1000  # grams
        self.milk = 1000  # ml
        self.water = 2000  # ml
        self.sugar = 500  # grams
        self.money = 0

    def display_status(self):
        print(f"Tea Leaves: {self.tea_leaves}g")
        print(f"Coffee: {self.coffee}g")
        print(f"Milk: {self.milk}ml")
        print(f"Water: {self.water}ml")
        print(f"Sugar: {self.sugar}g")
        print(f"Money: ${self.money}")

    def make_tea(self, tea_type):
        tea_recipes = {
            "plain": {"water": 200, "tea_leaves": 5, "milk": 0, "sugar": 0},
            "masala": {"water": 200, "tea_leaves": 5, "milk": 50, "sugar": 10},
            "ginger": {"water": 200, "tea_leaves": 5, "milk": 0, "sugar": 10},
            "milk_tea": {"water": 200, "tea_leaves": 5, "milk": 100, "sugar": 10},
        }

        recipe = tea_recipes.get(tea_type)
        if not recipe:
            print("Invalid tea type.")
            return

        if self.water < recipe["water"]:
            print("Not enough water.")
            return
        if self.tea_leaves < recipe["tea_leaves"]:
            print("Not enough tea leaves.")
            return
        if self.milk < recipe["milk"]:
            print("Not enough milk.")
            return
        if self.sugar < recipe["sugar"]:
            print("Not enough sugar.")
            return

        self.water -= recipe["water"]
        self.tea_leaves -= recipe["tea_leaves"]
        self.milk -= recipe["milk"]
        self.sugar -= recipe["sugar"]
        self.money += 1  # assume each tea costs $1

        print(f"Here's your {tea_type} tea!")

    def make_coffee(self, coffee_type):
        coffee_recipes = {
            "espresso": {"water": 50, "coffee": 18, "milk": 0},
            "latte": {"water": 200, "coffee": 24, "milk": 150},
            "cappuccino": {"water": 250, "coffee": 24, "milk": 100},
        }

        recipe = coffee_recipes.get(coffee_type)
        if not recipe:
            print("Invalid coffee type.")
            return

        if self.water < recipe["water"]:
            print("Not enough water.")
            return
        if self.coffee < recipe["coffee"]:
            print("Not enough coffee.")
            return
        if self.milk < recipe["milk"]:
            print("Not enough milk.")
            return

        self.water -= recipe["water"]
        self.coffee -= recipe["coffee"]
        self.milk -= recipe["milk"]
        self.money += 1  # assume each coffee costs $1

        print(f"Here's your {coffee_type}!")

    def refill(self):
        self.tea_leaves = 1000
        self.coffee = 1000
        self.milk = 1000
        self.water = 2000
        self.sugar = 500
        print("Machine refilled.")

def main():
    machine = BeverageMachine()
    while True:
        print("\nOptions:")
        print("1. Make tea")
        print("2. Make coffee")
        print("3. Display status")
        print("4. Refill machine")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            print("\nTea options:")
            print("1. Plain tea")
            print("2. Masala tea")
            print("3. Ginger tea")
            print("4. Milk tea")
            tea_choice = input("Choose a tea option: ")
            if tea_choice == "1":
                machine.make_tea("plain")
            elif tea_choice == "2":
                machine.make_tea("masala")
            elif tea_choice == "3":
                machine.make_tea("ginger")
            elif tea_choice == "4":
                machine.make_tea("milk_tea")
            else:
                print("Invalid option.")
        elif choice == "2":
            print("\nCoffee options:")
            print("1. Espresso")
            print("2. Latte")
            print("3. Cappuccino")
            coffee_choice = input("Choose a coffee option: ")
            if coffee_choice == "1":
                machine.make_coffee("espresso")
            elif coffee_choice == "2":
                machine.make_coffee("latte")
            elif coffee_choice == "3":
                machine.make_coffee("cappuccino")
            else:
                print("Invalid option.")
        elif choice == "3":
            machine.display_status()
        elif choice == "4":
            machine.refill()
        elif choice == "5":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()