import time
import random

# ---------- helpers ----------
def print_delay(text: str, delay: float = 0.6):
    print(text)
    if delay > 0:
        time.sleep(delay)

def ask_choice(prompt: str, valid: list[str]) -> str:
    choice = ""
    while choice not in valid:
        choice = input(prompt).strip().lower()
    return choice

def ask_yes_no(prompt: str) -> bool:
    return ask_choice(prompt, ["yes", "no"]) == "yes"

# ---------- player state ----------
class Player:
    def __init__(self):
        self.score = 0
        self.health = 100
        self.inventory: list[str] = []
        self.name = "Adventurer"

    def add_score(self, pts: int):
        self.score += pts
        print_delay(f"[Score: {self.score} | Health: {self.health} | Items: {', '.join(self.inventory) if self.inventory else 'none'}]")

    def take_damage(self, dmg: int):
        self.health = max(0, self.health - dmg)
        print_delay(f"You lose {dmg} health! Health now: {self.health}")
        return self.health > 0

# ---------- LEVEL 1 : your original game ----------
def intro(p: Player):
    print_delay("=" * 55)
    print_delay("LEVEL 1 - THE TWO DOORS")
    print_delay("=" * 55)
    print_delay("You wake up in a dark, mysterious room.")
    print_delay("You can't remember how you got here.")
    print_delay("As you look around, you see two doors in front of you.")
    print_delay("One door is red, and the other door is blue.")

def red_door_scenario(p: Player):
    print_delay("You open the red door and find yourself in a fiery cave.")
    print_delay("There's a dragon sleeping in the middle of the cave!")
    print_delay("You can either:")
    print_delay("1. Try to sneak around the dragon.")
    print_delay("2. Grab a nearby sword and fight the dragon.")
    choice = ask_choice("Enter 1 or 2: ", ["1", "2"])
    if choice == "1":
        print_delay("You try to sneak around the dragon.")
        if random.random() < 0.5:
            print_delay("You successfully sneak past the dragon!")
            print_delay("You find a treasure chest filled with gold and gems!")
            p.inventory.append("Gold Coins")
            p.add_score(100)
        else:
            print_delay("Unfortunately, the dragon wakes up and chases you!")
            print_delay("You barely manage to escape through the red door.")
            p.take_damage(20)
            p.add_score(0)
    else:
        print_delay("You pick up the sword and bravely attack the dragon.")
        if random.random() < 0.7:
            print_delay("After an intense battle, you defeat the dragon!")
            print_delay("You find a treasure chest behind the dragon's nest.")
            p.inventory.append("Dragon Sword")
            p.inventory.append("Dragon Gems")
            p.add_score(150)
        else:
            print_delay("The dragon is too powerful, and you are defeated.")
            if not p.take_damage(40):
                return False
            p.add_score(-50)
    return True

def blue_door_scenario(p: Player):
    print_delay("You open the blue door and find yourself in a peaceful garden.")
    print_delay("There's a friendly fairy sitting on a bench.")
    print_delay("The fairy offers you a magical potion.")
    print_delay("You can either:")
    print_delay("1. Drink the potion.")
    print_delay("2. Politely decline the offer.")
    choice = ask_choice("Enter 1 or 2: ", ["1", "2"])
    if choice == "1":
        print_delay("You drink the potion and feel a sudden burst of energy.")
        print_delay("Your memory is restored, and you remember everything!")
        print_delay("The fairy thanks you for accepting her gift.")
        p.inventory.append("Fairy Potion")
        p.health = min(100, p.health + 30)
        print_delay(f"The potion heals you! Health: {p.health}")
        p.add_score(100)
    else:
        print_delay("You politely decline the potion.")
        print_delay("The fairy understands and smiles at you.")
        print_delay("You feel a sense of peace in the garden.")
        p.inventory.append("Fairy Blessing")
        p.add_score(50)
    return True

