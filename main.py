from lexer import tokenize
from parser import Parser
from interpreter import CalculatorInterpreter
from world import World
from player import Player
import json
import random

# TODO: Spellcasting implementation
# TODO: Combat implementation
# TODO: Validate input for internal menu items
# TODO: Finish upstairs of haunted house level
# TODO: Add more levels!
# TODO: Commenting and docstrings

def select_valid_level():
    '''
    Prompt user to select a valid level.
    Returns the selected level as an integer.
    '''
    while True:
        print("Select a level")
        print("1) Haunted House")
        choice = input("Which level would you like to complete: ")
        
        if choice in ("1"):
            return int(choice)


def select_valid_action(world):
    '''
    Prompt user to select a valid action.
    
    :param world: the current game world
    :return: the selected action as an integer
    '''
    while True:
        print("Select an action")
        print("1) Move")
        print("2) Investigate Target")
        print("3) View and Modify Inventory")
        print("4) View Stats")
        print("5) Save Progress")

        valid = ["1", "2", "3", "4", "5"]
        if world.player.unlocked["spellbook"] == True: 
            print("5) Use Spell")
            valid.append("6")

        choice = input("Which action: ")
            
        if choice in valid:
                return int(choice)
        

def to_dict(self):
    '''
    Converts the Player object to a dictionary for JSON serialization.
    
    :param self: Player object
    :return: dictionary representation of the Player
    '''
    return {
        "name": self.name,
        "hp": self.hp,
        "unlocked": self.unlocked,

        # inventory = {name: itemobject}
        "inventory": {
            name: item.to_dict() for name, item in self.inventory.items()
        },

        # equipped = {slot: itemobject or None}
        "equipped": {
            slot: item.to_dict() if item else None
            for slot, item in self.equipped.items()
        },

        "attack": self.attack,
        "defense": self.defense,
        "stealth": self.stealth,
        "wit": self.wit
    }


def start_script():
    '''
    Start script to initialize or load player data.

    :return: None
    '''
    # If not existing player, set new player stats and name
    while True:
        print("1) Start New Game and Override Save")
        print("2) Load From Save")
        choice = input("Choose: ")
        if choice in ("1", "2"):
            if int(choice) == 1:
                name = input("Choose a name: ")
                with open("player.json") as f:
                    data = json.load(f)
                player = Player(name, 10, {"spellbook": False}, {}, {}, 5, 5, 5, 5)
                with open("player.json", "w") as f:
                    json.dump(to_dict(player), f, indent=2)

            break

def combat2(world):
    print("\nCombat initiated!")

    revealed = set()

    advantage = {
        "power": "speed",
        "speed": "trick",
        "trick": "power"
    }

    while world.current_room.enemies:
        # Show enemy list
        print("\nEnemies:")
        for key, enemy in world.current_room.enemies.items():
            print(f" - {enemy.name}")

        # Player chooses enemy
        choice = input("\nAttack which enemy? ").strip().lower().replace(" ", "_")
        if choice not in world.current_room.enemies:
            print("Invalid enemy.")
            continue

        enemy = world.current_room.enemies[choice]

        # First-time reveal
        if choice not in revealed:
            print(f"\n➡ {enemy.name}: {enemy.description}")
            revealed.add(choice)

        # Player chooses attack style
        move = ""
        while move not in ("power", "speed", "trick"):
            move = input("Choose attack (power/speed/trick): ").strip().lower()

        enemy_move = random.choice(["power", "speed", "trick"])

        # Determine outcome
        if advantage[move] == enemy_move:
            dmg = world.player.attack
            print(f"\nYou win the clash! {enemy.name} takes {dmg} damage.")
        elif move == enemy_move:
            dmg = world.player.attack // 2
            print(f"\nTie. {enemy.name} takes {dmg} damage.")
        else:
            dmg = 0
            print("\nYou lose the clash! No damage dealt.")

        enemy.hp -= dmg

        # Enemy defeated
        if enemy.hp <= 0:
            print(f"{enemy.name} is defeated!")
            del world.current_room.enemies[choice]
            continue
        else:
            pass

        # Enemy strikes back
        retaliation = max(1, enemy.attack - world.player.defense)
        world.player.hp -= retaliation
        print(f"{enemy.name} hits you for {retaliation}. Your HP: {world.player.hp}")

        if world.player.hp <= 0:
            print("You have been defeated.\n")
            exit()


