from lexer import tokenize
from parser import Parser
from interpreter import CalculatorInterpreter
from world import World
from player import Player
import json


def select_valid_level():
    while True:
        print("Select a level")
        print("1) Haunted House")
        choice = input("Which level would you like to complete: ")
        
        if choice in ("1"):
            return int(choice)


def select_valid_action(world):
    while True:
        print("Select an action")
        print("1) Move")
        print("2) Investigate Target")
        print("3) View and Modify Inventory")
        print("4) Save Progress")

        valid = ["1", "2", "3", "4"]
        if world.player.unlocked["spellbook"] == True: 
            print("5) Use Spell")
            valid.append("5")

        choice = input("Which action: ")
            
        if choice in valid:
                return int(choice)
        

def to_dict(player):
    return {
        "name": player.name,
        "hp": player.hp,
        "unlocked": player.unlocked,
        "inventory": [item.to_dict() for item in player.inventory],
        "equiped":  [item.to_dict() for item in player.equiped],
        "attack": player.attack,
        "defense": player.defense,
        "stealth": player.stealth,
        "wit": player.wit
    }

def start_script():
    # If not existing player, set new player stats and name
    while True:
        print("1) Start New Game")
        print("2) Load From Save")
        choice = input("Choose: ")
        if choice in ("1", "2"):
            if int(choice) == 1:
                name = input("Choose a name: ")
                with open("player.json") as f:
                    data = json.load(f)
                player = Player(name, 25, {"spellbook": False}, [], [], 5, 5, 5, 5)
                with open("player.json", "w") as f:
                    json.dump(to_dict(player), f, indent=2)

            break
        

### GAME START
print("Welcome to Codebound!\n")
start_script()

level = select_valid_level()

if level == 1:
    world = World("world.json")
        
world.run_startup()

### GAME LOOP
try:
    while True: 

        print("\n" +  world.current_room.description + "\n")

        action = select_valid_action(world)

        if action == 1:
            print("\nChoose an exit:")
            for exits in world.current_room.exits:
                print("- Go " + exits)
            direction = input("Choose a direction: ").strip().lower()
            if direction in world.current_room.exits:
                if world.current_room.exits[direction].unlocked:
                    world.current_room = world.current_room.exits[direction].room
                else:
                    unlocked = False
                    for item in world.player.inventory:
                        if item.unlock_door == world.current_room.exits[direction].room.name:
                            print("\nYou use the key to unlock the door.")
                            world.current_room.exits[direction].unlocked = True
                            world.current_room = world.current_room.exits[direction].room
                            unlocked = True
                            break
                    if unlocked == False:
                        print("\nThe door is locked")

        elif action == 2:
            # print("\nChoose an item:")
            # for search in world.current_room.searchables:
            #     print("- " + search.name.replace("_", " "))
            choice = input("Choose an item to search: ").strip().lower().replace(" ", "_")
        
            found = False
            for searchable in world.current_room.searchables:
                if choice == searchable.name:
                    items = searchable.items
                    print("\nYou found: ")
                    for item in items:
                        print("- " + item.name)
                        world.player.inventory.append(item)
                        if item.unlock_spellbook == True:
                            world.player.unlocked["spellbook"] = True
                    searchable.items = []
                    found = True
                print("")
            if found == False:
                print("That item is not searchable.\n")

        elif action == 3:
            print("\nYour Inventory:")
            for item in world.player.inventory:
                print("- " + item.name.replace("_", " "))
            
            print("\nYour Equiped Items:")
            for item in world.player.equiped:
                print("- " + item.name.replace("_", " "))

            print("\nA)Investigate an Item")
            print("\nB)Equip an Item")
            print("\nC)De-equip an Item")

            choice = input("Choose an option")
            if choice == "A":
                choice = input("Choose an item to search: ").strip().lower().replace(" ", "_")
                print(world.player.inventory[choice])
            elif choice == "B":
                choice = input("Choose an item to equip: ").strip().lower().replace(" ", "_")
            elif choice == "C":
                choice = input("Choose an item to de-equip: ").strip().lower().replace(" ", "_")
            
        elif action == 4:
            with open("player.json", "w") as f:
                        json.dump(to_dict(world.player), f, indent=2)

            print("Your game has been saved. Press CTRL-D or close the window to quit.")

        elif action == 5:
            program = input("Input your program. Separate commands with \">\":")
            program = program.replace(">", "\n")
            print(program)

            tokens = tokenize(program)
            ast = Parser(tokens).parse()
            CalculatorInterpreter(world).run(ast)

except (KeyboardInterrupt, EOFError):
    print("Quitting Codebound")
