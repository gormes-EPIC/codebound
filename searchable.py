class Searchable:
    def __init__(self, name, items, flamable=False):
        self.name = name
        self.items = items  # list of Item objects
        self.flamable = flamable

    def __repr__(self):
        return f"Searchable({self.name}, items={self.items})"