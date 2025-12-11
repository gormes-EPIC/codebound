class Construct:
    def __init__(self, name, room=None):
        self.name = name
        self.hp = 5
        self.attack = 3
        self.defense = 4
        self.wit = 2
        self.stealth = 1
        self.current_room = room
        self.report = ""

    def move(self, direction, world):
        if direction in world.current_room.exits:
            if world.current_room.exits[direction].unlocked and world.current_room.exits[direction].hidden == False:
                self.current_room = world.current_room.exits[direction].room
            elif world.current_room.exits[direction].hidden == True:
                print("\nYou can't go that way.")
            elif world.current_room.exits[direction].unlocked == False:
                unlocked = False
                for item in world.player.inventory:
                    if world.player.inventory[item].unlock_door == world.current_room.exits[direction].room.name:
                        print("\nYou use the key to unlock the door.")
                        world.current_room.exits[direction].unlocked = True
                        self.current_room = world.current_room.exits[direction].room
                        unlocked = True
                        break
                if unlocked == False:
                    print("\nThe door is locked.")
            else:
                print("\nYou can't go that way.")
        else:
            print("\nYou can't go that way.")

        self.report += f"{direction}: " + self.current_room.description + "\n"

        print(f"The construct moves {direction}.")

class Bat:
    def __init__(self, name, room=None):
        self.name = name
        self.hp = 2
        self.attack = 2
        self.defense = 1
        self.wit = 3
        self.stealth = 4
        self.current_room = room
        self.report = ""

    def move(self, direction, world):
        if direction in world.current_room.exits:
            if world.current_room.exits[direction].unlocked and world.current_room.exits[direction].hidden == False:
                self.current_room = world.current_room.exits[direction].room
            elif world.current_room.exits[direction].hidden == True:
                print("\nYou can't go that way.")
            elif world.current_room.exits[direction].unlocked == False:
                unlocked = False
                for item in world.player.inventory:
                    if world.player.inventory[item].unlock_door == world.current_room.exits[direction].room.name:
                        print("\nYou use the key to unlock the door.")
                        world.current_room.exits[direction].unlocked = True
                        self.current_room = world.current_room.exits[direction].room
                        unlocked = True
                        break
                if unlocked == False:
                    print("\nThe door is locked.")
            else:
                print("\nYou can't go that way.")
        else:
            print("\nYou can't go that way.")

        self.report += f"{direction}: " + self.current_room.description + "\n"
        print(f"The construct moves {direction}.")


class Ghost:
    def __init__(self, name, room=None):
        self.name = name
        self.hp = 3
        self.attack = 0
        self.defense = 2
        self.wit = 4
        self.stealth = 5
        self.current_room = room
        self.report = ""
    
    def move(self, direction, world):
        if direction in world.current_room.exits:
            if world.current_room.exits[direction].unlocked and world.current_room.exits[direction].hidden == False:
                self.current_room = world.current_room.exits[direction].room
            elif world.current_room.exits[direction].hidden == True:
                print("\nYou can't go that way.")
            elif world.current_room.exits[direction].unlocked == False:
                unlocked = False
                for item in world.player.inventory:
                    if world.player.inventory[item].unlock_door == world.current_room.exits[direction].room.name:
                        print("\nYou use the key to unlock the door.")
                        world.current_room.exits[direction].unlocked = True
                        self.current_room = world.current_room.exits[direction].room
                        unlocked = True
                        break
                if unlocked == False:
                    print("\nThe door is locked.")
            else:
                print("\nYou can't go that way.")
        else:
            print("\nYou can't go that way.")

        print("Current Summons Room: " + self.current_room.name)
        self.report += f"{direction}: " + self.current_room.description + "\n"
        print(f"The construct moves {direction}.")


