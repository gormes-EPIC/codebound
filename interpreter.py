from ast_nodes import PlusNode
from ast_nodes import MinusNode
from ast_nodes import TimesNode
from ast_nodes import DivideNode
from ast_nodes import ProgramNode
from ast_nodes import ReportNode
from ast_nodes import SaveNode
from ast_nodes import SetNode
from ast_nodes import UndoNode
from ast_nodes import TeleportNode

class WorldInterpreter:
    def __init__(self, world):
        self.world = world

    def add_amount(self, amount):
        self.world.add(amount)
        
    def subtract_amount(self, amount):
        self.world.subtract(amount)

    def multiply_amount(self, amount):
        self.world.multiply(amount)

    def divide_amount(self, amount):
        self.world.divide(amount)
    
    def set_amount(self, amount):
        self.world.set_value(amount)

    def report(self):
        value = self.world.get_value()
        print(f"Value is {value}")

    def save(self):
        self.world.save()
    
    def undo(self):
        self.world.undo()

    def teleport(self, location):
        print("executing teleport")
        if location.lower() in self.world.rooms:
            self.world.current_room = self.world.rooms[location]
            print(f"Teleported to {location}.")
        elif location.lower() == "home":
            self.world.current_room = self.world.rooms[self.world.start_room]
            print(f"Teleported home to {self.world.start_room}.")
        else:
            print(f"Location '{location}' does not exist.")

    def run(self, program_node):
        for stmt in program_node.statements:
            if isinstance(stmt, PlusNode):
                self.add_amount(stmt.amount)
            elif isinstance(stmt, MinusNode):
                self.subtract_amount(stmt.amount)
            elif isinstance(stmt, TimesNode):
                self.multiply_amount(stmt.amount)
            elif isinstance(stmt, DivideNode):
                self.divide_amount(stmt.amount)
            elif isinstance(stmt, SetNode):
                self.set_amount(stmt.amount)
            elif isinstance(stmt, ReportNode):
                self.report()
            elif isinstance(stmt, SaveNode):
                self.save()
            elif isinstance(stmt, UndoNode):
                self.undo()
            elif isinstance(stmt, TeleportNode):
                self.teleport(stmt.location)