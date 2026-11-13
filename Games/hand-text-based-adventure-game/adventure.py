import random
from typing import Required, TypedDict

RoomData = TypedDict('RoomData', {
    'description': str,
    'items': list[str],
    'enemies': list[str],
    'exits': list[str],
})

PlayerData = TypedDict('PlayerData', {
    'name': str,
    'class': str,
    'health': int,
    'max_health': int,
    'strength': int,
    'intelligence': int,
    'agility': int,
    'level': int,
    'experience': int,
    'gold': int,
    'inventory': list[str],
    'equipped_weapon': str | None,
    'equipped_armor': str | None,
    'current_room': str,
})

ClassStats = TypedDict('ClassStats', {
    'health': int,
    'strength': int,
    'intelligence': int,
    'agility': int,
})

EnemyData = TypedDict('EnemyData', {
    'health': int,
    'strength': int,
    'intelligence': int,
    'agility': int,
    'xp': int,
    'gold': tuple[int, int],
})

ItemData = TypedDict('ItemData', {
    'type': Required[str],
    'value': Required[int],
    'damage': int,
    'defense': int,
    'healing': int,
}, total=False)

# Game data
rooms: dict[str, RoomData] = {
    'hallway': {'description': 'You are in a dark hallway.', 'items': ['key'], 'enemies': [], 'exits': ['garden', 'kitchen', 'shop']},
    'garden': {'description': 'You are in a beautiful garden.', 'items': ['potion'], 'enemies': ['goblin'], 'exits': ['hallway', 'forest']},
    'kitchen': {'description': 'You are in a kitchen.', 'items': ['knife'], 'enemies': [], 'exits': ['hallway', 'pantry']},
    'forest': {'description': 'You are in a dense forest.', 'items': ['sword'], 'enemies': ['troll'], 'exits': ['garden']},
    'pantry': {'description': 'You are in a pantry.', 'items': ['food'], 'enemies': [], 'exits': ['kitchen']},
    'shop': {'description': 'You are in a shop.', 'items': ['sword', 'shield', 'potion'], 'enemies': [], 'exits': ['hallway']}
}

player: PlayerData = {'name': '', 'class': '', 'health': 0, 'max_health': 0, 'strength': 0, 'intelligence': 0, 'agility': 0,
          'level': 1, 'experience': 0, 'gold': 50, 'inventory': [], 'equipped_weapon': None, 'equipped_armor': None,
          'current_room': 'hallway'}

classes: dict[str, ClassStats] = {
    'warrior': {'health': 120, 'strength': 15, 'intelligence': 5, 'agility': 10},
    'mage': {'health': 80, 'strength': 5, 'intelligence': 15, 'agility': 10},
    'rogue': {'health': 100, 'strength': 10, 'intelligence': 5, 'agility': 15}
}

enemies: dict[str, EnemyData] = {
    'goblin': {'health': 50, 'strength': 10, 'intelligence': 5, 'agility': 10, 'xp': 80, 'gold': (10, 30)},
    'troll': {'health': 100, 'strength': 15, 'intelligence': 5, 'agility': 5, 'xp': 150, 'gold': (20, 50)}
}

items: dict[str, ItemData] = {
    'key': {'type': 'misc', 'value': 10},
    'sword': {'type': 'weapon', 'value': 50, 'damage': 10},
    'shield': {'type': 'armor', 'value': 30, 'defense': 5},
    'potion': {'type': 'potion', 'value': 20, 'healing': 20},
    'knife': {'type': 'weapon', 'value': 20, 'damage': 5},
    'food': {'type': 'misc', 'value': 5, 'healing': 10}
}

# --- Helpers ---
def get_weapon_damage():
    if player['equipped_weapon']:
        return items[player['equipped_weapon']].get('damage', 0)
    return 0

def get_defense():
    if player['equipped_armor']:
        return items[player['equipped_armor']].get('defense', 0)
    return 0

