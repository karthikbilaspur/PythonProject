import random

class Room:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = random.choice(['normal', 'treasure', 'enemy'])

class Dungeon:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.rooms = []

    def generate(self):
        self.add_rooms()
        self.add_corridors()
        self.add_doors()
        self.add_enemies()
        self.add_treasures()
        self.add_stairs()

    def add_rooms(self):
        num_rooms = random.randint(5, 10)
        for _ in range(num_rooms):
            room_width = random.randint(4, 12)
            room_height = random.randint(4, 10)
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)
            room = Room(x, y, room_width, room_height)
            self.rooms.append(room)
            self.create_room(room)

    def create_room(self, room: Room):
        for i in range(room.x, room.x + room.width):
            for j in range(room.y, room.y + room.height):
                self.grid[j][i] = '.'

    def add_corridors(self):
        for i in range(len(self.rooms) - 1):
            room1 = self.rooms[i]
            room2 = self.rooms[i + 1]
            self.create_corridor(room1, room2)

    def create_corridor(self, room1: Room, room2: Room):
        x1 = room1.x + room1.width // 2
        y1 = room1.y + room1.height // 2
        x2 = room2.x + room2.width // 2
        y2 = room2.y + room2.height // 2
        if x1 < x2:
            for x in range(x1, x2 + 1):
                self.grid[y1][x] = '.'
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[y][x2] = '.'
        else:
            for x in range(x2, x1 + 1):
                self.grid[y2][x] = '.'
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[y][x1] = '.'

    def add_doors(self):
        for room in self.rooms:
            if random.random() < 0.2:
                self.grid[room.y + room.height // 2][room.x + room.width // 2] = '+'

    def add_enemies(self):
        num_enemies = random.randint(5, 10)
        for _ in range(num_enemies):
            room = random.choice(self.rooms)
            x = random.randint(room.x + 1, room.x + room.width - 2)
            y = random.randint(room.y + 1, room.y + room.height - 2)
            self.grid[y][x] = 'E'

    def add_treasures(self):
        num_treasures = random.randint(5, 10)
        for _ in range(num_treasures):
            room = random.choice(self.rooms)
            x = random.randint(room.x + 1, room.x + room.width - 2)
            y = random.randint(room.y + 1, room.y + room.height - 2)
            self.grid[y][x] = '$'

    def add_stairs(self):
        self.grid[self.rooms[0].y + self.rooms[0].height // 2][self.rooms[0].x + self.rooms[0].width // 2] = '<'
        self.grid[self.rooms[-1].y + self.rooms[-1].height // 2][self.rooms[-1].x + self.rooms[-1].width // 2] = '>'

    def print_dungeon(self):
        for row in self.grid:
            print(''.join(row))

dungeon = Dungeon(80, 40)
dungeon.generate()
dungeon.print_dungeon()