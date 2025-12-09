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

class UndoNode:
    pass

class ReportNode:
    pass

class SaveNode:
    pass

class ProgramNode:
    def __init__(self, statements):
        self.statements = statements


