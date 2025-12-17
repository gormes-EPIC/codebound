from dsl.ast_nodes import ProgramNode
from dsl.ast_nodes import ReportNode
from dsl.ast_nodes import TeleportNode
from dsl.ast_nodes import IgniteNode
from dsl.ast_nodes import SummonNode
from dsl.ast_nodes import MoveSummonsNode
from dsl.ast_nodes import DrawSummoningCircleNode
from dsl.ast_nodes import RememberNode
from dsl.ast_nodes import AlertNode

class WorldInterpreter:
    def __init__(self, world):
        self.world = world

    def report(self):
        self.world.report()

    def teleport(self, location):
        self.world.teleport(location)

    def ignite(self, target_type, target):
        self.world.ignite(target_type, target)
    
    def summon(self, entity):
        self.world.summon(entity)

    def move_summons(self, direction):
        self.world.move_summons(direction)

    def draw_circle(self):
        self.world.draw_circle()

    def add_remember(self, name, value):
        self.world.add_remember(name, value)
    
    def alert(self):
        self.world.alert()

    def run(self, program_node):
        for stmt in program_node.statements:
            if isinstance(stmt, ReportNode):
                self.report()
            elif isinstance(stmt, TeleportNode):
                self.teleport(stmt.location)
            elif isinstance(stmt, IgniteNode):
                self.ignite(stmt.target_type, stmt.target)
            elif isinstance(stmt, SummonNode):
                self.summon(stmt.entity)
            elif isinstance(stmt, MoveSummonsNode):
                self.move_summons(stmt.location)   
            elif isinstance(stmt, DrawSummoningCircleNode):
                self.draw_circle() 
            elif isinstance(stmt, RememberNode):
                self.add_remember(stmt.name, stmt.value)
            elif isinstance(stmt, AlertNode):
                self.alert()