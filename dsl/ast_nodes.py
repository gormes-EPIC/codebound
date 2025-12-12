class PlusNode:
    def __init__(self, amount):
        self.amount = amount

class MinusNode:
    def __init__(self, amount):
        self.amount = amount

class TimesNode:
    def __init__(self, amount):
        self.amount = amount

class DivideNode:
    def __init__(self, amount):
        self.amount = amount

class SetNode:
    def __init__(self, amount):
        self.amount = amount

class TeleportNode:
    def __init__(self, location):
        self.location = location


class IgniteNode:
    def __init__(self, target_type, target):
        self.target = target
        self.target_type = target_type

class DrawSummoningCircleNode:
    def __init__(self, location):
        self.location = location

class SummonNode:
    def __init__(self, entity):
        self.entity = entity

class MoveSummonsNode:
    def __init__(self, direction):
        self.location = direction
        
class ReportNode:
    pass

class SaveNode:
    pass

class ProgramNode:
    def __init__(self, statements):
        self.statements = statements


