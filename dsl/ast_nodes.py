class TeleportNode:
    def __init__(self, location):
        self.location = location

class IgniteNode:
    def __init__(self, target_type, target):
        self.target = target
        self.target_type = target_type

class DrawSummoningCircleNode:
    pass

class SummonNode:
    def __init__(self, entity):
        self.entity = entity

class MoveSummonsNode:
    def __init__(self, direction):
        self.location = direction

class RememberNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class AlertNode:
    pass

class ReportNode:
    pass

class ProgramNode:
    def __init__(self, statements):
        self.statements = statements


