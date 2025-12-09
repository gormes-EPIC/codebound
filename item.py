class Item:
    def __init__(self, name, **kwargs):
        self.name = name
        self.description = kwargs.get("description", "")
        self.attack = kwargs.get("attack", 0)
        self.defense = kwargs.get("defense", 0)
        self.stealth = kwargs.get("stealth", 0)
        self.wit = kwargs.get("wit", 0)
        self.hp = kwargs.get("hp", 0)
        self.unlock_door = kwargs.get("unlock_door", False)
        self.unlock_spellbook = kwargs.get("unlock_spellbook", False)

    def __repr__(self):
        return f"Item({self.name})"
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "attack": self.attack,
            "defense": self.defense,
            "stealth": self.stealth,
            "wit": self.wit,
            "hp": self.hp,
            "unlock_door": self.unlock_door,
            "unlock_spellbook": self.unlock_spellbook
        }