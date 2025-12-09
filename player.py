class Player:
    def __init__(self, name, hp, unlocked, inventory, equiped, attack, defense, stealth, wit):
        self.name = name
        self.hp = hp
        self.unlocked = unlocked

        self.inventory = inventory
        self.equiped = equiped
        
        self.attack = attack
        self.defense = defense 
        self.stealth = stealth
        self.wit = wit