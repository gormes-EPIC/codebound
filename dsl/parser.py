from dsl.ast_nodes import ProgramNode
from dsl.ast_nodes import ReportNode
from dsl.ast_nodes import IgniteNode
from dsl.ast_nodes import TeleportNode
from dsl.ast_nodes import SummonNode
from dsl.ast_nodes import MoveSummonsNode
from dsl.ast_nodes import DrawSummoningCircleNode
from dsl.ast_nodes import RememberNode
from dsl.ast_nodes import AlertNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, type=None):
        tok = self.tokens[self.pos]
        if type and tok.type != type:
            raise SyntaxError(f"Expected {type}, got {tok.type}")
        self.pos += 1
        return tok

    def parse(self):
        statements = []

        while self.peek().type != "EOF":
            tok = self.peek().type
            
            if tok == "TELEPORT":
                self.consume("TELEPORT")
                location = self.consume("IDENT").value
                statements.append(TeleportNode(location))
            
            elif tok == "IGNITE":
                self.consume("IGNITE")
                target_type = self.consume("IDENT").value
                target = self.consume("IDENT").value
                statements.append(IgniteNode(target_type, target))

            elif tok == "SUMMON":
                self.consume("SUMMON")
                entity = self.consume("IDENT").value
                statements.append(SummonNode(entity))
        
            elif tok == "MOVE":
                self.consume("MOVE")
                direction = self.consume("IDENT").value
                statements.append(MoveSummonsNode(direction))

            elif tok == "REPORT":
                self.consume("REPORT")
                statements.append(ReportNode())

            elif tok == "DRAW":
                self.consume("DRAW")
                circle = self.consume("IDENT").value
                statements.append(DrawSummoningCircleNode())
            
            elif tok == "REMEMBER":
                self.consume("REMEMBER")
                name = self.consume("IDENT").value
                value = self.consume("IDENT").value
                statements.append(RememberNode(name, value))

            elif tok == "ALERT":
                self.consume("ALERT")
                statements.append(AlertNode())

            else:
                raise SyntaxError(f"Unexpected token: {tok}")

        return ProgramNode(statements)