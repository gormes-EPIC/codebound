class Door:
    def __init__(self, direction, room=None, flamable=False, unlocked=True, hidden=False):
        self.direction = direction
        self.room = room            # actual Room object (linked later)
        self.flamable = flamable
        self.unlocked = unlocked
        self.hidden = hidden

    def __repr__(self):
        return f"Door({self.direction} -> {self.room.name}, unlocked={self.unlocked})"
