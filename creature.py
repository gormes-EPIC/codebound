class Summons: 

    def move(self, direction, world):
        if direction in self.current_room.exits:
            if self.current_room.exits[direction].unlocked and self.current_room.exits[direction].hidden == False:
                self.current_room = self.current_room.exits[direction].room
            elif self.current_room.exits[direction].hidden == True:
                print("\nYour summons can't go that way.")
            # elif self.current_room.exits[direction].unlocked == False:
            #     unlocked = False
            #     for item in world.player.inventory:
            #         if world.player.inventory[item].unlock_door == self.current_room.exits[direction].room.name:
            #             print("\nYour summons uses the key to unlock the door.")
            #             self.current_room.exits[direction].unlocked = True
            #             self.current_room = self.current_room.exits[direction].room
            #             unlocked = True
            #             break
                # if unlocked == False:
            elif self.current_room.exits[direction].unlocked == False:
                print("\nYour summons can't go that way. The door is locked.")
            else:
                print("\nYour summons can't go that way.")
        else:
            print("\nYour summons can't go that way.")

        self.report += f" - {direction}: " + self.current_room.description + "\n"
        # print(f"The construct moves {direction}.")

class Construct(Summons):
    def __init__(self, name, room=None):
        self.name = name
        self.hp = 5
        self.attack = 3
        self.defense = 4
        self.wit = 2
        self.stealth = 1
        self.current_room = room
        self.report = ""

class Bat(Summons):
    def __init__(self, name, room=None):
        self.name = name
        self.hp = 2
        self.attack = 2
        self.defense = 1
        self.wit = 3
        self.stealth = 4
        self.current_room = room
        self.report = ""


class Ghost(Summons):
    def __init__(self, name, room=None):
        self.name = name
        self.hp = 3
        self.attack = 0
        self.defense = 2
        self.wit = 4
        self.stealth = 5
        self.current_room = room
        self.report = ""