def gain_xp(amount: int) -> None:
    player['experience'] += amount
    print(f"You gained {amount} XP!")
    while player['experience'] >= 100:
        player['experience'] -= 100
        player['level'] += 1
        player['max_health'] += 20
        player['health'] = player['max_health']
        player['strength'] += 2
        player['agility'] += 1
        print(f"*** You leveled up! You are now level {player['level']} ***")
        print(f"Health restored to {player['health']}. Strength +2, Agility +1")

# --- Game functions ---
def create_player():
    player['name'] = input("Enter your name: ").strip() or "Adventurer"
    print("Choose a class:")
    print("1. Warrior  2. Mage  3. Rogue")
    choice = input("> ").strip()
    class_map = {'1': 'warrior', '2': 'mage', '3': 'rogue'}
    player['class'] = class_map.get(choice, 'warrior')
    stats = classes[player['class']]
    player['health'] = player['max_health'] = stats['health']
    player['strength'] = stats['strength']
    player['intelligence'] = stats['intelligence']
    player['agility'] = stats['agility']
    print(f"Welcome, {player['name']} the {player['class']}!")

def describe_room(room: str):
    r = rooms[room]
    print(f"\n--- {room.upper()} ---")
    print(r['description'])
    print("Exits:", ", ".join(r['exits']))
    print("Items:", ", ".join(r['items']) or "none")
    print("Enemies:", ", ".join(r['enemies']) or "none")

def move_room(direction: str):
    if direction in rooms[player['current_room']]['exits']:
        player['current_room'] = direction
        describe_room(player['current_room'])
    else:
        print("You can't go that way.")

def take_item(item: str):
    room_items = rooms[player['current_room']]['items']
    if item in room_items:
        room_items.remove(item)
        player['inventory'].append(item)
        print(f"You took {item}")
        # Auto-equip first weapon/armor
        if items[item]['type'] == 'weapon' and not player['equipped_weapon']:
            player['equipped_weapon'] = item
            print(f"You equipped {item}!")
        elif items[item]['type'] == 'armor' and not player['equipped_armor']:
            player['equipped_armor'] = item
            print(f"You equipped {item}!")
    else:
        print(f"There is no {item} here.")

def use_item(item: str):
    if item not in player['inventory']:
        print(f"You don't have {item}.")
        return
    data = items[item]
    if data['type'] == 'potion' or item == 'food':
        heal = data.get('healing', 0)
        player['health'] = min(player['max_health'], player['health'] + heal)
        player['inventory'].remove(item)
        print(f"You used {item} and healed {heal} HP. Health: {player['health']}/{player['max_health']}")
    elif data['type'] == 'weapon':
        player['equipped_weapon'] = item
        print(f"You equipped {item} (+{data.get('damage', 0)} damage)")
    elif data['type'] == 'armor':
        player['equipped_armor'] = item
        print(f"You equipped {item} (+{data.get('defense', 0)} defense)")
    else:
        print(f"You can't use {item} like that.")