def secret_room_scenario(p: Player):
    print_delay("You find a hidden passage behind the bookshelf.")
    print_delay("You enter a mysterious room filled with ancient artifacts.")
    print_delay("In the center of the room, there's a glowing amulet.")
    print_delay("You can either:")
    print_delay("1. Take the amulet.")
    print_delay("2. Leave the room without taking anything.")
    choice = ask_choice("Enter 1 or 2: ", ["1", "2"])
    if choice == "1":
        print_delay("You take the amulet, and it starts to shine even brighter.")
        print_delay("Suddenly, you feel a surge of power flowing through you.")
        p.inventory.append("Glowing Amulet")
        p.add_score(200)
    else:
        print_delay("You decide not to touch anything and leave the room.")
        print_delay("As you exit the secret room, you feel a sense of relief.")
        p.add_score(50)
    return True

def level_1(p: Player):
    intro(p)
    door = ask_choice("Which door do you choose? (red/blue): ", ["red", "blue"])
    alive = red_door_scenario(p) if door == "red" else blue_door_scenario(p)
    if not alive:
        return False
    print_delay("You continue exploring and find a hidden door behind a bookshelf.")
    if ask_yes_no("Do you want to open the door? Enter 'yes' or 'no': "):
        secret_room_scenario(p)
    print_delay(f"Level 1 complete! Score: {p.score}")
    return True

# ---------- LEVEL 2 : NEW - The Crystal Bridge & The Riddle Keeper ----------
def level_2(p: Player):
    print_delay("")
    print_delay("=" * 55)
    print_delay("LEVEL 2 - THE CRYSTAL BRIDGE")
    print_delay("=" * 55)
    print_delay("You walk through a tunnel and reach a deep chasm.")
    print_delay("A narrow crystal bridge crosses it. Below you - darkness.")
    print_delay("In the middle of the bridge stands the Riddle Keeper.")
    print_delay("'Answer my riddle, or the bridge will vanish beneath you!'")

    riddles = [
        ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "echo"),
        ("The more of me you take, the more you leave behind. What am I?", "footsteps"),
        ("What has keys but can't open a single lock?", "piano"),
    ]
    question, answer = random.choice(riddles)
    print_delay(f"Riddle: {question}")
    print_delay("Hint: one word, lowercase.")
    tries = 2
    while tries > 0:
        guess = input(f"Your answer ({tries} tries left): ").strip().lower()
        if guess == answer:
            print_delay("The Riddle Keeper smiles. 'Correct! The bridge holds!'")
            p.inventory.append("Crystal Key")
            p.add_score(150)
            break
        tries -= 1
        if tries > 0:
            print_delay("Wrong! The bridge shakes...")
        else:
            print_delay("Wrong! A crystal shard breaks off under your feet!")
            if not p.take_damage(30):
                return False
            print_delay("You jump back just in time, but the Keeper lets you pass out of pity.")
            p.add_score(20)

    print_delay("On the other side you find 3 chests. Only one is safe.")
    print_delay("1. Golden chest  2. Silver chest  3. Wooden chest")
    chest = ask_choice("Pick a chest (1/2/3): ", ["1", "2", "3"])
    safe = random.choice(["1", "2", "3"])
    if chest == safe:
        print_delay("You open it - inside is a Healing Crystal and 100 gold!")
        p.inventory.append("Healing Crystal")
        p.health = min(100, p.health + 40)
        p.add_score(100)
    else:
        print_delay("Trap! Poison gas! You cough and lose health.")
        if not p.take_damage(25):
            return False
        p.add_score(10)

    if "Healing Crystal" in p.inventory or ask_yes_no("Drink a healing potion from your bag? (yes/no): "):
        p.health = min(100, p.health + 20)
        print_delay(f"You feel better. Health: {p.health}")
    print_delay(f"Level 2 complete! Score: {p.score} | Health: {p.health}")
    return True

