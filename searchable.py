class Searchable:
    def __init__(self, name, items):
        self.name = name
        self.items = items  # list of Item objects

    def __repr__(self):
        return f"Searchable({self.name}, items={self.items})"