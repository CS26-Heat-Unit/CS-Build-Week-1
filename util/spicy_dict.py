from django.db import models
import random


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


spicy_dict = {
    "Jalapeno": "2,500 – 8,000",
    "Serrano Peppers": "10,000 – 23,000",
    "Chile de Arbol Peppers": "15,000 – 65,000",
    "Cayenne Peppers": "30,000 – 50,000",
    "Chiltepin Peppers": "50,000 – 100,000",
    "Habanero Peppers": "100,000 – 350,000",
    "Ghost Peppers": "1,000,000",
    "Carolina Reaper Chili Pepper": "2,200,000+"
}

spicy_choices = list(spicy_dict.keys())[:len(spicy_dict.keys())]

Room.objects.all().delete()

r_outside = Room(title="California Reaper",
                 description="North of you, the cave mount beckons")

r_foyer = Room(title="Ghost Pepper", description="""Dim light filters in from the south. Dusty
passages run north and east.""")

r_overlook = Room(title="Habenero", description="""A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""")

r_narrow = Room(title="Jalepeno", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Poblano", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")
r_foyer.connectRooms(r_outside, "s")

r_foyer.connectRooms(r_overlook, "n")
r_overlook.connectRooms(r_foyer, "s")

r_foyer.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_foyer, "w")

r_narrow.connectRooms(r_treasure, "n")
r_treasure.connectRooms(r_narrow, "s")

players = Player.objects.all()
for p in players:
    p.currentRoom = r_outside.id
    p.save()


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        x = -1
        y = 0
        room_count = 0

        direction = 1

        previous_room = None
        while room_count < num_rooms:

            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                room_direction = "n"
                y += 1
                direction *= -1

            pepper = random.choice(spicy_choices)
            pepper_description = "This room is listed at {} on the scoville scale, your discretion is advised".format(
                spicy_dict[pepper])
            room = Room(room_count, title="{} Room".format(pepper), description=pepper_description)

            room.save()

            self.grid[y][x] = room

            if previous_room is not None:
                previous_room.connectRooms(room, room_direction)

            previous_room = room
            room_count += 1

    def print_rooms(self):

        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        reverse_grid = list(self.grid)
        reverse_grid.reverse()
        for row in reverse_grid:
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        print(str)


w = World()
num_rooms = 100
width = 12
height = 12
w.generate_rooms(width, height, num_rooms)
w.print_rooms()

print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
