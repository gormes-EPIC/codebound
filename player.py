class Player:
    def __init__(
        self,
        name,
        hp=25,
        unlocked=None,
        inventory=None,
        equipped=None,
        attack=5,
        defense=5,
        stealth=5,
        wit=5
    ):
        self.name = name
        self.hp = hp
        self.unlocked = unlocked or {}

        # INVENTORY IS NOW A DICT:  {item_name: Item}
        self.inventory = inventory or {}

        # EQUIPPED IS NOW A DICT:  {slot_name: Item or None}
        self.equipped = equipped or {}

        self.attack = attack
        self.defense = defense
        self.stealth = stealth
        self.wit = wit

    @classmethod
    def from_dict(cls, data, item_class):
        player = cls(
            name=data["name"],
            hp=data["hp"],
            unlocked=data.get("unlocked", {}),

                # TEMP placeholders, populate after
            inventory={},
            equipped={},

            attack=data["attack"],
            defense=data["defense"],
            stealth=data["stealth"],
            wit=data["wit"]
        )

        # Load inventory dict
        inv = {}
        for name, item_data in data.get("inventory", {}).items():
            inv[name] = item_class.from_dict(item_data)
        player.inventory = inv

            # Load equipped dict
        eq = {}
        for slot, item_data in data.get("equipped", {}).items():
            eq[slot] = item_class.from_dict(item_data) if item_data else None
        player.equipped = eq

        return player