class CoffeeMachine:
    def __init__(self):
        self.water = 1000  # ml
        self.coffee = 1000  # grams
        self.milk = 500  # ml
        self.money = 0

    def display_status(self):
        print(f"Water: {self.water}ml")
        print(f"Coffee: {self.coffee}g")
        print(f"Milk: {self.milk}ml")
        print(f"Money: ${self.money}")

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
        self.water = 1000
        self.coffee = 1000
        self.milk = 500
        print("Machine refilled.")

def main():
    machine = CoffeeMachine()
    while True:
        print("\nOptions:")
        print("1. Make espresso")
        print("2. Make latte")
        print("3. Make cappuccino")
        print("4. Display status")
        print("5. Refill machine")
        print("6. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            machine.make_coffee("espresso")
        elif choice == "2":
            machine.make_coffee("latte")
        elif choice == "3":
            machine.make_coffee("cappuccino")
        elif choice == "4":
            machine.display_status()
        elif choice == "5":
            machine.refill()
        elif choice == "6":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()