class Enemy:
    def __init__(self, name, description, hp=10, attack=5, defense=5, stealth=5, wit=5, awareness=2):
        self.name = name
        self.description = description
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.stealth = stealth
        self.wit = wit
        self.awareness = awareness

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            hp=data.get("hp", 10),
            attack=data.get("attack", 5),
            defense=data.get("defense", 5),
            stealth=data.get("stealth", 5),
            wit=data.get("wit", 5),
            awareness = data.get("awareness", 2)
        )