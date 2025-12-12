from dsl.ast_nodes import PlusNode
from dsl.ast_nodes import MinusNode
from dsl.ast_nodes import TimesNode
from dsl.ast_nodes import DivideNode
from dsl.ast_nodes import ProgramNode
from dsl.ast_nodes import ReportNode
from dsl.ast_nodes import SaveNode
from dsl.ast_nodes import SetNode
from dsl.ast_nodes import TeleportNode
from dsl.ast_nodes import IgniteNode
from dsl.ast_nodes import SummonNode
from dsl.ast_nodes import MoveSummonsNode

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
        self.world.report()

    def save(self):
        self.world.save()
    
    def undo(self):
        self.world.undo()

    def teleport(self, location):
        self.world.teleport(location)

    def ignite(self, target_type, target):
        self.world.ignite(target_type, target)
    
    def summon(self, entity):
        self.world.summon(entity)

    def move_summons(self, direction):
        self.world.move_summons(direction)

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
            elif isinstance(stmt, TeleportNode):
                self.teleport(stmt.location)
            elif isinstance(stmt, IgniteNode):
                self.ignite(stmt.target_type, stmt.target)
            elif isinstance(stmt, SummonNode):
                self.summon(stmt.entity)
            elif isinstance(stmt, MoveSummonsNode):
                self.move_summons(stmt.location)    