# ---------- LEVEL 3 : NEW - The Final Guardian ----------
def level_3(p: Player):
    print_delay("")
    print_delay("=" * 55)
    print_delay("LEVEL 3 - THE FINAL GUARDIAN")
    print_delay("=" * 55)
    print_delay("A giant stone door blocks the exit. In front of it sleeps the Guardian.")
    print_delay("To wake it, you need the Crystal Key from Level 2 - or pure courage.")
    has_key = "Crystal Key" in p.inventory
    has_amulet = "Glowing Amulet" in p.inventory
    has_sword = "Dragon Sword" in p.inventory

    if has_key:
        print_delay("You use the Crystal Key. The Guardian opens one eye and nods.")
        print_delay("'You earned the right to fight me fairly.'")
    else:
        print_delay("You have no key. You must bang on the door to wake the Guardian!")
        print_delay("It roars in anger!")

    print_delay("The Guardian has 60 HP. You must bring it to 0.")
    print_delay("Choose your attack each round:")
    guardian_hp = 60
    round_no = 1
    while guardian_hp > 0 and p.health > 0:
        print_delay(f"--- Round {round_no} | Guardian HP: {guardian_hp} | Your Health: {p.health} ---")
        print_delay("1. Attack  2. Defend (take less damage)  3. Use item")
        move = ask_choice("Enter 1, 2 or 3: ", ["1", "2", "3"])
        defending = False
        if move == "1":
            base = 20
            if has_sword:
                base += 10
                print_delay("Your Dragon Sword glows!")
            if has_amulet:
                base += 10
                print_delay("Your Glowing Amulet boosts your attack!")
            dmg = base + random.randint(0, 10)
            guardian_hp -= dmg
            print_delay(f"You hit the Guardian for {dmg} damage!")
        elif move == "2":
            defending = True
            print_delay("You raise your guard. You will take less damage this round.")
            p.health = min(100, p.health + 5)
        else:
            if "Fairy Potion" in p.inventory:
                p.inventory.remove("Fairy Potion")
                p.health = min(100, p.health + 35)
                print_delay("You drink the Fairy Potion! +35 health.")
            elif "Healing Crystal" in p.inventory:
                p.inventory.remove("Healing Crystal")
                p.health = min(100, p.health + 40)
                print_delay("You use the Healing Crystal! +40 health.")
            elif "Fairy Blessing" in p.inventory:
                print_delay("The Fairy Blessing shields you! Guardian misses this round.")
                defending = True
            else:
                print_delay("No usable item! You waste a turn.")
        if guardian_hp <= 0:
            break
        # Guardian attacks
        g_dmg = random.randint(10, 25)
        if defending:
            g_dmg //= 2
        print_delay(f"The Guardian slams you for {g_dmg} damage!")
        if not p.take_damage(g_dmg):
            print_delay("The Guardian defeats you...")
            return False
        round_no += 1

    print_delay("The Guardian falls to one knee and bows.")
    print_delay("'You are worthy, adventurer. The door is open.'")
    p.add_score(300)
    if p.health >= 70:
        print_delay("BONUS: You finished with high health! +100 bonus!")
        p.add_score(100)
    print_delay("You step through the stone door into sunlight.")
    print_delay("You finally remember everything - and you are free!")
    return True

# ---------- main ----------
def play_game():
    p = Player()
    p.name = input("What is your name, adventurer? ").strip() or "Adventurer"
    print_delay(f"Welcome, {p.name}!")
    if not level_1(p):
        print_delay(f"Game Over. Final score: {p.score}")
        return
    if not level_2(p):
        print_delay(f"Game Over. Final score: {p.score}")
        return
    if not level_3(p):
        print_delay(f"Game Over. Final score: {p.score}")
        return
    print_delay("")
    print_delay("=" * 55)
    print_delay(f"YOU ESCAPED! Final score: {p.score}")
    print_delay(f"Health left: {p.health}")
    print_delay(f"Items collected: {', '.join(p.inventory) if p.inventory else 'none'}")
    if p.score >= 700:
        print_delay("Rank: LEGENDARY HERO!")
    elif p.score >= 450:
        print_delay("Rank: BRAVE ADVENTURER!")
    else:
        print_delay("Rank: LUCKY SURVIVOR!")
    print_delay("=" * 55)
    if ask_yes_no("Play again? Enter 'yes' or 'no': "):
        play_game()

if __name__ == "__main__":
    play_game()
