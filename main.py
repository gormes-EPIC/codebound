from lexer import tokenize
from parser import Parser
from interpreter import WorldInterpreter
from world import World
from player import Player
import json
import random

# TODO: Spellcasting implementation
# TODO: Combat implementation - rough draft done
# TODO: Finish upstairs of haunted house level
# TODO: Commenting and docstrings
# TODO: Implement key items and add them to stats
# TODO: Add level ending and winning condition(then with ending stats of what the user found/defeated)
# TODO: Implement teleporting
# TODO: Implement gated rooms (needing stat level to enter)
# TODO: Implement enemy abilities (favoring for certain attack styles)
# TODO: Implement enemry dropping items
# TODO: Implement puzzle rooms
# TODO: Implement combat tutorial
# TODO: Polish text and descriptions
# TODO: Implement getting rid of items when you find secret doors
# TODO: Implement more items and searchables - items to increase other stats
# TODO: Implement sneaking past enemies
# TODO: Implement list of seen rooms and you can only teleport to seen rooms
# TODO: Implement drawing teleportation circles that you can use to teleport to certain rooms

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
            print("6) Use Spell")
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
import random

def combat3(world):
    print("\nCombat initiated!")

    revealed = set()

    # RPS relationships
    advantage = {
        "power": "speed",   # Power beats Speed
        "speed": "trick",   # Speed beats Trick
        "trick": "power"    # Trick beats Power
    }

    # Move -> stat mapping (for both player and enemy)
    stat_map = {
        "power": "attack",
        "speed": "stealth",
        "trick": "wit"
    }

    while world.current_room.enemies:

        # Show enemies
        print("\nEnemies:")
        for key, enemy in world.current_room.enemies.items():
            print(f" - {enemy.name.replace("_", " ")} (HP: {enemy.hp})")

        # Choose target
        if len(world.current_room.enemies) == 1:
            choice = list(world.current_room.enemies.keys())[0]
            print(f"\nOnly one enemy present. Attacking {choice.replace('_', ' ')}.")
        else:
            choice = input("\nAttack which enemy? ").strip().lower().replace(" ", "_")
            if choice not in world.current_room.enemies:
                print("No such enemy.")
                continue

        enemy = world.current_room.enemies[choice]

        # Reveal description first time
        if choice not in revealed:
            print(f"\n➡ {enemy.name.replace("_", " ")}: {enemy.description}")
            revealed.add(choice)

        # Player move
        move = ""
        while move not in ("power", "speed", "trick"):
            move = input("Choose attack (power/speed/trick): ").strip().lower()

        # Enemy move randomly every turn
        enemy_move = random.choice(["power", "speed", "trick"])
        print(f"{enemy.name} uses {enemy_move}!")

        # Damage stats
        player_stat = getattr(world.player, stat_map[move])
        enemy_stat  = getattr(enemy, stat_map[enemy_move])

        # Determine outcome & damage
        if advantage[move] == enemy_move:
            dmg = max(1, player_stat - enemy.defense)
            print(f"You win the clash! {enemy.name} takes {dmg} damage.")
        elif move == enemy_move:
            dmg = max(1, (player_stat // 2) - enemy.defense)
            print(f"Tie. {enemy.name} takes {dmg} damage.")
        else:
            dmg = 0
            print("You lose the clash! No damage dealt.")

        enemy.hp -= dmg

        # Enemy defeated?
        if enemy.hp <= 0:
            print(f"{enemy.name} is defeated!")
            del world.current_room.enemies[choice]
            continue

        # Enemy retaliation uses *their attack style stat*
        retaliation = max(1, enemy_stat - world.player.defense)
        world.player.hp -= retaliation
        print(f"{enemy.name} strikes you for {retaliation} damage! Your HP: {world.player.hp}")

        if world.player.hp <= 0:
            print("You have been defeated.")
            tabulate(world)
            exit()


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

def tabulate(world):
    sum = 0
    for item in world.player.inventory:
        if world.player.inventory[item].key_item == True:
            sum += 1
    for item in world.player.equipped:
        if world.player.equipped[item].key_item == True:
            sum += 1
    print(f"You have found {sum} key items during your adventure.")
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

        if world.game_won == True:
            print("Congratulations! You have gathered all the necessary evidence and are able to escape!")
            tabulate(world)
            break

        print("\n" +  world.current_room.description + "\n")
        if world.summons != None:
            print('\n' + world.summons.current_room.name + '\n')

        if world.current_room.enemies != {}:
            print(world.current_room.combat_init_text + "\n")
            combat3(world)
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
            print("\nChoose an item:")
            for search in world.current_room.searchables:
                print("- " + search.name.replace("_", " "))
            choice = input("Choose an item to search: ").strip().lower().replace(" ", "_")
        
            found = False
            for searchable in world.current_room.searchables:
                if choice == searchable.name:
                    items = searchable.items
                    print("\nYou found: ")
                    for item in items:
                        print("- " + item.display_name)
                        world.player.inventory[item.name] = item
                        if item.unlock_spellbook == True:
                            world.player.unlocked["spellbook"] = True
                        if item.end_condition == True:
                            world.game_won = True
                    searchable.items = []
                    found = True
                print("")
            if found == False:
                print("That item is not searchable.\n")

        elif action == 3:
            number = 1
            item_list = []
            print("\nYour Inventory:")
            for item in world.player.inventory:
                print(f"{number}) " + world.player.inventory[item].display_name)
                item_list.append(world.player.inventory[item])
                number += 1
            
            print("\nYour Equipped Items:")
            for item in world.player.equipped:
                print(f"{number}) " + world.player.equipped[item].display_name)
                item_list.append(world.player.equipped[item])
                number += 1

            print("\nA) Investigate an Item")
            print("B) Equip an Item")
            print("C) De-equip an Item")

            choice = input("Choose an option: ").upper().strip()
            if choice == "A":
                choice = input("Choose an item to search(by number as listed above): ")
                try: 
                    choice = int(choice) - 1
                    if choice < 0 or choice >= len(item_list):
                        print("\nInvalid item.\n")
                        continue
                    print("\n" + item_list[choice].description)
                except ValueError:
                    print("\nInvalid item.\n")
                    continue
            elif choice == "B":
                choice = input("Choose an item to equip(by number as listed above): ")
                try: 
                    choice = int(choice) - 1
                    if choice < 0 or choice >= len(item_list):
                        print("\nInvalid item.\n")
                        continue
                    choice = item_list[choice].name
                except ValueError:
                    print("\nInvalid item.\n")
                    continue
                print(choice)
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
            elif choice == "C":
                choice = input("Choose an item to equip(by number as listed above): ")
                try: 
                    choice = int(choice) - 1
                    if choice < 0 or choice >= len(item_list):
                        print("\nInvalid item.\n")
                        continue
                    choice = item_list[choice].name
                except ValueError:
                    print("\nInvalid item.\n")
                    continue
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
            print(f"Cunning: {world.player.stealth}")
            print(f"Wit: {world.player.wit}\n")

        elif action == 5:
            with open("player.json", "w") as f:
                        json.dump(to_dict(world.player), f, indent=2)

            print("Your game has been saved. Press CTRL-D or close the window to quit.")

        elif action == 6:
            program = input("Input your program. Separate commands with \">\":")
            program = program.replace(">", "\n")
            print(program)

            tokens = tokenize(program)
            ast = Parser(tokens).parse()
            WorldInterpreter(world).run(ast)

except (KeyboardInterrupt, EOFError):
    print("\nQuitting Codebound")
