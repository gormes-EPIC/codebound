import json
from player import Player
from room import Room
from searchable import Searchable
from item import Item
from door import Door
from enemy import Enemy



def load_player(data):
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
                searchables=r_searchables
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
                    wit=enemy_props.get("wit", 0)
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
        
    def get_value(self):
        return self.value
    
    def add(self, amount):
        self.previous = self.value
        self.value += amount
    
    def subtract(self, amount):
        self.previous = self.value
        self.value -= amount
    
    def multiply(self, amount):
        self.previous = self.value
        self.value *= amount
    
    def divide(self, amount):
        self.previous = self.value
        self.value /= amount

    def set_value(self, amount):
        self.previous = self.value
        self.value = amount

    def undo(self):
        self.value = self.previous

    def to_dict(self):
        return {"value": self.value, "previous": self.previous, "startup": self.startup}
    
    def save(self):
        with open("world.json", "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def run_startup(self):
        print(self.startup)