def combat(world):
    print("Combat initiated!")

    moves = {
        "power": {"beats": "speed"},
        "speed": {"beats": "trick"},
        "trick": {"beats": "power"}
    }

    room = world.current_room
    enemies = room.enemies

    while enemies:
        # Player chooses move
        print("Choose your style (power / speed / trick):")
        player_move = input("> ").strip().lower()
        if player_move not in moves:
            print("Invalid move.")
            continue

        # Choose an enemy
        enemy_name = list(enemies.keys())[0]
        enemy = enemies[enemy_name]

        # Enemy randomly chooses move
        import random
        enemy_move = random.choice(list(moves.keys()))
        print(f"{enemy_name} chooses {enemy_move}!")

        # Resolve
        if moves[player_move]["beats"] == enemy_move:
            dmg = max(1, world.player.attack - enemy.defense)
            enemy.hp -= dmg
            print(f"You outmaneuver {enemy_name}! You deal {dmg} damage.")
        elif moves[enemy_move]["beats"] == player_move:
            dmg = max(1, enemy.attack - world.player.defense)
            world.player.hp -= dmg
            print(f"{enemy_name} outplays you! You take {dmg} damage.")
        else:
            print("Your moves clash and nothing happens!")

        # Check death
        if enemy.hp <= 0:
            print(f"{enemy_name} is defeated!")
            del enemies[enemy_name]

        if world.player.hp <= 0:
            print("You died.")
            exit()



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

        if world.current_room.enemies != {}:
            print(world.current_room.combat_init_text + "\n")
            combat2(world)
            print("\nYou have defeated all enemies in the room!\n")
            print(world.current_room.description + "\n")

        action = select_valid_action(world)

        if action == 1:
            print("\nChoose an exit:")
            for exits in world.current_room.exits:
                if world.current_room.exits[exits].hidden == False:
                    print("- Go " + exits)
                else:
                    for item in world.player.inventory:
                        if  world.player.inventory[item].reveal_exit == world.current_room.exits[exits].room.name:
                            print("You use your parchment to reveal a door.")
                            print("- Go " + exits)
                            world.current_room.exits[exits].hidden = False
                            break
            direction = input("Choose a direction: ").strip().lower()
            if direction in world.current_room.exits:
                if world.current_room.exits[direction].unlocked and world.current_room.exits[direction].hidden == False:
                    world.current_room = world.current_room.exits[direction].room
                elif world.current_room.exits[direction].hidden == True:
                    print("\nYou can't go that way.")
                elif world.current_room.exits[direction].unlocked == False:
                    unlocked = False
                    for item in world.player.inventory:
                        if world.player.inventory[item].unlock_door == world.current_room.exits[direction].room.name:
                            print("\nYou use the key to unlock the door.")
                            world.current_room.exits[direction].unlocked = True
                            world.current_room = world.current_room.exits[direction].room
                            unlocked = True
                            break
                    if unlocked == False:
                        print("\nThe door is locked.")
                else:
                    print("\nYou can't go that way.")
            else:
                print("\nYou can't go that way.")

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
                        print("- " + item.name.replace("_", " "))
                        world.player.inventory[item.name] = item
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
                print("- " + item.replace("_", " "))
            
            print("\nYour Equipped Items:")
            for item in world.player.equipped:
                print("- " + item.replace("_", " "))

            print("\n1)Investigate an Item")
            print("2)Equip an Item")
            print("3)De-equip an Item")

            choice = input("Choose an option: ")
            if choice == "1":
                choice = input("Choose an item to search: ").strip().lower().replace(" ", "_")
                print(world.player.inventory[choice].description)
            elif choice == "2":
                choice = input("Choose an item to equip: ").strip().lower().replace(" ", "_")
                if choice not in world.player.inventory:
                    print("\nYou don't have that item in your inventory.\n")
                    continue
                world.player.equipped[choice] = world.player.inventory[choice]
                del world.player.inventory[choice]
                world.player.attack += world.player.equipped[choice].attack
                world.player.defense += world.player.equipped[choice].defense
                world.player.stealth += world.player.equipped[choice].stealth
                world.player.wit += world.player.equipped[choice].wit
                print(f"\nYou have equipped {choice}.\n")
            elif choice == "3":
                choice = input("Choose an item to de-equip: ").strip().lower().replace(" ", "_")
                if choice not in world.player.equipped:
                    print("\nYou don't have that item equipped.\n")
                    continue
                world.player.inventory[choice] = world.player.equipped[choice]
                world.player.attack -= world.player.equipped[choice].attack
                world.player.defense -= world.player.equipped[choice].defense
                world.player.stealth -= world.player.equipped[choice].stealth
                world.player.wit -= world.player.equipped[choice].wit
                del world.player.equipped[choice]
                print(f"\nYou have de-equipped {choice}.\n")
            
        elif action == 4:
            print(f"\nPlayer Stats for {world.player.name}:")
            print(f"HP: {world.player.hp}")
            print(f"Attack: {world.player.attack}")
            print(f"Defense: {world.player.defense}")
            print(f"Stealth: {world.player.stealth}")
            print(f"Wit: {world.player.wit}\n")

        elif action == 5:
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
    print("\nQuitting Codebound")
