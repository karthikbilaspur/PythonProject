class TeaMachine:
    def __init__(self):
        self.tea_leaves = 1000  # grams
        self.milk = 500  # ml
        self.water = 1000  # ml
        self.sugar = 500  # grams
        self.money = 0

    def display_status(self):
        print(f"Tea Leaves: {self.tea_leaves}g")
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

    def refill(self):
        self.tea_leaves = 1000
        self.milk = 500
        self.water = 1000
        self.sugar = 500
        print("Machine refilled.")

def main():
    machine = TeaMachine()
    while True:
        print("\nOptions:")
        print("1. Make plain tea")
        print("2. Make masala tea")
        print("3. Make ginger tea")
        print("4. Make milk tea")
        print("5. Display status")
        print("6. Refill machine")
        print("7. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            machine.make_tea("plain")
        elif choice == "2":
            machine.make_tea("masala")
        elif choice == "3":
            machine.make_tea("ginger")
        elif choice == "4":
            machine.make_tea("milk_tea")
        elif choice == "5":
            machine.display_status()
        elif choice == "6":
            machine.refill()
        elif choice == "7":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()