def fight_enemy(enemy_name: str) -> bool | None:
    if enemy_name not in rooms[player['current_room']]['enemies']:
        print(f"There is no {enemy_name} here.")
        return

    # Copy so the global template doesn't get mutated
    enemy = enemies[enemy_name].copy()
    print(f"A wild {enemy_name} appears! (HP: {enemy['health']})")

    while enemy['health'] > 0 and player['health'] > 0:
        action = input("Do you want to [attack / use potion / run]? ").lower().strip()

        if action == 'run':
            # Agility vs enemy agility decides escape chance
            chance = 0.5 + (player['agility'] - enemy['agility']) * 0.02
            if random.random() < chance:
                dest = random.choice(rooms[player['current_room']]['exits'])
                print(f"You escaped to {dest}!")
                move_room(dest)
                return
            else:
                print("You failed to escape!")

        elif action in ('attack', 'a'):
            # Player attack: base + weapon + random variance + crit
            base = player['strength'] + get_weapon_damage()
            damage = max(1, base + random.randint(-3, 3))
            crit = random.random() < 0.15  # 15% crit
            if crit:
                damage *= 2
                print("CRITICAL HIT!")
            enemy['health'] -= damage
            print(f"You attacked {enemy_name} for {damage} damage. (Enemy HP: {max(0, enemy['health'])})")

            if enemy['health'] <= 0:
                break

            # Enemy attack: can miss based on player agility
            dodge_chance = player['agility'] * 0.01
            if random.random() < dodge_chance:
                print(f"You dodged {enemy_name}'s attack!")
            else:
                enemy_damage = max(1, enemy['strength'] + random.randint(-2, 4) - get_defense())
                player['health'] -= enemy_damage
                print(f"{enemy_name} attacked you for {enemy_damage} damage. (Your HP: {max(0, player['health'])})")

        elif action.startswith('use'):
            parts = action.split()
            if len(parts) > 1:
                use_item(parts[1])
            else:
                print("Use what? Try 'use potion'")
        else:
            print("Invalid combat action.")

    if player['health'] <= 0:
        print("You died! Game over.")
        return False

    if enemy['health'] <= 0:
        rooms[player['current_room']]['enemies'].remove(enemy_name)
        gold_won = random.randint(*enemy['gold'])
        player['gold'] += gold_won
        print(f"You killed {enemy_name}! +{gold_won} gold.")
        gain_xp(enemy['xp'])
    return True

def shop():
    print("\nWelcome to the shop! Your gold:", player['gold'])
    for item in rooms['shop']['items']:
        print(f"  {item} - {items[item]['value']} gold")
    print("Your inventory:", player['inventory'])

    action = input("Do you want to [buy / sell / leave]? ").lower().strip()
    if action == 'buy':
        item = input("What do you want to buy? ").lower().strip()
        if item not in rooms['shop']['items']:
            print("We don't have that item.")
        elif player['gold'] < items[item]['value']:
            print("You don't have enough gold!")
        else:
            player['gold'] -= items[item]['value']
            rooms['shop']['items'].remove(item)
            player['inventory'].append(item)
            print(f"You bought {item} for {items[item]['value']} gold.")
    elif action == 'sell':
        item = input("What do you want to sell? ").lower().strip()
        if item not in player['inventory']:
            print("You don't have that item.")
        else:
            sell_price = items[item]['value'] // 2
            player['gold'] += sell_price
            player['inventory'].remove(item)
            rooms['shop']['items'].append(item)
            print(f"You sold {item} for {sell_price} gold.")

def show_stats():
    print(f"\n{player['name']} | {player['class']} | Lv {player['level']}")
    print(f"HP: {player['health']}/{player['max_health']} | Gold: {player['gold']} | XP: {player['experience']}/100")
    print(f"STR: {player['strength']} INT: {player['intelligence']} AGI: {player['agility']}")
    print(f"Weapon: {player['equipped_weapon']} | Armor: {player['equipped_armor']}")
    print(f"Inventory: {player['inventory']}")

# --- Game loop ---
create_player()
describe_room(player['current_room'])
print("\nCommands: go <room> | take <item> | use <item> | fight <enemy> | inventory | stats | health | shop | look | quit")

while True:
    if player['health'] <= 0:
        break
    parts = input("\n> ").lower().split()
    if not parts:
        continue
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if cmd == 'go':
        move_room(arg)
    elif cmd == 'take':
        take_item(arg)
    elif cmd == 'use':
        use_item(arg)
    elif cmd == 'fight':
        if not fight_enemy(arg):
            break
    elif cmd == 'inventory':
        print("You have:", player['inventory'], f"| Gold: {player['gold']}")
    elif cmd == 'health':
        print(f"Your health is: {player['health']}/{player['max_health']}")
    elif cmd == 'stats':
        show_stats()
    elif cmd == 'look':
        describe_room(player['current_room'])
    elif cmd == 'shop':
        if player['current_room'] == 'shop':
            shop()
        else:
            print("You need to go to the shop first! It's off the hallway.")
    elif cmd == 'quit':
        print("Thanks for playing!")
        break
    else:
        print("Invalid command. Try: go, take, use, fight, inventory, stats, health, shop, look, quit")