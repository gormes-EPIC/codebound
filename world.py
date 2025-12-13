import json
from player import Player
from room import Room
from searchable import Searchable
from item import Item
from door import Door
from enemy import Enemy
from summons import Bat
from summons import Ghost
from summons import Construct



def load_player(data):
    """
    Loads the player json data into player object
    
    :param data: the Player json data
    """
    player = Player(
        name=data["name"],
        hp=data["hp"],
        attack=data["attack"],
        defense=data["defense"],
        stealth=data["stealth"],
        wit=data["wit"]
    )

    # Load inventory dict
    player.inventory = {
        name: Item.from_dict(item_data)
        for name, item_data in data.get("inventory", {}).items()
    }

    # Load equipped dict
    player.equipped = {
        slot: Item.from_dict(item_data) if item_data else None
        for slot, item_data in data.get("equipped", {}).items()
    }

    player.unlocked = data["unlocked"]

    return player



class World:

    def create_world(self, world_json):
        """
        Creates items, searchables, and rooms and links them together from world json

        :param self: World object
        :param world_json: json data storing world
        """
        # 1. Create items
        items_data = world_json.get("items", {})
        items = {name: Item(name, **props) for name, props in items_data.items()}

        # 2. Create searchables
        searchables_data = world_json.get("searchable", {})
        searchables = {}
        for s_name, s_props in searchables_data.items():
            s_items = [items[i_name] for i_name in s_props.get("items", [])]
            searchables[s_name] = Searchable(s_name, s_items)

        # 3. Create rooms WITHOUT exits first
        rooms_data = world_json.get("rooms", {})
        rooms = {}
        for r_name, r_props in rooms_data.items():
            r_searchables = [searchables[s] for s in r_props.get("searchable", [])]
            rooms[r_name] = Room(
                name=r_name,
                description=r_props.get("description", ""),
                searchables=r_searchables,
                summoning_circle=r_props.get("summoning_circle", False)
            )

        # 4. Now create Door objects and link room exits
        # 4. Link exits + populate enemies
        for r_name, r_props in rooms_data.items():
            room = rooms[r_name]

            # ---------- Exits ----------
            for direction, door_info in r_props.get("exits", {}).items():
                door = Door(
                    direction=direction,
                    flamable=door_info.get("flamable", False),
                    unlocked=door_info.get("unlocked", True),
                    hidden=door_info.get("hidden", False)
                )
                door.room = rooms[door_info["room_id"]]
                room.exits[direction] = door

            # ---------- Enemies ----------
            for enemy_name, enemy_props in r_props.get("enemies", {}).items():
                room.enemies[enemy_name] = Enemy(
                    name=enemy_name,
                    description=enemy_props.get("description", ""),
                    hp=enemy_props.get("hp", 0),
                    attack=enemy_props.get("attack", 0),
                    defense=enemy_props.get("defense", 0),
                    stealth=enemy_props.get("stealth", 0),
                    wit=enemy_props.get("wit", 0),
                    awareness=enemy_props.get("awareness",0)
                )
            room.combat_init_text = r_props.get("combat_init_text", "")


        return items, searchables, rooms


    def __init__(self, filename): 
        
        with open(filename) as f:
            data = json.load(f)
        
        self.value = data["value"]
        self.previous = self.value
        self.startup = data["startup_text"]

        items, searchables, rooms = self.create_world(data)

        self.items = items
        self.searchables = searchables
        self.rooms = rooms

        self.start_room = data["start_room"]
        self.current_room = rooms[data["start_room"]]

        with open("player.json", "r") as f:
            player_data = json.load(f)

        self.player = load_player(player_data)

        self.game_won = False

        self.summons = None

        self.summoning_circle = None


    def teleport(self, location):
        if location.lower() in self.rooms:
            self.current_room = self.rooms[location]
            print(f"Teleported to {location}.")
        elif location.lower() == "home":
            self.current_room = self.rooms[self.start_room]
            print(f"Teleported home to {self.start_room}.")
        elif location.lower() == "circle":
            self.current_room = self.summoning_circle
            print(f"Teleported to {self.current_room.name} using the summoning circle.")
        else:
            print(f"Location '{location}' does not exist.")

    def ignite(self, target_type, target):
        if target_type.lower() == "item":
            if target in self.player.inventory or target in self.player.equipped:
                item = self.items[target]
                if item.flamable:
                    print(f"You ignite the {target}.")
                else:
                    print(f"The {target} cannot be ignited.")
            else:
                print(f"Item '{target}' does not exist.")
        elif target_type.lower() == "door":
            room = self.current_room
            if target in room.exits:
                door = room.exits[target]
                if door.flamable:
                    door.unlocked = True
                    print(f"You ignite the {target} door.")
                else:
                    print(f"The {target} door cannot be ignited.")
        else:
            print(f"Target type '{target_type}' is not recognized for ignite.")

    def summon(self, entity):
        entity_lower = entity.lower()
        if entity_lower == "bat":
            self.summons = Bat("summons", self.current_room)
        elif entity_lower == "ghost":
            self.summons = Ghost("summons", self.current_room)
        elif entity_lower == "construct":
            self.summons = Construct("summons", self.current_room)
        else:
            print(f"Entity '{entity}' cannot be summoned.")

    def move_summons(self, direction):
        if self.summons:
            self.summons.move(direction, self)
        else:
            print("No summons to move.")
        
    def report(self):
        if self.summons.current_room == self.current_room:
            print("Report:\n" + self.summons.report)
        else:
            print(f"Your summons is not here with you.")
            print("\nYou cannot read its report from here.")

    def draw_circle(self):
        room = self.current_room
        if self.summoning_circle:
            self.summoning_circle.summoning_circle = False
        self.summoning_circle = room
        if room.summoning_circle == False:
            room.summoning_circle = True
            print(f"You drew a summoning circle in {room.name}")



    def save(self):
        with open("world.json", "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def run_startup(self):
        print(self.startup)