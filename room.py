class Room:
    def __init__(self, name, description, exits=None, searchables=None):
        self.name = name
        self.description = description
        self.exits = exits if exits else {}  # dictionary of direction -> Room object
        self.searchables = searchables if searchables else []  # list of Searchable objects

    def __repr__(self):
        exit_names = {dir: room.name for dir, room in self.exits.items()}
        return f"Room({self.name}, exits={exit_names}, searchables={self.searchables})"
