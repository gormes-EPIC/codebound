class Item:
    def __init__(self, name, **kwargs):
        self.name = name
        self.display_name = kwargs.get("display_name", name)
        self.description = kwargs.get("description", "")
        self.attack = kwargs.get("attack", 0)
        self.defense = kwargs.get("defense", 0)
        self.stealth = kwargs.get("stealth", 0)
        self.wit = kwargs.get("wit", 0)
        self.hp = kwargs.get("hp", 0)
        self.unlock_door = kwargs.get("unlock_door", False)
        self.unlock_spellbook = kwargs.get("unlock_spellbook", False)
        self.reveal_exit = kwargs.get("reveal_exit", False)
        self.flamable = kwargs.get("flamable", False)
        self.key_item = kwargs.get("key_item", False)
        self.end_condition = kwargs.get("end_condition", False)
        self.equipable = kwargs.get("equipable", False)
        self.map = kwargs.get("map", False)
        self.map_filepath = kwargs.get("map_filepath", False)

    def __repr__(self):
        return f"Item({self.name})"

    def to_dict(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "attack": self.attack,
            "defense": self.defense,
            "stealth": self.stealth,
            "wit": self.wit,
            "hp": self.hp,
            "unlock_door": self.unlock_door,
            "unlock_spellbook": self.unlock_spellbook,
            "reveal_exit": self.reveal_exit,
            "flamable": self.flamable,
            "key_item": self.key_item,
            "end_condition": self.end_condition,
            "eqiupable": self.equipable,
            "map":self.map,
            "map_filename": self.map_filepath
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            display_name=data.get("display_name", data["name"]),
            description=data.get("description", ""),
            attack=data.get("attack", 0),
            defense=data.get("defense", 0),
            stealth=data.get("stealth", 0),
            wit=data.get("wit", 0),
            hp=data.get("hp", 0),
            unlock_door=data.get("unlock_door", False),
            unlock_spellbook=data.get("unlock_spellbook", False),
            reveal_exit=data.get("reveal_exit", False),
            flamable=data.get("flamable", False),
            key_item=data.get("key_item", False),
            end_condition=data.get("end_condition", False),
            equipable=data.get("equipable", False),
            map=data.get("map",False),
            map_filepath=data.get("map_filepath", False)
        )
