import random

# Game data
rooms = {
    'hallway': {'description': 'You are in a dark hallway.', 'items': ['key'], 'enemies': [], 'exits': ['garden', 'kitchen']},
    'garden': {'description': 'You are in a beautiful garden.', 'items': ['potion'], 'enemies': ['goblin'], 'exits': ['hallway', 'forest']},
    'kitchen': {'description': 'You are in a kitchen.', 'items': ['knife'], 'enemies': [], 'exits': ['hallway', 'pantry']},
    'forest': {'description': 'You are in a dense forest.', 'items': ['sword'], 'enemies': ['troll'], 'exits': ['garden']},
    'pantry': {'description': 'You are in a pantry.', 'items': ['food'], 'enemies': [], 'exits': ['kitchen']},
    'shop': {'description': 'You are in a shop.', 'items': ['sword', 'shield', 'potion'], 'enemies': [], 'exits': ['hallway']}
}

player = {'name': '', 'class': '', 'health': 0, 'strength': 0, 'intelligence': 0, 'agility': 0, 'level': 1, 'experience': 0, 'inventory': [], 'current_room': 'hallway'}

classes = {
    'warrior': {'health': 120, 'strength': 15, 'intelligence': 5, 'agility': 10},
    'mage': {'health': 80, 'strength': 5, 'intelligence': 15, 'agility': 10},
    'rogue': {'health': 100, 'strength': 10, 'intelligence': 5, 'agility': 15}
}

enemies = {
    'goblin': {'health': 50, 'strength': 10, 'intelligence': 5, 'agility': 10},
    'troll': {'health': 100, 'strength': 15, 'intelligence': 5, 'agility': 5}
}

items = {
    'key': {'type': 'misc', 'value': 10},
    'sword': {'type': 'weapon', 'value': 50, 'damage': 10},
    'shield': {'type': 'armor', 'value': 30, 'defense': 5},
    'potion': {'type': 'potion', 'value': 20, 'healing': 20},
    'knife': {'type': 'weapon', 'value': 20, 'damage': 5},
    'food': {'type': 'misc', 'value': 5}
}

# Game functions
def create_player():
    player['name'] = input("Enter your name: ")
    print("Choose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    choice = input("> ")
    if choice == '1':
        player['class'] = 'warrior'
    elif choice == '2':
        player['class'] = 'mage'
    elif choice == '3':
        player['class'] = 'rogue'
    player['health'] = classes[player['class']]['health']
    player['strength'] = classes[player['class']]['strength']
    player['intelligence'] = classes[player['class']]['intelligence']
    player['agility'] = classes[player['class']]['agility']

def describe_room(room):
    print(rooms[room]['description'])
    print("Exits:", rooms[room]['exits'])
    print("Items:", rooms[room]['items'])
    print("Enemies:", rooms[room]['enemies'])

def move_room(direction):
    if direction in rooms[player['current_room']]['exits']:
        player['current_room'] = direction
        describe_room(player['current_room'])
    else:
        print("You can't go that way.")

def take_item(item):
    if item in rooms[player['current_room']]['items']:
        rooms[player['current_room']]['items'].remove(item)
        player['inventory'].append(item)
        print("You took", item)
    else:
        print("There is no", item, "here.")

def fight_enemy(enemy):
    enemy_stats = enemies[enemy]
    while enemy_stats['health'] > 0:
        action = input("Do you want to attack or run? ")
        if action.lower() == 'attack':
            damage = player['strength'] + items.get('sword', {}).get('damage', 0)
            enemy_stats['health'] -= damage
            print("You attacked", enemy, "for", damage, "damage.")
            if enemy_stats['health'] > 0:
                damage = enemy_stats['strength']
                player['health'] -= damage
                print(enemy, "attacked you for", damage, "damage.")
        elif action.lower() == 'run':
            move_room(random.choice(rooms[player['current_room']]['exits']))
            break
    if enemy_stats['health'] <= 0:
        rooms[player['current_room']]['enemies'].remove(enemy)
        player['experience'] += 100
        print("You killed", enemy)
        if player['experience'] >= 100:
            player['level'] += 1
            player['experience'] = 0
            print("You leveled up!")

def shop():
    print("Welcome to the shop!")
    print("Items:")
    for item in rooms['shop']['items']:
        print(item, items[item]['value'])
    action = input("Do you want to buy or sell? ")
    if action.lower() == 'buy':
        item = input("What do you want to buy? ")
        if item in rooms['shop']['items']:
            rooms['shop']['items'].remove(item)
            player['inventory'].append(item)
            print("You bought", item)
        else:
            print("We don't have that item.")
    elif action.lower() == 'sell':
        item = input("What do you want to sell? ")
        if item in player['inventory']:
            player['inventory'].remove(item)
            rooms['shop']['items'].append(item)
            print("You sold", item)
        else:
            print("You don't have that item.")

# Game loop
create_player()
describe_room(player['current_room'])
while True:
    action = input("> ").lower().split()
    if action[0] == 'go':
        move_room(action[1])
    elif action[0] == 'take':
        take_item(action[1])
    elif action[0] == 'fight':
        fight_enemy(action[1])
    elif action[0] == 'inventory':
        print("You have:", player['inventory'])
    elif action[0] == 'health':
        print("Your health is:", player['health'])
    elif action[0] == 'shop':
        shop()
    elif action[0] == 'quit':
        break
    else:
        print("Invalid command. Type 'go <direction>', 'take <item>', 'fight <enemy>', 'inventory', 'health', 'shop', or 'quit'.")