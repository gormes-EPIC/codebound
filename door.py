class Door:
    def __init__(self, direction, room=None, flamable=False, unlocked=True):
        self.direction = direction
        self.room = room            # actual Room object (linked later)
        self.flamable = flamable
        self.unlocked = unlocked

    def __repr__(self):
        return f"Door({self.direction} -> {self.room.name}, unlocked={self.unlocked})"
